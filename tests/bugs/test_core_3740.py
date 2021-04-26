#coding:utf-8
#
# id:           bugs.core_3740
# title:        SELECT using IN list with 153 or more elements causes crash
# decription:   
# tracker_id:   CORE-3740
# min_versions: ['2.5.0']
# versions:     2.5
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 2.5
# resources: None

substitutions_1 = []

init_script_1 = """
    -- Note-1. Firebird 2.5.0 and 2.5.1 -- also WORK fine on the following script
    -- (despite ticket's issue "affected version(s) 2.5.1"), so these versions also can be tested here.
    -- Note-2. As of march-2015 (build 3.0.0.31756), there is some kind of regression in performance 
    -- of parsing huge literal lists in comparison with all 2.5.x versions, see CORE-4728.
  """

db_1 = db_factory(page_size=4096, sql_dialect=3, init=init_script_1)

test_script_1 = """
    set list on;
    select 1 x from
    rdb$database where 1500 in(
    2147483647
    ,2147483646
    ,2147483645
    ,2147483644
    ,2147483643
    ,2147483642
    ,2147483641
    ,2147483640
    ,2147483639
    ,2147483638
    ,2147483637
    ,2147483636
    ,2147483635
    ,2147483634
    ,2147483633
    ,2147483632
    ,2147483631
    ,2147483630
    ,2147483629
    ,2147483628
    ,2147483627
    ,2147483626
    ,2147483625
    ,2147483624
    ,2147483623
    ,2147483622
    ,2147483621
    ,2147483620
    ,2147483619
    ,2147483618
    ,2147483617
    ,2147483616
    ,2147483615
    ,2147483614
    ,2147483613
    ,2147483612
    ,2147483611
    ,2147483610
    ,2147483609
    ,2147483608
    ,2147483607
    ,2147483606
    ,2147483605
    ,2147483604
    ,2147483603
    ,2147483602
    ,2147483601
    ,2147483600
    ,2147483599
    ,2147483598
    ,2147483597
    ,2147483596
    ,2147483595
    ,2147483594
    ,2147483593
    ,2147483592
    ,2147483591
    ,2147483590
    ,2147483589
    ,2147483588
    ,2147483587
    ,2147483586
    ,2147483585
    ,2147483584
    ,2147483583
    ,2147483582
    ,2147483581
    ,2147483580
    ,2147483579
    ,2147483578
    ,2147483577
    ,2147483576
    ,2147483575
    ,2147483574
    ,2147483573
    ,2147483572
    ,2147483571
    ,2147483570
    ,2147483569
    ,2147483568
    ,2147483567
    ,2147483566
    ,2147483565
    ,2147483564
    ,2147483563
    ,2147483562
    ,2147483561
    ,2147483560
    ,2147483559
    ,2147483558
    ,2147483557
    ,2147483556
    ,2147483555
    ,2147483554
    ,2147483553
    ,2147483552
    ,2147483551
    ,2147483550
    ,2147483549
    ,2147483548
    ,2147483547
    ,2147483546
    ,2147483545
    ,2147483544
    ,2147483543
    ,2147483542
    ,2147483541
    ,2147483540
    ,2147483539
    ,2147483538
    ,2147483537
    ,2147483536
    ,2147483535
    ,2147483534
    ,2147483533
    ,2147483532
    ,2147483531
    ,2147483530
    ,2147483529
    ,2147483528
    ,2147483527
    ,2147483526
    ,2147483525
    ,2147483524
    ,2147483523
    ,2147483522
    ,2147483521
    ,2147483520
    ,2147483519
    ,2147483518
    ,2147483517
    ,2147483516
    ,2147483515
    ,2147483514
    ,2147483513
    ,2147483512
    ,2147483511
    ,2147483510
    ,2147483509
    ,2147483508
    ,2147483507
    ,2147483506
    ,2147483505
    ,2147483504
    ,2147483503
    ,2147483502
    ,2147483501
    ,2147483500
    ,2147483499
    ,2147483498
    ,2147483497
    ,2147483496
    ,2147483495
    ,2147483494
    ,2147483493
    ,2147483492
    ,2147483491
    ,2147483490
    ,2147483489
    ,2147483488
    ,2147483487
    ,2147483486
    ,2147483485
    ,2147483484
    ,2147483483
    ,2147483482
    ,2147483481
    ,2147483480
    ,2147483479
    ,2147483478
    ,2147483477
    ,2147483476
    ,2147483475
    ,2147483474
    ,2147483473
    ,2147483472
    ,2147483471
    ,2147483470
    ,2147483469
    ,2147483468
    ,2147483467
    ,2147483466
    ,2147483465
    ,2147483464
    ,2147483463
    ,2147483462
    ,2147483461
    ,2147483460
    ,2147483459
    ,2147483458
    ,2147483457
    ,2147483456
    ,2147483455
    ,2147483454
    ,2147483453
    ,2147483452
    ,2147483451
    ,2147483450
    ,2147483449
    ,2147483448
    ,2147483447
    ,2147483446
    ,2147483445
    ,2147483444
    ,2147483443
    ,2147483442
    ,2147483441
    ,2147483440
    ,2147483439
    ,2147483438
    ,2147483437
    ,2147483436
    ,2147483435
    ,2147483434
    ,2147483433
    ,2147483432
    ,2147483431
    ,2147483430
    ,2147483429
    ,2147483428
    ,2147483427
    ,2147483426
    ,2147483425
    ,2147483424
    ,2147483423
    ,2147483422
    ,2147483421
    ,2147483420
    ,2147483419
    ,2147483418
    ,2147483417
    ,2147483416
    ,2147483415
    ,2147483414
    ,2147483413
    ,2147483412
    ,2147483411
    ,2147483410
    ,2147483409
    ,2147483408
    ,2147483407
    ,2147483406
    ,2147483405
    ,2147483404
    ,2147483403
    ,2147483402
    ,2147483401
    ,2147483400
    ,2147483399
    ,2147483398
    ,2147483397
    ,2147483396
    ,2147483395
    ,2147483394
    ,2147483393
    ,2147483392
    ,2147483391
    ,2147483390
    ,2147483389
    ,2147483388
    ,2147483387
    ,2147483386
    ,2147483385
    ,2147483384
    ,2147483383
    ,2147483382
    ,2147483381
    ,2147483380
    ,2147483379
    ,2147483378
    ,2147483377
    ,2147483376
    ,2147483375
    ,2147483374
    ,2147483373
    ,2147483372
    ,2147483371
    ,2147483370
    ,2147483369
    ,2147483368
    ,2147483367
    ,2147483366
    ,2147483365
    ,2147483364
    ,2147483363
    ,2147483362
    ,2147483361
    ,2147483360
    ,2147483359
    ,2147483358
    ,2147483357
    ,2147483356
    ,2147483355
    ,2147483354
    ,2147483353
    ,2147483352
    ,2147483351
    ,2147483350
    ,2147483349
    ,2147483348
    ,2147483347
    ,2147483346
    ,2147483345
    ,2147483344
    ,2147483343
    ,2147483342
    ,2147483341
    ,2147483340
    ,2147483339
    ,2147483338
    ,2147483337
    ,2147483336
    ,2147483335
    ,2147483334
    ,2147483333
    ,2147483332
    ,2147483331
    ,2147483330
    ,2147483329
    ,2147483328
    ,2147483327
    ,2147483326
    ,2147483325
    ,2147483324
    ,2147483323
    ,2147483322
    ,2147483321
    ,2147483320
    ,2147483319
    ,2147483318
    ,2147483317
    ,2147483316
    ,2147483315
    ,2147483314
    ,2147483313
    ,2147483312
    ,2147483311
    ,2147483310
    ,2147483309
    ,2147483308
    ,2147483307
    ,2147483306
    ,2147483305
    ,2147483304
    ,2147483303
    ,2147483302
    ,2147483301
    ,2147483300
    ,2147483299
    ,2147483298
    ,2147483297
    ,2147483296
    ,2147483295
    ,2147483294
    ,2147483293
    ,2147483292
    ,2147483291
    ,2147483290
    ,2147483289
    ,2147483288
    ,2147483287
    ,2147483286
    ,2147483285
    ,2147483284
    ,2147483283
    ,2147483282
    ,2147483281
    ,2147483280
    ,2147483279
    ,2147483278
    ,2147483277
    ,2147483276
    ,2147483275
    ,2147483274
    ,2147483273
    ,2147483272
    ,2147483271
    ,2147483270
    ,2147483269
    ,2147483268
    ,2147483267
    ,2147483266
    ,2147483265
    ,2147483264
    ,2147483263
    ,2147483262
    ,2147483261
    ,2147483260
    ,2147483259
    ,2147483258
    ,2147483257
    ,2147483256
    ,2147483255
    ,2147483254
    ,2147483253
    ,2147483252
    ,2147483251
    ,2147483250
    ,2147483249
    ,2147483248
    ,2147483247
    ,2147483246
    ,2147483245
    ,2147483244
    ,2147483243
    ,2147483242
    ,2147483241
    ,2147483240
    ,2147483239
    ,2147483238
    ,2147483237
    ,2147483236
    ,2147483235
    ,2147483234
    ,2147483233
    ,2147483232
    ,2147483231
    ,2147483230
    ,2147483229
    ,2147483228
    ,2147483227
    ,2147483226
    ,2147483225
    ,2147483224
    ,2147483223
    ,2147483222
    ,2147483221
    ,2147483220
    ,2147483219
    ,2147483218
    ,2147483217
    ,2147483216
    ,2147483215
    ,2147483214
    ,2147483213
    ,2147483212
    ,2147483211
    ,2147483210
    ,2147483209
    ,2147483208
    ,2147483207
    ,2147483206
    ,2147483205
    ,2147483204
    ,2147483203
    ,2147483202
    ,2147483201
    ,2147483200
    ,2147483199
    ,2147483198
    ,2147483197
    ,2147483196
    ,2147483195
    ,2147483194
    ,2147483193
    ,2147483192
    ,2147483191
    ,2147483190
    ,2147483189
    ,2147483188
    ,2147483187
    ,2147483186
    ,2147483185
    ,2147483184
    ,2147483183
    ,2147483182
    ,2147483181
    ,2147483180
    ,2147483179
    ,2147483178
    ,2147483177
    ,2147483176
    ,2147483175
    ,2147483174
    ,2147483173
    ,2147483172
    ,2147483171
    ,2147483170
    ,2147483169
    ,2147483168
    ,2147483167
    ,2147483166
    ,2147483165
    ,2147483164
    ,2147483163
    ,2147483162
    ,2147483161
    ,2147483160
    ,2147483159
    ,2147483158
    ,2147483157
    ,2147483156
    ,2147483155
    ,2147483154
    ,2147483153
    ,2147483152
    ,2147483151
    ,2147483150
    ,2147483149
    ,2147483148
    ,2147483147
    ,2147483146
    ,2147483145
    ,2147483144
    ,2147483143
    ,2147483142
    ,2147483141
    ,2147483140
    ,2147483139
    ,2147483138
    ,2147483137
    ,2147483136
    ,2147483135
    ,2147483134
    ,2147483133
    ,2147483132
    ,2147483131
    ,2147483130
    ,2147483129
    ,2147483128
    ,2147483127
    ,2147483126
    ,2147483125
    ,2147483124
    ,2147483123
    ,2147483122
    ,2147483121
    ,2147483120
    ,2147483119
    ,2147483118
    ,2147483117
    ,2147483116
    ,2147483115
    ,2147483114
    ,2147483113
    ,2147483112
    ,2147483111
    ,2147483110
    ,2147483109
    ,2147483108
    ,2147483107
    ,2147483106
    ,2147483105
    ,2147483104
    ,2147483103
    ,2147483102
    ,2147483101
    ,2147483100
    ,2147483099
    ,2147483098
    ,2147483097
    ,2147483096
    ,2147483095
    ,2147483094
    ,2147483093
    ,2147483092
    ,2147483091
    ,2147483090
    ,2147483089
    ,2147483088
    ,2147483087
    ,2147483086
    ,2147483085
    ,2147483084
    ,2147483083
    ,2147483082
    ,2147483081
    ,2147483080
    ,2147483079
    ,2147483078
    ,2147483077
    ,2147483076
    ,2147483075
    ,2147483074
    ,2147483073
    ,2147483072
    ,2147483071
    ,2147483070
    ,2147483069
    ,2147483068
    ,2147483067
    ,2147483066
    ,2147483065
    ,2147483064
    ,2147483063
    ,2147483062
    ,2147483061
    ,2147483060
    ,2147483059
    ,2147483058
    ,2147483057
    ,2147483056
    ,2147483055
    ,2147483054
    ,2147483053
    ,2147483052
    ,2147483051
    ,2147483050
    ,2147483049
    ,2147483048
    ,2147483047
    ,2147483046
    ,2147483045
    ,2147483044
    ,2147483043
    ,2147483042
    ,2147483041
    ,2147483040
    ,2147483039
    ,2147483038
    ,2147483037
    ,2147483036
    ,2147483035
    ,2147483034
    ,2147483033
    ,2147483032
    ,2147483031
    ,2147483030
    ,2147483029
    ,2147483028
    ,2147483027
    ,2147483026
    ,2147483025
    ,2147483024
    ,2147483023
    ,2147483022
    ,2147483021
    ,2147483020
    ,2147483019
    ,2147483018
    ,2147483017
    ,2147483016
    ,2147483015
    ,2147483014
    ,2147483013
    ,2147483012
    ,2147483011
    ,2147483010
    ,2147483009
    ,2147483008
    ,2147483007
    ,2147483006
    ,2147483005
    ,2147483004
    ,2147483003
    ,2147483002
    ,2147483001
    ,2147483000
    ,2147482999
    ,2147482998
    ,2147482997
    ,2147482996
    ,2147482995
    ,2147482994
    ,2147482993
    ,2147482992
    ,2147482991
    ,2147482990
    ,2147482989
    ,2147482988
    ,2147482987
    ,2147482986
    ,2147482985
    ,2147482984
    ,2147482983
    ,2147482982
    ,2147482981
    ,2147482980
    ,2147482979
    ,2147482978
    ,2147482977
    ,2147482976
    ,2147482975
    ,2147482974
    ,2147482973
    ,2147482972
    ,2147482971
    ,2147482970
    ,2147482969
    ,2147482968
    ,2147482967
    ,2147482966
    ,2147482965
    ,2147482964
    ,2147482963
    ,2147482962
    ,2147482961
    ,2147482960
    ,2147482959
    ,2147482958
    ,2147482957
    ,2147482956
    ,2147482955
    ,2147482954
    ,2147482953
    ,2147482952
    ,2147482951
    ,2147482950
    ,2147482949
    ,2147482948
    ,2147482947
    ,2147482946
    ,2147482945
    ,2147482944
    ,2147482943
    ,2147482942
    ,2147482941
    ,2147482940
    ,2147482939
    ,2147482938
    ,2147482937
    ,2147482936
    ,2147482935
    ,2147482934
    ,2147482933
    ,2147482932
    ,2147482931
    ,2147482930
    ,2147482929
    ,2147482928
    ,2147482927
    ,2147482926
    ,2147482925
    ,2147482924
    ,2147482923
    ,2147482922
    ,2147482921
    ,2147482920
    ,2147482919
    ,2147482918
    ,2147482917
    ,2147482916
    ,2147482915
    ,2147482914
    ,2147482913
    ,2147482912
    ,2147482911
    ,2147482910
    ,2147482909
    ,2147482908
    ,2147482907
    ,2147482906
    ,2147482905
    ,2147482904
    ,2147482903
    ,2147482902
    ,2147482901
    ,2147482900
    ,2147482899
    ,2147482898
    ,2147482897
    ,2147482896
    ,2147482895
    ,2147482894
    ,2147482893
    ,2147482892
    ,2147482891
    ,2147482890
    ,2147482889
    ,2147482888
    ,2147482887
    ,2147482886
    ,2147482885
    ,2147482884
    ,2147482883
    ,2147482882
    ,2147482881
    ,2147482880
    ,2147482879
    ,2147482878
    ,2147482877
    ,2147482876
    ,2147482875
    ,2147482874
    ,2147482873
    ,2147482872
    ,2147482871
    ,2147482870
    ,2147482869
    ,2147482868
    ,2147482867
    ,2147482866
    ,2147482865
    ,2147482864
    ,2147482863
    ,2147482862
    ,2147482861
    ,2147482860
    ,2147482859
    ,2147482858
    ,2147482857
    ,2147482856
    ,2147482855
    ,2147482854
    ,2147482853
    ,2147482852
    ,2147482851
    ,2147482850
    ,2147482849
    ,2147482848
    ,2147482847
    ,2147482846
    ,2147482845
    ,2147482844
    ,2147482843
    ,2147482842
    ,2147482841
    ,2147482840
    ,2147482839
    ,2147482838
    ,2147482837
    ,2147482836
    ,2147482835
    ,2147482834
    ,2147482833
    ,2147482832
    ,2147482831
    ,2147482830
    ,2147482829
    ,2147482828
    ,2147482827
    ,2147482826
    ,2147482825
    ,2147482824
    ,2147482823
    ,2147482822
    ,2147482821
    ,2147482820
    ,2147482819
    ,2147482818
    ,2147482817
    ,2147482816
    ,2147482815
    ,2147482814
    ,2147482813
    ,2147482812
    ,2147482811
    ,2147482810
    ,2147482809
    ,2147482808
    ,2147482807
    ,2147482806
    ,2147482805
    ,2147482804
    ,2147482803
    ,2147482802
    ,2147482801
    ,2147482800
    ,2147482799
    ,2147482798
    ,2147482797
    ,2147482796
    ,2147482795
    ,2147482794
    ,2147482793
    ,2147482792
    ,2147482791
    ,2147482790
    ,2147482789
    ,2147482788
    ,2147482787
    ,2147482786
    ,2147482785
    ,2147482784
    ,2147482783
    ,2147482782
    ,2147482781
    ,2147482780
    ,2147482779
    ,2147482778
    ,2147482777
    ,2147482776
    ,2147482775
    ,2147482774
    ,2147482773
    ,2147482772
    ,2147482771
    ,2147482770
    ,2147482769
    ,2147482768
    ,2147482767
    ,2147482766
    ,2147482765
    ,2147482764
    ,2147482763
    ,2147482762
    ,2147482761
    ,2147482760
    ,2147482759
    ,2147482758
    ,2147482757
    ,2147482756
    ,2147482755
    ,2147482754
    ,2147482753
    ,2147482752
    ,2147482751
    ,2147482750
    ,2147482749
    ,2147482748
    ,2147482747
    ,2147482746
    ,2147482745
    ,2147482744
    ,2147482743
    ,2147482742
    ,2147482741
    ,2147482740
    ,2147482739
    ,2147482738
    ,2147482737
    ,2147482736
    ,2147482735
    ,2147482734
    ,2147482733
    ,2147482732
    ,2147482731
    ,2147482730
    ,2147482729
    ,2147482728
    ,2147482727
    ,2147482726
    ,2147482725
    ,2147482724
    ,2147482723
    ,2147482722
    ,2147482721
    ,2147482720
    ,2147482719
    ,2147482718
    ,2147482717
    ,2147482716
    ,2147482715
    ,2147482714
    ,2147482713
    ,2147482712
    ,2147482711
    ,2147482710
    ,2147482709
    ,2147482708
    ,2147482707
    ,2147482706
    ,2147482705
    ,2147482704
    ,2147482703
    ,2147482702
    ,2147482701
    ,2147482700
    ,2147482699
    ,2147482698
    ,2147482697
    ,2147482696
    ,2147482695
    ,2147482694
    ,2147482693
    ,2147482692
    ,2147482691
    ,2147482690
    ,2147482689
    ,2147482688
    ,2147482687
    ,2147482686
    ,2147482685
    ,2147482684
    ,2147482683
    ,2147482682
    ,2147482681
    ,2147482680
    ,2147482679
    ,2147482678
    ,2147482677
    ,2147482676
    ,2147482675
    ,2147482674
    ,2147482673
    ,2147482672
    ,2147482671
    ,2147482670
    ,2147482669
    ,2147482668
    ,2147482667
    ,2147482666
    ,2147482665
    ,2147482664
    ,2147482663
    ,2147482662
    ,2147482661
    ,2147482660
    ,2147482659
    ,2147482658
    ,2147482657
    ,2147482656
    ,2147482655
    ,2147482654
    ,2147482653
    ,2147482652
    ,2147482651
    ,2147482650
    ,2147482649
    ,2147482648
    ,2147482647
    ,2147482646
    ,2147482645
    ,2147482644
    ,2147482643
    ,2147482642
    ,2147482641
    ,2147482640
    ,2147482639
    ,2147482638
    ,2147482637
    ,2147482636
    ,2147482635
    ,2147482634
    ,2147482633
    ,2147482632
    ,2147482631
    ,2147482630
    ,2147482629
    ,2147482628
    ,2147482627
    ,2147482626
    ,2147482625
    ,2147482624
    ,2147482623
    ,2147482622
    ,2147482621
    ,2147482620
    ,2147482619
    ,2147482618
    ,2147482617
    ,2147482616
    ,2147482615
    ,2147482614
    ,2147482613
    ,2147482612
    ,2147482611
    ,2147482610
    ,2147482609
    ,2147482608
    ,2147482607
    ,2147482606
    ,2147482605
    ,2147482604
    ,2147482603
    ,2147482602
    ,2147482601
    ,2147482600
    ,2147482599
    ,2147482598
    ,2147482597
    ,2147482596
    ,2147482595
    ,2147482594
    ,2147482593
    ,2147482592
    ,2147482591
    ,2147482590
    ,2147482589
    ,2147482588
    ,2147482587
    ,2147482586
    ,2147482585
    ,2147482584
    ,2147482583
    ,2147482582
    ,2147482581
    ,2147482580
    ,2147482579
    ,2147482578
    ,2147482577
    ,2147482576
    ,2147482575
    ,2147482574
    ,2147482573
    ,2147482572
    ,2147482571
    ,2147482570
    ,2147482569
    ,2147482568
    ,2147482567
    ,2147482566
    ,2147482565
    ,2147482564
    ,2147482563
    ,2147482562
    ,2147482561
    ,2147482560
    ,2147482559
    ,2147482558
    ,2147482557
    ,2147482556
    ,2147482555
    ,2147482554
    ,2147482553
    ,2147482552
    ,2147482551
    ,2147482550
    ,2147482549
    ,2147482548
    ,2147482547
    ,2147482546
    ,2147482545
    ,2147482544
    ,2147482543
    ,2147482542
    ,2147482541
    ,2147482540
    ,2147482539
    ,2147482538
    ,2147482537
    ,2147482536
    ,2147482535
    ,2147482534
    ,2147482533
    ,2147482532
    ,2147482531
    ,2147482530
    ,2147482529
    ,2147482528
    ,2147482527
    ,2147482526
    ,2147482525
    ,2147482524
    ,2147482523
    ,2147482522
    ,2147482521
    ,2147482520
    ,2147482519
    ,2147482518
    ,2147482517
    ,2147482516
    ,2147482515
    ,2147482514
    ,2147482513
    ,2147482512
    ,2147482511
    ,2147482510
    ,2147482509
    ,2147482508
    ,2147482507
    ,2147482506
    ,2147482505
    ,2147482504
    ,2147482503
    ,2147482502
    ,2147482501
    ,2147482500
    ,2147482499
    ,2147482498
    ,2147482497
    ,2147482496
    ,2147482495
    ,2147482494
    ,2147482493
    ,2147482492
    ,2147482491
    ,2147482490
    ,2147482489
    ,2147482488
    ,2147482487
    ,2147482486
    ,2147482485
    ,2147482484
    ,2147482483
    ,2147482482
    ,2147482481
    ,2147482480
    ,2147482479
    ,2147482478
    ,2147482477
    ,2147482476
    ,2147482475
    ,2147482474
    ,2147482473
    ,2147482472
    ,2147482471
    ,2147482470
    ,2147482469
    ,2147482468
    ,2147482467
    ,2147482466
    ,2147482465
    ,2147482464
    ,2147482463
    ,2147482462
    ,2147482461
    ,2147482460
    ,2147482459
    ,2147482458
    ,2147482457
    ,2147482456
    ,2147482455
    ,2147482454
    ,2147482453
    ,2147482452
    ,2147482451
    ,2147482450
    ,2147482449
    ,2147482448
    ,2147482447
    ,2147482446
    ,2147482445
    ,2147482444
    ,2147482443
    ,2147482442
    ,2147482441
    ,2147482440
    ,2147482439
    ,2147482438
    ,2147482437
    ,2147482436
    ,2147482435
    ,2147482434
    ,2147482433
    ,2147482432
    ,2147482431
    ,2147482430
    ,2147482429
    ,2147482428
    ,2147482427
    ,2147482426
    ,2147482425
    ,2147482424
    ,2147482423
    ,2147482422
    ,2147482421
    ,2147482420
    ,2147482419
    ,2147482418
    ,2147482417
    ,2147482416
    ,2147482415
    ,2147482414
    ,2147482413
    ,2147482412
    ,2147482411
    ,2147482410
    ,2147482409
    ,2147482408
    ,2147482407
    ,2147482406
    ,2147482405
    ,2147482404
    ,2147482403
    ,2147482402
    ,2147482401
    ,2147482400
    ,2147482399
    ,2147482398
    ,2147482397
    ,2147482396
    ,2147482395
    ,2147482394
    ,2147482393
    ,2147482392
    ,2147482391
    ,2147482390
    ,2147482389
    ,2147482388
    ,2147482387
    ,2147482386
    ,2147482385
    ,2147482384
    ,2147482383
    ,2147482382
    ,2147482381
    ,2147482380
    ,2147482379
    ,2147482378
    ,2147482377
    ,2147482376
    ,2147482375
    ,2147482374
    ,2147482373
    ,2147482372
    ,2147482371
    ,2147482370
    ,2147482369
    ,2147482368
    ,2147482367
    ,2147482366
    ,2147482365
    ,2147482364
    ,2147482363
    ,2147482362
    ,2147482361
    ,2147482360
    ,2147482359
    ,2147482358
    ,2147482357
    ,2147482356
    ,2147482355
    ,2147482354
    ,2147482353
    ,2147482352
    ,2147482351
    ,2147482350
    ,2147482349
    ,2147482348
    ,2147482347
    ,2147482346
    ,2147482345
    ,2147482344
    ,2147482343
    ,2147482342
    ,2147482341
    ,2147482340
    ,2147482339
    ,2147482338
    ,2147482337
    ,2147482336
    ,2147482335
    ,2147482334
    ,2147482333
    ,2147482332
    ,2147482331
    ,2147482330
    ,2147482329
    ,2147482328
    ,2147482327
    ,2147482326
    ,2147482325
    ,2147482324
    ,2147482323
    ,2147482322
    ,2147482321
    ,2147482320
    ,2147482319
    ,2147482318
    ,2147482317
    ,2147482316
    ,2147482315
    ,2147482314
    ,2147482313
    ,2147482312
    ,2147482311
    ,2147482310
    ,2147482309
    ,2147482308
    ,2147482307
    ,2147482306
    ,2147482305
    ,2147482304
    ,2147482303
    ,2147482302
    ,2147482301
    ,2147482300
    ,2147482299
    ,2147482298
    ,2147482297
    ,2147482296
    ,2147482295
    ,2147482294
    ,2147482293
    ,2147482292
    ,2147482291
    ,2147482290
    ,2147482289
    ,2147482288
    ,2147482287
    ,2147482286
    ,2147482285
    ,2147482284
    ,2147482283
    ,2147482282
    ,2147482281
    ,2147482280
    ,2147482279
    ,2147482278
    ,2147482277
    ,2147482276
    ,2147482275
    ,2147482274
    ,2147482273
    ,2147482272
    ,2147482271
    ,2147482270
    ,2147482269
    ,2147482268
    ,2147482267
    ,2147482266
    ,2147482265
    ,2147482264
    ,2147482263
    ,2147482262
    ,2147482261
    ,2147482260
    ,2147482259
    ,2147482258
    ,2147482257
    ,2147482256
    ,2147482255
    ,2147482254
    ,2147482253
    ,2147482252
    ,2147482251
    ,2147482250
    ,2147482249
    ,2147482248
    ,2147482247
    ,2147482246
    ,2147482245
    ,2147482244
    ,2147482243
    ,2147482242
    ,2147482241
    ,2147482240
    ,2147482239
    ,2147482238
    ,2147482237
    ,2147482236
    ,2147482235
    ,2147482234
    ,2147482233
    ,2147482232
    ,2147482231
    ,2147482230
    ,2147482229
    ,2147482228
    ,2147482227
    ,2147482226
    ,2147482225
    ,2147482224
    ,2147482223
    ,2147482222
    ,2147482221
    ,2147482220
    ,2147482219
    ,2147482218
    ,2147482217
    ,2147482216
    ,2147482215
    ,2147482214
    ,2147482213
    ,2147482212
    ,2147482211
    ,2147482210
    ,2147482209
    ,2147482208
    ,2147482207
    ,2147482206
    ,2147482205
    ,2147482204
    ,2147482203
    ,2147482202
    ,2147482201
    ,2147482200
    ,2147482199
    ,2147482198
    ,2147482197
    ,2147482196
    ,2147482195
    ,2147482194
    ,2147482193
    ,2147482192
    ,2147482191
    ,2147482190
    ,2147482189
    ,2147482188
    ,2147482187
    ,2147482186
    ,2147482185
    ,2147482184
    ,2147482183
    ,2147482182
    ,2147482181
    ,2147482180
    ,2147482179
    ,2147482178
    ,2147482177
    ,2147482176
    ,2147482175
    ,2147482174
    ,2147482173
    ,2147482172
    ,2147482171
    ,2147482170
    ,2147482169
    ,2147482168
    ,2147482167
    ,2147482166
    ,2147482165
    ,2147482164
    ,2147482163
    ,2147482162
    ,2147482161
    ,2147482160
    ,2147482159
    ,2147482158
    ,2147482157
    ,2147482156
    ,2147482155
    ,2147482154
    ,2147482153
    ,2147482152
    ,2147482151
    ,2147482150
    ,2147482149
    ,1500
    );
  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    X                               1
  """

@pytest.mark.version('>=2.5')
def test_core_3740_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_expected_stdout == act_1.clean_stdout

