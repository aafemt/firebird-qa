#coding:utf-8

"""
ID:          issue-3221
ISSUE:       3221
TITLE:       Natural is used to select instead of primary key index
DESCRIPTION:
JIRA:        CORE-2835
"""

import pytest
from firebird.qa import *

db_1 = db_factory()

test_script = """
    create table net_net_device(
      id integer not null,
     constraint pk_net_net_device primary key (id)
    );

    create table net_dev_interconnection(
      prim_devid integer not null,
      secondary_devid integer not null,
      interconnect_level integer,
      constraint pk_net_dev_interconnection primary key (prim_devid, secondary_devid)
    );

    alter table net_dev_interconnection add constraint fk_net_dev_interconnection_001
      foreign key (prim_devid) references net_net_device(id);

    alter table net_dev_interconnection add constraint fk_net_dev_interconnection_002
      foreign key (secondary_devid) references net_net_device(id);

    commit;

    set term ^;
    execute block
    as
      declare cnt1 int = 8636;
      declare cnt2 int = 4029;
    begin
      delete from NET_DEV_INTERCONNECTION;
      delete from NET_NET_DEVICE;

      while (cnt1 > 0) do
      begin
          insert into NET_NET_DEVICE values (:cnt1);
          cnt1 = cnt1 - 1;
      end

      while (cnt2 > 0) do
      begin
          insert into NET_DEV_INTERCONNECTION values (1, :cnt2, null);
          cnt2 = cnt2 - 1;
      end

      execute statement 'set statistics index PK_NET_NET_DEVICE';
      execute statement 'set statistics index PK_NET_DEV_INTERCONNECTION';
      execute statement 'set statistics index FK_NET_DEV_INTERCONNECTION_001';
      execute statement 'set statistics index FK_NET_DEV_INTERCONNECTION_002';
    end
    ^
    set term ;^
    commit;

    set planonly;
    select distinct t0_dep.id
    from net_net_device t1_nd,
      net_net_device t0_dep,
      net_dev_interconnection t3_nd_dependantdevices_relation
    where ((t1_nd.id = ? ))
      and t1_nd.id=t3_nd_dependantdevices_relation.prim_devid
      and t0_dep.id=t3_nd_dependantdevices_relation.secondary_devid;
"""

act = isql_act('db_1', test_script)

expected_stdout = """
    PLAN SORT (JOIN (T1_ND INDEX (PK_NET_NET_DEVICE), T3_ND_DEPENDANTDEVICES_RELATION INDEX (FK_NET_DEV_INTERCONNECTION_001), T0_DEP INDEX (PK_NET_NET_DEVICE)))
"""

@pytest.mark.version('>=3')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout

