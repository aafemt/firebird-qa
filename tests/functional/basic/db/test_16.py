#coding:utf-8
#
# id:           functional.basic.db.db_16
# title:        Empty DB - RDB$INDICES
# decription:   
#                   Check for correct content of RDB$INDICES in empty database.
#                   Checked on:
#                       2.5.9.27126: OK, 0.640s.
#                       3.0.5.33086: OK, 1.532s.
#                       4.0.0.1378: OK, 5.922s.
#                 
# tracker_id:   
# min_versions: []
# versions:     3.0, 4.0
# qmid:         functional.basic.db.db_16

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 3.0
# resources: None

substitutions_1 = [('RDB\\$INDEX_NAME[\\s]+RDB\\$INDEX.*', 'RDB\\$INDEX_NAME RDB\\$INDEX'), ('DECRIPTN_BLOB_ID.*', ''), ('EXPR_BLR_BLOB_ID.*', ''), ('EXPR_SRC_BLOB_ID.*', '')]

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """
    -- 28.10.2015:
    -- Added blocks in subst-section in order to ignore concrete values in RBD$INDEX_** (i.e. suffixes).
    -- Moved all BLOB fields at the end of output, suppress comparison of their IDs.
    -- Added query to select FIELDS list of table because main check does not use asterisk
    -- and we have to know if DDL of table will have any changes in future.
    
    set list on;
    set blob all;
    set count on;

    -- Query for check whether fields list of table was changed:
    select rf.rdb$field_name
    from rdb$relation_fields rf
    where rf.rdb$relation_name = upper('rdb$indices')
    order by rf.rdb$field_name;

    -- Main test query:
    select
        rdb$index_name
        ,rdb$relation_name
        ,rdb$index_id
        ,rdb$unique_flag
        ,rdb$segment_count
        ,rdb$index_inactive
        ,rdb$index_type
        ,rdb$system_flag
        ,rdb$statistics
        ,rdb$foreign_key
        ,rdb$description        as decriptn_blob_id
        ,rdb$expression_blr     as expr_blr_blob_id
        ,rdb$expression_source  as expr_src_blob_id
    from rdb$indices
    order by rdb$index_name;
  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    RDB$FIELD_NAME                  RDB$DESCRIPTION                                                                              
    RDB$FIELD_NAME                  RDB$EXPRESSION_BLR                                                                           
    RDB$FIELD_NAME                  RDB$EXPRESSION_SOURCE                                                                        
    RDB$FIELD_NAME                  RDB$FOREIGN_KEY                                                                              
    RDB$FIELD_NAME                  RDB$INDEX_ID                                                                                 
    RDB$FIELD_NAME                  RDB$INDEX_INACTIVE                                                                           
    RDB$FIELD_NAME                  RDB$INDEX_NAME                                                                               
    RDB$FIELD_NAME                  RDB$INDEX_TYPE                                                                               
    RDB$FIELD_NAME                  RDB$RELATION_NAME                                                                            
    RDB$FIELD_NAME                  RDB$SEGMENT_COUNT                                                                            
    RDB$FIELD_NAME                  RDB$STATISTICS                                                                               
    RDB$FIELD_NAME                  RDB$SYSTEM_FLAG                                                                              
    RDB$FIELD_NAME                  RDB$UNIQUE_FLAG                                                                              
    Records affected: 13

    RDB$INDEX_NAME                  RDB$INDEX_0                                                                                  
    RDB$RELATION_NAME               RDB$RELATIONS                                                                                
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_1                                                                                  
    RDB$RELATION_NAME               RDB$RELATIONS                                                                                
    RDB$INDEX_ID                    2
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_10                                                                                 
    RDB$RELATION_NAME               RDB$FUNCTION_ARGUMENTS                                                                       
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               2
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_11                                                                                 
    RDB$RELATION_NAME               RDB$GENERATORS                                                                               
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_12                                                                                 
    RDB$RELATION_NAME               RDB$RELATION_CONSTRAINTS                                                                     
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_13                                                                                 
    RDB$RELATION_NAME               RDB$REF_CONSTRAINTS                                                                          
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_14                                                                                 
    RDB$RELATION_NAME               RDB$CHECK_CONSTRAINTS                                                                        
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_15                                                                                 
    RDB$RELATION_NAME               RDB$RELATION_FIELDS                                                                          
    RDB$INDEX_ID                    3
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               2
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_16                                                                                 
    RDB$RELATION_NAME               RDB$FORMATS                                                                                  
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               2
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_17                                                                                 
    RDB$RELATION_NAME               RDB$FILTERS                                                                                  
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               2
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_18                                                                                 
    RDB$RELATION_NAME               RDB$PROCEDURE_PARAMETERS                                                                     
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               3
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_19                                                                                 
    RDB$RELATION_NAME               RDB$CHARACTER_SETS                                                                           
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_2                                                                                  
    RDB$RELATION_NAME               RDB$FIELDS                                                                                   
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_20                                                                                 
    RDB$RELATION_NAME               RDB$COLLATIONS                                                                               
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_21                                                                                 
    RDB$RELATION_NAME               RDB$PROCEDURES                                                                               
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               2
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_22                                                                                 
    RDB$RELATION_NAME               RDB$PROCEDURES                                                                               
    RDB$INDEX_ID                    2
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_23                                                                                 
    RDB$RELATION_NAME               RDB$EXCEPTIONS                                                                               
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_24                                                                                 
    RDB$RELATION_NAME               RDB$EXCEPTIONS                                                                               
    RDB$INDEX_ID                    2
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_25                                                                                 
    RDB$RELATION_NAME               RDB$CHARACTER_SETS                                                                           
    RDB$INDEX_ID                    2
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_26                                                                                 
    RDB$RELATION_NAME               RDB$COLLATIONS                                                                               
    RDB$INDEX_ID                    2
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               2
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_27                                                                                 
    RDB$RELATION_NAME               RDB$DEPENDENCIES                                                                             
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_28                                                                                 
    RDB$RELATION_NAME               RDB$DEPENDENCIES                                                                             
    RDB$INDEX_ID                    2
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_29                                                                                 
    RDB$RELATION_NAME               RDB$USER_PRIVILEGES                                                                          
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_3                                                                                  
    RDB$RELATION_NAME               RDB$RELATION_FIELDS                                                                          
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_30                                                                                 
    RDB$RELATION_NAME               RDB$USER_PRIVILEGES                                                                          
    RDB$INDEX_ID                    2
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_31                                                                                 
    RDB$RELATION_NAME               RDB$INDICES                                                                                  
    RDB$INDEX_ID                    2
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_32                                                                                 
    RDB$RELATION_NAME               RDB$TRANSACTIONS                                                                             
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_33                                                                                 
    RDB$RELATION_NAME               RDB$VIEW_RELATIONS                                                                           
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_34                                                                                 
    RDB$RELATION_NAME               RDB$VIEW_RELATIONS                                                                           
    RDB$INDEX_ID                    2
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_35                                                                                 
    RDB$RELATION_NAME               RDB$TRIGGER_MESSAGES                                                                         
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_36                                                                                 
    RDB$RELATION_NAME               RDB$FIELD_DIMENSIONS                                                                         
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_37                                                                                 
    RDB$RELATION_NAME               RDB$TYPES                                                                                    
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_38                                                                                 
    RDB$RELATION_NAME               RDB$TRIGGERS                                                                                 
    RDB$INDEX_ID                    2
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_39                                                                                 
    RDB$RELATION_NAME               RDB$ROLES                                                                                    
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_4                                                                                  
    RDB$RELATION_NAME               RDB$RELATION_FIELDS                                                                          
    RDB$INDEX_ID                    2
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_40                                                                                 
    RDB$RELATION_NAME               RDB$CHECK_CONSTRAINTS                                                                        
    RDB$INDEX_ID                    2
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_41                                                                                 
    RDB$RELATION_NAME               RDB$INDICES                                                                                  
    RDB$INDEX_ID                    3
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_42                                                                                 
    RDB$RELATION_NAME               RDB$RELATION_CONSTRAINTS                                                                     
    RDB$INDEX_ID                    2
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               2
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_43                                                                                 
    RDB$RELATION_NAME               RDB$RELATION_CONSTRAINTS                                                                     
    RDB$INDEX_ID                    3
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_44                                                                                 
    RDB$RELATION_NAME               RDB$BACKUP_HISTORY                                                                           
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               2
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  1
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_45                                                                                 
    RDB$RELATION_NAME               RDB$FILTERS                                                                                  
    RDB$INDEX_ID                    2
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_46                                                                                 
    RDB$RELATION_NAME               RDB$GENERATORS                                                                               
    RDB$INDEX_ID                    2
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_47                                                                                 
    RDB$RELATION_NAME               RDB$PACKAGES                                                                                 
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_48                                                                                 
    RDB$RELATION_NAME               RDB$PROCEDURE_PARAMETERS                                                                     
    RDB$INDEX_ID                    2
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_49                                                                                 
    RDB$RELATION_NAME               RDB$FUNCTION_ARGUMENTS                                                                       
    RDB$INDEX_ID                    2
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_5                                                                                  
    RDB$RELATION_NAME               RDB$INDICES                                                                                  
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_50                                                                                 
    RDB$RELATION_NAME               RDB$PROCEDURE_PARAMETERS                                                                     
    RDB$INDEX_ID                    3
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               2
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_51                                                                                 
    RDB$RELATION_NAME               RDB$FUNCTION_ARGUMENTS                                                                       
    RDB$INDEX_ID                    3
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               2
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_52                                                                                 
    RDB$RELATION_NAME               RDB$AUTH_MAPPING                                                                             
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_53                                                                                 
    RDB$RELATION_NAME               RDB$FUNCTIONS                                                                                
    RDB$INDEX_ID                    2
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_6                                                                                  
    RDB$RELATION_NAME               RDB$INDEX_SEGMENTS                                                                           
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_7                                                                                  
    RDB$RELATION_NAME               RDB$SECURITY_CLASSES                                                                         
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_8                                                                                  
    RDB$RELATION_NAME               RDB$TRIGGERS                                                                                 
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_9                                                                                  
    RDB$RELATION_NAME               RDB$FUNCTIONS                                                                                
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               2
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>
    Records affected: 54
  """

@pytest.mark.version('>=3.0,<4.0')
def test_db_16_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_expected_stdout == act_1.clean_stdout

# version: 4.0
# resources: None

substitutions_2 = [('RDB\\$INDEX_NAME[\\s]+RDB\\$INDEX.*', 'RDB\\$INDEX_NAME RDB\\$INDEX'), ('DECRIPTN_BLOB_ID.*', ''), ('EXPR_BLR_BLOB_ID.*', ''), ('EXPR_SRC_BLOB_ID.*', '')]

init_script_2 = """"""

db_2 = db_factory(sql_dialect=3, init=init_script_2)

test_script_2 = """
    -- 28.10.2015:
    -- Added blocks in subst-section in order to ignore concrete values in RBD$INDEX_** (i.e. suffixes).
    -- Moved all BLOB fields at the end of output, suppress comparison of their IDs.
    -- Added query to select FIELDS list of table because main check does not use asterisk
    -- and we have to know if DDL of table will have any changes in future.
    
    set list on;
    set blob all;
    set count on;

    -- Query for check whether fields list of table was changed:
    select rf.rdb$field_name
    from rdb$relation_fields rf
    where rf.rdb$relation_name = upper('rdb$indices')
    order by rf.rdb$field_name;

    -- Main test query:
    select
        rdb$index_name
        ,rdb$relation_name
        ,rdb$index_id
        ,rdb$unique_flag
        ,rdb$segment_count
        ,rdb$index_inactive
        ,rdb$index_type
        ,rdb$system_flag
        ,rdb$statistics
        ,rdb$foreign_key
        ,rdb$description        as decriptn_blob_id
        ,rdb$expression_blr     as expr_blr_blob_id
        ,rdb$expression_source  as expr_src_blob_id
    from rdb$indices
    order by rdb$index_name;
  """

act_2 = isql_act('db_2', test_script_2, substitutions=substitutions_2)

expected_stdout_2 = """
    RDB$FIELD_NAME                  RDB$DESCRIPTION                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  RDB$EXPRESSION_BLR                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  RDB$EXPRESSION_SOURCE                                                                                                                                                                                                                                       
    RDB$FIELD_NAME                  RDB$FOREIGN_KEY                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  RDB$INDEX_ID                                                                                                                                                                                                                                                
    RDB$FIELD_NAME                  RDB$INDEX_INACTIVE                                                                                                                                                                                                                                          
    RDB$FIELD_NAME                  RDB$INDEX_NAME                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  RDB$INDEX_TYPE                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  RDB$RELATION_NAME                                                                                                                                                                                                                                           
    RDB$FIELD_NAME                  RDB$SEGMENT_COUNT                                                                                                                                                                                                                                           
    RDB$FIELD_NAME                  RDB$STATISTICS                                                                                                                                                                                                                                              
    RDB$FIELD_NAME                  RDB$SYSTEM_FLAG                                                                                                                                                                                                                                             
    RDB$FIELD_NAME                  RDB$UNIQUE_FLAG                                                                                                                                                                                                                                             

    Records affected: 13


    RDB$INDEX_NAME                  RDB$INDEX_0                                                                                                                                                                                                                                                 
    RDB$RELATION_NAME               RDB$RELATIONS                                                                                                                                                                                                                                               
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_1                                                                                                                                                                                                                                                 
    RDB$RELATION_NAME               RDB$RELATIONS                                                                                                                                                                                                                                               
    RDB$INDEX_ID                    2
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_10                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$FUNCTION_ARGUMENTS                                                                                                                                                                                                                                      
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               2
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_11                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$GENERATORS                                                                                                                                                                                                                                              
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_12                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$RELATION_CONSTRAINTS                                                                                                                                                                                                                                    
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_13                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$REF_CONSTRAINTS                                                                                                                                                                                                                                         
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_14                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$CHECK_CONSTRAINTS                                                                                                                                                                                                                                       
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_15                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$RELATION_FIELDS                                                                                                                                                                                                                                         
    RDB$INDEX_ID                    3
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               2
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_16                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$FORMATS                                                                                                                                                                                                                                                 
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               2
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_17                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$FILTERS                                                                                                                                                                                                                                                 
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               2
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_18                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$PROCEDURE_PARAMETERS                                                                                                                                                                                                                                    
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               3
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_19                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$CHARACTER_SETS                                                                                                                                                                                                                                          
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_2                                                                                                                                                                                                                                                 
    RDB$RELATION_NAME               RDB$FIELDS                                                                                                                                                                                                                                                  
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_20                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$COLLATIONS                                                                                                                                                                                                                                              
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_21                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$PROCEDURES                                                                                                                                                                                                                                              
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               2
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_22                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$PROCEDURES                                                                                                                                                                                                                                              
    RDB$INDEX_ID                    2
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_23                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$EXCEPTIONS                                                                                                                                                                                                                                              
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_24                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$EXCEPTIONS                                                                                                                                                                                                                                              
    RDB$INDEX_ID                    2
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_25                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$CHARACTER_SETS                                                                                                                                                                                                                                          
    RDB$INDEX_ID                    2
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_26                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$COLLATIONS                                                                                                                                                                                                                                              
    RDB$INDEX_ID                    2
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               2
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_27                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$DEPENDENCIES                                                                                                                                                                                                                                            
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               2
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_28                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$DEPENDENCIES                                                                                                                                                                                                                                            
    RDB$INDEX_ID                    2
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               3
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_29                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$USER_PRIVILEGES                                                                                                                                                                                                                                         
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_3                                                                                                                                                                                                                                                 
    RDB$RELATION_NAME               RDB$RELATION_FIELDS                                                                                                                                                                                                                                         
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_30                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$USER_PRIVILEGES                                                                                                                                                                                                                                         
    RDB$INDEX_ID                    2
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_31                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$INDICES                                                                                                                                                                                                                                                 
    RDB$INDEX_ID                    2
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_32                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$TRANSACTIONS                                                                                                                                                                                                                                            
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_33                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$VIEW_RELATIONS                                                                                                                                                                                                                                          
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_34                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$VIEW_RELATIONS                                                                                                                                                                                                                                          
    RDB$INDEX_ID                    2
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_35                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$TRIGGER_MESSAGES                                                                                                                                                                                                                                        
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_36                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$FIELD_DIMENSIONS                                                                                                                                                                                                                                        
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_37                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$TYPES                                                                                                                                                                                                                                                   
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_38                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$TRIGGERS                                                                                                                                                                                                                                                
    RDB$INDEX_ID                    2
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_39                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$ROLES                                                                                                                                                                                                                                                   
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_4                                                                                                                                                                                                                                                 
    RDB$RELATION_NAME               RDB$RELATION_FIELDS                                                                                                                                                                                                                                         
    RDB$INDEX_ID                    2
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_40                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$CHECK_CONSTRAINTS                                                                                                                                                                                                                                       
    RDB$INDEX_ID                    2
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_41                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$INDICES                                                                                                                                                                                                                                                 
    RDB$INDEX_ID                    3
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_42                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$RELATION_CONSTRAINTS                                                                                                                                                                                                                                    
    RDB$INDEX_ID                    2
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               2
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_43                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$RELATION_CONSTRAINTS                                                                                                                                                                                                                                    
    RDB$INDEX_ID                    3
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_44                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$BACKUP_HISTORY                                                                                                                                                                                                                                          
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               2
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  1
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_45                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$FILTERS                                                                                                                                                                                                                                                 
    RDB$INDEX_ID                    2
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_46                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$GENERATORS                                                                                                                                                                                                                                              
    RDB$INDEX_ID                    2
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_47                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$PACKAGES                                                                                                                                                                                                                                                
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_48                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$PROCEDURE_PARAMETERS                                                                                                                                                                                                                                    
    RDB$INDEX_ID                    2
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_49                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$FUNCTION_ARGUMENTS                                                                                                                                                                                                                                      
    RDB$INDEX_ID                    2
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_5                                                                                                                                                                                                                                                 
    RDB$RELATION_NAME               RDB$INDICES                                                                                                                                                                                                                                                 
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_50                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$PROCEDURE_PARAMETERS                                                                                                                                                                                                                                    
    RDB$INDEX_ID                    3
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               2
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_51                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$FUNCTION_ARGUMENTS                                                                                                                                                                                                                                      
    RDB$INDEX_ID                    3
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               2
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_52                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$AUTH_MAPPING                                                                                                                                                                                                                                            
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_53                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$FUNCTIONS                                                                                                                                                                                                                                               
    RDB$INDEX_ID                    2
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_54                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$BACKUP_HISTORY                                                                                                                                                                                                                                          
    RDB$INDEX_ID                    2
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_55                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$PUBLICATIONS                                                                                                                                                                                                                                            
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_56                                                                                                                                                                                                                                                
    RDB$RELATION_NAME               RDB$PUBLICATION_TABLES                                                                                                                                                                                                                                      
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               2
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_6                                                                                                                                                                                                                                                 
    RDB$RELATION_NAME               RDB$INDEX_SEGMENTS                                                                                                                                                                                                                                          
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 0
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_7                                                                                                                                                                                                                                                 
    RDB$RELATION_NAME               RDB$SECURITY_CLASSES                                                                                                                                                                                                                                        
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_8                                                                                                                                                                                                                                                 
    RDB$RELATION_NAME               RDB$TRIGGERS                                                                                                                                                                                                                                                
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               1
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>

    RDB$INDEX_NAME                  RDB$INDEX_9                                                                                                                                                                                                                                                 
    RDB$RELATION_NAME               RDB$FUNCTIONS                                                                                                                                                                                                                                               
    RDB$INDEX_ID                    1
    RDB$UNIQUE_FLAG                 1
    RDB$SEGMENT_COUNT               2
    RDB$INDEX_INACTIVE              0
    RDB$INDEX_TYPE                  <null>
    RDB$SYSTEM_FLAG                 1
    RDB$STATISTICS                  <null>
    RDB$FOREIGN_KEY                 <null>
    DECRIPTN_BLOB_ID                <null>
    EXPR_BLR_BLOB_ID                <null>
    EXPR_SRC_BLOB_ID                <null>


    Records affected: 57
  """

@pytest.mark.version('>=4.0')
def test_db_16_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_expected_stdout == act_2.clean_stdout

