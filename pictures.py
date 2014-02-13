#coding=utf-8

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship, backref
from accounts import User, UserInfo
from database import Base, db_session
from datetime import datetime

class Album(Base):
	"""docstring for Album"""
	__tablename__ = 'albums'
	id = Column(Integer,primary_key=True)
	user_id = Column(Integer,ForeignKey('users.id'))
	name = Column(String(50))
	place = Column(String(200))
	cover_id = Column(Integer)
	create_date = Column(DateTime)
	album_type = Column(String(20)) #photo个人照片, activity活动相册, avatar头像相册?, album个人相册？

	user = relationship('User',backref=backref('albums',lazy='dynamic'))
	#authority = Column(String(50)) #用户权限 仅好友可看／私密／公开

	def __init__(self, user_id, album_name, place,album_type, cover_id=3):# authority):
		self.user_id = user_id
		self.name = album_name
		self.place = place
		self.album_type = album_type
		self.cover_id = cover_id #默认相册封面 后应为形参中默认id1
		self.create_date = datetime.now()
		#self.authority = 0

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

	def __repr__(self):
		return '<Album %r>' %self.id #return the object

class Picture(Base):
	"""docstring for Picture"""
	__tablename__ = 'pictures'
	id = Column(Integer,primary_key=True)
	user_id = Column(Integer,ForeignKey('users.id'))
	album_id = Column(Integer,ForeignKey('albums.id'))
	pic_src = Column(String(200))
	pic_type = Column(String(20))
	description = Column(String(200))
	post_date = Column(DateTime)

	user = relationship("User", backref=backref('pics',lazy='dynamic'))
	album = relationship("Album", backref=backref('pics',lazy='dynamic'))

	def __init__(self, user_id, album_id, pic_src, pic_type, description=''):
		self.user_id = user_id
		self.album_id = album_id
		self.pic_src = pic_src
		self.pic_type = pic_type
		self.description = description
		self.post_date = datetime.now()

	def change_src(self, pic_src):
		self.pic_src = pic_src

	def get_picinfo(self):
		picinfo={
			'id':self.id,
			'uid':self.user_id,
			'uname':self.user.nickname,
			'ugender':self.user.gender,
			'date':self.post_date,
			'type':self.pic_type,
			'pic':self.pic_src,
			'description':self.description,
		}

		return picinfo

	def __repr__(self):
		return '<Picture %r>' %self.id #return the object

class News(Base):
	"""docstring for Picture"""
	__tablename__ = 'news'

	id = Column(Integer,primary_key=True)
	user_id = Column(Integer,ForeignKey('users.id'))
	pic_id = Column(Integer, ForeignKey('pictures.id'))
	news_type = Column(String(20)) #register, photo, activity, declaration, poster
	post_date = Column(DateTime)
	user_gender = Column(String(20))
	description = Column(String(100)) #xx加入了觅校缘， 发布了照片， 发布了活动， 更新了她的宣言，上传了活动照片

	user = relationship("User", backref=backref('usernews',lazy='dynamic'))
	picture = relationship("Picture", backref=backref('news',lazy='dynamic'))

	def __init__(self, user_id, pic_id, news_type, gender, description=''):
		self.user_id = user_id
		self.pic_id = pic_id
		self.news_type = news_type
		self.user_gender = gender
		self.post_date = datetime.now()
		self.description = description

	def _get_news(self):
		news = {
			'id':self.id,
			'uid':self.user_id,
			'uname':self.user.nickname,
			'ugender':self.user.gender,
			'date':self.post_date.strftime('%Y-%m-%d %H:%M:%S'),
			'type':self.news_type,
			'pic':self.picture.pic_src,
			'description':self.description
		}
		return news

	def __repr__(self):
		return '<AllNews %r>' %self.id #return the object	

class MiLetter(Base):
	"""docstring for Picture"""
	__tablename__ = 'miletters'
	id = Column(Integer,primary_key=True)
	sender_id = Column(Integer,ForeignKey('users.id'))
	receiver_id = Column(Integer)
	content = Column(String(400))
	send_date = Column(DateTime)
	read = Column(Integer) #是否已读 0为未读 1为已读

	user = relationship("User", backref=backref('usermsgs',lazy='dynamic'))

	def __init__(self, sender_id, receiver_id, content):
		self.sender_id = sender_id
		self.receiver_id = receiver_id
		self.content = content
		self.send_date = datetime.now()
		self.read = 0

	def get_letterinfo(self):
		msgs = {
			'from_id':self.sender_id,
			'from_name':self.user.nickname,
			'read':self.read,
			'msg':self.content,
		}
		return msgs

	def __repr__(self):
		return '<Letter %r>' %self.id #return the object





		