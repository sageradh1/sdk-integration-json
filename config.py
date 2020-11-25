import secrets
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
        
    ADIMAGE_UPLOADS_FOLDER = basedir+ "/app/static/img/ad-images"
    VIDEO_UPLOADS_FOLDER =  basedir+"/app/static/video/uploaded"
    VIDEO_GENERATED_FOLDER =  basedir+"/app/static/video/generated"
    VIDEOANALYTICS_GENERATED_FOLDER =  basedir+"/app/static/analyticsFolder/generated"
    THUMBNAIL_FOR_UPLOADED_VIDEO_FOLDER = basedir+"/app/static/img/generated/thumbnails"
    
    MAX_VIDEO_FILESIZE = 100 * 1024 * 1024 #max allowed video filesize is 16MB
    
    BASE_URL_WITH_PORT = "http://asmi.co"
    
    ALLOWED_VIDEO_EXTENSIONS = set(['mp4', 'mkv'])
    
    SESSION_COOKIE_SECURE = True


class DevelopmentConfig(Config):
    DEBUG = True
    
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_SQLALCHEMY_DATABASE_URI')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DB_NAME = os.getenv('DEV_DB_NAME')
    DB_USERNAME = os.getenv('DEV_DB_USERNAME')
    DB_PASSWORD = os.getenv('DEV_DB_PASSWORD')

    SESSION_COOKIE_SECURE = False
