#coding:utf-8
#
# id:           bugs.core_1148
# title:        Every user can view server log using services API
# decription:
#                  Instead of usage 'resource:test_user' (as it was before) we create every time this test run  user TMP$C1148
#                  and make test connect to database as this user in order to check ability to connect and get engine version.
#                  Then we parse engine version (is it 2.5 or 3.0 ?) and construct command to obtain Firebird log using FBSVCMGR
#                  (switches differ for 2.5 and 3.0! For 2.5 it must be: "action_get_ib_log", for 3.0: "action_get_fb_log").
#                  After that we try to extract firebird log using fbsvcmgr and this command is EXPECTED return error, so we log
#                  this message to separate file (and STDOUT is redirected to /dev/null).
#                  Finally, we check content of 1st and 2nd files and remove temply created user.
#
# tracker_id:   CORE-1148
# min_versions: ['2.5.0']
# versions:     2.5
# qmid:         bugs.core_1148

import pytest
from firebird.qa import db_factory, python_act, Action, user_factory, User
from firebird.driver import DatabaseError

# version: 2.5
# resources: None

substitutions_1 = [('ENGINE_VERSION .*', 'ENGINE_VERSION'),
                   ('STDERR: UNABLE TO PERFORM OPERATION.*', 'STDERR: UNABLE TO PERFORM OPERATION'),
                   ('STDERR: -YOU MUST HAVE SYSDBA RIGHTS AT THIS SERVER*', '')]

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

# test_script_1
#---
#
#
#  # Refactored 05-JAN-2016: removed dependency on recource 'test_user' because this lead to:
#  # UNTESTED: bugs.core_2729
#  # Add new user
#  # Unexpected stderr stream received from GSEC.
#  # (i.e. test remained in state "Untested" because of internal error in gsec while creating user 'test' from resource).
#  # Checked on WI-V2.5.5.26952 (SC), WI-V3.0.0.32266 (SS/SC/CS).
#
#  import os
#  import subprocess
#  import time
#
#  # Obtain engine version:
#  engine = str(db_conn.engine_version)
#
#  db_conn.execute_immediate("create user tmp$c1148 password 'QweRtyUi'")
#  db_conn.commit()
#
#  if engine.startswith('2.5'):
#      get_firebird_log_key='action_get_ib_log'
#  else:
#      get_firebird_log_key='action_get_fb_log'
#
#  fn_nul = open(os.devnull, 'w')
#  fn_err=open( os.path.join(context['temp_directory'],'tmp_1148_get_fb_log.err'), 'w')
#  subprocess.call([ context['fbsvcmgr_path'],
#                    "localhost:service_mgr",
#                    "user","TMP$C1148","password","QweRtyUi",
#                    get_firebird_log_key
#                  ],
#                  stdout=fn_nul,
#                  stderr=fn_err
#                 )
#  fn_nul.close()
#  fn_err.close()
#
#  # CLEANUP: drop user that was temp-ly created for this test:
#  ##########
#  db_conn.execute_immediate('drop user tmp$c1148')
#  db_conn.commit()
#
#  # Ouput error log: it should contain text about unable to perform operation.
#  # NB: text in FB 4.0 was splitted, phrase "You must have SYSDBA rights..." is
#  # printed on separate line. Checking for matching to this phrase can be skipped
#  # (see 'substitutions' section below):
#  with open( fn_err.name,'r') as f:
#      for line in f:
#          print("STDERR: "+line.upper())
#
#  # Do not remove this pause: on Windows closing of handles can take some (small) time.
#  # Otherwise Windows(32) access error can raise here.
#  time.sleep(1)
#
#  if os.path.isfile(fn_err.name):
#      os.remove(fn_err.name)
#
#
#---

act_1 = python_act('db_1', substitutions=substitutions_1)

user_1 = user_factory('db_1', name='TMP$C1148', password='QweRtyUi')

@pytest.mark.version('>=3.0')
def test_1(act_1: Action, user_1: User):
    if act_1.is_version('<4'):
        if act_1.platform == 'Windows':
            pattern = 'Unable to perform operation'
        else:
            pattern = 'You must be either SYSDBA or owner of the database'
    else:
        pattern = 'You must have SYSDBA rights at this server'
    with act_1.connect_server(user=user_1.name, password=user_1.password) as srv:
        with pytest.raises(DatabaseError, match=pattern):
            srv.info.get_log()

