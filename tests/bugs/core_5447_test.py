#coding:utf-8
#
# id:           bugs.core_5447
# title:        EXECUTE STATEMENT <e> when <e> starts with '--' issues -Unexpected ... column <NNN>, value <NNN> is invalid and can change randomly
# decription:
#                  We run EB that is show in the ticket three times, with redirection STDOUT and STDERR to separate files.
#                  Then we open file of STDERR and parse it: search for lines which contain "-Unexpected end of command" text.
#                  Extract nineth word from this and add it to Python structure of type = SET.
#                  Finally, we check that this set:
#                  1) all columns are positive integers;
#                  2) contains only one element (i.e. all columns have the same value).
#
#                  Checked on 3.0.02.32684, 4.0.0.531 - all fine.
#
# tracker_id:   CORE-5447
# min_versions: ['3.0.2']
# versions:     3.0.2
# qmid:         None

import pytest
from firebird.qa import db_factory, python_act, Action

# version: 3.0.2
# resources: None

substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

# test_script_1
#---
#
#  import os
#  import sys
#
#  os.environ["ISC_USER"] = user_name
#  os.environ["ISC_PASSWORD"] = user_password
#
#  so=sys.stdout
#  se=sys.stderr
#
#
#  f_sql_log=os.path.join(context['temp_directory'],'tmp_c5447.log')
#  f_sql_err=os.path.join(context['temp_directory'],'tmp_c5447.err')
#
#  sys.stdout = open( f_sql_log, 'w')
#  sys.stderr = open( f_sql_err, 'w')
#
#  es_sql='''
#    set term ^;
#    execute block as
#    begin
#        execute statement '-- table ''test'' has no trigger, DROP TRIGGER is skipped.';
#    end
#    ^
#    execute block as
#    begin
#        execute statement '-- table ''test'' has no trigger, DROP TRIGGER is skipped.';
#    end
#    ^
#    execute block as
#    begin
#        execute statement '-- table ''test'' has no trigger, DROP TRIGGER is skipped.';
#    end
#    ^
#    set term ;^
#  '''
#  runProgram('isql',[dsn], es_sql)
#
#  sys.stdout = so
#  sys.stderr = se
#
#  col_set=set()
#  with open( f_sql_err, 'r') as f:
#      for line in f:
#         if '-Unexpected end of command' in line:
#             # -Unexpected end of command - line 0, column -45949567
#             #    0         1  2    3     4   5  6    7       8
#             col_number=line.split()[8]
#             print( 'OK: column is integer > 0' if col_number.isdigit() and str(col_number) > 0 else 'FAIL: column is ZERO, NEGATIVE or NaN' )
#             col_set.add( line.split()[8] )
#
#  print( 'OK: all columns are the same' if len(col_set)==1 else 'FAIL: columns differ or empty set()' )
#
#  os.remove(f_sql_log)
#  os.remove(f_sql_err)
#
#---

act_1 = python_act('db_1', substitutions=substitutions_1)

test_script_1 = """
    set term ^;
    execute block as
    begin
        execute statement '-- table ''test'' has no trigger, DROP TRIGGER is skipped.';
    end
    ^
    execute block as
    begin
        execute statement '-- table ''test'' has no trigger, DROP TRIGGER is skipped.';
    end
    ^
    execute block as
    begin
        execute statement '-- table ''test'' has no trigger, DROP TRIGGER is skipped.';
    end
    ^
    set term ;^
"""

@pytest.mark.version('>=3.0.2')
def test_1(act_1: Action):
    act_1.expected_stderr = "We expect errors"
    act_1.isql(switches=[], input=test_script_1)
    col_set = set()
    for line in act_1.stderr.splitlines():
        if '-Unexpected end of command' in line:
            # -Unexpected end of command - line 0, column -45949567
            #    0         1  2    3     4   5  6    7       8
            col_number = line.split()[8]
            assert col_number.isdigit() and int(col_number) > 0, "column is ZERO, NEGATIVE or NaN"
            col_set.add(col_number)
    assert len(col_set) == 1, "columns differ or empty set()"
