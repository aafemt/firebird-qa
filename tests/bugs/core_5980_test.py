#coding:utf-8
#
# id:           bugs.core_5980
# title:        Firebird crashes due to concurrent operations with expression indices
# decription:
#                   Scenario for reproducing was given by Vlad, letter 25-02-2020 19:15.
#                   Unfortuinately, this crash can occur only in developer build rather than release one.
#
#                   Although issues from ticket can NOT be reproduced, it was encountered in 2.5.0.26074
#                   that statements from here lead DB to be corrupted:
#                       Error while commiting transaction:
#                       - SQLCODE: -902
#                       - database file appears corrupt...
#                       - wrong page type
#                       - page 0 is of wrong type (expected 6, found 1)
#                       -902
#                       335544335
#                  No such problem in 2.5.1 and above.
#                  Decided to add this .fbt just for check that DB will not be corrupted.
#
#                  TICKET ISSUE REMAINS IRREPRODUCIBLE (checked on following SuperServer builds: 2.5.1, 2.5.6, 2.5.9, 3.0.6, 4.0.0).
#
# tracker_id:   CORE-5980
# min_versions: ['2.5.1']
# versions:     2.5.1
# qmid:         None

import pytest
from firebird.qa import db_factory, python_act, Action

# version: 2.5.1
# resources: None

substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

# test_script_1
#---
# import os
#  import sys
#  from fdb import services
#
#  os.environ["ISC_USER"] = user_name
#  os.environ["ISC_PASSWORD"] = user_password
#
#  fb_home = services.connect(host='localhost', user= user_name, password= user_password).get_home_directory()
#  if db_conn.engine_version < 3:
#      fb_home = os.path.join( fb_home, 'bin')
#
#  db_conn.close()
#  con1 = fdb.connect( dsn = dsn )
#  con2 = fdb.connect( dsn = dsn )
#
#  con1.execute_immediate('recreate table t1(id int)')
#  con1.execute_immediate('create index t1_idx on t1 computed by (id + 0)')
#  con1.commit()
#
#  cur1 = con1.cursor()
#  cur1.execute( 'insert into t1(id) values(?)', (1,) )
#  con1.commit()
#
#  # this lead to corruption of database in 2.5.0
#  # page 0 is of wrong type (expected 6, found 1):
#  # -----------------------
#  con2.execute_immediate('alter index t1_idx active')
#  con2.commit()
#  con2.close()
#
#  con1.close()
#  cur1.close()
#
#
#---

act_1 = python_act('db_1', substitutions=substitutions_1)

@pytest.mark.version('>=2.5.1')
def test_1(act_1: Action):
    with act_1.db.connect() as con1, act_1.db.connect() as con2:
        con1.execute_immediate('recreate table t1(id int)')
        con1.execute_immediate('create index t1_idx on t1 computed by (id + 0)')
        con1.commit()
        c = con1.cursor()
        c.execute('insert into t1(id) values(?)', [1])
        con1.commit()
        # this lead to corruption of database in 2.5.0
        # page 0 is of wrong type (expected 6, found 1)
        con2.execute_immediate('alter index t1_idx active')
        con2.commit()
