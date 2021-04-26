#coding:utf-8
#
# id:           bugs.core_3056
# title:        Problems may happen when issuing DDL commands in the same transaction after CREATE COLLATION was issued
# decription:   
# tracker_id:   CORE-3056
# min_versions: ['3.0']
# versions:     3.0
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 3.0
# resources: None

substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(page_size=4096, sql_dialect=3, init=init_script_1)

test_script_1 = """
    -- NOTES.
    -- 1. Results are identical on: LI-T3.0.0.31827 (64 bit) and  WI-T3.0.0.31827 (32 bit).
    -- 2. Despite of ticket issue that it was fixed only in 3.0, following script works OK on also oon 2.5
    --    (tested on WI-V2.5.5.26861; differences are only in stderr).
    -- 3. ## TODO ### 
    --    Uncomment lines "--,constraint test_pk1 primary key" after CORE-4783 will be fixed, and add
    --    statement 'alter table drop constraint <PK>" before each DROP TABLE statements.

    create or alter view v_test_fields_ddl as
    select
        rf.rdb$field_name fld_name
        ,cs.rdb$character_set_name cset_name
        ,co.rdb$base_collation_name base_coll
    from rdb$relation_fields rf
    join rdb$collations co on rf.rdb$collation_id = co.rdb$collation_id
    join rdb$fields ff on rf.rdb$field_source = ff.rdb$field_name
    join rdb$character_sets cs on ff.rdb$character_set_id = cs.rdb$character_set_id
    where rf.rdb$relation_name = 'TEST'
    order by rf.rdb$field_position;
    
    /* 
    -- This works only in 3.0 and does NOT in 2.5 (rdb$collation_id present there only in rdb$relation_fields and NOT in rdb$fields):
    create or alter view v_test_fields_ddl as
    select rf.rdb$field_name fld_name, cs.rdb$character_set_name cset_name, co.rdb$base_collation_name base_coll, co.rdb$collation_attributes
    from rdb$relation_fields rf
    join rdb$fields ff on rf.rdb$field_source = ff.rdb$field_name
    join rdb$character_sets cs on ff.rdb$character_set_id = cs.rdb$character_set_id
    join rdb$collations co on ff.rdb$collation_id = co.rdb$collation_id
    where rf.rdb$relation_name = 'TEST'
    order by rf.rdb$field_position;
    */
    
    recreate table test(id int);
    commit;
    set term ^;
    execute block as
      declare stt varchar(255);
      declare c_coll cursor for -- collations
        (select rc.rdb$collation_name
           from rdb$collations rc
          where coalesce(rc.rdb$system_flag,0)=0
        );
    begin
      open c_coll; ---------------  d r o p    c o l l a t i o n s -----------------
      while (1=1) do
      begin
        fetch c_coll into stt;
        if (row_count = 0) then leave;
        stt = 'drop collation '||stt;
        execute statement (:stt);
      end
      close c_coll;
    end
    ^
    set term ;^
    drop table test;
    
    set autoddl off; -- ######### NOTE: all statements below will be run in the same Tx #########
    commit;
    
    set list on;
    
    -- This is sample from ticket:
    create collation coll_01 for utf8 from unicode no pad;
    --commit; -- (1)

    -- This statement should FAIL with error "COLLATION COLL_01 for CHARACTER SET NONE is not defined"
    -- Before this ticked was fixed, text fields are implicitly assigned with charset = UTF8:

    create table test (
      k1 varchar(3) collate coll_01,
      k2 char(1) collate coll_01,
      primary key (k1, k2)
    ); -- Result: table `test` should NOT be created!

    set count on;

    -- `select * from v_test_fields_ddl;`: must return 0 rows
    set echo on;
    select * from v_test_fields_ddl; 
    drop collation coll_01;
    set echo off;
    set count off;
    
    -- All the following statements should NOT fail:
    
    create collation coll_01 for win1251 from pxw_cyrl pad space case insensitive accent insensitive;
    create collation coll_02 for win1251 from pxw_cyrl pad space case insensitive accent insensitive;
    create collation coll_03 for win1251 from pxw_cyrl pad space case insensitive accent insensitive;
    create collation coll_04 for win1251 from pxw_cyrl pad space case insensitive accent insensitive;
    create collation coll_05 for win1251 from pxw_cyrl pad space case insensitive accent insensitive;
    create collation coll_06 for win1251 from pxw_cyrl pad space case insensitive accent insensitive;
    create collation coll_07 for win1251 from pxw_cyrl pad space case insensitive accent insensitive;
    create collation coll_08 for win1251 from pxw_cyrl pad space case insensitive accent insensitive;
    create collation coll_09 for win1251 from pxw_cyrl pad space case insensitive accent insensitive;
    create collation coll_10 for win1251 from pxw_cyrl pad space case insensitive accent insensitive;
    create collation coll_11 for win1251 from pxw_cyrl pad space case insensitive accent insensitive;
    create collation coll_12 for win1251 from pxw_cyrl pad space case insensitive accent insensitive;
    
    create table test(
      f01 varchar(2) character set win1251 collate coll_01
     ,f02 varchar(2) character set win1251 collate coll_02
     ,f03 varchar(2) character set win1251 collate coll_03
     ,f04 varchar(2) character set win1251 collate coll_04
     ,f05 varchar(2) character set win1251 collate coll_05
     ,f06 varchar(2) character set win1251 collate coll_06
     ,f07 varchar(2) character set win1251 collate coll_07
     ,f08 varchar(2) character set win1251 collate coll_08
     ,f09 varchar(2) character set win1251 collate coll_09
     ,f10 varchar(2) character set win1251 collate coll_10
     ,f11 varchar(2) character set win1251 collate coll_11
     ,f12 varchar(2) character set win1251 collate coll_12
     --,constraint test_pk1 primary key (f01, f02, f03, f04, f05, f06, f07, f08, f09, f10, f11, f12)
    );
    
    select * from v_test_fields_ddl;
    
    drop table test;
    
    drop collation coll_01;
    drop collation coll_02;
    drop collation coll_03;
    drop collation coll_04;
    drop collation coll_05;
    drop collation coll_06;
    drop collation coll_07;
    drop collation coll_08;
    drop collation coll_09;
    drop collation coll_10;
    drop collation coll_11;
    drop collation coll_12;
    
    create collation coll_01 for utf8 from unicode no pad;
    create collation coll_02 for utf8 from unicode no pad;
    create collation coll_03 for utf8 from unicode no pad;
    create collation coll_04 for utf8 from unicode no pad;
    create collation coll_05 for utf8 from unicode no pad;
    create collation coll_06 for utf8 from unicode no pad;
    create collation coll_07 for utf8 from unicode no pad;
    create collation coll_08 for utf8 from unicode no pad;
    create collation coll_09 for utf8 from unicode no pad;
    create collation coll_10 for utf8 from unicode no pad;
    create collation coll_11 for utf8 from unicode no pad;
    create collation coll_12 for utf8 from unicode no pad;
    
    create table test(
      f01 varchar(2) character set utf8 collate coll_01
     ,f02 varchar(2) character set utf8 collate coll_02
     ,f03 varchar(2) character set utf8 collate coll_03
     ,f04 varchar(2) character set utf8 collate coll_04
     ,f05 varchar(2) character set utf8 collate coll_05
     ,f06 varchar(2) character set utf8 collate coll_06
     ,f07 varchar(2) character set utf8 collate coll_07
     ,f08 varchar(2) character set utf8 collate coll_08
     ,f09 varchar(2) character set utf8 collate coll_09
     ,f10 varchar(2) character set utf8 collate coll_10
     ,f11 varchar(2) character set utf8 collate coll_11
     ,f12 varchar(2) character set utf8 collate coll_12
     --,constraint test_pk2 primary key (f01, f02, f03, f04, f05, f06, f07, f08, f09, f10, f11, f12)
    );
    
    select * from v_test_fields_ddl;
    drop table test;
    
    drop collation coll_01;
    drop collation coll_02;
    drop collation coll_03;
    drop collation coll_04;
    drop collation coll_05;
    drop collation coll_06;
    drop collation coll_07;
    drop collation coll_08;
    drop collation coll_09;
    drop collation coll_10;
    drop collation coll_11;
    drop collation coll_12;
    
    -- this was tested both on windows ans linux, should be created OK
    -- (all these collations are declared in the file 'fbintl.conf'):
    create collation coll_01 for iso8859_1 from external ('DA_DA');
    create collation coll_02 for iso8859_1 from external ('DE_DE');
    create collation coll_03 for iso8859_1 from external ('DU_NL');
    create collation coll_04 for iso8859_1 from external ('EN_UK');
    create collation coll_05 for iso8859_1 from external ('EN_US');
    create collation coll_06 for iso8859_1 from external ('ES_ES');
    create collation coll_07 for iso8859_1 from external ('ES_ES_CI_AI');
    create collation coll_08 for iso8859_1 from external ('FI_FI');
    create collation coll_09 for iso8859_1 from external ('FR_CA');
    create collation coll_10 for iso8859_1 from external ('FR_FR');
    create collation coll_11 for iso8859_1 from external ('IS_IS');
    create collation coll_12 for iso8859_1 from external ('IT_IT');
    
    create table test(
      f01 varchar(2) character set iso8859_1 collate coll_01
     ,f02 varchar(2) character set iso8859_1 collate coll_02
     ,f03 varchar(2) character set iso8859_1 collate coll_03
     ,f04 varchar(2) character set iso8859_1 collate coll_04
     ,f05 varchar(2) character set iso8859_1 collate coll_05
     ,f06 varchar(2) character set iso8859_1 collate coll_06
     ,f07 varchar(2) character set iso8859_1 collate coll_07
     ,f08 varchar(2) character set iso8859_1 collate coll_08
     ,f09 varchar(2) character set iso8859_1 collate coll_09
     ,f10 varchar(2) character set iso8859_1 collate coll_10
     ,f11 varchar(2) character set iso8859_1 collate coll_11
     ,f12 varchar(2) character set iso8859_1 collate coll_12
     --,constraint test_pk2 primary key (f01, f02, f03, f04, f05, f06, f07, f08, f09, f10, f11, f12)
    );
    
    select * from v_test_fields_ddl;
    --select current_transaction from rdb$database;
    
    rollback;
    set count on;
    -- Both selects below must return 0 rows:
    set echo on;
    select * from v_test_fields_ddl;
    select * from rdb$collations co where co.rdb$collation_name starting with 'COLL_';
  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    select * from v_test_fields_ddl;
    Records affected: 0
    drop collation coll_01;
    set echo off;
    
    FLD_NAME                        F01
    CSET_NAME                       WIN1251
    BASE_COLL                       PXW_CYRL
    
    FLD_NAME                        F02
    CSET_NAME                       WIN1251
    BASE_COLL                       PXW_CYRL
    
    FLD_NAME                        F03
    CSET_NAME                       WIN1251
    BASE_COLL                       PXW_CYRL
    
    FLD_NAME                        F04
    CSET_NAME                       WIN1251
    BASE_COLL                       PXW_CYRL
    
    FLD_NAME                        F05
    CSET_NAME                       WIN1251
    BASE_COLL                       PXW_CYRL
    
    FLD_NAME                        F06
    CSET_NAME                       WIN1251
    BASE_COLL                       PXW_CYRL
    
    FLD_NAME                        F07
    CSET_NAME                       WIN1251
    BASE_COLL                       PXW_CYRL
    
    FLD_NAME                        F08
    CSET_NAME                       WIN1251
    BASE_COLL                       PXW_CYRL
    
    FLD_NAME                        F09
    CSET_NAME                       WIN1251
    BASE_COLL                       PXW_CYRL
    
    FLD_NAME                        F10
    CSET_NAME                       WIN1251
    BASE_COLL                       PXW_CYRL
    
    FLD_NAME                        F11
    CSET_NAME                       WIN1251
    BASE_COLL                       PXW_CYRL
    
    FLD_NAME                        F12
    CSET_NAME                       WIN1251
    BASE_COLL                       PXW_CYRL
    
    
    
    FLD_NAME                        F01
    CSET_NAME                       UTF8
    BASE_COLL                       UNICODE
    
    FLD_NAME                        F02
    CSET_NAME                       UTF8
    BASE_COLL                       UNICODE
    
    FLD_NAME                        F03
    CSET_NAME                       UTF8
    BASE_COLL                       UNICODE
    
    FLD_NAME                        F04
    CSET_NAME                       UTF8
    BASE_COLL                       UNICODE
    
    FLD_NAME                        F05
    CSET_NAME                       UTF8
    BASE_COLL                       UNICODE
    
    FLD_NAME                        F06
    CSET_NAME                       UTF8
    BASE_COLL                       UNICODE
    
    FLD_NAME                        F07
    CSET_NAME                       UTF8
    BASE_COLL                       UNICODE
    
    FLD_NAME                        F08
    CSET_NAME                       UTF8
    BASE_COLL                       UNICODE
    
    FLD_NAME                        F09
    CSET_NAME                       UTF8
    BASE_COLL                       UNICODE
    
    FLD_NAME                        F10
    CSET_NAME                       UTF8
    BASE_COLL                       UNICODE
    
    FLD_NAME                        F11
    CSET_NAME                       UTF8
    BASE_COLL                       UNICODE
    
    FLD_NAME                        F12
    CSET_NAME                       UTF8
    BASE_COLL                       UNICODE
    
    
    
    FLD_NAME                        F01
    CSET_NAME                       ISO8859_1
    BASE_COLL                       DA_DA
    
    FLD_NAME                        F02
    CSET_NAME                       ISO8859_1
    BASE_COLL                       DE_DE
    
    FLD_NAME                        F03
    CSET_NAME                       ISO8859_1
    BASE_COLL                       DU_NL
    
    FLD_NAME                        F04
    CSET_NAME                       ISO8859_1
    BASE_COLL                       EN_UK
    
    FLD_NAME                        F05
    CSET_NAME                       ISO8859_1
    BASE_COLL                       EN_US
    
    FLD_NAME                        F06
    CSET_NAME                       ISO8859_1
    BASE_COLL                       ES_ES
    
    FLD_NAME                        F07
    CSET_NAME                       ISO8859_1
    BASE_COLL                       ES_ES_CI_AI
    
    FLD_NAME                        F08
    CSET_NAME                       ISO8859_1
    BASE_COLL                       FI_FI
    
    FLD_NAME                        F09
    CSET_NAME                       ISO8859_1
    BASE_COLL                       FR_CA
    
    FLD_NAME                        F10
    CSET_NAME                       ISO8859_1
    BASE_COLL                       FR_FR
    
    FLD_NAME                        F11
    CSET_NAME                       ISO8859_1
    BASE_COLL                       IS_IS
    
    FLD_NAME                        F12
    CSET_NAME                       ISO8859_1
    BASE_COLL                       IT_IT
    
    
    select * from v_test_fields_ddl;
    Records affected: 0
    select * from rdb$collations co where co.rdb$collation_name starting with 'COLL_';
    Records affected: 0
  """
expected_stderr_1 = """
    Statement failed, SQLSTATE = 22021
    unsuccessful metadata update
    -CREATE TABLE TEST failed
    -Dynamic SQL Error
    -SQL error code = -204
    -COLLATION COLL_01 for CHARACTER SET NONE is not defined
  """

@pytest.mark.version('>=3.0')
def test_core_3056_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.expected_stderr = expected_stderr_1
    act_1.execute()
    assert act_1.clean_expected_stderr == act_1.clean_stderr
    assert act_1.clean_expected_stdout == act_1.clean_stdout

