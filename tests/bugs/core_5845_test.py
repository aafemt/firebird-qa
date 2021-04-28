#coding:utf-8
#
# id:           bugs.core_5845
# title:        ORDER BY on index can cause suboptimal index choices
# decription:   
#                     Confirmed ineffective plan on: 3.0.4.33053, 4.0.0.1249
#                     Works fine on:
#                       3.0.5.33084: OK, 1.344s.
#                       4.0.0.1340: OK, 2.594s.
#                 
# tracker_id:   CORE-5845
# min_versions: ['3.0.4']
# versions:     3.0.4
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 3.0.4
# resources: None

substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """
    recreate table test 
    ( 
        id1 integer, 
        id2 integer, 
        id3 integer, 
        x numeric(18,2), 
        constraint pk_test primary key(id1, id2, id3) 
    ); 
    create index ixa_test__x on test(x); 
    create index ixa_test__id1_x on test(id1, x); 
    commit;
    -------------------------------------------------------------------------------- 

    set plan on;

    select * 
    from test t 
    where t.id1=1 and t.x>0 
    ;
    --plan (t index (ixa_test__id1_x)) 
    --index ixa_test__id1_x is used 

    -------------------------------------------------------------------------------- 

    select * from test t 
    where t.id1=1 and t.x>0 
    order by t.id1, t.id2, t.id3 
    ;
    --plan (t order pk_test index (ixa_test__x)) 
    --index ixa_test__x - suboptimal 
    --as you can see adding order by which consume some index (pk_test) 
    --cause suboptimal choice of index (ixa_test__x) 

    -------------------------------------------------------------------------------- 

    --if query is changed to order by not by index 
    --plan sort (t index (ixa_test__id1_x)) 

    select * from test t 
    where 
        t.id1=1 
        and t.x>0 
    order by t.id1+0, t.id2, t.id3 
    ;
  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    PLAN (T INDEX (IXA_TEST__ID1_X))
    PLAN SORT (T INDEX (IXA_TEST__ID1_X))
    PLAN SORT (T INDEX (IXA_TEST__ID1_X))
  """

@pytest.mark.version('>=3.0.4')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_expected_stdout == act_1.clean_stdout

