// JavaScript Document
$(document).ready(function(){ 
	$("#submit").mousedown(function(){ 
		login(); //点击ID为submit"的按钮后触发函数 login(); 
	}); 
}); 

function login()
{
	$.ajax({
		url: 'login.php', //访问路径
		data: 'username=' + $("#username").val() + "&password=" + $("#passwd").val(), //需要验证的参数
		type: 'post', //传值的方式
		error: function ()
		{//访问失败时调用的函数
			alert("链接服务器错误！");
		},
		success: function (msg)
		{//访问成功时调用的函数,这里的msg是login.php返回的值
			$(".container").load(msg);
			$("#comic").hide();
		}
	});
}