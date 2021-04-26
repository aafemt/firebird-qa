#coding:utf-8
#
# id:           functional.fkey.primary.insert_pk_15
# title:        Check correct work fix with foreign key
# decription:   Check foreign key work.
#               Master transaction inserts record into master_table but DOES NOT commit.
#               Detail transaction inserts record in detail_table and tries to COMMIT.
#               Expected: referential integrity error.
# tracker_id:   
# min_versions: ['2.5']
# versions:     3.0
# qmid:         functional.fkey.primary.ins_15

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 3.0
# resources: None

substitutions_1 = [('-At block line: [\\d]+, col: [\\d]+', '-At block line')]

init_script_1 = """
    recreate table t_detl(id int);
    commit;
    recreate table t_main(
         id int constraint t_main_pk primary key using index t_main_pk
    );
    commit;
    recreate table t_detl(
        id int constraint t_detl_pk primary key using index t_detl_pk,
        master_pk_id int constraint fk_tdetl_tmain references t_main(id) using index fk_tdetl_tmain
    );
    commit;
  """

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """
    commit;
    set transaction no wait;
    set term ^;
    execute block as
    begin
        insert into t_main(id) values(1);
        in autonomous transaction do
        insert into t_detl(id, master_pk_id) values(100, 1);
    end
    ^
    set term ;^
  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stderr_1 = """
    Statement failed, SQLSTATE = 23000
    violation of FOREIGN KEY constraint "FK_TDETL_TMAIN" on table "T_DETL"
    -Foreign key reference target does not exist
    -Problematic key value is ("MASTER_PK_ID" = 1)
    -At block line: 5, col: 9
  """

@pytest.mark.version('>=3.0')
def test_insert_pk_15_1(act_1: Action):
    act_1.expected_stderr = expected_stderr_1
    act_1.execute()
    assert act_1.clean_expected_stderr == act_1.clean_stderr

