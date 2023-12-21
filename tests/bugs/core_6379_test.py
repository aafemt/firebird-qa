#coding:utf-8

"""
ID:          issue-6618
ISSUE:       6618
TITLE:       Bugcheck 179
DESCRIPTION:
  Could not reproduce with scenario described in the ticket.
  Test uses steps described by letter from me to Vlad, date: 15-JUL-2020 10:53 (subj: "read consistency tests").
  Scripts for initial test can be found here:
  https://drive.google.com/drive/folders/1CEOSVfOMHzlZ1F3Gi0Jv3TEbvWLs9DPR?usp=sharing

  Reproduced problem on 4.0.0.2108 SS:
  1. Content of firebird.log:
        deadlock
        update conflicts with concurrent update
        concurrent transaction number is 12
        internal Firebird consistency check (wrong record version (185), file: Savepoint.cpp line: 267)
  2. Client gets:
    Statement failed, SQLSTATE 08006
    Error reading data from the connection.

    Statement failed, SQLSTATE 08006
    Error writing data to the connection.
    -send_packet/send
JIRA:        CORE-6379
FBTEST:      bugs.core_6379
NOTES:
    [25.11.2023] pzotov
    Writing code requires more care since 6.0.0.150: ISQL does not allow to specify THE SAME terminator twice,
    i.e.
    set term @; select 1 from rdb$database @ set term @; - will not compile ("Unexpected end of command" raises).
"""

import pytest
import subprocess
import time
from pathlib import Path
from firebird.qa import *

init_script = """
    set echo on ;
    set bail on ;
    create table test(id int generated by default as identity, x int, s varchar(32765) ) ;
    set term ^ ;
    execute block as
        declare n_limit int = 1000 ;
        declare i int = 1 ;
    begin
       rdb$set_context('USER_SESSION', 'N_LIMIT', n_limit) ;
       while (i <= n_limit) do
       begin
           insert into test (x, s) values (0, lpad('', 32700, uuid_to_char(gen_uuid()))) ;
           i = i + 1 ;
       end
    end ^
    set term ;^
    commit ;

    delete from test order by id rows (cast(rdb$get_context('USER_SESSION', 'N_LIMIT') as int) - 13) ;
    commit ;
"""

db = db_factory() # We run init_script manually

act = python_act('db', substitutions=[('=', ''), ('[ \t]+', ' ')])

test_script = """
set autoddl off;
commit;
set transaction read committed read consistency;
set count on;

set bail on;
delete from test;

set heading on;
select rdb$db_key, id, x from test order by rdb$db_key;
"""

expected_stdout = """
    Records affected: 14
    Records affected: 0
"""

worker_script = temp_file('core_6379.sql')
worker_output = temp_file('core_6379.out')

@pytest.mark.version('>=4.0')
def test_1(act: Action, worker_script: Path, worker_output: Path):
    worker_script.write_text(test_script)
    # Run init_script
    act.isql(switches=[], input=init_script)
    #
    with act.db.connect() as con_lock_1, act.db.connect() as con_lock_2:
        # Locker 1
        con_lock_1.execute_immediate('update test set x = -1111 order by id rows 6 to 6')
        # Scenario for WORKER
        with open(worker_output, mode='w') as worker_out:
            p_worker_sql = subprocess.Popen([act.vars['isql'], '-pag', '9999', '-q',
                                             '-i', str(worker_script),
                                             '-user', act.db.user,
                                             '-password', act.db.password, act.db.dsn],
                                            stdout=worker_out, stderr=subprocess.STDOUT)
            try:
                time.sleep(2)
                # Locker 2
                con_lock_2.execute_immediate('insert into test (x) values (3333)')
                con_lock_2.commit()
                # Locker 1
                con_lock_1.commit()
            finally:
                # Here we wait for ISQL complete its mission
                p_worker_sql.wait()
    # Check
    act.expected_stdout = expected_stdout
    act.stdout = worker_output.read_text()
    assert act.clean_stdout == act.clean_expected_stdout
