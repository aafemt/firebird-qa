#coding:utf-8

"""
ID:          issue-8100
ISSUE:       8100
TITLE:       The isc_array_lookup_bounds function returns invalid values for low and high array bounds
DESCRIPTION:
    Test verifies ability to create table with array-type column, store data in it and obtain array by query.
    Script based on example provided in firebird-driver doc:
    https://firebird-driver.readthedocs.io/en/latest/usage-guide.html#firebird-array-type
NOTES:
    [11.05.2024] pzotov
    Confirmed problem on 5.0.0.1391, 6.0.0.344: got "ValueError: Incorrect ARRAY field value"
    Checked on 6.0.0.345 #17b007d, 5.0.1.1394 #aa3cafb - all OK.
"""

import pytest
from pathlib import Path
from firebird.qa import *

db = db_factory()
act = python_act('db', substitutions = [('[ \t]+', ' ')])

@pytest.mark.version('>=5.0.1')
def test_1(act: Action, capsys):

    with act.db.connect() as con:
        cur = con.cursor()
        con.execute_immediate("recreate table array_table (id int generated by default as identity constraint pk_arr primary key, arr int[3,4])")
        con.commit()

        data = (
             [ [87, 13, 16, 19], [25, 52, 73, 24], [81, 92, 63, 14] ]
            ,[ [21, 79, 63, 57], [34, 42, 13, 34], [71, 15, 73, 34] ]
            ,[ [31, 33, 55, 47], [17, 22, 33, 14], [91, 21, 93, 24] ]
        )

        ps = cur.prepare("insert into array_table(arr) values (?)")
        for x in data:
            cur.execute(ps, (x,))
        con.commit()

        cur.execute("select id, arr from array_table order by (arr[1,2]) desc")
        for r in cur:
            print(r[0], r[1])

    act.expected_stdout = """
        2 [[21, 79, 63, 57], [34, 42, 13, 34], [71, 15, 73, 34]]
        3 [[31, 33, 55, 47], [17, 22, 33, 14], [91, 21, 93, 24]]
        1 [[87, 13, 16, 19], [25, 52, 73, 24], [81, 92, 63, 14]]
    """
    act.stdout = capsys.readouterr().out
    assert act.clean_stdout == act.clean_expected_stdout