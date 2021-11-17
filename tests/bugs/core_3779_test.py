#coding:utf-8
#
# id:           bugs.core_3779
# title:        Report OS user name in MON$ATTACHMENTS
# decription:
#                    We compare values in mon$attachment with those that can be obtained using pure Python calls (without FB).
#                    NB: on Windows remote_os_user contains value in lower case ('zotov'), exact value was: 'Zotov'.
#
# tracker_id:   CORE-3779
# min_versions: ['3.0']
# versions:     3.0
# qmid:         None

import pytest
import socket
import getpass
from firebird.qa import db_factory, python_act, Action

# version: 3.0
# resources: None

substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

# test_script_1
#---
#
#  import os
#  import socket
#  import getpass
#
#  cur=db_conn.cursor()
#  cur.execute('select mon$remote_host, mon$remote_os_user from mon$attachments where mon$attachment_id=current_connection')
#  for r in cur:
#      if r[0].upper() == socket.gethostname().upper():
#          print('Check of remote_host: passed')
#      else:
#          print('FAILED check remote_host: got |'+r[0]+'| instead of |'+socket.gethostname()+'|')
#
#      if r[1].upper() == getpass.getuser().upper():
#          print('Check of remote_os_user: passed')
#      else:
#          print('FAILED check remote_os_user: got |'+r[1]+'| instead of |'+getpass.getuser()+'|')
#
#  cur.close()
#
#---

act_1 = python_act('db_1', substitutions=substitutions_1)

@pytest.mark.version('>=3.0')
def test_1(act_1: Action):
    with act_1.db.connect() as con:
        c = con.cursor()
        c.execute('select mon$remote_host, mon$remote_os_user from mon$attachments where mon$attachment_id=current_connection')
        r = c.fetchone()
        if r[0].upper() != socket.gethostname().upper():
            pytest.fail(f'FAILED check remote_host: got "{r[0]}" instead of "{socket.gethostname()}"')
        if r[1].upper() != getpass.getuser().upper():
            pytest.fail(f'FAILED check remote_os_user: got "{r[1]}" instead of "{getpass.getuser()}"')
