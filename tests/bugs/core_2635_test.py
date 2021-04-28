#coding:utf-8
#
# id:           bugs.core_2635
# title:        Unique index with a lot of NULL keys can be corrupted at level 1
# decription:   
# tracker_id:   CORE-2635
# min_versions: ['2.1.4', '2.0.6', '2.5']
# versions:     2.5
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 2.5
# resources: None

substitutions_1 = []

init_script_1 = """set term ^;
recreate table t (id int, sss varchar(255)) ^
create unique descending index t_id_desc on t (id) ^
create unique ascending  index t_id_asc  on t (id) ^
create unique descending index t_id_sss_desc on t (id, sss) ^
create unique ascending  index t_id_sss_asc  on t (id, sss) ^
commit ^

execute block as
declare n int = 0;
begin
  while (n < 10000) do
  begin
    insert into t values (:n, :n);
    n = n + 1;
  end

  n = 0;
  while (n < 10000) do
  begin
    insert into t values (null, null);
    n = n + 1;
  end
end ^
commit ^

execute block as
declare n int = 5000;
begin
  while (n > 0) do
  begin
    n = n - 1;
    update t set id = null, sss = null where id = :n;
  end
end ^
commit ^
"""

db_1 = db_factory(page_size=4096, sql_dialect=3, init=init_script_1)

# test_script_1
#---
# db_conn.close()
#  runProgram('gfix',['-validate','-full','-no_update','-user',user_name,'-password',user_password,dsn])
#---
#act_1 = python_act('db_1', test_script_1, substitutions=substitutions_1)


@pytest.mark.version('>=2.5')
@pytest.mark.xfail
def test_1(db_1):
    pytest.fail("Test not IMPLEMENTED")


