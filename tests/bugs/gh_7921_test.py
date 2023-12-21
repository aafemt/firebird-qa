#coding:utf-8

"""
ID:          issue-7921
ISSUE:       7921
TITLE:       FB5 uses PK for ordered plan even if less count of fields matching index exists
DESCRIPTION:
NOTES:
    Confirmed problem on 5.0.0.1303.
    Checked on 6.0.0.180 (intermediate build 18.12.2023).
"""

import pytest
from firebird.qa import *

UMOWA_ROWS = 7000
ROZL_MULTIPLIER = 10

init_sql = f"""
    set bail on;

    create table umowa
    (
      umowa_id char(8) not null,
      dyr_id smallint not null,
      umowa_id_seq smallint not null,
      typ_umowy_id char(1) not null,
      rodz_umowy_id char(2) not null,
      constraint
          pk_umowa primary key (umowa_id,dyr_id,umowa_id_seq)
          using index pk_umowa
    );

    create table dok_rozliczeniowy 
    (
      dok_rozliczeniowy_id char(2) not null,
      dok_rozliczeniowy_inkaso char(1) not null,
      constraint
          pk_dok_rozliczeniowy primary key (dok_rozliczeniowy_id)
          using index pk_dok_rozliczeniowy
    );

    create table rozliczenie 
    (
      dyr_id smallint not null,
      insp_id smallint not null,
      okres_numer char(7) not null,
      rozlicz_nr smallint not null,
      rozlicz_nr_poz smallint not null,
      umowa_id char(8) not null,
      umowa_id_seq smallint not null,
      umowa_id_poz smallint not null,
      dok_rozliczeniowy_id char(2) not null,
      rozlicz_rodz_dzial_id char(3),
      rozlicz_kwota_rozliczona decimal(10,2) not null,
      constraint
          pk_rozliczenie primary key (dyr_id,insp_id,okres_numer,rozlicz_nr,rozlicz_nr_poz)
          using index pk_rozliczenie
    );

    create table rodzaj_umowy
    (
      rodz_umowy_id char(2) not null,
      typ_umowy_id char(1) not null,
      constraint
          pk_rodzaj_umowy
          primary key (rodz_umowy_id,typ_umowy_id)
          using index pk_rodzaj_umowy
    );

    create table dyrekcja (
      dyr_id smallint not null primary key using index pk_dyrekcja 
    );


    set term ^ ;
    recreate procedure fill_data
    as
        declare rozlicz_nr integer;
        declare umowa_id integer;
        declare dyr_id integer;
        declare typ_umowy_id integer;
        declare rodz_umowy_id integer;
        declare umowa_id_seq integer;
        declare var_i integer;
        declare okres_numer integer;
    begin
        umowa_id = 1;
        rozlicz_nr = 1;
        dyr_id = 1;
        typ_umowy_id = 1;
        rodz_umowy_id = 1;
        okres_numer = 1;
        while (umowa_id < {UMOWA_ROWS}) do
        begin
            if ( mod(umowa_id, 100) < 95 ) then
                umowa_id_seq = 0;
            else 
                umowa_id_seq = 1;
            
            -- primary key (rodz_umowy_id,typ_umowy_id)
            update or insert into rodzaj_umowy (rodz_umowy_id, typ_umowy_id)
              values (
                  :rodz_umowy_id, 
                  :typ_umowy_id
              );

            -- pk_dok_rozliczeniowy primary key (dok_rozliczeniowy_id)
            update or insert into dok_rozliczeniowy (dok_rozliczeniowy_id, dok_rozliczeniowy_inkaso)
              values (
                  :rodz_umowy_id, 
                  :typ_umowy_id
              );
       
       
            insert into umowa (umowa_id, dyr_id, umowa_id_seq, typ_umowy_id, rodz_umowy_id)
              values (
                  :umowa_id, 
                  :dyr_id, 
                  :umowa_id_seq, 
                  :typ_umowy_id, 
                  :rodz_umowy_id
              );
            
           var_i = 1;  
           while (var_i < {ROZL_MULTIPLIER}) do
           begin
               insert into rozliczenie (dyr_id, insp_id, okres_numer, rozlicz_nr,
                     rozlicz_nr_poz, umowa_id, umowa_id_seq, umowa_id_poz, dok_rozliczeniowy_id,
                     rozlicz_rodz_dzial_id, rozlicz_kwota_rozliczona
               ) values (
                     :dyr_id, :rodz_umowy_id, :okres_numer, :rozlicz_nr, 
                     :var_i,  :umowa_id, :umowa_id_seq, :var_i, :rodz_umowy_id, 
                     :rodz_umowy_id, 1
               );

               rozlicz_nr = rozlicz_nr + 1; 
               if (rozlicz_nr > 3000) then
                 begin
                     rozlicz_nr = 1;
                     okres_numer = okres_numer + 1;
                 end
               var_i = var_i + 1;
           end
            
           umowa_id = umowa_id + 1;
           dyr_id = dyr_id + 1;
           typ_umowy_id = typ_umowy_id + 1;
           rodz_umowy_id = rodz_umowy_id + 1;
           if (dyr_id > 16) then
               dyr_id = 1;
           if (typ_umowy_id > 2) then
               typ_umowy_id = 1;
           if (rodz_umowy_id > 40) then
               rodz_umowy_id = 1;  
        end
    end
    ^
    set term ;^
    commit;

    execute procedure fill_data;

    insert into dyrekcja(dyr_id)
    select distinct dyr_id from rozliczenie;
    commit;

    alter table rozliczenie add constraint fk_rozliczenie__umowa foreign key(umowa_id, dyr_id, umowa_id_seq) references umowa(umowa_id, dyr_id, umowa_id_seq)  on update cascade;
    alter table umowa add constraint fk_umowa__rodzaj_umowy foreign key(rodz_umowy_id, typ_umowy_id) references rodzaj_umowy(rodz_umowy_id, typ_umowy_id)  on update cascade;
    alter table rozliczenie add constraint rozliczenie_fk4 foreign key(dok_rozliczeniowy_id) references dok_rozliczeniowy(dok_rozliczeniowy_id);
    alter table rozliczenie add constraint fk_rozliczenie__dyrekcja  foreign key (dyr_id) references dyrekcja (dyr_id);

    set statistics index pk_umowa;
    set statistics index pk_dok_rozliczeniowy;
    set statistics index pk_rozliczenie;
    set statistics index pk_rodzaj_umowy;
    set statistics index pk_dyrekcja;
    commit;

"""

db = db_factory(init = init_sql)

query_lst = [
    """
        select
            q2_rozl.dyr_id as "dyrekcja"
            ,count(*) as "q2_rozl"
        from
            rozliczenie q2_rozl
        where
            q2_rozl.okres_numer = '15'
            and q2_rozl.dok_rozliczeniowy_id in ('1')
        group by
            q2_rozl.dyr_id
    """,
]

act = python_act('db')

#---------------------------------------------------------
def replace_leading(source, char="."):
    stripped = source.lstrip()
    return char * (len(source) - len(stripped)) + stripped
#---------------------------------------------------------

@pytest.mark.version('>=6.0')
def test_1(act: Action, capsys):
    with act.db.connect() as con:
        cur = con.cursor()
        for q in query_lst:
            with cur.prepare(q) as ps:
                print( '\n'.join([replace_leading(s) for s in ps.detailed_plan .split('\n')]) )

    expected_stdout = """
        Select Expression
        ....-> Aggregate
        ........-> Filter
        ............-> Table "ROZLICZENIE" as "Q2_ROZL" Access By ID
        ................-> Index "FK_ROZLICZENIE__DYREKCJA" Full Scan
        ....................-> Bitmap
        ........................-> Index "ROZLICZENIE_FK4" Range Scan (full match)
    """
    
    act.expected_stdout = expected_stdout
    act.stdout = capsys.readouterr().out
    assert act.clean_stdout == act.clean_expected_stdout
