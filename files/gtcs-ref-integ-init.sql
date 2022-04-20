set bail on;
create domain dm_emp_id smallint;
create domain dm_dep_id smallint;
create domain dm_name varchar(20);

create table department (
    dept_no dm_dep_id not null,
    dept_name dm_name not null,
    constraint dept_key primary key (dept_no)
);

create table employee (
    emp_no dm_emp_id not null,
    last_name dm_name not null, 
    dept_no dm_dep_id not null constraint ref_key references department(dept_no),
    constraint emp_key primary key (emp_no)
);
commit;
insert into department( dept_no, dept_name) values (1, 'd1');
insert into department( dept_no, dept_name) values (2, 'd2');
insert into department( dept_no, dept_name) values (3, 'd3');
insert into employee( emp_no, last_name, dept_no) values (1, 'e1', 1);
insert into employee( emp_no, last_name, dept_no) values (2, 'e2', 2);
insert into employee( emp_no, last_name, dept_no) values (3, 'e3', 3);
insert into employee( emp_no, last_name, dept_no) values (4, 'e4', 1);
insert into employee( emp_no, last_name, dept_no) values (5, 'e5', 1);
insert into employee( emp_no, last_name, dept_no) values (6, 'e6', 1);
insert into employee( emp_no, last_name, dept_no) values (7, 'e7', 2);
insert into employee( emp_no, last_name, dept_no) values (8, 'e8', 3);
insert into employee( emp_no, last_name, dept_no) values (9, 'e9', 3);
commit;
