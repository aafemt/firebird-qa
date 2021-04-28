#coding:utf-8
#
# id:           bugs.core_0166
# title:        cannot specify PLAN in UPDATE statement
# decription:   
# tracker_id:   CORE-0166
# min_versions: ['2.5.0']
# versions:     2.5
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 2.5
# resources: None

substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """
    recreate table company(id int not null primary key, contact_id int, company_name varchar(60));
    recreate table contact(id int not null  primary key using index contact_id, contact_name varchar(60));
    alter table company add constraint company_fk foreign key(contact_id) references contact(id);
    commit;

    insert into contact values(1, '+784956253581, Vovan');
    insert into contact values(2, '+375172223217, Shurik');
    insert into contact values(3, '+380442057337, Vitalik');

    insert into company values(100, 1, 'Pepsico, Inc.');
    insert into company values(101, 1, '');
    insert into company values(102, 2, 'Balaha, Inc.');
    insert into company values(103, 2, '');
    insert into company values(104, 2, null);
    insert into company values(105, 3, null);
    insert into company values(106, 3, 'Firebird Foundation');
    commit;

    set list on;

    select c.*
    from company c order by c.id;

    set plan on;
    set count on;

    update company c set c.company_name = 
    ( select k.contact_name 
      from contact k 
      where k.id = c.contact_id
      PLAN (K INDEX (CONTACT_ID))
    )
    where c.company_name is null or c.company_name = ''
    PLAN (C NATURAL)
    ;

    set plan off;
    set count off;

    select c.*
    from company c order by c.id;
  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    ID                              100
    CONTACT_ID                      1
    COMPANY_NAME                    Pepsico, Inc.

    ID                              101
    CONTACT_ID                      1
    COMPANY_NAME                    

    ID                              102
    CONTACT_ID                      2
    COMPANY_NAME                    Balaha, Inc.

    ID                              103
    CONTACT_ID                      2
    COMPANY_NAME                    

    ID                              104
    CONTACT_ID                      2
    COMPANY_NAME                    <null>

    ID                              105
    CONTACT_ID                      3
    COMPANY_NAME                    <null>

    ID                              106
    CONTACT_ID                      3
    COMPANY_NAME                    Firebird Foundation

    PLAN (K INDEX (CONTACT_ID))
    PLAN (C NATURAL)
    Records affected: 4

    ID                              100
    CONTACT_ID                      1
    COMPANY_NAME                    Pepsico, Inc.

    ID                              101
    CONTACT_ID                      1
    COMPANY_NAME                    +784956253581, Vovan

    ID                              102
    CONTACT_ID                      2
    COMPANY_NAME                    Balaha, Inc.

    ID                              103
    CONTACT_ID                      2
    COMPANY_NAME                    +375172223217, Shurik

    ID                              104
    CONTACT_ID                      2
    COMPANY_NAME                    +375172223217, Shurik

    ID                              105
    CONTACT_ID                      3
    COMPANY_NAME                    +380442057337, Vitalik

    ID                              106
    CONTACT_ID                      3
    COMPANY_NAME                    Firebird Foundation
  """

@pytest.mark.version('>=2.5')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_expected_stdout == act_1.clean_stdout

