r = [{"endpoint": "127.0.0.1", "id": 2, "identifiers": ["steam:110000117697e24", "license:2144a8951e3db41942826bfe14dd1a2d192048c3", "live:914798750515047", "discord:557571586383675404", "license2:0d62739c394e6d56cefc5d45c783b85b5486e2f4"], "name": "玄樂", "ping": 45}, {"endpoint": "127.0.0.1", "id": 4, "identifiers": ["steam:1100001111cf5e0", "license:1cbced73eecea9df559280b01c5d8078faab7088", "live:914798324932540", "discord:429047106825748512", "license2:a9ebef3872c5fe721c487ff98805886c0f688817"], "name": "雪狼", "ping": 50}, {"endpoint": "127.0.0.1", "id": 22, "identifiers": ["steam:11000013f26db22", "license:cd2b05326d207d97d877049ea7faeb32d85e2318", "live:844425486995643", "discord:526286383548071946", "license2:339c14a76e8182f1c0fe45955b8e1df203af0f51"], "name": "小凡", "ping": 49}, {"endpoint": "127.0.0.1", "id": 35, "identifiers": ["steam:11000010b4ab134", "license:828c9ca22e6ae7f388db7069441f1e1210b6cc2b", "xbl:2535446609264265", "live:844428530479521", "discord:602562788677779466", "license2:ecacd05ced68eb5b4e646da8eeb554a70f821585"], "name": "A$AP chun", "ping": 50}, {"endpoint": "127.0.0.1", "id": 40, "identifiers": ["steam:110000135059b88", "license:abe014cbc4c8a63c01f1fac5945f34211305b93e", "discord:508607574694821909", "license2:928fd66ab126f2d066892eac9faa7c039b90f37a"], "name": "尹裴", "ping": 62}, {"endpoint": "127.0.0.1", "id": 48, "identifiers": ["steam:11000013e5360a1", "license:ba57be89ec74a16343c989229f83fe9649db95ba", "xbl:2535419816516391", "live:1055521713962161", "discord:686411615087755472", "fivem:3146111", "license2:ba57be89ec74a16343c989229f83fe9649db95ba"], "name": "Lil Anan", "ping": 41}, {"endpoint": "127.0.0.1", "id": 49, "identifiers": ["steam:11000010dea7891", "license:d5449a3b1f64835152b97c6ccf1cef26663c57a6", "xbl:2535447191789397", "live:985157494440670", "discord:442195305824256010", "fivem:2804405"], "name": "^5H̶o̶n̶g̶^7 ̶K̶", "ping": 44}]
print(len(r))
for i in r:
    print(i['name'])
    print(i['ping'])