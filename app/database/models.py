from app import db
from datetime import datetime

class UploadedVideo(db.Model):
    videoid = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(400), unique=True)
    extension = db.Column(db.String(5))
    uploadStartedTime = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    uploadCompletedTime = db.Column(db.DateTime, index=True, default=datetime.utcnow)    
    totalduration = db.Column(db.String())
    analyticsFile = db.relationship('VideoAnalyticsFile', backref='videoAnalyticsFile', lazy='dynamic')
    generatedVideoFile = db.relationship('GeneratedVideo', backref='generatedVideo', lazy='dynamic')

    def __repr__(self):
        return "<UploadedVideo filename:{} uploadCompletedTime:{} >".format(self.filename,self.uploadCompletedTime)

class VideoAnalyticsFile(db.Model):
    analyticsfileid = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(400))
    createdTime = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    video_id = db.Column(db.Integer, db.ForeignKey('uploaded_video.videoid'))
    def __repr__(self):
        return '<VideoAnalyticsFile video_id:{}  filename:{} createdTime:{}  >'.format(self.video_id,self.filename,self.createdTime)

class GeneratedVideo(db.Model):
    gvideoid = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(400))
    createdTime = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    video_id = db.Column(db.Integer, db.ForeignKey('uploaded_video.videoid'))

    def __repr__(self):
        return '<GeneratedVideo gvideoid:{}  filename:{} createdTime:{} video_id >'.format(self.gvideoid,self.filename,self.createdTime.self.video_id)

########################### Merged AdCategory ###################################
# class MergedAdCategory(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     category_name = db.Column(db.String(100),nullable=False)
#     created_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#     last_modified_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    
#     adtitle = db.Column(db.String(500),nullable=False)
#     adbrand = db.Column(db.String(200))
#     adseller = db.Column(db.String(200))
#     adprice = db.Column(db.Numeric(12,2),nullable=False,default=0)
#     adimage_url = db.Column(db.String(500),nullable=False)
#     image_filename= db.Column(db.String(500))
#     adinitial_quantity = db.Column(db.Integer)
#     adleft_quantity = db.Column(db.Integer)
#     is_active = db.Column(db.Boolean, unique=False, default=True)

#     def __repr__(self):
#         return '<MergedAdCategory adcategoryid:{}  category_name:{} adtitle:{} adprice:{} createdTime:{}  >'.format(self.id,self.category_name,self.adtitle,self.adprice,self.createdTime) 

