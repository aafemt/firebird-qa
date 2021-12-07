#coding:utf-8
#
# id:           bugs.core_5434
# title:        Read-only transactions in SuperServer could avoid immediate write of Header and TIP pages after change
# decription:
#                  If current FB arch is SuperServer then we:
#                      1. We make 'snapshot' of mon$io_stats.mon$page_writes value before test and then launch plently transactions (e.g, 50)
#                         in READ-ONLY mode. All of them then are immediately committed, w/o any actions.
#                      2. After this we take 2nd 'snapshot' of mon$io_stats.mon$page_writes and compare it with 1st one.
#                      3. Difference of 'mon$page_writes' values should be 1 (One).
#                  Otherwise (SC/CS) we defer checking because improvement currently not implemented for these modes.
#
#                  Checked on:
#                  1) WI-T4.0.0.463, WI-V3.0.2.32670 - room for improvement DOES exist: page_diff = 102 pages
#                  2) WI-T4.0.0.511, WI-V3.0.2.32676 - all OK, page_diff = 1 (One).
#
# tracker_id:   CORE-5434
# min_versions: ['3.0.2']
# versions:     3.0.2
# qmid:         None

import pytest
from firebird.qa import db_factory, python_act, Action
from firebird.driver import TraAccessMode, TPB

# version: 3.0.2
# resources: None

#substitutions_1 = [('Deferred: fb_arch=.*', 'Acceptable')]
substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

# test_script_1
#---
#
#  import os
#  import sys
#  os.environ["ISC_USER"] = user_name
#  os.environ["ISC_PASSWORD"] = user_password
#
#  def get_fb_arch(a_dsn):
#     try:
#        con1 = fdb.connect(dsn = a_dsn)
#        con2 = fdb.connect(dsn = a_dsn)
#
#        cur1 = con1.cursor()
#
#        sql=(
#               "select count(distinct a.mon$server_pid), min(a.mon$remote_protocol), max(iif(a.mon$remote_protocol is null,1,0))"
#              +" from mon$attachments a"
#              +" where a.mon$attachment_id in (%s, %s) or upper(a.mon$user) = upper('%s')"
#              % (con1.attachment_id, con2.attachment_id, 'cache writer')
#            )
#
#        cur1.execute(sql)
#        for r in cur1.fetchall():
#            server_cnt=r[0]
#            server_pro=r[1]
#            cache_wrtr=r[2]
#
#        if server_pro == None:
#            fba='Embedded'
#        elif cache_wrtr == 1:
#            fba='SS'
#        elif server_cnt == 2:
#            fba='CS'
#        else:
#
#            f1=con1.db_info(fdb.isc_info_fetches)
#
#            cur2=con2.cursor()
#            cur2.execute('select 1 from rdb$database')
#            for r in cur2.fetchall():
#               pass
#
#            f2=con1.db_info(fdb.isc_info_fetches)
#
#            fba = 'SC' if f1 ==f2 else 'SS'
#
#        #print(fba, con1.engine_version, con1.version)
#        return fba
#
#     finally:
#        con1.close()
#        con2.close()
#
#  fb_arch=get_fb_arch(dsn)
#
#  if fb_arch == 'SS':
#
#      txParams = ( [ fdb.isc_tpb_read ] )
#      c2 = fdb.connect(dsn=dsn)
#
#      sql='select mon$page_writes from mon$io_stats where mon$stat_group=0'
#      cur=db_conn.cursor()
#
#      cur.execute(sql)
#      for r in cur:
#        page_writes_before_test = r[0]
#      db_conn.commit()
#
#      ta=[]
#      for i in range(0, 50):
#         ta.append( c2.trans( default_tpb = txParams ) )
#         ta[i].begin()
#
#      for i in range(0,len(ta)):
#         ta[i].rollback()
#
#
#      cur.execute(sql)
#      for r in cur:
#        page_writes_after_test = r[0]
#
#      pw_diff = page_writes_after_test - page_writes_before_test
#
#      db_conn.commit()
#      c2.close()
#
#      msg = 'Acceptable' if pw_diff == 1 else ('Too big value of page_writes diff: %s' % ( pw_diff ))
#  else:
#      # FB works NOT in SuperServer. This currently must be SKIPPED from checking (see notes in the ticket).
#      msg = 'Deferred: fb_arch=%s' % fb_arch
#
#  print(msg)
#
#
#---

act_1 = python_act('db_1', substitutions=substitutions_1)

@pytest.mark.version('>=3.0.2')
def test_1(act_1: Action):
    tpb = TPB(access_mode=TraAccessMode.READ).get_buffer()
    sql = 'select mon$page_writes from mon$io_stats where mon$stat_group=0'
    if act_1.get_server_architecture() == 'SS':
        with act_1.db.connect() as con:
            with act_1.db.connect() as con2:
                cur = con.cursor()
                page_writes_before_test = cur.execute(sql).fetchone()[0]
                con.commit()
                #
                ta = []
                for i in range(50):
                    tra = con2.transaction_manager(default_tpb=tpb)
                    tra.begin()
                    ta.append(tra)
                for tra in ta:
                    tra.rollback()
                #
                cur = con.cursor()
                page_writes_after_test = cur.execute(sql).fetchone()[0]
                con.commit()
    #
    assert page_writes_after_test - page_writes_before_test == 1
