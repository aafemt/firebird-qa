#coding:utf-8
#
# id:           functional.datatypes.decfloat_columns_handlng
# title:        Check ability of misc. actions against table column for DECFLOAT datatype.
# decription:   
#                   See CORE-5535 and doc\\sql.extensions\\README.data_types
#                   FB40CS, build 4.0.0.651: OK, 2.203ss.
#                
# tracker_id:   
# min_versions: ['4.0.0']
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
    set list on;

    recreate table test(id int, x decfloat(16));
    commit;

    set term ^;
    execute block as
    begin
      begin
          execute statement 'drop domain dm_df16';
          when any do begin end
      end
      begin
          execute statement 'drop domain dm_df34';
          when any do begin end
      end
    end
    ^
    set term ;^
    commit;

    create domain dm_df16 as decfloat(16) default -9.999999999999999E384;
    create domain dm_df34 as decfloat(34) default -9.999999999999999999999999999999999E6144;
    commit;

    -- check ability to alter column of a table when initially datatype was numeric or double precision:
    recreate table test(
        id bigint default 9223372036854775807
       ,n numeric(18,2)
       ,x double precision
    );

    recreate table test2(
        id bigint
       ,n dm_df16
       ,x dm_df34
    );


    recreate table test3(
        id dm_df16
       ,n dm_df34
       ,x dm_df16
    );

    commit;


    alter table test
        alter column n type dm_df34,
        alter column x type dm_df16;
    commit;


    -- Should FAIL with:
    -- - Conversion from base type DECFLOAT(34) to DECFLOAT(16) is not supported.
    alter table test alter n type decfloat(16);

    commit;


    -- Check that one may insert default values:
    insert into test default values returning id, n, x;
    commit;

    set count on;
    --set echo on;

    --insert into test2 select * from test;
    --show table test;
    --show table test3;

    insert into test2 select * from test; -- should FAIL

    insert into test3 
    select 
        cast(id as decfloat(16))*id*id*id*id*id*id*id*id*id*id*id*id*id*id*id*id*id*id*id, 
        -n, 
        -x 
    from test; -- should PASS

    set count off;
    select * from test3;
  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    ID                              9223372036854775807
    N                               -9.999999999999999999999999999999999E+6144
    X                               -9.999999999999999E+384

    Records affected: 0
    Records affected: 1

    ID                               1.985155524189834E+379
    N                                9.999999999999999999999999999999999E+6144
    X                                9.999999999999999E+384

 """
expected_stderr_1 = """
    Statement failed, SQLSTATE = 42000
    unsuccessful metadata update
    -ALTER TABLE TEST failed
    -Cannot change datatype for N.  Conversion from base type DECFLOAT(34) to DECFLOAT(16) is not supported.

    Statement failed, SQLSTATE = 22003
    Decimal float overflow.  The exponent of a result is greater than the magnitude allowed.
 """

@pytest.mark.version('>=4.0')
def test_decfloat_columns_handlng_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.expected_stderr = expected_stderr_1
    act_1.execute()
    assert act_1.clean_expected_stderr == act_1.clean_stderr
    assert act_1.clean_expected_stdout == act_1.clean_stdout

