#coding:utf-8
#
# id:           functional.gtcs.gtcs_proc_isql_08
# title:        gtcs-proc-isql-08
# decription:   
#               	Original test see in:
#                       https://github.com/FirebirdSQL/fbtcs/blob/master/GTCS/tests/PROC_ISQL_08.script
#               	SQL script for creating test database ('gtcs_sp1.fbk') and fill it with some data:
#                       https://github.com/FirebirdSQL/fbtcs/blob/master/GTCS/tests/PROCS_QA_INIT_ISQL.script
#                   Checked on: 4.0.0.1803 SS; 3.0.6.33265 SS; 2.5.9.27149 SC.
#                'd_atabase': 'Restore',
#                'b_ackup_file': 'gtcs_sp1.fbk',
#               
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

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """
    set bail on;

    recreate table sp (
        sno  varchar(6),
        pno  varchar(6),
        qty  integer
    );
    commit;

    insert into sp (sno, pno, qty) values ('S1', 'P1', 300);
    insert into sp (sno, pno, qty) values ('S1', 'P3', 400);
    insert into sp (sno, pno, qty) values ('S2', 'P1', 300);
    insert into sp (sno, pno, qty) values ('S2', 'P2', 400);
    insert into sp (sno, pno, qty) values ('S4', 'P4', 300);
    insert into sp (sno, pno, qty) values ('S4', 'P5', 400);
    commit;


    set term ^;
    create procedure proc08 returns (a char(5), b char(5), c integer) as
    begin
        for
            select * from sp
            into :a, :b, :c
        do
            suspend;
    end
    ^
    set term ;^

    set count on;

    execute procedure proc08;
    
    select 'point-1' msg, p.a, p.b, p.c from proc08 p order by 2,3,4;

    select 'point-2' msg, max(p.c) from proc08 p;
    
    select 'point-3' msg, p.a from proc08 p order by 2;

    select 'point-4' msg, p.* from proc08 p order by p.c, p.a, p.b;

    select 'point-5' msg, p.a, avg(p.c) from proc08 p group by a having avg(p.c) > 300 order by p.a;
    select 'point-6' msg, p.a, avg(p.c) from proc08 p group by p.a order by p.a;

    select 'point-7' msg, p.a, p.c from proc08 p where p.c < (select avg(x.c) from proc08 x) order by p.a, p.c;
  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    A      B                 C
    ====== ====== ============
    S1     P1              300

    MSG     A      B                 C
    ======= ====== ====== ============
    point-1 S1     P1              300
    point-1 S1     P3              400
    point-1 S2     P1              300
    point-1 S2     P2              400
    point-1 S4     P4              300
    point-1 S4     P5              400
    Records affected: 6

    MSG              MAX
    ======= ============
    point-2          400
    Records affected: 1

    MSG     A
    ======= ======
    point-3 S1
    point-3 S1
    point-3 S2
    point-3 S2
    point-3 S4
    point-3 S4
    Records affected: 6

    MSG     A      B                 C
    ======= ====== ====== ============
    point-4 S1     P1              300
    point-4 S2     P1              300
    point-4 S4     P4              300
    point-4 S1     P3              400
    point-4 S2     P2              400
    point-4 S4     P5              400
    Records affected: 6

    MSG     A                        AVG
    ======= ====== =====================
    point-5 S1                       350
    point-5 S2                       350
    point-5 S4                       350
    Records affected: 3

    MSG     A                        AVG
    ======= ====== =====================
    point-6 S1                       350
    point-6 S2                       350
    point-6 S4                       350
    Records affected: 3

    MSG     A                 C
    ======= ====== ============
    point-7 S1              300
    point-7 S2              300
    point-7 S4              300
    Records affected: 3
  """

@pytest.mark.version('>=2.5')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_expected_stdout == act_1.clean_stdout

