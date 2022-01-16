#coding:utf-8
#
# id:           bugs.core_6411
# title:        FB crashes on attempt to create table with number of fields greater than 5460
# decription:
#                   It was found that maximal number of fields with type = BIGINT that could fit in a table DDL is 8066.
#                   If this limit is exeeded then FB raises "new record size of N bytes is too big" (where N >= 65536).
#                   We use for-loop with two iterations, each of them does following:
#                       1. Create table with total number of fields = <N> (one for 'ID primary key' plus 8064 for
#                          'user-data' fields with names 'F1', 'F2', ..., 'F'<N>-1). All of them have type = BIGINT.
#                       2. DO RECONNECT // mandatory! otherwise crash can not be reproduced.
#                       3. Run UPDATE OR INSERT statement that is specified in the ticker(insert single record with ID=1).
#                       4. Run SELECT statement which calculates total sum on all 'user-data' fields.
#                   When N = 8065 then these actions must complete successfully and result of final SELECT must be displayed.
#                   When N = 8066 then we have to get exception:
#                       Statement failed, SQLSTATE = 54000
#                       unsuccessful metadata update
#                       -new record size of 65536 bytes is too big
#
#                   Confirmed bug on 4.0.0.2204: got crash when N=8065 (but still "new record size of 65536 bytes is too big" when N=8066).
#                   Checked on 3.0.7.33368, 4.0.0.2214 - all OK.
#
# tracker_id:   CORE-6411
# min_versions: ['3.0.7']
# versions:     3.0.7
# qmid:         None

import pytest
from firebird.qa import db_factory, python_act, Action

# version: 3.0.7
# resources: None

substitutions_1 = [('.*(-)?After line \\d+.*', ''), ('[ \t]+', ' ')]

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

# test_script_1
#---
# import os
#  import sys
#  import subprocess
#  import time
#
#  db_file=db_conn.database_name
#  db_conn.close()
#
#  os.environ["ISC_USER"] = user_name
#  os.environ["ISC_PASSWORD"] = user_password
#
#  #--------------------------------------------
#
#  def flush_and_close( file_handle ):
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
#      for f in f_names_list:
#         if type(f) == file:
#            del_name = f.name
#         elif type(f) == str:
#            del_name = f
#         else:
#            print('Unrecognized type of element:', f, ' - can not be treated as file.')
#            del_name = None
#
#         if del_name and os.path.isfile( del_name ):
#             os.remove( del_name )
#
#  #--------------------------------------------
#
#  subprocess.call([ context['fbsvcmgr_path'], "localhost:service_mgr",
#                    "action_properties", "prp_write_mode", "prp_wm_async",
#                    "dbname", db_file ]
#                 )
#  #--------------------------------------------
#
#  for iter in range(0,2):
#      FLD_COUNT = 8064 + iter
#
#      ddl_init = 'recreate table tdata(id bigint primary key'
#      ddl_addi = '\\n'.join( (',f%d bigint' %i for i in range(1,FLD_COUNT)) )
#      ddl_expr = ''.join( ( ddl_init, ddl_addi, ')' ) )
#
#      upd_init = 'update or insert into tdata values( 1'
#      upd_addi = '\\n'.join( ( ',' + str(i) for i in range(1,FLD_COUNT)) )
#      upd_expr = ''.join( ( upd_init, upd_addi, ') matching(id)' ) )
#
#
#      sel_init = 'select '
#      sel_addi = '+'.join( ( str(i) for i in range(0,FLD_COUNT)) )
#      sel_expr = ''.join( ( sel_init, sel_addi, ' as fields_total from tdata' ) )
#
#      sql_expr=    '''
#          set bail on;
#          %(ddl_expr)s;
#          commit;
#          connect '%(dsn)s';
#          %(upd_expr)s;
#          set list on;
#          %(sel_expr)s;
#          quit;
#      ''' % dict(globals(), **locals())
#
#      f_run_sql = open( os.path.join(context['temp_directory'],'tmp_run_6411.sql'), 'w')
#      f_run_sql.write(sql_expr)
#      f_run_sql.close()
#
#      f_run_log = open( os.path.join(context['temp_directory'],'tmp_run_6411.log'), 'w')
#
#      p_hanged_isql=subprocess.call(   [ context['isql_path'], dsn, "-i", f_run_sql.name ],
#                                        stdout = f_run_log,
#                                        stderr = subprocess.STDOUT
#                                    )
#      flush_and_close(f_run_log)
#
#      with open(f_run_log.name,'r') as f:
#          for line in f:
#              if line.strip():
#                  print('iter: %(iter)s, FLD_COUNT: %(FLD_COUNT)s, result: %(line)s' % locals())
#  #< for iter in range(0,2)
#
#  # Cleanup.
#  ##########
#  time.sleep(1)
#  cleanup( (f_run_sql, f_run_log) )
#
#
#---

act_1 = python_act('db_1', substitutions=substitutions_1)

expected_stdout_1 = """
    step: 0, FLD_COUNT: 8064, result: FIELDS_TOTAL 32510016
    step: 1, FLD_COUNT: 8065, result: Statement failed, SQLSTATE = 54000
    step: 1, FLD_COUNT: 8065, result: unsuccessful metadata update
    step: 1, FLD_COUNT: 8065, result: -new record size of 65536 bytes is too big
    step: 1, FLD_COUNT: 8065, result: -TABLE TDATA
"""

@pytest.mark.version('>=3.0.7')
def test_1(act_1: Action, capsys):
    #
    for step in range(2):
        FLD_COUNT = 8064 + step

        ddl_init = 'recreate table tdata (id bigint primary key'
        ddl_addi = '\n'.join([f',f{i} bigint' for i in range(1,FLD_COUNT)])
        ddl_expr = ''.join([ddl_init, ddl_addi, ')'])

        upd_init = 'update or insert into tdata values(1'
        upd_addi = '\n'.join( [f',{i}' for i in range(1,FLD_COUNT)])
        upd_expr = ''.join([upd_init, upd_addi, ') matching(id)'])


        sel_init = 'select '
        sel_addi = '+'.join([str(i) for i in range(0,FLD_COUNT)])
        sel_expr = ''.join([sel_init, sel_addi, ' as fields_total from tdata'])

        sql_expr=  f"""
            set bail on ;
            {ddl_expr} ;
            commit;
            connect '{act_1.db.dsn}' user {act_1.db.user} password '{act_1.db.password}' ;
            {upd_expr} ;
            set list on ;
            {sel_expr} ;
            quit ;
"""
        #
        act_1.reset()
        act_1.isql(switches=[], input=sql_expr, combine_output=True)
        for line in act_1.string_strip(act_1.stdout).splitlines():
            if line.strip():
                print(f'step: {step}, FLD_COUNT: {FLD_COUNT}, result: {line}')
    # Check
    act_1.reset()
    act_1.expected_stdout = expected_stdout_1
    act_1.stdout = capsys.readouterr().out
    assert act_1.clean_stdout == act_1.clean_expected_stdout
