import datetime
from flask import Flask,Blueprint
from referral.config import Development
from referral.creds import db

#APP INITIALIZATION
app=Flask(__name__)

#APP CONFIGURATIONS 
app.config.from_object(Development())

#BLUEPRINT REGISTER
from referral.routes import api
app.register_blueprint(api)

