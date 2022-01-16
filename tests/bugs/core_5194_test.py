#coding:utf-8
#
# id:           bugs.core_5194
# title:         Invalid computed by definition generated by isql -x
# decription:
#                  We create table and then run ISQL with '-x' key and saving its output to file.
#                  This operation should NOT produce any error (see var. 'f_xmeta_err').
#                  Then we drop table and run ISQL again but for APPLYING extracted metadata.
#                  If "ISQL -x" will produce script with invalid syntax, compiler will raise error.
#                  Test checks that:
#                  1) table is recreated successfully and consists of the same fields as before;
#                  2) compiler STDERR (see var. 'f_apply_err') is empty.
#                  Confirmed:
#                  1) wrong metadata generation on 4.0.0.130
#                  2) works fine on 4.0.0.132, 3.0.0.32474
#
# tracker_id:   CORE-5194
# min_versions: ['3.0']
# versions:     3.0
# qmid:         None

import pytest
from firebird.qa import db_factory, python_act, Action

# version: 3.0
# resources: None

substitutions_1 = [('.* line \\d+ .*', '')]

init_script_1 = """
recreate table test(a timestamp, b computed by (current_timestamp - a));
"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

# test_script_1
#---
# import os
#  import time
#  import subprocess
#  from subprocess import Popen
#
#  os.environ["ISC_USER"] = user_name
#  os.environ["ISC_PASSWORD"] = user_password
#  db_conn.close()
#
#  #--------------------------------------------
#
#  def flush_and_close(file_handle):
#      # https://docs.python.org/2/library/os.html#os.fsync
#      # If you're starting with a Python file object f,
#      # first do f.flush(), and
#      # then do os.fsync(f.fileno()), to ensure that all internal buffers associated with f are written to disk.
#      global os
#
#      file_handle.flush()
#      if file_handle.mode not in ('r', 'rb') and file_handle.name != os.devnull:
#          # otherwise: "OSError: [Errno 9] Bad file descriptor"!
#          os.fsync(file_handle.fileno())
#      file_handle.close()
#
#  #--------------------------------------------
#
#  def cleanup( f_names_list ):
#      global os
#      for i in range(len( f_names_list )):
#         if type(f_names_list[i]) == file:
#            del_name = f_names_list[i].name
#         elif type(f_names_list[i]) == str:
#            del_name = f_names_list[i]
#         else:
#            print('Unrecognized type of element:', f_names_list[i], ' - can not be treated as file.')
#            del_name = None
#
#         if del_name and os.path.isfile( del_name ):
#             os.remove( del_name )
#
#  #--------------------------------------------
#
#
#  sql_ddl='''recreate table test( a timestamp, b computed by (current_timestamp - a) );'''
#
#  f_init_sql = open( os.path.join(context['temp_directory'],'tmp_init_5194.sql'), 'w')
#  f_init_sql.write(sql_ddl)
#  flush_and_close( f_init_sql )
#
#  f_init_log = open( os.path.join(context['temp_directory'],'tmp_init_5194.log'), 'w')
#
#  subprocess.call( [context['isql_path'], dsn, "-i", f_init_sql.name],
#                   stdout = f_init_log,
#                   stderr = subprocess.STDOUT
#                 )
#  # This file should be empty:
#  flush_and_close( f_init_log )
#
#  f_xmeta_log = open( os.path.join(context['temp_directory'],'tmp_xmeta_5194.log'), 'w')
#  f_xmeta_err = open( os.path.join(context['temp_directory'],'tmp_xmeta_5194.err'), 'w')
#
#  subprocess.call( [context['isql_path'], dsn, "-x"],
#                   stdout = f_xmeta_log,
#                   stderr = f_xmeta_err
#                 )
#
#  # This file should contain metadata - table TEST definition with its COMPUTED BY column 'B':
#  flush_and_close( f_xmeta_log )
#
#  # This file should be empty:
#  flush_and_close( f_xmeta_err )
#
#  att1 = fdb.connect(dsn=dsn.encode())
#  cur1=att1.cursor()
#  cur1.execute("drop table test")
#  att1.commit()
#  att1.close()
#
#  # This should issue "There is no table TEST in this database":
#  #runProgram('isql',[dsn, '-q','-user',user_name,'-pas',user_password],'show table test;')
#
#  f_apply_log = open( os.path.join(context['temp_directory'],'tmp_apply_5194.log'), 'w')
#  f_apply_err = open( os.path.join(context['temp_directory'],'tmp_apply_5194.err'), 'w')
#  subprocess.call( [context['isql_path'], dsn, "-i", f_xmeta_log.name],
#                   stdout = f_apply_log,
#                   stderr = f_apply_err
#                 )
#  # Both of these files should be empty:
#  flush_and_close( f_apply_log )
#  flush_and_close( f_apply_err )
#
#  # This should issue DDL of table TEST which was just created by extracted metadata:
#  table_ddl='''
#  set list on;
#  select
#      rf.rdb$field_name
#      ,ff.rdb$field_length
#      ,ff.rdb$field_scale
#      ,ff.rdb$field_type
#      ,cast(ff.rdb$computed_source as varchar(100)) as rdb$computed_source
#  from rdb$relation_fields rf
#  join rdb$fields ff on rf.rdb$field_source = ff.rdb$field_name
#  where rf.rdb$relation_name='TEST'
#  order by rdb$field_name;
#  '''
#  runProgram('isql',[dsn, '-q'],table_ddl)
#
#  # No output should be here:
#  with open( f_xmeta_err.name,'r') as f:
#      print(f.read())
#
#  # No output should be here:
#  with open( f_apply_log.name,'r') as f:
#      print(f.read())
#
#  # No output should be here:
#  with open( f_apply_err.name,'r') as f:
#      for line in f:
#          print( "APPLY_METADATA_STDERR: "+line )
#
#
#  # Cleanup
#  #########
#  time.sleep(1)
#  cleanup( (f_init_sql,f_init_log,f_xmeta_log,f_xmeta_err,f_apply_log,f_apply_err) )
#
#
#---

act_1 = python_act('db_1', substitutions=substitutions_1)

test_script = """
    set list on;
    select
        rf.rdb$field_name
        ,ff.rdb$field_length
        ,ff.rdb$field_scale
        ,ff.rdb$field_type
        ,cast(ff.rdb$computed_source as varchar(100)) as rdb$computed_source
    from rdb$relation_fields rf
    join rdb$fields ff on rf.rdb$field_source = ff.rdb$field_name
    where rf.rdb$relation_name='TEST'
    order by rdb$field_name;
"""

expected_stdout_1 = """
    RDB$FIELD_NAME                  A
    RDB$FIELD_LENGTH                8
    RDB$FIELD_SCALE                 0
    RDB$FIELD_TYPE                  35
    RDB$COMPUTED_SOURCE             <null>
    RDB$FIELD_NAME                  B
    RDB$FIELD_LENGTH                8
    RDB$FIELD_SCALE                 -9
    RDB$FIELD_TYPE                  16
    RDB$COMPUTED_SOURCE             (current_timestamp - a)
"""

@pytest.mark.version('>=3.0')
def test_1(act_1: Action):
    act_1.isql(switches=['-x'])
    init_meta = act_1.stdout
    #
    with act_1.db.connect() as att1:
        cur1 = att1.cursor()
        cur1.execute("drop table test")
        att1.commit()
    #
    act_1.reset()
    act_1.isql(switches=[], input=init_meta)
    assert act_1.clean_stdout == ''
    # This should issue DDL of table TEST which was just created by extracted metadata:
    act_1.reset()
    act_1.expected_stdout = expected_stdout_1
    act_1.isql(switches=['-q'], input= test_script)
    assert act_1.clean_stdout == act_1.clean_expected_stdout
