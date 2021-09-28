from datetime import timedelta
import re, pymysql, json, requests
from flask import Flask, request,  render_template, redirect, session, Response
from flask_cors import CORS
from requests.api import post
from requests.sessions import PreparedRequest

app = Flask(__name__,static_folder='static/')
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config.update(
TESTING=True,
SECRET_KEY=b'eere43443d',
SESSION_COOKIE_NAME="WHATDOUWANT",
#SESSION_COOKIE_DOMAIN=""
)

@app.route("/api/test")
def test():
    r = requests.get("http://103.122.190.111:30120/players.json").json()
    ping_avg = []
    for i in r:
        ping_avg.append(i['ping'])
    return render_template("admin.html")
    #return Response(json.dumps(r, ensure_ascii=False).encode('utf8'), mimetype='application/json')

# 重導
@app.route('/')
def main():
    return redirect("login")

#設置session timeout
@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)

#登入介面 and session
@app.route('/login',methods=["POST","GET"])
def login():
    try:
        if 'login' not in session:
            session['login'] = 0
        if 'login_uid' not in session:
            session['login_uid'] = "X"
    except:
        print("F?")
    if session['login'] == 1:
        return redirect("/admin")
    if request.method == "POST":
        uid = request.form["uid"]
        upass = request.form["upass"]
        db = pymysql.connect(host="oapw.mc2021.net",user="hmt",passwd="12345678",database="hmt_data")
        cursor = db.cursor()
        print(uid,upass)
        try:
            cursor.execute("SELECT PASSWORD from SYS_USERS where USER='{}'".format(uid))
            result = list(cursor)[0][0]
            print(result)
            if upass == result:
                session['login'] = 1
                session['login_uid'] = uid
                return redirect("admin")
            else:
                print("Error")
                return render_template("login.html",errorMsg="錯誤的使用者帳號密碼")
        except:
            return render_template("login.html",errorMsg="錯誤的使用者帳號密碼")
    else:
        return render_template("login.html",errorMsg=" ")

@app.route("/new",methods=["POST","GET"])
def newhost():
    if 'login' not in session:
        session['login'] = 0
    if 'login_uid' not in session:
        session['login_uid'] = "X"
    if request.method == "POST":
        if session['login'] == 1:
            uid = session['login_uid']
            hname = request.form["hname"]
            hip = request.form["hip"]
            hport = request.form["hport"]
            
            #check patarn
            IPREGEX = "^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
            PORTREGEX = "^([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$"
            if re.search(IPREGEX,hip):
                ok_hip = hip
            else:
                print("SQLi Dectected!",hip)
            if re.search(PORTREGEX,hport):
                ok_hport = hport
            else:
                print("SQLi Dectected!",hport)
            try:
                db = pymysql.connect(host="oapw.mc2021.net",user="hmt",passwd="12345678",database="hmt_data")
                cursor = db.cursor()
                cursor.execute(f"INSERT INTO SYS_HOSTS (OWNEDBY, NAME, IP, PORT) VALUES ('{uid}','{hname}','{ok_hip}','{ok_hport}')")
                db.commit()
                return render_template("new.html",uid=uid,ErrorMsg="成功")
            except:
                return render_template("new.html",ErrorMsg="Faild To Connect SQL Server")
        else:
            return redirect("/admin")
        
    else:
        if session['login'] == 1:
            return render_template("new.html",uid=session['login_uid'])
        else:
            return redirect("/admin")

@app.route("/delete")
def delete_host():
    if 'login' not in session:
        session['login'] = 0
    if 'login_uid' not in session:
        session['login_uid'] = "X"
    try:
        if session['login'] == 1:
            uid=session["login_uid"]
            html = ""
            #SQL CONN
            db = pymysql.connect(host="oapw.mc2021.net",user="hmt",passwd="12345678",database="hmt_data")
            cursor = db.cursor()
            cursor.execute(f"SELECT SERVER_ID, NAME, IP, PORT from SYS_HOSTS where OWNEDBY='{uid}'")
            results = cursor.fetchall()
            print(results)
            for i in range(len(results)):
                server_id = results[i][0]
                name = results[i][1]
                ip = results[i][2]
                port = results[i][3]
                print(server_id,name,ip,port)
                html +=f' \
                    <tr> \
                        <td>{server_id}</td>\
                        <td><a href="/server/{ip}">{ip}</a></td>\
                        <td class="hostname">{name}</td>\
                        <td><form action="/delete/?ip={ip}" method="POST"><a type=">確認刪除</a></td>\
                    </tr> '
            
            return render_template("delete.html",uid=uid,html=html)
        else:
            return redirect("/admin")
    except:
        return render_template("delete.html",uid=uid,html=html)

# 管理頁面
@app.route('/admin')
def admin():
    if 'login' not in session:
        session['login'] = 0
    if 'login_uid' not in session:
        session['login_uid'] = "X"
    try:
        if session['login'] == 1:
            uid=session["login_uid"]
            faild_count = 0
            html = ""
            #SQL CONN
            db = pymysql.connect(host="oapw.mc2021.net",user="hmt",passwd="12345678",database="hmt_data")
            cursor = db.cursor()
            cursor.execute(f"SELECT SERVER_ID, NAME, IP, PORT from SYS_HOSTS where OWNEDBY='{uid}'")
            results = cursor.fetchall()

            for i in range(len(results)):
                server_id = results[i][0]
                name = results[i][1]
                ip = results[i][2]
                port = results[i][3]
                print(server_id,name,ip,port)
                try:
                    r_player = requests.get(f"http://{ip}:{port}/players.json", timeout=5).json()
                    r_info = requests.get(f"http://{ip}:{port}/info.json", timeout=5).json()
                    hostname = r_info['vars']['sv_projectDesc']
                    players = len(r_player)
                    ping = []

                    for i in r_player:
                        ping.append(i['ping'])
                    ping_avg = str(round(sum(ping)/len(r_player),2))

                    html +=f' \
                        <tr> \
                            <td>{server_id}</td>\
                            <td><a href="/server/1">{ip}</a></td>\
                            <td>{name}</td>\
                            <td class="hostname">{hostname}</td>\
                            <td>{players}</td>\
                            <td>{ping_avg}</td>\
                        </tr> '
                except:
                    faild_count += 1
                    print("Cant Fetch",server_id,name,ip,port)
            return render_template("admin.html",html=html,uid=uid,host_count=len(results),faild_count=faild_count)
        else:
            return redirect("login")
    except pymysql.Error as e:
        print("DB Failed"+str(e))
        return redirect("login")

# 登出
@app.route('/logout')
def logout():
    session['login'] = 0
    return redirect("login")

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port=8080, debug=True)