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
            var url = msg.url;
            var logoutid = msg.logoutaccount;
            window.location = url + "?logoutid=" + logoutid;
        }
    });
}
