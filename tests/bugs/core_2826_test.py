#coding:utf-8
#
# id:           bugs.core_2826
# title:        Join condition fails for UTF-8 databases.
# decription:   
# tracker_id:   CORE-2826
# min_versions: ['2.1.4']
# versions:     2.1.4
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 2.1.4
# resources: None

substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(page_size=4096, charset='UTF8', sql_dialect=3, init=init_script_1)

test_script_1 = """
    set autoddl off;
    commit;

    create collation unicode_nopad for utf8 from unicode no pad;
    -- !!! >>> COMMENTED THIS ACCORDING TO NOTES IN THE TICKET: >>> commit; <<<
    -- Table is created in the same transaction as collation:
    create table tst1_nopad (
      k1 varchar(3) character set utf8 collate unicode_nopad,
      k2 int,
      k3 char(1)  character set utf8 collate unicode_nopad,
      primary key (k1, k2, k3) using index txt1_nopad_pk
    );
    commit;

    insert into tst1_nopad values ('ap', 123, ' ');
    insert into tst1_nopad values ('hel', 666, 'v');
    commit;
    
    set list on;
    set plan on;
    select t1.*
      from tst1_nopad t1
     where t1.k1 = 'ap'
       and t1.k2 = 123
       and t1.k3 = ' '
    plan (t1 natural);
    
    select t1.*
      from tst1_nopad t1
     where t1.k1 = 'ap'
       and t1.k2 = 123
       and t1.k3 = ' ';
  
     -- 'show table' was removed, see CORE-4782 ("Command `SHOW TABLE` fails..." - reproduced on Windows builds 2.5 and 3.0 only)
  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    PLAN (T1 NATURAL)
    K1                              ap
    K2                              123
    K3                                  

    PLAN (T1 INDEX (TXT1_NOPAD_PK))
    K1                              ap
    K2                              123
    K3                                  
  """

@pytest.mark.version('>=2.1.4')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_expected_stdout == act_1.clean_stdout

