//JavaScript Document

$(document).ready(function(){
    $("#view-score-btn").click(function(){
        getScore();
    });
});

function getScore()
{
    $.ajax({
        url: '/take/getTakeScore/',
        data: 'school-year=' + $("#school-year-5").val() + '&school-term=' + $("#school-term-5").val(),
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
            $("#score-result").empty();
            $("#score-result").append("<table class='table table-bordered table-hover table-condensed'><thead><tr><th>序号</th><th>课程名称</th><th>课程类别</th><th>学分</th><th>平时成绩</th><th>期末成绩</th><th>总评</th><th>排名</th></tr></thead><tbody id='score-list'></tbody></table>");
            var courses = msg.takes;
            var course_name,course_type,credit,usual_score,final_score,final_percentage,total_score,rank;
            for (var i = 0;i < courses.length;i++)
            {
                course_name = courses[i].course.name;
                course_type = courses[i].course.course_type;
                credit = courses[i].course.credit;
                usual_score = courses[i].usual_score;
                final_score = courses[i].final_score;
                final_percentage = courses[i].final_percentage;
                total_score = courses[i].score;
                rank = courses[i].rank;
                $("#score-list").append("<tr><td>" + (i + 1) + "</td><td>" + course_name + "</td><td>" + course_type + "</td><td>" + credit + "</td><td>" + usual_score + "</td><td>" + final_score + "</td><td>" + total_score + "</td><td>" + rank + "</td></tr>");
            }
            $("#score-result").append("<div class='msg-area'></div>");
        }
    });
    $("[rel = 'popover']").popover();
}
