#coding:utf-8
#
# id:           bugs.core_4388
# title:        SELECT WITH LOCK may enter an infinite loop for a single record
# decription:
#                  Caution: could not reproduce on neither WI-T3.0.0.30566 Firebird 3.0 Alpha 1 nor WI-T3.0.0.30809 Firebird 3.0 Alpha 2.
#                  Any advice about how this test should be properly written will be appreciated.
#                  Added separate code for 4.0 because isc_update_conflict now can be primary code of exception reason
#                  (after consulting with Vlad, letter 06-aug-2018 16:27).
#
#                  01-apr-2020. Expected STDERR section for 4.0.x was changed BACK TO PREVIOUS set of messages, i.e.:
#                      1. Statement failed, SQLSTATE = 40001
#                      2. deadlock <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  THIS LINE APPEARED SINCE 4.0.0.1848
#                      3. update conflicts with concurrent update
#                      4. concurrent transaction number is ...
#                  Confirmed by Alex, letter 31.03.2020 12:01.
#
#                  Checked on:
#                       3.0.4.33022: OK, 5.453s.
#                       4.0.0.1158: OK, 5.313s.
#
#                  21.09.2020: removed separate section for 4.0 because error messages equal to FB 3.x. Changed 'substitution' section.
#
#                  Waiting for completion of child ISQL async process is done by call <isql_PID>.wait() instead of old (and "fragile")
#                  assumption about maximal time that it could last before forcedly terminate it.
#
#                  Replaced direct specification of executable 'isql' with context['isql_path'] in order to remove dependence on PATH
#                  (suggested by dimitr, letter 28.08.2020, 13:42; otherwise directory with isql must be added into PATH list).
#
#
# tracker_id:   CORE-4388
# min_versions: ['3.0']
# versions:     3.0
# qmid:         None

import pytest
import subprocess
import time
from pathlib import Path
from firebird.qa import db_factory, python_act, Action, temp_file

# version: 3.0
# resources: None

substitutions_1 = [('(-)?concurrent\\s+transaction\\s+number(\\s+is)?\\s+\\d+', 'concurrent transaction'),
                   ('After\\s+line\\s+\\d+.*', '')]

init_script_1 = """
    create table test(id int primary key, x int);
    commit;
    insert into test values(1, 100);
    commit;
"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

# test_script_1
#---
# import os
#  import subprocess
#  from subprocess import Popen
#  import time
#  import fdb
#
#  db_conn.close()
#
#  os.environ["ISC_USER"] = user_name
#  os.environ["ISC_PASSWORD"] = user_password
#
#  #-----------------------------------
#
#  def flush_and_close(file_handle):
#      # https://docs.python.org/2/library/os.html#os.fsync
#      # If you're starting with a Python file object f,
#      # first do f.flush(), and
#      # then do os.fsync(f.fileno()), to ensure that all internal buffers associated with f are written to disk.
#      global os
#
#      file_handle.flush()
#      os.fsync(file_handle.fileno())
#
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
#
#  #--------------------------------------------
#
#  att1 = fdb.connect( dsn = dsn)
#
#  # Delete record but not yet commit - it's a time
#  # to make another connection:
#  att1.execute_immediate("delete from test where id = 1")
#
#  sql_cmd='''
#      set list on;
#      -- set echo on;
#      commit;
#      set transaction lock timeout 20;
#      select x from test where id = 1 with lock;
#  '''
#
#  f_select_with_lock_sql = open( os.path.join(context['temp_directory'],'tmp_4388_select_with_lock.sql'), 'w')
#  f_select_with_lock_sql.write(sql_cmd)
#  f_select_with_lock_sql.close()
#
#  #context['isql_path']
#
#  f_select_with_lock_log = open( os.path.join(context['temp_directory'],'tmp_4388_select_with_lock.log'), 'w')
#
#  p_hanged_isql=subprocess.Popen(   [ context['isql_path'], dsn, "-n", "-i", f_select_with_lock_sql.name ],
#                                    stdout = f_select_with_lock_log,
#                                    stderr = subprocess.STDOUT
#                                )
#
#  # Let ISQL to be loaded and establish its attachment:
#  time.sleep(2)
#
#  # Return to att1 and make COMMIT of deleted record:
#  #############
#  att1.commit()
#  att1.close()
#  #############
#
#  # Wait until ISQL complete its mission:
#  p_hanged_isql.wait()
#
#  flush_and_close(f_select_with_lock_log)
#
#  with open(f_select_with_lock_log.name,'r') as f:
#      print(f.read())
#  f.close()
#
#  ###############################
#  # Cleanup.
#  time.sleep(1)
#  f_list = [ i.name for i in (f_select_with_lock_sql, f_select_with_lock_log) ]
#  cleanup( f_list )
#
#
#---

act_1 = python_act('db_1', substitutions=substitutions_1)

expected_stdout_1 = """
    Statement failed, SQLSTATE = 40001
    deadlock
    -update conflicts with concurrent update
    -concurrent transaction number is 13
"""

test_script_1 = temp_file('test-script.sql')
script_out = temp_file('test-script.out')

@pytest.mark.version('>=3.0')
def test_1(act_1: Action, test_script_1: Path, script_out: Path):
    with act_1.db.connect() as att1:
        # Delete record but not yet commit - it's a time
        # to make another connection:
        att1.execute_immediate("delete from test where id = 1")
        test_script_1.write_text("""
        set list on;
        -- set echo on;
        commit;
        set transaction lock timeout 20;
        select x from test where id = 1 with lock;
        """)
        try:
            with open(script_out, mode='w') as output:
                p_test_sql = subprocess.Popen([act_1.vars['isql'], '-n', '-i', str(test_script_1),
                                               '-user', act_1.db.user,
                                               '-password', act_1.db.password, act_1.db.dsn],
                                               stdout=output, stderr=subprocess.STDOUT)
            #
            time.sleep(2)
        finally:
            att1.commit()
            p_test_sql.wait()
        # Check
        act_1.expected_stdout = expected_stdout_1
        act_1.stdout = script_out.read_text()
        assert act_1.clean_stdout == act_1.clean_expected_stdout
