#coding:utf-8
#
# id:           functional.datatypes.decfloat_binding_to_other_types
# title:        Test ability for DECFLOAT values to be represented as other data types (char, double, bigint).
# decription:   
#                   See CORE-5535 and doc\\sql.extensions\\README.data_types:
#                   ---
#                   SET DECFLOAT BIND <bind-type> - controls how are DECFLOAT values represented in outer
#                   world (i.e. in messages or in XSQLDA). Valid binding types are: NATIVE (use IEEE754
#                   binary representation), CHAR/CHARACTER (use ASCII string), DOUBLE PRECISION (use
#                   8-byte FP representation - same as used for DOUBLE PRECISION fields) or BIGINT
#                   with possible comma-separated SCALE clause (i.e. 'BIGINT, 3').
#                   ---
#                   FB40SS, build 4.0.0.651: OK, 0.921s.
#               
#                   ::: NB ::::
#                   Temply deferred check of "set decfloat bind bigint, 3" when value has at least one digit in floating part.
#                   Also, one need to check case when we try to bind to BIGINT value that is too big for it (say, more than 19 digits).
#                   Waiting for reply from Alex, letters 25.05.2017 21:12 & 21:22.
#               
#               
#                   10.12.2019. Updated syntax for SET BIND command because it was changed in 11-nov-2019. 
#                   Replaced 'bigint,3' with numeric(18,3) - can not specify scale using comma delimiter, i.e. ",3"
#                   Checked on: WI-T4.0.0.1685.
#               
#                   27.12.2019. Updated expected_stdout after discuss with Alex: subtype now must be zero in all cases.
#                   Checked on: WI-T4.0.0.1710.
#               
#                   25.06.2020, 4.0.0.2076: changed types in SQLDA from numeric to int128 // after discuss with Alex about CORE-6342.
#                   01.07.2020, 4.0.0.2084: adjusted expected output ('subtype' values). Added SET BIND from decfloat to INT128.
#                   Removed unnecessary lines from output and added substitution section for result to be properly filtered.
#                
# tracker_id:   
# min_versions: ['4.0.0']
# versions:     4.0
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 4.0
# resources: None

substitutions_1 = [('^((?!sqltype|DECFLOAT_TO_).)*$', ''), ('[ \t]+', ' ')]

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """
    set list on;
    set sqlda_display on;

    -- set decfloat bind char;
    set bind of decfloat to char;
    select 123456789012345678901234567890.1234 as decfloat_to_char
    from rdb$database;

    -- set decfloat bind double precision;
    set bind of decfloat to double precision;
    select 123456789012345678901234567890.1234 as decfloat_to_double
    from rdb$database;

    -- set decfloat bind bigint;
    set bind of decfloat to bigint;
    select 1234567890123456789.1234 as decfloat_to_bigint
    from rdb$database;

    -- set decfloat bind bigint, 0;
    set bind of decfloat to numeric(18,0);
    select 1234567890123456789.1234 as decfloat_to_bigint_0
    from rdb$database;


    -- Alex' samples, letter 25.05.2017 21:56
    -- set decfloat bind bigint, 3;
    set bind of decfloat to numeric(18,3);
    select cast(1234.5678 as decfloat(16)) as decfloat_to_bigint_3
    from rdb$database; -- 1234.568


    -- set decfloat bind bigint, 8;
    set bind of decfloat to numeric(18,8);
    select cast(1234.5678 as decfloat(16)) as decfloat_to_bigint_9
    from rdb$database; -- 1234.56780000

    set bind of decfloat to int128;
    -- -170141183460469231731687303715884105728 ; 170141183460469231731687303715884105727
    select cast( 1701411834604692317316873037158841.05727 as decfloat(34)) as decfloat_to_int128
    from rdb$database;

  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    01: sqltype: 32752 INT128 scale: -4 subtype: 0 len: 16
    :  name: CONSTANT  alias: DECFLOAT_TO_CHAR
    DECFLOAT_TO_CHAR                          123456789012345678901234567890.1234
    01: sqltype: 32752 INT128 scale: -4 subtype: 0 len: 16
    :  name: CONSTANT  alias: DECFLOAT_TO_DOUBLE
    DECFLOAT_TO_DOUBLE                        123456789012345678901234567890.1234
    01: sqltype: 32752 INT128 scale: -4 subtype: 0 len: 16
    :  name: CONSTANT  alias: DECFLOAT_TO_BIGINT
    DECFLOAT_TO_BIGINT                                   1234567890123456789.1234
    01: sqltype: 32752 INT128 scale: -4 subtype: 0 len: 16
    :  name: CONSTANT  alias: DECFLOAT_TO_BIGINT_0
    DECFLOAT_TO_BIGINT_0                                 1234567890123456789.1234
    01: sqltype: 580 INT64 scale: -3 subtype: 1 len: 8
    :  name: CAST  alias: DECFLOAT_TO_BIGINT_3
    DECFLOAT_TO_BIGINT_3            1234.568
    01: sqltype: 580 INT64 scale: -8 subtype: 1 len: 8
    :  name: CAST  alias: DECFLOAT_TO_BIGINT_9
    DECFLOAT_TO_BIGINT_9            1234.56780000
    01: sqltype: 32752 INT128 scale: 0 subtype: 0 len: 16
    :  name: CAST  alias: DECFLOAT_TO_INT128
    DECFLOAT_TO_INT128                         1701411834604692317316873037158841
  """

@pytest.mark.version('>=4.0')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_expected_stdout == act_1.clean_stdout

