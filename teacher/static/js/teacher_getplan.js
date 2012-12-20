//JavaScript Document

$(document).ready(function(){
    getPlan();
    $("#view-course-btn").click(function(){
        getPlan();
    });
    $("#school-year-1").change(function(){
        getPlan();
    });
    $("#course-type-1").change(function(){
        getPlan();
    });
});

function getPlan() {
    $.ajax({
        url: '/teacher/getTeachPlan/',
        data: 'school-year=' + $("#school-year-1").val() + '&course-type=' + $("#course-type-1").val(),
        type: 'get',
        async: false,
        error: function(jqXHR,textStatus,errorThrown) {
            switch(jqXHR.status) {
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
              default:
                  alert(jqXHR.status + "\n" + textStatus + "\n" + errorThrown);
                  break;
            }
        },
        success: function(msg,textStatus,jqXHR) {
            var courses = msg.courses;
            $("#available-result").empty();
            if (courses.length == 0)
                $("#available-result").append("暂无课程可开设。");
            else
            {
                $("#available-result").append("<br><table class='table table-bordered table-hover table-condensed'><thead><tr><th>课程名称</th><th>类别</th><th>学分</th><th>任课教师</th><th>开课学年</th><th>开课学期</th></tr></thead><tbody id='available-list'></tbody></table>");
                var name, teacher, sem, term;
                for (var i = 0; i < courses.length; ++i) {
                    name = courses[i].name;
                    teacher = courses[i].teacher.teacher_name;
                    if (teacher == null || teacher == "")
                        teacher = "待定";
                    sem = courses[i].semester;
                    switch (sem) {
                        case 1:
                            term = "上学期";
                            break;
                        case 2:
                            term = "下学期";
                            break;
                        case 3:
                            term = "小学期";
                            break;
                    }
                    $("#available-list").append("<tr><td>" + name + "</td><td>" + courses[i].course_type + "</td><td>" + courses[i].credit + "</td><td>" + teacher + "</td><td>" + courses[i].academic_year + "</td><td>"+ term + "</td></tr>");
                }
                $("#available-result").append("<div class='msg-area'></div>");
            }
        }
    });
    $("[rel = 'popover']").popover();
}
