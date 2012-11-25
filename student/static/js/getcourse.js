//JavaScript Document

$(document).ready(function(){
    $("#view-course-btn").click(function(){
        getCourse();
    });
    $("[rel='popover']").popover();
});

function toggleCourse(n)
{
    var course_id = $("tr." + n + " td:eq(1)").attr("id");
    if (sendRequest(course_id))
    {
        if ($("." + n + ".btn").val() == "选课")
        {
            $("." + n + ".btn").removeClass("btn-primary").addClass("btn-danger");
            $("." + n + ".btn").val("退课");
        }
        else
        {
            $("." + n + ".btn").removeClass("btn-danger").addClass("btn-primary");
            $("." + n + ".btn").val("选课");
        }
    }
}

function getCourse()
{
    var cultivate = document.getElementById("cultivate-1").selectedIndex;
    var po = !($("#po").hasClass("active"));
    var pr = !($("#pr").hasClass("active"));
    var mo = !($("#mo").hasClass("active"));
    var mr = !($("#mr").hasClass("active"));
    $.ajax({
        url: '/course/getAvailableList/',
        data: 'cultivate=' + cultivate +'&po=' + po + '&pr=' + pr + '&mo=' + mo + '&mr=' + mr,
        datatype: 'json',
        type: 'get',
        async: false,
        error: function()
        {
            alert("链接服务器错误！");
        },
        success: function(msg)
        {
            var i = 0;
            var list = msg.courses;
            var total = list.length;
            for (i = 0;i < total;i++)
            {
                var index = i + 1;
                var id = list[i].id;
                var courseName = list[i].name;
                var courseType = list[i].course_type;
                var credit = list[i].credit;
                var teacher = list[i].teacher;
                var exam = list[i].exam_method;
                var period = list[i].from_week + "~" + list[i].to_week + "周";
                var week = list[i].course_time[0].week;
                var time = list[i].course_time[0].time;
                var capacity = list[i].capacity;
                $("#course-result").empty();
                $("#course-result").append("<table class='table table-bordered table-condensed'><thead><tr><th>序号</th><th width='200'>课程名称</th><th>类别</th><th>学分</th><th>任课教师</th><th>考核方式</th><th>起止时间</th><th>上课时段</th><th width='100'>剩余容量</th><th>是否选择</th></tr></thead><tbody id='course-list'></tbody</table>");
                $("#course-list").append("<tr class='" + index + "'><td>" + index + "</td><td id='"+ id + "'>" + courseName + "</td><td>" + courseType + "</td><td>" + credit + "</td><td><a rel='popover' title='教师信息' data-content='姓名：" + teacher.teacher_name + "<br>学系：" + teacher.department + "<br>职称：" + teacher.title + "<br>主页：" + teacher.site + "'>" + teacher.teacher_name + "</a></td><td>" + exam + "</td><td>" + period + "</td><td>" + week + time + "</td><td>" + capacity + "</td><td><input type='button' class='btn btn-primary " + index + "' onclick='toggleCourse(" + index + ")' value='选课'/></td></tr>");
            }
        }
    });
}

function sendRequest(course_id)
{
    var flag = false;
    $.ajax({
        url: '/student/withdrawalCourse/',
        data: 'id=' + course_id,
        datatype: 'json',
        type: 'post',
        async: false,
        error: function()
        {
            alert("链接服务器错误！");
            flag = false;
        },
        success: function(msg)
        {
            var valid = msg.valid;
            if (valid == false)
            {
                alert("选/退课失败！");
                flag = false;
            }
            else
            {
                flag = true;
            }
        }
    });
    return flag;
}
