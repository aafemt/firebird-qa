#coding:utf-8
#
# id:           bugs.core_5330
# title:        Trace session leads FB 4.0 to hang after 2nd launch of trivial .sql script. Neither attach to any database nor regular restart of FB service can be done.
# decription:   
#                  Ticket issue was reproduced on trivial trace config with single line ("enabled = true").
#                  We prepare such config, launch trace session in async mode and run THREE times isql with logging its output.
#                  Then we stop trace session and open isql log - it should contain three 'packets' of table records.
#                  If FB becomes unavaliable, this (and all subsequent) test will not finish at all.
#               
#                  Checked on 4.0.0.331 (SS, SC) - works fine.
#                
# tracker_id:   CORE-5330
# min_versions: ['4.0']
# versions:     4.0
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 4.0
# resources: None

substitutions_1 = []

init_script_1 = """"""

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
#  
#  db_conn.close()
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
#  # Obtain engine version:
#  
#  txt30 = '''database =
#  {
#    enabled = true
#  }
#  '''
#  
#  f_trccfg=open( os.path.join(context['temp_directory'],'tmp_trace_5330.cfg'), 'w')
#  f_trccfg.write(txt30)
#  flush_and_close( f_trccfg )
#  
#  # Starting trace session in new child process (async.):
#  #######################################################
#  
#  f_trclog=open( os.path.join(context['temp_directory'],'tmp_trace_5330.log'), 'w')
#  f_trcerr=open( os.path.join(context['temp_directory'],'tmp_trace_5330.err'), 'w')
#  
#  
#  p_trace=Popen([context['fbsvcmgr_path'], "localhost:service_mgr",
#                 "action_trace_start",
#                  "trc_cfg", f_trccfg.name],
#                  stdout=f_trclog, 
#                  stderr=f_trcerr
#               )
#  
#  sql='''recreate table ttt(id int generated by default as identity, x int, y int);
#  commit;
#  
#  set term ^;
#  execute block as
#      declare s varchar(200) = 'insert into ttt(x, y) values(?, ?)';
#      declare n int = 3;
#  begin
#      while (n>0) do
#      begin
#        execute statement (s) (:n, :n * 2);
#        n = n - 1;
#      end
#  end
#  ^
#  set term ;^
#  commit;
#  set list on;
#  select * from ttt;
#  '''
#  
#  f_isql_cmd=open( os.path.join(context['temp_directory'],'tmp_isql_5330.sql'), 'w')
#  f_isql_cmd.write(sql)
#  flush_and_close( f_isql_cmd )
#  
#  f_isql_log=open( os.path.join(context['temp_directory'],'tmp_isql_5330.log'), 'w')
#  f_isql_err=open( os.path.join(context['temp_directory'],'tmp_isql_5330.err'), 'w')
#  
#  for i in range(3,0,-1):
#      subprocess.call([ context['isql_path'], dsn, '-i', f_isql_cmd.name], stdout=f_isql_log, stderr=subprocess.STDOUT)
#      if i > 1:
#          time.sleep(1)
#  flush_and_close( f_isql_log )
#  flush_and_close( f_isql_err )
#  
#  
#  #####################################################
#  # Getting ID of launched trace session and STOP it:
#  
#  # Save active trace session info into file for further parsing it and obtain session_id back (for stop):
#  f_trclst=open( os.path.join(context['temp_directory'],'tmp_trace_5330.lst'), 'w')
#  subprocess.call([context['fbsvcmgr_path'], "localhost:service_mgr",
#                   "action_trace_list"],
#                   stdout=f_trclst, 
#                   stderr=subprocess.STDOUT
#                 )
#  flush_and_close( f_trclst )
#  
#  trcssn=0
#  with open( f_trclst.name,'r') as f:
#      for line in f:
#          i=1
#          if 'Session ID' in line:
#              for word in line.split():
#                  if i==3:
#                      trcssn=word
#                  i=i+1
#              break
#  f.close()
#  
#  # Result: `trcssn` is ID of active trace session. Now we have to terminate it:
#  f_trclst=open(f_trclst.name,'a')
#  f_trclst.seek(0,2)
#  subprocess.call([context['fbsvcmgr_path'], "localhost:service_mgr",
#                   "action_trace_stop",
#                   "trc_id",trcssn],
#                   stdout=f_trclst, stderr=subprocess.STDOUT
#                 )
#  flush_and_close( f_trclst )
#  
#  # do NOT remove this delay: trase session can not be stopped immediatelly:
#  time.sleep(1)
#  
#  # Terminate child process of launched trace session (though it should already be killed):
#  p_trace.terminate()
#  flush_and_close( f_trclog )
#  flush_and_close( f_trcerr )
#  
#  # STDERR for ISQL (that created DB) and trace session - they both must be EMPTY:
#  #################
#  f_list=[f_isql_err, f_trcerr]
#  for i in range(len(f_list)):
#     f_name=f_list[i].name
#     if os.path.getsize(f_name) > 0:
#         with open( f_name,'r') as f:
#             for line in f:
#                 print("Unexpected STDERR, file "+f_name+": "+line)
#  
#  # STDLOG of isql:
#  #################
#  with open(f_isql_log.name,'r') as f:
#      for line in f:
#          if line.split():
#              print(line)
#  
#  # Cleanup:
#  ##########
#  time.sleep(1)
#  cleanup( (f_isql_cmd, f_isql_log, f_isql_err, f_trccfg, f_trclst, f_trcerr, f_trclog) )
#  
#    
#---
#act_1 = python_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    ID                              1
    X                               3
    Y                               6

    ID                              2
    X                               2
    Y                               4

    ID                              3
    X                               1
    Y                               2

    ID                              1
    X                               3
    Y                               6

    ID                              2
    X                               2
    Y                               4

    ID                              3
    X                               1
    Y                               2

    ID                              1
    X                               3
    Y                               6

    ID                              2
    X                               2
    Y                               4

    ID                              3
    X                               1
    Y                               2
  """

@pytest.mark.version('>=4.0')
@pytest.mark.xfail
def test_1(db_1):
    pytest.fail("Test not IMPLEMENTED")


