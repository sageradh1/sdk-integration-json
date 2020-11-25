from flask import Flask
from datetime import timedelta

import os
from dotenv import load_dotenv

app = Flask(__name__)

#Loading environment from .startingenv
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')   # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

app.config["APP"] = os.getenv('FLASK_APP')
app.config["ENV"] = os.getenv('FLASK_ENV')

#Loading which configuration to use
if app.config["ENV"]=="development":
    app.config.from_object("config.DevelopmentConfig")
elif app.config["ENV"]=="testing":
    app.config.from_object("config.TestingConfig")
else:
    app.config.from_object("config.ProductionConfig")

print("The environment is : "+app.config["ENV"])

#Loading views
from app import json_api
