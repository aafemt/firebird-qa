#coding:utf-8
#
# id:           bugs.core_1291
# title:        Can't transliterate character set when look at procedure text in database just created from script (and thus in ODS 11.1)
# decription:   
# tracker_id:   CORE-1291
# min_versions: []
# versions:     2.1
# qmid:         bugs.core_1291

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 2.1
# resources: None

substitutions_1 = [('Use CONNECT or CREATE DATABASE to specify a database', ''), ('SQL> ', ''), ('CON> ', '')]

init_script_1 = """"""

db_1 = db_factory(init=init_script_1)

# test_script_1
#---
# import os
#  
#  script = """SET SQL DIALECT 3;
#  
#  SET NAMES WIN1251;
#  
#  CREATE DATABASE '%s'
#  DEFAULT CHARACTER SET WIN1251;
#  """ % dsn
#  
#  scriptfile = open(os.path.join(context['files_location'],'core_1291.sql'),'r')
#  script = script + ''.join(scriptfile)
#  scriptfile.close()
#  
#  runProgram('isql',['-user',user_name,'-pas',user_password],script)
#---
#act_1 = python_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """Procedure text:
=============================================================================
DECLARE VARIABLE NDSDiv DOUBLE PRECISION;
DECLARE VARIABLE ID_ExportFieldDoc Integer;
begin
  SELECT Val FROM TBL_Const_Float
  WHERE Name='NDSDiv'
  INTO :NDSDiv;
  FOR SELECT id_exportfielddoc, accountcredit, accountdebit FROM tbl_exportentry
      WHERE id_exportgroupentry=:id_group
      INTO :id_exportfielddoc, :accountcredit, :accountdebit
      DO BEGIN
         IF ((AccountCredit<>0) or (AccountDebit<>0)) THEN BEGIN
           IF (id_exportfielddoc=110) THEN BEGIN
             SELECT SUM(A.PriceRub*B.Volume/A.PointMul), SUM(A.PriceDoc*B.Volume/A.PointMul)  FROM TBL_INDOC_TEMP A,
                                                                                                                                              TBL_OUTDOC_TEMP B,
                                                                                                                                              TBL_ITEMSALE C,
                                                                                                                                              TBL_INDOC D
             WHERE b.id_outdoc=:id_outdoc and b.id_itemsale=c.id_itemsale and c.id_firstindoc_temp=a.id_indoc_temp and
                               d.id_indoc=a.id_indoc and d.doctype = 6
             INTO :summrus, :summdoc;
           END
           IF (id_exportfielddoc=111) THEN BEGIN
             SELECT SUM(A.PriceCalcRub*B.Volume/A.PointMul), SUM(A.PriceCalcDoc*B.Volume/A.PointMul) FROM TBL_INDOC_TEMP A,
                                                                                                                                              TBL_OUTDOC_TEMP B,
                                                                                                                                              TBL_ITEMSALE C,
                                                                                                                                              TBL_INDOC D
             WHERE b.id_outdoc=:id_outdoc and b.id_itemsale=c.id_itemsale and c.id_firstindoc_temp=a.id_indoc_temp and
                               d.id_indoc=a.id_indoc and d.doctype = 6
             INTO :summrus, :summdoc;
           END
           IF (id_exportfielddoc=112) THEN BEGIN
             SELECT SUM(A.SummDoc), SUM(A.SummDoc) FROM TBL_OUTDOC_TEMP A,
                                                                                                                            TBL_ITEMSALE B,
                                                                                                                            TBL_INDOC_TEMP C,
                                                                                                                            TBL_INDOC D
             WHERE A.ID_OUTDOC=:id_outdoc and b.id_itemsale=a.id_itemsale and c.id_indoc_temp=b.id_firstindoc_temp and
                               d.id_indoc=c.id_indoc and d.doctype = 6
             INTO :summrus, :summdoc;
           END
           IF (id_exportfielddoc=113) THEN BEGIN
             SELECT SUM(A.NDS*A.PriceRub*B.Volume/(A.PointMul*100)), SUM(A.NDS*A.PriceDoc*B.Volume/(A.PointMul*100))  FROM TBL_INDOC_TEMP A,
                                                                                                                                              TBL_OUTDOC_TEMP B,
                                                                                                                                              TBL_ITEMSALE C,
                                                                                                                                              TBL_INDOC D
             WHERE b.id_outdoc=:id_outdoc and b.id_itemsale=c.id_itemsale and c.id_firstindoc_temp=a.id_indoc_temp and
                               d.id_indoc=a.id_indoc and d.doctype = 6
             INTO :summrus, :summdoc;
           END
           IF (id_exportfielddoc=114) THEN BEGIN
             SELECT SUM(A.NDS*A.PriceCalcRub*B.Volume/(A.PointMul*100)), SUM(A.NDS*A.PriceCalcDoc*B.Volume/(A.PointMul*100))  FROM TBL_INDOC_TEMP A,
                                                                                                                                              TBL_OUTDOC_TEMP B,
                                                                                                                                              TBL_ITEMSALE C,
                                                                                                                                              TBL_INDOC D
             WHERE b.id_outdoc=:id_outdoc and b.id_itemsale=c.id_itemsale and c.id_firstindoc_temp=a.id_indoc_temp and
                               d.id_indoc=a.id_indoc and d.doctype = 6
             INTO :summrus, :summdoc;
           END
            IF (id_exportfielddoc=115) THEN BEGIN
             SELECT SUM(A.SummNDSDoc), SUM(A.SummNDSDoc) FROM TBL_OUTDOC_TEMP A,
                                                                                                                            TBL_ITEMSALE B,
                                                                                                                            TBL_INDOC_TEMP C,
                                                                                                                            TBL_INDOC D
             WHERE A.ID_OUTDOC=:id_outdoc and b.id_itemsale=a.id_itemsale and c.id_indoc_temp=b.id_firstindoc_temp and
                               d.id_indoc=c.id_indoc and d.doctype = 6
             INTO :summrus, :summdoc;
           END
           IF (id_exportfielddoc=116) THEN BEGIN
             SELECT SUM((A.PriceRub*B.Volume/A.PointMul)*(1+A.NDS/100)), SUM((A.PriceDoc*B.Volume/A.PointMul)*(1+A.NDS/100))  FROM TBL_INDOC_TEMP A,
                                                                                                                                              TBL_OUTDOC_TEMP B,
                                                                                                                                              TBL_ITEMSALE C,
                                                                                                                                              TBL_INDOC D
             WHERE b.id_outdoc=:id_outdoc and b.id_itemsale=c.id_itemsale and c.id_firstindoc_temp=a.id_indoc_temp and
                               d.id_indoc=a.id_indoc and d.doctype = 6
             INTO :summrus, :summdoc;
           END
           IF (id_exportfielddoc=117) THEN BEGIN
             SELECT SUM((A.PriceCalcRub*B.Volume/A.PointMul)*(1+A.NDS/100)), SUM((A.PriceCalcDoc*B.Volume/A.PointMul)*(1+A.NDS/100)) FROM TBL_INDOC_TEMP A,
                                                                                                                                              TBL_OUTDOC_TEMP B,
                                                                                                                                              TBL_ITEMSALE C,
                                                                                                                                              TBL_INDOC D
             WHERE b.id_outdoc=:id_outdoc and b.id_itemsale=c.id_itemsale and c.id_firstindoc_temp=a.id_indoc_temp and
                               d.id_indoc=a.id_indoc and d.doctype = 6
             INTO :summrus, :summdoc;
           END
           IF (id_exportfielddoc=118) THEN BEGIN
             SELECT SUM(A.SummWithNDSDoc), SUM(A.SummWithNDSDoc) FROM TBL_OUTDOC_TEMP A,
                                                                                                                            TBL_ITEMSALE B,
                                                                                                                            TBL_INDOC_TEMP C,
                                                                                                                            TBL_INDOC D
             WHERE A.ID_OUTDOC=:id_outdoc and b.id_itemsale=a.id_itemsale and c.id_indoc_temp=b.id_firstindoc_temp and
                               d.id_indoc=c.id_indoc and d.doctype = 6
             INTO :summrus, :summdoc;
           END
           IF (id_exportfielddoc=119) THEN BEGIN
             SELECT SUM((A.PriceCalcRub-A.PriceRub)*B.Volume/A.PointMul), SUM((A.PriceCalcDoc-A.PriceDoc)*B.Volume/A.PointMul)  FROM TBL_INDOC_TEMP A,
                                                                                                                                              TBL_OUTDOC_TEMP B,
                                                                                                                                              TBL_ITEMSALE C,
                                                                                                                                              TBL_INDOC D
             WHERE b.id_outdoc=:id_outdoc and b.id_itemsale=c.id_itemsale and c.id_firstindoc_temp=a.id_indoc_temp and
                               d.id_indoc=a.id_indoc and d.doctype = 6
             INTO :summrus, :summdoc;
           END
           IF (id_exportfielddoc=120) THEN BEGIN
             SELECT SUM(B.SummDoc-(A.PriceRub*B.Volume/A.PointMul)), SUM(B.SummDoc-(A.PriceDoc*B.Volume/A.PointMul))  FROM TBL_INDOC_TEMP A,
                                                                                                                                              TBL_OUTDOC_TEMP B,
                                                                                                                                              TBL_ITEMSALE C,
                                                                                                                                              TBL_INDOC D
             WHERE b.id_outdoc=:id_outdoc and b.id_itemsale=c.id_itemsale and c.id_firstindoc_temp=a.id_indoc_temp and
                               d.id_indoc=a.id_indoc and d.doctype = 6
             INTO :summrus, :summdoc;
           END
           IF (id_exportfielddoc=121) THEN BEGIN
             SELECT SUM(A.NDS*(A.PriceCalcRub-A.PriceRub)*B.Volume/(A.PointMul*100)), SUM(A.NDS*(A.PriceCalcDoc-A.PriceDoc)*B.Volume/(A.PointMul*100))  FROM TBL_INDOC_TEMP A,
                                                                                                                                              TBL_OUTDOC_TEMP B,
                                                                                                                                              TBL_ITEMSALE C,
                                                                                                                                              TBL_INDOC D
             WHERE b.id_outdoc=:id_outdoc and b.id_itemsale=c.id_itemsale and c.id_firstindoc_temp=a.id_indoc_temp and
                               d.id_indoc=a.id_indoc and d.doctype = 6
             INTO :summrus, :summdoc;
           END
           IF (id_exportfielddoc=122) THEN BEGIN
             SELECT SUM(B.SummNDSDoc-A.NDS*A.PriceRub*B.Volume/(A.PointMul*100)), SUM(B.SummNDSDoc-A.NDS*A.PriceDoc*B.Volume/(A.PointMul*100))  FROM TBL_INDOC_TEMP A,
                                                                                                                                              TBL_OUTDOC_TEMP B,
                                                                                                                                              TBL_ITEMSALE C,
                                                                                                                                              TBL_INDOC D
             WHERE b.id_outdoc=:id_outdoc and b.id_itemsale=c.id_itemsale and c.id_firstindoc_temp=a.id_indoc_temp and
                               d.id_indoc=a.id_indoc and d.doctype = 6
             INTO :summrus, :summdoc;
           END
           IF (id_exportfielddoc=123) THEN BEGIN
             SELECT SUM(((A.PriceCalcRub-A.PriceRub)*B.Volume/A.PointMul)*(1+A.NDS/100)), SUM(((A.PriceCalcDoc-A.PriceDoc)*B.Volume/A.PointMul)*(1+A.NDS/100)) FROM TBL_INDOC_TEMP A,
                                                                                                                                              TBL_OUTDOC_TEMP B,
                                                                                                                                              TBL_ITEMSALE C,
                                                                                                                                              TBL_INDOC D
             WHERE b.id_outdoc=:id_outdoc and b.id_itemsale=c.id_itemsale and c.id_firstindoc_temp=a.id_indoc_temp and
                               d.id_indoc=a.id_indoc and d.doctype = 6
             INTO :summrus, :summdoc;
           END
           IF (id_exportfielddoc=124) THEN BEGIN
             SELECT SUM(B.SummWithNDSDoc-(A.PriceRub*B.Volume/A.PointMul)*(1+A.NDS/100)), SUM(B.SummWithNDSDoc-(A.PriceDoc*B.Volume/A.PointMul)*(1+A.NDS/100)) FROM TBL_INDOC_TEMP A,
                                                                                                                                              TBL_OUTDOC_TEMP B,
                                                                                                                                              TBL_ITEMSALE C,
                                                                                                                                              TBL_INDOC D
             WHERE b.id_outdoc=:id_outdoc and b.id_itemsale=c.id_itemsale and c.id_firstindoc_temp=a.id_indoc_temp and
                               d.id_indoc=a.id_indoc and d.doctype = 6
             INTO :summrus, :summdoc;
           END

           IF (id_exportfielddoc=125) THEN BEGIN
             SELECT SUM(A.PriceRub*B.Volume/A.PointMul), SUM(A.PriceDoc*B.Volume/A.PointMul)  FROM TBL_INDOC_TEMP A,
                                                                                                                                              TBL_OUTDOC_TEMP B,
                                                                                                                                              TBL_ITEMSALE C,
                                                                                                                                              TBL_INDOC D
             WHERE b.id_outdoc=:id_outdoc and b.id_itemsale=c.id_itemsale and c.id_firstindoc_temp=a.id_indoc_temp and
                               d.id_indoc=a.id_indoc and d.doctype = 6 and b.nds=0
             INTO :summrus, :summdoc;
           END
           IF (id_exportfielddoc=126) THEN BEGIN
             SELECT SUM(A.PriceCalcRub*B.Volume/A.PointMul), SUM(A.PriceCalcDoc*B.Volume/A.PointMul) FROM TBL_INDOC_TEMP A,
                                                                                                                                              TBL_OUTDOC_TEMP B,
                                                                                                                                              TBL_ITEMSALE C,
                                                                                                                                              TBL_INDOC D
             WHERE b.id_outdoc=:id_outdoc and b.id_itemsale=c.id_itemsale and c.id_firstindoc_temp=a.id_indoc_temp and
                               d.id_indoc=a.id_indoc and d.doctype = 6 and b.nds=0
             INTO :summrus, :summdoc;
           END
           IF (id_exportfielddoc=127) THEN BEGIN
             SELECT SUM(A.SummDoc), SUM(A.SummDoc) FROM TBL_OUTDOC_TEMP A,
                                                                                                                            TBL_ITEMSALE B,
                                                                                                                            TBL_INDOC_TEMP C,
                                                                                                                            TBL_INDOC D
             WHERE A.ID_OUTDOC=:id_outdoc and b.id_itemsale=a.id_itemsale and c.id_indoc_temp=b.id_firstindoc_temp and
                               d.id_indoc=c.id_indoc and d.doctype = 6 and a.nds=0
             INTO :summrus, :summdoc;
           END
           IF (id_exportfielddoc=128) THEN BEGIN
             SELECT SUM((A.PriceCalcRub-A.PriceRub)*B.Volume/A.PointMul), SUM((A.PriceCalcDoc-A.PriceDoc)*B.Volume/A.PointMul)  FROM TBL_INDOC_TEMP A,
                                                                                                                                              TBL_OUTDOC_TEMP B,
                                                                                                                                              TBL_ITEMSALE C,
                                                                                                                                              TBL_INDOC D
             WHERE b.id_outdoc=:id_outdoc and b.id_itemsale=c.id_itemsale and c.id_firstindoc_temp=a.id_indoc_temp and
                               d.id_indoc=a.id_indoc and d.doctype = 6 and b.nds=0
             INTO :summrus, :summdoc;
           END
           IF (id_exportfielddoc=129) THEN BEGIN
             SELECT SUM(B.SummDoc-(A.PriceRub*B.Volume/A.PointMul)), SUM(B.SummDoc-(A.PriceDoc*B.Volume/A.PointMul))  FROM TBL_INDOC_TEMP A,
                                                                                                                                              TBL_OUTDOC_TEMP B,
                                                                                                                                              TBL_ITEMSALE C,
                                                                                                                                              TBL_INDOC D
             WHERE b.id_outdoc=:id_outdoc and b.id_itemsale=c.id_itemsale and c.id_firstindoc_temp=a.id_indoc_temp and
                               d.id_indoc=a.id_indoc and d.doctype = 6 and b.nds=0
             INTO :summrus, :summdoc;
           END
           IF ((id_exportfielddoc>129)and(id_exportfielddoc<145)) THEN BEGIN
                execute procedure  prc_expsumm_8_10 ( id_exportfielddoc, id_outdoc, NDSDiv ) returning_values( summrus, summdoc );
           END
           IF ((id_exportfielddoc>144)and(id_exportfielddoc<160)) THEN BEGIN
                execute procedure  prc_expsumm_8_20 ( id_exportfielddoc, id_outdoc, NDSDiv ) returning_values( summrus, summdoc );
           END
           IF ((SummRus>0) or (SummDoc>0)) THEN SUSPEND;
         END
      END
END
=============================================================================
Parameters:
ID_INDOC                          INPUT INTEGER
ID_OUTDOC                         INPUT INTEGER
ID_GROUP                          INPUT INTEGER
ACCOUNTCREDIT                     OUTPUT INTEGER
ACCOUNTDEBIT                      OUTPUT INTEGER
SUMMRUS                           OUTPUT DOUBLE PRECISION
SUMMDOC                           OUTPUT DOUBLE PRECISION
"""

@pytest.mark.version('>=2.1')
@pytest.mark.xfail
def test_core_1291_1(db_1):
    pytest.fail("Test not IMPLEMENTED")


