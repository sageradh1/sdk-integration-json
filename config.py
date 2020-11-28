import secrets
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False

    ADIMAGE_POSTER_INJECTION_UPLOADS_FOLDER = basedir+ "/app/static/image/posterinjection/ad-images"
    VIDEO_POSTER_INJECTION_UPLOADS_FOLDER =  basedir+"/app/static/video/posterinjection/uploaded"
    VIDEO_POSTER_INJECTION_GENERATED_FOLDER =  basedir+"/app/static/video/posterinjection/generated"
    VIDEOANALYTICS_POSTER_INJECTION_GENERATED_FOLDER =  basedir+"/app/static/analyticsFolder/posterinjection/generated"
    
    MAX_VIDEO_FILESIZE = 16 * 1024 * 1024 #max allowed video filesize is 16MB
    
    ALLOWED_VIDEO_EXTENSIONS = set(['mp4', 'mkv'])

class DevelopmentConfig(Config):
    DEBUG = True

    # TODO SHOULD BE PASSED FROM ENV VARIRABLE LATER
    # SQLALCHEMY_DATABASE_URI = os.getenv('DEV_SQLALCHEMY_DATABASE_URI')
    # DB_NAME = os.getenv('DEV_DB_NAME')
    # DB_USERNAME = os.getenv('DEV_DB_USERNAME')
    # DB_PASSWORD = os.getenv('DEV_DB_PASSWORD')
    
    SQLALCHEMY_DATABASE_URI = "postgresql://sdkgroup:sdkpassword123@localhost/sdk_db"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

