#coding:utf-8

"""
ID:          tabloid.join-transformation-03
TITLE:       Check ability of outer join simplification.
DESCRIPTION:
  Null-rejected expr in WHERE clause refers to most right datasource, and this leads to replacement of TWO outer joins.
FBTEST:      functional.tabloid.join_transformation_003
"""

import pytest
from firebird.qa import *

db = db_factory(from_backup='join-transformations.fbk')

test_script = """
    execute procedure sp_fill( 50, 30 );
    --                         ^    ^- probability of assign each field on each row to NULL (percent).
    --                         +- number of rows in each of tables t1...t6

    commit;
    execute procedure sp_recalc_idx_stat;
    commit;

    set list on;
    set term ^;
    execute block returns(result varchar(50)) as
    begin
        select result
        from sp_run(
            ---------------------- Query-1 (not simplified)
            -- NB: we have to make "padding" of null literals up to 6 fields
            -- if query returns less columns:
            'select a.id, b.id, c.id, d.id, null, null
            from (
               t1 a
               left
               join t2 b using(x,y)
            )
            left
            join (
               t3 c
               left
               join t4 d using(x,y)
            ) using(x,y)
            where d.x>0' -- NB: 'd' is alias for t4 which is most right data source.
          ,
            ---------------------- Query-2 (simplified and we assume that it ALWAYS produces the same result as Q1)
            'select a.id, b.id, c.id, d.id, null, null
            from (
               t1 a
               left -- NB: this can NOT be replaced with "inner"!
               join t2 b using(x,y)
            )
            inner -- [1]
            join (
                t3 c
                inner -- [2]
                join t4 d using(x,y)
            ) using(x,y)
            where d.x>0'
          , 0 ------------------------------------ nr_total: when 0 then do NOT run sp_fill because we already do have data for checking
        ) into result;

        suspend;

        if ( result not containing 'Passed' ) then
            -- this context variable serves as 'flag' to show
            -- problematic data (see following EB):
            rdb$set_context('USER_SESSION', 'FAULT', '1');
    end
    ^
    execute block returns( failed_on varchar(255) ) as
    begin
        -- When queries are NOT equal on some data then we have to output
        -- rows from all tables in order to reproduce this trouble later:
        if ( rdb$get_context('USER_SESSION', 'FAULT') = '1' ) then
        begin
          for
              select dml from sp_show_data
              into failed_on
          do
              suspend;
        end
    end
    ^
    set term ^;


"""

act = isql_act('db', test_script)

expected_stdout = """
    RESULT                          Passed.
"""

@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
