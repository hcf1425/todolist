$(function(){

	// 打开登录框
	$('.login_btn').click(function(){
        $('.login_form_con').show();
	})
	
	// 点击关闭按钮关闭登录框或者注册框
	$('.shutoff').click(function(){
		$(this).closest('form').hide();
	})

    // 隐藏错误
    $(".login_form #mobile").focus(function(){
        $("#login-mobile-err").hide();
    });
    $(".login_form #password").focus(function(){
        $("#login-password-err").hide();
    });

    $(".register_form #mobile").focus(function(){
        $("#register-mobile-err").hide();
    });
    $(".register_form #imagecode").focus(function(){
        $("#register-image-code-err").hide();
    });
    $(".register_form #smscode").focus(function(){
        $("#register-sms-code-err").hide();
    });
    $(".register_form #password").focus(function(){
        $("#register-password-err").hide();
    });


	// 点击输入框，提示文字上移
	// $('.form_group').on('click focusin',function(){
	// 	$(this).children('.input_tip').animate({'top':-5,'font-size':12},'fast').siblings('input').focus().parent().addClass('hotline');
	// })
    
    $('.form_group').on('click',function(){
        $(this).children('input').focus();
    });

    $('.form_group input').on('focusin',function(){
        $(this).siblings('.input_tip').animate({'top':-5,'font-size':12},'fast');
        $(this).parent().addClass('hotline');
    });


	// 输入框失去焦点，如果输入框为空，则提示文字下移
	$('.form_group input').on('blur focusout',function(){
		$(this).parent().removeClass('hotline');
		var val = $(this).val();
		if(val=='')
		{
			$(this).siblings('.input_tip').animate({'top':22,'font-size':14},'fast');
		}
	})


	// 打开注册框
	$('.register_btn').click(function(){
		$('.register_form_con').show();
		generateImageCode()
	})


	// 登录框和注册框切换
	$('.to_register').click(function(){
		$('.login_form_con').hide();
		$('.register_form_con').show();
        generateImageCode()
	})

	// 登录框和注册框切换
	$('.to_login').click(function(){
		$('.login_form_con').show();
		$('.register_form_con').hide();
	})

	// 根据地址栏的hash值来显示用户中心对应的菜单
	var sHash = window.location.hash;
	if(sHash!=''){
		var sId = sHash.substring(1);
		var oNow = $('.'+sId);		
		var iNowIndex = oNow.index();
		$('.option_list li').eq(iNowIndex).addClass('active').siblings().removeClass('active');
		oNow.show().siblings().hide();
	}

	// 用户中心菜单切换
	var $li = $('.option_list li');
	var $frame = $('#main_frame');

	$li.click(function(){
	    // alert($(this).index())
		if($(this).index()==5){
			$('#main_frame').css({'height':900});
		}
		else{
			$('#main_frame').css({'height':660});
		}
		$(this).addClass('active').siblings().removeClass('active');
		$(this).find('a')[0].click()
	})

    // TODO 登录表单提交
    $(".login_form_con").submit(function (e) {
    // $(".input_sub").submit(function (e) {
        e.preventDefault()
        var mobile = $(".login_form #mobile").val()
        var password = $(".login_form #password").val()

        if (!mobile) {
            $("#login-mobile-err").show();
            return;
        }

        if (!password) {
            $("#login-password-err").show();
            return;
        }

        // 发起登录请求
        var params = {
            "mobile":mobile,
            "password":password
        }
        $.ajax({
            url:"/passport/login",
            type:"POST",
            contentType:"application/json",
            data:JSON.stringify(params),
            headers:{'X-CSRFToken':getCookie('csrf_token')},
            success:function (repsonse) {
                if (repsonse.errno == '0'){
                    location.reload()
                    // alert("登录成功")
                }
                else {
                    alert(repsonse.errmsg)
                }

            }
        })
    })


    // TODO 注册按钮点击
    $(".register_form_con").submit(function (e) {
        // 阻止默认提交操作
        e.preventDefault()

		// 取到用户输入的内容
        var mobile = $("#register_mobile").val()
        var smscode = $("#smscode").val()
        var password = $("#register_password").val()

		if (!mobile) {
            $("#register-mobile-err").show();
            return;
        }
        if (!smscode) {
            $("#register-sms-code-err").show();
            return;
        }
        if (!password) {
            $("#register-password-err").html("请填写密码!");
            $("#register-password-err").show();
            return;
        }

		if (password.length < 6) {
            $("#register-password-err").html("密码长度不能少于6位");
            $("#register-password-err").show();
            return;
        }

        // 发起注册请求
        var  params_for_register = {
            "mobile":mobile,
            "smscode":smscode,
            "password":password
        }
        $.ajax({
            url : "/passport/register",
            type : "POST",
            data: JSON.stringify(params_for_register),
            contentType : "application/json",
            headers:{"X-CSRFToken":getCookie('csrf_token')},
            success:function (response) {
                if (response.errno = "0"){
                    location.reload()
                    // alert("注册成功！")
                }
                else{
                    alert(response.errmsg)
                }
            },
            error:function (e) {
                alert(e)
                alert("连接服务器失败，或为跨站请求保护！")
            }
        })


    })
})

var imageCodeId = ""

// TODO 生成一个图片验证码的编号，并设置页面中图片验证码img标签的src属性
function generateImageCode() {
    // alert("进行图片验证码验证")
    // 1.生成imagecodeId(UUID)
    imageCodeId = generateUUID();
    // 2.生成访问后端验证码视图的路由
    var url = '/passport/image_code?imageCodeID='+ imageCodeId
    // 3.将生成路由赋值给img标签的src属性
    // attr: 读取对应属性，并给对应属性赋值
    $('.get_pic_code').attr('src',url)
}


// 发送短信验证码
function sendSMSCode() {
    // 校验参数，保证输入框有数据填写
    $(".get_code").removeAttr("onclick");
    var mobile = $("#register_mobile").val();
    if (!mobile) {
        $("#register-mobile-err").html("请填写正确的手机号！");
        $("#register-mobile-err").show();
        $(".get_code").attr("onclick", "sendSMSCode();");
        return;
    }
    var imageCode = $("#imagecode").val();
    if (!imageCode) {
        $("#image-code-err").html("请填写验证码！");
        $("#image-code-err").show();
        $(".get_code").attr("onclick", "sendSMSCode();");
        return;
    }


    // TODO 发送短信验证码
    // 准备参数
    var params = {
        'mobile':mobile,
        'image_code':imageCode,
        'image_code_id':imageCodeId
    };
    // 发送ajax请求，向服务器获取短信验证码
    $.ajax({
        url:'/passport/sms_code', // 请求地址
        type:'post', // 请求方法
        data:JSON.stringify(params), // 请求体,将字典params转成json字符串
        contentType:'application/json', // 指定请求体数据类型
        headers:{'X-CSRFToken':getCookie('csrf_token')},
        success:function (response) { // 准备接受响应的回调
            if (response.errno == '0') {
                // 代表成功
                // alert('发送短信验证码成功');
                var num = 10;
                var t = setInterval(function(){
                    if (num == 1){
                    //    倒计时完成，清楚计时器
                        clearInterval(t);
                        generateImageCode();
                    //    重置内容
                        $(".get_code").html("点击获取验证码");
                        $(".get_code").attr("onclick","sendSMSCode()");
                    }
                    else {
                        $(".get_code").html(num+"秒");
                    }
                    // 每一秒减一
                    num -= 1;

                },1000);
            } else {
                // 请求发送失败
                alert(response.errmsg);
                generateImageCode()
                $(".get_code").attr("onclick","sendSMSCode()")
            }
        },
        error:function () {

            alert("请求失败，服务器拒绝访问，或为CSRF跨站请求保护")
        }
    });


}

// 调用该函数模拟点击左侧按钮
function fnChangeMenu(n) {
    var $li = $('.option_list li');
    if (n >= 0) {
        $li.eq(n).addClass('active').siblings().removeClass('active');
        // 执行 a 标签的点击事件
        $li.eq(n).find('a')[0].click()
    }
}

// 一般页面的iframe的高度是660
// 新闻发布页面iframe的高度是900
function fnSetIframeHeight(num){
	var $frame = $('#main_frame');
	$frame.css({'height':num});
}

//  该函数用于从cookie中读取到值
function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function generateUUID() {
    var d = new Date().getTime();
    if(window.performance && typeof window.performance.now === "function"){
        d += performance.now(); //use high-precision timer if available
    }
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (d + Math.random()*16)%16 | 0;
        d = Math.floor(d/16);
        return (c=='x' ? r : (r&0x3|0x8)).toString(16);
    });
    return uuid;
}

//退出登录
function logout() {

    // ajax 简写形式
    $.get("/passport/logout",function (response) {
        if (response.errno == "0"){
            location.reload();
        }else {
            alert(response.errmsg);
        }

    })

}