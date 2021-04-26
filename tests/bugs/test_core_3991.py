#coding:utf-8
#
# id:           bugs.core_3991
# title:        "attempted update of read-only column" when trying update editable view without triggers
# decription:   
#                
# tracker_id:   CORE-3991
# min_versions: ['2.5.7']
# versions:     2.5.7
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 2.5.7
# resources: None

substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """
    create or alter view v_test as select 1 id from rdb$database;
    commit;
    recreate table test_table (id int);
    create or alter view v_test as select id from test_table;
    commit;

    insert into v_test(id) values(10);
    commit;

    set count on;
    update v_test set id = 10; 
  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    Records affected: 1
  """

@pytest.mark.version('>=2.5.7')
def test_core_3991_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_expected_stdout == act_1.clean_stdout

