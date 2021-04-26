#coding:utf-8
#
# id:           functional.syspriv.use_nbackup_utility
# title:        Check ability to use nbackup.
# decription:   
#                  Verify ability to issue ALTER DATABASE BEGIN/END BACKUP command by non-sysdba user.
#                  Checked on 4.0.0.262.
#                
# tracker_id:   
# min_versions: ['4.0.0']
# versions:     4.0
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 4.0
# resources: None

substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """
    set wng off;
    set bail on;
    set list on;
    set count on;

    create or alter view v_check as
    select 
         current_user as who_ami
        ,r.rdb$role_name
        ,rdb$role_in_use(r.rdb$role_name) as RDB_ROLE_IN_USE
        ,r.rdb$system_privileges
    from mon$database m cross join rdb$roles r;
    commit;
    grant select on v_check to public;

    commit;
    connect '$(DSN)' user sysdba password 'masterkey';
    create or alter user u01 password '123' revoke admin role;
    revoke all on all from u01;
    commit;

    set term ^;
    execute block as
    begin
      execute statement 'drop role role_for_use_nbackup_utility';
      when any do begin end
    end^
    set term ;^
    commit;

    -- Use nbackup to create database's copies
    create role role_for_use_nbackup_utility set system privileges to USE_NBACKUP_UTILITY;
    commit;

    -- Without following grant user U01 will NOT be able to set database-level lock that
    -- is used by "alter database begin backup" command (that's what "nbackup -L 0" does):
    -- Statement failed, SQLSTATE = 28000
    -- unsuccessful metadata update
    -- -ALTER DATABASE failed
    -- -no permission for ALTER access to DATABASE 
    grant default role_for_use_nbackup_utility to user u01;
    commit;

    connect '$(DSN)' user u01 password '123';
    select * from v_check;
    commit;

    set list on;

    select mon$backup_state from mon$database;
    alter database begin backup;
    commit;

    select mon$backup_state from mon$database;
    alter database end backup;
    commit;

    select mon$backup_state from mon$database;
    commit;

    connect '$(DSN)' user sysdba password 'masterkey';
    drop user u01;
    drop role role_for_use_nbackup_utility;
    commit;
  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    WHO_AMI                         U01
    RDB$ROLE_NAME                   RDB$ADMIN                                                                                                                                                                                                                                                   
    RDB_ROLE_IN_USE                 <false>
    RDB$SYSTEM_PRIVILEGES           FFFFFFFFFFFFFFFF

    WHO_AMI                         U01
    RDB$ROLE_NAME                   ROLE_FOR_USE_NBACKUP_UTILITY                                                                                                                                                                                                                                
    RDB_ROLE_IN_USE                 <true>
    RDB$SYSTEM_PRIVILEGES           1000000000000000


    Records affected: 2

    MON$BACKUP_STATE                0


    Records affected: 1

    MON$BACKUP_STATE                1


    Records affected: 1

    MON$BACKUP_STATE                0


    Records affected: 1
  """

@pytest.mark.version('>=4.0')
def test_use_nbackup_utility_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_expected_stdout == act_1.clean_stdout

