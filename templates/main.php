<!doctype html>
<html>
<head>
	<meta charset="utf-8">
	<link type="image/x-icon" rel="shortcut icon" href="logo.png">
	<title>觅校缘</title>
	<link rel="stylesheet" href="css/googlecode.css">
	<link rel="stylesheet" type="text/css" href="css/style.css">
</head>
<body>

	<div class="show-bg"></div>
	<img id="leftBtn" class="left-btn" src="/img/me.png">
	<iframe src="sidebar.php" id="leftCol" class="left-col-bar"></iframe>
<div id="rightCol" class="right-col-bar">
	<a class="go-top">▲ Go Top</a>
	<div id="dark"></div>
	<div id="showContainer" class="container animation">
		<div class="header">
			<img class="logo" src="/img/logo2.png">
			<img class="banner" src="/img/banner.png">
			<ul class="nav">
				<li class="tab"><a href="?s=1" url-opt="push">首页</a></li>
				<li class="tab"><a href="?s=1" url-opt="push">觅女神</a></li>
				<li class="tab"><a href="?s=3" url-opt="push">觅活动</a></li>
				<li class="tab"><a href="?s=4" url-opt="push">消息</a></li>
			</ul>
		</div>
		<div id="showPage" class="page">
			<div class="content">
				<div class="left-col">
					<a class="close">&lt;&lt;返回</a>
					<div class="btn pull-left full-width">加为好友</div>
					<div class="btn pull-left full-width">站内私信</div>
					<div id="pInfo"></div>
					<div id="pShare">
					</div>
				</div>
				<div id="showPageRight" class="right-col">
					<img src="avatar/0.jpg" class="pull-left" style="width:200px;height:300px;margin-right:20px;">
					<div class="pull-left">
						<h1 class="grey-color" style="padding:0;margin:0">锌燃</h1>
						<p>树在，山在，我在，你还要怎样更好的世界。</p>
						<br><br>
						<p>浙江大学，计算机学院，研一</p>
						<p>生日：1990.10.25</p>
						<p>星座：天秤座</p>
						<p>家乡：山东省菏泽市</p>
						<p><a>更多详细资料...</a></p>
					</div><br>
					<div class="full-width pull-left">
						<h1 class="grey-color">最新动态<small>News</small></h1>
						<p>再嫁不出去就成剩女了 TAT</p>
						<p>
							<div class="pull-left"><a href="">评论</a>(5)<a href="">赞</a>(12)</div>
							<div class="text-right">2013-9-12 @银泰城</div>
						</p>
						<hr>
						<p><a>点击查看更多···</a></p>
						<hr>
					</div>
					<div class="full-width pull-left">
						<h1 class="grey-color">她的活动<small>Activities</small></h1>
						<div class="pull-left half-width" style="width:49%;padding-right:1%;">
							<h2 class="grey-color">她发起的</h2>
							<hr>
							<p class="text-center">她有点内向，还没有发起过活动哟</p>
						</div>
						<div class="pull-left" style="width:49%;padding-left:1%;">
							<h2 class="grey-color">她参与的</h2>
							<hr>
							<p class="text-center">她有点内向，还没有参与过活动哟</p>
						</div>
					</div>
					<div class="full-width pull-left">
						<h1 class="grey-color">她的相册<small>Photos</small></h1>
						<div class="photo-album">
							<div class="album-cover"><img src="album/0.jpg"></div>
							<div class="pull-left text-right full-width">音乐</div>
						</div>
					</div>
					<div id="pContent"></div>
					<div id="pComment"></div>
				</div>
			</div>
		</div>
	</div>
	<div id="container" class="container">

		<div class="header">
			<img class="logo" src="/img/logo2.png">
			<img class="banner" src="/img/banner.png">
			<ul class="nav">
				<li class="tab"><a href="?s=1" url-opt="push">首页</a></li>
				<li class="tab"><a href="?s=1" url-opt="push">觅女神</a></li>
				<li class="tab"><a href="?s=3" url-opt="push">觅活动</a></li>
				<li class="tab"><a href="?s=4" url-opt="push">消息</a></li>
			</ul>
		</div>
		<div id="page1" class="page">
			<div class="content">
				<div class="left-col" style="padding-top: 100px;">
					<div class="find-block">
						<h1 class="grey-color"><a href="?s=1" url-opt="push">人 <small>FIND PEOPLE</small></a></h1>
						<h1 class="grey-color"><a href="?s=3" url-opt="push"><small>FIND THINGS</small> 事</a></h1>
					</div>
				</div>
				<div id="mainRightCol" class="right-col">
					<div style="display:none">
						<div id="pCountInfo">
						</div>
						<div class="pull-left half-width">
							<h4>分类：</h4>
							<p id="catInfo"></p>
						</div>
						<div class="pull-left half-width">
							<h4>标签：</h4>
							<p id='tagInfo'></p>
						</div>
						<p><b id="listKey">全部文章：</b><label id="listValue"></label></p>
					</div>
					<h1 class="grey-color border-bottom">最新动态<small class="pull-right"><a href="?p=random" url-opt="push">随便看看&gt;&gt;</a></small></h1>
					<ul id="indexList" class="title-list">
					</ul>
				</div>
			</div>
		</div>
		<div id="page2" class="page">
			<div class="content">
				<div class="left-col" style="padding-top: 100px;">
					<div class="find-block">
						<h1 class="grey-color"><a href="?s=1" url-opt="push">人 <small>FIND PEOPLE</small></a></h1>
						<h1 class="grey-color"><a href="?s=3" url-opt="push"><small>FIND THINGS</small> 事</a></h1>
					</div>
				</div>
				<div id="mainRightCol" class="right-col">
					<div style="display:none">
						<div id="pCountInfo">
						</div>
						<div class="pull-left half-width">
							<h4>分类：</h4>
							<p id="catInfo"></p>
						</div>
						<div class="pull-left half-width">
							<h4>标签：</h4>
							<p id='tagInfo'></p>
						</div>
						<p><b id="listKey">全部文章：</b><label id="listValue"></label></p>
					</div>
					<h1 class="grey-color border-bottom">觅女神<small class="pull-right"><a href="?p=random" url-opt="push">随便看看？</a></small></h1>
					<div style="margin:0 auto;width:270px"><input style="width:140px;height:33px;"><label class="btn" style="height:10px;background:#EDBD03;padding-left:20px;padding-right:20px;">搜索</label></div>
				</div>
			</div>
		</div>
		<div id="page3" class="page">
			<div class="content">
				<div class="left-col" style="padding-top: 100px;">
					<div class="find-block">
						<h1 class="grey-color"><a href="?s=1" url-opt="push">人 <small>FIND PEOPLE</small></a></h1>
						<h1 class="grey-color"><a href="?s=3" url-opt="push"><small>FIND THINGS</small> 事</a></h1>
					</div>
				</div>
				<div id="mainRightCol" class="right-col">
					<div style="display:none">
						<div id="pCountInfo">
						</div>
						<div class="pull-left half-width">
							<h4>分类：</h4>
							<p id="catInfo"></p>
						</div>
						<div class="pull-left half-width">
							<h4>标签：</h4>
							<p id='tagInfo'></p>
						</div>
						<p><b id="listKey">全部文章：</b><label id="listValue"></label></p>
					</div>
					<h1 class="grey-color border-bottom">热门活动<small class="pull-right"><a href="?p=random" url-opt="push">随便看看&gt;&gt;</a></small></h1>
					<div class="pull-left" style="width: 300px; height:300px; margin-right: 20px;">
						<div class="pull-left half-width text-center" style="overflow:hidden"><img src="album/0.jpg" style="height:100%;"></div>
						<div class="pull-left half-width" style="position:relative;left: 10px;">
							<h4><a href="">不插电音乐会</a></h4>
							<br><br><br><br><br>
							时间：2013-8-31<br>
							地点：浙江大学永谦205
						</div>
					</div>
					<div class="pull-left" style="width: 300px; height:300px; margin-right: 20px;">
						<div class="pull-left half-width text-center" style="overflow:hidden"><img src="album/0.jpg" style="height:100%;"></div>
						<div class="pull-left half-width" style="position:relative;left: 10px;">
							<h4><a href="">不插电音乐会</a></h4>
							<br><br><br><br><br>
							时间：2013-8-31<br>
							地点：浙江大学永谦205
						</div>
					</div>
					<div class="pull-left" style="width: 300px; height:300px; margin-right: 20px;">
						<div class="pull-left half-width text-center" style="overflow:hidden"><img src="album/0.jpg" style="height:100%;"></div>
						<div class="pull-left half-width" style="position:relative;left: 10px;">
							<h4><a href="">不插电音乐会</a></h4>
							<br><br><br><br><br>
							时间：2013-8-31<br>
							地点：浙江大学永谦205
						</div>
					</div>
					<div class="pull-left" style="width: 300px; height:300px; margin-right: 20px;">
						<div class="pull-left half-width text-center" style="overflow:hidden"><img src="album/0.jpg" style="height:100%;"></div>
						<div class="pull-left half-width" style="position:relative;left: 10px;">
							<h4><a href="">不插电音乐会</a></h4>
							<br><br><br><br><br>
							时间：2013-8-31<br>
							地点：浙江大学永谦205
						</div>
					</div>
				</div>
			</div>
		</div>
	</div><!--container-->
</div><!--rightCol-->
<div id="tab1"></div><div id="tab2"></div><div id="tab3"></div>
<script>var duoshuoQuery = {short_name:"imsun"}</script>
<script src="http://static.duoshuo.com/embed.js"></script>
<script src="js/prouter.js"></script>
<script src="js/jquery.min.js"></script>
<script src="js/highlight.pack.js"></script>
<script>hljs.initHighlightingOnLoad();</script>
<script type="text/javascript" src="js/jquery.wookmark.min.js"></script>
<script src="http://code.ciaoca.com/jquery/wookmark/demo/js/jquery.imagesloaded.js"></script>
<script src="js/main.js"></script>
<!-- Baidu Button BEGIN -->
<script type="text/javascript" id="bdshare_js" data="type=slide&amp;img=0&amp;pos=right&amp;uid=6858101" ></script>
<script type="text/javascript" id="bdshell_js"></script>
<script type="text/javascript">
var bds_config={"bdTop":179};
document.getElementById("bdshell_js").src = "http://bdimg.share.baidu.com/static/js/shell_v2.js?cdnversion=" + Math.ceil(new Date()/3600000);
</script>
<!-- Baidu Button END -->
<script>
_('leftBtn').onclick = function slideRight(){
	_('leftCol').style.left = '0';
	_('rightCol').style.left = '30%';
	_('rightCol').style.width = '100%';
	_('leftBtn').style.left = '30%';
}
_('rightCol').onclick = function slideLeft(){
	_('leftCol').style.left = '0';
	_('rightCol').style.left = '0';
	_('rightCol').style.width = '100%';
	_('leftBtn').style.left = '0';
}
</script>
</body>
</html>