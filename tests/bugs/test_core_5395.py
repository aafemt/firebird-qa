#coding:utf-8
#
# id:           bugs.core_5395
# title:        Invalid data type for negation (minus operator)
# decription:   
#                   Confirmed on:
#                       WI-V3.0.4.33053, WI-T4.0.0.1249
#                       Statement failed, SQLSTATE = 42000
#               
#                   Checked on:
#                       3.0.5.33084: OK, 1.250s.
#                       4.0.0.1340: OK, 2.344s.
#                   -- works fine both when SQL dialect = 1 and 3.
#                 
# tracker_id:   CORE-5395
# min_versions: ['3.0.5']
# versions:     3.0.5
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 3.0.5
# resources: None

substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """
    set  list on;
    set term ^;
    execute block returns (eval_result int) as 
    begin 
        for 
            execute statement ('select 1 from rdb$database where 1 = - :id') (id := -1) 
        into :eval_result 
        do 
            suspend; 

        -- Statement failed, SQLSTATE = 42000
        -- Dynamic SQL Error
        -- -expression evaluation not supported
        -- -Invalid data type for negation (minus operator)
        -- -At block line: 3, col: 5

    end
    ^

    execute block returns (eval_result int) as 
    begin 
        for 
            execute statement ('select 1 from rdb$database where 1 = (:id) * -1') (id := -1) 
        into :eval_result 
        do 
            suspend; 

        -- Statement failed, SQLSTATE = 42000
        -- Dynamic SQL Error
        -- -expression evaluation not supported
        -- -Invalid data type for multiplication in dialect N, N=1 or 3
        -- -At block line: 13, col: 3

    end
    ^

    execute block returns (eval_result int) as 
       declare selected_year int;
       declare selected_mont int;
    begin 
        selected_year = extract(year from current_timestamp);
        selected_mont = extract(month from current_timestamp);

        for 
            execute statement ('select 1 from rdb$database where extract(year from current_timestamp)*100 + extract(month from current_timestamp) = ? * 100 + ? ') (selected_year, selected_mont)
        into :eval_result 
        do 
            suspend; 

        -- Statement failed, SQLSTATE = 42000
        -- Dynamic SQL Error
        -- -expression evaluation not supported
        -- -Invalid data type for multiplication in dialect N, N=1 or 3
        -- -At block line: 8, col: 5

    end
    ^
    set term ;^
  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    EVAL_RESULT                     1
    EVAL_RESULT                     1
    EVAL_RESULT                     1
  """

@pytest.mark.version('>=3.0.5')
def test_core_5395_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_expected_stdout == act_1.clean_stdout

