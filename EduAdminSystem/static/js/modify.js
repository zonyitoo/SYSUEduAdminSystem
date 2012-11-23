//JavaScript Document
function check()
{
    var oldpasswd = $("#oldpasswd").val();
    var newpasswd = $("#newpasswd").val();
    var confirmpasswd = $("#confirmpasswd").val();
    if (newpasswd != confirmpasswd)
    {
        $("#success").hide();
        $("#error").show();
        $("#error-content").text("确认密码必须与新密码相同！");
    }
    else if (oldpasswd.length < 6)
    {
        $("#success").hide();
        $("#error").show();
        $("#error-content").text("旧密码错误！");
    }
    else if (newpasswd.length < 6)
    {
        $("#success").hide();
        $("#error").show();
        $("#error-content").text("密码不得少于6位！");
    }
    else
    {
        $.ajax({
            url: "/user/modifypwd/", //访问路径
            data: "oldpasswd=" + $("#oldpasswd").val() + "&newpasswd=" + $("#newpasswd").val(), //需要验证的参数
            type: 'post', //传值的方式
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
                    $("#error").show();
                    $("#error-content").text("旧密码错误！");
                }
                else
                {
                    $("#error").hide();
                    $("#success").show();
                    $("#success-content").text("密码修改成功！");
                }
            }
        });
    }
    return false;
}
