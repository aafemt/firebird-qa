#coding:utf-8
#
# id:           bugs.gh_6817
# title:        Command switch "-fetch_password <passwordfile>" does not work with gfix
# decription:
#                   https://github.com/FirebirdSQL/firebird/issues/6817
#
#                   Confirmed bug on 5.0.0.63, 4.0.0.2508, 3.0.8.33470.
#                   Checked on intermediate builds 4.x and 5.x with the same numbers, timestamps: 08-jun-2021 16:32, 16:35 -- all OK.
#
# tracker_id:   GH-6817
# min_versions: ['3.0.8']
# versions:     3.0.8
# qmid:         None

import pytest
from firebird.qa import db_factory, python_act, Action

# version: 3.0.8
# resources: None

substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

# test_script_1
#---
#
#  import os
#  import time
#
#  try:
#      del os.environ["ISC_USER"]
#  except KeyError as e:
#      pass
#
#
#  # tmpfdb = db_conn.database_name
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
#            print('type(f_names_list[i])=',type(f_names_list[i]))
#            del_name = None
#
#         if del_name and os.path.isfile( del_name ):
#             os.remove( del_name )
#
#  #--------------------------------------------
#
#  f_pswd_file = open( os.path.join(context['temp_directory'], 'tmp_gh_6817.dat'), 'w' )
#  f_pswd_file.write( user_password )
#  flush_and_close( f_pswd_file )
#
#  runProgram('gfix',[ '-user', user_name, '-fetch_password', f_pswd_file.name, dsn, '-w', 'async'])
#  runProgram('gfix',[ '-fetch_password', f_pswd_file.name, dsn, '-user', user_name, '-w', 'async'])
#  runProgram('gfix',[ '-user', user_name, dsn, '-fetch_password', f_pswd_file.name, '-w', 'async'])
#  runProgram('gfix',[ dsn, '-fetch_password', f_pswd_file.name, '-user', user_name, '-w', 'async'])
#
#  # Cleanup:
#  time.sleep(1)
#  cleanup( (f_pswd_file,) )
#
#---

act_1 = python_act('db_1', substitutions=substitutions_1)


@pytest.mark.skip('FIXME: Not IMPLEMENTED')
@pytest.mark.version('>=3.0.8')
def test_1(act_1: Action):
    pytest.fail("Not IMPLEMENTED")
