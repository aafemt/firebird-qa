#coding:utf-8
#
# id:           functional.basic.db.31
# title:        Empty DB - RDB$USER_PRIVILEGES
# decription:   
#                   Check for correct content of RDB$USER_PRIVILEGES in empty database.',
#                
# tracker_id:   
# min_versions: ['2.5.7']
# versions:     3.0, 4.0
# qmid:         

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 3.0
# resources: None

substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """
    -- 30.10.2015: field rdb$grantor now contain NULLs in all records for new empty database (since build ~32134).
    -- Confirmed by Alex that this is OK 30.10.2015 15:28.
    set list on;

    -- Query for check whether fields list of table was changed:
    select rf.rdb$field_name
    from rdb$relation_fields rf
    where rf.rdb$relation_name = upper('rdb$user_privileges')
    order by rf.rdb$field_name;

    set count on;

    select * from rdb$user_privileges t
    order by
        t.rdb$user
        ,coalesce(t.rdb$grantor,'[none]')
        ,t.rdb$relation_name
        ,t.rdb$privilege
        ,t.rdb$grant_option
        ,coalesce(t.rdb$field_name, '[none')
        ,t.rdb$user_type
        ,t.rdb$object_type
    ;

    set count off;
    select iif(
                count(*) =
                 count(distinct rdb$user || coalesce(rdb$grantor,'[none]') || rdb$privilege || rdb$relation_name || rdb$privilege || rdb$grant_option || coalesce(rdb$field_name, '[none') || rdb$user_type || rdb$object_type
                      )
                 ,1
                 ,0
              ) as "Are ordered columns unique ?" from rdb$user_privileges
    ;
  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """

    RDB$FIELD_NAME                  RDB$FIELD_NAME                                                                               

    RDB$FIELD_NAME                  RDB$GRANTOR                                                                                  

    RDB$FIELD_NAME                  RDB$GRANT_OPTION                                                                             

    RDB$FIELD_NAME                  RDB$OBJECT_TYPE                                                                              

    RDB$FIELD_NAME                  RDB$PRIVILEGE                                                                                

    RDB$FIELD_NAME                  RDB$RELATION_NAME                                                                            

    RDB$FIELD_NAME                  RDB$USER                                                                                     

    RDB$FIELD_NAME                  RDB$USER_TYPE                                                                                



    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               MON$ATTACHMENTS                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               MON$CALL_STACK                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               MON$CONTEXT_VARIABLES                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               MON$DATABASE                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               MON$IO_STATS                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               MON$MEMORY_USAGE                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               MON$RECORD_STATS                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               MON$STATEMENTS                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               MON$TABLE_STATS                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               MON$TRANSACTIONS                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$AUTH_MAPPING                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$BACKUP_HISTORY                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$CHARACTER_SETS                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$CHECK_CONSTRAINTS                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$COLLATIONS                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$DATABASE                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$DB_CREATORS                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$DEPENDENCIES                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$EXCEPTIONS                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$FIELDS                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$FIELD_DIMENSIONS                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$FILES                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$FILTERS                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$FORMATS                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$FUNCTIONS                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$FUNCTION_ARGUMENTS                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$GENERATORS                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$INDEX_SEGMENTS                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$INDICES                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$LOG_FILES                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$PACKAGES                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$PAGES                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$PROCEDURES                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$PROCEDURE_PARAMETERS                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$REF_CONSTRAINTS                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$RELATIONS                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$RELATION_CONSTRAINTS                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$RELATION_FIELDS                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$ROLES                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$SECURITY_CLASSES                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$TRANSACTIONS                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$TRIGGERS                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$TRIGGER_MESSAGES                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$TYPES                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$USER_PRIVILEGES                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$VIEW_RELATIONS                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               SEC$DB_CREATORS                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               SEC$GLOBAL_AUTH_MAPPING                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               SEC$USERS                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               SEC$USER_ATTRIBUTES                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 20

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ASCII                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ASCII                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               BIG_5                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               BIG_5                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               BS_BA                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               CP943C                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               CP943C                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               CP943C_UNICODE                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               CS_CZ                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               CYRL                                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               CYRL                                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DA_DA                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_CSY                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_DAN865                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_DEU437                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_DEU850                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_ESP437                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_ESP850                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_FIN437                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_FRA437                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_FRA850                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_FRC850                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_FRC863                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_ITA437                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_ITA850                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_NLD437                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_NLD850                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_NOR865                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_PLK                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_PTB850                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_PTG860                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_RUS                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_SLO                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_SVE437                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_SVE850                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_TRK                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_UK437                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_UK850                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_US437                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_US850                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DE_DE                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS437                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS437                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS737                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS737                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS775                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS775                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS850                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS850                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS852                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS852                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS857                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS857                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS858                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS858                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS860                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS860                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS861                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS861                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS862                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS862                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS863                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS863                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS864                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS864                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS865                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS865                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS866                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS866                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS869                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS869                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DU_NL                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               EN_UK                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               EN_US                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ES_ES                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ES_ES_CI_AI                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               EUCJ_0208                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               EUCJ_0208                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               FI_FI                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               FR_CA                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               FR_CA_CI_AI                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               FR_FR                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               FR_FR_CI_AI                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               GB18030                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               GB18030                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               GB18030_UNICODE                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               GBK                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               GBK                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               GBK_UNICODE                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               GB_2312                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               GB_2312                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ISO8859_1                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ISO8859_1                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ISO8859_13                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ISO8859_13                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ISO8859_2                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ISO8859_2                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ISO8859_3                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ISO8859_3                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ISO8859_4                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ISO8859_4                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ISO8859_5                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ISO8859_5                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ISO8859_6                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ISO8859_6                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ISO8859_7                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ISO8859_7                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ISO8859_8                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ISO8859_8                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ISO8859_9                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ISO8859_9                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ISO_HUN                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ISO_PLK                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               IS_IS                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               IT_IT                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               KOI8R                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               KOI8R                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               KOI8R_RU                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               KOI8U                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               KOI8U                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               KOI8U_UA                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               KSC_5601                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               KSC_5601                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               KSC_DICTIONARY                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               LT_LT                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$ATTACHMENTS                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$ATTACHMENTS                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$ATTACHMENTS                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$ATTACHMENTS                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$ATTACHMENTS                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$CALL_STACK                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$CALL_STACK                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$CALL_STACK                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$CALL_STACK                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$CALL_STACK                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$CONTEXT_VARIABLES                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$CONTEXT_VARIABLES                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$CONTEXT_VARIABLES                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$CONTEXT_VARIABLES                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$CONTEXT_VARIABLES                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$DATABASE                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$DATABASE                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$DATABASE                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$DATABASE                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$DATABASE                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$IO_STATS                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$IO_STATS                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$IO_STATS                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$IO_STATS                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$IO_STATS                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$MEMORY_USAGE                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$MEMORY_USAGE                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$MEMORY_USAGE                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$MEMORY_USAGE                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$MEMORY_USAGE                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$RECORD_STATS                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$RECORD_STATS                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$RECORD_STATS                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$RECORD_STATS                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$RECORD_STATS                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$SEC_DATABASE                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$STATEMENTS                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$STATEMENTS                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$STATEMENTS                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$STATEMENTS                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$STATEMENTS                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$TABLE_STATS                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$TABLE_STATS                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$TABLE_STATS                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$TABLE_STATS                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$TABLE_STATS                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$TRANSACTIONS                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$TRANSACTIONS                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$TRANSACTIONS                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$TRANSACTIONS                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$TRANSACTIONS                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               NEXT                                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               NEXT                                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               NONE                                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               NONE                                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               NO_NO                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               NXT_DEU                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               NXT_ESP                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               NXT_FRA                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               NXT_ITA                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               NXT_US                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               OCTETS                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               OCTETS                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PDOX_ASCII                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PDOX_CSY                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PDOX_CYRL                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PDOX_HUN                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PDOX_INTL                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PDOX_ISL                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PDOX_NORDAN4                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PDOX_PLK                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PDOX_SLO                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PDOX_SWEDFIN                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PT_BR                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PT_PT                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PXW_CSY                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PXW_CYRL                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PXW_GREEK                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PXW_HUN                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PXW_HUNDC                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PXW_INTL                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PXW_INTL850                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PXW_NORDAN4                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PXW_PLK                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PXW_SLOV                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PXW_SPAN                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PXW_SWEDFIN                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PXW_TURK                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$ACL                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$ADMIN                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 13

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$ARGUMENT_MECHANISM                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$ARGUMENT_NAME                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$ATTACHMENT_ID                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$AUTH_MAPPING                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$AUTH_MAPPING                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$AUTH_MAPPING                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$AUTH_MAPPING                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$AUTH_MAPPING                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$AUTH_METHOD                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$BACKUP_HISTORY                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$BACKUP_HISTORY                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 14

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$BACKUP_HISTORY                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$BACKUP_HISTORY                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$BACKUP_HISTORY                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$BACKUP_HISTORY                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$BACKUP_ID                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$BACKUP_LEVEL                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$BACKUP_STATE                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$BOOLEAN                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$BOUND                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CALL_ID                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CHARACTER_SETS                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CHARACTER_SETS                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CHARACTER_SETS                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CHARACTER_SETS                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CHARACTER_SETS                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CHARACTER_SET_ID                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CHARACTER_SET_NAME                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CHECK_CONSTRAINTS                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CHECK_CONSTRAINTS                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CHECK_CONSTRAINTS                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CHECK_CONSTRAINTS                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CHECK_CONSTRAINTS                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CLIENT_VERSION                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$COLLATIONS                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$COLLATIONS                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$COLLATIONS                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$COLLATIONS                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$COLLATIONS                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$COLLATION_ID                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$COLLATION_NAME                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CONSTRAINT_NAME                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CONSTRAINT_NAME                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 14

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CONSTRAINT_TYPE                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CONTEXT_NAME                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CONTEXT_VAR_NAME                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CONTEXT_VAR_VALUE                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$COUNTER                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DATABASE                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DATABASE                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DATABASE                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DATABASE                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DATABASE                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DBKEY_LENGTH                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DB_CREATORS                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DB_CREATORS                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DB_CREATORS                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DB_CREATORS                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DB_CREATORS                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DEBUG_INFO                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DEFERRABLE                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DEPENDENCIES                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DEPENDENCIES                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DEPENDENCIES                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DEPENDENCIES                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DEPENDENCIES                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DESCRIPTION                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DESCRIPTOR                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DIMENSION                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DIMENSIONS                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$EDIT_STRING                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$ENGINE_NAME                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$EXCEPTIONS                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$EXCEPTIONS                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 14

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$EXCEPTIONS                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$EXCEPTIONS                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$EXCEPTIONS                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$EXCEPTIONS                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$EXCEPTION_NAME                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$EXCEPTION_NUMBER                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$EXTERNAL_DESCRIPTION                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$EXTERNAL_NAME                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FIELDS                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FIELDS                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FIELDS                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FIELDS                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FIELDS                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FIELD_DIMENSIONS                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FIELD_DIMENSIONS                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FIELD_DIMENSIONS                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FIELD_DIMENSIONS                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FIELD_DIMENSIONS                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FIELD_ID                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FIELD_LENGTH                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FIELD_NAME                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FIELD_NAME                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 14

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FIELD_POSITION                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FIELD_PRECISION                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FIELD_SCALE                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FIELD_SUB_TYPE                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FIELD_TYPE                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FILES                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FILES                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FILES                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FILES                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FILES                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FILE_FLAGS                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FILE_LENGTH                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FILE_NAME                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FILE_NAME2                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FILE_PARTITIONS                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FILE_P_OFFSET                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FILE_SEQUENCE                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FILE_START                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FILTERS                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FILTERS                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FILTERS                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FILTERS                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FILTERS                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FORMAT                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FORMATS                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FORMATS                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FORMATS                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FORMATS                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FORMATS                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FUNCTIONS                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FUNCTIONS                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 14

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FUNCTIONS                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FUNCTIONS                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FUNCTIONS                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FUNCTIONS                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FUNCTION_ARGUMENTS                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FUNCTION_ARGUMENTS                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FUNCTION_ARGUMENTS                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FUNCTION_ARGUMENTS                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FUNCTION_ARGUMENTS                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FUNCTION_BLR                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FUNCTION_ID                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FUNCTION_NAME                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FUNCTION_TYPE                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$GENERATORS                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$GENERATORS                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$GENERATORS                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$GENERATORS                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$GENERATORS                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$GENERATOR_ID                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$GENERATOR_INCREMENT                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$GENERATOR_NAME                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$GENERATOR_NAME                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 14

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$GENERATOR_VALUE                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$GENERIC_NAME                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$GENERIC_TYPE                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$GUID                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$HOST_NAME                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$IDENTITY_TYPE                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$INDEX_ID                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$INDEX_NAME                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$INDEX_NAME                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 14

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$INDEX_SEGMENTS                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$INDEX_SEGMENTS                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$INDEX_SEGMENTS                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$INDEX_SEGMENTS                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$INDEX_SEGMENTS                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$INDICES                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$INDICES                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$INDICES                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$INDICES                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$INDICES                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$ISOLATION_MODE                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$LINGER                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$LOCK_TIMEOUT                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$LOG_FILES                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$LOG_FILES                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$LOG_FILES                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$LOG_FILES                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$LOG_FILES                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$MAP_DB                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$MAP_FROM                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$MAP_FROM_TYPE                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$MAP_NAME                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$MAP_TO                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$MAP_USING                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$MATCH_OPTION                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$MECHANISM                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$MESSAGE                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$MESSAGE_NUMBER                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$NULL_FLAG                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$NUMBER_OF_CHARACTERS                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$OBJECT_TYPE                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$ODS_NUMBER                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$OS_USER                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PACKAGES                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PACKAGES                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PACKAGES                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PACKAGES                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PACKAGES                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PACKAGE_NAME                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PAGES                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PAGES                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PAGES                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PAGES                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PAGES                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PAGE_BUFFERS                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PAGE_NUMBER                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PAGE_SEQUENCE                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PAGE_SIZE                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PAGE_TYPE                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PARAMETER_MECHANISM                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PARAMETER_NAME                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PARAMETER_NUMBER                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PARAMETER_TYPE                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PID                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PLAN                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PLUGIN                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PRIVILEGE                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PROCEDURES                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PROCEDURES                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 14

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PROCEDURES                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PROCEDURES                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PROCEDURES                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PROCEDURES                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PROCEDURE_BLR                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PROCEDURE_ID                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PROCEDURE_NAME                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PROCEDURE_PARAMETERS                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PROCEDURE_PARAMETERS                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PROCEDURE_PARAMETERS                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PROCEDURE_PARAMETERS                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PROCEDURE_PARAMETERS                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PROCEDURE_PARAMETERS                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PROCEDURE_TYPE                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$QUERY_HEADER                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$REF_CONSTRAINTS                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$REF_CONSTRAINTS                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$REF_CONSTRAINTS                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$REF_CONSTRAINTS                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$REF_CONSTRAINTS                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$RELATIONS                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$RELATIONS                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$RELATIONS                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$RELATIONS                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$RELATIONS                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$RELATION_CONSTRAINTS                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$RELATION_CONSTRAINTS                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$RELATION_CONSTRAINTS                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$RELATION_CONSTRAINTS                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$RELATION_CONSTRAINTS                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$RELATION_FIELDS                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$RELATION_FIELDS                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$RELATION_FIELDS                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$RELATION_FIELDS                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$RELATION_FIELDS                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$RELATION_ID                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$RELATION_NAME                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$RELATION_TYPE                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$REMOTE_ADDRESS                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$REMOTE_PROTOCOL                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$REMOTE_VERSION                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$ROLES                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$ROLES                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$ROLES                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$ROLES                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$ROLES                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$RULE                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$RUNTIME                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$SCN                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$SECURITY_CLASS                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$SECURITY_CLASS                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 14

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$SECURITY_CLASSES                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$SECURITY_CLASSES                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$SECURITY_CLASSES                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$SECURITY_CLASSES                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$SECURITY_CLASSES                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$SEGMENT_COUNT                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$SEGMENT_LENGTH                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$SHADOW_NUMBER                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$SHUTDOWN_MODE                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$SOURCE                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$SOURCE_INFO                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$SPECIFIC_ATTRIBUTES                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$SQL_DIALECT                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$STATE                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$STATEMENT_ID                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$STATISTICS                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$STAT_GROUP                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$STAT_ID                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$SWEEP_INTERVAL                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$SYSTEM_FLAG                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$SYSTEM_NULLFLAG                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TIMESTAMP                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRANSACTIONS                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRANSACTIONS                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRANSACTIONS                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRANSACTIONS                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRANSACTIONS                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRANSACTION_DESCRIPTION                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRANSACTION_ID                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRANSACTION_STATE                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRIGGERS                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRIGGERS                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRIGGERS                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRIGGERS                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRIGGERS                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRIGGER_BLR                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRIGGER_MESSAGES                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRIGGER_MESSAGES                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRIGGER_MESSAGES                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRIGGER_MESSAGES                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRIGGER_MESSAGES                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRIGGER_NAME                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRIGGER_NAME                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 14

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRIGGER_SEQUENCE                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRIGGER_TYPE                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TYPES                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TYPES                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TYPES                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TYPES                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TYPES                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TYPE_NAME                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$USER                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$USER_PRIVILEGES                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$USER_PRIVILEGES                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$USER_PRIVILEGES                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$USER_PRIVILEGES                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$USER_PRIVILEGES                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$VALIDATION_BLR                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$VALUE                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$VIEW_BLR                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$VIEW_CONTEXT                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$VIEW_RELATIONS                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$VIEW_RELATIONS                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$VIEW_RELATIONS                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$VIEW_RELATIONS                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$VIEW_RELATIONS                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$DB_CREATORS                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$DB_CREATORS                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$DB_CREATORS                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$DB_CREATORS                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$DB_CREATORS                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$GLOBAL_AUTH_MAPPING                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$GLOBAL_AUTH_MAPPING                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$GLOBAL_AUTH_MAPPING                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$GLOBAL_AUTH_MAPPING                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$GLOBAL_AUTH_MAPPING                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$KEY                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$NAME_PART                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$USERS                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$USERS                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$USERS                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$USERS                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$USERS                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$USER_ATTRIBUTES                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$USER_ATTRIBUTES                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$USER_ATTRIBUTES                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$USER_ATTRIBUTES                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$USER_ATTRIBUTES                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$USER_NAME                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$VALUE                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SJIS_0208                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SJIS_0208                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SQL$DEFAULT                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 14

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SV_SV                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               TIS620                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               TIS620                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               TIS620_UNICODE                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               UCS_BASIC                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               UNICODE                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               UNICODE_CI                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               UNICODE_CI_AI                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               UNICODE_FSS                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               UNICODE_FSS                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               UTF8                                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               UTF8                                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN1250                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN1250                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN1251                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN1251                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN1251_UA                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN1252                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN1252                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN1253                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN1253                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN1254                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN1254                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN1255                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN1255                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN1256                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN1256                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN1257                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN1257                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN1257_EE                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN1257_LT                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN1257_LV                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN1258                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN1258                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN_CZ                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN_CZ_CI_AI                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                       
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN_PTBR                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17


    Records affected: 664

    Are ordered columns unique ?    1

  """

@pytest.mark.version('>=3.0,<4.0')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_expected_stdout == act_1.clean_stdout

# version: 4.0
# resources: None

substitutions_2 = []

init_script_2 = """"""

db_2 = db_factory(sql_dialect=3, init=init_script_2)

test_script_2 = """
    set list on;

    -- Query for check whether fields list of table was changed:
    select rf.rdb$field_name
    from rdb$relation_fields rf
    where rf.rdb$relation_name = upper('rdb$user_privileges')
    order by rf.rdb$field_name;

    set count on;

    select * from rdb$user_privileges t
    order by
        t.rdb$user
        ,coalesce(t.rdb$grantor,'[none]')
        ,t.rdb$relation_name
        ,t.rdb$privilege
        ,t.rdb$grant_option
        ,coalesce(t.rdb$field_name, '[none')
        ,t.rdb$user_type
        ,t.rdb$object_type
    ;
    set count off;
    select iif(
                count(*) =
                 count(distinct rdb$user || coalesce(rdb$grantor,'[none]') || rdb$privilege || rdb$relation_name || rdb$privilege || rdb$grant_option || coalesce(rdb$field_name, '[none') || rdb$user_type || rdb$object_type
                      )
                 ,1
                 ,0
              ) as "Are ordered columns unique ?" from rdb$user_privileges
    ;
  """

act_2 = isql_act('db_2', test_script_2, substitutions=substitutions_2)

expected_stdout_2 = """

    RDB$FIELD_NAME                  RDB$FIELD_NAME                                                                                                                                                                                                                                              

    RDB$FIELD_NAME                  RDB$GRANTOR                                                                                                                                                                                                                                                 

    RDB$FIELD_NAME                  RDB$GRANT_OPTION                                                                                                                                                                                                                                            

    RDB$FIELD_NAME                  RDB$OBJECT_TYPE                                                                                                                                                                                                                                             

    RDB$FIELD_NAME                  RDB$PRIVILEGE                                                                                                                                                                                                                                               

    RDB$FIELD_NAME                  RDB$RELATION_NAME                                                                                                                                                                                                                                           

    RDB$FIELD_NAME                  RDB$USER                                                                                                                                                                                                                                                    

    RDB$FIELD_NAME                  RDB$USER_TYPE                                                                                                                                                                                                                                               



    RDB$USER                        22                                                                                                                                                                                                                                                          
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$DB_CREATORS                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   20
    RDB$OBJECT_TYPE                 0

    RDB$USER                        22                                                                                                                                                                                                                                                          
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$DB_CREATORS                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   20
    RDB$OBJECT_TYPE                 0

    RDB$USER                        22                                                                                                                                                                                                                                                          
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$DB_CREATORS                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   20
    RDB$OBJECT_TYPE                 0

    RDB$USER                        22                                                                                                                                                                                                                                                          
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$DB_CREATORS                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   20
    RDB$OBJECT_TYPE                 0

    RDB$USER                        22                                                                                                                                                                                                                                                          
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$DB_CREATORS                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   20
    RDB$OBJECT_TYPE                 0

    RDB$USER                        3                                                                                                                                                                                                                                                           
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$TYPES                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   20
    RDB$OBJECT_TYPE                 0

    RDB$USER                        3                                                                                                                                                                                                                                                           
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$TYPES                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   20
    RDB$OBJECT_TYPE                 0

    RDB$USER                        3                                                                                                                                                                                                                                                           
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$TYPES                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   20
    RDB$OBJECT_TYPE                 0

    RDB$USER                        3                                                                                                                                                                                                                                                           
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$TYPES                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   20
    RDB$OBJECT_TYPE                 0

    RDB$USER                        3                                                                                                                                                                                                                                                           
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$TYPES                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   20
    RDB$OBJECT_TYPE                 0

    RDB$USER                        4                                                                                                                                                                                                                                                           
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$BACKUP_HISTORY                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   20
    RDB$OBJECT_TYPE                 0

    RDB$USER                        4                                                                                                                                                                                                                                                           
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$BACKUP_HISTORY                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   20
    RDB$OBJECT_TYPE                 0

    RDB$USER                        4                                                                                                                                                                                                                                                           
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$BACKUP_HISTORY                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   20
    RDB$OBJECT_TYPE                 0

    RDB$USER                        4                                                                                                                                                                                                                                                           
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$BACKUP_HISTORY                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   20
    RDB$OBJECT_TYPE                 0

    RDB$USER                        4                                                                                                                                                                                                                                                           
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$BACKUP_HISTORY                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   20
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               MON$ATTACHMENTS                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               MON$CALL_STACK                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               MON$CONTEXT_VARIABLES                                                                                                                                                                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               MON$DATABASE                                                                                                                                                                                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               MON$IO_STATS                                                                                                                                                                                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               MON$MEMORY_USAGE                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               MON$RECORD_STATS                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               MON$STATEMENTS                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               MON$TABLE_STATS                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               MON$TRANSACTIONS                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$AUTH_MAPPING                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$BACKUP_HISTORY                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$CHARACTER_SETS                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$CHECK_CONSTRAINTS                                                                                                                                                                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$COLLATIONS                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$CONFIG                                                                                                                                                                                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$DATABASE                                                                                                                                                                                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$DB_CREATORS                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$DEPENDENCIES                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$EXCEPTIONS                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$FIELDS                                                                                                                                                                                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$FIELD_DIMENSIONS                                                                                                                                                                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$FILES                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$FILTERS                                                                                                                                                                                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$FORMATS                                                                                                                                                                                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$FUNCTIONS                                                                                                                                                                                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$FUNCTION_ARGUMENTS                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$GENERATORS                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$INDEX_SEGMENTS                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$INDICES                                                                                                                                                                                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$LOG_FILES                                                                                                                                                                                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$PACKAGES                                                                                                                                                                                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$PAGES                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$PROCEDURES                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$PROCEDURE_PARAMETERS                                                                                                                                                                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$PUBLICATIONS                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$PUBLICATION_TABLES                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$REF_CONSTRAINTS                                                                                                                                                                                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$RELATIONS                                                                                                                                                                                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$RELATION_CONSTRAINTS                                                                                                                                                                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$RELATION_FIELDS                                                                                                                                                                                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$ROLES                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$SECURITY_CLASSES                                                                                                                                                                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$TIME_ZONES                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$TRANSACTIONS                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$TRIGGERS                                                                                                                                                                                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$TRIGGER_MESSAGES                                                                                                                                                                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$TYPES                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$USER_PRIVILEGES                                                                                                                                                                                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               RDB$VIEW_RELATIONS                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               SEC$DB_CREATORS                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               SEC$GLOBAL_AUTH_MAPPING                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               SEC$USERS                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        PUBLIC                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                0
    RDB$RELATION_NAME               SEC$USER_ATTRIBUTES                                                                                                                                                                                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ASCII                                                                                                                                                                                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ASCII                                                                                                                                                                                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               BIG_5                                                                                                                                                                                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               BIG_5                                                                                                                                                                                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               BS_BA                                                                                                                                                                                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               CP943C                                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               CP943C                                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               CP943C_UNICODE                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               CS_CZ                                                                                                                                                                                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               CYRL                                                                                                                                                                                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               CYRL                                                                                                                                                                                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DA_DA                                                                                                                                                                                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_CSY                                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_DAN865                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_DEU437                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_DEU850                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_ESP437                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_ESP850                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_FIN437                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_FRA437                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_FRA850                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_FRC850                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_FRC863                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_ITA437                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_ITA850                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_NLD437                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_NLD850                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_NOR865                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_PLK                                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_PTB850                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_PTG860                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_RUS                                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_SLO                                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_SVE437                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_SVE850                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_TRK                                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_UK437                                                                                                                                                                                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_UK850                                                                                                                                                                                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_US437                                                                                                                                                                                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DB_US850                                                                                                                                                                                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DE_DE                                                                                                                                                                                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS437                                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS437                                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS737                                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS737                                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS775                                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS775                                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS850                                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS850                                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS852                                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS852                                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS857                                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS857                                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS858                                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS858                                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS860                                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS860                                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS861                                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS861                                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS862                                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS862                                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS863                                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS863                                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS864                                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS864                                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS865                                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS865                                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS866                                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS866                                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS869                                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DOS869                                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               DU_NL                                                                                                                                                                                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               EN_UK                                                                                                                                                                                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               EN_US                                                                                                                                                                                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ES_ES                                                                                                                                                                                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ES_ES_CI_AI                                                                                                                                                                                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               EUCJ_0208                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               EUCJ_0208                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               FI_FI                                                                                                                                                                                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               FR_CA                                                                                                                                                                                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               FR_CA_CI_AI                                                                                                                                                                                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               FR_FR                                                                                                                                                                                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               FR_FR_CI_AI                                                                                                                                                                                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               GB18030                                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               GB18030                                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               GB18030_UNICODE                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               GBK                                                                                                                                                                                                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               GBK                                                                                                                                                                                                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               GBK_UNICODE                                                                                                                                                                                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               GB_2312                                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               GB_2312                                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ISO8859_1                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ISO8859_1                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ISO8859_13                                                                                                                                                                                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ISO8859_13                                                                                                                                                                                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ISO8859_2                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ISO8859_2                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ISO8859_3                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ISO8859_3                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ISO8859_4                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ISO8859_4                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ISO8859_5                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ISO8859_5                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ISO8859_6                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ISO8859_6                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ISO8859_7                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ISO8859_7                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ISO8859_8                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ISO8859_8                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ISO8859_9                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ISO8859_9                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ISO_HUN                                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               ISO_PLK                                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               IS_IS                                                                                                                                                                                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               IT_IT                                                                                                                                                                                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               KOI8R                                                                                                                                                                                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               KOI8R                                                                                                                                                                                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               KOI8R_RU                                                                                                                                                                                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               KOI8U                                                                                                                                                                                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               KOI8U                                                                                                                                                                                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               KOI8U_UA                                                                                                                                                                                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               KSC_5601                                                                                                                                                                                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               KSC_5601                                                                                                                                                                                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               KSC_DICTIONARY                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               LT_LT                                                                                                                                                                                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$ATTACHMENTS                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$ATTACHMENTS                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$ATTACHMENTS                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$ATTACHMENTS                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$ATTACHMENTS                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$CALL_STACK                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$CALL_STACK                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$CALL_STACK                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$CALL_STACK                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$CALL_STACK                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$CONTEXT_VARIABLES                                                                                                                                                                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$CONTEXT_VARIABLES                                                                                                                                                                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$CONTEXT_VARIABLES                                                                                                                                                                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$CONTEXT_VARIABLES                                                                                                                                                                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$CONTEXT_VARIABLES                                                                                                                                                                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$DATABASE                                                                                                                                                                                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$DATABASE                                                                                                                                                                                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$DATABASE                                                                                                                                                                                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$DATABASE                                                                                                                                                                                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$DATABASE                                                                                                                                                                                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$IDLE_TIMEOUT                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$IDLE_TIMER                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$IO_STATS                                                                                                                                                                                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$IO_STATS                                                                                                                                                                                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$IO_STATS                                                                                                                                                                                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$IO_STATS                                                                                                                                                                                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$IO_STATS                                                                                                                                                                                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$MEMORY_USAGE                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$MEMORY_USAGE                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$MEMORY_USAGE                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$MEMORY_USAGE                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$MEMORY_USAGE                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$RECORD_STATS                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$RECORD_STATS                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$RECORD_STATS                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$RECORD_STATS                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$RECORD_STATS                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$SEC_DATABASE                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$STATEMENTS                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$STATEMENTS                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$STATEMENTS                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$STATEMENTS                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$STATEMENTS                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$STATEMENT_TIMEOUT                                                                                                                                                                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$STATEMENT_TIMER                                                                                                                                                                                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$TABLE_STATS                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$TABLE_STATS                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$TABLE_STATS                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$TABLE_STATS                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$TABLE_STATS                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$TRANSACTIONS                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$TRANSACTIONS                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$TRANSACTIONS                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$TRANSACTIONS                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$TRANSACTIONS                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               MON$WIRE_CRYPT_PLUGIN                                                                                                                                                                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               NEXT                                                                                                                                                                                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               NEXT                                                                                                                                                                                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               NONE                                                                                                                                                                                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               NONE                                                                                                                                                                                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               NO_NO                                                                                                                                                                                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               NXT_DEU                                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               NXT_ESP                                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               NXT_FRA                                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               NXT_ITA                                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               NXT_US                                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               OCTETS                                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               OCTETS                                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PDOX_ASCII                                                                                                                                                                                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PDOX_CSY                                                                                                                                                                                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PDOX_CYRL                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PDOX_HUN                                                                                                                                                                                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PDOX_INTL                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PDOX_ISL                                                                                                                                                                                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PDOX_NORDAN4                                                                                                                                                                                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PDOX_PLK                                                                                                                                                                                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PDOX_SLO                                                                                                                                                                                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PDOX_SWEDFIN                                                                                                                                                                                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PT_BR                                                                                                                                                                                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PT_PT                                                                                                                                                                                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PXW_CSY                                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PXW_CYRL                                                                                                                                                                                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PXW_GREEK                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PXW_HUN                                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PXW_HUNDC                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PXW_INTL                                                                                                                                                                                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PXW_INTL850                                                                                                                                                                                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PXW_NORDAN4                                                                                                                                                                                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PXW_PLK                                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PXW_SLOV                                                                                                                                                                                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PXW_SPAN                                                                                                                                                                                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PXW_SWEDFIN                                                                                                                                                                                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               PXW_TURK                                                                                                                                                                                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$ACL                                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   M     
    RDB$GRANT_OPTION                2
    RDB$RELATION_NAME               RDB$ADMIN                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  D                                                                                                                                                                                                                                                           
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 13

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$ARGUMENT_MECHANISM                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$ARGUMENT_NAME                                                                                                                                                                                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$ATTACHMENT_ID                                                                                                                                                                                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$AUTH_MAPPING                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$AUTH_MAPPING                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$AUTH_MAPPING                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$AUTH_MAPPING                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$AUTH_MAPPING                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$AUTH_METHOD                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$BACKUP_HISTORY                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$BACKUP_HISTORY                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 14

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$BACKUP_HISTORY                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$BACKUP_HISTORY                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$BACKUP_HISTORY                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$BACKUP_HISTORY                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$BACKUP_ID                                                                                                                                                                                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$BACKUP_LEVEL                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$BACKUP_STATE                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$BOOLEAN                                                                                                                                                                                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$BOUND                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CALL_ID                                                                                                                                                                                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CHARACTER_SETS                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CHARACTER_SETS                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CHARACTER_SETS                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CHARACTER_SETS                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CHARACTER_SETS                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CHARACTER_SET_ID                                                                                                                                                                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CHARACTER_SET_NAME                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CHECK_CONSTRAINTS                                                                                                                                                                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CHECK_CONSTRAINTS                                                                                                                                                                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CHECK_CONSTRAINTS                                                                                                                                                                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CHECK_CONSTRAINTS                                                                                                                                                                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CHECK_CONSTRAINTS                                                                                                                                                                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CLIENT_VERSION                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$COLLATIONS                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$COLLATIONS                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$COLLATIONS                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$COLLATIONS                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$COLLATIONS                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$COLLATION_ID                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$COLLATION_NAME                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CONFIG                                                                                                                                                                                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CONFIG                                                                                                                                                                                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CONFIG                                                                                                                                                                                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CONFIG                                                                                                                                                                                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CONFIG                                                                                                                                                                                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CONFIG_ID                                                                                                                                                                                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CONFIG_IS_SET                                                                                                                                                                                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CONFIG_NAME                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CONFIG_VALUE                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CONSTRAINT_NAME                                                                                                                                                                                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CONSTRAINT_NAME                                                                                                                                                                                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 14

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CONSTRAINT_TYPE                                                                                                                                                                                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CONTEXT_NAME                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CONTEXT_VAR_NAME                                                                                                                                                                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CONTEXT_VAR_VALUE                                                                                                                                                                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$COUNTER                                                                                                                                                                                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$CRYPT_STATE                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DATABASE                                                                                                                                                                                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DATABASE                                                                                                                                                                                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DATABASE                                                                                                                                                                                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DATABASE                                                                                                                                                                                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DATABASE                                                                                                                                                                                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DBKEY_LENGTH                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DBTZ_VERSION                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DB_CREATORS                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DB_CREATORS                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DB_CREATORS                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DB_CREATORS                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DB_CREATORS                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DEBUG_INFO                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DEFERRABLE                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DEPENDENCIES                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DEPENDENCIES                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DEPENDENCIES                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DEPENDENCIES                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DEPENDENCIES                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DESCRIPTION                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DESCRIPTOR                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DIMENSION                                                                                                                                                                                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$DIMENSIONS                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$EDIT_STRING                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$ENGINE_NAME                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$EXCEPTIONS                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$EXCEPTIONS                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 14

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$EXCEPTIONS                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$EXCEPTIONS                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$EXCEPTIONS                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$EXCEPTIONS                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$EXCEPTION_NAME                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$EXCEPTION_NUMBER                                                                                                                                                                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$EXTERNAL_DESCRIPTION                                                                                                                                                                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$EXTERNAL_NAME                                                                                                                                                                                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FIELDS                                                                                                                                                                                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FIELDS                                                                                                                                                                                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FIELDS                                                                                                                                                                                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FIELDS                                                                                                                                                                                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FIELDS                                                                                                                                                                                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FIELD_DIMENSIONS                                                                                                                                                                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FIELD_DIMENSIONS                                                                                                                                                                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FIELD_DIMENSIONS                                                                                                                                                                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FIELD_DIMENSIONS                                                                                                                                                                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FIELD_DIMENSIONS                                                                                                                                                                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FIELD_ID                                                                                                                                                                                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FIELD_LENGTH                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FIELD_NAME                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FIELD_NAME                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 14

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FIELD_POSITION                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FIELD_PRECISION                                                                                                                                                                                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FIELD_SCALE                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FIELD_SUB_TYPE                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FIELD_TYPE                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FILES                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FILES                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FILES                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FILES                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FILES                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FILE_FLAGS                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FILE_ID                                                                                                                                                                                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FILE_LENGTH                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FILE_NAME                                                                                                                                                                                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FILE_NAME2                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FILE_PARTITIONS                                                                                                                                                                                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FILE_P_OFFSET                                                                                                                                                                                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FILE_SEQUENCE                                                                                                                                                                                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FILE_START                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FILTERS                                                                                                                                                                                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FILTERS                                                                                                                                                                                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FILTERS                                                                                                                                                                                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FILTERS                                                                                                                                                                                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FILTERS                                                                                                                                                                                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FORMAT                                                                                                                                                                                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FORMATS                                                                                                                                                                                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FORMATS                                                                                                                                                                                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FORMATS                                                                                                                                                                                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FORMATS                                                                                                                                                                                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FORMATS                                                                                                                                                                                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FUNCTIONS                                                                                                                                                                                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FUNCTIONS                                                                                                                                                                                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 14

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FUNCTIONS                                                                                                                                                                                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FUNCTIONS                                                                                                                                                                                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FUNCTIONS                                                                                                                                                                                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FUNCTIONS                                                                                                                                                                                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FUNCTION_ARGUMENTS                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FUNCTION_ARGUMENTS                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FUNCTION_ARGUMENTS                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FUNCTION_ARGUMENTS                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FUNCTION_ARGUMENTS                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FUNCTION_BLR                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FUNCTION_ID                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FUNCTION_NAME                                                                                                                                                                                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$FUNCTION_TYPE                                                                                                                                                                                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$GENERATORS                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$GENERATORS                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$GENERATORS                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$GENERATORS                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$GENERATORS                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$GENERATOR_ID                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$GENERATOR_INCREMENT                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$GENERATOR_NAME                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$GENERATOR_NAME                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 14

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$GENERATOR_VALUE                                                                                                                                                                                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$GENERIC_NAME                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$GENERIC_TYPE                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$GUID                                                                                                                                                                                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$HOST_NAME                                                                                                                                                                                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$IDENTITY_TYPE                                                                                                                                                                                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$INDEX_ID                                                                                                                                                                                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$INDEX_NAME                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$INDEX_NAME                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 14

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$INDEX_SEGMENTS                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$INDEX_SEGMENTS                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$INDEX_SEGMENTS                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$INDEX_SEGMENTS                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$INDEX_SEGMENTS                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$INDICES                                                                                                                                                                                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$INDICES                                                                                                                                                                                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$INDICES                                                                                                                                                                                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$INDICES                                                                                                                                                                                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$INDICES                                                                                                                                                                                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$ISOLATION_MODE                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$LINGER                                                                                                                                                                                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$LOCK_TIMEOUT                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$LOG_FILES                                                                                                                                                                                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$LOG_FILES                                                                                                                                                                                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$LOG_FILES                                                                                                                                                                                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$LOG_FILES                                                                                                                                                                                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$LOG_FILES                                                                                                                                                                                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$MAP_DB                                                                                                                                                                                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$MAP_FROM                                                                                                                                                                                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$MAP_FROM_TYPE                                                                                                                                                                                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$MAP_NAME                                                                                                                                                                                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$MAP_TO                                                                                                                                                                                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$MAP_USING                                                                                                                                                                                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$MATCH_OPTION                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$MECHANISM                                                                                                                                                                                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$MESSAGE                                                                                                                                                                                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$MESSAGE_NUMBER                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$NULL_FLAG                                                                                                                                                                                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$NUMBER_OF_CHARACTERS                                                                                                                                                                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$OBJECT_TYPE                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$ODS_NUMBER                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$OS_USER                                                                                                                                                                                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PACKAGES                                                                                                                                                                                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PACKAGES                                                                                                                                                                                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PACKAGES                                                                                                                                                                                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PACKAGES                                                                                                                                                                                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PACKAGES                                                                                                                                                                                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PACKAGE_NAME                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PAGES                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PAGES                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PAGES                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PAGES                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PAGES                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PAGE_BUFFERS                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PAGE_NUMBER                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PAGE_SEQUENCE                                                                                                                                                                                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PAGE_SIZE                                                                                                                                                                                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PAGE_TYPE                                                                                                                                                                                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PARAMETER_MECHANISM                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PARAMETER_NAME                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PARAMETER_NUMBER                                                                                                                                                                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PARAMETER_TYPE                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PID                                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PLAN                                                                                                                                                                                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PLUGIN                                                                                                                                                                                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PRIVILEGE                                                                                                                                                                                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PROCEDURES                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PROCEDURES                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 14

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PROCEDURES                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PROCEDURES                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PROCEDURES                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PROCEDURES                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PROCEDURE_BLR                                                                                                                                                                                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PROCEDURE_ID                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PROCEDURE_NAME                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PROCEDURE_PARAMETERS                                                                                                                                                                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PROCEDURE_PARAMETERS                                                                                                                                                                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PROCEDURE_PARAMETERS                                                                                                                                                                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PROCEDURE_PARAMETERS                                                                                                                                                                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PROCEDURE_PARAMETERS                                                                                                                                                                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PROCEDURE_PARAMETERS                                                                                                                                                                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PROCEDURE_TYPE                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PUBLICATIONS                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PUBLICATIONS                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PUBLICATIONS                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PUBLICATIONS                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PUBLICATIONS                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PUBLICATION_NAME                                                                                                                                                                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PUBLICATION_TABLES                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PUBLICATION_TABLES                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PUBLICATION_TABLES                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PUBLICATION_TABLES                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$PUBLICATION_TABLES                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$QUERY_HEADER                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$REF_CONSTRAINTS                                                                                                                                                                                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$REF_CONSTRAINTS                                                                                                                                                                                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$REF_CONSTRAINTS                                                                                                                                                                                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$REF_CONSTRAINTS                                                                                                                                                                                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$REF_CONSTRAINTS                                                                                                                                                                                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$RELATIONS                                                                                                                                                                                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$RELATIONS                                                                                                                                                                                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$RELATIONS                                                                                                                                                                                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$RELATIONS                                                                                                                                                                                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$RELATIONS                                                                                                                                                                                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$RELATION_CONSTRAINTS                                                                                                                                                                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$RELATION_CONSTRAINTS                                                                                                                                                                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$RELATION_CONSTRAINTS                                                                                                                                                                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$RELATION_CONSTRAINTS                                                                                                                                                                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$RELATION_CONSTRAINTS                                                                                                                                                                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$RELATION_FIELDS                                                                                                                                                                                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$RELATION_FIELDS                                                                                                                                                                                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$RELATION_FIELDS                                                                                                                                                                                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$RELATION_FIELDS                                                                                                                                                                                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$RELATION_FIELDS                                                                                                                                                                                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$RELATION_ID                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$RELATION_NAME                                                                                                                                                                                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$RELATION_TYPE                                                                                                                                                                                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$REMOTE_ADDRESS                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$REMOTE_PROTOCOL                                                                                                                                                                                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$REMOTE_VERSION                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$REPLICA_MODE                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$ROLES                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$ROLES                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$ROLES                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$ROLES                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$ROLES                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$RULE                                                                                                                                                                                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$RUNTIME                                                                                                                                                                                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$SCN                                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$SECURITY_CLASS                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$SECURITY_CLASS                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 14

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$SECURITY_CLASSES                                                                                                                                                                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$SECURITY_CLASSES                                                                                                                                                                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$SECURITY_CLASSES                                                                                                                                                                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$SECURITY_CLASSES                                                                                                                                                                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$SECURITY_CLASSES                                                                                                                                                                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$SEGMENT_COUNT                                                                                                                                                                                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$SEGMENT_LENGTH                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$SHADOW_NUMBER                                                                                                                                                                                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$SHUTDOWN_MODE                                                                                                                                                                                                                                           
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$SOURCE                                                                                                                                                                                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$SOURCE_INFO                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$SPECIFIC_ATTRIBUTES                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$SQL_DIALECT                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$SQL_SECURITY                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$STATE                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$STATEMENT_ID                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$STATISTICS                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$STAT_GROUP                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$STAT_ID                                                                                                                                                                                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$SWEEP_INTERVAL                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$SYSTEM_FLAG                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$SYSTEM_NULLFLAG                                                                                                                                                                                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$SYSTEM_PRIVILEGES                                                                                                                                                                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TIMESTAMP                                                                                                                                                                                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TIMESTAMP_TZ                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TIME_ZONES                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TIME_ZONES                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TIME_ZONES                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TIME_ZONES                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TIME_ZONES                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TIME_ZONE_ID                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TIME_ZONE_NAME                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TIME_ZONE_OFFSET                                                                                                                                                                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   X     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TIME_ZONE_UTIL                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 18

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRANSACTIONS                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRANSACTIONS                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRANSACTIONS                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRANSACTIONS                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRANSACTIONS                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRANSACTION_DESCRIPTION                                                                                                                                                                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRANSACTION_ID                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRANSACTION_STATE                                                                                                                                                                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRIGGERS                                                                                                                                                                                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRIGGERS                                                                                                                                                                                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRIGGERS                                                                                                                                                                                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRIGGERS                                                                                                                                                                                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRIGGERS                                                                                                                                                                                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRIGGER_BLR                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRIGGER_MESSAGES                                                                                                                                                                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRIGGER_MESSAGES                                                                                                                                                                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRIGGER_MESSAGES                                                                                                                                                                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRIGGER_MESSAGES                                                                                                                                                                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRIGGER_MESSAGES                                                                                                                                                                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRIGGER_NAME                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRIGGER_NAME                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 14

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRIGGER_SEQUENCE                                                                                                                                                                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TRIGGER_TYPE                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TYPES                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TYPES                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TYPES                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TYPES                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TYPES                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$TYPE_NAME                                                                                                                                                                                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$USER                                                                                                                                                                                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$USER_PRIVILEGES                                                                                                                                                                                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$USER_PRIVILEGES                                                                                                                                                                                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$USER_PRIVILEGES                                                                                                                                                                                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$USER_PRIVILEGES                                                                                                                                                                                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$USER_PRIVILEGES                                                                                                                                                                                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$VALIDATION_BLR                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$VALUE                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$VIEW_BLR                                                                                                                                                                                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$VIEW_CONTEXT                                                                                                                                                                                                                                            
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$VIEW_RELATIONS                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$VIEW_RELATIONS                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$VIEW_RELATIONS                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$VIEW_RELATIONS                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               RDB$VIEW_RELATIONS                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$DB_CREATORS                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$DB_CREATORS                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$DB_CREATORS                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$DB_CREATORS                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$DB_CREATORS                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$GLOBAL_AUTH_MAPPING                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$GLOBAL_AUTH_MAPPING                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$GLOBAL_AUTH_MAPPING                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$GLOBAL_AUTH_MAPPING                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$GLOBAL_AUTH_MAPPING                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$KEY                                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$NAME_PART                                                                                                                                                                                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$USERS                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$USERS                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$USERS                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$USERS                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$USERS                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   D     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$USER_ATTRIBUTES                                                                                                                                                                                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   I     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$USER_ATTRIBUTES                                                                                                                                                                                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   R     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$USER_ATTRIBUTES                                                                                                                                                                                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   S     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$USER_ATTRIBUTES                                                                                                                                                                                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   U     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$USER_ATTRIBUTES                                                                                                                                                                                                                                         
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 0

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$USER_NAME                                                                                                                                                                                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SEC$VALUE                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 9

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SJIS_0208                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SJIS_0208                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SQL$DEFAULT                                                                                                                                                                                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 14

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               SV_SV                                                                                                                                                                                                                                                       
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               TIS620                                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               TIS620                                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               TIS620_UNICODE                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               UCS_BASIC                                                                                                                                                                                                                                                   
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               UNICODE                                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               UNICODE_CI                                                                                                                                                                                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               UNICODE_CI_AI                                                                                                                                                                                                                                               
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               UNICODE_FSS                                                                                                                                                                                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               UNICODE_FSS                                                                                                                                                                                                                                                 
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               UTF8                                                                                                                                                                                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               UTF8                                                                                                                                                                                                                                                        
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN1250                                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN1250                                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN1251                                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN1251                                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN1251_UA                                                                                                                                                                                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN1252                                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN1252                                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN1253                                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN1253                                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN1254                                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN1254                                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN1255                                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN1255                                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN1256                                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN1256                                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN1257                                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN1257                                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN1257_EE                                                                                                                                                                                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN1257_LT                                                                                                                                                                                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN1257_LV                                                                                                                                                                                                                                                  
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN1258                                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 11

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN1258                                                                                                                                                                                                                                                     
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN_CZ                                                                                                                                                                                                                                                      
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN_CZ_CI_AI                                                                                                                                                                                                                                                
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17

    RDB$USER                        SYSDBA                                                                                                                                                                                                                                                      
    RDB$GRANTOR                     <null>
    RDB$PRIVILEGE                   G     
    RDB$GRANT_OPTION                1
    RDB$RELATION_NAME               WIN_PTBR                                                                                                                                                                                                                                                    
    RDB$FIELD_NAME                  <null>
    RDB$USER_TYPE                   8
    RDB$OBJECT_TYPE                 17


    Records affected: 723

    Are ordered columns unique ?    1
  """

@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_expected_stdout == act_2.clean_stdout

