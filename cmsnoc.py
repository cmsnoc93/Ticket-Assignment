from flask import Flask,render_template,request,redirect,url_for,Response,session
from flask_mail import Mail,Message
from pymongo import MongoClient
import json
import urllib
import threading,jinja2
# pip install dnspython required to resolve mongo IP

mongo = MongoClient('mongodb+srv://cmsnoc93:'+ urllib.parse.quote('cmsnoc@123') + '@cluster0-qxw77.mongodb.net/test?retryWrites=true&w=majority')
db = mongo.CMS_Automation
collection = db.Ticket_automation
app = Flask(__name__)

@app.route('/test', methods=['GET', 'POST'])
def test():
    collection.insert({'student_id': 12345})
    return "Hi"
