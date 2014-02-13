#coding=utf-8
from flask import Flask, session, url_for, redirect, render_template, flash, request,jsonify, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import or_, and_
from database import db_session #数据库session, 用于操作数据库，如db_session.add(u), db_session.commit()
from accounts import User, UserInfo, TAInfo
from pictures import News, Picture, Album, MiLetter
import hashlib
import sys
import os
import Image
from werkzeug import secure_filename
reload(sys)
sys.setdefaultencoding('utf-8')

from datetime import datetime
import encodings.utf_8
import re #正则表达式

#如果需要初始化数据库请取消注释
#from database import init_db
#init_db()

app = Flask(__name__)

UPLOAD_FOLDER="static/pictures/"
PHOTO_FOLDER="static/photo/"
AVATAR_FOLDER="static/avatar/"

PHOTO_WIDTH=1024

ALLOWED_EXTENSIONS=set(['jpg','png','gif','bmp','jpeg','JPG', 'JPEG', 'PNG'])

def checklogin():
	if 'has_login' in session and 'userid' in session and 'password' in session:
		this_user = User.query.filter_by(id = session['userid']).first()
		pwd = session['password']
		for user in User.query.all():
			if(user.id == this_user.id):
				if(user._password == pwd):
					session['userid'] = this_user.id
					session['gender'] = this_user.gender
					session['username'] = this_user.nickname
					session['error'] = None					
				else:
					session['error'] = "请重新登陆-密码错误"
	else:
		session['error'] = "请先登陆"
	return session['error']

#验证图片文件类型
def allowed_pic(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.teardown_appcontext
def shutdown_session(exception=None):
	db_session.remove()

#注册页面函数
@app.route('/register',methods=['GET','POST'])
def register():
	if 'error' not in session:
		session['error']=None
	if request.method=='POST':
		new_user_email = request.form['email'] + request.form['mail-type']
		if re.match("^.+\\@(zju.edu.cn|st.zju.edu.cn)$", new_user_email) != None:
			print 'yes'
			for user in User.query.all(): #查询所有User对象里是否有该用户email
				if new_user_email == user.usermail:
					session['error']='该邮箱已经被注册'
					error=session['error']       
					session.pop('error',None)					
					return render_template('account/register.html',error=error)

			if len(request.form['pwd'])>5: #验证密码大于5位
				nickname = request.form['nickname']
				password = hashlib.md5(request.form['pwd']).hexdigest()
				newuser=User(new_user_email,password,nickname,request.form['gender'])
				db_session.add(newuser) #执行数据库操作
				db_session.commit()
				session['has_login']=True
				session['userid']=User.query.filter_by(usermail=new_user_email).first().id  #保存userid
				session['username']=request.form['nickname']
				session['password']=password
				session['gender']=request.form['gender']
				#photo_src = PHOTO_FOLDER + "default.jpg"
				new_userinfo = UserInfo(session['userid'],request.form['gender'])
				db_session.add(new_userinfo)
				db_session.commit()
				flash('successfully registered')
				print session['gender']
				session.pop('error',None)
				return render_template('account/register-success.html')                
			else:
				session['error']='密码小于5位，请重新填写'
		else:
			session['error'] = '请使用zju邮箱进行注册'

	error=session['error']       
	session.pop('error',None)    #释放error键
	return render_template('account/register.html',error=error)

#登陆页面函数
@app.route('/login', methods=['GET','POST'])
def login():
	error = None #开始无错误可在页面根据{% if error == None %} 来判断
	#umail = request.args.get('usermail', 0, type=str)
	#pwd = request.args.get('password', 0, type=str)
	umail= '3100102592@zju.edu.cn'
	pwd='123456'
	print pwd, umail
	if request.method == 'POST':
		for user in User.query.all():
			if(user.usermail == umail):
				#if user._validaccount(umail, hashlib.md5(pwd).hexdigest()):
				if user._validaccount(umail, pwd):
					session['has_login'] = True  #标记已经登陆
					session['username']=user.nickname #记录用户昵称显示
					session['password']=user._password #纪录用户密码
					session['gender']=user.gender #记录用户性别
					session['userid']=user.id #纪录用户ID
					flash("successfully login")
					return redirect(url_for('index'))
				else:
					session['error'] = '密码错误' #密码错误

		if 'error' not in session:
			session['error'] = "该帐户不存在"
	if 'error' in session:
		error = session['error']
		session.pop('error',None)
	return render_template('account/login.html',error=error)

#退出函数
@app.route('/logout')
def logout():
	session.pop('has_login', None)
	session.pop('userid',None)
	session.pop('username',None)
	session.pop('gender',None)
	session.pop('password',None)
	flash('You were logged out')
	return redirect(url_for('login'))

#在UserInfo表中查询是否有该用户id
def userinfo_exist(user_id):
	for userinfo in UserInfo.query.all(): 
		if user_id == userinfo.user_id:
			return True
	return False

#在TAInfo表中查询是否有该用户id
def TAinfo_exist(user_id):
	for TAinfo in TAInfo.query.all(): 
		if user_id == TAinfo.user_id:
			return True
	return False

#填写用户资料页函数 
@app.route('/userinfo', methods=['GET','POST'])
def userinfo():
	error=None
	error = checklogin()
	#this_user_id = session['userid']
	this_user_id = 1

	if request.method=='POST':
		#在UserInfo表中查询是否有该用户id，有则更新，无则插入
		if userinfo_exist(this_user_id):
			this_user_info = db_session.query(UserInfo).filter(UserInfo.user_id==this_user_id).first()

			photo_id = this_user_info.photo_id
			avatar_id = this_user_info.avatar_id

			#更新用户资料
			this_user_info._update(this_user_id, request.form['grade'], request.form['campus'],\
						request.form['major'],request.form['love'],request.form['interest-tag'],\
						request.form['character-tag'], request.form['real-name'],request.form['birthday'],\
						request.form['constellation'],request.form['province'], request.form['city'], \
						request.form['blood'],request.form['height'],request.form['weight'], \
						request.form['phone'], request.form['mail'],request.form['real-name-open'],\
						request.form['birthday-open'], request.form['constellation-open'],request.form['home-open'],\
						request.form['blood-open'], request.form['height-open'], request.form['weight-open'],\
						request.form['phone-open'],request.form['mail-open'])

			this_user_TAinfo = db_session.query(TAInfo).filter(TAInfo.user_id==this_user_id).first()
			this_user_TAinfo._update(this_user_id,request.form['TA-grade-s'],request.form['TA-grade-e'],\
								request.form['TA-brthd-s'],request.form['TA-brthd-e'],request.form['TA-height-s'],\
								request.form['TA-height-e'], request.form['TA-compus'], request.form['TA-province'],\
								request.form['TA-city'])
			db_session.commit()
			return redirect(url_for('index')) 			

		else:
			this_user_info = UserInfo(this_user_id, 'female', request.form['grade'], \
							request.form['campus'],request.form['major'],request.form['love'],\
							request.form['interest-tag'],request.form['character-tag'], request.form['real-name'],\
							request.form['birthday'],request.form['constellation'],request.form['province'], \
							request.form['city'], request.form['blood'],request.form['height'],\
							request.form['weight'], request.form['phone'], request.form['mail'],\
							request.form['real-name-open'],request.form['birthday-open'], \
							request.form['constellation-open'],request.form['home-open'],\
							request.form['blood-open'], request.form['height-open'], request.form['weight-open'],\
							request.form['phone-open'],request.form['mail-open'])
			db_session.add(this_user_info)	

			TAinfo=TAInfo(this_user_id, request.form['TA-grade-s'],request.form['TA-start-e'],\
				request.form['TA-brthd-s'],request.form['TA-brthd-e'],
				request.form['TA-height-s'],request.form['TA-height-e'], request.form['TA-compus'],\
				request.form['TA-province'],request.form['TA-city'])
			db_session.add(TAinfo)
			db_session.commit()
			return redirect(url_for('index')) 

	if 'error' in session:
		result = session['error']
		session.pop('error',None)
	#print this_user_info
	return render_template('account/user.html', error=error) #, userinfo=this_user_info, TAinfo=this_user_TAinfo)

#主页
@app.route('/')
def index():
	return render_template('index.html')

#获取用户资料函数，每次修改用户资料之前先获取
@app.route('/api/user/info', methods=['GET','POST'])
def get_userinfo():
	userid = request.args.get('uid', 0, type=str)
	#userid=2
	error=None
	error = checklogin()
	#userid=session['userid']
	if(db_session.query(UserInfo).filter(UserInfo.user_id==userid).first()):
		this_user = db_session.query(UserInfo).filter(UserInfo.user_id==userid).first()
		print "this_user.id"
		userinfo = this_user._getuserinfo()
		return jsonify(data=userinfo, error=error)

#修改宣言函数
@app.route('/api/user/signature', methods=['GET','POST'])
def set_signature():
	signature = request.args.get('signature', 0, type=str)
	#signature="只愿得一人心，白首不分离"
	userid = 1
	error=None
	error = checklogin()

	#修改宣言
	this_user_info = db_session.query(UserInfo).filter(UserInfo.user_id==userid).first()
	this_user_info._change_declaration(signature)
	pic_id = this_user_info.photo_id

	#发布到新鲜事
	news = News(this_user_info.user_id, pic_id,'declaration', this_user_info.gender, '修改了TA的宣言')
	db_session.add(news)
	db_session.commit()
	if 'error' in session:
		result = session['error']
		session.pop('error',None)
	else:
		error = ''

	return jsonify(error=error)

@app.route('/api/user/search', methods=['GET','POST'])
def search_TA():
	interest_tag = ['看书','画画','编程']
	personality_tag = ['开朗','中二','闷骚']
	grade =[4,7]
	expected_gender='female'
	campus = ['紫金港','玉泉']
	photo = 1

	simple_matching_users = []
	for userinfo in UserInfo.query.all():
		print userinfo.id
		simple_matching_degree, matched_user = userinfo.simple_matching_degree(campus, grade,\
											 personality_tag, interest_tag, expected_gender)
		if not simple_matching_degree == -1:
			MU=matched_user._getuserinfo()
			myarr=['simple_matching_degree',simple_matching_degree]
			MU[myarr[0]]=myarr[1]
			simple_matching_users.append(MU)

	SMU=sorted(simple_matching_users,\
		key=(lambda simple_matching_users:simple_matching_users['simple_matching_degree']),reverse=True)
	if 'error' in session:
		result = session['error']
		session.pop('error',None)
	else:
		error = ''
	return jsonify(data=SMU, err=error)


#删除新鲜事
@app.route('/api/news/delete', methods=['GET','POST'])
def delete_news():
	#news_id= request.args.get('id', 0, type=str)
	news_id=1
	userid = 1
	error=None
	error = checklogin()

	#删除新鲜事
	if (db_session.query(News).filter(News.id==news_id).first()):
		this_news = db_session.query(News).filter(News.id==news_id).first()
		db_session.delete(this_news)
		db_session.commit()
	else:
		session['error'] = "该新鲜事不存在"

	if 'error' in session:
		result = session['error']
		session.pop('error',None)
	else:
		error = ''

	return jsonify(error=error)

#获取新鲜事
@app.route('/api/news/get', methods=['GET','POST'])
def get_news():
	error=None
	error = checklogin()
	#sort = request.args.get('sort', 0, type=str)
	#uid = request.args.get('uid', 0, type=str)
	item_id = request.args.get('item_id', 0, type=int)
	#item_id=0
	allnew = News.query.all()
	allnews = []
	for news in allnew:
		newsinfo = news._get_news()
		allnews.append(newsinfo)

	if 'error' in session:
		result = session['error']
		session.pop('error',None)
	else:
		error = ''
	return jsonify(date=allnews[item_id:], error=error)
 
#新建相册 需要加入封面设置
@app.route('/api/album/set', methods=['GET','POST'])
def set_album(): 
	this_user_id=1
	album_name='西藏游'
	place = "西藏"
	album_type ="album"
	error=None
	error = checklogin()
	if album_name:
		if not place:
			album_place = ""
		else:
			album_place = place

		if not os.path.isdir(ALBUM_FOLDER+str(this_user_id)):
			os.makedirs(ALBUM_FOLDER+str(this_user_id))

		new_album = Album(this_user_id, album_name, place, album_type)
		db_session.add(new_album)
		db_session.commit()
		os.makedirs(ALBUM_FOLDER+str(this_user_id)+"/"+str(new_album.id))
		#创建成功

	else:
		session['error'] = "请填写相册名称"

	if 'error' in session:
		result = session['error']
		session.pop('error',None)
	return jsonify(error=error)

#获取相册信息
@app.route('/api/album/get', methods=['GET','POST'])
def get_album(): 
	this_user_id=1
	error=None
	error = checklogin()
	
	this_user = db_session.query(User).filter(User.id==this_user_id).first()
	albums = this_user.albums
	data=[]
	for album in albums:
		albuminfo = album._get_album()
		data.append(albuminfo)

	if 'error' in session:
		result = session['error']
		session.pop('error',None)
	else:
		error = ''
	return jsonify(data=data, error=error)

#删除相册
@app.route('/api/album/delete', methods=['GET','POST'])
def delete_album(): 
	album_id=4
	error=None
	error = checklogin()
	
	if (db_session.query(Album).filter(Album.id==album_id).first()):
		this_album =db_session.query(Album).filter(Album.id==album_id).first()
		if this_album.user_id == session['userid']:
			db_session.delete(this_album)
			db_session.commit()
		else:
			session['error'] = "对不起，您没有该权限"
	else:
		session['error'] = "该相册不存在"

	if 'error' in session:
		result = session['error']
		session.pop('error',None)
	else:
		error = ''
	return jsonify(error=error)

#添加照片
@app.route('/api/picture/set', methods=['GET', 'POST'])
def upload_pic():
	error=None
	error = checklogin()

	#this_user_id = session['userid']
	#this_user_gender = session['gender']
	this_user_id=1
	album_id=request.args.get('album_id', 0, type=int)
	description = ""
	#pic_type = 'photo'
	pic_type = request.args.get('pic_type', 0, type=str)
	this_user_gender = 'female'

	if request.method=='POST':
		if request.files['file']:
			upload_picture = request.files['file']
			file_name = upload_picture.filename #获取图片文件名称	
			print upload_picture
			pic_tmp = Image.open(upload_picture)
			pic_size=pic_tmp.size

			#如果图片太大进行一点压缩到1024*X
			if (pic_tmp.size[0]>PHOTO_WIDTH):
				height=PHOTO_WIDTH*pic_tmp.size[1]/pic_tmp.size[0]
				size=PHOTO_WIDTH,height
				upload_picture=pic_tmp.resize(size)
			else:
				upload_picture = pic_tmp
				
			print file_name
			if album_id:
				
				upload_album_id = album_id

				if allowed_pic(file_name):	
					if not description:  #获取图片描述
						description=""
					else:
						description = description

					new_picture=Picture(this_user_id, upload_album_id, '', pic_type, description)
					db_session.add(new_picture)
					db_session.commit()
					if pic_type == 'photo':
						description = "更新了头像"
						this_user=db_session.query(UserInfo).filter(UserInfo.user_id == this_user_id).first()
						this_user.change_photo(new_picture.id)
						db_session.commit()
						picture_path = PHOTO_FOLDER

					elif pic_type == 'album':
						description = "上传了新的照片"
						picture_path = UPLOAD_FOLDER
					elif pic_type == 'avatar':
						picture_path = AVATAR_FOLDER

					file_name = str(new_picture.id)+'.jpg'
					picture_path = picture_path+file_name
					upload_picture.save(picture_path,"JPEG")
					picture = db_session.query(Picture).filter(Picture.id==new_picture.id).first()
					picture_path = "/"+picture_path
					picture.change_src(picture_path) 
					db_session.commit()
					#发布新鲜事
					news = News(this_user_id, new_picture.id, pic_type, this_user_gender, description)
					db_session.add(news)
					db_session.commit()

					if pic_type == 'avatar':
						this_user=db_session.query(UserInfo).filter(UserInfo.user_id == this_user_id).first()
						this_user.change_avatar(new_picture.id)
						db_session.commit()
							
				else:
					session['error'] = "请选择正确的图片文件, 我们仅支持jpg,png,gif,bmp,jpeg几种格式"
			else:
				session['error'] = "请选择相册"
		else:
			session['error'] = "请上传图片"
		if 'error' in session:
			error = session['error']
			session.pop('error',None)
		else:
			error=''
		return jsonify(error=error)
	return render_template('album/uploadphoto.html')

#删除照片
@app.route('/api/picture/delete', methods=['GET','POST'])
def delete_pic():
	#pic_id= request.args.get('pic_id', 0, type=str)
	pic_id=4
	userid = 1
	error=None
	error = checklogin()

	#删除照片
	if (db_session.query(Picture).filter(Picture.id==pic_id).first()):

		this_pic = db_session.query(Picture).filter(Picture.id==pic_id).first()
		if this_pic.user_id == session['userid']:
			db_session.delete(this_pic)
			db_session.commit()
		else:
			session['error'] = "对不起，您没有该权限"
	else:
		session['error'] = "该照片不存在"

	if 'error' in session:
		result = session['error']
		session.pop('error',None)
	else:
		error = ''

	return jsonify(error=error)

#获取照片
@app.route('/api/picture/get', methods=['GET','POST'])
def get_pic():
	error=None
	error = checklogin()
	album_id=1
	this_album = db_session.query(Album).filter(Album.id==album_id).first()
	pics = this_album.pics
	data=[]
	for pic in pics:
		picinfo = pic.get_picinfo()
		data.append(picinfo)

	if 'error' in session:
		result = session['error']
		session.pop('error',None)
	else:
		error = ''
	return jsonify(data=data, error=error)

#检测有无新消息
@app.route('/api/message/check', methods=['GET', 'POST'])
def check_message():
	error=None
	userid=2
	error = checklogin()
	letters = MiLetter.query.filter(and_(MiLetter.receiver_id==userid,MiLetter.read==0)).all()
	count = len(letters)

	if 'error' in session:
		result = session['error']
		session.pop('error',None)
	else:
		error = ''	
	return jsonify(count=count, err=error)

#写觅信
@app.route('/api/message/send', methods=['GET','POST'])
def send_letter_to():
	error=None
	error = checklogin()
	receiverid=2
	userid = 1
	content = "dsjahsja"

	new_miletter = MiLetter(userid, receiverid, content)
	db_session.add(new_miletter)
	db_session.commit()
	return jsonify(err=error)

@app.route('/api/message/get', methods=['GET','POST'])
def read_letter():
	error=None
	error = checklogin()
	userid = 2
	letters = MiLetter.query.filter(or_(MiLetter.receiver_id==userid,MiLetter.sender_id==userid)).all()
	data=[]
	for letter in letters:
		letterinfo = letter.get_letterinfo()
		data.append(letterinfo)

	if 'error' in session:
		result = session['error']
		session.pop('error',None)
	else:
		error = ''
	return jsonify(data=data, error=error)	

app.secret_key = 'SPARKMORRY'
if __name__ == '__main__':
	app.run(debug=True)
