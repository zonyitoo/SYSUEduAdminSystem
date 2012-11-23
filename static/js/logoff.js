$(document).ready(function (){
    $("#logoff").click(function (){
        logoff();
    })
});

function logoff()
{
    $.ajax({
        url: '/user/logoff/',
        data: 'username=' + $("#user-id").val() + "&rid=" + Math.random(),
        type: 'get',
        error: function() {
            alert("链接服务器错误！");
        }
        success: function(msg) {
            alert(msg);
            window.location = msg;
        }
    });
}
