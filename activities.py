#coding=utf-8

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship, backref
from accounts import User, UserInfo
from database import Base, db_session
from datetime import datetime

class Activity(Base):
	"""docstring for Activity"""
	__tablename__ = 'activities'
	id = Column(Integer,primary_key=True)
	founder_id = Column(Integer,ForeignKey('users.id'))
	name = Column(String(50))
	place = Column(String(200))
	create_date = Column(DateTime)
	start_time = Column(Date)
	end_time = Column(Date)
	infomation=Column(String(500))
	poster_id = Column(Integer,ForeignKey('pictures.id')) #默认相册4
	album_id=Column(Integer,ForeignKey('albums.id'))
	activity_type=Column(String(20))
	cost=Column(String(20))

	user = relationship('User',backref=backref('activities',lazy='dynamic'))
	poster = relationship('Picture', backref=backref('activities'), lazy='dynamic')
	album = relationship('Album', backref=backref('albums'), lazy='dynamic')
	

	def __init__(self, founder_id, name, place, start_time, end_time, infomation, \
				 album_id, activity_type, poster_id=4, cost='免费'):
		self.founder_id = founder_id
		self.name = ame
		self.place = place
		self.start_time = start_time
		self.end_time = end_time
		self.infomation = infomation
		self.album_id = album_id
		self.activity_type = activity_type
		self.poster_id = poster_id 
		self.create_date = datetime.now()
'''
	def _get_album(self):
		pic = db_session.query(Picture).filter(Picture.id == self.cover_id).first()		
		albuminfo={
			'id':self.id,
			'uid':self.user_id,
			'uname':self.user.nickname,
			'ugender':self.user.gender,
			'date':self.create_date,
			'type':self.album_type,
			'pic':pic.pic_src,
			'description':self.place,
		}
		return albuminfo
'''
	def __repr__(self):
		return '<Activity %r>' %self.id #return the object