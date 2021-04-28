#coding:utf-8
#
# id:           bugs.core_3937
# title:        DeActivate/Activate INDEX or RESTORE not possible with NULL in unique index.
# decription:   
# tracker_id:   CORE-3937
# min_versions: ['2.5.7']
# versions:     2.5.7
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 2.5.7
# resources: None

substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """
    create generator gen_new_table_id;
    recreate table testtable (
        id integer not null,
        field1 integer not null,
        field2 integer not null,
        field3 varchar(10),
        field4 varchar(10)
    );
    alter table testtable add constraint pk_testtable primary key (id);
    create unique index testtable_idx1 on testtable (field1, field2, field3, field4);
    alter index testtable_idx1 inactive;

    set term ^ ;
    create or alter trigger testtable_bi for testtable
    active before insert position 0
    as
    begin
      if (new.id is null) then
        new.id = gen_id(gen_new_table_id,1);
    end
    ^
    set term ;^
    --commit;

    insert into testtable (field1, field2, field3, field4) values (1, 2, null, null);
    insert into testtable (field1, field2, field3, field4) values (1, 2, '', '');
    commit;

    alter index testtable_idx1 inactive;
    alter index testtable_idx1 active; -- NOTE: could NOT reproduce error on WI-V2.5.1.26351
  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)


@pytest.mark.version('>=2.5.7')
def test_1(act_1: Action):
    act_1.execute()

