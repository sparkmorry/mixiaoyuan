#coding=utf-8
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship, backref
from database import Base, db_session
from datetime import datetime

GRADE_DICT={1:'大一', 2:'大二', 3:'大三',4:'大四',5:'大五', 6:'研一',7:'研二',8:'研三',9:'博士及以上',10:'已毕业'}

class User(Base):
	__tablename__ = 'users'
	id = Column(Integer,primary_key=True)
	usermail = Column(String(120), unique=True, nullable=False)
	_password = Column("password", String(80), nullable=False)
	nickname = Column(String(80))
	gender=Column(String(20))
	register_date = Column(DateTime)
	
	def __init__(self, usermail,password,nickname, gender):
		self.usermail = usermail
		self._password = password
		self.gender = gender
		self.nickname = nickname
		self.registerdate = datetime.now()

	def _validaccount(self, usermail, password):
		if usermail == self.usermail:
			if password == self._password:
				return True
			else:
				return False

	def __repr__(self):
		return '<User %r>' %self.nickname #return the object

class UserInfo(Base):
	"""docstring for UserInfo"""
	__tablename__ = 'userinfos'
	id = Column(Integer,primary_key=True)
	user_id = Column(Integer,ForeignKey('users.id'))
	gender = Column(String(20)) #female, male
	avatar_id = Column(Integer)
	photo_id = Column(Integer)
	has_photo = Column(Boolean) #人工验证，0为没有，1为有
	grade = Column(Integer) #0无 1开始查找字典
	campus = Column(String(20))
	major = Column(String(20))
	status = Column(String(20))
	interest_tags = Column(String(200))
	personality_tags = Column(String(200))
	declaration = Column(String(200))

	realname = Column(String(20))
	birthday = Column(Date)
	constellation = Column(String(20))
	home_province = Column(String(20))
	home_city = Column(String(20))
	blood_type = Column(String(20))
	height = Column(Integer)
	weight = Column(Integer)
	phone = Column(String(50))
	email = Column(String(50))

	realname_pub = Column(Boolean)
	birthday_pub = Column(Boolean)
	constellation_pub = Column(Boolean)
	home_pub = Column(Boolean)
	height_pub = Column(Boolean)
	weight_pub = Column(Boolean)
	phone_pub = Column(Boolean)
	email_pub = Column(Boolean)

	user = relationship("User", backref=backref('userinfo',lazy='dynamic'))
	#picture = relationship("Picture", backref=backref('pics',lazy='dynamic'))

	
	def __init__(self, user_id, gender, grade=0, campus='', major='', status='', \
				interest='', personality='', name='',birthday='1900-01-01', constellation='', \
				home_province='',home_city='', blood_type='', height=0, weight=0, phone='', email='', \
				realname_pub=False, birthday_pub=False, constellation_pub=False, home_pub=False, blood_pub=False,\
				height_pub=False, weight_pub=False, phone_pub=False, email_pub=False):
		self.user_id = user_id
		self.gender = gender
		self.grade = grade
		self.campus = campus
		self.major = major
		self.status = status
		self.interest_tags = interest #以逗号分割
		self.personality_tags = personality
		self.realname = name
		self.birthday = birthday
		self.constellation = constellation
		self.home_province = home_province
		self.home_city = home_city
		self.blood_type = blood_type
		self.height = height
		self.weight = weight
		self.phone = phone
		self.email = email
		self.realname_pub = realname_pub
		self.birthday_pub = birthday_pub
		self.constellation_pub=constellation_pub
		self.home_pub=home_pub
		self.height_pub=height_pub
		self.weight_pub=weight_pub
		self.phone_pub=phone_pub
		self.email_pub=email_pub

	#无法更新性别和宣言
	def _update(self, user_id, grade=0, campus='', major='', status='', \
				interest='', personality='', name='',birthday='', constellation='', \
				home_province='',home_city='', blood_type='', height=0, weight=0, phone='', email='', \
				realname_pub=False, birthday_pub=False, constellation_pub=False, home_pub=False,\
				blood_pub=0, height_pub=False, weight_pub=False, phone_pub=False, email_pub=False):
		self.user_id = user_id
		self.grade = grade
		self.campus = campus
		self.major = major
		self.status = status
		self.interest_tags = interest #以逗号分割
		self.personality_tags = personality
		self.realname = name
		self.birthday = birthday
		self.constellation = constellation
		self.home_province = home_province
		self.home_city = home_city
		self.blood_type = blood_type
		self.height = height
		self.weight = weight
		self.phone = phone
		self.email = email
		self.realname_pub = realname_pub
		self.birthday_pub = birthday_pub
		self.constellation_pub=constellation_pub
		self.home_pub=home_pub
		self.height_pub=height_pub
		self.weight_pub=weight_pub
		self.phone_pub=phone_pub
		self.email_pub=email_pub
	

	def _getuserinfo(self):
		
		photo_src = ''
		avatar_src = ''
		pics = self.user.pics	
		for pic in pics:
			if pic.pic_type == "photo":
				photo_src = pic.pic_src
			if pic.pic_type == "avatar":
				avatar_src = pic.pic_src

		userinfo={

			'user_id':self.user_id,
			'gender':self.gender,
			'photo_src':photo_src,
			'avatar_src':avatar_src,
			'grade':GRADE_DICT.get(self.grade,0),
			'major':self.major,
			'love':self.status,
			'interest-tag':self.interest_tags,
			'character-tag':self.personality_tags,
			'love-declaration':self.declaration,
			'real-name':self.realname,
			'birthday':str(self.birthday),
			'constellation':self.constellation,
			'province':self.home_province,
			'city':self.home_city,
			'blood':self.blood_type,
			'height':self.height,
			'weight':self.weight,
			'phone':self.phone,
			'mail':self.email,

		}

		return userinfo

	def _change_declaration(self, declaration=''):
		self.declaration = declaration

	def change_photo(self, photo_id):
		self.photo_id=photo_id

	def change_avatar(self, avatar_id):
		self.avatar_id=avatar_id

	#计算简单搜索匹配度，传入的均为序列类型，如：expected_campus为一组期望校区序列，expected_grade为最小年级和最大年级的序列
	def simple_matching_degree(self, expected_campus, expected_grade, expected_personality, \
								expected_interest, expected_gender):
		simple_matching_degree = 0
		match_tag = 0

		if(self.gender == expected_gender):
			#如果校区不限则直接加20，否则在期望的校区中查找有没有当前用户所在校区
			if expected_campus == '不限':
				simple_matching_degree += 100/5
			else:
				for campus in expected_campus:
					if(self.campus == campus):
						simple_matching_degree += 100/5

			if(self.grade >= expected_grade[0] and self.grade <= expected_grade[1]):
				simple_matching_degree += 100/5

			this_user_personality = self.personality_tags.split(',')
			for personality in expected_personality:
				for this_personality in this_user_personality:
					if(this_personality == personality):
						match_tag += 1

			simple_matching_degree += 1.0*match_tag/len(expected_personality)*100/5

			match_tag = 0
			this_user_interest = self.interest_tags.split(',')
			for interest in expected_interest:
				for this_interest in this_user_interest:
					if(this_interest == interest):
						match_tag += 1
			
			simple_matching_degree += 1.0*match_tag/len(expected_interest)*100/5	
		else:
			simple_matching_degree = -1
		return int(simple_matching_degree), self	

	#计算简单搜索匹配度，传入的均为序列类型，如：expected_campus为一组期望校区序列，expected_grade为最小年级和最大年级的序列
	def advance_matching_degree(self, expected_campus, expected_grade, expected_personality, expected_interest, \
								expected_birthday,expected_gender, expected_province, expected_city,\
								expected_height):
		advance_matching_degree = 0
		match_tag = 0

		if(self.gender == expected_gender):
			#如果校区不限则直接加20，否则在期望的校区中查找有没有当前用户所在校区
			if expected_campus == '不限':
				advance_matching_degree += 100/8
			else:
				for campus in expected_campus:
					if(self.campus == campus):
						advance_matching_degree += 100/8

			if(self.grade >= expected_grade[0] and self.grade <= expected_grade[1]):
				advance_matching_degree += 100/8

			this_user_personality = self.personality.split(',')
			for personality in expected_personality:
				for this_personality in this_user_personality:

					if(this_personality == personality):
						match_tag += 1

			advance_matching_degree += 1.0*match_tag/len(expected_personality)*100/8

			match_tag = 0
			this_user_interest = self.interest.split(',')
			for interest in expected_interest:
				for this_interest in this_user_interest:
					if(this_interest == interest):
						match_tag += 1
			
			#print match_tag
			advance_matching_degree += 1.0*match_tag/len(expected_interest)*100/8

			print self.birthday.year

			if(self.birthday.year >= expected_birthday[0] and self.birthday.year <= expected_birthday[1]):
				advance_matching_degree += 100/8

			if expected_province == self.home_province:
				advance_matching_degree += 50/16

			if expected_city == self.home_city:
				advance_matching_degree += 50/16

			if(self.height >= expected_height[0] and self.height <= expected_height[1]):
				advance_matching_degree += 100/8
		else:
			advance_matching_degree = -1
		return int(advance_matching_degree), self	



	def __repr__(self):
		return '<UserInfo %r>' %self.user_id #return the object

class TAInfo(Base):
	__tablename__ = 'TAinfos'
	user_id = Column(Integer,primary_key=True)
	TA_grade_start = Column(String(20))
	TA_grade_end = Column(String(20))
	TA_birthyear_start = Column(Integer)
	TA_birthyear_end = Column(Integer)
	TA_height_start = Column(Integer)
	TA_height_end = Column(Integer)
	TA_campus = Column(String(120))
	TA_province = Column(String(20))
	TA_city = Column(String(20))

	def __init__(self, userid,TA_grade_start, TA_grade_end, TA_birthyear_start, TA_birthyear_end, \
				 TA_height_start, TA_height_end, TA_campus, TA_province, TA_city):
		self.user_id = userid
		self.TA_grade_start = TA_grade_start
		self.TA_grade_end = TA_grade_end
		self.TA_birthyear_start = TA_birthyear_start
		self.TA_birthyear_end = TA_birthyear_end
		self.TA_height_start = TA_height_start
		self.TA_height_end = TA_height_end
		self.TA_campus = TA_campus
		self.TA_province = TA_province
		self.TA_city = TA_city

	def _update(self, userid,TA_grade_start, TA_grade_end, TA_birthyear_start, TA_birthyear_end, \
				 TA_height_start, TA_height_end, TA_campus, TA_province, TA_city):
		#super(User, self).__init__()
		self.user_id = userid
		self.TA_grade_start = TA_grade_start
		self.TA_grade_end = TA_grade_end
		self.TA_birthyear_start = TA_birthyear_start
		self.TA_birthyear_end = TA_birthyear_end
		self.TA_height_start = TA_height_start
		self.TA_height_end = TA_height_end
		self.TA_campus = TA_campus
		self.TA_province = TA_province
		self.TA_city = TA_city

	def __repr__(self):
		return '<TAInfo %r>' %self.user_id #return the object