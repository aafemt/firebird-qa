#coding:utf-8
#
# id:           functional.gtcs.computed_fields_14
# title:        GTCS/tests/CF_ISQL_14; computed-fields-14
# decription:   
#               	Original test see in:
#                       https://github.com/FirebirdSQL/fbtcs/blob/master/GTCS/tests/CF_ISQL_14.script
#               	SQL script for creating test database ('gtcs_sp1.fbk') and fill it with some data:
#                       https://github.com/FirebirdSQL/fbtcs/blob/master/GTCS/tests/PROCS_QA_INIT_ISQL.script
#                   Checked on: 4.0.0.1803 SS; 3.0.6.33265 SS; 2.5.9.27149 SC.
#                
# tracker_id:   
# min_versions: ['2.5.0']
# versions:     2.5
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 2.5
# resources: None

substitutions_1 = [('=', ''), ('[ \t]+', ' '), ('attempted update of read-only column.*', 'attempted update of read-only column')]

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """
    set heading off;
    /*---------------------------------------------*/
    /* Create a table with computed field.         */
    /*---------------------------------------------*/
    create table t0 (a integer, af computed by (a*3));
    insert into t0(a) values(10);

    /*---------------------------------------------------------------*/
    /* Insert a value into computed-field column, which should fail. */
    /*---------------------------------------------------------------*/
    insert into t0(af) values(11);
    select 'point-1' msg, p.* from t0 p;

    /*---------------------------------------------------------------*/
    /* Update the computed-field column directly, which should fail. */
    /*---------------------------------------------------------------*/
    update t0 set af = 99 where a = 10;
    select 'point-2' msg, p.* from t0 p;

    /*---------------------------------------------------------------*/
    /* Create a table with only a computed-field should fail.        */
    /*---------------------------------------------------------------*/
    create table t5 (af computed by (1+2));

    /*-----------------------------------------------------------------*/
    /* Create a table with a computed-field, which has constant value. */
    /* Trying to insert a value in it should fail.                     */
    /*-----------------------------------------------------------------*/
    create table t6 (af int, bf computed by (1+2));
    insert into t6 values(10, 12);
  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    point-1 10 30
    point-2 10 30
  """
expected_stderr_1 = """
    Statement failed, SQLSTATE 42000
    attempted update of read-only column

    Statement failed, SQLSTATE 42000
    attempted update of read-only column

    Statement failed, SQLSTATE 42000
    unsuccessful metadata update
    -TABLE T5
    -Can't have relation with only computed fields or constraints

    Statement failed, SQLSTATE 21S01
    Dynamic SQL Error
    -SQL error code -804
    -Count of read-write columns does not equal count of values
  """

@pytest.mark.version('>=2.5')
def test_computed_fields_14_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.expected_stderr = expected_stderr_1
    act_1.execute()
    assert act_1.clean_expected_stderr == act_1.clean_stderr
    assert act_1.clean_expected_stdout == act_1.clean_stdout

