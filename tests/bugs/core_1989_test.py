#coding:utf-8
#
# id:           bugs.core_1989
# title:        UTF8 UNICODE_CI collate can´t be used in foreing key constraint
# decription:   
# tracker_id:   CORE-1989
# min_versions: []
# versions:     2.5.0
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 2.5.0
# resources: None

substitutions_1 = []

init_script_1 = """-- Domains

CREATE DOMAIN INT64 AS
BIGINT;

CREATE DOMAIN VARCHAR100 AS
VARCHAR(100)
COLLATE UNICODE_CI;

CREATE DOMAIN VARCHAR100_CS AS
VARCHAR(100)
COLLATE UNICODE;

CREATE DOMAIN VARCHAR30 AS
VARCHAR(30)
COLLATE UNICODE_CI;

CREATE DOMAIN VARCHAR30_CS AS
VARCHAR(30)
COLLATE UNICODE;

-- Tables

CREATE TABLE ROLES (
    ROLE_NAME VARCHAR30 NOT NULL,
    APPLICATION_NAME VARCHAR100 NOT NULL
);


CREATE TABLE ROLES_CS (
    ROLE_NAME VARCHAR30_CS NOT NULL,
    APPLICATION_NAME VARCHAR100_CS NOT NULL
);


CREATE TABLE USERS (
    USER_NAME VARCHAR100 NOT NULL,
    APPLICATION_NAME VARCHAR100 NOT NULL
);


CREATE TABLE USERS_CS (
    USER_NAME VARCHAR100_CS NOT NULL,
    APPLICATION_NAME VARCHAR100_CS NOT NULL
);


CREATE TABLE USERS_IN_ROLES (
    USER_NAME VARCHAR100 NOT NULL,
    ROLE_NAME VARCHAR30 NOT NULL,
    APPLICATION_NAME VARCHAR100 NOT NULL
);


CREATE TABLE USERS_IN_ROLES_CS (
    USER_NAME VARCHAR100_CS NOT NULL,
    ROLE_NAME VARCHAR30_CS NOT NULL,
    APPLICATION_NAME VARCHAR100_CS NOT NULL
);

-- Primary Keys

ALTER TABLE ROLES ADD CONSTRAINT PK_ROLES PRIMARY KEY (ROLE_NAME, APPLICATION_NAME);
ALTER TABLE ROLES_CS ADD CONSTRAINT PK_ROLES_CS PRIMARY KEY (ROLE_NAME, APPLICATION_NAME);
ALTER TABLE USERS ADD CONSTRAINT PK_USERS PRIMARY KEY (USER_NAME, APPLICATION_NAME);
ALTER TABLE USERS_CS ADD CONSTRAINT PK_USERS_CS PRIMARY KEY (USER_NAME, APPLICATION_NAME);

-- Foreign Keys

ALTER TABLE USERS_IN_ROLES ADD CONSTRAINT FK_USERS_IN_ROLES_ROLES FOREIGN KEY (ROLE_NAME, APPLICATION_NAME) REFERENCES ROLES (ROLE_NAME, APPLICATION_NAME) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE USERS_IN_ROLES ADD CONSTRAINT FK_USERS_IN_ROLES_USERS FOREIGN KEY (USER_NAME, APPLICATION_NAME) REFERENCES USERS (USER_NAME, APPLICATION_NAME) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE USERS_IN_ROLES_CS ADD CONSTRAINT FK_USERS_IN_ROLES_ROLES_CS FOREIGN KEY (ROLE_NAME, APPLICATION_NAME) REFERENCES ROLES_CS (ROLE_NAME, APPLICATION_NAME) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE USERS_IN_ROLES_CS ADD CONSTRAINT FK_USERS_IN_ROLES_USERS_CS FOREIGN KEY (USER_NAME, APPLICATION_NAME) REFERENCES USERS_CS (USER_NAME, APPLICATION_NAME) ON DELETE CASCADE ON UPDATE CASCADE;


"""

db_1 = db_factory(page_size=16384, charset='UTF8', sql_dialect=3, init=init_script_1)

test_script_1 = """insert into USERS(USER_NAME, APPLICATION_NAME) values('User', 'App');
insert into USERS_CS(USER_NAME, APPLICATION_NAME) values('User', 'App');
insert into ROLES(ROLE_NAME, APPLICATION_NAME) values('Role', 'App');
insert into ROLES_CS(ROLE_NAME, APPLICATION_NAME) values('Role', 'App');
commit;
insert into USERS_IN_ROLES_CS(USER_NAME, ROLE_NAME, APPLICATION_NAME) values('User', 'Role', 'App');
commit;
-- Raises error
insert into USERS_IN_ROLES(USER_NAME, ROLE_NAME, APPLICATION_NAME) values('User', 'Role', 'App');
commit;
"""

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)


@pytest.mark.version('>=2.5.0')
def test_1(act_1: Action):
    act_1.execute()

