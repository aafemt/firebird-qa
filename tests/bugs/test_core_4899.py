#coding:utf-8
#
# id:           bugs.core_4899
# title:        GFIX -online: message "IProvider::attachDatabase failed when loading mapping cache" appears in Classic (only) if access uses remote protocol
# decription:   
#                
# tracker_id:   CORE-4899
# min_versions: ['3.0']
# versions:     3.0
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 3.0
# resources: None

substitutions_1 = [('^((?!Attributes).)*$', ''), ('[\t]+', ' ')]

init_script_1 = """"""

db_1 = db_factory(page_size=4096, sql_dialect=3, init=init_script_1)

# test_script_1
#---
# 
#  import os
#  
#  os.environ["ISC_USER"] = user_name
#  os.environ["ISC_PASSWORD"] = user_password
#  
#  db_conn.close()
#  
#  fdb='$(DATABASE_LOCATION)bugs.core_4899.fdb'
#  fdx=os.path.join(context['temp_directory'],'tmp_copy_4899.fdb')
#  
#  if os.path.isfile(fdx):
#      os.remove(fdx)
#  
#  script="create database 'localhost:%s';" % fdx
#  runProgram('isql',['-q'],script)
#  # --------------------- I ----------------
#  
#  #shutil.copy2( fdb, fdx )
#  
#  # Trying to move database to OFFLINE:
#  
#  runProgram('gfix',['-shut', 'full', '-force', '0', fdx])
#  
#  runProgram('gstat',['-h',fdx])
#  
#  # Trying to move database online using LOCAL protocol:
#  runProgram('gfix',['-online',fdx])
#  
#  # gfix attachment via local protocol reflects with following lines in trace:
#  # 2015-08-24T18:30:03.2580 (2516:012417E0) ATTACH_DATABASE
#  #	C:\\MIX\\FIREBIRD\\QA\\FBT-REPO\\TMP\\CORE4899-TMP.FDB (ATT_9, SYSDBA:NONE, NONE, <internal>)
#  
#  runProgram('gstat',['-h',fdx])
#  
#  if os.path.isfile(fdx):
#      os.remove(fdx)
#  
#  # --------------------- II ---------------
#  
#  #shutil.copy2( fdb, fdx )
#  runProgram('isql',['-q'],script)
#  
#  runProgram('gfix',['-shut', 'full', '-force', '0', fdx])
#  runProgram('gstat',['-h',fdx])
#  
#  # Trying to move database online using REMOTE protocol:
#  runProgram('gfix',['-online','localhost:'+fdx])
#  
#  # Note: gfix attachment via remote protocol refects with following lines in trace:
#  # 2015-08-24T18:30:03.8520 (3256:01B526A8) ATTACH_DATABASE
#  #	C:\\MIX\\FIREBIRD\\QA\\FBT-REPO\\TMP\\CORE4899-TMP.FDB (ATT_9, SYSDBA:NONE, NONE, TCPv4:127.0.0.1)
#  #	C:\\MIX
#  irebird
#  b30\\gfix.exe:1448
#  
#  runProgram('gstat',['-h',fdx])
#  
#  if os.path.isfile(fdx):
#      os.remove(fdx)
#  
#  #,  'substitutions':[('^((?!Attributes).)*$',''),('[\\s]+',' ')]
#  
#    
#---
#act_1 = python_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
Attributes force write, full shutdown
Attributes force write
Attributes force write, full shutdown
Attributes force write
  """

@pytest.mark.version('>=3.0')
@pytest.mark.xfail
def test_core_4899_1(db_1):
    pytest.fail("Test not IMPLEMENTED")


