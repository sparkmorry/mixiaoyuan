需要安装的Python框架／库：
$pip install Flask
$pip install Flask-SQLAlchemy

1. 先在本地数据库创建表mi，按utf8编码形式（重要！）
create database mi DEFAULT CHARACTER SET utf8;

2. 运行run.py文件即可
再打开127.0.0.1:5000
如果有出现问题，就先运行一下database.py，再运行mi.py

当前进度：
http://www.mixiaoyuan.com/ 配置在士权服务器上的网站
http://www.mixiaoyuan.test/ 配置在阿里云上的网站

添删接口的数据现在都直接写在函数里模拟了，比如

#删除照片
@app.route('/api/picture/delete', methods=['GET','POST'])
def delete_pic():
	#pic_id= request.args.get('pic_id', 0, type=str)
	pic_id=4
	userid = 1

换成＃里的语句就直接获取请求的数据了

database.py accounts.py pictures.py都是用SQLALchemy写的数据库对象
templetes里的页面都不是最新的