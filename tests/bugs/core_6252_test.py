#coding:utf-8

"""
ID:          issue-6495
ISSUE:       6495
TITLE:       UNIQUE / PRIMARY KEY constraint can be violated when AUTODDL = OFF and
  mixing commands for DDL and DML
DESCRIPTION:
JIRA:        CORE-6252
FBTEST:      bugs.core_6252
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
    set autoddl off; -- [ !! ]
    commit;

    recreate table test1(
        a int not null,
        b int not null
    );

    recreate table test2(
        u int not null,
        v int not null
    );

    commit;

    insert into test1(a, b) values (1,1);
    insert into test1(a, b) values (1,2);

    insert into test2(u, v) values (1,1);
    insert into test2(u, v) values (1,2);
    commit;


    -------------------------------------------------------
    update test1 set b = 1;
    alter table test1 add constraint test1_unq unique (a);
    commit;

    -------------------------------------------------------
    rollback; -- otherwise exception about PK violation will be supressed by 1st one (about test1_UNQ)
    -------------------------------------------------------

    update test2 set v = 1;
    alter table test2 add constraint test2_pk primary key (u);
    commit;

    set list on;
    select * from test1;
    select * from test2;
    rollback;

    -- We have to ensure that there are no indices that were created (before this bug fixed)
    -- for maintainace of PK/UNQ constraints:
    select
        ri.rdb$index_name idx_name
        ,ri.rdb$unique_flag idx_uniq
    from rdb$database r
    left join rdb$indices ri on
        ri.rdb$relation_name starting with 'TEST'
        and ri.rdb$system_flag is distinct from 1
    ;
"""

act = isql_act('db', test_script)

expected_stdout = """
    A                               1
    B                               1
    A                               1
    B                               2

    U                               1
    V                               1
    U                               1
    V                               1

    IDX_NAME                        <null>
    IDX_UNIQ                        <null>
"""

expected_stderr = """
    Statement failed, SQLSTATE = 23000
    violation of PRIMARY or UNIQUE KEY constraint "TEST1_UNQ" on table "TEST1"
    -Problematic key value is ("A" = 1)

    Statement failed, SQLSTATE = 23000
    violation of PRIMARY or UNIQUE KEY constraint "TEST2_PK" on table "TEST2"
    -Problematic key value is ("U" = 1)
"""

@pytest.mark.version('>=3.0.6')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.expected_stderr = expected_stderr
    act.execute()
    assert (act.clean_stderr == act.clean_expected_stderr and
            act.clean_stdout == act.clean_expected_stdout)
