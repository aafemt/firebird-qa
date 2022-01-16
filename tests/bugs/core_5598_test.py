#coding:utf-8
#
# id:           bugs.core_5598
# title:        Error "block size exceeds implementation restriction" while inner joining large datasets with a long key using the HASH JOIN plan
# decription:
#                   Hash join have to operate with keys of total length >= 1 Gb if we want to reproduce runtime error
#                   "Statement failed, SQLSTATE = HY001 / unable to allocate memory from operating system"
#                   If test table that serves as the source for HJ has record length about 65 Kb than not less than 16K records must be added there.
#                   If we use charset UTF8 than record length in bytes will be 8 times of declared field_len, so we declare field with len = 8191 charactyer
#                   (and this is current implementation limit).
#                   Than we add into this table >= 16Kb rows of unicode (NON-ascii!) characters.
#                   Finally, we launch query against this table and this query will use hash join because of missed indices.
#                   We have to check that NO errors occured during this query.
#
#                   Discuss with dimitr: letters 08-jan-2018 .. 06-feb-2018.
#                   Confirmed bug on:
#                       3.0.3.32838
#                       4.0.0.838
#                   Works fine on:
#                       3.0.4.32939 (SS, CS) - time ~ 29-32"
#                       4.0.0.945   (SS, CS) - time ~ 29-32"
#
# tracker_id:   CORE-5598
# min_versions: ['3.0.3']
# versions:     3.0.3
# qmid:         None

import pytest
from firebird.qa import db_factory, python_act, Action

# version: 3.0.3
# resources: None

substitutions_1 = [('[ \t]+', ' '), ('.*RECORD LENGTH:[ \t]+[\\d]+[ \t]*\\)', ''),
                   ('.*COUNT[ \t]+[\\d]+', ''), ('(?m)DATABASE:.*\\n?', '')]

init_script_1 = """"""

db_1 = db_factory(charset='UTF8', sql_dialect=3, init=init_script_1)

# test_script_1
#---
# import sys
#  import os
#  import subprocess
#  from subprocess import Popen
#  from fdb import services
#  import time
#
#  os.environ["ISC_USER"] = user_name
#  os.environ["ISC_PASSWORD"] = user_password
#  fdb_file=db_conn.database_name
#  db_conn.close()
#
#  # Threshold: minimal records that is to be inserted in order to reproduce runtime exception
#  # 'unable to allocate memory from OS':
#  MIN_RECS_TO_ADD = 17000
#
#  fbs = fdb.services.connect( host = 'localhost:service_mgr' )
#  fbs.set_write_mode( database = fdb_file, mode = fdb.services.WRITE_BUFFERED )
#  fbs.close()
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
#  db_conn=fdb.connect(dsn = dsn, charset = 'utf8')
#  db_conn.execute_immediate( 'create table test(id int, s varchar(8191))' )
#  db_conn.commit()
#  cur=db_conn.cursor()
#  cur.execute( "insert into test( id, s ) select row_number()over(), lpad('', 8191, 'Алексей, Łukasz, Máté, François, Jørgen, Νικόλαος') from rdb$types,rdb$types rows %d" % MIN_RECS_TO_ADD)
#  db_conn.commit()
#  db_conn.close()
#
#  isql_cmd='''
#      set list on;
#      --show version;
#      set explain on;
#      select count(*) from test a join test b using(id, s);
#      set explain off;
#      quit;
#      select
#           m.MON$STAT_ID
#          ,m.MON$STAT_GROUP
#          ,m.MON$MEMORY_USED
#          ,m.MON$MEMORY_ALLOCATED
#          ,m.MON$MAX_MEMORY_USED
#          ,m.MON$MAX_MEMORY_ALLOCATED
#      from mon$database d join mon$memory_usage m using (MON$STAT_ID)
#      ;
#  '''
#
#  isql_run=open( os.path.join(context['temp_directory'],'tmp_isql_5596.sql'), 'w')
#  isql_run.write( isql_cmd )
#  isql_run.close()
#
#  #-----------------------------------
#  isql_log=open( os.path.join(context['temp_directory'],'tmp_isql_5596.log'), 'w')
#  isql_err=open( os.path.join(context['temp_directory'],'tmp_isql_5596.err'), 'w')
#
#  p_isql = subprocess.call( [context['isql_path'], dsn, '-i', isql_run.name ], stdout=isql_log, stderr=isql_err )
#
#  flush_and_close( isql_log )
#  flush_and_close( isql_err )
#
#
#  # do NOT remove this delay:
#  time.sleep(1)
#
#  # STDOUT must contain:
#  #   Select Expression
#  #       -> Aggregate
#  #           -> Filter
#  #               -> Hash Join (inner)
#  #                   -> Table "TEST" as "B" Full Scan
#  #                   -> Record Buffer (record length: 32793)
#  #                       -> Table "TEST" as "A" Full Scan
#  #
#  #   COUNT                           17000
#
#  with open(isql_log.name,'r') as f:
#      for line in f:
#          if line.rstrip():
#              print('STDOUT:' + line.upper() )
#
#  with open(isql_err.name,'r') as f:
#      for line in f:
#          if line.rstrip():
#              print('UNEXPECTED STDERR:' + line.upper() )
#
#
#  # cleanup:
#  ##########
#  time.sleep(1)
#  cleanup( ( isql_run, isql_log, isql_err ) )
#
#---

act_1 = python_act('db_1', substitutions=substitutions_1)

expected_stdout_1 = """
    SELECT EXPRESSION
     -> AGGREGATE
     -> FILTER
     -> HASH JOIN (INNER)
     -> TABLE "TEST" AS "B" FULL SCAN
     -> RECORD BUFFER (RECORD LENGTH: 32793)
     -> TABLE "TEST" AS "A" FULL SCAN
    COUNT 17000
"""

MIN_RECS_TO_ADD = 17000

test_script_1 = """
    set list on;
    --show version;
    set explain on;
    select count(*) from test a join test b using(id, s);
    set explain off;
    quit;
    select
         m.MON$STAT_ID
        ,m.MON$STAT_GROUP
        ,m.MON$MEMORY_USED
        ,m.MON$MEMORY_ALLOCATED
        ,m.MON$MAX_MEMORY_USED
        ,m.MON$MAX_MEMORY_ALLOCATED
    from mon$database d join mon$memory_usage m using (MON$STAT_ID);
"""

@pytest.mark.version('>=3.0.3')
def test_1(act_1: Action):
    with act_1.db.connect(charset='utf8') as con:
        con.execute_immediate('create table test(id int, s varchar(8191))')
        con.commit()
        c = con.cursor()
        c.execute(f"insert into test(id, s) select row_number()over(), lpad('', 8191, 'Алексей, Łukasz, Máté, François, Jørgen, Νικόλαος') from rdb$types,rdb$types rows {MIN_RECS_TO_ADD}")
        con.commit()
    #
    act_1.expected_stdout = expected_stdout_1
    act_1.isql(switches=['-q'], input=test_script_1)
    act_1.stdout = act_1.stdout.upper()
    assert act_1.clean_stdout == act_1.clean_expected_stdout
