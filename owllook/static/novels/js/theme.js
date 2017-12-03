/*
Created By MSCSTSTS
2017年10月11日 14:13:13 UTC+8
*/


$(document).ready(function () {
	function theme(bg_color, bg_img, color , img){
		this.bg_color = bg_color;
		this.bg_img = bg_img;
		this.color = color;
		this.img = img;
	}


	/*-------------------初始化-------------------*/
	var base = [];

	base["http://qidian.gtimg.com/qd/images/read.qidian.com/body_base_bg.0.4.png"] = "../img/body_base_bg.0.4.png";
	base["http://qidian.gtimg.com/qd/images/read.qidian.com/basic_bg.0.4.png"] = "../img/basic_bg.0.4.png";
	base["http://qidian.gtimg.com/qd/images/read.qidian.com/theme/body_theme1_bg.0.4.png"] = "../img/body_theme1_bg.0.4.png";
	base["http://qidian.gtimg.com/qd/images/read.qidian.com/theme/theme_1_bg.0.4.png"] = "../img//theme_1_bg.0.4.png";
	base["http://qidian.gtimg.com/qd/images/read.qidian.com/theme/body_theme2_bg.0.4.png"] = "../img/body_theme2_bg.0.4.png";
	base["http://qidian.gtimg.com/qd/images/read.qidian.com/theme/theme_2_bg.0.4.png"] = "../img/theme_2_bg.0.4.png";
	base["http://qidian.gtimg.com/qd/images/read.qidian.com/theme/body_theme3_bg.0.4.png"] = "../img/body_theme3_bg.0.4.png";
	base["http://qidian.gtimg.com/qd/images/read.qidian.com/theme/theme_3_bg.0.4.png"] = "../img/theme_3_bg.0.4.png";
	base["http://qidian.gtimg.com/qd/images/read.qidian.com/theme/body_theme5_bg.0.4.png"] = "../img/body_theme5_bg.0.4.png";
	base["http://qidian.gtimg.com/qd/images/read.qidian.com/theme/theme_5_bg.0.4.png"] = "../img/theme_5_bg.0.4.png";

	var mise = new theme("rgb(237, 231, 218)", base["http://qidian.gtimg.com/qd/images/read.qidian.com/body_base_bg.0.4.png"],"rgba(0, 0, 0, 0)" ,base["http://qidian.gtimg.com/qd/images/read.qidian.com/basic_bg.0.4.png"] );    //米色
	var maihuang=new theme("rgb(224, 206, 158)" ,base["http://qidian.gtimg.com/qd/images/read.qidian.com/theme/body_theme1_bg.0.4.png"] ,"rgb(243, 233, 198)" ,base["http://qidian.gtimg.com/qd/images/read.qidian.com/theme/theme_1_bg.0.4.png"] ); //麦黄
	var yaqing = new theme("rgb(205, 223, 205)" , base["http://qidian.gtimg.com/qd/images/read.qidian.com/theme/body_theme2_bg.0.4.png"],"rgb(226, 238, 226)" ,base["http://qidian.gtimg.com/qd/images/read.qidian.com/theme/theme_2_bg.0.4.png"] );//雅青
	var hulan = new theme("rgb(207, 221, 225)" ,base["http://qidian.gtimg.com/qd/images/read.qidian.com/theme/body_theme3_bg.0.4.png"] ,"rgb(226, 239, 243)" ,base["http://qidian.gtimg.com/qd/images/read.qidian.com/theme/theme_3_bg.0.4.png"] );//湖蓝
	var danfen = new theme("rgb(235, 206, 206)","none" ,"rgb(245, 228, 228)" ,"none" );//淡粉
	var wuhui = new theme( "rgb(208, 208, 208)",base["http://qidian.gtimg.com/qd/images/read.qidian.com/theme/body_theme5_bg.0.4.png"] , "rgb(220, 220, 220)",base["http://qidian.gtimg.com/qd/images/read.qidian.com/theme/theme_5_bg.0.4.png"] );//雾灰


	var bg_target = $("body");
	var target = $("body > div.container.all-content");
	var setting = $("body > div.container.all-content > div.left-bar-list > div:nth-child(2)");
	var content = $($(".show-content").children("*").get(0));
	$("body").append('<div id="helper"><div class="theme"><div class="color mise" theme-data="mise"></div><div class="color maihuang" theme-data="maihuang"></div><div class="color yaqing" theme-data="yaqing"></div><div class="color hulan" theme-data="hulan"></div><div class="color danfen" theme-data="danfen"></div><div class="color wuhui" theme-data="wuhui"></div></div><div class="font"><button id="helper-font-minus">A-</button><div id="helper-font-size">16px</div><button id="helper-font-plus">A+</button></div><div class="family"><button id="yahei">雅黑</button><button id="songti">宋体</button><button id="kaiti">楷书</button></div></div><div class="layer"></div>');
	$("body").append('<style>#helper{margin:0;padding:20px 0;position:fixed;left:12%;left:-moz-calc(12% + 60px);left:-webkit-calc(12% + 60px);left:calc(12% + 60px);top:193px;width:240px;background-color:#eee;z-index:100;display:none}.theme{background-color:rgba(255.255.255.0.6);width:100%;height:40px}.color{width:30px;height:30px;border-radius:15px;float:left;margin:4px;border:1px gray solid;transition:all .5s}.color:hover{border:1px white solid}.mise{background-color:#ede7da}.maihuang{background-color:#e0ce9e}.yaqing{background-color:#cddfcd}.hulan{background-color:#cfdde1}.danfen{background-color:#ebcece}.wuhui{background-color:#d0d0d0}.font,.family{width:100%;height:40px;text-align:center;padding:0 15px;margin:10px 0;-webkit-touch-callout:none;-webkit-user-select:none;-khtml-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select:none}.font div{width:70px;height:40px;border:0;float:left;background-color:#888;line-height:40px;font-size:25px;color:#fff}.font button,.family button{outline:0;width:70px;height:40px;border:1px gray solid;float:left;background-color:#eee;line-height:40px;font-size:24px;color:#666;transition:all .25s}.font button:hover,.family .act{background-color:#666;color:#eee}.layer{top:0px;left:0px;background-color:rgba(0,0,0,0);position:fixed;z-index:99;width:100%;height:100%;display:none}.yahei{font-family:STHeiti,"Microsoft YaHei",HelveticaNeue-Light,"Helvetica Neue Light",sans-serif!important}.songti{font-family:PingFangSC-Regular,"-apple-system",Simsun,STSong,STFangsong!important}.kaiti{font-family:Kaiti,STKaiti!important}@media(max-width:767px){.left-bar-list{display:block !important;height:60px;width:100%;left:0;top:71px;position:absolute}.left-bar-flag{width:25%;float:left;text-align:center;background:none !important;background-color:rgba(242,238,230,0.58) !important;border-top-color:rgba(0,0,0,0.1) !important;border-top-style:solid !important;border-top-width:1px}.left-bar-flag>a{margin:0 auto}body>div.container.all-content{margin-top:81px !important;}.footer>nav{position:relative !important;bottom:0}#helper{position:fixed;left:12%;left:-moz-calc(50% - 120px);left:-webkit-calc(50% - 120px);left:calc(50% - 120px);top:20%;margin:0 auto}.layer{background-color:rgba(0,0,0,0.4)}}</style>');
	/*-------------------初始化-------------------*/

	var arr = [];
	arr["mise"]=mise;
	arr["maihuang"]=maihuang;
	arr["yaqing"]=yaqing;
	arr["hulan"]=hulan;
	arr["danfen"]=danfen;
	arr["wuhui"]=wuhui;
	var ff = [];
	ff['"Microsoft YaHei"']="yahei";
	ff["Microsoft YaHei"]="yahei";
	ff["Simsun"]="songti";
	ff['"Simsun"']="songti";
	ff["Kaiti"]="kaiti";
	ff['"Kaiti"']="kaiti";
	ff["yahei"]="Microsoft YaHei";
	ff["songti"]="Simsun";
	ff["kaiti"]="Kaiti";
	ff[""]="yahei";

	function Forcr_css(tar,att1,data1,data2){
		tar.css("cssText", att1+": url("+data2+") "+data1+"!important;");
	}
	function set_font(num){
		//console.log(num);
		//console.log("font-size:"+(fz-(-num))+"px !important;");
		content.css("cssText", "font-size: "+num+"px !important;");
		refresh_font_size();
		window.localStorage["theme-font-size"]=num;
	}
	function set_font_family(ff){
		content.removeClass("songti");
		content.removeClass("kaiti");
		content.removeClass("yahei");
		content.addClass(ff);
		 //content.css("cssText", "font-family: "+ff+" !important;");
		refresh_font_family();
		window.localStorage["theme-font-family"]=ff;
	}


	function refresh_font_size(){
		$("#helper-font-size").text(content.css("font-size"));
		return parseInt(content.css("font-size"));
	}
	function refresh_font_family(){
		bright_font_family(content.attr("class"));
		//console.log(content.css("font-family"));
		return ff[content.css("font-family")];
	}
	function bright_font_family(ff){
		$("#helper div.family button").removeClass("act");
		$("#"+ff).addClass("act");
	}
	function change_Theme(theme){
		Forcr_css(bg_target,"background",theme.bg_color,theme.bg_img);
		var href =""+ window.location.href;
		if(href.indexOf("/chapter?")>0){
			Forcr_css($("#maininfo"),"background",theme.color,theme.img);
			Forcr_css($("#list > dl"),"background",theme.color,theme.img);
			Forcr_css($("div.container.all-chapter > div.inner > dl.chapterlist"),"background",theme.color,theme.img);
			Forcr_css($(" #at"),"background",theme.color,theme.img);
			Forcr_css($("div>dl"),"background",theme.color,theme.img);
			Forcr_css($("table"),"background",theme.color,theme.img);
			Forcr_css($("dl"),"background",theme.color,theme.img);
			Forcr_css($("ul"),"background",theme.color,theme.img);
		 }
		else{
			Forcr_css(target,"background",theme.color,theme.img);
		}
		target.css("box-shadow","0 0 8px 1px rgba(100,100,100,0.4)");
	}
	$(document).ready(function(){
		if("undefined" == typeof localStorage["theme-color"]){
		}
		else{
			change_Theme(arr[localStorage["theme-color"]]);
		}
		if("undefined" == typeof localStorage["theme-font-size"]){
		}
		else{
			set_font(localStorage["theme-font-size"]);
		}
		if("undefined" == typeof localStorage["theme-font-family"]){
		}
		else{
			set_font_family(localStorage["theme-font-family"]);
		}



		setting.click(function(){
			event.preventDefault();
			/** Show Div**/
			$("#helper").toggle();
			$(".layer").toggle();
			refresh_font_size();
			refresh_font_family();
		});
		$("div.color").click(function(e){
			change_Theme(arr[$(this).attr("theme-data")]);
		   window.localStorage["theme-color"] = $(this).attr("theme-data");
		});
		$("#helper-font-minus").click(function(){
			set_font((parseInt(refresh_font_size())-(1)));
		});
		$("#helper-font-plus").click(function(){
			set_font((parseInt(refresh_font_size())-(-1)));
			//console.log("+1");
		});
		$("#songti").click(function(){
			set_font_family("songti");
		});
		$("#yahei").click(function(){
			set_font_family("yahei");
		});
		$("#kaiti").click(function(){
			set_font_family("kaiti");
		});
		$(".layer").click(function(){
			$("#helper").hide();
			$(".layer").hide();
		});
	});
});