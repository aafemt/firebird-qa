#coding:utf-8

"""
ID:          issue-2487
ISSUE:       2487
TITLE:       Don't work subquery in COALESCE
DESCRIPTION:
JIRA:        CORE-2051
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
    recreate table test1(id int primary key using index test1_pk);
    commit;
    insert into test1 values(1);
    insert into test1 values(2);
    insert into test1 values(3);
    commit;

    recreate table test2(id int primary key using index test2_pk);
    commit;
    insert into test2 values(1);
    insert into test2 values(2);
    commit;

    set plan on;
    set list on;
    select coalesce((select t2.id from test2 t2 where t2.id = t1.id), 0) id2 from test1 t1 order by t1.id;
"""

act = isql_act('db', test_script)

expected_stdout = """
    PLAN (T2 INDEX (TEST2_PK))
    PLAN (T1 ORDER TEST1_PK)
    ID2                             1
    ID2                             2
    ID2                             0
"""

@pytest.mark.version('>=3')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout

