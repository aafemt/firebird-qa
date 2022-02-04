#coding:utf-8

"""
ID:          domain.create-24
FBTEST:      functional.domain.create.24
TITLE:       CREATE DOMAIN - NATIONAL CHAR VARYING
DESCRIPTION: Simple domain creation based NATIONAL CHAR VARYING datatype
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """CREATE DOMAIN test NATIONAL CHAR VARYING(32765);
SHOW DOMAIN test;"""

act = isql_act('db', test_script)

expected_stdout = """TEST                            VARCHAR(32765) CHARACTER SET ISO8859_1 Nullable"""

@pytest.mark.version('>=3')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
