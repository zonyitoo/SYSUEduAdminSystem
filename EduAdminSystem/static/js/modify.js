//JavaScript Document

$(document).ready(function(){
    $("#modify").on('show', function(){
        $(document).keydown(function(e){
            if (e.which == 27)
            {
                $("#modify").modal('hide');
                refresh();
            }
        });
    });
    $("#contact").on('show', function(){
        $(document).keydown(function(e){
            if (e.which == 27)
                $("#contact").modal('hide');
        });
    });
    $("#calendar").on('show', function(){
        $(document).keydown(function(e){
            if (e.which == 27)
                $("#calendar").modal('hide');
        });
    });
    $("#about").on('show', function(){
        $(document).keydown(function(e){
            if (e.which == 27)
                $("#about").modal('hide');
        });
    });
});

function check()
{
    var oldpasswd = $("#oldpasswd").val();
    var newpasswd = $("#newpasswd").val();
    var confirmpasswd = $("#confirmpasswd").val();
    if (newpasswd != confirmpasswd)
    {
        $("#success").hide();
        $("#error").hide();
        $("#error-content").text("确认密码必须与新密码相同！");
        $("#error").fadeIn();
        $("#confirmpasswd").focus();
    }
    else if (oldpasswd == "")
    {
        $("#success").hide();
        $("#error").hide()
        $("#error-content").text("旧密码错误！");
        $("#error").fadeIn();
        $("#oldpasswd").focus();
    }
    else if (newpasswd.length < 6)
    {
        $("#success").hide();
        $("#error").hide();
        $("#error-content").text("密码不得少于6位！");
        $("#error").fadeIn();
        $("#newpasswd").focus();
    }
    else
    {
        $.ajax({
            url: '/user/modifypwd/',
            data: 'oldpasswd=' + $("#oldpasswd").val() + '&newpasswd=' + $("#newpasswd").val(), 
            type: 'post',
            async: false,
            error: function(jqXHR,textStatus,errorThrown)
            {
                switch(jqXHR.status)
                {
                    case 400:
                        alert("网络状态异常，请刷新后重试");
                        break;
                    case 401:
                        alert("当前用户已过期，请重新登录");
                        window.location = '/user/login/';
                        break;
                    case 403:
                        alert("页面无法访问，请刷新后重试");
                        break;
                    case 404:
                        alert("页面不存在，请刷新后重试");
                        break;
                    case 500:
                        alert("服务器傲娇");
                        break;
                    default:
                        alert(jqXHR.status + "\n" + textStatus + "\n" + errorThrown);
                        break;
                }
            },
            success: function(msg,textStatus,jqXHR)
            {
                var valid = msg.valid;
                if (valid == false)
                {
                    $("#success").hide();
                    $("#error").hide();
                    $("#error-content").text("旧密码错误！");
                    $("#error").fadeIn();
                    $("#oldpasswd").focus();
                }
                else
                {
                    $("#error").hide();
                    $("#success").hide();
                    $("#success-content").text("密码修改成功！");
                    $("#success").fadeIn();
                    $("#close").focus();
                }
            }
        });
    }
    return false;
}

function refresh()
{
    $("#error").hide();
    $("#success").hide();
    $("#oldpasswd").val("");
    $("#newpasswd").val("");
    $("#confirmpasswd").val("");
    $("#oldpasswd").focus();
}
