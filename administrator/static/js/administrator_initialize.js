//JavaScript Document

$(document).ready(function() {
    $(".upload").on('show', function(){
        $(document).keydown(function(e){
            if (e.which == 27)
                $(".upload").modal('hide');
        });
    });
    var date = new Date()
    var year = date.getFullYear();
    var month = date.getMonth() + 1;
    var term = 0;
    if (month < 9)
        year--;
    if (month >= 9 || month < 2)
        term = 1;
    else if (month >= 2 && month < 7)
        term = 2;
    else term = 3;
    for (var i = year;i >= 2005;i--)
    {
        $(".school-year").append("<option class='" + i + "'>" + i + "-" + (i + 1) + "</option>");
        $(".grade").append("<option class='" + i + "'>" + i + "</option>");
    }
    $(".school-term option[value='" + term + "']").attr("selected","selected");
    $(".current-year").text(year + "-" + (year + 1));
    $(".current-term").text(term);
    $.ajax({
        url: '/school/getAllSchools/',
        type: 'get',
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
            var school_name = msg.schools;
            for (var i = 0;i < school_name.length;i++)
                $(".school").append("<option class='" + i + "'>" + school_name[i].name + "</option>");
        }
    });
});
