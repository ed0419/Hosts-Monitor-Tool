from datetime import timedelta
import re, pymysql, json, requests
from flask import Flask, request,  render_template, redirect, session, Response
from flask_cors import CORS

app = Flask(__name__,static_folder='static/')
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config.update(
TESTING=True,
SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/',
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
@app.route("/test")
def testa():
    try:
        db = pymysql.connect(host="192.168.88.34",user="hmt",passwd="12345678",database="hmt_data")
        cursor = db.cursor()
        uid=session["login_uid"]
        cursor.execute(f"SELECT SERVER_ID, NAME, IP, PORT from SYS_HOSTS where OWNEDBY='{uid}'")
        results = cursor.fetchall()
        for row in results:
            server_id = row[0]
            name = row[1]
            ip = row[2]
            port = row[3]
        print(ip,port)
        r_player = requests.get(f"http://{ip}:{port}/players.json").json()
        r_info = requests.get(f"http://{ip}:{port}/info.json").json()
        hostname = r_info['vars']['sv_projectDesc']
        players = len(r_player)
        ping = []
        for i in r_player:
            ping.append(i['ping'])
        ping_avg = str(sum(ping)/len(r_player))
        html =f' \
            <tr> \
                <td>{server_id}</td>\
                <td><a href="/server/1">{ip}</a></td>\
                <td>{name}</td>\
                <td class="hostname">{hostname}</td>\
                <td>{players}</td>\
                <td>{ping_avg}</td>\
            </tr> '
    except:
        return "Error"
    return render_template("admin.html",html=html)

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
    if 'login' not in session:
        session['login'] = 0
    if 'login_uid' not in session:
        session['login_uid'] = "OR 1=1"
    if request.method == "POST":
        uid = request.form["uid"]
        upass = request.form["upass"]
        db = pymysql.connect(host="192.168.88.34",user="hmt",passwd="12345678",database="hmt_data")
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
@app.route("/new")
def newhost():
    try:
        if session['login'] == 1:
            uid=session['uid']
        return render_template("new.html")
    except:
        return redirect("/admin")
# 管理頁面
@app.route('/admin')
def admin():
        try:
            if session['login'] == 1:
                uid=session["login_uid"]
                faild_count = 0
                html = ""
                #SQL CONN
                db = pymysql.connect(host="192.168.88.34",user="hmt",passwd="12345678",database="hmt_data")
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
                        r_player = requests.get(f"http://{ip}:{port}/players.json", timeout=10).json()
                        r_info = requests.get(f"http://{ip}:{port}/info.json", timeout=10).json()
                        hostname = r_info['vars']['sv_projectDesc']
                        players = len(r_player)
                        ping = []
                        for i in r_player:
                            ping.append(i['ping'])
                        ping_avg = str(sum(ping)/len(r_player))
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