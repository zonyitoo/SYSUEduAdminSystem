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
        var username = $("#username").val();
        var passwd = $("#passwd").val();
        for (var i = 0;i < username.length;i++)
          if (username[i] < '0' || username[i] > '9' && username[i] < 'A' || username[i] > 'Z' && username[i] < 'a' || username[i] > 'z')
          {
              alert("用户名非法！");
              return false;
          }
        $.ajax({
            url: '/user/login/',
            data: 'username=' + username + '&passwd=' + passwd,
            type: 'post',
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
