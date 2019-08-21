from flask import Flask,render_template,request,redirect,url_for,Response,session,flash
from flask_mail import Mail,Message
from pymongo import MongoClient
import json
import urllib
import datetime
import threading,jinja2
# pip install dnspython required to resolve mongo IP

mongo = MongoClient('mongodb+srv://cmsnoc93:'+ urllib.parse.quote('cmsnoc@123') + '@cluster0-qxw77.mongodb.net/test?retryWrites=true&w=majority')
db = mongo.CMS_Automation
collection = db.Ticket_automation
app = Flask(__name__)
app.secret_key = 'some_secret'

@app.route('/login', methods=['GET', 'POST'])
def login():
    m = dict()
    login_det = db.Login_table.find()
    time = ''
    if datetime.datetime.today().strftime('%p') == 'AM':
        time = 'Morning'
    elif datetime.datetime.today().strftime('%p') == 'PM':
        time = 'Night'
    shift_det = collection.find({"date":datetime.datetime.today().strftime('%d-%m-%Y'),'shift':time,'freeze':0})
    shift_freeze = collection.find({"date":datetime.datetime.today().strftime('%d-%m-%Y'),'shift':time,'freeze':1})
    for l in login_det:
        m[l['username']] = l['password']
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        if shift_freeze.count() > 0:
            flash("Login Duration Expired", 'log_msg')
            return redirect(url_for('login'))
        elif shift_freeze.count() == 0:
            if (request.form['username'] in m.keys()):
                if (m[request.form['username']] == request.form['password']):
                    session['logged_in'] = True
                    session['role'] = request.form['role']
                    session['username'] = request.form['username']
                    if shift_det.count() == 0:
                        engineers = {}
                        engineers[request.form['username']] = dict()
                        engineers[request.form['username']]['name'] = request.form['username']
                        engineers[request.form['username']]['role'] = request.form['role']
                        engineers[request.form['username']]['cases'] = []
                        engineers[request.form['username']]['leave'] = 0
                        print(engineers)
                        collection.insert({"date": datetime.datetime.today().strftime('%d-%m-%Y'), 'shift': time, 'engineers':engineers, 'freeze':0})
                    elif shift_det.count()>0:
                        engineers = {}
                        for i in shift_det:
                            engineers = i['engineers']
                        engineers[request.form['username']] = dict()
                        engineers[request.form['username']]['name'] = request.form['username']
                        engineers[request.form['username']]['role'] = request.form['role']
                        engineers[request.form['username']]['cases'] = []
                        engineers[request.form['username']]['leave'] = 0
                        myquery = {"date":datetime.datetime.today().strftime('%d-%m-%Y'),'shift':time,'freeze':0}
                        newvalues = {"$set": {"engineers":engineers}}
                        collection.update_one(myquery,newvalues)
                    return redirect(url_for('test'))# function name not endpoint name
                else:
                    flash("Invalid Password", 'log_msg')
                    return redirect(url_for('login'))
            else:
                error = "Invalid Credentials"
                flash(error, 'log_msg')
    return redirect(url_for('login'))  # function name of the /attendance ednpoint

@app.route('/logout',methods=['GET'])
def logout():
    time = ''
    if datetime.datetime.today().strftime('%p') == 'AM':
        time = 'Morning'
    elif datetime.datetime.today().strftime('%p') == 'PM':
        time = 'Night'
    username = session['username']
    shift_det = collection.find({"date": datetime.datetime.today().strftime('%d-%m-%Y'), 'shift': time, 'freeze': 0})
    shift_freeze = collection.find({"date": datetime.datetime.today().strftime('%d-%m-%Y'), 'shift': time, 'freeze': 1})
    if shift_freeze.count()>0:
        session['logged_in'] = False
        return login()
        # return redirect(url_for('test'))
    engineers = {}
    for i in shift_det:
        engineers = i['engineers']
    print(engineers)
    if engineers[username]:
        del engineers[username]
    myquery = {"date": datetime.datetime.today().strftime('%d-%m-%Y'), 'shift': time, 'freeze': 0}
    newvalues = {"$set": {"engineers": engineers}}
    collection.update_one(myquery, newvalues)
    session['logged_in'] = False
    flash(u'You were successfully logged  out!', 'log_msg')
    return login()

@app.route('/test', methods=['GET', 'POST'])
def test():
    #print(datetime.datetime.today().strftime('%d-%m-%Y %p'))
    time = ''
    x= ''
    if datetime.datetime.today().strftime('%p') == 'AM':
        time = 'Morning'
    elif datetime.datetime.today().strftime('%p') == 'PM':
        time = 'Night'
    shift_details = collection.find({"date": datetime.datetime.today().strftime('%d-%m-%Y'), 'shift': time})
    for i in shift_details:
        x = i['freeze']
    shift_details.rewind()
    if session['role']=='SL':
        http_response = render_template('index.html', shift_info=shift_details,freeze=x)
        return http_response
    return "Hi  " + session['username'] + " " + session['role'] + "<form action = 'logout' method = 'get'><input type='submit' value = 'Logout'/></form>"

@app.route('/freeze', methods=['GET', 'POST'])
def freeze():
    time = ''
    if datetime.datetime.today().strftime('%p') == 'AM':
        time = 'Morning'
    elif datetime.datetime.today().strftime('%p') == 'PM':
        time = 'Night'
    myquery = {"date": datetime.datetime.today().strftime('%d-%m-%Y'), 'shift': time, 'freeze': 0}
    newvalues = {"$set": {"freeze": 1}}
    collection.update_one(myquery, newvalues)
    return redirect(url_for('test'))

@app.route('/remsess', methods=['GET', 'POST'])
def remsess():
    session['logged_in'] = False
    flash(u'You were successfully logged  out!', 'log_msg')
    return login()

@app.route('/clearall',methods=['GET','POST'])
def clearall():
    print(session)
    #session.clear()
    return login()