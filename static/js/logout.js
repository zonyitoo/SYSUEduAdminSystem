// JavaScript Document

function logout()
{
    $.ajax({
        url: '/user/logout/',
        type: 'get',
        error: function() {
            alert("链接服务器错误！");
        },
        success: function(msg) {
            window.location = '/user/login/';
        }
    });
}
