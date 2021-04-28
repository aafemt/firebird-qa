#coding:utf-8
#
# id:           bugs.core_4928
# title:        It is not possible to save the connection information in the ON CONNECT trigger, if the connection is created by the gbak
# decription:   
# tracker_id:   CORE-4928
# min_versions: ['3.0']
# versions:     3.0
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 3.0
# resources: None

substitutions_1 = []

init_script_1 = """
    recreate table att_log (
        att_id int,
        att_name varchar(255),
        att_user varchar(255),
        att_addr varchar(255),
        att_prot varchar(255),
        att_auth varchar(255),
        att_dts timestamp default 'now'
    );
    
    commit;
    
    set term ^;
    create or alter trigger trg_connect active on connect as
    begin
      in autonomous transaction do
      insert into att_log(att_id, att_name, att_user, att_addr, att_prot, att_auth)
      select
           mon$attachment_id
          ,mon$attachment_name
          ,mon$user
          ,mon$remote_address
          ,mon$remote_protocol
          ,mon$auth_method
      from mon$attachments
      where mon$remote_protocol starting with upper('TCP') and mon$user = upper('SYSDBA')
      ;
    end
    ^
    set term ;^
    commit; 
  """

db_1 = db_factory(sql_dialect=3, init=init_script_1)

# test_script_1
#---
# import os
#  db_conn.close()
#  fbk = os.path.join(context['temp_directory'],'tmp.core_4928.fbk')
#  runProgram('gbak',['-b','-user',user_name,'-password',user_password,dsn,fbk])
#  runProgram('gbak',['-rep','-user',user_name,'-password',user_password,fbk,dsn])
#  
#  sql='''
#  set list on;
#  select 
#      iif( att_id > 0, 1, 0) is_att_id_ok
#     ,iif( att_name containing 'core_4928.fdb', 1, 0) is_att_name_ok
#     ,iif( att_user = upper('SYSDBA'), 1, 0) is_att_user_ok
#     ,iif( att_addr is not null, 1, 0) is_att_addr_ok
#     ,iif( upper(att_prot) starting with upper('TCP'), 1, 0) is_att_prot_ok
#     ,iif( att_auth is not null, 1, 0) is_att_auth_ok
#     ,iif( att_dts is not null, 1, 0) is_att_dts_ok
#  from att_log 
#  where att_id <> current_connection;
#  '''
#  runProgram('isql',[dsn,'-user',user_name,'-pas',user_password],sql)
#  
#  if os.path.isfile(fbk):
#      os.remove(fbk)
#    
#---
#act_1 = python_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    IS_ATT_ID_OK                    1
    IS_ATT_NAME_OK                  1
    IS_ATT_USER_OK                  1
    IS_ATT_ADDR_OK                  1
    IS_ATT_PROT_OK                  1
    IS_ATT_AUTH_OK                  1
    IS_ATT_DTS_OK                   1
  """

@pytest.mark.version('>=3.0')
@pytest.mark.xfail
def test_1(db_1):
    pytest.fail("Test not IMPLEMENTED")


