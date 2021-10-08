import pymysql
try:
  db = pymysql.connect(host="192.168.88.34",user="hmt",passwd="12345678",database="hmt_data")
  print("OK")
except pymysql.Error as e:
  print("DB Failed"+str(e))
cursor = db.cursor()
uid = "admin"
name = "local"
ip = "127.0.0.1"
port = "30120"
cursor.execute(f"INSERT INTO SYS_HOSTS (OWNEDBY, NAME, IP, PORT) VALUES ('{uid}','{name}','{ip}','{port}')")
db.commit()
results = cursor.fetchall()
print(results)