window.onload = function(){
	MyBlog.select(1);
	PRouter.bind('s', function(value){
		MyBlog.hidePage();
		MyBlog.select(value);
	});
	PRouter.bind('p', function(value){
		MyBlog.showPage(value);
	});
	PRouter.bind('cat', function(value){
		MyBlog.closePage('ignore');
		MyBlog.sortWithKV('cat', value);
	});
	PRouter.bind('tag', function(value){
		MyBlog.closePage('ignore');
		MyBlog.sortWithKV('tag', value);
	});
	PRouter.bind('date', function(value){
		MyBlog.closePage('ignore');
		MyBlog.sortWithKV('date', value);
	});
	MyBlog.addListener4Click();
	MyBlog.loadList(function(){
		PRouter.start();
	});
	$('#container').scroll(function() {
		if (this.scrollTop > 200) {
			$('.go-top').fadeIn(200);
		} else {
			$('.go-top').fadeOut(200);
		}
		if (this.scrollTop + this.clientHeight == this.scrollHeight){
			setTimeout(function(){
				if (_('container').scrollTop + _('container').clientHeight == _('container').scrollHeight) {
					MyBlog.initWithContent();
				};
			}, 500);
		}
	});
	$('.go-top').click(function(event) {
		event.preventDefault();
		if (PRouter.get('p')) {
			$('#showPage').animate({scrollTop: 0}, 600);
		}else $('.container').animate({scrollTop: 0}, 600);
	});
};
function _(id){
	return document.getElementById(id);
}
window.MyBlog = {
		BlogName: '觅校缘',
		pCount: 0,
		pList: {},
		sortCount: {
			cat: {},
			tag: {},
			date: {}
		},
		selected: '',
		addListener4Click: function(){
			PRouter.bindForTag();
			/*MyBlog._bind4Click('.tab', function(){
				PRouter.remove(['cat', 'tag', 'date'], 'ignore');
				PRouter.set('s', this.id.substring(3));
			});*/
			MyBlog._bind4Click('.close', function(){
				MyBlog.closePage();
			});
			MyBlog._bind4Click('.cat-label', function(){
				PRouter.remove(['tag', 'date'], 'ignore');
				PRouter.set('cat', this.innerHTML);
			});
			MyBlog._bind4Click('.tag-label', function(){
				PRouter.remove(['cat', 'date'], 'ignore');
				PRouter.set('tag', this.innerHTML);
			});
			MyBlog._bind4Click('.date-label', function(){
				PRouter.remove(['cat', 'tag'], 'ignore');
				PRouter.set('date', this.innerHTML.substring(0, 7));
			});
			MyBlog._bind4Click('.all-p-btn', function(){
				MyBlog._listAllP();
			});
			MyBlog._bind4Click('.news-item', function(){
				$(this.children[0].children[0]).animate({right: '0'}, 100);
			}, 'onmouseover');
			MyBlog._bind4Click('.news-item', function(){
				$(this.children[0].children[0]).animate({right: '100%'}, 100);
			}, 'onmouseout');
		},
		select: function(count){
			var n = count || 1;
			if (MyBlog.selected) {
				_('page' + MyBlog.selected).style.display = 'none';
				_('tab' + MyBlog.selected).className = 'tab';
				_('tab' + n).className = 'tab selected';
				_('page' + n).style.display = 'inline';
			}else{
				_('tab' + n).className = 'tab selected';
				_('page' + n).style.display = 'inline';
				setTimeout(function(){
					_('container').className += ' animation';
				}, 1);
			}
			MyBlog.selected = n;
		},
		loadList: function(callback){
			if (window.pList) {
				MyBlog.pList = eval('(' + pList + ')');
				MyBlog.initWithContent();
				if (callback) callback();
			}else{
				$.getJSON('/p.json', function(data){
					MyBlog.pList = data;
					MyBlog.initWithContent();
					if (callback) callback();
				});
			}
		},
		initWithContent: function(){
			for (var item in MyBlog.pList) {
				var cat = MyBlog._generateLabel(MyBlog.pList[item].cat, 'cat', 'init'); // true for count
				var tag = MyBlog._generateLabel(MyBlog.pList[item].tag, 'tag', 'init');
				var inner = MyBlog._generateSummary(item);
				_('indexList').innerHTML += inner;
				MyBlog.pCount++;

				if(!MyBlog.sortCount['date'][MyBlog.pList[item].date.substring(0, 7)]) MyBlog.sortCount['date'][MyBlog.pList[item].date.substring(0, 7)] = 0;
				MyBlog.sortCount['date'][MyBlog.pList[item].date.substring(0, 7)]++;
			};
			_('pCountInfo').innerHTML = '<b><a class="all-p-btn">全部文章</a></b>(' + MyBlog.pCount + ')';
			_('catInfo').innerHTML = MyBlog._generateLabelInfo('cat');
			_('tagInfo').innerHTML = MyBlog._generateLabelInfo('tag');
			_('listKey').innerHTML = '全部文章：';
			MyBlog.addListener4Click();

			$('#indexList').imagesLoaded(function() {
				// Prepare layout options.
				var options = {
					autoResize: true, // This will auto-update the layout when the browser window is resized.
					container: $('#mainRightCol'), // Optional, used for some extra CSS styling
					offset: 10, // Optional, the distance between grid items
				};
				
				// Get a reference to your grid items.
				var handler = $('#indexList li');
				
				// Call the layout function.
				handler.wookmark(options);
			});
		},
		_listAllP :function(){
			_('indexList').innerHTML = '';
			PRouter.remove(['cat', 'tag', 'date']);
			for (var item in MyBlog.pList) {
				var inner = MyBlog._generateSummary(item);
				_('indexList').innerHTML += inner;
			};
			_('listKey').innerHTML = '全部文章：';
			_('listValue').innerHTML = '';
			MyBlog.addListener4Click();
		},
		sortWithKV: function(key, value){
			PRouter.set('s', '1', 'replace');
			switch(key){
				case 'cat':
					_('listKey').innerHTML = '分类：';
				break;
				case 'tag':
					_('listKey').innerHTML = '标签：';
				break;
				case 'date':
					_('listKey').innerHTML = '日期：';
					value = value.substring(0, 7);
				break;
				default:
					_('listKey').innerHTML = key;
			}
			_('listValue').innerHTML = value;
			_('indexList').innerHTML = '';

			for (var item in MyBlog.pList) {
				if (MyBlog._inArray(MyBlog.pList[item][key], value) || (typeof(MyBlog.pList[item][key]) == 'string' && value == MyBlog.pList[item][key].substring(0, 7))) {
					var inner = MyBlog._generateSummary(item);
					_('indexList').innerHTML += inner;
				}
			};
			MyBlog.addListener4Click();
		},
		showPage: function(item){
			$('#dark').fadeIn();
			setTimeout(function(){
				$('#dark').hide();
			}, 500);
			_('showContainer').style.left = 0;/*
			document.title = MyBlog.pList[item].title + ' | ' + MyBlog.BlogName;
			var cat = MyBlog._generateLabel(MyBlog.pList[item].cat, 'cat');
			var tag = MyBlog._generateLabel(MyBlog.pList[item].tag, 'tag');
			var inner = '\
			<a class="close">&lt;&lt;返回</a>\
			<div class="text-left">\
				<p><b>标题:</b></p>\
				<p>' + MyBlog.pList[item].title + '</p>\
				<p><b>日期：</b></pre>\
				<a class="date-label">' + MyBlog.pList[item].date + '</a>\
				<p><b>分类:</b></p>' + cat + '\
				<p><b>标签:</b></p>' + tag + '\
			</div>';
			_('pInfo').innerHTML = inner;
			MyBlog.addListener4Click();

			var title = MyBlog.pList[item].title;
			var pId = item;
			var url = 'http://www.imsun.net/?p=' + pId;

			$('#dark').fadeIn();
			_('showContainer').style.left = 0;
			_('pContent').innerHTML = '文章加载中...';
			_('pComment').innerHTML = '评论加载中...';

			var el = document.createElement('div');
			el.setAttribute('data-thread-key', pId);
			el.setAttribute('data-url', url);
			try{
				DUOSHUO.EmbedThread(el);
				setTimeout(function(){
					_('pComment').innerHTML = '';
					$('#pComment').append(el);
					el = null;
				}, 500);
			}catch(e){
				_('pComment').innerHTML = '<p style="color:red">评论加载失败</p>';
			}
			if (sessionStorage.getItem('p=' + item)) {
				_('pContent').innerHTML = sessionStorage.getItem('p=' + item);
				$('pre code').each(function(i, e) {hljs.highlightBlock(e)});
			}else{
				$.get(MyBlog.pList[item].url, function(data){
					var inner = '<h2>' + MyBlog.pList[item].title + '</h2><p>日期：' + MyBlog.pList[item].date + ' 作者：<a href="http://www.imsun.net/" target="_blank">Trevor Sun</a></p>' + data + '<h5 class="text-center">—— 原文来自<a href="http://www.imsun.net/?p=' + item + '" target="_blank">孙士权的博客</a>，转载请注明作者及出处 ——</h5>';
					_('pContent').innerHTML = inner;
					sessionStorage.setItem('p=' + item, inner);
					$('pre code').each(function(i, e) {hljs.highlightBlock(e)});
				});
			}*/
		},
		closePage: function(opt){
			document.title = MyBlog.BlogName;
			PRouter.remove('p', opt);
			_('showContainer').style.left = '100%';
			$('#dark').show();
			setTimeout(function(){
				$('#dark').fadeOut();
			}, 300);
			setTimeout(function(){
				_('pContent').innerHTML = '';
				_('pComment').innerHTML = '';
			}, 500);
		},
		hidePage: function(){
			_('showContainer').style.left = '100%';
			setTimeout(function(){
				$('#dark').fadeOut();
			}, 300);
		},
		_inArray: function(a, element){
			for (var i = 0; i < a.length; i++) {
				if (a[i] == element) return true;
			};
			return false;
		},
		_generateSummary: function(item){
			var cat = MyBlog._generateLabel(MyBlog.pList[item].cat, 'cat'); // true for count
			var tag = MyBlog._generateLabel(MyBlog.pList[item].tag, 'tag');
			var inner = 
			'<div>\
				<h2><a title="' + MyBlog.pList[item].title + '" href="?p=' + item + '" url-opt="push" target="_blank">' + MyBlog.pList[item].title + '</a></h2>\
				<p>\
					By: Trevor Date: \
					<a class="date-label">' + MyBlog.pList[item].date + '</a> \
					<b>分类: </b><a class="cat-label">' + cat + '</a> \
					<b>标签: </b>' + tag +
				'</p>\
			</div>';
			inner = '<li class="news-item"><a href="?p=sdfsdf" url-opt="push"><label class="news animation">' + MyBlog.pList[item].news + '</label><img width=150 src="' + MyBlog.pList[item].avatar + '"></a></li>';
			return inner;
		},
		_generateLabel: function(a, key, count){
			var ans = '';
			if (a == 'none') return '无';
			for (var i = 0; i < a.length; i++) {
				if(count == 'init') {
					if(!MyBlog.sortCount[key][a[i]]) MyBlog.sortCount[key][a[i]] = 0;
					MyBlog.sortCount[key][a[i]]++;
				}
				if (count == 'count') {
					ans += '<a class="' + key + '-label">' + a[i] + '</a>(' + MyBlog.sortCount[key][a[i]] + ') ';
				}else ans += '<a class="' + key + '-label">' + a[i] + '</a> ';
			};
			return ans;
		},
		_generateLabelInfo: function(key){
			var ans = '';
			for (var item in MyBlog.sortCount[key]){
				ans += '<a class="' + key + '-label">' + item + '</a>(' + MyBlog.sortCount[key][item] + ') ';
			}
			return ans;
		},
		_bind4Click: function(selector, callback, event){
			var ev = event || 'onclick';
			$(selector).each(function(i, e){
				if (!e[ev]) {
					e[ev] = callback;
				};
			})
		}
}