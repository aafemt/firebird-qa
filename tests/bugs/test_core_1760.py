#coding:utf-8
#
# id:           bugs.core_1760
# title:        Support hex numeric and string literals
# decription:   
#                   See doc\\sql.extensions\\README.hex_literals.txt
#               
#                   REFACTORED 27.02.2020:
#                   1) all SQL code was moved into separate file: $files_location/core_1760.sql because it is common for all major FB versions;
#                   2) added examples from https://firebirdsql.org/refdocs/langrefupd25-bigint.html (see core_1760.sql);
#                   3) added check for output datatypes (sqlda_display).
#               
#                   Checked on:
#                       4.0.0.1789 SS: 1.458s.
#                       3.0.6.33259 SS: 0.805s.
#                       2.5.9.27149 SC: 0.397s.
#                
# tracker_id:   CORE-1760
# min_versions: ['2.5.0']
# versions:     3.0
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 3.0
# resources: None

substitutions_1 = [('.*At line.*', ''), ('-Token unknown.*', '-Token unknown')]

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

# test_script_1
#---
# 
#  import os
#  import sys
#  import subprocess
#  from fdb import services
#  
#  os.environ["ISC_USER"] = user_name
#  os.environ["ISC_PASSWORD"] = user_password
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
#  #--------------------------------------------
#  
#  db_conn.close()
#  
#  sql_chk = os.path.join(context['files_location'],'core_1760.sql')
#  
#  f_sql_log = open( os.path.join(context['temp_directory'],'tmp_core_1760.log'), 'w', buffering = 0)
#  f_sql_err = open( os.path.join(context['temp_directory'],'tmp_core_1760.err'), 'w', buffering = 0)
#  
#  subprocess.call( [ context['isql_path'], dsn, '-q', '-i', sql_chk ], stdout = f_sql_log, stderr = f_sql_err)
#  
#  flush_and_close( f_sql_log )
#  flush_and_close( f_sql_err )
#  
#  for f in (f_sql_log, f_sql_err):
#      with open( f.name,'r') as g:
#          for line in g:
#              if line.strip():
#                  print( ('STDOUT: ' if f == f_sql_log else 'STDERR: ') + line )
#  
#  cleanup( (f_sql_log.name, f_sql_err.name) )
#    
#---
#act_1 = python_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    STDOUT: CONSTANT                        11 
    STDOUT: CONSTANT                        0123456789 
    STDOUT: CONSTANT                        01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789 
    STDOUT: UUID_TO_CHAR                    BA1749B5-83BF-9146-B360-F54E25FE583E 
    STDOUT: -1(a)                           -1 
    STDOUT: +15                             15 
    STDOUT: 32767                           32767 
    STDOUT: 32768                           32768 
    STDOUT: 65535                           65535 
    STDOUT: 65536(a)                        65536 
    STDOUT: 65536(b)                        65536 
    STDOUT: -2147483648                     -2147483648 
    STDOUT: +2147483648(a)                  2147483648 
    STDOUT: +2147483648(b)                  2147483648 
    STDOUT: -1(b)                           -1 
    STDOUT: +4294967295                     4294967295 
    STDOUT: +4294967296(a)                  4294967296 
    STDOUT: +4294967296(b)                  4294967296 
    STDOUT: 9223372036854775807             9223372036854775807 
    STDOUT: -9223372036854775808            -9223372036854775808 
    STDOUT: -9223372036854775807            -9223372036854775807 
    STDOUT: -9223372036854775806            -9223372036854775806 
    STDOUT: -1(c)                           -1 
    STDOUT: INPUT message field count: 0 
    STDOUT: OUTPUT message field count: 19 
    STDOUT: 01: sqltype: 496 LONG Nullable scale: 0 subtype: 0 len: 4 
    STDOUT:   :  name: -1(a)  alias: -1(a) 
    STDOUT:   : table: V_TEST  owner: SYSDBA 
    STDOUT: 02: sqltype: 496 LONG Nullable scale: 0 subtype: 0 len: 4 
    STDOUT:   :  name: +15  alias: +15 
    STDOUT:   : table: V_TEST  owner: SYSDBA 
    STDOUT: 03: sqltype: 496 LONG Nullable scale: 0 subtype: 0 len: 4 
    STDOUT:   :  name: 32767  alias: 32767 
    STDOUT:   : table: V_TEST  owner: SYSDBA 
    STDOUT: 04: sqltype: 496 LONG Nullable scale: 0 subtype: 0 len: 4 
    STDOUT:   :  name: 32768  alias: 32768 
    STDOUT:   : table: V_TEST  owner: SYSDBA 
    STDOUT: 05: sqltype: 496 LONG Nullable scale: 0 subtype: 0 len: 4 
    STDOUT:   :  name: 65535  alias: 65535 
    STDOUT:   : table: V_TEST  owner: SYSDBA 
    STDOUT: 06: sqltype: 496 LONG Nullable scale: 0 subtype: 0 len: 4 
    STDOUT:   :  name: 65536(a)  alias: 65536(a) 
    STDOUT:   : table: V_TEST  owner: SYSDBA 
    STDOUT: 07: sqltype: 580 INT64 Nullable scale: 0 subtype: 0 len: 8 
    STDOUT:   :  name: 65536(b)  alias: 65536(b) 
    STDOUT:   : table: V_TEST  owner: SYSDBA 
    STDOUT: 08: sqltype: 496 LONG Nullable scale: 0 subtype: 0 len: 4 
    STDOUT:   :  name: -2147483648  alias: -2147483648 
    STDOUT:   : table: V_TEST  owner: SYSDBA 
    STDOUT: 09: sqltype: 580 INT64 Nullable scale: 0 subtype: 0 len: 8 
    STDOUT:   :  name: +2147483648(a)  alias: +2147483648(a) 
    STDOUT:   : table: V_TEST  owner: SYSDBA 
    STDOUT: 10: sqltype: 580 INT64 Nullable scale: 0 subtype: 0 len: 8 
    STDOUT:   :  name: +2147483648(b)  alias: +2147483648(b) 
    STDOUT:   : table: V_TEST  owner: SYSDBA 
    STDOUT: 11: sqltype: 496 LONG Nullable scale: 0 subtype: 0 len: 4 
    STDOUT:   :  name: -1(b)  alias: -1(b) 
    STDOUT:   : table: V_TEST  owner: SYSDBA 
    STDOUT: 12: sqltype: 580 INT64 Nullable scale: 0 subtype: 0 len: 8 
    STDOUT:   :  name: +4294967295  alias: +4294967295 
    STDOUT:   : table: V_TEST  owner: SYSDBA 
    STDOUT: 13: sqltype: 580 INT64 Nullable scale: 0 subtype: 0 len: 8 
    STDOUT:   :  name: +4294967296(a)  alias: +4294967296(a) 
    STDOUT:   : table: V_TEST  owner: SYSDBA 
    STDOUT: 14: sqltype: 580 INT64 Nullable scale: 0 subtype: 0 len: 8 
    STDOUT:   :  name: +4294967296(b)  alias: +4294967296(b) 
    STDOUT:   : table: V_TEST  owner: SYSDBA 
    STDOUT: 15: sqltype: 580 INT64 Nullable scale: 0 subtype: 0 len: 8 
    STDOUT:   :  name: 9223372036854775807  alias: 9223372036854775807 
    STDOUT:   : table: V_TEST  owner: SYSDBA 
    STDOUT: 16: sqltype: 580 INT64 Nullable scale: 0 subtype: 0 len: 8 
    STDOUT:   :  name: -9223372036854775808  alias: -9223372036854775808 
    STDOUT:   : table: V_TEST  owner: SYSDBA 
    STDOUT: 17: sqltype: 580 INT64 Nullable scale: 0 subtype: 0 len: 8 
    STDOUT:   :  name: -9223372036854775807  alias: -9223372036854775807 
    STDOUT:   : table: V_TEST  owner: SYSDBA 
    STDOUT: 18: sqltype: 580 INT64 Nullable scale: 0 subtype: 0 len: 8 
    STDOUT:   :  name: -9223372036854775806  alias: -9223372036854775806 
    STDOUT:   : table: V_TEST  owner: SYSDBA 
    STDOUT: 19: sqltype: 580 INT64 Nullable scale: 0 subtype: 0 len: 8 
    STDOUT:   :  name: -1(c)  alias: -1(c) 
    STDOUT:   : table: V_TEST  owner: SYSDBA 

    STDERR: Statement failed, SQLSTATE = 42000 
    STDERR: Dynamic SQL Error 
    STDERR: -SQL error code = -104 
    STDERR: -Token unknown - line 1, column 9 
    STDERR: -'1' 

    STDERR: Statement failed, SQLSTATE = 42000 
    STDERR: Dynamic SQL Error 
    STDERR: -SQL error code = -104 
    STDERR: -Token unknown - line 1, column 9 
    STDERR: -'0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678x' 
  """

@pytest.mark.version('>=3.0')
@pytest.mark.xfail
def test_core_1760_1(db_1):
    pytest.fail("Test not IMPLEMENTED")


