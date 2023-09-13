#coding:utf-8
"""
ID:          issue-7350
ISSUE:       https://github.com/FirebirdSQL/firebird/issues/7350
TITLE:       SKIP LOCKED clause for SELECT WITH LOCK, UPDATE and DELETE
DESCRIPTION: test verifies ability to get records from table which already has several locked rows by another transaction.
             Check performs for several type of queries:
                 1) DSQL 
                 2) PSQL which uses static SQL code
                 3) PSQL which uses ES/EDS mechanism.
             Two type of access mode is checked: READ and READ_WRITE
             Both WAIT and NO WAIT modes are used, but for WAIT we have to skip exectuion for TABLE STABILITY and RC NO_REC_VER.
             All kinds of transaction isolation levels are involved: TABLE STABILITY; SNAPSHOT; RC READ_CONSISTENCY; RC REC_VER and RC NO_REC_VER.
NOTES:
    [27.02.2023] pzotov
    ::: NB :::
    1) Parameter ReadConsistency in firebird.conf must be set to 0, i.e. NOT-default value.
    2) Query that uses TIL = "RC NO_record_version" actually can not obtain any records, despite usage of SKIP LOCKED clause. It always fail with:
       "-read conflicts with concurrent update / -concurrent transaction number is ..."
    3) NB: only persistent table is checked. For GTT it is unable to run 'select ... with lock' or 'update/delete ... skip locked'
       (using two transactions for single attach): exception raises with message: "SQLSTATE = HY000 / Cannot select temporary table ... WITH LOCK"
       Discussed with dimitr and hvlad, 13.09.2023

    Checked on 5.0.0.959 SS/CS.

    [13.09.2023] pzotov
    1. Removed limit for selected rows (previous: "rows 2").
    2. Added WAIT mode to be checked after fixed https://github.com/FirebirdSQL/firebird/issues/7700
       ( https://github.com/FirebirdSQL/firebird/commit/5b14baa37b6ee214cd8ccc21f2e99dce119fe60e )

    3. NOTE: before fix gh-7700, following statement hanged:
         set transaction read committed record_version WAIT;
         select id from test order by id with lock skip locked

    Checked on 5.0.0.1209 
"""

import pytest
from firebird.qa import *
from firebird.driver import tpb, Isolation, TraLockResolution, TraAccessMode, DatabaseError
import time

db = db_factory()
substitutions = [ ('transaction number is \\d+', 'transaction number is'),
                  ("-At procedure 'SP_GET_UNLOCKED_ROWS_LOCAL' line.*", "-At procedure 'SP_GET_UNLOCKED_ROWS_LOCAL'"),
                  ("-At procedure 'SP_GET_UNLOCKED_ROWS_REMOTE' line.*", "-At procedure 'SP_GET_UNLOCKED_ROWS_REMOTE'"),
                  ('Data source : Firebird::localhost:.*', 'Data source : Firebird::localhost:')
                ]
act = python_act('db', substitutions = substitutions)

CHECK_SQL = 'select id from test order by id with lock skip locked'

expected_stdout = f"""
    QUERY_TYPE = DSQL, TIL = SERIALIZABLE, ACCESS = READ, WAIT = NO_WAIT:
    lock conflict on no wait transaction
    -Acquire lock for relation (TEST) failed
    -901
    335544345
    335544382
    QUERY_TYPE = DSQL, TIL = SNAPSHOT, ACCESS = READ, WAIT = NO_WAIT:
    attempted update during read-only transaction
    -817
    335544361
    QUERY_TYPE = DSQL, TIL = SNAPSHOT, ACCESS = READ, WAIT = WAIT:
    attempted update during read-only transaction
    -817
    335544361
    QUERY_TYPE = DSQL, TIL = READ_COMMITTED_READ_CONSISTENCY, ACCESS = READ, WAIT = NO_WAIT:
    attempted update during read-only transaction
    -817
    335544361
    QUERY_TYPE = DSQL, TIL = READ_COMMITTED_READ_CONSISTENCY, ACCESS = READ, WAIT = WAIT:
    attempted update during read-only transaction
    -817
    335544361
    QUERY_TYPE = DSQL, TIL = READ_COMMITTED_RECORD_VERSION, ACCESS = READ, WAIT = NO_WAIT:
    attempted update during read-only transaction
    -817
    335544361
    QUERY_TYPE = DSQL, TIL = READ_COMMITTED_RECORD_VERSION, ACCESS = READ, WAIT = WAIT:
    attempted update during read-only transaction
    -817
    335544361
    QUERY_TYPE = DSQL, TIL = READ_COMMITTED_NO_RECORD_VERSION, ACCESS = READ, WAIT = NO_WAIT:
    deadlock
    -read conflicts with concurrent update
    -concurrent transaction number is
    -913
    335544336
    335545096
    335544878
    QUERY_TYPE = DSQL, TIL = SERIALIZABLE, ACCESS = WRITE, WAIT = NO_WAIT:
    lock conflict on no wait transaction
    -Acquire lock for relation (TEST) failed
    -901
    335544345
    335544382
    QUERY_TYPE = DSQL, TIL = SNAPSHOT, ACCESS = WRITE, WAIT = NO_WAIT:
    ID=2
    ID=3
    ID=4
    ID=6
    ID=7
    ID=8
    ID=10
    QUERY_TYPE = DSQL, TIL = SNAPSHOT, ACCESS = WRITE, WAIT = WAIT:
    ID=2
    ID=3
    ID=4
    ID=6
    ID=7
    ID=8
    ID=10
    QUERY_TYPE = DSQL, TIL = READ_COMMITTED_READ_CONSISTENCY, ACCESS = WRITE, WAIT = NO_WAIT:
    ID=2
    ID=3
    ID=4
    ID=6
    ID=7
    ID=8
    ID=10
    QUERY_TYPE = DSQL, TIL = READ_COMMITTED_READ_CONSISTENCY, ACCESS = WRITE, WAIT = WAIT:
    ID=2
    ID=3
    ID=4
    ID=6
    ID=7
    ID=8
    ID=10
    QUERY_TYPE = DSQL, TIL = READ_COMMITTED_RECORD_VERSION, ACCESS = WRITE, WAIT = NO_WAIT:
    ID=2
    ID=3
    ID=4
    ID=6
    ID=7
    ID=8
    ID=10
    QUERY_TYPE = DSQL, TIL = READ_COMMITTED_RECORD_VERSION, ACCESS = WRITE, WAIT = WAIT:
    ID=2
    ID=3
    ID=4
    ID=6
    ID=7
    ID=8
    ID=10
    QUERY_TYPE = DSQL, TIL = READ_COMMITTED_NO_RECORD_VERSION, ACCESS = WRITE, WAIT = NO_WAIT:
    deadlock
    -read conflicts with concurrent update
    -concurrent transaction number is
    -913
    335544336
    335545096
    335544878
    QUERY_TYPE = PSQL_LOCAL, TIL = SERIALIZABLE, ACCESS = READ, WAIT = NO_WAIT:
    lock conflict on no wait transaction
    -Acquire lock for relation (TEST) failed
    -At procedure 'SP_GET_UNLOCKED_ROWS_LOCAL'
    -901
    335544345
    335544382
    335544842
    QUERY_TYPE = PSQL_LOCAL, TIL = SNAPSHOT, ACCESS = READ, WAIT = NO_WAIT:
    attempted update during read-only transaction
    -At procedure 'SP_GET_UNLOCKED_ROWS_LOCAL'
    -817
    335544361
    335544842
    QUERY_TYPE = PSQL_LOCAL, TIL = SNAPSHOT, ACCESS = READ, WAIT = WAIT:
    attempted update during read-only transaction
    -At procedure 'SP_GET_UNLOCKED_ROWS_LOCAL'
    -817
    335544361
    335544842
    QUERY_TYPE = PSQL_LOCAL, TIL = READ_COMMITTED_READ_CONSISTENCY, ACCESS = READ, WAIT = NO_WAIT:
    attempted update during read-only transaction
    -At procedure 'SP_GET_UNLOCKED_ROWS_LOCAL'
    -817
    335544361
    335544842
    QUERY_TYPE = PSQL_LOCAL, TIL = READ_COMMITTED_READ_CONSISTENCY, ACCESS = READ, WAIT = WAIT:
    attempted update during read-only transaction
    -At procedure 'SP_GET_UNLOCKED_ROWS_LOCAL'
    -817
    335544361
    335544842
    QUERY_TYPE = PSQL_LOCAL, TIL = READ_COMMITTED_RECORD_VERSION, ACCESS = READ, WAIT = NO_WAIT:
    attempted update during read-only transaction
    -At procedure 'SP_GET_UNLOCKED_ROWS_LOCAL'
    -817
    335544361
    335544842
    QUERY_TYPE = PSQL_LOCAL, TIL = READ_COMMITTED_RECORD_VERSION, ACCESS = READ, WAIT = WAIT:
    attempted update during read-only transaction
    -At procedure 'SP_GET_UNLOCKED_ROWS_LOCAL'
    -817
    335544361
    335544842
    QUERY_TYPE = PSQL_LOCAL, TIL = READ_COMMITTED_NO_RECORD_VERSION, ACCESS = READ, WAIT = NO_WAIT:
    deadlock
    -read conflicts with concurrent update
    -concurrent transaction number is
    -At procedure 'SP_GET_UNLOCKED_ROWS_LOCAL'
    -913
    335544336
    335545096
    335544878
    335544842
    QUERY_TYPE = PSQL_LOCAL, TIL = SERIALIZABLE, ACCESS = WRITE, WAIT = NO_WAIT:
    lock conflict on no wait transaction
    -Acquire lock for relation (TEST) failed
    -At procedure 'SP_GET_UNLOCKED_ROWS_LOCAL'
    -901
    335544345
    335544382
    335544842
    QUERY_TYPE = PSQL_LOCAL, TIL = SNAPSHOT, ACCESS = WRITE, WAIT = NO_WAIT:
    ID=2
    ID=3
    ID=4
    ID=6
    ID=7
    ID=8
    ID=10
    QUERY_TYPE = PSQL_LOCAL, TIL = SNAPSHOT, ACCESS = WRITE, WAIT = WAIT:
    ID=2
    ID=3
    ID=4
    ID=6
    ID=7
    ID=8
    ID=10
    QUERY_TYPE = PSQL_LOCAL, TIL = READ_COMMITTED_READ_CONSISTENCY, ACCESS = WRITE, WAIT = NO_WAIT:
    ID=2
    ID=3
    ID=4
    ID=6
    ID=7
    ID=8
    ID=10
    QUERY_TYPE = PSQL_LOCAL, TIL = READ_COMMITTED_READ_CONSISTENCY, ACCESS = WRITE, WAIT = WAIT:
    ID=2
    ID=3
    ID=4
    ID=6
    ID=7
    ID=8
    ID=10
    QUERY_TYPE = PSQL_LOCAL, TIL = READ_COMMITTED_RECORD_VERSION, ACCESS = WRITE, WAIT = NO_WAIT:
    ID=2
    ID=3
    ID=4
    ID=6
    ID=7
    ID=8
    ID=10
    QUERY_TYPE = PSQL_LOCAL, TIL = READ_COMMITTED_RECORD_VERSION, ACCESS = WRITE, WAIT = WAIT:
    ID=2
    ID=3
    ID=4
    ID=6
    ID=7
    ID=8
    ID=10
    QUERY_TYPE = PSQL_LOCAL, TIL = READ_COMMITTED_NO_RECORD_VERSION, ACCESS = WRITE, WAIT = NO_WAIT:
    deadlock
    -read conflicts with concurrent update
    -concurrent transaction number is
    -At procedure 'SP_GET_UNLOCKED_ROWS_LOCAL'
    -913
    335544336
    335545096
    335544878
    335544842
    QUERY_TYPE = PSQL_REMOTE, TIL = SERIALIZABLE, ACCESS = READ, WAIT = NO_WAIT:
    Execute statement error at isc_dsql_fetch :
    335544345 : lock conflict on no wait transaction
    335544382 : Acquire lock for relation (TEST) failed
    Statement : select id from test order by id with lock skip locked
    Data source : Firebird::localhost:
    -At procedure 'SP_GET_UNLOCKED_ROWS_REMOTE'
    -901
    335544926
    335544842
    QUERY_TYPE = PSQL_REMOTE, TIL = SNAPSHOT, ACCESS = READ, WAIT = NO_WAIT:
    Execute statement error at isc_dsql_fetch :
    335544361 : attempted update during read-only transaction
    Statement : select id from test order by id with lock skip locked
    Data source : Firebird::localhost:
    -At procedure 'SP_GET_UNLOCKED_ROWS_REMOTE'
    -901
    335544926
    335544842
    QUERY_TYPE = PSQL_REMOTE, TIL = SNAPSHOT, ACCESS = READ, WAIT = WAIT:
    Execute statement error at isc_dsql_fetch :
    335544361 : attempted update during read-only transaction
    Statement : select id from test order by id with lock skip locked
    Data source : Firebird::localhost:
    -At procedure 'SP_GET_UNLOCKED_ROWS_REMOTE'
    -901
    335544926
    335544842
    QUERY_TYPE = PSQL_REMOTE, TIL = READ_COMMITTED_READ_CONSISTENCY, ACCESS = READ, WAIT = NO_WAIT:
    Execute statement error at isc_dsql_fetch :
    335544361 : attempted update during read-only transaction
    Statement : select id from test order by id with lock skip locked
    Data source : Firebird::localhost:
    -At procedure 'SP_GET_UNLOCKED_ROWS_REMOTE'
    -901
    335544926
    335544842
    QUERY_TYPE = PSQL_REMOTE, TIL = READ_COMMITTED_READ_CONSISTENCY, ACCESS = READ, WAIT = WAIT:
    Execute statement error at isc_dsql_fetch :
    335544361 : attempted update during read-only transaction
    Statement : select id from test order by id with lock skip locked
    Data source : Firebird::localhost:
    -At procedure 'SP_GET_UNLOCKED_ROWS_REMOTE'
    -901
    335544926
    335544842
    QUERY_TYPE = PSQL_REMOTE, TIL = READ_COMMITTED_RECORD_VERSION, ACCESS = READ, WAIT = NO_WAIT:
    Execute statement error at isc_dsql_fetch :
    335544361 : attempted update during read-only transaction
    Statement : select id from test order by id with lock skip locked
    Data source : Firebird::localhost:
    -At procedure 'SP_GET_UNLOCKED_ROWS_REMOTE'
    -901
    335544926
    335544842
    QUERY_TYPE = PSQL_REMOTE, TIL = READ_COMMITTED_RECORD_VERSION, ACCESS = READ, WAIT = WAIT:
    Execute statement error at isc_dsql_fetch :
    335544361 : attempted update during read-only transaction
    Statement : select id from test order by id with lock skip locked
    Data source : Firebird::localhost:
    -At procedure 'SP_GET_UNLOCKED_ROWS_REMOTE'
    -901
    335544926
    335544842
    QUERY_TYPE = PSQL_REMOTE, TIL = READ_COMMITTED_NO_RECORD_VERSION, ACCESS = READ, WAIT = NO_WAIT:
    Execute statement error at isc_dsql_fetch :
    335544336 : deadlock
    335545096 : read conflicts with concurrent update
    335544878 : concurrent transaction number is
    Statement : select id from test order by id with lock skip locked
    Data source : Firebird::localhost:
    -At procedure 'SP_GET_UNLOCKED_ROWS_REMOTE'
    -901
    335544926
    335544842
    QUERY_TYPE = PSQL_REMOTE, TIL = SERIALIZABLE, ACCESS = WRITE, WAIT = NO_WAIT:
    Execute statement error at isc_dsql_fetch :
    335544345 : lock conflict on no wait transaction
    335544382 : Acquire lock for relation (TEST) failed
    Statement : select id from test order by id with lock skip locked
    Data source : Firebird::localhost:
    -At procedure 'SP_GET_UNLOCKED_ROWS_REMOTE'
    -901
    335544926
    335544842
    QUERY_TYPE = PSQL_REMOTE, TIL = SNAPSHOT, ACCESS = WRITE, WAIT = NO_WAIT:
    ID=2
    ID=3
    ID=4
    ID=6
    ID=7
    ID=8
    ID=10
    QUERY_TYPE = PSQL_REMOTE, TIL = SNAPSHOT, ACCESS = WRITE, WAIT = WAIT:
    ID=2
    ID=3
    ID=4
    ID=6
    ID=7
    ID=8
    ID=10
    QUERY_TYPE = PSQL_REMOTE, TIL = READ_COMMITTED_READ_CONSISTENCY, ACCESS = WRITE, WAIT = NO_WAIT:
    ID=2
    ID=3
    ID=4
    ID=6
    ID=7
    ID=8
    ID=10
    QUERY_TYPE = PSQL_REMOTE, TIL = READ_COMMITTED_READ_CONSISTENCY, ACCESS = WRITE, WAIT = WAIT:
    ID=2
    ID=3
    ID=4
    ID=6
    ID=7
    ID=8
    ID=10
    QUERY_TYPE = PSQL_REMOTE, TIL = READ_COMMITTED_RECORD_VERSION, ACCESS = WRITE, WAIT = NO_WAIT:
    ID=2
    ID=3
    ID=4
    ID=6
    ID=7
    ID=8
    ID=10
    QUERY_TYPE = PSQL_REMOTE, TIL = READ_COMMITTED_RECORD_VERSION, ACCESS = WRITE, WAIT = WAIT:
    ID=2
    ID=3
    ID=4
    ID=6
    ID=7
    ID=8
    ID=10
    QUERY_TYPE = PSQL_REMOTE, TIL = READ_COMMITTED_NO_RECORD_VERSION, ACCESS = WRITE, WAIT = NO_WAIT:
    Execute statement error at isc_dsql_fetch :
    335544336 : deadlock
    335545096 : read conflicts with concurrent update
    335544878 : concurrent transaction number is
    Statement : select id from test order by id with lock skip locked
    Data source : Firebird::localhost:
    -At procedure 'SP_GET_UNLOCKED_ROWS_REMOTE'
    -901
    335544926
    335544842
"""
@pytest.mark.version('>=5.0')
def test_1(act: Action, capsys):

    init_sql = f"""
        set term ^;
        recreate table test(id int primary key, f01 int)
        -- recreate global temporary table test(id int primary key, f01 int) on commit preserve rows
        ^
        create or alter procedure sp_get_unlocked_rows_local returns(id int) as
        begin
            for
                {CHECK_SQL}
                into id
            do
                suspend;
        end
        ^
        create or alter procedure sp_get_unlocked_rows_remote returns(id int) as
        begin
            for
                execute statement '{CHECK_SQL}'
                on external 'localhost:' || rdb$get_context('SYSTEM', 'DB_NAME')
                as user '{act.db.user}' password '{act.db.password}'
                into id
            do
                suspend;
        end
        ^
        set term ^;
        commit;

        insert into test(id, f01) select row_number()over(), 0 from rdb$types rows 10;
        commit;
    """ 
    act.isql(switches=['-q'], input = init_sql, combine_output = True)
    assert act.clean_stdout == ''
    act.reset()

    tpb_isol_set = (Isolation.SERIALIZABLE, Isolation.SNAPSHOT, Isolation.READ_COMMITTED_READ_CONSISTENCY, Isolation.READ_COMMITTED_RECORD_VERSION, Isolation.READ_COMMITTED_NO_RECORD_VERSION)
    tpb_wait_set = (TraLockResolution.NO_WAIT,TraLockResolution.WAIT)
    tpb_mode_set = (TraAccessMode.READ, TraAccessMode.WRITE)
    query_types_set = ('DSQL', 'PSQL_LOCAL', 'PSQL_REMOTE')
    #query_types_set = ('DSQL',)

    with act.db.connect() as con_rows_locker, act.db.connect() as con_free_seeker:
        con_rows_locker.execute_immediate('update test set f01 = 1 where id in (1,5,9)')
        for query_type in query_types_set:
            for x_mode in tpb_mode_set:
                for x_isol in tpb_isol_set:
                    for x_wait in tpb_wait_set:
                        if x_isol in (Isolation.SERIALIZABLE, Isolation.READ_COMMITTED_NO_RECORD_VERSION) and x_wait == TraLockResolution.WAIT:
                            
                            #######################################
                            ###    D O    N O T    C H E C K    ###
                            #######################################
                            #
                            # 1. Isolation.SERIALIZABLE requires that the whole table must not be changed by anyone else.
                            # 2. Isolation.READ_COMMITTED_NO_RECORD_VERSION can not be used due to implementation details, see:
                            #    Adriano, 26-feb-2023, https://github.com/FirebirdSQL/firebird/pull/7350#issuecomment-1445408462
                            #    "WITH LOCK [SKIP LOCKED] needs a record read before, but this locked records cannot be read with NO RECORD VERSION.
                            #    Considering that this transaction mode is replaced by default I would only document it as in fact I don't think
                            #    there are anything we could do."

                            continue

                        custom_tpb = tpb(isolation = x_isol, access_mode = x_mode, lock_timeout = -1 if x_wait == TraLockResolution.WAIT else 0)
                        #custom_tpb = TPB(isolation = x_isol, access_mode = x_mode, lock_timeout = 0).get_buffer()
                        tx_free_seeker = con_free_seeker.transaction_manager(custom_tpb)
                        cur_free_seeker = tx_free_seeker.cursor()
                        tx_free_seeker.begin()
                        try:
                            print('\n')
                            print(f'QUERY_TYPE = {query_type}, TIL = {x_isol.name}, ACCESS = {x_mode.name}, WAIT = {x_wait.name}:')
                            if query_type == 'DSQL':
                                cur_free_seeker.execute(f'{CHECK_SQL}')
                            elif query_type == 'PSQL_LOCAL':
                                cur_free_seeker.execute('select id from sp_get_unlocked_rows_local')
                            elif query_type == 'PSQL_REMOTE':
                                cur_free_seeker.execute('select id from sp_get_unlocked_rows_remote')
                            for r in cur_free_seeker:
                                 print('ID='+str(r[0]))
                        except DatabaseError as e:
                            print(e.__str__())
                            print(e.sqlcode)
                            for g in e.gds_codes:
                                print(g)
                        finally:
                            tx_free_seeker.rollback()

    act.expected_stdout = expected_stdout
    act.stdout = capsys.readouterr().out
    assert act.clean_stdout == act.clean_expected_stdout
