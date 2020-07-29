import datetime
import requests
from flask import Flask,Blueprint,request,jsonify,make_response
from referral import app
from referral.creds import db
from referral.userFunction.uniqueIdGenerator import UniqueID
from passlib.hash import pbkdf2_sha256
from functools import wraps
from .algorithm.main import DriverFunction,createTree
api=Blueprint('api',__name__,url_prefix='/api')
#-------------------------DECORATOR-----------------------------
def apiAuth(f):
    @wraps(f)
    def inner_apiAuth(*args,**kwargs):
        key=request.args.get('api_key')
        if key is None:
            return jsonify({"message":"API key missing"}),403
        check_key=db.apiKeys.find_one({"API_KEY":key})
        if check_key:
            return f(*args,**kwargs)
        return jsonify({"message":"API key invalid"}),403
    return inner_apiAuth
#------------------------DECORATOR END---------------------------

#------------------------USER ROUTES-----------------------------
@api.route('/user',methods=['POST'])
@apiAuth
def addUser():
    username=request.json["username"]
    referrer=request.json["referrer"]
    password=request.json["password"]
    access_log=request.headers.get('X-Forwarded-For',request.remote_addr)
    access_agent=request.user_agent
    url='http://ip-api.com/json/'
    geo_location=requests.get(url.format(access_log)).json()
    password_hash=pbkdf2_sha256.hash(password)
    generatedId=str(UniqueID())
    try:
        log_entry=db.geo_logs.insert({'userID':generatedId,"logs":[
            {
                "geo_logs":geo_location,
                "datetime":datetime.datetime.utcnow()
            }
        ]})
    except Exception as exp:
        db.error_logs.insert({
            "userID":generatedId,
            "datetime":datetime.datetime.utcnow,
            "error":exp
        })
    tree=createTree(generatedId)
    init_user=db.users.insert({
        "username":username,
        "password":password_hash,
        "referralId":generatedId,
        "trees":tree,
        "wallet":0,
        "lastLogin":access_log,
        "datetime":datetime.datetime.utcnow(),
        "recent_agent":str(access_agent),
        "loginHistory":[]
    })
    if init_user:
        status=DriverFunction(generatedId,referrer)
        if status==True:
            return jsonify({"message":"success"}),200
        return jsonify({"message":"failure"}),400
    # return "success"

#-------------------GET ALL USER DATA----------------
@api.route('/user',methods=['GET'])
@apiAuth
def getUser():
    response=db.users.find()
    if response:
        output=[]
        for users_info in response:
            output.append(
                {
                    "username":users_info['username'],
                    "referralId":users_info['referralId'],
                    "trees":users_info['trees'],
                    "wallet":users_info['wallet'],
                    "lastLogin":users_info['lastLogin'],
                    "recent_agent":users_info['recent_agent'],
                    "loginHistory":users_info['loginHistory']
                }
            )
        return jsonify({"response":output}),200
    return jsonify({"message":"Something went wrong"}),400


#-------------------GET SPECIFIC USER DATA----------------
@api.route('/user/<id>',methods=['GET'])
@apiAuth
def getUserById(id):
    users_info=db.users.find_one({"referralId":id})
    output=[]
    if users_info:
        output.append(
            {
                "username":users_info['username'],
                "referralId":users_info['referralId'],
                "trees":users_info['trees'],
                "wallet":users_info['wallet'],
                "lastLogin":users_info['lastLogin'],
                "recent_agent":users_info['recent_agent'],
                "loginHistory":users_info['loginHistory']
            }
        )
        return jsonify({"response":output}),200
    return jsonify({"message":"Something went wrong"}),400


#-------------------GET ALL USER ACCESS LOGS-------------------
@api.route('/logs',methods=['GET'])
@apiAuth
def getLogs():
    response=db.geo_logs.find()
    if response:
        output=[]
        for users_info in response:
            output.append(
                {
                    "userID":users_info['userID'],
                    "logs":users_info['logs']
                }
            )
        return jsonify({"response":output}),200
    return jsonify({"message":"Something went wrong"}),400


#-------------------GET SPECIFIC USER ACCESS LOGS----------------
@api.route('/logs/<id>',methods=['GET'])
@apiAuth
def getLogsById(id):
    users_info=db.geo_logs.find_one({"userID":id})
    output=[]
    if users_info:
        output.append(
            {
                "userID":users_info['userID'],
                "logs":users_info['logs']
            }
        )
        return jsonify({"response":output}),200
    return jsonify({"message":"Something went wrong"}),400

#----------------------USER ROUTES END--------------------------



#--------------------API KEY GENERATION-------------------------
@api.route('/gen_token')
def gen_token():
    auth=request.authorization
    if auth:
        check_username=db.admins.find_one({"username":auth.username})
        if check_username:
            check_password=pbkdf2_sha256.verify(auth.password,check_username["password"])
            if check_password:
                unique=UniqueID()
                key='api_'+str(unique)
                db.apiKeys.insert({"API_KEY":key})
                return jsonify({"api_key":key}),200
    return make_response('Could not verify',401,{'WWW-Authenticate':'Basic realm="Login-Required"'})

#-------------------ADMIN MANAGEMENT-----------------------------
@api.route('/admin',methods=['POST'])
def admin():
    username=request.json["username"]
    password=request.json["password"]
    password_hash=pbkdf2_sha256.hash(password)
    status=db.admins.insert({"username":username,"password":password_hash})
    if status:
        return jsonify({"message":"success"}),200
    return jsonify({"message":"failure"}),400



    