#coding:utf-8
#
# id:           bugs.core_2018
# title:        Only one client can access a readonly database
# decription:   
#                   Restored database contains GTT. According to CORE-3399 we can write in it even in read-only database.
#                   This GTT serves as temp buffer for output row (we can not use windowed function in 2.5)
#                   Checked on:
#                       4.0.0.1635 SS: 2.094s.
#                       4.0.0.1633 CS: 3.591s.
#                       3.0.5.33180 SS: 2.061s.
#                       3.0.5.33178 CS: 2.383s.
#                       2.5.9.27119 SS: 0.872s.
#                       2.5.9.27146 SC: 0.435s.
#                
# tracker_id:   CORE-2018
# min_versions: ['2.5.1']
# versions:     2.5.1
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 2.5.1
# resources: None

substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(from_backup='core2018-read_only.fbk', init=init_script_1)

test_script_1 = """
    set list on;
    select MON$READ_ONLY from mon$database;
    commit;

    -- ::: NB :::
    -- For CLASSIC mode each ES/EDS will increase value of current_connection by 2, for SS/SC - by 1.
    -- In order to avoid dependency of architecture it was decided to accumulate _SEQUENTIAL_ numbers
    -- of  connection IDs (i.e. without holes) in GTT and ouput all of them after loop finish.
    -- This sequential order can be easy achieved in 3.0 using dense_rank() but in 2.5 we need to
    -- write SQL with additional subquery, see below.
    set term ^;
    execute block returns(sequential_attach_no int, attaches_i_can_see int) as
        declare v_dbname type of column mon$database.mon$database_name;
        declare v_stt varchar(192) = 'select current_connection, count(distinct a.mon$attachment_id) from mon$attachments a where a.mon$user=current_user and a.mon$remote_protocol is not null';
        declare v_usr varchar(31) = 'SYSDBA';
        declare v_pwd varchar(20) = 'masterkey';
        declare n int = 10;
        declare v_attach_id int;
    begin
        v_dbname = 'localhost:' || rdb$get_context('SYSTEM', 'DB_NAME');
    
        while (n > 0 ) do
        begin
            execute statement v_stt
            on external v_dbname
            as user v_usr password v_pwd role upper('BOSS#'||n)
            into v_attach_id, attaches_i_can_see;

            -- This CAN be done since CORE-3399 was fixed (2.5.1):
            insert into gtt_attaches(attach_id, sequential_id, attaches_i_can_see)
            select
                 :v_attach_id
                ,( select count(*) from gtt_attaches x where x.attach_id < :v_attach_id ) + 1 -- can`t use windowed funcs in 2.5
                ,:attaches_i_can_see
            from rdb$database;
            n = n-1;
        end
        for
            select sequential_id, attaches_i_can_see
            from gtt_attaches
           into sequential_attach_no, attaches_i_can_see 
        do suspend;
    end
    ^
    set term ;^
    --select * from gtt_attaches;
    commit;

    --                                    ||||||||||||||||||||||||||||
    -- ###################################|||  FB 4.0+, SS and SC  |||##############################
    --                                    ||||||||||||||||||||||||||||
    -- If we check SS or SC and ExtConnPoolLifeTime > 0 (config parameter FB 4.0+) then current
    -- DB (bugs.core_NNNN.fdb) will be 'captured' by firebird.exe process and fbt_run utility
    -- will not able to drop this database at the final point of test.
    -- Moreover, DB file will be hold until all activity in firebird.exe completed and AFTER this
    -- we have to wait for <ExtConnPoolLifeTime> seconds after it (discussion and small test see
    -- in the letter to hvlad and dimitr 13.10.2019 11:10).
    -- This means that one need to kill all connections to prevent from exception on cleanup phase:
    -- SQLCODE: -901 / lock time-out on wait transaction / object <this_test_DB> is in use
    -- #############################################################################################
    delete from mon$attachments where mon$attachment_id != current_connection;
    commit;    

  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    MON$READ_ONLY                   1
    
    SEQUENTIAL_ATTACH_NO            1
    ATTACHES_I_CAN_SEE              2
    
    SEQUENTIAL_ATTACH_NO            2
    ATTACHES_I_CAN_SEE              3
    
    SEQUENTIAL_ATTACH_NO            3
    ATTACHES_I_CAN_SEE              4
    
    SEQUENTIAL_ATTACH_NO            4
    ATTACHES_I_CAN_SEE              5
    
    SEQUENTIAL_ATTACH_NO            5
    ATTACHES_I_CAN_SEE              6
    
    SEQUENTIAL_ATTACH_NO            6
    ATTACHES_I_CAN_SEE              7
    
    SEQUENTIAL_ATTACH_NO            7
    ATTACHES_I_CAN_SEE              8
    
    SEQUENTIAL_ATTACH_NO            8
    ATTACHES_I_CAN_SEE              9
    
    SEQUENTIAL_ATTACH_NO            9
    ATTACHES_I_CAN_SEE              10
    
    SEQUENTIAL_ATTACH_NO            10
    ATTACHES_I_CAN_SEE              11
  """

@pytest.mark.version('>=2.5.1')
def test_core_2018_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_expected_stdout == act_1.clean_stdout

