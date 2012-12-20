//JavaScript Document

$(document).ready(function(){
    $("#start-screen-btn").click(function(){
        toggleCourseScreen();
    });
});

function toggleCourseScreen()
{
    var select_type;
    if ($("#po").hasClass("active"))
        select_type = 0;
    else if ($("#pr").hasClass("active"))
        select_type = 1;
    else if ($("#mo").hasClass("active"))
        select_type = 2;
    else if ($("#mr").hasClass("active"))
        select_type = 3;
    else if ($("#pe").hasClass("active"))
        select_type = 4;
    $.ajax({
        url: '/administrator/toggleCourseScreen/',
        data: 'course_type=' + select_type,
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
            alert("OK");
        }
    });
}
