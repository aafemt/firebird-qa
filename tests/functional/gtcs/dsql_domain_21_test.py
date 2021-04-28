#coding:utf-8
#
# id:           functional.gtcs.dsql_domain_21
# title:        GTCS/tests/DSQL_DOMAIN_21. Verify result of ALTER DOMAIN with changing DEFAULT values and DROP constraints when a table exists with field based on this domain.
# decription:   
#               	Original test see in:
#                       https://github.com/FirebirdSQL/fbtcs/blob/master/GTCS/tests/DSQL_DOMAIN_21.script 
#               
#                   Comment in GTCS:
#                       This script will test using the alter domain statement on domains that are already in use in table definitions,
#                       with domain defaults and check constraints.
#                       Related bugs: have to exit db for changes made to domains to affect data being entered into tables.
#               
#                   We create domains with default values and constraints. Initially we use such default values that PASS requirements of check-constraints.
#                   Statement INSERT DEFAULT and query to the test table is used in order to ensure that we have ability to use such values.
#               
#                   Then we change values in DEFAULT clause so that all of them will VILOLATE check expressions. Here take domains one-by-one and try to user
#                   INSERT DEFAULT after each such change of DEFAULT value. Every such attempt must fail.
#               
#                   Then we drop CHECK constraints in all domains and again try INSERT DEFAULT. It must pass and new default values must be stored in the test table.
#                   Finally, we drop DEFAULT in all domains and try INSERT DEFAULT one more time. It must result to NULL value in all fields.
#               
#                   ::: NB::: Changing default value for BLOB field to one that violates CHECK-expression of domain leads to strange message that does not
#                   relates to actual problem: SQLSTATE = 22018 / conversion error from string "BLOB". See CORE-6297 for details. 
#                   
#                   ::: NOTE :::
#                   Added domains with datatype that did appear only in FB 4.0: DECFLOAT and TIME[STAMP] WITH TIME ZONE. For this reason only FB 4.0+ can be tested.
#               
#                   Checked on 4.0.0.1954.
#               
#                   08.04.2021: changed expected output for date 01-jan-0001 after discuss with Adriano.
#                
# tracker_id:   
# min_versions: ['4.0']
# versions:     4.0
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 4.0
# resources: None

substitutions_1 = [('[ \t]+', ' '), ('F18_BLOB_ID.*', ''), ('F19_BLOB_ID.*', ''), ('F20_BLOB_ID.*', '')]

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """
    set bail on;
	set list on;
	set blob all;

    create or alter view v_test as
    select
        ff.rdb$field_name as dm_name
        ,ff.rdb$field_type as dm_type
        ,ff.rdb$field_sub_type as dm_subtype
        ,ff.rdb$field_length as dm_flen
        ,ff.rdb$field_scale as dm_fscale
        ,ff.rdb$field_precision as dm_fprec
        ,ff.rdb$character_set_id as dm_fcset
        ,ff.rdb$collation_id as dm_fcoll
        ,ff.rdb$character_length dm_fchrlen
        ,ff.rdb$null_flag as dm_fnull
        ,ff.rdb$validation_source as dm_fvalid
        ,ff.rdb$default_source as dm_fdefault
    from rdb$fields ff
    where
        ff.rdb$system_flag is distinct from 1
        and ff.rdb$field_name starting with upper( 'dom21' )
    order by dm_name
	;
    commit;

    create domain dom21_01 as smallint default -32768 check (value not in ( select r.rdb$relation_id from rdb$relations r where r.rdb$system_flag = 1 ) );
	
    create domain dom21_02 as int default 1500
	check (
        value in (
          1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,
          42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,
          80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,
          113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,
          141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,
          169,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,
          197,198,199,200,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,221,222,223,224,
          225,226,227,228,229,230,231,232,233,234,235,236,237,238,239,240,241,242,243,244,245,246,247,248,249,250,251,252,
          253,254,255,256,257,258,259,260,261,262,263,264,265,266,267,268,269,270,271,272,273,274,275,276,277,278,279,280,
          281,282,283,284,285,286,287,288,289,290,291,292,293,294,295,296,297,298,299,300,301,302,303,304,305,306,307,308,
          309,310,311,312,313,314,315,316,317,318,319,320,321,322,323,324,325,326,327,328,329,330,331,332,333,334,335,336,
          337,338,339,340,341,342,343,344,345,346,347,348,349,350,351,352,353,354,355,356,357,358,359,360,361,362,363,364,
          365,366,367,368,369,370,371,372,373,374,375,376,377,378,379,380,381,382,383,384,385,386,387,388,389,390,391,392,
          393,394,395,396,397,398,399,400,401,402,403,404,405,406,407,408,409,410,411,412,413,414,415,416,417,418,419,420,
          421,422,423,424,425,426,427,428,429,430,431,432,433,434,435,436,437,438,439,440,441,442,443,444,445,446,447,448,
          449,450,451,452,453,454,455,456,457,458,459,460,461,462,463,464,465,466,467,468,469,470,471,472,473,474,475,476,
          477,478,479,480,481,482,483,484,485,486,487,488,489,490,491,492,493,494,495,496,497,498,499,500,501,502,503,504,
          505,506,507,508,509,510,511,512,513,514,515,516,517,518,519,520,521,522,523,524,525,526,527,528,529,530,531,532,
          533,534,535,536,537,538,539,540,541,542,543,544,545,546,547,548,549,550,551,552,553,554,555,556,557,558,559,560,
          561,562,563,564,565,566,567,568,569,570,571,572,573,574,575,576,577,578,579,580,581,582,583,584,585,586,587,588,
          589,590,591,592,593,594,595,596,597,598,599,600,601,602,603,604,605,606,607,608,609,610,611,612,613,614,615,616,
          617,618,619,620,621,622,623,624,625,626,627,628,629,630,631,632,633,634,635,636,637,638,639,640,641,642,643,644,
          645,646,647,648,649,650,651,652,653,654,655,656,657,658,659,660,661,662,663,664,665,666,667,668,669,670,671,672,
          673,674,675,676,677,678,679,680,681,682,683,684,685,686,687,688,689,690,691,692,693,694,695,696,697,698,699,700,
          701,702,703,704,705,706,707,708,709,710,711,712,713,714,715,716,717,718,719,720,721,722,723,724,725,726,727,728,
          729,730,731,732,733,734,735,736,737,738,739,740,741,742,743,744,745,746,747,748,749,750,751,752,753,754,755,756,
          757,758,759,760,761,762,763,764,765,766,767,768,769,770,771,772,773,774,775,776,777,778,779,780,781,782,783,784,
          785,786,787,788,789,790,791,792,793,794,795,796,797,798,799,800,801,802,803,804,805,806,807,808,809,810,811,812,
          813,814,815,816,817,818,819,820,821,822,823,824,825,826,827,828,829,830,831,832,833,834,835,836,837,838,839,840,
          841,842,843,844,845,846,847,848,849,850,851,852,853,854,855,856,857,858,859,860,861,862,863,864,865,866,867,868,
          869,870,871,872,873,874,875,876,877,878,879,880,881,882,883,884,885,886,887,888,889,890,891,892,893,894,895,896,
          897,898,899,900,901,902,903,904,905,906,907,908,909,910,911,912,913,914,915,916,917,918,919,920,921,922,923,924,
          925,926,927,928,929,930,931,932,933,934,935,936,937,938,939,940,941,942,943,944,945,946,947,948,949,950,951,952,
          953,954,955,956,957,958,959,960,961,962,963,964,965,966,967,968,969,970,971,972,973,974,975,976,977,978,979,980,
          981,982,983,984,985,986,987,988,989,990,991,992,993,994,995,996,997,998,999,1000,1001,1002,1003,1004,1005,1006,
          1007,1008,1009,1010,1011,1012,1013,1014,1015,1016,1017,1018,1019,1020,1021,1022,1023,1024,1025,1026,1027,1028,
          1029,1030,1031,1032,1033,1034,1035,1036,1037,1038,1039,1040,1041,1042,1043,1044,1045,1046,1047,1048,1049,1050,
          1051,1052,1053,1054,1055,1056,1057,1058,1059,1060,1061,1062,1063,1064,1065,1066,1067,1068,1069,1070,1071,1072,
          1073,1074,1075,1076,1077,1078,1079,1080,1081,1082,1083,1084,1085,1086,1087,1088,1089,1090,1091,1092,1093,1094,
          1095,1096,1097,1098,1099,1100,1101,1102,1103,1104,1105,1106,1107,1108,1109,1110,1111,1112,1113,1114,1115,1116,
          1117,1118,1119,1120,1121,1122,1123,1124,1125,1126,1127,1128,1129,1130,1131,1132,1133,1134,1135,1136,1137,1138,
          1139,1140,1141,1142,1143,1144,1145,1146,1147,1148,1149,1150,1151,1152,1153,1154,1155,1156,1157,1158,1159,1160,
          1161,1162,1163,1164,1165,1166,1167,1168,1169,1170,1171,1172,1173,1174,1175,1176,1177,1178,1179,1180,1181,1182,
          1183,1184,1185,1186,1187,1188,1189,1190,1191,1192,1193,1194,1195,1196,1197,1198,1199,1200,1201,1202,1203,1204,
          1205,1206,1207,1208,1209,1210,1211,1212,1213,1214,1215,1216,1217,1218,1219,1220,1221,1222,1223,1224,1225,1226,
          1227,1228,1229,1230,1231,1232,1233,1234,1235,1236,1237,1238,1239,1240,1241,1242,1243,1244,1245,1246,1247,1248,
          1249,1250,1251,1252,1253,1254,1255,1256,1257,1258,1259,1260,1261,1262,1263,1264,1265,1266,1267,1268,1269,1270,
          1271,1272,1273,1274,1275,1276,1277,1278,1279,1280,1281,1282,1283,1284,1285,1286,1287,1288,1289,1290,1291,1292,
          1293,1294,1295,1296,1297,1298,1299,1300,1301,1302,1303,1304,1305,1306,1307,1308,1309,1310,1311,1312,1313,1314,
          1315,1316,1317,1318,1319,1320,1321,1322,1323,1324,1325,1326,1327,1328,1329,1330,1331,1332,1333,1334,1335,1336,
          1337,1338,1339,1340,1341,1342,1343,1344,1345,1346,1347,1348,1349,1350,1351,1352,1353,1354,1355,1356,1357,1358,
          1359,1360,1361,1362,1363,1364,1365,1366,1367,1368,1369,1370,1371,1372,1373,1374,1375,1376,1377,1378,1379,1380,
          1381,1382,1383,1384,1385,1386,1387,1388,1389,1390,1391,1392,1393,1394,1395,1396,1397,1398,1399,1400,1401,1402,
          1403,1404,1405,1406,1407,1408,1409,1410,1411,1412,1413,1414,1415,1416,1417,1418,1419,1420,1421,1422,1423,1424,
          1425,1426,1427,1428,1429,1430,1431,1432,1433,1434,1435,1436,1437,1438,1439,1440,1441,1442,1443,1444,1445,1446,
          1447,1448,1449,1450,1451,1452,1453,1454,1455,1456,1457,1458,1459,1460,1461,1462,1463,1464,1465,1466,1467,1468,
          1469,1470,1471,1472,1473,1474,1475,1476,1477,1478,1479,1480,1481,1482,1483,1484,1485,1486,1487,1488,1489,1490,
          1491,1492,1493,1494,1495,1496,1497,1498,1499,1500
       )
	)
	;
    create domain dom21_03 as bigint default -9223372036854775807
	check (
        value NOT in (
          1500,1499,1498,1497,1496,1495,1494,1493,1492,1491,1490,1489,1488,1487,1486,1485,1484,1483,1482,1481,1480,1479,
          1478,1477,1476,1475,1474,1473,1472,1471,1470,1469,1468,1467,1466,1465,1464,1463,1462,1461,1460,1459,1458,1457,
          1456,1455,1454,1453,1452,1451,1450,1449,1448,1447,1446,1445,1444,1443,1442,1441,1440,1439,1438,1437,1436,1435,
          1434,1433,1432,1431,1430,1429,1428,1427,1426,1425,1424,1423,1422,1421,1420,1419,1418,1417,1416,1415,1414,1413,
          1412,1411,1410,1409,1408,1407,1406,1405,1404,1403,1402,1401,1400,1399,1398,1397,1396,1395,1394,1393,1392,1391,
          1390,1389,1388,1387,1386,1385,1384,1383,1382,1381,1380,1379,1378,1377,1376,1375,1374,1373,1372,1371,1370,1369,
          1368,1367,1366,1365,1364,1363,1362,1361,1360,1359,1358,1357,1356,1355,1354,1353,1352,1351,1350,1349,1348,1347,
          1346,1345,1344,1343,1342,1341,1340,1339,1338,1337,1336,1335,1334,1333,1332,1331,1330,1329,1328,1327,1326,1325,
          1324,1323,1322,1321,1320,1319,1318,1317,1316,1315,1314,1313,1312,1311,1310,1309,1308,1307,1306,1305,1304,1303,
          1302,1301,1300,1299,1298,1297,1296,1295,1294,1293,1292,1291,1290,1289,1288,1287,1286,1285,1284,1283,1282,1281,
          1280,1279,1278,1277,1276,1275,1274,1273,1272,1271,1270,1269,1268,1267,1266,1265,1264,1263,1262,1261,1260,1259,
          1258,1257,1256,1255,1254,1253,1252,1251,1250,1249,1248,1247,1246,1245,1244,1243,1242,1241,1240,1239,1238,1237,
          1236,1235,1234,1233,1232,1231,1230,1229,1228,1227,1226,1225,1224,1223,1222,1221,1220,1219,1218,1217,1216,1215,
          1214,1213,1212,1211,1210,1209,1208,1207,1206,1205,1204,1203,1202,1201,1200,1199,1198,1197,1196,1195,1194,1193,
          1192,1191,1190,1189,1188,1187,1186,1185,1184,1183,1182,1181,1180,1179,1178,1177,1176,1175,1174,1173,1172,1171,
          1170,1169,1168,1167,1166,1165,1164,1163,1162,1161,1160,1159,1158,1157,1156,1155,1154,1153,1152,1151,1150,1149,
          1148,1147,1146,1145,1144,1143,1142,1141,1140,1139,1138,1137,1136,1135,1134,1133,1132,1131,1130,1129,1128,1127,
          1126,1125,1124,1123,1122,1121,1120,1119,1118,1117,1116,1115,1114,1113,1112,1111,1110,1109,1108,1107,1106,1105,
          1104,1103,1102,1101,1100,1099,1098,1097,1096,1095,1094,1093,1092,1091,1090,1089,1088,1087,1086,1085,1084,1083,
          1082,1081,1080,1079,1078,1077,1076,1075,1074,1073,1072,1071,1070,1069,1068,1067,1066,1065,1064,1063,1062,1061,
          1060,1059,1058,1057,1056,1055,1054,1053,1052,1051,1050,1049,1048,1047,1046,1045,1044,1043,1042,1041,1040,1039,
          1038,1037,1036,1035,1034,1033,1032,1031,1030,1029,1028,1027,1026,1025,1024,1023,1022,1021,1020,1019,1018,1017,
          1016,1015,1014,1013,1012,1011,1010,1009,1008,1007,1006,1005,1004,1003,1002,1001,1000,999,998,997,996,995,994,
          993,992,991,990,989,988,987,986,985,984,983,982,981,980,979,978,977,976,975,974,973,972,971,970,969,968,967,
          966,965,964,963,962,961,960,959,958,957,956,955,954,953,952,951,950,949,948,947,946,945,944,943,942,941,940,
          939,938,937,936,935,934,933,932,931,930,929,928,927,926,925,924,923,922,921,920,919,918,917,916,915,914,913,
          912,911,910,909,908,907,906,905,904,903,902,901,900,899,898,897,896,895,894,893,892,891,890,889,888,887,886,
          885,884,883,882,881,880,879,878,877,876,875,874,873,872,871,870,869,868,867,866,865,864,863,862,861,860,859,
          858,857,856,855,854,853,852,851,850,849,848,847,846,845,844,843,842,841,840,839,838,837,836,835,834,833,832,
          831,830,829,828,827,826,825,824,823,822,821,820,819,818,817,816,815,814,813,812,811,810,809,808,807,806,805,
          804,803,802,801,800,799,798,797,796,795,794,793,792,791,790,789,788,787,786,785,784,783,782,781,780,779,778,
          777,776,775,774,773,772,771,770,769,768,767,766,765,764,763,762,761,760,759,758,757,756,755,754,753,752,751,
          750,749,748,747,746,745,744,743,742,741,740,739,738,737,736,735,734,733,732,731,730,729,728,727,726,725,724,
          723,722,721,720,719,718,717,716,715,714,713,712,711,710,709,708,707,706,705,704,703,702,701,700,699,698,697,
          696,695,694,693,692,691,690,689,688,687,686,685,684,683,682,681,680,679,678,677,676,675,674,673,672,671,670,
          669,668,667,666,665,664,663,662,661,660,659,658,657,656,655,654,653,652,651,650,649,648,647,646,645,644,643,
          642,641,640,639,638,637,636,635,634,633,632,631,630,629,628,627,626,625,624,623,622,621,620,619,618,617,616,
          615,614,613,612,611,610,609,608,607,606,605,604,603,602,601,600,599,598,597,596,595,594,593,592,591,590,589,
          588,587,586,585,584,583,582,581,580,579,578,577,576,575,574,573,572,571,570,569,568,567,566,565,564,563,562,
          561,560,559,558,557,556,555,554,553,552,551,550,549,548,547,546,545,544,543,542,541,540,539,538,537,536,535,
          534,533,532,531,530,529,528,527,526,525,524,523,522,521,520,519,518,517,516,515,514,513,512,511,510,509,508,
          507,506,505,504,503,502,501,500,499,498,497,496,495,494,493,492,491,490,489,488,487,486,485,484,483,482,481,
          480,479,478,477,476,475,474,473,472,471,470,469,468,467,466,465,464,463,462,461,460,459,458,457,456,455,454,
          453,452,451,450,449,448,447,446,445,444,443,442,441,440,439,438,437,436,435,434,433,432,431,430,429,428,427,
          426,425,424,423,422,421,420,419,418,417,416,415,414,413,412,411,410,409,408,407,406,405,404,403,402,401,400,
          399,398,397,396,395,394,393,392,391,390,389,388,387,386,385,384,383,382,381,380,379,378,377,376,375,374,373,
          372,371,370,369,368,367,366,365,364,363,362,361,360,359,358,357,356,355,354,353,352,351,350,349,348,347,346,
          345,344,343,342,341,340,339,338,337,336,335,334,333,332,331,330,329,328,327,326,325,324,323,322,321,320,319,
          318,317,316,315,314,313,312,311,310,309,308,307,306,305,304,303,302,301,300,299,298,297,296,295,294,293,292,
          291,290,289,288,287,286,285,284,283,282,281,280,279,278,277,276,275,274,273,272,271,270,269,268,267,266,265,
          264,263,262,261,260,259,258,257,256,255,254,253,252,251,250,249,248,247,246,245,244,243,242,241,240,239,238,
          237,236,235,234,233,232,231,230,229,228,227,226,225,224,223,222,221,220,219,218,217,216,215,214,213,212,211,
          210,209,208,207,206,205,204,203,202,201,200,199,198,197,196,195,194,193,192,191,190,189,188,187,186,185,184,
          183,182,181,180,179,178,177,176,175,174,173,172,171,170,169,168,167,166,165,164,163,162,161,160,159,158,157,
          156,155,154,153,152,151,150,149,148,147,146,145,144,143,142,141,140,139,138,137,136,135,134,133,132,131,130,
          129,128,127,126,125,124,123,122,121,120,119,118,117,116,115,114,113,112,111,110,109,108,107,106,105,104,103,
          102,101,100,99,98,97,96,95,94,93,92,91,90,89,88,87,86,85,84,83,82,81,80,79,78,77,76,75,74,73,72,71,70,69,68,
          67,66,65,64,63,62,61,60,59,58,57,56,55,54,53,52,51,50,49,48,47,46,45,44,43,42,41,40,39,38,37,36,35,34,33,32,
          31,30,29,28,27,26,25,24,23,22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1
       )
    )	
	;
	
    create domain dom21_04 as date default '01.01.1980' check ( value >='01.01.0001' and value <= '30.12.9999');
	
    create domain dom21_05 as time default '23:59:59.999' check ( extract(hour from value) >=21 );
	
    create domain dom21_06 as time with time zone default '11:11:11.111 Indian/Cocos' check ( extract(hour from value) <=12 );
    create domain dom21_07 as timestamp default '01.01.0001 00:00:01.001' check ( extract(minute from value) = 0 );
    create domain dom21_08 as timestamp with time zone default '21.12.2013 11:11:11.111 Indian/Cocos'  check ( extract(minute from value) <=30 );
    create domain dom21_09 as char(1) character set utf8 default '€' check( value in ('€', '¢') );
    create domain dom21_10 as varchar(1) character set utf8 default '¢' check( value in ('€', '¢') );
    -- https://en.wikipedia.org/wiki/ISO/IEC_8859-1,
	-- see table "Languages with incomplete coverage",
	-- column "Typical workaround" for Hungarian 'Ő':
	create domain dom21_11 as nchar(1) default 'Ö' check( value in ('Ö', 'Ø') );
    create domain dom21_12 as binary(2) default 'Œ' check( value in ('Œ', 'Ÿ', '¿') ); -- this datatype is alias for char(N) character set octets
    create domain dom21_13 as varbinary(2) default 'Œ' check( value in ('Œ', 'Ÿ', '¿') );
	
    create domain dom21_14 as numeric(2,2) default -327.68 check ( value < 0 );
	create domain dom21_15 as decimal(20,2) default -999999999999999999 check( value < 0 );
	
	-- Online evaluation of expressions: https://www.wolframalpha.com

	-- https://en.wikipedia.org/wiki/Single-precision_floating-point_format
	-- (largest number less than one):  1 - power(2,-24)
	create domain dom21_16 as float default 0.999999940395355224609375 check( abs(value) < 1 );
	
	-- https://en.wikipedia.org/wiki/Double-precision_floating-point_format
	-- Max Double: power(2,1023) * ( 1+(1-power(2,-52) )
	create domain dom21_17 as double precision default 1.7976931348623157e308 check( abs(value) > 1 );
    
	create domain dom21_18 as blob default 'Ø' check( value in ('Ö', 'Ø') );
    create domain dom21_19 as blob sub_type text default 'W' check (value > '');
    create domain dom21_20 as blob sub_type binary default 'f' check (value similar to '([0-9]|[a-f]){1,}');
	

    create domain dom21_21 as boolean default false check ( value is not true );
    create domain dom21_22 as decfloat(16) default -9.999999999999999E+384 check( log10(abs(value)) >= 384 );
    create domain dom21_23 as decfloat default -9.999999999999999999999999999999999E6144 check( log10(abs(value)) >= 6144 );
    commit;	
	
	--select * from v_test;

    recreate table test(
         f01 dom21_01
        ,f02 dom21_02
        ,f03 dom21_03
        ,f04 dom21_04
        ,f05 dom21_05
        ,f06 dom21_06
        ,f07 dom21_07
        ,f08 dom21_08
        ,f09 dom21_09
        ,f10 dom21_10
        ,f11 dom21_11
        ,f12 dom21_12
        ,f13 dom21_13
        ,f14 dom21_14
        ,f15 dom21_15
		,f16 dom21_16
        ,f17 dom21_17
        ,f18_blob_id dom21_18
        ,f19_blob_id dom21_19
        ,f20_blob_id dom21_20
        ,f21 dom21_21
        ,f22 dom21_22
        ,f23 dom21_23
	);
	commit;
    
	set bail off; -- ### NB ###
	
	insert into test default values; -- this must PASS
	select 'point-1' as msg, t.* from test t;
	rollback;
	
	----------------------------------
	-- Now we change DEFAULT values of domains so that they become violate CHECK expressions:
	alter domain dom21_01 set default 1;
	insert into test default values; -- this must FAIL with SQLSTATE = 23000 / validation error for column "TEST"."F01", value "1"
	alter domain dom21_01 drop constraint; -- in order to have ability to test next domain and field
	
	alter domain dom21_02 set default -1;
	insert into test default values; -- validation error for column "TEST"."F02", value "-1"
	alter domain dom21_02 drop constraint;

	alter domain dom21_03 set default 1;
	insert into test default values; -- validation error for column "TEST"."F03", value "1"
	alter domain dom21_03 drop constraint;
	
	alter domain dom21_04 set default '31.12.9999';
	insert into test default values; -- validation error for column "TEST"."F04", value "9999-12-31"
	alter domain dom21_04 drop constraint;

	alter domain dom21_05 set default '20:59:59.999';
	insert into test default values; -- validation error for column "TEST"."F05", value "20:59:59.9990"
	alter domain dom21_05 drop constraint;

	alter domain dom21_06 set default '13:00:00 Indian/Cocos';
	insert into test default values; -- validation error for column "TEST"."F06", value "13:00:00.0000 Indian/Cocos"
	alter domain dom21_06 drop constraint;
	
	alter domain dom21_07 set default '01.01.0001 01:01:01.001';
	insert into test default values; -- validation error for column "TEST"."F07", value "01-JAN-1 1:01:01.0010" // changed 08.04.2021, was: '1-jan'
	alter domain dom21_07 drop constraint;

	alter domain dom21_08 set default '21.12.2013 10:31:00 Indian/Cocos';
	insert into test default values; -- validation error for column "TEST"."F08", value "21-DEC-2013 10:31:00.0000 Indian/Cocos"
	alter domain dom21_08 drop constraint;

	alter domain dom21_09 set default 'Ő';
	insert into test default values; -- validation error for column "TEST"."F09", value "Ő"
	alter domain dom21_09 drop constraint;

	alter domain dom21_10 set default '';
	insert into test default values; -- validation error for column "TEST"."F10", value ""
	alter domain dom21_10 drop constraint;

	alter domain dom21_11 set default '';
	insert into test default values; -- validation error for column "TEST"."F11", value " " // nchar(1)
	alter domain dom21_11 drop constraint;

	alter domain dom21_12 set default 'Ø';
	insert into test default values; -- validation error for column "TEST"."F12", value "Ø"
	alter domain dom21_12 drop constraint;

	alter domain dom21_13 set default '¢';
	insert into test default values; -- validation error for column "TEST"."F13", value "¢"
	alter domain dom21_13 drop constraint;

	alter domain dom21_14 set default 327.67;
	insert into test default values; -- validation error for column "TEST"."F14", value "327.67"
	alter domain dom21_14 drop constraint;

	alter domain dom21_15 set default 0;
	insert into test default values; -- validation error for column "TEST"."F15", value "0.00"
	alter domain dom21_15 drop constraint;

	alter domain dom21_16 set default 1;
	insert into test default values; -- validation error for column "TEST"."F16", value "1.0000000"
	alter domain dom21_16 drop constraint;

	alter domain dom21_17 set default 1.0000000000000001;
	insert into test default values; -- validation error for column "TEST"."F17", value "1.000000000000000"
	alter domain dom21_17 drop constraint;

	alter domain dom21_18 set default 'x';
	insert into test default values; -- ### CORE-6297 ### STRANGE MESSAGE HERE: Statement failed, SQLSTATE = 22018 / conversion error from string "BLOB"
	alter domain dom21_18 drop constraint;

	alter domain dom21_19 set default '';
	insert into test default values; -- ### CORE-6297 ### STRANGE MESSAGE HERE: Statement failed, SQLSTATE = 22018 / conversion error from string "BLOB"
	alter domain dom21_19 drop constraint;

	alter domain dom21_20 set default 'g';
	insert into test default values; -- ### CORE-6297 ### STRANGE MESSAGE HERE: Statement failed, SQLSTATE = 22018 / conversion error from string "BLOB"
	alter domain dom21_20 drop constraint;

	alter domain dom21_21 set default true;
	insert into test default values; -- validation error for column "TEST"."F21", value "TRUE"
	alter domain dom21_21 drop constraint;

	alter domain dom21_22 set default -9.999999999999999E+382;
	insert into test default values; -- validation error for column "TEST"."F22", value "-9.999999999999999E+382"
	alter domain dom21_22 drop constraint;

	alter domain dom21_23 set default -9.999999999999999999999999999999999E6142;
	insert into test default values; -- validation error for column "TEST"."F23", value "-9.999999999999999999999999999999999E+6142"
	alter domain dom21_23 drop constraint;

    ---------------------------------------
	-- Now we have NO constraints in any domain. 
	-- We can run again INSERT DEFAULT and verify that new values appear in the table
	insert into test default values; -- this must PASS
	select 'point-2' as msg, t.* from test t; -- all values must have now NEW defaults for domains
	rollback;
	
	alter domain dom21_01 drop default;
	alter domain dom21_02 drop default;
	alter domain dom21_03 drop default;
	alter domain dom21_04 drop default;
	alter domain dom21_05 drop default;
	alter domain dom21_06 drop default;
	alter domain dom21_07 drop default;
	alter domain dom21_08 drop default;
	alter domain dom21_09 drop default;
	alter domain dom21_10 drop default;
	alter domain dom21_11 drop default;
	alter domain dom21_12 drop default;
	alter domain dom21_13 drop default;
	alter domain dom21_14 drop default;
	alter domain dom21_15 drop default;
	alter domain dom21_16 drop default;
	alter domain dom21_17 drop default;
	alter domain dom21_18 drop default;
	alter domain dom21_19 drop default;
	alter domain dom21_20 drop default;
	alter domain dom21_21 drop default;
	alter domain dom21_22 drop default;
	alter domain dom21_23 drop default;

	insert into test default values; -- this must PASS
	select 'point-3' as msg, t.* from test t; -- all values now must be NULL
	rollback;
  
  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
	MSG                             point-1                     
	F01                             -32768
	F02                             1500
	F03                             -9223372036854775807
	F04                             1980-01-01
	F05                             23:59:59.9990
	F06                             11:11:11.1110 Indian/Cocos
	F07                             0001-01-01 00:00:01.0010
	F08                             2013-12-21 11:11:11.1110 Indian/Cocos
	F09                             € 
	F10                             ¢
	F11                             Ö  
	F12                             C592
	F13                             C592
	F14                             -327.68
	F15                                                    -999999999999999999.00
	F16                             0.99999994
	F17                             1.797693134862316e+308
	F18_BLOB_ID                     81:0
	Ø
	F19_BLOB_ID                     81:1
	W
	F20_BLOB_ID                     81:2
	f
	F21                             <false>
	F22                             -9.999999999999999E+384
	F23                             -9.999999999999999999999999999999999E+6144



	MSG                             point-2                     
	F01                             1
	F02                             -1
	F03                             1
	F04                             9999-12-31
	F05                             20:59:59.9990
	F06                             13:00:00.0000 Indian/Cocos
	F07                             0001-01-01 01:01:01.0010
	F08                             2013-12-21 10:31:00.0000 Indian/Cocos
	F09                             Ő  
	F10                             
	F11                                 
	F12                             C398
	F13                             C2A2
	F14                             327.67
	F15                                                                      0.00
	F16                             1
	F17                             1.000000000000000
	F18_BLOB_ID                     81:45
	x
	F19_BLOB_ID                     81:46

	F20_BLOB_ID                     81:47
	g
	F21                             <true>
	F22                             -9.999999999999999E+382
	F23                             -9.999999999999999999999999999999999E+6142



	MSG                             point-3                     
	F01                             <null>
	F02                             <null>
	F03                             <null>
	F04                             <null>
	F05                             <null>
	F06                             <null>
	F07                             <null>
	F08                             <null>
	F09                             <null>
	F10                             <null>
	F11                             <null>
	F12                             <null>
	F13                             <null>
	F14                             <null>
	F15                             <null>
	F16                             <null>
	F17                             <null>
	F18_BLOB_ID                     <null>
	F19_BLOB_ID                     <null>
	F20_BLOB_ID                     <null>
	F21                             <null>
	F22                             <null>
	F23                             <null>
  """
expected_stderr_1 = """
	Statement failed, SQLSTATE = 23000
	validation error for column "TEST"."F01", value "1"

	Statement failed, SQLSTATE = 23000
	validation error for column "TEST"."F02", value "-1"

	Statement failed, SQLSTATE = 23000
	validation error for column "TEST"."F03", value "1"

	Statement failed, SQLSTATE = 23000
	validation error for column "TEST"."F04", value "9999-12-31"

	Statement failed, SQLSTATE = 23000
	validation error for column "TEST"."F05", value "20:59:59.9990"

	Statement failed, SQLSTATE = 23000
	validation error for column "TEST"."F06", value "13:00:00.0000 Indian/Cocos"

	Statement failed, SQLSTATE = 23000
	validation error for column "TEST"."F07", value "01-JAN-0001 1:01:01.0010"

	Statement failed, SQLSTATE = 23000
	validation error for column "TEST"."F08", value "21-DEC-2013 10:31:00.0000 Indian/Cocos"

	Statement failed, SQLSTATE = 23000
	validation error for column "TEST"."F09", value "Ő"

	Statement failed, SQLSTATE = 23000
	validation error for column "TEST"."F10", value ""

	Statement failed, SQLSTATE = 23000
	validation error for column "TEST"."F11", value " "

	Statement failed, SQLSTATE = 23000
	validation error for column "TEST"."F12", value "Ø"

	Statement failed, SQLSTATE = 23000
	validation error for column "TEST"."F13", value "¢"

	Statement failed, SQLSTATE = 23000
	validation error for column "TEST"."F14", value "327.67"

	Statement failed, SQLSTATE = 23000
	validation error for column "TEST"."F15", value "0.00"

	Statement failed, SQLSTATE = 23000
	validation error for column "TEST"."F16", value "1.0000000"

	Statement failed, SQLSTATE = 23000
	validation error for column "TEST"."F17", value "1.000000000000000"

	Statement failed, SQLSTATE = 22018
	conversion error from string "BLOB"

	Statement failed, SQLSTATE = 22018
	conversion error from string "BLOB"

	Statement failed, SQLSTATE = 22018
	conversion error from string "BLOB"

	Statement failed, SQLSTATE = 23000
	validation error for column "TEST"."F21", value "TRUE"

	Statement failed, SQLSTATE = 23000
	validation error for column "TEST"."F22", value "-9.999999999999999E+382"

	Statement failed, SQLSTATE = 23000
	validation error for column "TEST"."F23", value "-9.999999999999999999999999999999999E+6142"
  """

@pytest.mark.version('>=4.0')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.expected_stderr = expected_stderr_1
    act_1.execute()
    assert act_1.clean_expected_stderr == act_1.clean_stderr
    assert act_1.clean_expected_stdout == act_1.clean_stdout

