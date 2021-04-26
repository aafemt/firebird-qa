#coding:utf-8
#
# id:           bugs.core_3611
# title:        Wrong data while retrieving from CTEs (or derived tables) with same column names
# decription:   
# tracker_id:   CORE-3611
# min_versions: ['2.5.2']
# versions:     2.5.2
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 2.5.2
# resources: None

substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """
    recreate table t(
      tab_name char(31) character set unicode_fss,
      sum1_abc int,
      sum1_oth int,
      sum2_abc int,
      sum2_oth int
    );
    commit;
    
    insert into t(tab_name, sum1_abc, sum1_oth)
    with
    fields_abc as (
        select rdb$relation_name, count(*) cnt
        from rdb$relation_fields
        where rdb$field_name<'rdb$d'
        group by 1
    ),
    fields_other as (
        select rdb$relation_name, count(*) cnt
        from rdb$relation_fields
        where rdb$field_name>='rdb$d'
        group by 1
    )
    ,fields_all as (
        select
            substring(r.rdb$relation_name from 1 for 5) tab_name,
            sum(f1.cnt) sum_abc,
            sum(f2.cnt) sum_other
        from rdb$relations r
        left join fields_abc f1 on f1.rdb$relation_name=r.rdb$relation_name
        left join fields_other f2 on f2.rdb$relation_name=r.rdb$relation_name
        where r.rdb$flags is null
        group by 1
    )
    select tab_name, sum_abc, sum_other from fields_all
    ;
    
    insert into t(tab_name, sum2_abc, sum2_oth)
    with
    fields_abc as (
        select rdb$relation_name, count(*) cnt
        from rdb$relation_fields
        where rdb$field_name<'rdb$d'
        group by 1
    ),
    fields_other as (
        select rdb$relation_name, count(*) cnt____________
        from rdb$relation_fields
        where rdb$field_name>='rdb$d'
        group by 1
    )
    ,fields_all as (
        select substring(r.rdb$relation_name from 1 for 5) tab_name,
        sum(f1.cnt) sum_abc,
        sum(f2.cnt____________) sum_other
        from rdb$relations r
        left join fields_abc f1 on f1.rdb$relation_name=r.rdb$relation_name
        left join fields_other f2 on f2.rdb$relation_name=r.rdb$relation_name
        where r.rdb$flags is null
        group by 1
    )
    select tab_name, sum_abc, sum_other from fields_all
    ;
    commit;
    
    select
        tab_name
        ,min(sum1_abc) as sum1_abc
        ,min(sum2_abc) as sum2_abc
        ,min(sum1_oth) as sum1_oth
        ,min(sum2_oth) as sum2_oth
    from t
    group by tab_name
    having
        min(sum1_abc) is distinct from min(sum2_abc)
        or
        min(sum1_oth) is distinct from min(sum2_oth)
    ;
  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)


@pytest.mark.version('>=2.5.2')
def test_core_3611_1(act_1: Action):
    act_1.execute()

