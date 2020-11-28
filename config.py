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

    API_BASE_URL = "http://127.0.0.1:5000"
    DB_NAME = os.getenv('DEV_DB_NAME')
    DB_USERNAME = os.getenv('DEV_DB_USERNAME')
    DB_PASSWORD = os.getenv('DEV_DB_PASSWORD')
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('DEV_DB_USERNAME')}:{os.getenv('DEV_DB_PASSWORD')}@localhost/{os.getenv('DEV_DB_NAME')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(Config):
    # TODO
    DEBUG = True

    # API_BASE_URL = ""
    DB_NAME = os.getenv('TEST_DB_NAME')
    DB_USERNAME = os.getenv('TEST_DB_USERNAME')
    DB_PASSWORD = os.getenv('TEST_DB_PASSWORD')
    # SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('TEST_DB_USERNAME')}:{os.getenv('TEST_DB_PASSWORD')}@someip/{os.getenv('TEST_DB_NAME')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


