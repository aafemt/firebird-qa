#coding:utf-8
#
# id:           bugs.core_0188
# title:        trigger on view with union receive nulls
# decription:   
#                  Passed on:  WI-V3.0.0.32487, WI-T4.0.0.141 -- works fine.
#                  On WI-V2.5.6.27001 issues wrong result thus min_version (for now) is 3.0.
#                
# tracker_id:   CORE-0188
# min_versions: ['3.0']
# versions:     3.0
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 3.0
# resources: None

substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """
    set bail on;
    set width ctx_name 30;
    set width ctx_val 10;

    recreate view v_ctx_data as
    select mon$variable_name as ctx_name, mon$variable_value as ctx_val 
    from mon$context_variables c
    where mon$attachment_id = current_connection or mon$transaction_id = current_transaction;

    recreate view v_test as select 1 k from rdb$database;
    commit;

    recreate table test_a (id int);
    recreate table test_b (id int);

    commit;

    recreate view v_test(id, row_from_table_b)
    as
      select id, cast(0 as int)
      from test_a a
      where not exists (select * from test_b b where b.id = a.id)

      union all

      select id, cast(1 as int)
      from test_b;

    commit;

    set term ^;
    create or alter procedure sp_zap_context_vars as
      declare ctx_ssn int;
      declare ctx_name varchar(80);
    begin
      for 
      select mon$attachment_id, mon$variable_name as ctx_name
      from mon$context_variables c
      where mon$attachment_id = current_connection or mon$transaction_id = current_transaction
      into ctx_ssn, ctx_name
      do 
      execute statement 
          'rdb$set_context(' 
          || iif(ctx_ssn is not null, '''USER_SESSION''', '''USER_TRANSACTION''')
          || ', ''' 
          || ctx_name 
          || ''', null )'
      ;
    end
    ^

    create trigger v_test_bu for v_test active before update position 0 as
      declare o int;
    begin
      rdb$set_context('USER_SESSION','trigger_sees_old_id', old.id);
      rdb$set_context('USER_SESSION','trigger_sees_old_of_b1', old.row_from_table_b);
      rdb$set_context('USER_SESSION','trigger_sees_new_id', new.id);
      rdb$set_context('USER_SESSION','trigger_sees_new_of_b', new.row_from_table_b);
      if (new.row_from_table_b = 1) then
          begin
              rdb$set_context('USER_SESSION','trigger_sees_old_of_b2', old.row_from_table_b);
              if (old.row_from_table_b = 0) then
              begin
                  rdb$set_context('USER_SESSION','trigger_sees_old_of_b3', old.row_from_table_b);
                  execute statement ( 'insert into test_b(id) values(?)') (new.id);
                  execute statement ( 'delete from test_a where id = ?' ) (new.id);
                  rdb$set_context('USER_SESSION','trigger_DID_its_job', new.id);
              end
          end
      else
          delete from test_b
          where id = old.id;
    end
    ^
    set term ;^
    commit;


    insert into test_a(id) values(1);
    commit;

    set list on;

    select * from v_test; -- will return one record based on data in table test_a 

    -- must insert row into test_b and remove row with the same id from test_a:
    execute procedure sp_zap_context_vars;
    select * from v_ctx_data;

    update v_test set row_from_table_b = 1 where id = 1;
    commit;

    set count on;
    select * from test_a;
    select * from test_b;
    select * from v_ctx_data;
  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    ID                              1
    ROW_FROM_TABLE_B                0
    Records affected: 0
    ID                              1
    Records affected: 1

    CTX_NAME                        trigger_DID_its_job
    CTX_VAL                         1

    CTX_NAME                        trigger_sees_new_id
    CTX_VAL                         1

    CTX_NAME                        trigger_sees_new_of_b
    CTX_VAL                         1

    CTX_NAME                        trigger_sees_old_id
    CTX_VAL                         1

    CTX_NAME                        trigger_sees_old_of_b1
    CTX_VAL                         0

    CTX_NAME                        trigger_sees_old_of_b2
    CTX_VAL                         0

    CTX_NAME                        trigger_sees_old_of_b3
    CTX_VAL                         0


    Records affected: 7
  """

@pytest.mark.version('>=3.0')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_expected_stdout == act_1.clean_stdout

