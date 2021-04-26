#coding:utf-8
#
# id:           bugs.core_4929
# title:        Cannot compile source with "ELSE IF ( <expr> ) THEN" statement and commands to manupulate explicit cursor inside
# decription:   
# tracker_id:   CORE-4929
# min_versions: ['3.0']
# versions:     3.0
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 3.0
# resources: None

substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(page_size=4096, sql_dialect=3, init=init_script_1)

test_script_1 = """
    set term ^;
    create or alter procedure sp_test(v smallint) returns(result int) as
    begin
        result = null;
        suspend;
    end
    ^
    set term ;^
    
    commit;
    
    set term ^;
    alter procedure sp_test(v smallint) returns(result int) as
    
      declare c1 cursor for (
         select 1 id from rdb$database
      );
    
      declare c2 cursor for (
         select 2 id from rdb$database
      );
    
    begin
    
        if ( v = 1 ) then open c1;
        else
            if ( :v = 2 ) then
                open c2;
    
        while (1=1) do
        begin
            if ( v = 1 ) then fetch c1 into result;
            else
                if ( :v = 2 ) then
                    fetch c2 into result;
    
            if (row_count = 0) then leave;
    
            suspend;
    
        end
        
        if ( v = 1 ) then close c1;
        else
            if ( :v = 2 ) then
                close c2;
    
    end
    ^
    set term ;^
    commit;
    
    set list on;
    select * from sp_test(1);
    select * from sp_test(2);

  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    RESULT                          1
    RESULT                          2
  """

@pytest.mark.version('>=3.0')
def test_core_4929_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_expected_stdout == act_1.clean_stdout

