#coding:utf-8
#
# id:           bugs.core_6058
# title:        Change behavior of skipped and repeated wall times within time zones
# decription:   
#                   Confirmed wrong output on 4.0.0.1421. Works OK on 4.0.0.1524
#               
#                   27.10.2020.
#                   Parser changed after following fixes:
#                       - CORE-6427 - Whitespace as date separator causes conversion error.
#                       - CORE-6429 - Timezone offset in timestamp/time literal and CAST should follow SQL standard syntax only.
#                   See: https://github.com/FirebirdSQL/firebird/commit/ff37d445ce844f991242b1e2c1f96b80a5d1636d
#                   Adjusted expected stdout/stderr after discuss with Adriano.
#                   Checked on 4.0.0.2238
#                
# tracker_id:   CORE-6058
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
    -- Change behavior of skipped and repeated wall times within time zones
    -- Within time zones, some wall times does not exist (DST starting) or repeats twice (DST ending).

    set heading off;

    -- is repeated twice (fall backward), but it must be interpreted as 1:30 AM UTC-04 instead of 1:30 AM UTC-05" 
    select timestamp '2017-11-05 01:30 America/New_York' from rdb$database;
    select timestamp '2017-11-05 01:30 -04' from rdb$database;
    select datediff(
        second from 
        timestamp '2017-11-05 01:30 America/New_York'
        to 
        timestamp '2017-11-05 01:30 -04'
    ) from rdb$database;


    -- does not exist, but it must be interpreted as 2:30 AM UTC-05 (equivalent to 3:30 AM UTC-04)"
    select timestamp '2017-03-12 02:30 America/New_York' from rdb$database;
    select timestamp '2017-03-12 02:30 -05' from rdb$database;
    select datediff(
        second from 
        timestamp '2017-03-12 02:30 America/New_York'
        to 
        timestamp '2017-03-12 02:30 -05'
    ) from rdb$database;
  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    2017-11-05 01:30:00.0000 America/New_York
    2017-03-12 03:30:00.0000 America/New_York
  """
expected_stderr_1 = """
    Statement failed, SQLSTATE = 22009
    Invalid time zone offset: -04 - must use format +/-hours:minutes and be between -14:00 and +14:00
    Statement failed, SQLSTATE = 22009
    Invalid time zone offset: -04 - must use format +/-hours:minutes and be between -14:00 and +14:00
    Statement failed, SQLSTATE = 22009
    Invalid time zone offset: -05 - must use format +/-hours:minutes and be between -14:00 and +14:00
    Statement failed, SQLSTATE = 22009
    Invalid time zone offset: -05 - must use format +/-hours:minutes and be between -14:00 and +14:00
  """

@pytest.mark.version('>=4.0')
def test_core_6058_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.expected_stderr = expected_stderr_1
    act_1.execute()
    assert act_1.clean_expected_stderr == act_1.clean_stderr
    assert act_1.clean_expected_stdout == act_1.clean_stdout

