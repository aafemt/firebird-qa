#coding:utf-8
#
# id:           functional.gtcs.gtcs_proc_isql_13
# title:        gtcs-proc-isql-13
# decription:   
#               	Original test see in:
#                       https://github.com/FirebirdSQL/fbtcs/blob/master/GTCS/tests/PROC_ISQL_13.script
#               	SQL script for creating test database ('gtcs_sp1.fbk') and fill it with some data:
#                       https://github.com/FirebirdSQL/fbtcs/blob/master/GTCS/tests/PROCS_QA_INIT_ISQL.script
#                   Checked on:
#                       4.0.0.1803 SS: 1.822s.
#                       3.0.6.33265 SS: 0.849s.
#                       2.5.9.27149 SC: 0.313s.
#                
# tracker_id:   
# min_versions: ['2.5.0']
# versions:     2.5
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 2.5
# resources: None

substitutions_1 = [('=', ''), ('[ \t]+', ' ')]

init_script_1 = """"""

db_1 = db_factory(from_backup='gtcs_sp1.fbk', init=init_script_1)

test_script_1 = """
    set bail on;
    set term ^;
    create procedure proc13 returns (a integer) as
    begin
        for
            select status from s
            UNION
            select weight from p
            into :a
        do
            suspend;
    end
    ^
    set term ;^

    execute procedure proc13 ;

    select 'point-1' msg, p.* from proc13 p;
    select 'point-2' msg, max(p.a) from proc13 p;
    select 'point-3' msg, p.a from proc13 p;
    select 'point-4' msg, p.a from proc13 p order by a;
    select 'point-5' msg, p.a, avg(p.a) from proc13 p group by p.a having avg(p.a) > 20;
    select 'point-6' msg, p.a, avg(p.a) from proc13 p group by p.a;
    select 'point-7' msg, p.a from proc13 p where p.a > (select avg(x.a) from proc13 x);


  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    A
    10


    MSG                A
    point-1           10
    point-1           12
    point-1           14
    point-1           17
    point-1           19
    point-1           20
    point-1           30

    MSG              MAX
    point-2           30

    MSG                A
    point-3           10
    point-3           12
    point-3           14
    point-3           17
    point-3           19
    point-3           20
    point-3           30

    MSG                A
    point-4           10
    point-4           12
    point-4           14
    point-4           17
    point-4           19
    point-4           20
    point-4           30

    MSG                A                   AVG
    point-5           30                    30

    MSG                A                   AVG
    point-6           10                    10
    point-6           12                    12
    point-6           14                    14
    point-6           17                    17
    point-6           19                    19
    point-6           20                    20
    point-6           30                    30

    MSG                A
    point-7           19
    point-7           20
    point-7           30
  """

@pytest.mark.version('>=2.5')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_expected_stdout == act_1.clean_stdout

