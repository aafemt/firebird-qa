#coding:utf-8
#
# id:           bugs.core_2475
# title:        External table data not visible to other sessions in Classic
# decription:   In 2.1.2 SuperServer, any data written to external tables are visible to other sessions.
#               However in Classic, this data is not visible. It seems to be cached and written to file eventually, when this happens it becomes visible.
#               
#               THIS TEST WILL END WITH ERROR IF EXTERNAL TABLE ACCESS IS NOT ALLOWED, WHICH IS BY DEFAULT. It's necessary to adjust firebird.conf.
# tracker_id:   CORE-2475
# min_versions: ['2.1.3']
# versions:     2.1.3
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 2.1.3
# resources: None

substitutions_1 = []

init_script_1 = """create table EXT1 external file '$(DATABASE_LOCATION)EXT1.TBL'
(PK INTEGER);
"""

db_1 = db_factory(page_size=4096, sql_dialect=3, init=init_script_1)

# test_script_1
#---
# # init
#  import os
#  ext_filename = '%sEXT1.TBL' % context[db_path_property]
#  
#  # session A
#  c1 = db_conn.cursor()
#  c1.execute("insert into EXT1 (PK) values (1)")
#  
#  db_conn.commit()
#  
#  # session B
#  con2 = kdb.connect(dsn=dsn,user=user_name,password=user_password)
#  c2 = con2.cursor()
#  c2.execute('select * from EXT1')
#  printData(c2)
#  
#  # cleanup
#  con2.close()
#  try:
#      os.remove(ext_filename)
#  except:
#      print("Error while removing external table file")
#  
#---
#act_1 = python_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """PK
-----------
1
"""

@pytest.mark.version('>=2.1.3')
@pytest.mark.xfail
def test_1(db_1):
    pytest.fail("Test not IMPLEMENTED")


