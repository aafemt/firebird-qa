#coding:utf-8

"""
ID:          issue-5450
ISSUE:       5450
TITLE:       Allow implicit conversion between boolean and string
DESCRIPTION:
  Test contains of TWO set of expressions: those which should finish OK and which should FAIL.
  Expressions that should work fine are called directly with checking only their result.
  Expressions that should fail are inserted into table and are called via ES from cursor on that table.
  Inside this cursor we register values of gdscode and sqlstate that raise, and issue via output args
  three columns: statement, gdscode, sqlstate. This output is then checked for matching with expected.
JIRA:        CORE-5167
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
   set list on;

    recreate sequence g;
    recreate table test(
        id int, --  generated by default as identity constraint pk_test primary key using index pk_test,
        expr varchar(128)
    );
    commit;


    -- ###########################################################
    -- ### FOLLOWING STATEMENTS SHOULD FINISH __SUCCESSFULLY__ ###
    -- ###########################################################

    -- check trivial ability to convert string to boolean
    select gen_id(g,1) as expr_no, true > 'false' as result from rdb$database;

    select gen_id(g,1) as expr_no, 'false' ~= true and true != 'false' and false ^= 'true' as result from rdb$database;

    -- following should work as: 1) (true > 'false)==> <true>;  2) true > 'false' ==> <true>
    select gen_id(g,1) as expr_no, true > 'false' > 'false' as result from rdb$database;


    -- 1) 'true' > false ==> TRUE > false ==> <TRUE>; 2) TRUE > 'true' ==> <TRUE> > TRUE ==> <FALSE>
    select gen_id(g,1) as expr_no, 'true' > false > 'true' as result from rdb$database;

    select gen_id(g,1) as expr_no, 'true' in (false, false, null, true) as result from rdb$database; -- <true>
    select gen_id(g,1) as expr_no, 'true' not in (false, null, true) as result from rdb$database; -- <false>

    select gen_id(g,1) as expr_no, 'true' between false and 'true' as result from rdb$database; -- <true>

    -- works as: NOT ('true' between false and 'true'):
    select gen_id(g,1) as expr_no, not 'true' between false and 'true' as result from rdb$database; -- <false>

    select gen_id(g,1) as expr_no, unknown = 'unknown' as result from rdb$database; -- null
    select gen_id(g,1) as expr_no, unknown in ('false', 'true','unknown') as result from rdb$database; -- null
    select gen_id(g,1) as expr_no, unknown = 'false' as result from rdb$database; -- null
    select gen_id(g,1) as expr_no, unknown > 'true' as result from rdb$database;  -- null
    select gen_id(g,1) as expr_no, unknown between 'false' and 'true' as result from rdb$database; -- null
    select gen_id(g,1) as expr_no, unknown = 'false' or 'true' = unknown as result from rdb$database; -- null

    -- check how 'NOT' works (operator precedence)
    -- Also check 'IS', 'IS DISTINCT FROM' and CaSe InsensItivity of strings:
    -- ASF,  06/Apr/16 01:37 PM: is 'true' is invalid.
    -- The operator is:
    --                  IS [NOT] {TRUE | FALSE}
    --
    -- but not like:
    --                  IS [NOT] <value>
    --
    -- not 'false' together with AND/OR, does not allow non boolean argument.

    select gen_id(g,1) as expr_no, not 'false' = true as result from rdb$database; -- works as: not ( 'false' = true ); result: <true>
    select gen_id(g,1) as expr_no, not 'faLSe' is distinct from true as result from rdb$database; -- works as: not ( 'false is ... ); result: <false>

    select gen_id(g,1) as expr_no, not true = 'false' as result from rdb$database;
    select gen_id(g,1) as expr_no, not true is not distinct from 'false' as result from rdb$database;
    select gen_id(g,1) as expr_no, 'false' <> not false as result from rdb$database; -- true

    select gen_id(g,1) as expr_no, 'true' between (not true) and (not false) as result from rdb$database;  --  true
    commit;

    -- #########################################################
    -- ### FOLLOWING STATEMENTS SHOULD FINISH __ABNORMALLY__ ###
    -- #########################################################

    delete from test;

    -- ASF 11/Apr/16 12:59 AM
    -- About BETWEEN, if we allow every crazy construct there, parser conflicts explodes.
    insert into test(id, expr) values(gen_id(g,1), 'select true between not true and not false as result from rdb$database');  -- token unknown ''not''
    insert into test(id, expr) values(gen_id(g,1), 'select true between not false and true as result from rdb$database'); -- token unknown ''not''

    insert into test(id, expr) values(gen_id(g,1), 'select (not ''true'') as result from rdb$database'); -- invalid usage of bool expr
    insert into test(id, expr) values(gen_id(g,1), 'select not ''faLSe'' is true as result from rdb$database'); -- works as: not ( ''false'' is true ) -- invalid usage of bool
    insert into test(id, expr) values(gen_id(g,1), 'select ''true'' is not false as result from rdb$database'); -- invalid usage of bool expr
    insert into test(id, expr) values(gen_id(g,1), 'select ''true'' is distinct from not ''unknown'' as result from rdb$database'); -- invalid usage of bool expr
    insert into test(id, expr) values(gen_id(g,1), 'select ''true'' is distinct from (not false and ''false'') as result from rdb$database'); -- -Invalid usage of boolean expression
    insert into test(id, expr) values(gen_id(g,1), 'select ''true'' is not false as result from rdb$database'); -- invalid usage of bool
    insert into test(id, expr) values(gen_id(g,1), 'select true = not ''false'' as result from rdb$database'); -- invalid usage of bool
    insert into test(id, expr) values(gen_id(g,1), 'select ''false'' is not distinct from not true or ''unknown'' as result from rdb$database'); -- invalid usage of bool
    insert into test(id, expr) values(gen_id(g,1), 'select true = not not ''true'' as result from rdb$database'); -- invalid usage of bool
    insert into test(id, expr) values(gen_id(g,1), 'select ''true'' is unknown as result from rdb$database'); -- invalid usage of bool

    insert into test(id, expr) values(gen_id(g,1), 'select ''true'' is unknown as result from rdb$database'); -- invalid usage of bool
    insert into test(id, expr) values(gen_id(g,1), 'select ''true'' is true as result from rdb$database'); -- invalid usage of bool
    insert into test(id, expr) values(gen_id(g,1), 'select true and ''false'' as result from rdb$database'); -- -Invalid usage of boolean expression
    insert into test(id, expr) values(gen_id(g,1), 'select ''true'' and false as result from rdb$database'); -- -Invalid usage of boolean expression


    -- convers error:
    insert into test(id, expr) values(gen_id(g,1), 'select true = ''unknown'' as result from rdb$database'); -- convers error
    insert into test(id, expr) values(gen_id(g,1), 'select true in (''unknown'', ''false'', ''true'') as result from rdb$database'); -- convers error
    insert into test(id, expr) values(gen_id(g,1), 'select cast(''true'' as blob) > false as result from rdb$database');
    insert into test(id, expr) values(gen_id(g,1), 'select list(b, '''') > false as result from (select ''true'' as b from rdb$database)');
    commit;

    set list on;
    set term ^;
    execute block returns(
        expr_no int,
        run_expr type of column test.expr,
        raised_gds int,
        raised_sql char(6)
    ) as
      declare bool_result boolean;
    begin
        for
            select id, expr
            from test
            order by id
            into expr_no, run_expr
        do begin
            raised_gds=null;
            raised_sql=null;
            begin
                execute statement run_expr into bool_result;
                when any do
                begin
                    raised_gds=gdscode;
                    raised_sql=sqlstate;
                end
            end
            suspend;
        end
    end
    ^
    set term ;^
    commit;

"""

act = isql_act('db', test_script)

expected_stdout = """
    EXPR_NO                         1
    RESULT                          <true>



    EXPR_NO                         2
    RESULT                          <true>



    EXPR_NO                         3
    RESULT                          <true>



    EXPR_NO                         4
    RESULT                          <false>



    EXPR_NO                         5
    RESULT                          <true>



    EXPR_NO                         6
    RESULT                          <false>



    EXPR_NO                         7
    RESULT                          <true>



    EXPR_NO                         8
    RESULT                          <false>



    EXPR_NO                         9
    RESULT                          <null>



    EXPR_NO                         10
    RESULT                          <null>



    EXPR_NO                         11
    RESULT                          <null>



    EXPR_NO                         12
    RESULT                          <null>



    EXPR_NO                         13
    RESULT                          <null>



    EXPR_NO                         14
    RESULT                          <null>



    EXPR_NO                         15
    RESULT                          <true>



    EXPR_NO                         16
    RESULT                          <false>



    EXPR_NO                         17
    RESULT                          <true>



    EXPR_NO                         18
    RESULT                          <true>



    EXPR_NO                         19
    RESULT                          <true>



    EXPR_NO                         20
    RESULT                          <true>



    EXPR_NO                         21
    RUN_EXPR                        select true between not true and not false as result from rdb$database
    RAISED_GDS                      335544569
    RAISED_SQL                      42000

    EXPR_NO                         22
    RUN_EXPR                        select true between not false and true as result from rdb$database
    RAISED_GDS                      335544569
    RAISED_SQL                      42000

    EXPR_NO                         23
    RUN_EXPR                        select (not 'true') as result from rdb$database
    RAISED_GDS                      335544569
    RAISED_SQL                      22000

    EXPR_NO                         24
    RUN_EXPR                        select not 'faLSe' is true as result from rdb$database
    RAISED_GDS                      335544569
    RAISED_SQL                      22000

    EXPR_NO                         25
    RUN_EXPR                        select 'true' is not false as result from rdb$database
    RAISED_GDS                      335544569
    RAISED_SQL                      22000

    EXPR_NO                         26
    RUN_EXPR                        select 'true' is distinct from not 'unknown' as result from rdb$database
    RAISED_GDS                      335544569
    RAISED_SQL                      22000

    EXPR_NO                         27
    RUN_EXPR                        select 'true' is distinct from (not false and 'false') as result from rdb$database
    RAISED_GDS                      335544569
    RAISED_SQL                      22000

    EXPR_NO                         28
    RUN_EXPR                        select 'true' is not false as result from rdb$database
    RAISED_GDS                      335544569
    RAISED_SQL                      22000

    EXPR_NO                         29
    RUN_EXPR                        select true = not 'false' as result from rdb$database
    RAISED_GDS                      335544569
    RAISED_SQL                      22000

    EXPR_NO                         30
    RUN_EXPR                        select 'false' is not distinct from not true or 'unknown' as result from rdb$database
    RAISED_GDS                      335544569
    RAISED_SQL                      22000

    EXPR_NO                         31
    RUN_EXPR                        select true = not not 'true' as result from rdb$database
    RAISED_GDS                      335544569
    RAISED_SQL                      22000

    EXPR_NO                         32
    RUN_EXPR                        select 'true' is unknown as result from rdb$database
    RAISED_GDS                      335544569
    RAISED_SQL                      22000

    EXPR_NO                         33
    RUN_EXPR                        select 'true' is unknown as result from rdb$database
    RAISED_GDS                      335544569
    RAISED_SQL                      22000

    EXPR_NO                         34
    RUN_EXPR                        select 'true' is true as result from rdb$database
    RAISED_GDS                      335544569
    RAISED_SQL                      22000

    EXPR_NO                         35
    RUN_EXPR                        select true and 'false' as result from rdb$database
    RAISED_GDS                      335544569
    RAISED_SQL                      22000

    EXPR_NO                         36
    RUN_EXPR                        select 'true' and false as result from rdb$database
    RAISED_GDS                      335544569
    RAISED_SQL                      22000

    EXPR_NO                         37
    RUN_EXPR                        select true = 'unknown' as result from rdb$database
    RAISED_GDS                      335544334
    RAISED_SQL                      22018

    EXPR_NO                         38
    RUN_EXPR                        select true in ('unknown', 'false', 'true') as result from rdb$database
    RAISED_GDS                      335544334
    RAISED_SQL                      22018

    EXPR_NO                         39
    RUN_EXPR                        select cast('true' as blob) > false as result from rdb$database
    RAISED_GDS                      335544334
    RAISED_SQL                      22018

    EXPR_NO                         40
    RUN_EXPR                        select list(b, '') > false as result from (select 'true' as b from rdb$database)
    RAISED_GDS                      335544334
    RAISED_SQL                      22018
"""

@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout

