#coding:utf-8

"""
ID:          issue-7123
ISSUE:       https://github.com/FirebirdSQL/firebird/issues/7123
TITLE:       ISQL does not extract "INCREMENT BY" for IDENTITY column
DESCRIPTION:
NOTES:
    [28.02.2023] pzotov
    Confirmed bug on 4.0.1.2692.
    Checked on 5.0.0.961, 4.0.3.2903 - all OK.
"""

import pytest
from firebird.qa import *

init_script = """
    create table test(
         id1a int generated always as identity (increment by 111)
        ,id1b int generated always as identity (start with -222 increment by 222)
        ,id1c int generated always as identity (start with -333)
        ,id2a int generated by default as identity (increment by 1111)
        ,id2b int generated by default as identity (start with -2222 increment by 2222)
        ,id2c int generated by default as identity (start with -3333)
    );
    commit;
"""

db = db_factory(init = init_script)
act = python_act('db', substitutions = [('^((?!ID1(A|B|C|D)|ID2(A|B|C|D)).)*$', '')] )

expected_stdout = """
    CREATE TABLE TEST (ID1A INTEGER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT 111) NOT NULL,
    ID1B INTEGER GENERATED ALWAYS AS IDENTITY (START WITH -222 INCREMENT 222) NOT NULL,
    ID1C INTEGER GENERATED ALWAYS AS IDENTITY (START WITH -333) NOT NULL,
    ID2A INTEGER GENERATED BY DEFAULT AS IDENTITY (START WITH 1 INCREMENT 1111) NOT NULL,
    ID2B INTEGER GENERATED BY DEFAULT AS IDENTITY (START WITH -2222 INCREMENT 2222) NOT NULL,
    ID2C INTEGER GENERATED BY DEFAULT AS IDENTITY (START WITH -3333) NOT NULL);
"""
@pytest.mark.version('>=4.0.2')
def test_1(act: Action):
    # meta = act.extract_meta()
    act.expected_stdout = expected_stdout
    act.isql(switches=['-x'], charset='utf8', combine_output = True)
    assert act.clean_stdout == act.clean_expected_stdout
