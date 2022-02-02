#coding:utf-8

"""
ID:          issue-4888
ISSUE:       4888
TITLE:       Can't select from table with ICU column when database (.FDB) is created on
  LINUX with icu 4.2.1 and then copied to WINDOWS
DESCRIPTION:
    Database for this test was created beforehand on Linux host.
    DDL:
        create collation nums_coll for utf8 from unicode case insensitive 'NUMERIC-SORT=1';
        create domain dm_nums as varchar(20) character set utf8 collate nums_coll;
        recreate table wares(id bigint generated by default as identity, numb dm_nums unique using index wares_numb_unq);

    Table 'wares' then filled-up with some utf8 data and then *raw* .fdb file was copied on Windows host.

        insert into wares(numb) values('lengéscsillapító');
        insert into wares(numb) values('viselő');
        insert into wares(numb) values('bærende');
        insert into wares(numb) values('ρουλεμάν');
        insert into wares(numb) values('αμορτισέρ');
        insert into wares(numb) values('støtdemper');

    Connect to this database without repairing ICU and querying table WARES will produce error:
    ===
      SQL> select * from wares;
      Statement failed, SQLSTATE = 22021
      COLLATION NUMS_COLL for CHARACTER SET UTF8 is not installed
    ===

    This test makes unzip of 'raw' .fdb and run fbsvcmgr with key 'rpr_icu' in order to fix ICU incompatibility.
    Result of fbsvcmgr (STDOUT and STDERR) should be empty.
    Than we run ISQL and query table with UTF8 data - several rows with varchar field which is filled by text
    from Hungarian, Norwegian and Greek languages.

    WARNING! 'Raw' database should be recreated in case of changing ODS structure, otherwise one may get:
    ===
          File "c:\\firebirdqa\\fbtest\\fbtest.py", line 827, in run
            exec substitute_macros(self.test_script) in global_ns, local_ns

          File "", line 29, in

          File "c:\\python27\\lib\\subprocess.py", line 540, in check_call
            raise CalledProcessError(retcode, cmd)
    ===

    Linux ICU info:
    $ rpm -qa | grep icu
    icu4j-eclipse-4.2.1-5.el6.x86_64
    libicu-4.2.1-9.1.el6_2.x86_64

    Database initially was created on LI-V3.0.0.32239, then re-created 20.10.2016 on LI-T4.0.0.419 because ODS was changed.
    Checked on OS = Windows XP: WI-V3.0.1.32570, WI-T4.0.0.321
    20.10.2016: checked on WI-T4.0.0.420
    22.04.2020: checked on WI-T4.0.0.1920 - updated .fdb because of new system tables.
JIRA:        CORE-4571
FBTEST:      bugs.core_4571
"""

import pytest
from firebird.qa import *

db = db_factory()

act = python_act('db')

expected_stdout = """
    ID                              3
    NUMB                            bærende
    ID                              1
    NUMB                            lengéscsillapító
    ID                              6
    NUMB                            støtdemper
    ID                              2
    NUMB                            viselő
    ID                              5
    NUMB                            αμορτισέρ
    ID                              4
    NUMB                            ρουλεμάν
"""

@pytest.mark.skip('FIXME: Not IMPLEMENTED')
@pytest.mark.version('>=3.0')
@pytest.mark.platform('Windows')
def test_1(act: Action):
    pytest.fail("Not IMPLEMENTED")

# test_script_1
#---
# import os
#  import time
#  import zipfile
#  import subprocess
#
#  os.environ["ISC_USER"] = user_name
#  os.environ["ISC_PASSWORD"] = user_password
#
#  # Obtain ODS major version:
#  cur1 = db_conn.cursor()
#  cur1.execute("select mon$ods_major as ods from mon$database")
#  for row in cur1:
#      ods = str(row[0])
#  db_conn.close()
#
#  zf = zipfile.ZipFile( os.path.join(context['files_location'],'core_4571.zip') )
#  tmpfdb = 'core_4571-ods'+ods+'.fdb'
#  zf.extract( tmpfdb, '$(DATABASE_LOCATION)')
#  zf.close()
#
#  tmpfdb='$(DATABASE_LOCATION)'+tmpfdb
#
#  f_svc_rpr=open( os.path.join(context['temp_directory'],'tmp_icu_repair_4571.log'), 'w')
#  subprocess.check_call(["fbsvcmgr","localhost:service_mgr",
#                         "action_repair",
#                         "dbname",tmpfdb,
#                         "rpr_icu"],
#                        stdout=f_svc_rpr,
#                        stderr=subprocess.STDOUT)
#  f_svc_rpr.close()
#
#  sqltxt='''set list on; select id, numb from wares order by numb;'''
#
#  f_sql_log=open( os.path.join(context['temp_directory'],'tmp_isql_4571.log'), 'w')
#  f_sql_log.close()
#  runProgram('isql', ['localhost:'+tmpfdb,'-q', '-o',f_sql_log.name], sqltxt)
#
#  with open( f_svc_rpr.name,'r') as f:
#    print(f.read())
#  f.close()
#
#  with open( f_sql_log.name,'r') as f:
#    print(f.read())
#  f.close()
#
#  # Checked result on Linux:
#  # ID NUMB
#  # == ===================
#  #  3 bærende
#  #  1 lengéscsillapító
#  #  6 støtdemper
#  #  2 viselő
#  #  5 αμορτισέρ
#  #  4 ρουλεμάν
#
#  #####################################################################
#  # Cleanup:
#
#  # do NOT remove this pause otherwise some of logs will not be enable for deletion and test will finish with
#  # Exception raised while executing Python test script. exception: WindowsError: 32
#  time.sleep(1)
#
#  f_list=[f_svc_rpr, f_sql_log]
#  for i in range(len(f_list)):
#      if os.path.isfile(f_list[i].name):
#          os.remove(f_list[i].name)
#  os.remove(tmpfdb)
#
#
#---
