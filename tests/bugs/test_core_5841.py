#coding:utf-8
#
# id:           bugs.core_5841
# title:        No permission for SELECT access to BLOB field if a TABLE is accessed using VIEW
# decription:   
#                   Confirmed bug on 3.0.4.32985
#                   Checked on both Srp and Legacy_Auth, builds:
#                       3.0.4.33053: OK, 4.125s.
#                       4.0.0.1224: OK, 4.203s.
#                
# tracker_id:   CORE-5841
# min_versions: ['3.0']
# versions:     3.0.4
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 3.0.4
# resources: None

substitutions_1 = [('BLOB_FLD.*', 'BLOB_FLD')]

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """
    set bail on;
    set list on;
    set blob all;

    create or alter user tmp$c5841 password '123';
    commit;

    create table test (
            name_fld varchar(64),
            blob_fld blob,
            bool_fld boolean,
            primary key (name_fld)
           );

    create view v_test as
    select 
        name_fld, 
        blob_fld,
        bool_fld 
        from test 
    ;

    grant select on test to view v_test;
    grant select on v_test to public;
    commit;

    insert into test (
        name_fld, 
        blob_fld, 
        bool_fld)
    values (
        upper('tmp$c5841'),
        lpad('', 70, 'qwerty'), 
        true
    );

    commit;

    connect '$(DSN)' user tmp$c5841 password '123';

    set bail off;
    set count on;
    select
         name_fld
         ,blob_fld -- content of this blob field was inaccessible before bug fix
         ,bool_fld
    from v_test
    ;
    rollback;

    connect '$(DSN)' user sysdba password 'masterkey';
    drop user tmp$c5841 ;
    commit;
  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    NAME_FLD                        TMP$C5841
    BLOB_FLD                        80:0
    qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwer
    BOOL_FLD                        <true>
    Records affected: 1
  """

@pytest.mark.version('>=3.0.4')
def test_core_5841_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_expected_stdout == act_1.clean_stdout

