#coding:utf-8
#
# id:           bugs.core_5754
# title:        ALTER TRIGGER check privilege for alter database instead of table
# decription:   
#                   3.0.4.32917: OK, 1.485s.
#                   4.0.0.907: OK, 1.843s.
#                
# tracker_id:   CORE-5754
# min_versions: ['3.0.4']
# versions:     3.0.4
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 3.0.4
# resources: None

substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """
    set bail on;

    create or alter user tmp$c5754 password '123';
    commit;

    recreate table test(id int);
    recreate sequence g;
    commit;

    -- GRANT ALTER ANY <OBJECT> TO [USER | ROLE] <user/role name> [WITH GRANT OPTION];
    -- DDL operations for managing triggers and indices re-use table privileges.
    grant alter any table to tmp$c5754;
    commit;

    set term ^;
    create or alter trigger test_bi for test active before insert position 0 as
    begin
       new.id = coalesce(new.id, gen_id(g, 1) );
    end
    ^
    set term ;^
    commit;

    connect '$(DSN)' user tmp$c5754 password '123';

    set term  ^;

    -- Following attempt to alter trigger will fail on 4.0.0.890 with message:
    -- Statement failed, SQLSTATE = 28000
    -- unsuccessful metadata update
    -- -ALTER TRIGGER TEST_BI failed
    -- -no permission for ALTER access to DATABASE
    alter trigger test_bi as
    begin
       -- this trigger was updated by tmp$c5754
       if ( new.id is null ) then
           new.id = gen_id(g, 1);
    end
    ^
    set term ^;
    commit;

    commit;
    connect '$(DSN)' user sysdba password 'masterkey';
    drop user tmp$c5754;
    commit;

    set list on;

    select 1 as result
    from rdb$triggers
    where rdb$trigger_name = upper('test_bi')
    and rdb$trigger_source containing 'tmp$c5754'
    ;

  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    RESULT                          1
  """

@pytest.mark.version('>=3.0.4')
def test_core_5754_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_expected_stdout == act_1.clean_stdout

