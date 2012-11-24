//JavaScript Document

$(document).ready(function(){
    $("#view-course-btn").click(function(){
        getCourse();
    });
});

function toggleCourse(n)
{
    $("." + n + ".btn").toggle(
                function(){
                    $(this).text("退课");
                },
                function(){
                    $(this).text("选课");
                }
    );
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
                var courseName = list[i].name;
                var courseType = list[i].course_type;
                var credit = list[i].credit;
                var teacher = list[i].teacher;
                var exam = list[i].exam_method;
                var period = list[i].from_week + "~" + list[i].to_week + "周";
                var time = list[i].course_time;
                var capacity = list[i].capacity;
                $("#course-result").empty();
                $("#course-result").append("<table class='table table-bordered table-condensed'><thead><tr><th>序号</th><th width='200'>课程名称</th><th>类别</th><th>学分</th><th>任课教师</th><th>考核方式</th><th>起止时间</th><th>上课时段</th><th width='100'>剩余容量</th><th>是否选择</th></tr></thead><tbody id='course-list'></tbody</table>");
                $("#course-list").append("<tr><td class='" + index + "'>" + index + "</td><td>" + courseName + "</td><td>" + courseType + "</td><td>" + credit + "</td><td>" + teacher + "</td><td>" + exam + "</td><td>" + period + "</td><td>" + time + "</td><td>" + capacity + "</td><td><button class='btn btn-primary " + index + "' onclick='toggleCourse(" + index + ")'>选课</button></td></tr>");
            }
        }
    });
}
