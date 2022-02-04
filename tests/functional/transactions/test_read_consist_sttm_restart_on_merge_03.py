#coding:utf-8

"""
ID:          transactions.read-consist-sttm-restart-on-merge-03
TITLE:       READ CONSISTENCY. Check creation of new statement-level snapshot and restarting changed caused by MERGE. Test-03.
DESCRIPTION:
  Initial article for reading:
          https://asktom.oracle.com/pls/asktom/f?p=100:11:::::P11_QUESTION_ID:11504247549852
          Note on terms which are used there: "BLOCKER", "LONG" and "FIRSTLAST" - their names are slightly changed here
          to: LOCKER-1, WORKER and LOCKER-2 respectively.
      See also: doc/README.read_consistency.md

      **********************************************

      This test verifies that statement-level snapshot and restart will be performed when "main" session ("worker")
      performs DELETE statement and is involved in update conflicts.
      ("When update conflict is detected <...> then engine <...> creates new statement-level snapshot and restart execution...")

      ::: NB :::
      This test uses script %FBT_REPO%/files/read-consist-sttm-restart-DDL.sql which contains common DDL for all other such tests.
      Particularly, it contains two TRIGGERS (TLOG_WANT and TLOG_DONE) which are used for logging of planned actions and actual
      results against table TEST. These triggers use AUTONOMOUS transactions in order to have ability to see results in any
      outcome of test.

      ###############
      Following scenario if executed here (see also: "doc/README.read_consistency.md"; hereafer is marked as "DOC"):

      * add new table that is child to test: TDETL (with FK that references TEST and 'on delete cascade' clause)
      * three rows are inserted into the table TEST, with IDs: 2, 3 and 5.

      * session 'locker-1' ("BLOCKER" in Tom Kyte's article ):
              update set id=id where id = 5;

      * session 'worker' ("LONG" in TK article) has mission:
              merge into test t using(select * from test where id >= 3 order by id) s on t.id = s.id when matched then delete;
              // using TIL = read committed read consistency

          // Execution will have PLAN ORDER <ASCENDING_INDEX>.
          // It will delete (first avaliable for cursor) row with ID = 3 but can not change row with ID = 5 because of locker-1.
          // Update conflict appears here and, because of this, worker temporary changes its TIL to RC no record_version (RC NRV).
          // [DOC]: "a) transaction isolation mode temporarily switched to the READ COMMITTED *NO RECORD VERSION MODE*"
          // This (new) TIL allows worker further to see all committed versions, regardless of its own snapshot.

      * session 'locker-2' ("FIRSTLAST" in TK article): replaces ID = 2 with new value = 4, then commits
        and locks this record again:
              (1) update test set id = 4 where id = 2;
              (2) commit;
              (3) update test set id=id where id = 4;
          // session-'worker' remains waiting at this point because row with ID = 5 is still occupied by by locker-1
          // but worker must further see record with (new) id = 4 because its TIL was changed to RC NO RECORD_VERSION.

      * session 'locker-1':
              (1) commit;
              (2) insert into test(id) values(6);
              (3) insert into detl(id, pid) values(6001, 6);
              (4) commit;
              (5) update test set id=id where id=6;
          // first of these statements: '(1) commit' - will release record with ID = 5.
          // Worker sees this record (because of TIL = RC NRV) and put write-lock on it.
          // [DOC]: "b) engine put write lock on conflicted record"
          // Also, because worker TIL = RC NRV, it will see two new rows with ID = 4 and 6, and they meet worker cursor condition ("id>=3").
          // Worker resumes search for any rows with ID >=3, and it does this with taking in account "ORDER BY ID ASC".
          // [DOC]: "c) engine continue to evaluate remaining records of update/delete cursor and put write locks on it too"
          // Worker starts to search records which must be involved in its DML and *found* sucn rows (with ID = 4 and 6).
          // NB. These rows currently can NOT be deleted by worker because of locker-2 and locker-1 have uncommitted updates.
          // BECAUSE OF FACT THAT AT LEAST ONE ROW *WAS FOUND* - STATEMENT-LEVEL RESTART *NOT* YET OCCURS HERE.
          // :::!! NB, AGAIN !! ::: restart NOT occurs here because at least one records found, see:
          // [DOC]: "d) when there is *no more* records to fetch, engine start to undo all actions performed since
          //            top-level statement execution starts and preserve already taken write locks
          //         e) then engine restores transaction isolation mode as READ COMMITTED *READ CONSISTENCY*,
          //            creates new statement-level snapshot and restart execution of top-level statement."

      * session 'locker-2':
             commit;
          // This will release record with ID = 4 (but row with ID = 6 is still inaccessible because of locker-1).
          // Worker sees record (because of TIL = RC NRV) with ID = 4 and put write-lock on it.
          // Then worker resumes search for any (new) rows with ID >= 3, and it does this with taking in account required order
          // of its DML (i.e. ORDER BY ID ASC).
          // [DOC]: "c) engine continue to evaluate remaining records of update/delete cursor and put write locks on it too"
          // But there are no such rows in the tableL earlier worker already encountered all possible rows (with ID=4 and 6)
          // and *did* put write-locks on them. So at this point NO new rows can be found for putting new lock on it.
          // BECAUSE OF FACT THAT NO RECORDS FOUND, WORKER DOES UNDO BUT KEEP LOCKS AND THEN MAKES FIRST STATEMENT-LEVEL RESTART.
          // [DOC]: "d) when there is no more records to fetch, engine start to undo all actions ... and preserve already taken write locks
          //         e) then engine restores transaction isolation mode as READ COMMITTED *READ CONSISTENCY*,
          //           creates new statement-level snapshot and restart execution of top-level statement."

      * session 'locker-1':
             commit;
          // This will release record with ID = 6 - and this is the last row which meet cursor condition of session-worker.
          // Worker sees record (because of TIL = RC NRV) with ID = 6 and put write-lock on it.
          // Then worker resumes search for any (new) rows with ID >= 3, and it does this with taking in account required order
          // of its DML (i.e. ORDER BY ID ASC). NO new rows (with ID >= 3) can be found for putting new lock on it.
          // BECAUSE OF FACT THAT NO RECORDS FOUND, WORKER DOES UNDO BUT KEEP LOCKS AND THEN MAKES SECOND STATEMENT-LEVEL RESTART.

      Expected result:
      * session-'worker' must *successfully* complete deletion of all rows which it could see at the starting point (ID=3 and 5)
        PLUS rows with ID = 4 (ex. ID=2) and 6  (this ID is new, it did not exist at the statement start).
        As result, all rows must be deleted.

      * three unique values must be in the column TLOG_DONE.SNAP_NO for session-'worker' when it performed DELETE statement: first of them
        was created by initial statement start and all others reflect two restarts (this column has values which are evaluated using
        rdb$get_context('SYSTEM', 'SNAPSHOT_NUMBER') -- see trigger TEST_AIUD).
        It is enough to count these values using COUNT(*) or enumarate them by DENSE_RANK() function.

      NOTE: concrete values of fields TRN, GLOBAL_CN and SNAP_NO in the TLOG_DONE can differ from one to another run!
      This is because of concurrent nature of connections that work against database. We must not assume that these values will be constant.
      ################

      Checked on 4.0.0.2204 SS/CS
      NOTE: added for-loop in order to check different target objects: TABLE ('test') and VIEW ('v_test'), see 'checked_mode'.
FBTEST:      functional.transactions.read_consist_sttm_restart_on_merge_03
"""

import pytest
from firebird.qa import *

db = db_factory()

act = python_act('db', substitutions=[('=', ''), ('[ \t]+', ' ')])

expected_stdout = """
    checked_mode: table, STDLOG: Records affected: 4

    checked_mode: table, STDLOG: Records affected: 0

    checked_mode: table, STDLOG:  OLD_ID OP              SNAP_NO_RANK
    checked_mode: table, STDLOG: ======= ====== =====================
    checked_mode: table, STDLOG:       3 DEL                        1
    checked_mode: table, STDLOG:       3 DEL                        2
    checked_mode: table, STDLOG:       3 DEL                        3
    checked_mode: table, STDLOG:       4 DEL                        3
    checked_mode: table, STDLOG:       5 DEL                        3
    checked_mode: table, STDLOG:       6 DEL                        3
    checked_mode: table, STDLOG: Records affected: 6


    checked_mode: view, STDLOG: Records affected: 4

    checked_mode: view, STDLOG: Records affected: 0

    checked_mode: view, STDLOG:  OLD_ID OP              SNAP_NO_RANK
    checked_mode: view, STDLOG: ======= ====== =====================
    checked_mode: view, STDLOG:       3 DEL                        1
    checked_mode: view, STDLOG:       3 DEL                        2
    checked_mode: view, STDLOG:       3 DEL                        3
    checked_mode: view, STDLOG:       4 DEL                        3
    checked_mode: view, STDLOG:       5 DEL                        3
    checked_mode: view, STDLOG:       6 DEL                        3
    checked_mode: view, STDLOG: Records affected: 6
"""

@pytest.mark.skip('FIXME: Not IMPLEMENTED')
@pytest.mark.version('>=4.0')
def test_1(act: Action):
    pytest.fail("Not IMPLEMENTED")

# Original python code for this test:
# -----------------------------------
#
# import os
# import sys
# import subprocess
# from subprocess import Popen
# import re
# import difflib
# from fdb import services
# import time
#
# os.environ["ISC_USER"] = user_name
# os.environ["ISC_PASSWORD"] = user_password
#
# db_conn.close()
#
# #--------------------------------------------
#
# def flush_and_close( file_handle ):
#     # https://docs.python.org/2/library/os.html#os.fsync
#     # If you're starting with a Python file object f,
#     # first do f.flush(), and
#     # then do os.fsync(f.fileno()), to ensure that all internal buffers associated with f are written to disk.
#     global os
#
#     file_handle.flush()
#     if file_handle.mode not in ('r', 'rb') and file_handle.name != os.devnull:
#         # otherwise: "OSError: [Errno 9] Bad file descriptor"!
#         os.fsync(file_handle.fileno())
#     file_handle.close()
#
# #--------------------------------------------
#
# def cleanup( f_names_list ):
#     global os
#     for f in f_names_list:
#        if type(f) == file:
#           del_name = f.name
#        elif type(f) == str:
#           del_name = f
#        else:
#           print('Unrecognized type of element:', f, ' - can not be treated as file.')
#           del_name = None
#
#        if del_name and os.path.isfile( del_name ):
#            os.remove( del_name )
#
# #--------------------------------------------
#
# sql_init_ddl = os.path.join(context['files_location'],'read-consist-sttm-restart-DDL.sql')
#
# for checked_mode in('table', 'view'):
#
#     target_obj = 'test' if checked_mode == 'table' else 'v_test'
#
#     # drop dependencies:
#     runProgram('isql', [ dsn, '-q' ], 'recreate table detl(id int);')
#
#     f_init_log=open( os.path.join(context['temp_directory'],'read-consist-sttm-restart-DDL.log'), 'w')
#     f_init_err=open( ''.join( ( os.path.splitext(f_init_log.name)[0], '.err') ), 'w')
#     subprocess.call( [context['isql_path'], dsn, '-q', '-i', sql_init_ddl], stdout=f_init_log, stderr=f_init_err )
#     flush_and_close(f_init_log)
#     flush_and_close(f_init_err)
#
#     sql_addi='''
#         recreate table detl(id int, PID int references test on delete cascade on update cascade);
#         commit;
#
#         delete from test;
#         insert into test(id, x) values(2,2);
#         insert into test(id, x) values(3,3);
#         insert into test(id, x) values(5,5);
#         insert into detl(id, pid) values(2000, 2);
#         insert into detl(id, pid) values(2001, 2);
#         insert into detl(id, pid) values(2002, 2);
#         insert into detl(id, pid) values(3001, 3);
#         insert into detl(id, pid) values(5001, 5);
#         insert into detl(id, pid) values(5001, 5);
#         commit;
#     '''
#     runProgram('isql', [ dsn, '-q' ], sql_addi)
#
#     locker_tpb = fdb.TPB()
#     locker_tpb.lock_timeout = 3; # LOCKER_LOCK_TIMEOUT
#     locker_tpb.lock_resolution = fdb.isc_tpb_wait
#
#     con_lock_1 = fdb.connect( dsn = dsn, isolation_level=locker_tpb )
#     con_lock_2 = fdb.connect( dsn = dsn, isolation_level=locker_tpb )
#
#
#     #########################
#     ###  L O C K E R - 1  ###
#     #########################
#
#     con_lock_1.execute_immediate( 'update %(target_obj)s set id=id where id=5' % locals() )
#
#     sql_text='''
#         connect '%(dsn)s';
#         set list on;
#         set autoddl off;
#         set term ^;
#         execute block returns (whoami varchar(30)) as
#         begin
#             whoami = 'WORKER'; -- , ATT#' || current_connection;
#             rdb$set_context('USER_SESSION','WHO', whoami);
#             -- suspend;
#         end
#         ^
#         set term ;^
#         commit;
#         SET KEEP_TRAN_PARAMS ON;
#         set transaction read committed read consistency;
#         --select current_connection, current_transaction from rdb$database;
#         set list off;
#         set wng off;
#         --set plan on;
#         set count on;
#
#         merge into %(target_obj)s t -- THIS MUST BE LOCKED
#         using(select * from %(target_obj)s where id >= 3 order by id) s on t.id = s.id
#         when matched then
#            DELETE
#         ;
#
#         -- check results:
#         -- ###############
#
#         select id from %(target_obj)s order by id; -- this will produce output only after all lockers do their commit/rollback
#
#         select v.old_id, v.op, v.snap_no_rank
#         from v_worker_log v
#         where v.op = 'del';
#
#         rollback;
#
#     '''  % dict(globals(), **locals())
#
#     f_worker_sql=open( os.path.join(context['temp_directory'],'tmp_sttm_restart_on_merge_03.sql'), 'w')
#     f_worker_sql.write(sql_text)
#     flush_and_close(f_worker_sql)
#
#
#     f_worker_log=open( ''.join( ( os.path.splitext(f_worker_sql.name)[0], '.log') ), 'w')
#     f_worker_err=open( ''.join( ( os.path.splitext(f_worker_log.name)[0], '.err') ), 'w')
#
#     ############################################################################
#     ###  L A U N C H     W O R K E R    U S I N G     I S Q L,   A S Y N C.  ###
#     ############################################################################
#
#     p_worker = Popen( [ context['isql_path'], '-q', '-i', f_worker_sql.name ],stdout=f_worker_log, stderr=f_worker_err)
#     time.sleep(1)
#
#
#     #########################
#     ###  L O C K E R - 2  ###
#     #########################
#     con_lock_2.execute_immediate( 'update %(target_obj)s set id=4 where id=2;' % locals() )
#     con_lock_2.commit()
#     con_lock_2.execute_immediate( 'update %(target_obj)s set id=id where id=4;' % locals() )
#
#
#     con_lock_1.commit() # release record with ID=5 (allow it to be deleted by session-worker)
#
#     # Add record which did not exists when session-worker statement started.
#     # Add also child record for it, then commit + re-lock just added record:
#     con_lock_1.execute_immediate('insert into %(target_obj)s(id,x) values(6,6)' % locals())
#     con_lock_1.execute_immediate('insert into detl(id, pid) values(6001, 6)')
#     con_lock_1.commit()
#     con_lock_1.execute_immediate('update %(target_obj)s set id=id where id=6' % locals())
#
#     con_lock_2.commit() # release record with ID=4. At this point session-worker will be allowed to delete rows with ID=4 and 5.
#
#     con_lock_1.commit() # release record with ID=6. It is the last record which also must be deleted by session-worker.
#
#     # Here we wait for ISQL complete its mission:
#     p_worker.wait()
#
#     flush_and_close(f_worker_log)
#     flush_and_close(f_worker_err)
#
#     # Close lockers:
#     ################
#     for c in (con_lock_1, con_lock_2):
#         c.close()
#
#
#     # CHECK RESULTS
#     ###############
#     with open(f_worker_log.name,'r') as f:
#         for line in f:
#             if line.strip():
#                 print('checked_mode: %(checked_mode)s, STDLOG: %(line)s' % locals())
#
#     for f in (f_init_err, f_worker_err):
#         with open(f.name,'r') as g:
#             for line in g:
#                 if line.strip():
#                     print( 'checked_mode: ', checked_mode, ' UNEXPECTED STDERR IN ' + g.name + ':', line)
#
# #<for checked mode in(...)
#
# # Cleanup.
# ##########
# time.sleep(1)
# cleanup( (f_init_log, f_init_err, f_worker_sql, f_worker_log, f_worker_err) )
#
# -----------------------------------
