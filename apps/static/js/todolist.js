/**
 * Created by huangchengfang on 2018/8/28.
 */

$(function(){
		// 增加按钮单击，增加数据到html；删除，上下单击
		$('#btn1').click(function(){
			var vals = $('#txt1').val()
			if(vals == '')
			{
				alert('请输入内容')
				return
			}

			// 发起添加任务请求
			var params = {
				"task":vals,
			}
			$.ajax({
                url: "/task/add",
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify(params),
                headers: {'X-CSRFToken': getCookie('csrf_token')},
                success: function (repsonse) {
                    if (repsonse.errno == '0') {
                        location.reload()
                        // alert("登录成功")
                    }
                    else {
                        alert(repsonse.errmsg)
                    }
                }
            })

			// var $li = $('<li><span>'+ vals +'</span><a href="javascript:;" class="up"> ↑ </a><a href="javascript:;" class="down"> ↓ </a><a href="javascript:void(0);" class="del">删除</a></li>')
			// $('#list').prepend( $li )
		})

		// $('a').click(function(){
		// 	alert(1)
		// }) **** 原始绑定命令的方法无法给未来元素绑定命令
		$('#list').delegate('a', 'click', function(){
			// alert(2)
			// 如果删除，执行删除标签li -- class值
			var myclass = $(this).prop('class')
			// alert(myclass)
			if(myclass == 'del')
			{
				// 删除自己的父级
				$(this).parent().remove()
			}
			if(myclass == 'up')
			{
				// 如果是第一个提示
				if($(this).parent().index() == 0){
					alert('已经是第一个了')
					return
				}
				$(this).parent().insertBefore( $(this).parent().prev() )
			}
			if(myclass == 'down')
			{
				// 如果是最后一个提示:li下标 == 长度-1
				// 后面没有别的li了就是最后一个，后面的所有人的长度==0
				if($(this).parent().nextAll().length == 0)
				{
					alert('已经是最后一个了')
					return
				}
				$(this).parent().insertAfter( $(this).parent().next() )
			}
		})
	})
