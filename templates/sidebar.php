<!--{eval $_TPL['nosidebar']=1;}-->

<html>
<head>
	<meta charset="UTF-8">
	<title>Find</title>
	<link type="image/x-icon" rel="shortcut icon" href="favicon.ico">
	<link type="text/css" rel="stylesheet" href="../static/css/style.css">
	<link type="text/css" rel="stylesheet" href="../static/css/sidebar.css">
</head>
<body>
	<div class="sidebar-banner"><img src="../static/img/carousel-bg2.jpg"></div>

	<div class="login-logo sidebar-login-logo">
		<div class="login-logo-bg"></div>
		<div class="login-logo-img">
			<img src="avatar/default.jpg">
		</div>
	</div>

		<!-- Controls -->
<div class="pull-left full-width" style="padding-top:70px;">
	<div class="border-bottom" style="height:25px;">
		<div class="pull-left" style="padding:2px 10px;color:#fff;background:#EDBD03">主页</div>
		<div class="pull-left" style="padding:2px 10px;">活动</div>
		<div class="pull-right" style="padding:2px 10px;">好友</div>
		<div class="pull-right" style="padding:2px 10px;">设置</div>
	</div>
</div>
<div class="sidebar-container">
	<div class="pull-left full-width">
		<h2 class="grey-color">宣言<small>Manifesto</small><small class="pull-right"><a>更新宣言</a></small></h2>
		<p class="text-center">树在，山在，我在，你还要怎样更好的世界。</p>
	</div>

	<div class="pull-left full-width">
		<h2 class="grey-color">相册<small>Photos</small><small class="pull-right"><a>+新建相册</a></small></h2>
		<div class="photo-album">
			<div class="album-cover"><img src="../static/img/album/0.jpg"></div>
			<div class="pull-left text-right full-width">音乐</div>
		</div>
		<div class="photo-album">
			<div class="album-cover"><img src="../static/img/album/1.jpg"></div>
			<div class="pull-left text-right full-width">2013欢乐多</div>
		</div>
	</div>

	<div class="pull-left full-width">
		<h2 class="grey-color pull-left full-width">活动<small>Activities</small><small class="pull-right"><a>发起活动</a></small></h2>
		<p class="pull-left full-width"><b class="main-color">cc</b>我参加了<a href="">古道徒步行</a>活动</p>
	</div>
</div>


<!--{if $_SGLOBAL['input_seccode']}-->
<script>
$('seccode').style.background = '#FFFFCC';
$('seccode').focus();
</script>
<!--{/if}-->

</div><!--container-->
<script type="text/javascript">
</script>
<!--{template footer}-->