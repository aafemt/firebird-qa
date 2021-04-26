#coding:utf-8
#
# id:           bugs.core_5463
# title:        Support GENERATED ALWAYS identity columns and OVERRIDE clause
# decription:   
#                  Checked on WI-T4.0.0.546. Works fine.
#                  18.08.2020: replaced expected_stdout, checked on 4.0.0.2164.
#                
# tracker_id:   CORE-5463
# min_versions: ['4.0']
# versions:     4.0
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 4.0
# resources: None

substitutions_1 = [('OVERRIDING SYSTEM VALUE should be used.*', 'OVERRIDING SYSTEM VALUE should be used')]

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """
    set list on;
    recreate table test_always(
       id_always int generated ALWAYS as identity (start with 11 increment 22) unique
    );

    recreate table test_default(
       id_default int generated BY DEFAULT as identity (start with -11 increment -22) unique
    );


    insert into test_default default values returning id_default; -- expected: -33

    insert into test_always default values returning id_always; -- expected: 33

    -- Comments taken from doc\\sql.extensions\\README.identity_columns.txt 
    -- ==================================================================

    -- ........................................
    -- Identity columns are implicitly NOT NULL
    -- ........................................
    -- Statement failed, SQLSTATE = 42000
    -- OVERRIDING SYSTEM VALUE should be used to override the value of an identity column defined as 'GENERATED ALWAYS' in ta
    insert into test_always(id_always) values(null);

    -- Statement failed, SQLSTATE = 23000
    -- validation error for column "TEST"."id_default", value "*** null ***"
    insert into test_default(id_default) values(null);


    -- ........................................................................
    -- BY DEFAULT identity columns can be overriden in INSERT statements
    -- just specifying the value in the values list
    -- ........................................................................
    insert into test_default(id_default) values(-7654321) returning id_default;
    -- insert into test_default default values returning id_default; ==> -99 !


    -- ........................................................................
    -- However, for ALWAYS identity columns that is not allowed.
    -- To use the value passed in the INSERT statement for an ALWAYS column, you should pass 
    -- OVERRIDING SYSTEM VALUE:
    -- ........................................................................


    -- 1) check that OVERRIDING SYSTEM VALUE clause does not affect on NOT_NULL constraint:
    -- Statement failed, SQLSTATE = 23000
    -- validation error for column "test_always"."ID_ALWAYS", value "*** null ***"
    insert into test_always(id_always) overriding system value values (null) returning id_always;

    -- 2) check ability to override system value by providing our own:
    insert into test_always(id_always) overriding system value values (7654321) returning id_always;

    -- .........................................................................
    -- OVERRIDING also supports a subclause to be used with BY DEFAULT columns, 
    -- to ignore the value passed in INSERT and use the defined sequence:
    -- .........................................................................

    -- 1) check that attempt to pass NULL into VALUES list has no effect:
    insert into test_default(id_default) overriding user value values(null) returning id_default; -- expected: -99

    -- 2) check ability to pass allowed value but it also must be overriden by default one:
    insert into test_default(id_default) overriding user value values(-7654322) returning id_default; -- expected: -121
  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    ID_DEFAULT                      -11
    ID_ALWAYS                       11
    ID_DEFAULT                      -7654321
    ID_ALWAYS                       7654321
    ID_DEFAULT                      -33
    ID_DEFAULT                      -55
  """
expected_stderr_1 = """
    Statement failed, SQLSTATE = 42000
    OVERRIDING SYSTEM VALUE should be used

    Statement failed, SQLSTATE = 23000
    validation error for column "TEST_DEFAULT"."ID_DEFAULT", value "*** null ***"

    Statement failed, SQLSTATE = 23000
    validation error for column "TEST_ALWAYS"."ID_ALWAYS", value "*** null ***"
  """

@pytest.mark.version('>=4.0')
def test_core_5463_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.expected_stderr = expected_stderr_1
    act_1.execute()
    assert act_1.clean_expected_stderr == act_1.clean_stderr
    assert act_1.clean_expected_stdout == act_1.clean_stdout

