#coding:utf-8
#
# id:           bugs.core_6389
# title:        Using binary string literal to assign to user-defined blob sub-types yield conversion error "filter not found to convert type 1 to type -13"
# decription:   
#                   Confirmed bug on 4.0.0.2087.
#                   Checked on 4.0.0.2170 -- all fine.
#                 
# tracker_id:   
# min_versions: ['4.0']
# versions:     4.0
# qmid:         

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 4.0
# resources: None

substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """
    recreate table blob13(id integer generated by default as identity primary key, blobfield blob sub_type -13);
    commit;
    -- This must pass w/o errors:
    insert into blob13 (blobfield) values (x'ab01'); 
  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)


@pytest.mark.version('>=4.0')
def test_1(act_1: Action):
    act_1.execute()

