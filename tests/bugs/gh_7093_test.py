#coding:utf-8

"""
ID:          issue-7093
ISSUE:       https://github.com/FirebirdSQL/firebird/issues/7093
TITLE:       Improve indexed lookup speed of strings when the last keys characters are part of collated contractions
DESCRIPTION:
    We create table TBENCH and save in it duration of every executed sttaement from list described in the ticket.
    Then we query this table and check whether ratio between maximal and minimal duration values more than 100.
    If no (expected) then no output must be from this table.
    Otherwise all statements will be displayed and this means that we have a problem with performance.
NOTES:
    [15.08.2023] pzotov
    Currently test passed only for FB 5.x.
    FB 4.x still has the same problem with performance of some statements.
    FB 3.x can not execute because of "Invalid collation attributes" when
    tries to run: CREATE COLLATION UNICODE_CSCZ_CI.
    Sent report to Adriano, waiting for reply.

    Checked on 5.0.0.1163 (passed), 4.0.4.2978 (failed), 3.0.12.33707 (error).
"""

import pytest
from firebird.qa import *

db = db_factory(async_write = True)

test_script = """
    create collation UNICODE_CSCZ_CI
       for UTF8  
       from UNICODE  
       case insensitive  
       'LOCALE=cs_CZ'
    ;
       
    create collation UNICODE_CSCZ_CS
       for UTF8  
       from UNICODE  
       case sensitive  
       'LOCALE=cs_CZ'
    ;

    CREATE TABLE TEST1M (
      ANSI_CZ VARCHAR(10)  CHARACTER SET WIN1250 COLLATE PXW_CSY,
      UNICODE_CS_CZ VARCHAR(10)  CHARACTER SET UTF8 COLLATE UNICODE_CSCZ_CS,
      UNICODE_CI_CZ VARCHAR(10) CHARACTER SET UTF8 COLLATE UNICODE_CSCZ_CI,
      UNICODE_CS VARCHAR(10) CHARACTER SET UTF8,
      UNICODE_CI VARCHAR(10) CHARACTER SET UTF8 COLLATE UNICODE_CI
    );

    recreate table tbench(
      measure_id int generated by default as identity constraint tbench_pk primary key
      ,sttm varchar(128)
      ,elap_ms int not null
    );

    set term ^;
    CREATE OR ALTER PROCEDURE GetStr(AORDERID BIGINT)
    RETURNS (AResult CHAR(10)) AS
    declare variable Base36Chars CHAR(36);
    declare variable mResult VARCHAR(10);
    declare variable ID BIGINT;
    declare variable I INT;
    BEGIN
        Base36Chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        mResult = '';
        AResult = mResult;
        ID = AORDERID;
        WHILE (ID > 0) DO
        BEGIN
          I = MOD(ID, 36);
          ID = ID / 36;
          mResult = mResult || SubString(Base36Chars from I + 1 for 1);
        END
        AResult = LEFT(mResult || '0000000', 7);
      Suspend;
    END
    ^

    -- Generate test string data
    -- 000000, 100000...900000...A00000...Z00000,
    -- 010000, 110000...910000...A10000...Z10000,
    -- ...

    EXECUTE BLOCK
    AS
      --DECLARE ROWSCOUNT INT = 1000000;
      DECLARE ROWSCOUNT INT = 100000;
      DECLARE I INT = 0;
      DECLARE C INT = 0;
      DECLARE Str VARCHAR(10);
    BEGIN
      WHILE (C < ROWSCOUNT) DO
      BEGIN
        SELECT AResult from GetStr(:I) into :Str;
        -- Skip Y, Z
        IF ((LEFT(Str, 1) <> 'Y') AND (LEFT(Str, 1) <> 'Z')) THEN BEGIN
          INSERT INTO TEST1M(ANSI_CZ, UNICODE_CS_CZ, UNICODE_CI_CZ, UNICODE_CS, UNICODE_CI) VALUES (:Str, :Str, :Str, :Str, :Str);
          C = C + 1;
        END
        I = I + 1;
      END
    END
    ^
    set term ;^
    commit;

    CREATE INDEX TEST1M_ANSI_CZ ON TEST1M (ANSI_CZ);
    CREATE INDEX TEST1M_UNICODE_CS_CZ ON TEST1M (UNICODE_CS_CZ);
    CREATE INDEX TEST1M_UNICODE_CI_CZ ON TEST1M (UNICODE_CI_CZ);
    CREATE INDEX TEST1M_UNICODE_CS ON TEST1M (UNICODE_CS);
    CREATE INDEX TEST1M_UNICODE_CI ON TEST1M (UNICODE_CI);
    commit;

    --######################################### Scenario use WHERE >= #########################################

    set term ^;
    execute block as
        declare v_sttm type of column tbench.sttm;
        declare procedure sp_exec_sttm(v_sttm type of column tbench.sttm) as
            declare t0 timestamp;
            declare c int;
        begin
            t0 = 'now';
            execute statement 'select count(*) from (' || v_sttm || ')' into c;
            insert into tbench(sttm, elap_ms) values(:v_sttm, maxvalue(1,datediff(millisecond from :t0 to cast('now' as timestamp))));
        end
    begin

        v_sttm = q'{SELECT ANSI_CZ FROM TEST1M WHERE ANSI_CZ >= 'Z' ORDER BY ANSI_CZ}';
        execute procedure sp_exec_sttm(v_sttm);
        ---------------------------------------
        v_sttm = q'{SELECT UNICODE_CS FROM TEST1M WHERE UNICODE_CS >= 'Z' ORDER BY UNICODE_CS}';
        execute procedure sp_exec_sttm(v_sttm);
        ---------------------------------------
        v_sttm = q'{SELECT UNICODE_CI FROM TEST1M WHERE UNICODE_CI >= 'Z' ORDER BY UNICODE_CI}';
        execute procedure sp_exec_sttm(v_sttm);
        ---------------------------------------
        v_sttm = q'{SELECT UNICODE_CS_CZ FROM TEST1M WHERE UNICODE_CS_CZ >= 'Z' ORDER BY UNICODE_CS_CZ}';
        execute procedure sp_exec_sttm(v_sttm);
        ---------------------------------------
        v_sttm = q'{SELECT UNICODE_CI_CZ FROM TEST1M WHERE UNICODE_CI_CZ >= 'Z' ORDER BY UNICODE_CI_CZ}'; -- was: ~4.29s
        execute procedure sp_exec_sttm(v_sttm);
        ---------------------------------------

        v_sttm = q'{SELECT UNICODE_CI_CZ FROM TEST1M WHERE UNICODE_CI_CZ >= 'Y' ORDER BY UNICODE_CI_CZ}';
        execute procedure sp_exec_sttm(v_sttm);
        ---------------------------------------
        v_sttm = q'{SELECT FIRST 1 UNICODE_CI_CZ FROM TEST1M WHERE UNICODE_CI_CZ >= 'C' ORDER BY UNICODE_CI_CZ}'; -- was: ~1.53s
        execute procedure sp_exec_sttm(v_sttm);
        ---------------------------------------
        v_sttm = q'{SELECT FIRST 1 UNICODE_CI_CZ FROM TEST1M WHERE UNICODE_CI_CZ >= 'D' ORDER BY UNICODE_CI_CZ}';
        execute procedure sp_exec_sttm(v_sttm);
        ---------------------------------------


        v_sttm = q'{SELECT ANSI_CZ FROM TEST1M WHERE ANSI_CZ LIKE 'Z%' ORDER BY ANSI_CZ}';
        execute procedure sp_exec_sttm(v_sttm);
        ---------------------------------------
        v_sttm = q'{SELECT UNICODE_CS FROM TEST1M WHERE UNICODE_CS LIKE 'Z%' ORDER BY UNICODE_CS}';
        execute procedure sp_exec_sttm(v_sttm);
        ---------------------------------------
        v_sttm = q'{SELECT UNICODE_CI FROM TEST1M WHERE UNICODE_CI LIKE 'Z%' ORDER BY UNICODE_CI}';
        execute procedure sp_exec_sttm(v_sttm);
        ---------------------------------------
        v_sttm = q'{SELECT UNICODE_CS_CZ FROM TEST1M WHERE UNICODE_CS_CZ LIKE 'Z%' ORDER BY UNICODE_CS_CZ}'; -- was: ~4.25s
        execute procedure sp_exec_sttm(v_sttm);
        ---------------------------------------
        v_sttm = q'{SELECT UNICODE_CS_CZ FROM TEST1M WHERE UNICODE_CS_CZ LIKE 'Y%' ORDER BY UNICODE_CS_CZ}';
        execute procedure sp_exec_sttm(v_sttm);
        ---------------------------------------
        v_sttm = q'{SELECT UNICODE_CI_CZ FROM TEST1M WHERE UNICODE_CI_CZ LIKE 'Z%' ORDER BY UNICODE_CI_CZ}'; -- was: ~ 4.52s
        execute procedure sp_exec_sttm(v_sttm);
        ---------------------------------------
        v_sttm = q'{SELECT UNICODE_CI_CZ FROM TEST1M WHERE UNICODE_CI_CZ LIKE 'Y%' ORDER BY UNICODE_CI_CZ}';
        execute procedure sp_exec_sttm(v_sttm);
        ---------------------------------------
        v_sttm = q'{SELECT FIRST 1 UNICODE_CI_CZ FROM TEST1M WHERE UNICODE_CI_CZ like 'C%' ORDER BY UNICODE_CI_CZ}'; -- was: ~1.53s
        execute procedure sp_exec_sttm(v_sttm);
        ---------------------------------------
        v_sttm = q'{SELECT FIRST 1 UNICODE_CI_CZ FROM TEST1M WHERE UNICODE_CI_CZ like 'D%' ORDER BY UNICODE_CI_CZ}';
        execute procedure sp_exec_sttm(v_sttm);
        ---------------------------------------



        v_sttm = q'{SELECT ANSI_CZ FROM TEST1M WHERE ANSI_CZ similar to 'Z%' ORDER BY ANSI_CZ}';
        execute procedure sp_exec_sttm(v_sttm);
        ---------------------------------------
        v_sttm = q'{SELECT UNICODE_CS FROM TEST1M WHERE UNICODE_CS similar to 'Z%' ORDER BY UNICODE_CS}';
        execute procedure sp_exec_sttm(v_sttm);
        ---------------------------------------
        v_sttm = q'{SELECT UNICODE_CI FROM TEST1M WHERE UNICODE_CI similar to 'Z%' ORDER BY UNICODE_CI}';
        execute procedure sp_exec_sttm(v_sttm);
        ---------------------------------------
        v_sttm = q'{SELECT UNICODE_CS_CZ FROM TEST1M WHERE UNICODE_CS_CZ similar to 'Z%' ORDER BY UNICODE_CS_CZ}'; -- was: ~4.25s
        execute procedure sp_exec_sttm(v_sttm);
        ---------------------------------------
        v_sttm = q'{SELECT UNICODE_CS_CZ FROM TEST1M WHERE UNICODE_CS_CZ similar to 'Y%' ORDER BY UNICODE_CS_CZ}';
        execute procedure sp_exec_sttm(v_sttm);
        ---------------------------------------
        v_sttm = q'{SELECT UNICODE_CI_CZ FROM TEST1M WHERE UNICODE_CI_CZ similar to 'Z%' ORDER BY UNICODE_CI_CZ}'; -- was: ~ 4.52s
        execute procedure sp_exec_sttm(v_sttm);
        ---------------------------------------
        v_sttm = q'{SELECT UNICODE_CI_CZ FROM TEST1M WHERE UNICODE_CI_CZ similar to 'Y%' ORDER BY UNICODE_CI_CZ}';
        execute procedure sp_exec_sttm(v_sttm);
        ---------------------------------------
        v_sttm = q'{SELECT FIRST 1 UNICODE_CI_CZ FROM TEST1M WHERE UNICODE_CI_CZ similar to 'C%' ORDER BY UNICODE_CI_CZ}'; -- was: ~1.53s
        execute procedure sp_exec_sttm(v_sttm);
        ---------------------------------------
        v_sttm = q'{SELECT FIRST 1 UNICODE_CI_CZ FROM TEST1M WHERE UNICODE_CI_CZ similar to 'D%' ORDER BY UNICODE_CI_CZ}';
        execute procedure sp_exec_sttm(v_sttm);
        ---------------------------------------



        v_sttm = q'{SELECT ANSI_CZ FROM TEST1M WHERE ANSI_CZ starting with 'Z' ORDER BY ANSI_CZ}';
        execute procedure sp_exec_sttm(v_sttm);
        ---------------------------------------
        v_sttm = q'{SELECT UNICODE_CS FROM TEST1M WHERE UNICODE_CS starting with 'Z' ORDER BY UNICODE_CS}';
        execute procedure sp_exec_sttm(v_sttm);
        ---------------------------------------
        v_sttm = q'{SELECT UNICODE_CI FROM TEST1M WHERE UNICODE_CI starting with 'Z' ORDER BY UNICODE_CI}';
        execute procedure sp_exec_sttm(v_sttm);
        ---------------------------------------
        v_sttm = q'{SELECT UNICODE_CS_CZ FROM TEST1M WHERE UNICODE_CS_CZ starting with 'Z' ORDER BY UNICODE_CS_CZ}';
        execute procedure sp_exec_sttm(v_sttm);
        ---------------------------------------
        v_sttm = q'{SELECT UNICODE_CS_CZ FROM TEST1M WHERE UNICODE_CS_CZ starting with 'Y' ORDER BY UNICODE_CS_CZ}';
        execute procedure sp_exec_sttm(v_sttm);
        ---------------------------------------
        v_sttm = q'{SELECT UNICODE_CI_CZ FROM TEST1M WHERE UNICODE_CI_CZ starting with 'Z' ORDER BY UNICODE_CI_CZ}';
        execute procedure sp_exec_sttm(v_sttm);
        ---------------------------------------
        v_sttm = q'{SELECT UNICODE_CI_CZ FROM TEST1M WHERE UNICODE_CI_CZ starting with 'Y' ORDER BY UNICODE_CI_CZ}';
        execute procedure sp_exec_sttm(v_sttm);
        ---------------------------------------
        v_sttm = q'{SELECT FIRST 1 UNICODE_CI_CZ FROM TEST1M WHERE UNICODE_CI_CZ starting with 'C' ORDER BY UNICODE_CI_CZ}'; -- was: ~1.53s
        execute procedure sp_exec_sttm(v_sttm);
        ---------------------------------------
        v_sttm = q'{SELECT FIRST 1 UNICODE_CI_CZ FROM TEST1M WHERE UNICODE_CI_CZ starting with 'D' ORDER BY UNICODE_CI_CZ}';
        execute procedure sp_exec_sttm(v_sttm);
        ---------------------------------------

    end
    ^
    set term ;^

    set list on;
    set count on;

    select 'RUNNING TOO SLOW:' as msg, b.*, a.min_elap_ms, a.max_elap_ms, a.max_to_min_ratio, a.avg_elap_ms
    from tbench b
    join
    (
        select
             min(elap_ms) as min_elap_ms
            ,max(elap_ms) as max_elap_ms
            ,max(1.00 * elap_ms) / min(1.00 * elap_ms) as max_to_min_ratio
            ,avg(elap_ms) avg_elap_ms
        from tbench
    ) a
    on b.elap_ms > a.avg_elap_ms
    where a.max_to_min_ratio > 100
    --                          ^
    --                          |
    --     ###########################
    --     ###  T H R E S H O L D  ###
    --     ###########################
    ;
"""

act = isql_act('db', test_script)

expected_stdout = """
    Records affected: 0
"""

@pytest.mark.version('>=5.0.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute(combine_output = True)
    assert act.clean_stdout == act.clean_expected_stdout
