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
                        // 添加成功即重新刷新页面
                        location.reload()
                    }
                    else {
                        alert(repsonse.errmsg)
                    }
                }
            })

		})

		$('#list').delegate('a', 'click', function(){
			// 找出自己要点击的行为
			var myclass = $(this).prop('class')

			var task_name = $(this).parent().children('span').html()

			var params = {
				"task_name":task_name,
			}

			if(myclass == 'del')
			{
				// 删除任务
				$.ajax({
                url: "/task/delete",
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify(params),
                headers: {'X-CSRFToken': getCookie('csrf_token')},
                success: function (repsonse) {
                    if (repsonse.errno == '0') {
                        // 添加成功即重新刷新页面
                        location.reload()
                    }
                    else {
                        alert(repsonse.errmsg)
                    }
                }
            })
			}
			if(myclass == 'up')
			{
				// 任务向上
				$.ajax({
                url: "/task/up",
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify(params),
                headers: {'X-CSRFToken': getCookie('csrf_token')},
                success: function (repsonse) {
                    if (repsonse.errno == '0') {
                        // 添加成功即重新刷新页面
                        location.reload()
                    }
                    else {
                        alert(repsonse.errmsg)
                    }
                }
            })
			}
			if(myclass == 'down')
			{
				// 任务向下
				$.ajax({
                url: "/task/down",
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify(params),
                headers: {'X-CSRFToken': getCookie('csrf_token')},
                success: function (repsonse) {
                    if (repsonse.errno == '0') {
                        // 添加成功即重新刷新页面
                        location.reload()
                    }
                    else {
                        alert(repsonse.errmsg)
                    }
                }
            })
			}
		})
	})
