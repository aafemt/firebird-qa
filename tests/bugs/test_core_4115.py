#coding:utf-8
#
# id:           bugs.core_4115
# title:        EXECUTE BLOCK execution cause server crash
# decription:   
#                   Confirmed lost of connection (but *not* crash) on 2.5.2.26540.
#                   Last lines in trace:
#                       INSERT INTO PU_BTET(ID,PBIZ_ID,... )VALUES(1711941,1559865, ...);
#                       INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,...
#                       (i.e. it occurs when performing EXECUTE BLOCK)
#                   STDERR contains:
#                       Statement failed, SQLSTATE = 08006
#                       Unable to complete network request to host "localhost".
#                       -Error reading data from the connection.
#                   No such problem on 2.5.7.27050
#               
#               	02-mar-2021. Re-implemented in order to have ability to run this test on Linux.
#               	Ttest creates table and fills it with non-ascii characters in init_script, using charset = UTF8.
#               	Then it generates .sql script for running it in separae ISQL process.
#               	This script makes connection to test DB using charset = WIN1250 and perform needed DML.
#               	Result will be redirected to .log which will be opened via codecs.open(...encoding='cp1250').
#               	Its content will be converted to UTF8 for showing in expected_stdout.
#               	
#               	Checked on:
#               		* Windows: 4.0.0.2377, 3.0.8.33420, 2.5.9.27152	
#               		* Linux:   4.0.0.2377, 3.0.8.33415
#                
# tracker_id:   CORE-4115
# min_versions: ['2.5.7']
# versions:     2.5.7
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 2.5.7
# resources: None

substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(charset='WIN1250', sql_dialect=1, init=init_script_1)

# test_script_1
#---
# 
#  import os
#  import codecs
#  import subprocess
#  import time
#  
#  db_conn.close()
#  
#  #--------------------------------------------
#  
#  def flush_and_close( file_handle ):
#      # https://docs.python.org/2/library/os.html#os.fsync
#      # If you're starting with a Python file object f,
#      # first do f.flush(), and
#      # then do os.fsync(f.fileno()), to ensure that all internal buffers associated with f are written to disk.
#      global os
#  
#      file_handle.flush()
#      if file_handle.mode not in ('r', 'rb') and file_handle.name != os.devnull:
#          # otherwise: "OSError: [Errno 9] Bad file descriptor"!
#          os.fsync(file_handle.fileno())
#      file_handle.close()
#  
#  #--------------------------------------------
#  
#  def cleanup( f_names_list ):
#      global os
#      for i in range(len( f_names_list )):
#         if type(f_names_list[i]) == file:
#            del_name = f_names_list[i].name
#         elif type(f_names_list[i]) == str:
#            del_name = f_names_list[i]
#         else:
#            print('Unrecognized type of element:', f_names_list[i], ' - can not be treated as file.')
#            del_name = None
#  
#         if del_name and os.path.isfile( del_name ):
#             os.remove( del_name )
#  
#  #--------------------------------------------
#  
#  # Code to be executed further in separate ISQL process:
#  #############################
#  sql_txt='''    set bail on;
#      set names WIN1250;
#      connect '%(dsn)s' user '%(user_name)s' password '%(user_password)s';
#  
#      create domain xadoszam as varchar(20);
#      create domain xarf10 as numeric(15, 10);
#      create domain xarf10n as numeric(15, 10) not null;
#      create domain xarfoly as numeric(15, 4);
#      create domain xbinary as blob sub_type 0 segment size 80;
#      create domain xblnev as varchar(15);
#      create domain xcrcn as varchar(30) not null;
#      create domain xcrdn as timestamp not null;
#      create domain xcrsn as varchar(30) not null;
#      create domain xcrun as varchar(30) not null;
#      create domain xdat as timestamp;
#      create domain xdatum as timestamp;
#      create domain xdatumn as timestamp not null;
#      create domain xdnem as varchar(3);
#      create domain xegysn as numeric(15, 4) not null;
#      create domain xert as numeric(15, 2);
#      create domain xert10 as numeric(15, 10);
#      create domain xert4 as numeric(15, 4);
#      create domain xert4n as numeric(15, 4) not null;
#      create domain xert6 as numeric(15, 6);
#      create domain xertdev as numeric(15, 4);
#      create domain xertdevn as numeric(15, 4) not null;
#      create domain xertgy as numeric(15, 2);
#      create domain xertn as numeric(15, 2) not null;
#      create domain xfloat52 as numeric(5, 2);
#      create domain xid as integer;
#      create domain xidn as integer not null;
#      create domain xiktn as integer not null;
#      create domain ximage as blob sub_type 0 segment size 80;
#      create domain xinfo as varchar(1000);
#      create domain xinfo2 as varchar(2000);
#      create domain xint as integer;
#      create domain xintn as integer not null;
#      create domain xkarfoly as numeric(15, 6);
#      create domain xkod as varchar(12);
#      create domain xkodn as varchar(12) not null;
#      create domain xlmc as varchar(30);
#      create domain xlmd as timestamp;
#      create domain xlms as varchar(30);
#      create domain xlmu as varchar(30);
#      create domain xmegj1 as blob sub_type text segment size 80;
#      create domain xmegyseg as varchar(6);
#      create domain xmenny as numeric(15, 3);
#      create domain xmennyn as numeric(15, 3) not null;
#      create domain xmeny as numeric(9, 3);
#      create domain xnyelv as varchar(2);
#      create domain xpfjsz as varchar(34);
#      create domain xpidn as integer not null;
#      create domain xpoz as integer;
#      create domain xreport as blob sub_type text segment size 80;
#      create domain xszamlamaszk as varchar(50);
#      create domain xszazalek as numeric(6, 2);
#      create domain xszazalekn as numeric(6, 2) not null;
#      create domain xszla as varchar(9);
#      create domain xszlan as varchar(9) not null;
#      create domain xszoveg as blob sub_type text segment size 80;
#      create domain xszovegn as blob sub_type text segment size 80 not null;
#      create domain xtblnev as varchar(15);
#      create domain xthnev as varchar(100);
#      create domain xthnevn as varchar(100) not null;
#      create domain xtimestamp as timestamp;
#      create domain xtimestampn as timestamp not null;
#      create domain xtort as numeric(15, 4);
#      create domain xtortn as numeric(15, 4) not null;
#      create domain xtrnevn as varchar(20) not null;
#      create domain xvar1 as varchar(1);
#      create domain xvar10 as varchar(10);
#      create domain xvar100 as varchar(100);
#      create domain xvar1000 as varchar(1000);
#      create domain xvar10000 as varchar(10000);
#      create domain xvar1000n as varchar(1000) not null;
#      create domain xvar100n as varchar(100) not null;
#      create domain xvar10n as varchar(10) not null;
#      create domain xvar11 as varchar(11);
#      create domain xvar12 as varchar(12);
#      create domain xvar12n as varchar(12) not null;
#      create domain xvar13 as varchar(13);
#      create domain xvar13n as varchar(13) not null;
#      create domain xvar14 as varchar(14);
#      create domain xvar140 as varchar(140);
#      create domain xvar14n as varchar(14) not null;
#      create domain xvar16 as varchar(16);
#      create domain xvar1n as varchar(1) not null;
#      create domain xvar2 as varchar(2);
#      create domain xvar20 as varchar(20);
#      create domain xvar200 as varchar(200);
#      create domain xvar200n as varchar(200) not null;
#      create domain xvar20n as varchar(20) not null;
#      create domain xvar24 as varchar(24);
#      create domain xvar25 as varchar(25);
#      create domain xvar25n as varchar(25) not null;
#      create domain xvar2n as varchar(2) not null;
#      create domain xvar3 as varchar(3);
#      create domain xvar30 as varchar(30);
#      create domain xvar300 as varchar(300);
#      create domain xvar300n as varchar(300) not null;
#      create domain xvar30n as varchar(30) not null;
#      create domain xvar32 as varchar(32);
#      create domain xvar32000 as varchar(32000);
#      create domain xvar34 as varchar(34);
#      create domain xvar3n as varchar(3) not null;
#      create domain xvar4 as varchar(4);
#      create domain xvar40 as varchar(40);
#      create domain xvar40n as varchar(40) not null;
#      create domain xvar4n as varchar(4) not null;
#      create domain xvar5 as varchar(5);
#      create domain xvar50 as varchar(50);
#      create domain xvar500 as varchar(500);
#      create domain xvar500n as varchar(500) not null;
#      create domain xvar50n as varchar(50) not null;
#      create domain xvar5n as varchar(5) not null;
#      create domain xvar6 as varchar(6);
#      create domain xvar60n as varchar(60) not null;
#      create domain xvar63 as varchar(63);
#      create domain xvar6n as varchar(6) not null;
#      create domain xvar70 as varchar(70);
#      create domain xvar70n as varchar(70) not null;
#      create domain xvar7n as varchar(7) not null;
#      create domain xvar8 as varchar(8);
#      create domain xvar80 as varchar(80);
#      create domain xvar80n as varchar(80) not null;
#      create domain xvar8n as varchar(8) not null;
#      create domain xvar9 as varchar(9);
#      create domain xvert as varchar(8);
#      commit work;
#  
#      create table pu_btet (id xidn,
#              pbiz_id xidn,
#              gysor xintn,
#              tipus xvar1n,
#              afa_kulcs xvar5,
#              alap xertn,
#              ado xertn,
#              egys_ar xert4,
#              dev_alap xert4,
#              dev_ado xert4,
#              devegys_ar xert4,
#              db xmenny,
#              szoveg xvar50,
#              megjegyzes xmegj1,
#              cru xcrun,
#              crd xcrdn,
#              lmu xlmu,
#              lmd xlmd,
#              termek_id xid,
#              tjegyz_id xid,
#              bto_id xid,
#              mert_id xid,
#              artip_kod xvar14,
#              enged_id xid,
#              gysor_tol xint,
#              gysor_ig xint,
#              afa_ossze xvar1,
#              pbtetkapcs xvar5,
#              kamozgnem_id xid,
#              melleklet_db xint,
#              sarzs xvar12,
#              lejar xdatum,
#              felszab xdatum,
#              pu_afatipus_id xid,
#              afa_alap xert,
#              afa_ado xert,
#              afa_akulcs xvar5,
#              db2 xmenny,
#              mert_id2 xid,
#              mert_seged xvar1,
#              jutalek xert,
#              hull xvar1,
#              kod1 xvar40,
#              kod2 xvar40,
#              kod3 xvar40,
#              kod4 xvar40,
#              kod5 xvar40,
#              eloleg_biz_id xid,
#              lista_ar xert4,
#              egys_ar_diff xert4,
#              pu_ar_id xid,
#              akcio_szazalek xszazalek,
#              akciozott_ar xert4,
#              pu_mn_id xid,
#              afa_szla xszla,
#              afa_eszla xszla,
#              afa_minosit1 xkod,
#              afa_minosit2 xkod,
#              bado xert,
#              balap xert,
#              bdev xvar3,
#              barf xarf10,
#              ef_alap xert,
#              ef_ado xert,
#              ef_egys_ar xert4,
#              ef_dev_alap xert,
#              ef_dev_ado xert,
#              ef_dev_egys_ar xert4,
#              ef_szazalek xert,
#              malap xert,
#              mado xert,
#              mdev xdnem,
#              marfdatum xdatum,
#              idoszakszla_datum xvar50,
#              tovabbszamla_ugyf_id xid,
#              telj xdatum,
#              telj_arfolyam xarf10,
#              szarmhely xvar2,
#              ktrk_kod xvar20,
#              richtextmegj xszoveg,
#              db_keszlet xmenny,
#              mert_id_keszlet xid,
#              auto_arfkul_eloleg_btet_id xid,
#              szallitojegy_szam xvar20);
#      set term ^ ;
#  
#      create trigger insertpu_btet for pu_btet inactive before insert position 0 
#      as begin
#          new.cru = user;
#          new.crd = 'now';
#      end^
#  
#      create trigger updatepu_btet for pu_btet active before update position 0 
#      as begin
#          new.lmu = user;
#          new.lmd = 'now';
#      end^
#      set term ;^
#      commit work;
#  
#      set term ^;
#      execute block as
#      begin
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712188,1560100,1,'N','15',59424,8914,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712187,1560099,1,'N','15',5467,820,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712186,1560098,1,'N','15',12991,1949,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712185,1560097,1,'N','15',30145,4522,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712184,1560096,1,'N','15',6455,968,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712183,1560095,1,'N','15',28020,4203,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712182,1560094,1,'N','15',4630,694,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712181,1560093,1,'N','15',36930,5540,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712180,1560092,1,'N','15',10734,1610,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712179,1560091,1,'N','15',3292,494,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712178,1560090,1,'N','15',27993,4199,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712177,1560089,1,'N','15',3195,479,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712176,1560088,1,'N','15',6520,978,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712175,1560087,1,'N','15',12399,1860,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712174,1560086,1,'N','15',17525,2629,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712173,1560085,1,'N','15',27000,4050,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712172,1560084,1,'N','15',28982,4347,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712171,1560083,1,'N','15',62384,9358,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712170,1560082,1,'N','15',29794,4469,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712169,1560081,1,'N','15',38982,5847,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712168,1560080,1,'N','15',32526,4879,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712167,1560079,1,'N','15',37630,5645,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712166,1560078,1,'N','15',3390,509,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712165,1560077,1,'N','15',75737,11361,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712164,1560076,1,'N','15',24257,3639,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712163,1560075,1,'N','15',44000,6600,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712162,1560074,1,'N','15',65663,9849,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712161,1560073,1,'N','15',33673,5051,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712160,1560072,1,'N','15',14943,2242,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712159,1560071,1,'N','15',4127,619,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712158,1560070,1,'N','15',35404,5311,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712157,1560069,1,'N','15',33337,5000,0,0,0,'2507-2511','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712156,1560068,1,'N','15',65810,9872,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712155,1560067,1,'N','25',84931,21233,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712154,1560066,1,'N','25',35486,8872,0,0,0,'656121,122','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712153,1560065,1,'N','25',46162,11541,0,0,0,'53479','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712152,1560064,1,'N','25',17183,4296,0,0,0,'700301,304','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712151,1560063,1,'N','25',38130,9532,0,0,0,'700117,700296','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712150,1560062,1,'N','25',48936,12234,0,0,0,'428','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712149,1560061,1,'N','25',38138,9534,0,0,0,'54431','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712148,1560060,1,'N','25',39791,9948,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712147,1560059,1,'N','25',92128,23032,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712146,1560058,1,'N','25',19069,4767,0,0,0,'429','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712145,1560057,1,'N','15',41340,6201,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712144,1560056,1,'N','15',76320,11448,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712143,1560055,1,'N','15',41460,6219,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712142,1560054,1,'N','25',20750,5188,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712141,1560053,1,'N','25',4152,1038,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712140,1560052,1,'N','25',240,60,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712139,1560051,1,'N','25',43223,10806,0,0,0,'53435','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712138,1560050,1,'N','25',9818,2455,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712137,1560049,1,'N','25',65693,16423,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712136,1560048,1,'N','25',36700,9175,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712135,1560047,1,'N','15',5534,830,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712134,1560046,1,'N','25',1550,388,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712133,1560045,1,'N','15',9036,1355,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712132,1560044,1,'N','25',12039,3010,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712131,1560043,1,'N','25',20280,5070,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712130,1560042,1,'N','15',124416,18662,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712129,1560041,1,'N','25',8420,2105,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712128,1560040,1,'N','25',78348,19587,0,0,0,'997915.602576','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712127,1560039,1,'N','25',7300,1825,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712126,1560038,1,'N','25',6393,1598,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712125,1560037,1,'N','25',8200,2050,0,0,0,'997916.602575','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712124,1560036,1,'N','25',46660,11665,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712123,1560035,1,'N','25',3228,807,0,0,0,'997917.602574','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712122,1560034,1,'N','15',303913,45587,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712121,1560033,1,'N','25',2032100,508025,0,0,0,'807851','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712120,1560032,1,'N','15',33571,5036,0,0,0,'61124-126','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712119,1560031,1,'N','25',40825,10206,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712118,1560030,1,'N','15',38106,5716,0,0,0,'128-130','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712117,1560029,1,'N','15',21545,3232,0,0,0,'2512','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712116,1560028,1,'N','25',30798,7700,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712115,1560027,2,'N','25',8588,2147,0,0,0,'28758','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712114,1560027,1,'N','15',20753,3113,0,0,0,'28758','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712113,1560026,2,'N','25',42716,10679,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712112,1560026,1,'N','15',31593,4739,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712111,1560025,1,'N','25',58080,14520,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712110,1560024,2,'N','25',11536,2884,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712109,1560024,1,'N','15',65790,9869,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712108,1560023,1,'N','25',42028,10507,0,0,0,'707335.708232','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712107,1560022,1,'N','15',216186,32428,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712106,1560021,1,'N','15',14112,2117,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712105,1560020,1,'N','15',26591,3989,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712104,1560019,1,'N','25',13980,3495,0,0,0,'708234','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712103,1560018,1,'N','25',172058,43015,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712102,1560017,1,'N','25',40842,10211,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712101,1560016,1,'N','25',248637,62159,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712100,1560015,2,'N','25',133760,33440,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712099,1560015,1,'N','15',527385,79108,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712098,1560014,1,'N','25',511560,127890,0,0,0,'3522','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712097,1560013,1,'N','15',7507,1126,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712096,1560012,1,'N','15',22440,3366,0,0,0,'28634','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712095,1560011,1,'N','25',29237,7309,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712094,1560010,1,'N','15',12647,1897,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712093,1560009,1,'N','15',52600,7890,0,0,0,'75098-99','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712092,1560008,1,'N','25',357092,89273,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712091,1560007,1,'N','15',44649,6697,0,0,0,'75094-5.75092','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712090,1560006,1,'N','15',22651,3398,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712089,1560005,1,'N','15',46998,7050,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712088,1560004,2,'N','25',98323,24581,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712087,1560004,1,'N','15',302600,45390,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712086,1560003,1,'N','15',95588,14338,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712085,1560002,1,'N','15',106649,15997,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712084,1560001,1,'N','15',290751,43613,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:13.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712083,1560000,1,'N','15',96480,14472,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712082,1559999,1,'N','15',54363,8155,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712081,1559998,1,'N','15',109602,16440,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712080,1559997,1,'N','25',986468,246617,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712079,1559996,1,'N','15',51440,7716,0,0,0,'15077,079','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712078,1559995,1,'N','15',61132,9170,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712077,1559994,1,'N','15',71938,10791,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712076,1559993,2,'N','25',357860,89465,0,0,0,'11916','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712075,1559993,1,'N','15',194888,29233,0,0,0,'11916','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712074,1559992,1,'N','15',70543,10581,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712073,1559991,1,'N','15',232673,34901,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712072,1559990,1,'N','15',67939,10191,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712071,1559989,1,'N','15',67430,10114,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712070,1559988,1,'N','15',257317,38597,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712069,1559987,1,'N','15',63028,9454,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712068,1559986,1,'N',' 5',52895,2645,0,0,0,'17559-560','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712067,1559985,1,'N','25',186876,46719,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712066,1559984,1,'N','15',49979,7497,0,0,0,'23025.28','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712065,1559983,1,'N','15',940004,141001,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712064,1559982,1,'N','15',36301,5445,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712063,1559981,1,'N','15',59507,8926,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712062,1559980,1,'N','15',107136,16070,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712061,1559979,1,'N','25',357696,89424,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712060,1559978,1,'N','15',15251,2288,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712059,1559977,2,'N','25',137352,34338,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712058,1559977,1,'N','15',29920,4488,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712057,1559976,1,'N','15',57186,8578,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712056,1559975,1,'N','25',176048,44012,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712055,1559974,1,'N','15',18968,2845,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712054,1559973,1,'N','15',53789,8068,0,0,0,'61318-320','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712053,1559972,1,'N','15',22820,3423,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712052,1559971,1,'N','15',35130,5270,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712051,1559970,1,'N','15',55930,8390,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712050,1559969,1,'N','15',338290,50743,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712049,1559968,1,'N','15',13678,2052,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712048,1559967,1,'N','15',159118,23868,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712047,1559966,1,'N','15',32627,4894,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712046,1559965,1,'N','15',12000,1800,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712045,1559964,1,'N','15',42680,6402,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712044,1559963,1,'N','15',22775,3416,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712043,1559962,1,'N','15',53105,7966,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712042,1559961,1,'N','25',32469,8117,0,0,0,'45618,620','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712041,1559960,1,'N','15',130094,19514,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712040,1559959,1,'N','15',14701,2205,0,0,0,'52361','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712039,1559958,1,'N','15',12912,1937,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1712038,1559957,1,'N','NK',10662,0,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712037,1559956,1,'N','15',27643,4146,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712036,1559955,2,'N','NK',14216,0,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712035,1559955,1,'N','25',799,200,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712034,1559954,2,'N','NK',30517,0,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712033,1559954,1,'N','25',400,100,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712032,1559953,2,'N','NK',56586,0,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712031,1559953,1,'N','25',1199,300,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1712030,1559952,1,'N','NK',10662,0,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1712029,1559951,1,'N','NK',24427,0,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1712028,1559950,1,'N','NK',45391,0,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712027,1559949,1,'N','15',81129,12169,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712026,1559948,1,'N','15',79560,11934,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712025,1559947,1,'N','15',14364,2155,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712024,1559946,1,'N','15',11522,1728,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712023,1559945,1,'N','15',28106,4216,0,0,0,'20546,549','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712022,1559944,1,'N','15',622689,93403,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712021,1559943,1,'N','15',58940,8841,0,0,0,'20540-41','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712020,1559942,1,'N','15',34094,5114,0,0,0,'20574-575','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712019,1559941,1,'N','15',31861,4779,0,0,0,'2518-22','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712018,1559940,1,'N','15',23012,3452,0,0,0,'2513-16','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712017,1559939,1,'N','25',40570,10142,0,0,0,'401922-926','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712016,1559938,1,'N','25',33346,8336,0,0,0,'401918-920','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712015,1559937,1,'N','15',91396,13709,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712014,1559936,1,'N','25',10790,2698,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712013,1559935,1,'N','25',108257,27064,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712012,1559934,1,'N','15',2270,341,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712011,1559933,2,'N','25',11076,2769,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712010,1559933,1,'N','15',21260,3189,0,0,0,'NINCS SZÖVEG','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712009,1559932,2,'N','25',7673,1918,0,0,0,'28755,784','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD)VALUES(1712008,1559932,1,'N','15',16161,2424,0,0,0,'28755,784','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000');
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1712007,1559931,1,'N','NK',143734,0,0,0,0,'Bónuszba beszámitva              D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1712006,1559930,1,'N','NK',663448,0,0,0,0,'Bónuszba beszámitva              D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1712005,1559929,1,'N','NK',401818,0,0,0,0,'Bónuszba beszámitva              D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1712004,1559928,1,'N','NK',87800,0,0,0,0,'Bónuszba beszámitva              D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1712003,1559927,1,'N','NK',56250,0,0,0,0,'Bónuszba beszámitva              D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1712002,1559926,1,'N','NK',307720,0,0,0,0,'Bónuszba beszámitva              D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1712001,1559925,1,'N','NK',64338,0,0,0,0,'Bónuszba beszámitva              D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1712000,1559924,1,'N','NK',70564,0,0,0,0,'Bónuszba beszámitva              D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711999,1559923,1,'N','NK',459,0,0,0,0,'Visszáru szla                    D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711998,1559922,1,'N','NK',1080,0,0,0,0,'Visszáru szla                    D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711997,1559921,1,'N','NK',1150,0,0,0,0,'Visszáru szla                    D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711996,1559920,1,'N','NK',2800,0,0,0,0,'Visszáru szla                    D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711995,1559919,1,'N','NK',6480,0,0,0,0,'Visszáru szla                    D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711994,1559918,1,'N','NK',4670,0,0,0,0,'Visszáru szla                    D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711993,1559917,1,'N','NK',800,0,0,0,0,'Visszáru szla                    D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711992,1559916,1,'N','NK',15300,0,0,0,0,'Visszáru szla                    D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711991,1559915,1,'N','NK',523202,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711990,1559914,1,'N','NK',844886,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711989,1559913,1,'N','NK',646060,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711988,1559912,1,'N','NK',2197306,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711987,1559911,1,'N','NK',111715,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711986,1559910,1,'N','NK',6836,0,0,0,0,'                                 D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711985,1559909,1,'N','NK',49479,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711984,1559908,1,'N','NK',337500,0,0,0,0,'Milek                            D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711983,1559907,1,'N','NK',110850,0,0,0,0,'Milek                            D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711982,1559906,1,'N','NK',130800,0,0,0,0,'Ergomat                          D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711981,1559905,1,'N','NK',82992,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711980,1559904,1,'N','NK',128144,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711979,1559903,1,'N','NK',37245,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711978,1559902,1,'N','NK',25374,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711977,1559901,1,'N','NK',132515,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711976,1559900,1,'N','NK',20250,0,0,0,0,'Elektro-top                      D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711975,1559899,1,'N','NK',37098,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711974,1559898,1,'N','NK',95067,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711973,1559897,1,'N','NK',99276,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711972,1559896,1,'N','NK',119538,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711971,1559895,1,'N','NK',124008,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711970,1559894,1,'N','NK',124356,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711969,1559893,1,'N','NK',221511,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711968,1559892,1,'N','NK',58665,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711967,1559891,1,'N','NK',37446,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711966,1559890,1,'N','NK',70422,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711965,1559889,1,'N','NK',157506,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711964,1559888,1,'N','NK',68310,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711963,1559887,1,'N','NK',87085,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711962,1559886,1,'N','NK',6698,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711961,1559885,1,'N','NK',6698,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711960,1559884,1,'N','NK',6698,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711959,1559883,1,'N','NK',6698,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711958,1559882,1,'N','NK',6698,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711957,1559881,1,'N','NK',6698,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711956,1559880,1,'N','NK',6120,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711955,1559879,1,'N','NK',78091,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711954,1559878,1,'N','NK',67735,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711953,1559877,1,'N','NK',67335,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711952,1559876,1,'N','NK',80344,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711951,1559875,1,'N','NK',1000484,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711950,1559874,1,'N','NK',87634,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711949,1559873,1,'N','NK',73417,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711948,1559872,1,'N','NK',110644,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711947,1559871,1,'N','NK',38715,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711946,1559870,1,'N','NK',185,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711945,1559869,1,'N','NK',498140,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711944,1559868,1,'N','NK',354749,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711943,1559867,1,'N','NK',123206,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711942,1559866,1,'N','NK',47458,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711941,1559865,1,'N','NK',52165,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#          INSERT INTO PU_BTET(ID,PBIZ_ID,GYSOR,TIPUS,AFA_KULCS,ALAP,ADO,EGYS_AR,DEVEGYS_AR,DB,SZOVEG,CRU,CRD,LMU,LMD,PU_AFATIPUS_ID)VALUES(1711940,1559864,1,'N','NK',103244,0,0,0,0,'Számla kiegyenlitése             D   193','SYSDBA','2005.10.07 07:38:12.000','SYSDBA','2007.06.15 08:47:42.000',1726469);
#      end
#      ^
#      set term ;^
#      commit;
#  
#      set list on;
#      select count(*) from pu_btet;
#  ''' % dict(globals(), **locals())
#  
#  f_run_sql = open( os.path.join(context['temp_directory'], 'tmp_4115_win1250.sql'), 'w' )
#  
#  # REMOVE INDENTATION IN .SQL to prevent limitation on length of single command (execute block).
#  # Write into .sql file each line without leading and trailing spaces,
#  # with decoding from utf8 to win1250:
#  #####################################
#  for i in sql_txt.split('\\n'):
#      f_run_sql.write( ''.join( (i.strip().decode('utf8').encode('cp1250'), '\\n' ) ) )
#  
#  flush_and_close( f_run_sql )
#  
#  # result: file tmp_3489_win1250.sql is encoded in win1250
#  
#  f_run_log = open( os.path.splitext(f_run_sql.name)[0]+'.log', 'w')
#  subprocess.call( [ context['isql_path'], '-q', '-i', f_run_sql.name ],
#                   stdout = f_run_log,
#                   stderr = subprocess.STDOUT
#                 )
#  flush_and_close( f_run_log ) # result: output will be encoded in win1250
#  
#  with codecs.open(f_run_log.name, 'r', encoding='cp1250' ) as f:
#      result_in_cp1250 = f.readlines()
#  
#  for i in result_in_cp1250:
#      print( i.encode('utf8') )
#  
#  # cleanup:
#  ###########	
#  cleanup( (f_run_sql, f_run_log) )
#  
#    
#---
#act_1 = python_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    COUNT                           249
  """

@pytest.mark.version('>=2.5.7')
@pytest.mark.xfail
def test_core_4115_1(db_1):
    pytest.fail("Test not IMPLEMENTED")


