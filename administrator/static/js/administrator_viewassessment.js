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
        url: '/assessment/getAssessments/',
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
            var assessments = msg.assessments;
            $("#assessment-result").empty();
            if (assessments.length == 0)
                $("#assessment-result").append("暂无学生评教。");
            else
            {
                $("#assessment-result").append("<table class='table table-hover table-bordered table-condensed'><thead><tr><th>序号</th><th>课程名称</th><th>类别</th><th>任课教师</th><th>评教总分</th></tr></thead><tbody id='assessment-list'></tbody></table>");
                var course_name,course_type,teacher,score;
                for (var i = 0;i < assessments.length;i++)
                {
                    course_name = assessments[i].course.name;
                    course_type = assessments[i].course.course_type;
                    teacher = assessments[i].course.teacher;
                    score = assessments[i].assessment_score;
                    $("#assessment-list").append("<tr><td>" + (i + 1) + "</td><td>" + course_name + "</td><td>" + course_type + "</td><td>" + teacher.teacher_name + "</td><td>" + score + "</td></tr>");
                }
                $("#assessment-result").append("<div class='msg-area'></div>");
            }
        }
    });
    $("[rel = 'popover']").popover();
}
