#coding:utf-8
#
# id:           bugs.core_3008
# title:        Add attachment's CHARACTER SET name into corresponding trace records
# decription:   
#                  1. Obtain engine_version from built-in context variable.
#                  2. Make config for trace in proper format according to FB engine version,
#                     with adding invalid element 'foo' instead on boolean ('true' or 'false')
#                  3. Launch trace session in separate child process using 'FBSVCMGR action_trace_start'
#                  4. Run ISQL single 'QUIT;' command in order trace session will register connection.
#                  5. Stop trace session. Output its log with filtering only messages related to connect/disconnect event.
#               
#                  Checked on: WI-V2.5.5.26916 (SS, SC, CS); WI-V3.0.0.32008 (SS, SC, CS). Result: OK.
#                  ::: NB :::
#                  Several delays (time.sleep) added in main thread because of OS buffering. Couldn't switch this buffering off.
#                
# tracker_id:   CORE-3008
# min_versions: ['2.5.0']
# versions:     2.5
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 2.5
# resources: None

substitutions_1 = [('^((?!ERROR|ELEMENT|SYSDBA:NONE).)*$', ''), ('.*SYSDBA:NONE', 'SYSDBA:NONE'), ('TCPV.*', 'TCP')]

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

# test_script_1
#---
# import os
#  import subprocess
#  from subprocess import Popen
#  import time
#  
#  os.environ["ISC_USER"] = user_name
#  os.environ["ISC_PASSWORD"] = user_password
#  
#  
#  # Obtain engine version, 2.5 or 3.0, for make trace config in appropriate format:
#  engine=str(db_conn.engine_version)
#  db_conn.close()
#  
#  #---------------------------------------------
#  
#  def flush_and_close(file_handle):
#      # https://docs.python.org/2/library/os.html#os.fsync
#      # If you're starting with a Python file object f, 
#      # first do f.flush(), and 
#      # then do os.fsync(f.fileno()), to ensure that all internal buffers associated with f are written to disk.
#      global os
#      
#      file_handle.flush()
#      if file_handle.mode not in ('r', 'rb'):
#          # otherwise: "OSError: [Errno 9] Bad file descriptor"!
#          os.fsync(file_handle.fileno())
#      file_handle.close()
#  
#  #--------------------------------------------
#  
#  def cleanup( f_names_list ):
#      global os
#      for i in range(len( f_names_list )):
#         if os.path.isfile( f_names_list[i]):
#              os.remove( f_names_list[i] )
#              if os.path.isfile( f_names_list[i]):
#                  print('ERROR: can not remove file ' + f_names_list[i])
#  
#  #--------------------------------------------
#  
#  txt25 = '''# Trace config, format for 2.5. Generated auto, do not edit!
#  <database %[\\\\\\\\/]bugs.core_3008.fdb>
#    enabled true
#    time_threshold 0
#    log_connections true
#  </database>
#  '''
#  
#  # NOTES ABOUT TRACE CONFIG FOR 3.0:
#  # 1) Header contains `database` clause in different format vs FB 2.5: its data must be enclosed with '{' '}'
#  # 2) Name and value must be separated by EQUALITY sign ('=') in FB-3 trace.conf, otherwise we get runtime error:
#  #    element "<. . .>" have no attribute value set
#  
#  txt30 = '''# Trace config, format for 3.0. Generated auto, do not edit!
#  database=%[\\\\\\\\/]bugs.core_3008.fdb
#  {
#    enabled = true
#    time_threshold = 0
#    log_connections =  true
#  }
#  '''
#  
#  f_trccfg=open( os.path.join(context['temp_directory'],'tmp_trace_3008.cfg'), 'w')
#  if engine.startswith('2.5'):
#      f_trccfg.write(txt25)
#  else:
#      f_trccfg.write(txt30)
#  f_trccfg.close()
#  
#  #####################################################
#  # Starting trace session in new child process (async.):
#  
#  f_trclog = open( os.path.join(context['temp_directory'],'tmp_trace_3008.log'), 'w')
#  # Execute a child program in a new process, redirecting STDERR to the same target as of STDOUT:
#  p_trace=Popen([context['fbsvcmgr_path'], "localhost:service_mgr",
#                 "action_trace_start",
#                  "trc_cfg", f_trccfg.name],
#                  stdout=f_trclog, stderr=subprocess.STDOUT)
#  
#  # Wait! Trace session is initialized not instantly!
#  time.sleep(1)
#  
#  sqltxt='''quit;'''
#  
#  runProgram('isql',[dsn,'-ch','utf8'],sqltxt)
#  runProgram('isql',[dsn,'-ch','iso8859_1'],sqltxt)
#  
#  # do NOT remove this otherwise trace log can contain only message about its start before being closed!
#  time.sleep(3)
#  
#  #####################################################
#  # Getting ID of launched trace session and STOP it:
#  
#  # Save active trace session info into file for further parsing it and obtain session_id back (for stop):
#  f_trclst = open( os.path.join(context['temp_directory'],'tmp_trace_3008.lst'), 'w')
#  subprocess.call([context['fbsvcmgr_path'], "localhost:service_mgr",
#                   "action_trace_list"],
#                   stdout=f_trclst, stderr=subprocess.STDOUT
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
#  # Terminate child process of launched trace session (though it should already be killed):
#  p_trace.terminate()
#  
#  flush_and_close( f_trclog )
#  
#  
#  # Output log of trace for comparing it with expected: it must contain only TWO events: TRACE_INIT and TRACE_FINI
#  # ::: NB ::: Content if trace log is converted to UPPER case in order to reduce change of mismatching with
#  # updated trace output in some future versions:
#  with open( f_trclog.name,'r') as f:
#      print(f.read().upper())
#  
#  
#  # do NOT remove this delay otherwise get access error 'Windows 32'
#  # (The process cannot access the file because it is being used by another process):
#  time.sleep(1)
#  
#  cleanup( [i.name for i in (f_trccfg, f_trclst, f_trclog ) ] )
#  
#    
#---
#act_1 = python_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    SYSDBA:NONE, UTF8, TCP
    SYSDBA:NONE, UTF8, TCP
    SYSDBA:NONE, ISO88591, TCP
    SYSDBA:NONE, ISO88591, TCP
  """

@pytest.mark.version('>=2.5')
@pytest.mark.xfail
def test_core_3008_1(db_1):
    pytest.fail("Test not IMPLEMENTED")


