#coding:utf-8
#
# id:           bugs.core_4923
# title:        Add ability to track domains rename in DDL triggers
# decription:   
# tracker_id:   CORE-4923
# min_versions: ['3.0']
# versions:     3.0
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 3.0
# resources: None

substitutions_1 = [('SQL_TEXT.*', '')]

init_script_1 = """"""

db_1 = db_factory(page_size=4096, sql_dialect=3, init=init_script_1)

test_script_1 = """
    recreate table ddl_log (
        id integer generated by default as identity constraint pk_ddl_log primary key using index pk_ddl_log
        ,who_logs varchar(50)
        ,evn_type varchar(50)
        ,obj_type varchar(50)
        ,obj_name varchar(50)
        ,old_name varchar(50)
        ,new_name varchar(50)
        ,sql_text blob sub_type text
    );
    commit;
    

    set term ^;

    -- active before create domain or alter domain or drop domain
    create trigger ddl_log_befo active before any ddl statement
    as
    begin
      insert into ddl_log(
         who_logs
        ,evn_type
        ,obj_type
        ,obj_name
        ,old_name
        ,new_name
        ,sql_text
      ) values (
         'DDL trigger BEFORE ddl statement'
        ,rdb$get_context('DDL_TRIGGER', 'EVENT_TYPE')
        ,rdb$get_context('DDL_TRIGGER', 'OBJECT_TYPE')
        ,rdb$get_context('DDL_TRIGGER', 'OBJECT_NAME')
        ,rdb$get_context('DDL_TRIGGER', 'OLD_OBJECT_NAME')
        ,rdb$get_context('DDL_TRIGGER', 'NEW_OBJECT_NAME')
        ,rdb$get_context('DDL_TRIGGER', 'SQL_TEXT')
      );
    end
    ^

    -- active before create domain or alter domain or drop domain
    create trigger ddl_log_afte active after any ddl statement
    as
    begin
      in autonomous transaction do
      insert into ddl_log(
         who_logs
        ,evn_type
        ,obj_type
        ,obj_name
        ,old_name
        ,new_name
        ,sql_text
      ) values (
         'DDL trigger AFTER ddl statement'
         ,rdb$get_context('DDL_TRIGGER', 'EVENT_TYPE')
        ,rdb$get_context('DDL_TRIGGER', 'OBJECT_TYPE')
        ,rdb$get_context('DDL_TRIGGER', 'OBJECT_NAME')
        ,rdb$get_context('DDL_TRIGGER', 'OLD_OBJECT_NAME')
        ,rdb$get_context('DDL_TRIGGER', 'NEW_OBJECT_NAME')
        ,rdb$get_context('DDL_TRIGGER', 'SQL_TEXT')
      );
    end
    ^

    set term ;^
    commit;
   

    create domain dm_foo smallint not null; -- here TWO transactions will start: DML and DDL. Only Tx for DDL will be auto-committed.

    -- For each of following DDL statements (which are executed with AUTOCOMMIT mode) two triggers fire:
    -- "ddl_log_befo" and "ddl_log_afte". Each trigger DOES write info about DDL changing to the log table 
    -- ("ddl_log") but it does this work in the same Tx as DDL. So, new content of DDL_LOG table can not
    -- be seen by starting DML transaction and we should do one more COMMIT before querying it (see below).
    alter domain dm_foo type int; 
    alter domain dm_foo to dm_bar; 
    alter domain dm_bar type bigint;
    alter domain dm_bar drop not null;
    drop domain dm_bar;

    -- NB: 1st DML transaction was started in TIL = SNAPSHOT when we did "create domain dm_foo smallint not null;", 
    -- so it does not yet see data in ddl_log and we have to COMMIT this DML transaction:
    commit; 


    set list on;
    set count on;
    select
         id
        ,who_logs
        ,evn_type
        ,obj_type
        ,obj_name
        ,old_name
        ,new_name
        ,sql_text
    from ddl_log
    where obj_type<>'TRIGGER'
    order by id;
  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    ID                              2
    WHO_LOGS                        DDL trigger BEFORE ddl statement
    EVN_TYPE                        CREATE
    OBJ_TYPE                        DOMAIN
    OBJ_NAME                        DM_FOO
    OLD_NAME                        <null>
    NEW_NAME                        <null>
    SQL_TEXT                        80:1
    create domain dm_foo smallint not null
    
    ID                              3
    WHO_LOGS                        DDL trigger AFTER ddl statement
    EVN_TYPE                        CREATE
    OBJ_TYPE                        DOMAIN
    OBJ_NAME                        DM_FOO
    OLD_NAME                        <null>
    NEW_NAME                        <null>
    SQL_TEXT                        80:2
    create domain dm_foo smallint not null
    
    ID                              4
    WHO_LOGS                        DDL trigger BEFORE ddl statement
    EVN_TYPE                        ALTER
    OBJ_TYPE                        DOMAIN
    OBJ_NAME                        DM_FOO
    OLD_NAME                        <null>
    NEW_NAME                        <null>
    SQL_TEXT                        80:3
    alter domain dm_foo type int
    
    ID                              5
    WHO_LOGS                        DDL trigger AFTER ddl statement
    EVN_TYPE                        ALTER
    OBJ_TYPE                        DOMAIN
    OBJ_NAME                        DM_FOO
    OLD_NAME                        <null>
    NEW_NAME                        <null>
    SQL_TEXT                        80:4
    alter domain dm_foo type int
    
    ID                              6
    WHO_LOGS                        DDL trigger BEFORE ddl statement
    EVN_TYPE                        ALTER
    OBJ_TYPE                        DOMAIN
    OBJ_NAME                        DM_FOO
    OLD_NAME                        DM_FOO
    NEW_NAME                        DM_BAR
    SQL_TEXT                        80:5
    alter domain dm_foo to dm_bar
    
    ID                              7
    WHO_LOGS                        DDL trigger AFTER ddl statement
    EVN_TYPE                        ALTER
    OBJ_TYPE                        DOMAIN
    OBJ_NAME                        DM_BAR
    OLD_NAME                        DM_FOO
    NEW_NAME                        DM_BAR
    SQL_TEXT                        80:6
    alter domain dm_foo to dm_bar
    
    ID                              8
    WHO_LOGS                        DDL trigger BEFORE ddl statement
    EVN_TYPE                        ALTER
    OBJ_TYPE                        DOMAIN
    OBJ_NAME                        DM_BAR
    OLD_NAME                        <null>
    NEW_NAME                        <null>
    SQL_TEXT                        80:7
    alter domain dm_bar type bigint
    
    ID                              9
    WHO_LOGS                        DDL trigger AFTER ddl statement
    EVN_TYPE                        ALTER
    OBJ_TYPE                        DOMAIN
    OBJ_NAME                        DM_BAR
    OLD_NAME                        <null>
    NEW_NAME                        <null>
    SQL_TEXT                        80:8
    alter domain dm_bar type bigint
    
    ID                              10
    WHO_LOGS                        DDL trigger BEFORE ddl statement
    EVN_TYPE                        ALTER
    OBJ_TYPE                        DOMAIN
    OBJ_NAME                        DM_BAR
    OLD_NAME                        <null>
    NEW_NAME                        <null>
    SQL_TEXT                        80:9
    alter domain dm_bar drop not null
    
    ID                              11
    WHO_LOGS                        DDL trigger AFTER ddl statement
    EVN_TYPE                        ALTER
    OBJ_TYPE                        DOMAIN
    OBJ_NAME                        DM_BAR
    OLD_NAME                        <null>
    NEW_NAME                        <null>
    SQL_TEXT                        80:a
    alter domain dm_bar drop not null
    
    ID                              12
    WHO_LOGS                        DDL trigger BEFORE ddl statement
    EVN_TYPE                        DROP
    OBJ_TYPE                        DOMAIN
    OBJ_NAME                        DM_BAR
    OLD_NAME                        <null>
    NEW_NAME                        <null>
    SQL_TEXT                        80:b
    drop domain dm_bar
    
    ID                              13
    WHO_LOGS                        DDL trigger AFTER ddl statement
    EVN_TYPE                        DROP
    OBJ_TYPE                        DOMAIN
    OBJ_NAME                        DM_BAR
    OLD_NAME                        <null>
    NEW_NAME                        <null>
    SQL_TEXT                        80:c
    drop domain dm_bar
    
    
    Records affected: 12
  """

@pytest.mark.version('>=3.0')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_expected_stdout == act_1.clean_stdout

