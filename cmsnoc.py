from flask import Flask,render_template,make_response,request,redirect,url_for,Response,flash,session,abort,g
from flask_mail import Mail,Message
import flask
from io import StringIO
from functools import wraps
import urllib.parse
import random,os,subprocess,sys
import platform
import datetime
import urllib.request
import urllib.parse
from twilio.rest import Client
import time
import atexit
import logging
from apscheduler.schedulers.background import BackgroundScheduler
import pdfkit,codecs
from bson import ObjectId
from pymongo import MongoClient
import json
import urllib
#import win32api
#from email.mime.base import MIMEBase
from flask_mail import Mail,Message
from bson import json_util
import threading,jinja2

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

    for l in login_det:
        m[l['username']] = l['password']
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        if (request.form['username'] in m.keys()):
            if (m[request.form['username']] == request.form['password']):
                session['logged_in'] = True
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
    engineers = {}
    for i in shift_det:
        engineers = i['engineers']
    del engineers[username]
    myquery = {"date": datetime.datetime.today().strftime('%d-%m-%Y'), 'shift': time, 'freeze': 0}
    newvalues = {"$set": {"engineers": engineers}}
    collection.update_one(myquery, newvalues)
    session['logged_in'] = False
    flash(u'You were successfully logged  out!', 'log_msg')
    return login()

@app.route('/test', methods=['GET', 'POST'])
def test():
    #collection.insert({'student_id': 12345})
    print(datetime.datetime.today().strftime('%d-%m-%Y %p'))
    return "Hi  " + session['username'] + "<form action = 'logout' method = 'get'><input type='submit' value = 'Logout'/></form>"