//JavaScript Document

$(document).ready(function(){
    $("#school-3").change(function(){
        $.ajax({
            url: '/school/getAllDepartments/',
            data: 'school=' + $("#school-3").val(),
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
                var department_name = msg.departments;
                $(".department").empty();
                for (var i = 0;i < department_name.length;i++)
                    $(".department").append("<option class='" + i + "'>" + department_name[i].name + "</option>");
            }
        });
    });
    $("#view-assessment-btn").click(function(){
        viewAssessment();
    });
});

function viewAssessment(){
    $.ajax({
        url: '/assessment/getCourseAssessments/',
        data: 'department=' + $("#department-3").val() + '&year=' + $("#school-year-3").val() + '&semester=' + $("#school-term-3").val(),
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
            $("#assessment-result").empty();
            alert(msg.assessments);
            $("#assessment-result").append("<div class='msg-area'></div>");
        }
    });
    $("[rel = 'popover']").popover();
}
