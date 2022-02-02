#coding:utf-8

"""
ID:          issue-3760
ISSUE:       3760
TITLE:       Failed attempt to violate unique constraint could leave unneeded "lock conflict" error in status-vector
DESCRIPTION:
JIRA:        CORE-3394
FBTEST:      bugs.core_3394
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
    recreate table t(id int, constraint t_pk primary key(id) using index t_id);
    commit;
    SET TRANSACTION READ COMMITTED RECORD_VERSION NO WAIT;
    set term ^;
    execute block as
    begin
      insert into t values(1);
      in autonomous transaction do
      insert into t values(1);
    end
    ^
    set term ;^
    rollback;
"""

act = isql_act('db', test_script, substitutions=[('-At block line: [\\d]+, col: [\\d]+', '-At block line')])

expected_stderr = """
    Statement failed, SQLSTATE = 23000
    violation of PRIMARY or UNIQUE KEY constraint "T_PK" on table "T"
    -Problematic key value is ("ID" = 1)
    -At block line: 5, col: 7
"""

@pytest.mark.version('>=3')
def test_1(act: Action):
    act.expected_stderr = expected_stderr
    act.execute()
    assert act.clean_stderr == act.clean_expected_stderr

