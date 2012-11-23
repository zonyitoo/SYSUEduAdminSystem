// JavaScript Document

$(document).ready(function(){ 
    var url = top.location.href;
    var pos = url.indexOf("login");
    if (pos < 0)
        getView();
}); 

function getView()
{
	$.ajax({
		url: '/getview/', //访问路径
		type: 'get', //传值的方式
		error: function ()
		{//访问失败时调用的函数
			alert("链接服务器错误！");
		},
		success: function (msg)
		{//访问成功时调用的函数,这里的msg是getview.php返回的值
			$(".container").html(msg);
		}
	});
}
