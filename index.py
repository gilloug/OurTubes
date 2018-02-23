#!/usr/bin/env python3

import sys
import hashlib
from templates import addMusic, index, joinChan, createChan, deleteChan, register, error, player, Help
from flask import Flask, render_template, request, json, jsonify
from flaskext.mysql import MySQL
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from flask_cors import CORS

DEVELOPER_KEY = 'AIzaSyBGrO4OFxP9ySwJ1gxLG7utMOb8Jki-JGg'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

mysql = MySQL()
app = Flask(__name__, static_url_path='')
CORS(app)
dbconf = {}

try:
    with open('conf/database.cfg', 'r') as f:
        for line in f:
            tmp = line.split('=')
            dbconf[tmp[0].strip()] = tmp[1].strip()
except Exception as e:
    print("Error in conf/database.cfg : " + str(e), file=sys.stderr)
    exit(84)

app.config['MYSQL_DATABASE_USER'] = dbconf['user']
app.config['MYSQL_DATABASE_PASSWORD'] = dbconf['password']
app.config['MYSQL_DATABASE_DB'] = dbconf['database']
app.config['MYSQL_DATABASE_HOST'] = dbconf['host']
mysql.init_app(app)
def ret(obj, code):
    response = jsonify(obj)
    response.status_code = code
    return response

def get_title(music):
    return "title"

@app.route("/")
@app.route("/index")
def idx():
    login = ""
    password = ""
    connected = ""
    connected_as = ""
    connected_to = ""
    try:
        login = request.cookies.get('Login')
        password = request.cookies.get('Password')
        connected = request.cookies.get('Connected')
        connected_as = request.cookies.get('Connected-as')
        connected_to = request.cookies.get('Connected-to')
    except:
        pass
    return index.main(mysql, connected, connected_as, connected_to, login, password)

@app.route('/register')
def rgstr():
    return register.main(mysql)

@app.route('/help')
def help():
    return Help.main()

@app.route('/player')
def plyr():
    login = ""
    connected_to = ""
    connected_as = ""
    try:
        login = request.cookies.get('Login')
        connected_to = request.cookies.get('Connected-to')
        connected_as = request.cookies.get('Connected-as')
    except:
        pass
    if login != "" and login != None and connected_as == "Administrator":
        return player.main(mysql, "True", "Administrator", connected_to)
    else:
        return error.login(mysql)

@app.route('/createChan')
def createaChan():
    login = ""
    connected_as = ""
    try:
        login = request.cookies.get('Login')
        connected_as = request.cookies.get('Connected-as')
    except:
        pass
    if login != "" and login != None:
        return createChan.main(mysql, connected_as)
    else:
        return error.login(mysql)

@app.route('/deleteChan')
def deleteaChan():
    login = ""
    connected_as = ""
    try:
        login = request.cookies.get('Login')
        connected_as = request.cookies.get('Connected-as')
    except:
        pass
    if login != "" and login != None:
        return deleteChan.main(mysql, connected_as)
    else:
        return error.login(mysql)

@app.route('/joinChan')
def joinaChan():
    login = ""
    connected_as = ""
    try:
        login = request.cookies.get('Login')
        connected_as = request.cookies.get('Connected-as')
    except:
        pass
    if login != "" and login != None:
        return joinChan.main(mysql, connected_as)
    else:
        return error.login(mysql)

@app.route('/searchMusic')
def addsearchMusic():
    try:
        connected = request.cookies.get('Connected')
        connected_as = request.cookies.get('Connected-as')
        connected_to = request.cookies.get('Connected-to')
    except:
        pass
    return addMusic.main(connected, connected_as, connected_to)

@app.route('/changeMusic', methods=['POST'])
def changeMusic():
    connected = request.cookies.get('Connected')
    connected_as = request.cookies.get('Connected-as')
    connected_to = request.cookies.get('Connected-to')
    if connected and connected_as == "Administrator" and connected_to:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('getPlaylist', [connected_to])
        data = cursor.fetchall()
        if len(data) > 0:
            data = tuple(sorted(data, reverse=True, key=lambda item: item[5]))
            conn.commit()
            conn.close()
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('removeMusic', [connected_to, data[0][2]])
            rep = cursor.fetchall()
            if len(rep) > 0:
                conn.commit()
                conn.close()
                return ret({'message':'Cannot create User'}, 400)
            conn.commit()
            conn.close()
            return ret({'message':'User successfully created'}, 200)
        else:
            conn.commit()
            conn.close()
            return ret({'message':'Cannot create User'}, 400)

@app.route('/connect', methods=['POST'])
def connect():
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    _password = hashlib.sha256(_password.encode('utf-8')).hexdigest()
    if _email and _password:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('getUser',(_email, _password))
        data = cursor.fetchall()
        conn.commit()
        conn.close()
        if len(data) > 0:
            resp = ret({'message':'Successfully connected'}, 200)
            resp.set_cookie('Login', _email)
            resp.set_cookie('Password', _password)
            return resp
        else:
            return ret({'message':'Cannot Connect'}, 400)

@app.route('/addUser', methods=['POST'])
def addUser():
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    _password = hashlib.sha256(_password.encode('utf-8')).hexdigest()
    _passwordd = request.form['inputPasswordd']
    _passwordd = hashlib.sha256(_passwordd.encode('utf-8')).hexdigest()
    if _password != _passwordd:
        return ret({'message':'Cannot Create user'}, 400)
    if _email and _password and _passwordd:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('addUser',(_email, _password))
        data = cursor.fetchall()
        conn.commit()
        conn.close()
        if len(data) > 0:
            return ret({'message':'Cannot create User'}, 400)
        else:
            resp = ret({'message':'User successfully created'}, 200)
            return resp

@app.route('/searchMusicParam', methods=['GET'])
def searchMusicParam():
    try:
        connected = request.cookies.get('Connected')
        connected_as = request.cookies.get('Connected-as')
        connected_to = request.cookies.get('Connected-to')
        search = request.args.get('search')
        musics = youtube_search(search, 20)
    except:
        pass
    return addMusic.result(musics)

@app.route('/addMusic', methods=['POST'])
def addaMusic():
    _url = request.form['url']
    _title = request.form['title']
    _picture = request.form['picture']
    _name = request.cookies.get('Connected-to')
    if _name and _url and _picture and _title:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('addMusic',(_name, _url, _picture, _title))
        data = cursor.fetchall()
        conn.commit()
        conn.close()
        if len(data) > 0:
            return ret({'message':'Cannot upvote music'}, 400)
        else:
            return ret({'message':'Music upvoted'}, 200)

@app.route('/upvoteMusic', methods=['POST'])
def upvoteMusic():
    _url = request.form['url']
    _name = request.cookies.get('Connected-to')
    _login = request.cookies.get('Login')
    if _name and _url:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('addAction',(_login, _url, _name, 1))
        data = cursor.fetchall()
        conn.commit()
        conn.close()
        if len(data) > 0:
            return ret({'message':'Cannot upvote music'}, 400)
        else:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('upMusic',(_name, _url))
            data = cursor.fetchall()
            conn.commit()
            conn.close()
            if len(data) > 0:
                return ret({'message':'Cannot upvote music'}, 400)
            else:
                return ret({'message':'Music upvoted'}, 200)

@app.route('/downvoteMusic', methods=['POST'])
def downvoteMusic():
    _url = request.form['url']
    _name = request.cookies.get('Connected-to')
    _login = request.cookies.get('Login')
    if _name and _url:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('addAction',(_login, _url, _name, -1))
        data = cursor.fetchall()
        conn.commit()
        conn.close()
        if len(data) > 0:
            return ret({'message':'Cannot upvote music'}, 400)
        else:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('downMusic',(_name, _url))
            data1 = cursor.fetchall()
            conn.commit()
            cursor.callproc('checkMusic',(_name, _url))
            data2 = cursor.fetchall()
            conn.commit()
            conn.close()
            if len(data1) > 0:
                return ret({'message':'Cannot downvote music'}, 400)
            else:
                return ret({'message':'Music downvoted'}, 200)

@app.route('/deleteMusic', methods=['POST'])
def deleteMusic():
    _url = request.form['url']
    _name = request.cookies.get('Connected-to')
    if _name and _url:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('removeMusic',(_name, _url))
        data = cursor.fetchall()
        conn.commit()
        conn.close()
        if len(data) > 0:
            return ret({'message':'Cannot remove music'}, 400)
        else:
            return ret({'message':'Music removed'}, 200)

@app.route('/leave',methods=['POST'])
def leave():
    resp = ret({'message':'Successfully deconnected'}, 200)
    resp.set_cookie('Connected', 'False')
    resp.set_cookie('Connected-to', '')
    resp.set_cookie('Connected-as', '')
    return resp


@app.route('/logout',methods=['POST'])
def log_out():
    resp = ret({'message':'Successfully deconnected'}, 200)
    resp.set_cookie('Connected', 'False')
    resp.set_cookie('Connected-to', '')
    resp.set_cookie('Connected-as', '')
    resp.set_cookie('Login', '')
    resp.set_cookie('Password', '')
    return resp

@app.route('/join',methods=['POST'])
def join():
    _name = request.form['inputChanName']
    _password = request.form['inputPassword']
    _password = hashlib.sha256(_password.encode('utf-8')).hexdigest()
    _isAdmin = True
    try:
        _isAdmin = request.form['isAdmin']
        _isAdmin = True
    except:
        _isAdmin = False
    if _name and _password:
        conn = mysql.connect()
        cursor = conn.cursor()
        if _isAdmin is False:
            cursor.callproc('joinAsGuest',(_name, _password))
        else:
            cursor.callproc('joinAsAdministrator',(_name, _password))
        data = cursor.fetchall()
        if len(data) is 0 or data[0][0] == 1:
            conn.commit()
            conn.close()
            resp = ret({'message':'Successfully connected'}, 200)
            resp.set_cookie('Connected', 'True')
            resp.set_cookie('Connected-to', _name)
            if _isAdmin is True:
                resp.set_cookie('Connected-as', 'Administrator')
            else:
                resp.set_cookie('Connected-as', 'Guest')
            return resp
        else:
            conn.close()
            return ret({'message':str(data[0])}, 400)
    else:
        return ret({'message':'Fill all the fields'}, 400)

@app.route('/create',methods=['POST'])
def create():
    _name = request.form['inputChanName']
    _publicPassword = request.form['inputPublicPassword']
    _publicPassword = hashlib.sha256(_publicPassword.encode('utf-8')).hexdigest()
    _privatePassword = request.form['inputPrivatePassword']
    _privatePassword = hashlib.sha256(_privatePassword.encode('utf-8')).hexdigest()
    if _name and _publicPassword and _privatePassword:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('createChan',(_name, _publicPassword, _privatePassword))
        data = cursor.fetchall()
        if len(data) is 0:
            conn.commit()
            conn.close()
            return ret({'message':'User created successfully !'}, 200)
        else:
            conn.close()
            return ret({'message':str(data[0])}, 400)
    else:
        return ret({'message':'Fill all the fields'}, 400)

@app.route('/delete',methods=['POST'])
def delete():
    _name = request.form['inputChanName']
    _privatePassword = request.form['inputPrivatePassword']
    _privatePassword = hashlib.sha256(_privatePassword.encode('utf-8')).hexdigest()
    if _name and _privatePassword:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('deleteChan',(_name, _privatePassword))
        data = cursor.fetchall()
        if len(data) is 0:
            conn.commit()
            conn.close()
            return ret({'message':'Chan successfully deleted !'}, 200)
        else:
            conn.close()
            return ret({'message':str(data[0])}, 400)
    else:
        return ret({'message':'Fill all the fields'}, 400)

def youtube_search(arg, num):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)
    search_response = youtube.search().list(
        q=arg,
        part='id,snippet',
        maxResults=num
    ).execute()
    videos = []
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            picture = search_result['snippet']['thumbnails']['default']['url']
            title = search_result['snippet']['title']
            url = "https://www.youtube.com/watch?v=" + search_result['id']['videoId']
            item = (picture, title, url)
            videos.append(item)
    return videos

if __name__ == "__main__":
    app.run()
