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
from bson.binary import Binary
from bson.json_util import dumps
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

@app.route('/test', methods=['GET', 'POST'])
def test():
    collection.insert({'student_id': 12345})
    return "Hi"