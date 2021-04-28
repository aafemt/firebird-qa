#coding:utf-8
#
# id:           bugs.core_4840
# title:        Transactions with isc_tpb_autocommit can hang the server
# decription:   
#                  Test creates trivial SP and comment for it (in UTF8 with multi-byte characters) in single Tx with autocommit = true.
#                  Confirmed:
#                  1. Crash on LI-V3.0.0.32173, WI-V3.0.0.32239
#                     Crash on WI-V3.0.0.32134 Firebird 3.0 Release Candidate 1 with issuing in firebird.log:
#                     ===
#                     internal Firebird consistency check (Too many savepoints (287), file: tra.cpp line: 2486)
#                     internal Firebird consistency check (wrong record version (185), file: vio.cpp line: 3823)
#                     ===
#                     (after this FB instance is unavaliable; no any *other* database can be attached).
#               
#                  2. Normal work on LI-V3.0.0.32239 Rev: 62705
#                  Example of TPB creation can be found here:
#                  http://www.firebirdsql.org/file/documentation/drivers_documentation/python/3.3.0/beyond-python-db-api.html
#                  List of allowed TPB parameters: C:\\Python27\\Lib\\site-packages
#               db\\ibase.py 
#                
# tracker_id:   CORE-4840
# min_versions: ['2.5.0']
# versions:     2.5
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 2.5
# resources: None

substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(charset='UTF8', sql_dialect=3, init=init_script_1)

# test_script_1
#---
# import fdb
#  
#  db_conn.close()
#  conn = kdb.connect(dsn=dsn.encode(),user='SYSDBA',password='masterkey')
#  
#  customTPB = ( [ fdb.isc_tpb_read_committed, fdb.isc_tpb_rec_version, fdb.isc_tpb_autocommit ] )
#  
#  conn.begin( tpb=customTPB )
#  xcur=conn.cursor()
#  
#  sp_ddl="create or alter procedure sp_test (in1 integer, in2 float)" + "returns (" + "    out1 varchar(20)," + "    out2 double precision, " + "    out3 integer" + ") as " + "    declare x integer;" + "begin" + "    out1 = 'out string';" + "    out2 = 2 * in2;" + "    out3 = 3 * in1;" + "    suspend; " + "end"
#  
#  sp_rem="comment on procedure sp_test is 'Det är inte alla präster, som göra prästgården eller dess torp till änkesäte åt orkeslösa trotjänarinnor, hade biskopen en gång sagt om Helenas prost.'"
#  
#  ### 27.01.2016: fdb 1.5 will produce 
#  ### ===
#  ### ReferenceError:
#  ### weakly-referenced object no longer exists
#  ### ===
#  ### - for these statements:
#  ###xcmd=xcur.prep( sp_ddl )
#  ###xcur.execute(xcmd)
#  ###xcmd=xcur.prep( sp_rem )
#  ###xcur.execute(xcmd)
#  
#  # For confirmation of ticket issues it is enough to do just this:
#  
#  xcur.execute(sp_ddl)
#  xcur.execute(sp_rem)
#  
#  conn.commit()
#  conn.close()
#  
#  sqltxt="set list on; select * from sp_test(12345, 3.1415926);"
#  runProgram('isql',[dsn,'-user',user_name,'-pas',user_password,'-q'],sqltxt)
#    
#---
#act_1 = python_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    OUT1                            out string
    OUT2                            6.283185005187988
    OUT3                            37035
  """

@pytest.mark.version('>=2.5')
@pytest.mark.xfail
def test_1(db_1):
    pytest.fail("Test not IMPLEMENTED")


