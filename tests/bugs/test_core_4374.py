#coding:utf-8
#
# id:           bugs.core_4374
# title:        Truncation error when using EXECUTE STATEMENT with a blob
# decription:   
# tracker_id:   CORE-4374
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
    -- ::: NB :::
    -- Memory consumption of procedural objects under 64-bit environment is much bigger than on 32-bit one.
    -- This test was retyped because it was encountered that previous limit for the size of BLR is too weak:
    -- test failed at runtime with error "implementation limit exceeds".
    -- New (more rigorous) limit was found by using 64-bit FB, build LI-T3.0.0.31822: BLR can not be larger 
    -- than ~2.35 Mb (previous: ~3.21 Mb)

    set list on;
    set term ^;
    execute block as
    begin
      execute statement 'drop procedure test_proc';
      when any do begin end
    end
    ^
    commit
    ^
    execute block as -- returns (proc_ddl_length int) as
      declare sql blob sub_type text;
      declare single_sttm varchar(10);
    
      -- for 32 bit:
      /***********************
      declare sn int = 32760;
      declare big_block_for_incr varchar(32760);
      declare max_length_for_big_blocks int = 1048576;
      declare small_incr_amount int = 2674; -- detected maximum for 3.0 Beta2 (WI-T3.0.0.31807)
      ***********************/
      
      -- for 64 bit:
      --/*
      declare sn int = 8192;
      declare big_block_for_incr varchar(8192);
      declare max_length_for_big_blocks int = 794500;
      declare small_incr_amount int = 19;
      --*/
    begin
      sql = 'create or alter procedure test_proc returns(id integer) as '||ascii_char(10)||'begin ';
      max_length_for_big_blocks = max_length_for_big_blocks - char_length(sql || 'end');
    
      single_sttm = 'suspend;' || ascii_char(10);
      big_block_for_incr = rpad('', trunc( sn / char_length(single_sttm) ) * char_length(single_sttm), single_sttm);
    
      while (max_length_for_big_blocks > sn) do
      begin
        sql = sql || big_block_for_incr;
        max_length_for_big_blocks = max_length_for_big_blocks - char_length(big_block_for_incr);
      end
    
      sql = sql || rpad('', small_incr_amount * char_length(single_sttm), single_sttm);
      sql = sql ||'end';
    
      --proc_ddl_length = octet_length(sql);
      rdb$set_context('USER_SESSION', 'PROC_DDL_LENGTH', octet_length(sql));
      --suspend;
    
      execute statement :SQL;
    
    end 
    ^
    set term ;^
    commit;
    
    
    set term ^;
    execute block returns(returned_rows int, proc_ddl_length int, proc_src_length int, approx_blr_length int) as
    begin
      execute statement 'select count(*) cnt from test_proc' 
      into returned_rows;
    
      proc_ddl_length = cast( rdb$get_context('USER_SESSION', 'PROC_DDL_LENGTH') as int);
    
      select octet_length(rdb$procedure_source)
      from rdb$procedures where rdb$procedure_name = upper('test_proc')
      into proc_src_length;
    
      select round(octet_length(rdb$procedure_blr), -3)
      from rdb$procedures where rdb$procedure_name = upper('test_proc')
      into approx_blr_length;
    
      suspend;
    
    end
    ^
    set term ;^
    commit;

    /************************************** 
    
    32 bit, WI-T3.0.0.31824
    RETURNED_ROWS                   119154
    PROC_DDL_LENGTH                 1072455
    PROC_SRC_LENGTH                 1072395
    APPROX_BLR_LENGTH               3217000
    
    64 bit, LI-T3.0.0.31822 
    RETURNED_ROWS                   87379
    PROC_DDL_LENGTH                 786480
    PROC_SRC_LENGTH                 786420
    APPROX_BLR_LENGTH               2359000
    
    **************************************/
  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    RETURNED_ROWS                   87379
    PROC_DDL_LENGTH                 786480
    PROC_SRC_LENGTH                 786420
    APPROX_BLR_LENGTH               2359000
  """

@pytest.mark.version('>=3.0')
def test_core_4374_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_expected_stdout == act_1.clean_stdout

