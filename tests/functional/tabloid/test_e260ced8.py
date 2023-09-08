#coding:utf-8

"""
ID:          issue-e260ced8
ISSUE:       https://github.com/FirebirdSQL/firebird/commit/5df6668c7bf5a4b27e15f687f8c6cc40e260ced8
TITLE:       Allow computable but non-invariant lists to be used for index lookup
DESCRIPTION:
NOTES:
    [08.09.2023]
    Before improvement explained plan was:
    =======
        Sub-query
            -> Filter
                -> Table "T1" as "B" Access By ID
                    -> Bitmap Or
                        -> Bitmap Or
                            -> Bitmap
                                -> Index "T1_X" Range Scan (full match)
                            -> Bitmap
                                -> Index "T1_X" Range Scan (full match)
                        -> Bitmap
                            -> Index "T1_X" Range Scan (full match)
        Select Expression
            -> Filter
                -> Table "T1" as "A" Full Scan
    =======
    After improvement only one (single) line for index "T1_X" must present in explained plan,
    and access method must be: Index "T1_X" Full Scan.
    Thanks to dimitr for suggestion, see letter 08-sep-2023 09:47.
    
    Test shows explained plan so that leading spaces are replaced in every its line with '#'
    (it is desirable to leading indents).

    Checked on 5.0.0.1190.
"""

import pytest
from firebird.qa import *

init_sql = """
    recreate table t1(
       id int primary key,
       x int
    );
    insert into t1(id, x) select row_number()over(), mod(row_number()over(), 19) from rdb$types;
    commit;
    create index t1_x on t1(x);
"""
db = db_factory(init = init_sql)

act = python_act('db')

def replace_leading(source, char="#"):
    stripped = source.lstrip()
    return char * (len(source) - len(stripped)) + stripped

@pytest.mark.version('>=5.0')
def test_1(act: Action, capsys):

    test_sql = """
        select a.x
        from t1 a
        where exists(
            select *
            from t1 b
            where b.x in (a.x, 2*a.x, 3*a.x)
        )
    """

    act.expected_stdout = """
        Sub-query
        ####-> Filter
        ########-> Table "T1" as "B" Access By ID
        ############-> Bitmap
        ################-> Index "T1_X" Full Scan
        Select Expression
        ####-> Filter
        ########-> Table "T1" as "A" Full Scan
    """
    with act.db.connect() as con:
        cur = con.cursor()
        ps = cur.prepare(test_sql)
        print( '\n'.join([replace_leading(s) for s in ps.detailed_plan .split('\n')]) )

    act.stdout = capsys.readouterr().out
    assert act.clean_stdout == act.clean_expected_stdout
