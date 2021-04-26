#coding:utf-8
#
# id:           bugs.core_5658
# title:        Execute statement with excess parameters
# decription:   
#                   Checked on 4.0.0.1479: OK, 1.608s.
#                
# tracker_id:   CORE-5658
# min_versions: ['4.0']
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
    create or alter procedure sp_test as begin end;
    commit;

    recreate table test(
       id int generated by default as identity constraint pk_test primary key
      ,n int
      ,t timestamp
      ,b boolean
      ,s varchar(1)
    );
    commit;

    insert into test(id, n ,t, b, s) values( 1, 11, '01.01.2019 01:01:01', false, 'q');
    insert into test(id, n ,t, b, s) values( 2, 11, '01.01.2019 01:01:01', true,  'a');
    insert into test(id, n ,t, b, s) values( 3, 22, '02.02.2019 03:03:03', true,  'z');
    insert into test(id, n ,t, b, s) values( 4, 22, '04.04.2019 04:04:04', false, 'q');
    insert into test(id, n ,t, b, s) values( 5, 22, '05.03.2019 05:05:05', null,  'q');
    insert into test(id, n ,t, b, s) values( 6, 33, '03.03.2019 03:03:03', true,  'q');
    insert into test(id, n ,t, b, s) values( 7, 33, '03.03.2019 03:03:03', true,  'q');
    commit;

    set term ^;
    create or alter procedure sp_test(
        a_n int = null
        ,a_t timestamp = null
        ,a_b boolean  = null
        ,a_s varchar(1) = null
        ,a_u varchar(9)  = null
    ) returns(
        id int
        --,sttm varchar(255)
    ) as
        declare sttm varchar(255);
    begin
        sttm = 'select t.id from rdb$database r left join test t on';
        if ( a_n is not null ) then
            sttm = sttm || ' t.n = :param_n and';

        if ( a_t is not null ) then
            sttm = sttm || ' extract(month from t.t) = :param_t and';

        if ( a_b is not null ) then
            sttm = sttm || ' t.b = :param_b and';

        if ( a_s is not null ) then
            sttm = sttm || ' t.s = :param_s and';


        sttm = sttm || ' 1=1'; 
        --suspend;

        for execute statement ( sttm ) ( excess param_n := :a_n, excess param_t := extract(month from :a_t), excess param_b := :a_b, excess param_s := :a_s ) into id
        do
            suspend;
    end
    ^
    set term ;^
    commit;

    -------------------------------------------
    --select * from sp_test;

    set list on;
    select 'case-1' as msg, p.* from sp_test(22) as p;
    select 'case-2' as msg, p.* from sp_test(22, timestamp '19.04.2011 11:12:13') as p;
    select 'case-3' as msg, p.* from sp_test(11, timestamp '11.01.2011 11:12:13', true) as p;
    select 'case-4' as msg, p.* from sp_test(null, timestamp '03.03.2003 03:13:23', null, 'q') as p;
    select 'case-5' as msg, p.* from sp_test(null, null, null, 'z') as p;
  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    MSG                             case-1
    ID                              3
    MSG                             case-1
    ID                              4
    MSG                             case-1
    ID                              5

    MSG                             case-2
    ID                              4

    MSG                             case-3
    ID                              2

    MSG                             case-4
    ID                              5
    MSG                             case-4
    ID                              6
    MSG                             case-4
    ID                              7

    MSG                             case-5
    ID                              3
  """

@pytest.mark.version('>=4.0')
def test_core_5658_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_expected_stdout == act_1.clean_stdout

