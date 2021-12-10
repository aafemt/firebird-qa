#coding:utf-8
#
# id:           bugs.core_6095
# title:        Extend trace record for COMMIT/ROLLBACK RETAINING to allow chaining of transaction ids
# decription:
#                   Test prepares trace config with requrement to watch only for TRANSACTION events.
#                   Then it starts trace session and makes several changes withing retained Tx.
#                   (this is done by invocation con.commit() method with argument 'retaining = True').
#
#                   Every COMMIT_RETAINING event in the trace log must contain following *new* elements:
#                   1) "INIT_" token with ID of transaction that originated changes; it must be shown in the same line with "TRA_" info;
#                   2) "New number <NN>" - ID that will be assigned to the next transaction in this 'chain'; it must be shown in separate line.
#
#                   All lines containing "INIT_" must have the same value of transaction that started changes but this value itself can depend
#                   on FB major version and (maybe) of server mode: CS / SC /SS. For this reason we must save this number as special 'base' that
#                   will be subtracted from concrete values during parsing of trace lines - see 'tx_base' variable here.
#
#                   We parse trace log and pay attention for lines like: "(TRA_nnn, INIT_mmm, ..."  and "New number <XXX>".
#                   Each interesting numbers are extracted from these lines and <tx_base> is subtracted from them.
#                   Finally, we display resulting values.
#                   1) number after phrase "Tx that is origin of changes:" must always be equal to zero;
#                   2) number after phrase "Tx that finished now" must be:
#                     2.1) LESS for 1 than value in the next line: "NEW NUMBER" for subsequent Tx..." - for all DML statements EXCEPT LAST;
#                     2.2) EQUALS to "NEW NUMBER" for subsequent Tx..." for LAST statement because it does not change anything (updates empty table);
#
#                   Checked on 4.0.0.1784 SS: 6.327s; 3.0.6.33255 SS: 5.039s.
#
# tracker_id:   CORE-6095
# min_versions: ['3.0.6']
# versions:     3.0.6
# qmid:         None

import pytest
import re
from firebird.qa import db_factory, python_act, Action

# version: 3.0.6
# resources: None

substitutions_1 = []

init_script_1 = """
    create sequence g;
    create table test(id int primary key, x int);
    set term ^;
    create trigger test_bi for test active before insert position 0 as
    begin
       new.id = coalesce(new.id, gen_id(g, 1) );
    end
    ^
    create procedure sp_worker(a_x int) as
    begin
        insert into test(x) values(:a_x);
    end
    ^
    set term ;^
    commit;
"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

# test_script_1
#---
# import os
#  import re
#  import time
#  import subprocess
#  from subprocess import Popen
#  from fdb import services
#
#  os.environ["ISC_USER"] = user_name
#  os.environ["ISC_PASSWORD"] = user_password
#
#  fdb_name = os.path.split(db_conn.database_name)[1]
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
#            del_name = None
#
#         if del_name and os.path.isfile( del_name ):
#             os.remove( del_name )
#
#  #--------------------------------------------
#
#  # Prepare config for trace session that will be launched:
#  #########################################################
#  txt = '''
#      database= %%[\\\\\\\\/]%(fdb_name)s
#      {
#          enabled = true
#          log_initfini = false
#          time_threshold = 0
#          log_transactions = true
#      }
#  ''' % locals()
#
#  trc_cfg=open( os.path.join(context['temp_directory'],'tmp_trace_6095.cfg'), 'w')
#  trc_cfg.write(txt)
#  flush_and_close( trc_cfg )
#
#  # Async. launch of trace session using FBSVCMGR action_trace_start:
#  ###################################################################
#  trc_log=open( os.path.join(context['temp_directory'],'tmp_trace_6095.log'), 'w', buffering = 0)
#  # Execute a child program in a new process, redirecting STDERR to the same target as of STDOUT:
#  p_svcmgr = Popen( [ context['fbsvcmgr_path'], "localhost:service_mgr",
#                      "action_trace_start",
#                      "trc_cfg", trc_cfg.name
#                    ],
#                    stdout=trc_log,
#                    stderr=subprocess.STDOUT
#                  )
#
#  # 08.01.2020. This delay is mandatory, otherwise file with trace session info can remain (sometimes)
#  # empty when we will read it at the next step:
#  time.sleep(1)
#
#  # Determine active trace session ID (for further stop):
#  #######################################################
#  trc_lst=open( os.path.join(context['temp_directory'],'tmp_trace_6095.lst'), 'w', buffering = 0)
#  subprocess.call([context['fbsvcmgr_path'], "localhost:service_mgr",
#                   "action_trace_list"],
#                   stdout=trc_lst, stderr=subprocess.STDOUT
#                 )
#  flush_and_close( trc_lst )
#
#  # Session ID: 5
#  #   user:
#  #   date:  2015-08-27 15:24:14
#  #   flags: active, trace
#
#  sid_pattern = re.compile('Session\\s+ID[:]{0,1}\\s+\\d+', re.IGNORECASE)
#
#  trc_ssn=0
#  with open( trc_lst.name,'r') as f:
#      for line in f:
#          if sid_pattern.search( line ) and len( line.split() ) == 3:
#              trc_ssn = line.split()[2]
#              break
#
#  # Result: `trc_ssn` is ID of active trace session.
#  # We have to terminate trace session that is running on server BEFORE we termitane process `p_svcmgr`
#
#  if trc_ssn==0:
#      print("Error parsing trace session ID.")
#
#  else:
#
#      ###########   W O R K    W I T H    D A T A B A S E    ########
#
#      con = fdb.connect( dsn = dsn )
#      cur = con.cursor()
#
#      con.execute_immediate( 'insert into test(x) values(123)' )
#      con.commit( retaining = True )                            # (TRA_12, ... ; next line: "New number 13"
#
#      cur.callproc( 'sp_worker', (456,) )                       # (TRA_13, INIT_12, ...
#      con.commit( retaining = True )                            # (TRA_13, INIT_12, ... ; next line: "New number 14"
#
#      con.execute_immediate( 'delete from test' )               # (TRA_14, INIT_12, ...
#      con.commit( retaining = True )                            # (TRA_14, INIT_12, ... ; next line: "New number 15"
#
#      # This statement does not change anything:
#      con.execute_immediate( 'update test set x = -x' )         # (TRA_15, INIT_12, ...
#      con.commit( retaining = True )                            # (TRA_15, INIT_12, ... ; next line: "New number 15" -- THE SAME AS PREVIOUS!
#
#      cur.close()
#      #####################################################################
#
#      # ::: NB ::: Here we have to be idle at least 2s (two seconds) otherwise trace log will
#      # not contain some or all of messages about create DB, start Tx, ES, Tx and drop DB.
#      # See also discussion with hvlad, 08.01.2020 15:16
#      # (subj: "action_trace_stop does not flush trace log (fully or partially)")
#      time.sleep(2)
#
#      # Stop trace session:
#      #####################
#
#      trc_lst=open(trc_lst.name, "a")
#      trc_lst.seek(0,2)
#
#      subprocess.call( [ context['fbsvcmgr_path'], "localhost:service_mgr",
#                         "action_trace_stop",
#                         "trc_id",trc_ssn
#                       ],
#                       stdout=trc_lst,
#                       stderr=subprocess.STDOUT
#                     )
#      flush_and_close( trc_lst )
#
#      p_svcmgr.terminate()
#
#
#      allowed_patterns = [
#          re.compile('\\s*\\(TRA_\\d+,', re.IGNORECASE)
#         ,re.compile('\\s*New\\s+number\\s+\\d+\\s*', re.IGNORECASE)
#      ]
#
#      tx_base = -1
#      with open( trc_log.name,'r') as f:
#          for line in f:
#              if line.rstrip().split():
#                  for p in allowed_patterns:
#                      if p.search(line):
#                          if '(TRA_' in line:
#                              words = line.replace(',',' ').replace('_',' ').replace('(',' ').split()
#                              # Result:
#                              # 1) for tx WITHOUT retaining: ['TRA', '12', 'READ', 'COMMITTED', '|', 'REC', 'VERSION', '|', 'WAIT', '|', 'READ', 'WRITE)']
#                              # 2) for tx which is RETAINED: ['TRA', '13', 'INIT', '12', 'READ', 'COMMITTED', '|', 'REC', 'VERSION', '|', 'WAIT', '|', 'READ', 'WRITE)']
#                              #                                 0      1     2       3
#
#                              tx_base = int(words[1]) if tx_base == -1 else tx_base
#
#                              if words[2] == 'INIT':
#                                 tx_origin_of_changes = int(words[3]) - tx_base
#                                 tx_that_finished_now = int(words[1]) - tx_base
#                                 print('Found "INIT_" token in "TRA_" record. Tx that is origin of changes: ', tx_origin_of_changes, '; Tx that finished now:', tx_that_finished_now)
#                          elif 'number' in line:
#                              tx_for_subsequent_changes = int(line.split()[2]) - tx_base # New number 15 --> 15
#                              print('Found record with "NEW NUMBER" for subsequent Tx numbers: ', tx_for_subsequent_changes)
#
#
#  #< cond "if trc_ssn>0"
#  flush_and_close( trc_log )
#
#
#  # cleanup:
#  ##########
#  time.sleep(1)
#  cleanup( (trc_lst, trc_cfg, trc_log) )
#
#---

act_1 = python_act('db_1', substitutions=substitutions_1)

expected_stdout_1 = """
    Found record with "NEW NUMBER" for subsequent Tx numbers:  1
    Found "INIT_" token in "TRA_" record. Tx that is origin of changes:  0 ; Tx that finished now: 1
    Found record with "NEW NUMBER" for subsequent Tx numbers:  2
    Found "INIT_" token in "TRA_" record. Tx that is origin of changes:  0 ; Tx that finished now: 2
    Found record with "NEW NUMBER" for subsequent Tx numbers:  3
    Found "INIT_" token in "TRA_" record. Tx that is origin of changes:  0 ; Tx that finished now: 3
    Found record with "NEW NUMBER" for subsequent Tx numbers:  3
    Found "INIT_" token in "TRA_" record. Tx that is origin of changes:  0 ; Tx that finished now: 3
"""

trace_1 = ['log_initfini = false',
           'log_transactions = true',
           'time_threshold = 0'
           ]

@pytest.mark.version('>=3.0.6')
def test_1(act_1: Action, capsys):
    allowed_patterns = [re.compile('\\s*\\(TRA_\\d+,', re.IGNORECASE),
                        re.compile('\\s*New\\s+number\\s+\\d+\\s*', re.IGNORECASE),
                        ]
    with act_1.trace(db_events=trace_1):
        with act_1.db.connect() as con:
            cur = con.cursor()
            con.execute_immediate('insert into test(x) values(123)')
            con.commit(retaining = True)                    # (TRA_12, ... ; next line: "New number 13"
            cur.callproc('sp_worker', [456])                # (TRA_13, INIT_12, ...
            con.commit(retaining = True)                    # (TRA_13, INIT_12, ... ; next line: "New number 14"
            con.execute_immediate('delete from test')       # (TRA_14, INIT_12, ...
            con.commit(retaining = True)                    # (TRA_14, INIT_12, ... ; next line: "New number 15"
            # This statement does not change anything:
            con.execute_immediate('update test set x = -x') # (TRA_15, INIT_12, ...
            con.commit(retaining = True)                    # (TRA_15, INIT_12, ... ; next line: "New number 15" -- THE SAME AS PREVIOUS!
    # Process trace
    tx_base = -1
    for line in act_1.trace_log:
        if line.rstrip().split():
            for p in allowed_patterns:
                if p.search(line):
                    if '(TRA_' in line:
                        words = line.replace(',',' ').replace('_',' ').replace('(',' ').split()
                        # Result:
                        # 1) for tx WITHOUT retaining: ['TRA', '12', 'READ', 'COMMITTED', '|', 'REC', 'VERSION', '|', 'WAIT', '|', 'READ', 'WRITE)']
                        # 2) for tx which is RETAINED: ['TRA', '13', 'INIT', '12', 'READ', 'COMMITTED', '|', 'REC', 'VERSION', '|', 'WAIT', '|', 'READ', 'WRITE)']
                        #                                 0      1     2       3
                        tx_base = int(words[1]) if tx_base == -1 else tx_base
                        if words[2] == 'INIT':
                            tx_origin_of_changes = int(words[3]) - tx_base
                            tx_that_finished_now = int(words[1]) - tx_base
                            print('Found "INIT_" token in "TRA_" record. Tx that is origin of changes: ', tx_origin_of_changes, '; Tx that finished now:', tx_that_finished_now)
                    elif 'number' in line:
                        tx_for_subsequent_changes = int(line.split()[2]) - tx_base # New number 15 --> 15
                        print('Found record with "NEW NUMBER" for subsequent Tx numbers: ', tx_for_subsequent_changes)
    #
    act_1.expected_stdout = expected_stdout_1
    act_1.stdout = capsys.readouterr().out
    assert act_1.clean_stdout == act_1.clean_expected_stdout
