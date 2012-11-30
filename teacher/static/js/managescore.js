//JavaScript Document

$(document).ready(function(){
    $("#view-student-btn").click(function(){
        manageScore();
    });
    $("#download-template-btn").click(function(){
    });
});

function manageScore(){
    $.ajax({
        url: '/teacher/getTakenInfoList/',
        data: 'course=' + $("#course-2").val(),
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
            $("#student-result").empty();
            $("#student-result").append("<table class='table table-hover table-bordered table-condensed'><thead><tr><th>学号</th><th>姓名</th><th>学院</th><th>学系</th><th>专业</th><th>出勤率</th><th>平时成绩</th><th>期末成绩</th><th>总评</th></tr></thead><tbody id='student-list'></tbody></table>");
            var takes = msg.takes;
            var course,student,school,major,usual_score,final_score,score;
            for (var i = 0;i < takes.length;i++)
            {
                course = takes[i].course;
                student = takes[i].student;
                attendance = takes[i].attendance;
                usual_score = takes[i].usual_score;
                final_score = takes[i].final_score;
                score = takes[i].score;
                $("#student-list").append("<tr><td>" + student.user.username + "</td><td>" + student.student_name + "</td><td>" + student.student_meta.major.department.school.name + "</td><td>" + student.student_meta.major.department.name + "</td><td>" + student.student_meta.major.name + "</td><td>" + attendance + "</td><td>" + usual_score + "</td><td>" + final_score + "</td><td>" + score + "</td></tr>");
            }
            $("#student-result").append("<div class='msg-area'></div>");
        }
    });
    $("[rel = 'popover']").popover();
}

function upload()
{
}
