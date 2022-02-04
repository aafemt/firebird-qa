#coding:utf-8

"""
ID:          domain.create-10
FBTEST:      functional.domain.create.10
TITLE:       CREATE DOMAIN - TIMESTAMP ARRAY
DESCRIPTION: Array domain creation based TIMESTAMP datatype
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """CREATE DOMAIN test TIMESTAMP [1024];
SHOW DOMAIN test;"""

act = isql_act('db', test_script)

expected_stdout = """TEST                            ARRAY OF [1024]
TIMESTAMP Nullable"""

@pytest.mark.version('>=3')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
