import re
import pymysql,requests
try:
  db = pymysql.connect(host="192.168.88.34",user="hmt",passwd="12345678",database="hmt_data")
  print("OK")
except pymysql.Error as e:
  print("DB Failed"+str(e))
cursor = db.cursor()
uid = "admin"
cursor.execute(f"SELECT SERVER_ID, NAME, IP, PORT from SYS_HOSTS where OWNEDBY='{uid}'")
results = cursor.fetchall()
print(results)
for i in range(len(results)):
  server_id = results[i][0]
  name = results[i][1]
  ip = results[i][2]
  port = results[i][3]
  print(server_id,name,ip,port)
#print(requests.get(f"http://{ip}:{port}/players.json").json())