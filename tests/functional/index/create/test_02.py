#coding:utf-8
#
# id:           functional.index.create.02
# title:        CREATE UNIQUE INDEX
# decription:   CREATE UNIQUE INDEX
#               
#               Dependencies:
#               CREATE DATABASE
#               CREATE TABLE
#               SHOW INDEX
# tracker_id:   
# min_versions: []
# versions:     1.0
# qmid:         functional.index.create.create_index_02

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 1.0
# resources: None

substitutions_1 = []

init_script_1 = """CREATE TABLE t( a INTEGER);
commit;
"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """CREATE UNIQUE INDEX test ON t(a);
SHOW INDEX test;"""

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """TEST UNIQUE INDEX ON T(A)
"""

@pytest.mark.version('>=1.0')
def test_02_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_expected_stdout == act_1.clean_stdout

