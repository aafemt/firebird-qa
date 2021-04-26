#coding:utf-8
#
# id:           bugs.core_4466
# title:        Add DROP NOT NULL to ALTER COLUMN
# decription:   This test does NOT verifies work when table has some data. It only checks ability to issue DDL statement
# tracker_id:   CORE-4466
# min_versions: ['3.0']
# versions:     3.0
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 3.0
# resources: None

substitutions_1 = [('=.*', '')]

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """
    set autoddl off;
    commit;
    
    create or alter view v_test_fields as
    select rf.rdb$field_name fld_name, coalesce(rf.rdb$null_flag, 0) is_NOT_null
    from rdb$relation_fields rf
    where rf.rdb$relation_name = upper('TEST')
    order by rf.rdb$field_position;
    commit;
    
    set width fld_name 10;
    
    recreate table test(
      si smallint not null
     ,ni int not null
     ,bi bigint not null
     ,nf numeric(18,0) not null
     ,dp double precision not null
     ,dt date not null
     ,tm time not null
     ,ts timestamp not null
     ,ss varchar(100) not null
     ,bs blob not null
    );
    commit;
    
    select 'init metadata' msg, v.* from v_test_fields v;
    
    alter table test
      alter si drop not null
     ,alter ni drop not null
     ,alter bi drop not null
     ,alter nf drop not null
     ,alter dp drop not null
     ,alter dt drop not null
     ,alter tm drop not null
     ,alter ts drop not null
     ,alter ss drop not null
     ,alter bs drop not null
    ;
    
    select 'drop not null' msg,v.* from v_test_fields v;
    
    alter table test
      alter si set not null
     ,alter ni set not null
     ,alter bi set not null
     ,alter nf set not null
     ,alter dp set not null
     ,alter dt set not null
     ,alter tm set not null
     ,alter ts set not null
     ,alter ss set not null
     ,alter bs set not null
    ;
    
    select 'reset not null' msg, v.* from v_test_fields v;
  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    MSG           FLD_NAME    IS_NOT_NULL
    ============= ========== ============
    init metadata SI                    1
    init metadata NI                    1
    init metadata BI                    1
    init metadata NF                    1
    init metadata DP                    1
    init metadata DT                    1
    init metadata TM                    1
    init metadata TS                    1
    init metadata SS                    1
    init metadata BS                    1
    
    
    MSG           FLD_NAME    IS_NOT_NULL
    ============= ========== ============
    drop not null SI                    0
    drop not null NI                    0
    drop not null BI                    0
    drop not null NF                    0
    drop not null DP                    0
    drop not null DT                    0
    drop not null TM                    0
    drop not null TS                    0
    drop not null SS                    0
    drop not null BS                    0
    
    
    MSG            FLD_NAME    IS_NOT_NULL
    ============== ========== ============
    reset not null SI                    1
    reset not null NI                    1
    reset not null BI                    1
    reset not null NF                    1
    reset not null DP                    1
    reset not null DT                    1
    reset not null TM                    1
    reset not null TS                    1
    reset not null SS                    1
    reset not null BS                    1
    
  """

@pytest.mark.version('>=3.0')
def test_core_4466_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_expected_stdout == act_1.clean_stdout

