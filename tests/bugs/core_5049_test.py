#coding:utf-8

"""
ID:          issue-5336
ISSUE:       5336
TITLE:       Regression: incorrect calculation of byte-length for view columns
DESCRIPTION:
JIRA:        CORE-5049
"""

import pytest
from firebird.qa import *

db = db_factory(charset='UTF8')

test_script = """
    -- Confirmed:
    -- 1) FAULT on WI-V3.0.0.32208.
    -- 2) SUCCESS on LI-V3.0.0.32233, Rev: 62699.
    create or alter view v_test as
    select
       cast(rdb$character_set_name as varchar(2000)) as test_f01
      ,cast(rdb$character_set_name as varchar(2000)) as test_f02
      ,cast(rdb$character_set_name as varchar(2000)) as test_f03
    from
      rdb$database
    rows 1;

    set sqlda_display on;
    set list on;
    select * from v_test;
"""

act = isql_act('db', test_script, substitutions=[('^((?!sqltype).)*$', ''), ('[ ]+', ' '),
                                                 ('[\t]*', ' ')])

expected_stdout = """
    01: sqltype: 448 VARYING Nullable scale: 0 subtype: 0 len: 8000 charset: 4 UTF8
    02: sqltype: 448 VARYING Nullable scale: 0 subtype: 0 len: 8000 charset: 4 UTF8
    03: sqltype: 448 VARYING Nullable scale: 0 subtype: 0 len: 8000 charset: 4 UTF8
"""

@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout

