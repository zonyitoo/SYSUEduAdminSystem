// JavaScript Document

function validate()
{
    var username = $("#username").val();
    var passwd = $("#passwd").val();
    if (username == "")
    {
        $("#prompt").hide();
        $("#alert").hide();
        $("#alert").text("请输入用户名！");
        $("#alert").fadeIn();
        $("#username")[0].focus();
        return false;
    }
    else 
    {
        $.ajax({
            url: "/user/login/", //访问路径
            data: "username=" + $("#username").val() + "&passwd=" + $("#passwd").val(), //需要验证的参数
            type: "post", //传值的方式
            error: function ()
            {//访问失败时调用的函数
                alert("链接服务器错误！");
            },
            success: function (msg)
            {//访问成功时调用的函数,这里的msg是login.php返回的值
                var valid = msg.valid;
                var next = msg.next;
                if (valid == false)
                {
                    $("#prompt").hide();
                    $("#alert").hide();
                    $("#alert").text("用户名或密码错误！");
                    $("#alert").fadeIn();
                }
                else
                    window.location = next;
            }
        });
        return false;
    }
}
