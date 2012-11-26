//JavaScript Document
$(document).ready(function(){
    $("#contact").on('show', function(){
        $(document).keydown(function(){
            $("#contact").modal('hide');
        });
    });
    $("#calendar").on('show', function(){
        $(document).keydown(function(){
            $("#calendar").modal('hide');
        });
    });
    $("#about").on('show', function(){
        $(document).keydown(function(){
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
            url: "/user/modifypwd/", //访问路径
            data: "oldpasswd=" + $("#oldpasswd").val() + "&newpasswd=" + $("#newpasswd").val(), //需要验证的参数
            type: 'post', //传值的方式
            async: false,
            error: function ()
            {//访问失败时调用的函数
                alert("链接服务器错误！");
            },
            success: function (msg)
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
    $("#oldpasswd").focus();
    $("#newpasswd").val("");
    $("#confirmpasswd").val("");
}
