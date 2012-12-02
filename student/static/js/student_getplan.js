//JavaScript Document

$(document).ready(function(){
    $("#view-plan-btn").click(function(){
        getPlan();
    });
});

function getPlan()
{
    $.ajax({
        url: '/course/getEducatePlan/',
        data: 'cultivate=' + $("#cultivate-2 option:selected").val(),
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
            var student = msg.student;
            var student_meta = student.student_meta;
            var courses = msg.courses;
            var pr_req = student_meta.req_pubcourse;
            var po_req = student_meta.req_pubelective;
            var mr_req = student_meta.req_procourse;
            var mo_req = student_meta.req_proelective;
            var pr_credit = student.pubcourse_credit;
            var po_credit = student.pubelective_credit;
            var mr_credit = student.procourse_credit;
            var mo_credit = student.proelective_credit;
            var gpa = student.gpa;
            var pr_gpa = student.pubcourse_gpa;
            var po_gpa = student.pubelective_gpa;
            var mr_gpa = student.procourse_gpa;
            var mo_gpa = student.proelective_gpa;
            var student_type = student_meta.type_name;
            var reg_year = student_meta.year;
            $("#plan-result").empty();
            $("#plan-result").append("<table class='table table-bordered table-hover table-condensed'><thead><tr><th>类别</th><th>应修学分</th><th>已修学分</th><th>平均绩点</th><th>专业排名</th></tr></thead><tbody id='plan-list'></tbody></table>");
            $("#plan-list").append("<tr><td>公必</td><td>" + pr_req + "</td><td>" + pr_credit + "</td><td>" + pr_gpa + "</td><td></td></tr><tr><td>公选</td><td>" + po_req + "</td><td>" + po_credit + "</td><td>" + po_gpa + "</td><td></td></tr><tr><td>专必</td><td>" + mr_req + "</td><td>" + mr_credit + "</td><td>" + mr_gpa + "</td><td></td></tr><tr><td>专选</td><td>" + mo_req + "</td><td>" + mo_credit + "</td><td>" + mo_gpa + "</td><td></td></tr><tr><td>合计</td><td>" + (pr_req + po_req + mr_req + mo_req) + "</td><td>" + (pr_credit + po_credit + mr_credit + mo_credit) + "</td><td>" + gpa + "</td><td></td></tr>");
            $("#plan-result").append("<br><table class='table table-bordered table-hover table-condensed'><thead><tr><th>课程名称</th><th>类别</th><th>学分</th><th>任课教师</th><th>开课学年</th><th>开课学期</th></tr></thead><tbody id='plan-course-list'></tbody></table>");
            var name,teacher,semester,term;
            for (var i = 0;i < courses.length;i++)
            {
                name = courses[i].name;
                teacher = courses[i].teacher.teacher_name;
                if (teacher == null || teacher == "")
                  teacher = "待定";
                semester = courses[i].semester;
                term = "上学期";
                switch(semester)
                {
                    case 1:
                        break;
                    case 2:
                        term = "下学期";
                        break;
                    case 3:
                        term = "小学期";
                        break;
                }
                $("#plan-course-list").append("<tr><td>" + name + "</td><td>" + courses[i].course_type + "</td><td>" + courses[i].credit + "</td><td>" + teacher + "</td><td>" + courses[i].academic_year + "</td><td>"+ term + "</td></tr>");
            }
            $("#plan-result").append("<div class='msg-area'></div>");
        }
    });
    $("[rel = 'popover']").popover();
}
