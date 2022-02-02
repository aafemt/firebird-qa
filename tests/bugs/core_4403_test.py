#coding:utf-8

"""
ID:          issue-4725
ISSUE:       4725
TITLE:       Allow referencing cursors as record variables in PSQL
DESCRIPTION:
JIRA:        CORE-4403
FBTEST:      bugs.core_4403
"""

import pytest
from firebird.qa import *

init_script = """
    recreate table t1(id int primary key, x int, y int);
    recreate table t2(id int primary key, x int, y int);
    recreate table t3(id int primary key, x int, y int);
    commit;
    insert into t1 values(1, 10, 11);
    commit;
    insert into t2 values(2, 10, 22);
    commit;
    insert into t3 values(3, 10, 33);
    commit;
    set term ^;
    create or alter procedure sp_test(a_x int) returns(o_y int) as
    begin
        o_y = 2 * a_x;
        suspend;
    end
    ^
    set term ;^
    commit;
"""

db = db_factory(init=init_script)

test_script = """
    set list on;
    set term ^;
    execute block returns(
       t1_id int, t1_x int, t1_y int
      ,t2_id int, t2_x int, t2_y int
      ,t3_id int, t3_x int, t3_y int
    ) as
    begin
      for
        select id, x, y from t1 as cursor c1
      do begin
        for select id, x, y from t2 where x = :c1.x as cursor c2 do
        begin
          for select id, x, y from t3 where x = :c1.x as cursor c3 do
          begin

            t1_id = c1.id;
            t1_x  = c1.x;
            t1_y  = c1.y;

            t2_id = c2.id;
            t2_x  = c2.x;
            t2_y  = c2.y;

            t3_id = c3.id;
            t3_x  = c3.x;
            t3_y  = c3.y;

            suspend;
          end
        end
      end
    end
    ^

    -- This should raise exception "attempted update of read-only column", sample has been taken from:
    -- sql.ru/forum/actualutils.aspx?action=gotomsg&tid=1158905&msg=17704102
    execute block as
    begin
      for select x, y from t1 as cursor ce do ce.x = ce.y + 1;
    end
    ^

    --/********************
    --### 29.05.2015. TODO ### UNCOMMENT LATER, AFTER FIX CORE-4819. CURRENTLY IT LEADS FB TO HANG / CRASH.

    -- Uncomment 06.08.2018:
    execute block returns(old_y int, new_y int) as
    begin
      for
          select x, y from t1
          as cursor ce
      do begin
          old_y = ce.y;
          execute procedure sp_test(ce.x) returning_values(ce.y);
          new_y = ce.y;
          suspend;
      end
    end
    ^
    -- ********************/

    set term ;^
    commit;
    set  list off;
"""

act = isql_act('db', test_script)

expected_stdout = """
   T1_ID                           1
   T1_X                            10
   T1_Y                            11
   T2_ID                           2
   T2_X                            10
   T2_Y                            22
   T3_ID                           3
   T3_X                            10
   T3_Y                            33
"""

# version: 3.0

expected_stderr_1 = """
    Statement failed, SQLSTATE = 42000
    attempted update of read-only column

    Statement failed, SQLSTATE = 42000
    attempted update of read-only column
"""

@pytest.mark.version('>=3.0,<4.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.expected_stderr = expected_stderr_1
    act.execute()
    assert (act.clean_stderr == act.clean_expected_stderr and
            act.clean_stdout == act.clean_expected_stdout)

# version: 4.0

expected_stderr_2 = """
    Statement failed, SQLSTATE = 42000
    attempted update of read-only column CE.X

    Statement failed, SQLSTATE = 42000
    attempted update of read-only column CE.Y
"""

@pytest.mark.version('>=4.0')
def test_2(act: Action):
    act.expected_stdout = expected_stdout
    act.expected_stderr = expected_stderr_2
    act.execute()
    assert (act.clean_stderr == act.clean_expected_stderr and
            act.clean_stdout == act.clean_expected_stdout)

