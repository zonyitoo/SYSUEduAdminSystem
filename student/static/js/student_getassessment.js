//JavaScript Document

$(document).ready(function(){
    getAssessment();
    $("#view-assessment-btn").click(function(){
        getAssessment();
    });
});

function getAssessment()
{
    $.ajax({
        url: '/take/getTakeAssessment/',
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
            $("#assessment-result").append("<table class='accordion table table-bordered table-hover table-condensed'><thead><tr><th>课程名称</th><th>类别</th><th>学分</th><th>任课教师</th><th>教学评分</th></tr></thead><tbody id='assessment-list'></tbody></table>");
            var assessment = msg.assessment;
            var course_name,course_type,credit,teacher;
            for (var i = 0;i < assessment.length;i++)
            {
                course_name = assessment[i].course.name;
                course_type = assessment[i].course.course_type;
                credit = assessment[i].course.credit;
                teacher = assessment[i].course.teacher;
                $("#assessment-list").append("<tr><td>" + course_name + "</td><td>" + course_type + "</td><td>" + credit + "</td><td>" + teacher.teacher_name + "</td><td id='assessment-" + i + "'></td></tr>");
                var assessment_block = $("#assessment-" + i);
                assessment_block.append("<div class='accordion-group'><div class='accordion-heading'><div class='accordion-toggle' data-toggle='collapse' data-parent='#assessment-" + i + "' data-target='#assessment-0-" + i + "'><strong>外貌</strong></div></div><div id='assessment-0-" + i + "' class='accordion-body collapse'><div class='accordion-inner'><div class='maintain'></div></div></div></div>");
                assessment_block.append("<div class='accordion-group'><div class='accordion-heading'><div class='accordion-toggle' data-toggle='collapse' data-parent='#assessment-" + i + "' data-target='#assessment-1-" + i + "'><strong>身材</strong></div></div><div id='assessment-1-" + i + "' class='accordion-body collapse'><div class='accordion-inner'><div class='figure'></div></div></div></div>");
                $(".maintain").raty({
                    hints: ['屌丝','毅丝','普通青年','文艺青年','糕帅富'],
                    scoreName: "score"
                });
                $(".figure").raty({
                    hints: ['1分不能再多','2分不能再多','3分不能再多','4分不能再多','5分不能再多'],
                    scoreName: "score"
                });
            }
        }
    });
}
