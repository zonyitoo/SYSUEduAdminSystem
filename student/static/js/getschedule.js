//JavaScript Document

$(document).ready(function(){
    $("#view-schedule-btn").click(function(){
        getSchedule();
    });
});

function getSchedule(){
    var yr = document.getElementById("school-year-3");
    var year = yr.options[yr.selectedIndex].text;
    var sem = document.getElementById("school-term-3").selectedIndex;
    sem = sem + 1;
    $.ajax({
        url: '/take/getTakeCourses/',
        data: 'year=' + year + '&sem=' + sem,
        datatype: 'json',
        type: 'get',
        error: function()
        {
            alert("链接服务器错误！");
        },
        success: function(msg)
        {
            var i = 0;
            var lt = msg.courses;
            var tot = lt.length;
            for (i = 0; i < tot; i++)
            {
                var index = i + 1;
                var courseName = lt[i].name;
                var courseType = lt[i].course_type;
                var credit = lt[i].credit;
                var teacher = lt[i].teacher.teacher_name;
                var exam = lt[i].exam_method;
                var period = lt[i].from_week + "~" + lt[i].to_week + "周";
                var time = lt[i].course_time.time;
                var capacity = lt[i].capacity;
                $("#schedule-result").empty();
                $("#schedule-result").append("<table class='table table-bordered table-condensed'><thead><tr><th>序号</th><th width='200'>课程名称</th><th>类别</th><th>学分</th><th>任课教师</th><th>考核方式</th><th>起止时间</th><th>上课时段</th><th width='100'>剩余容量</th></tr></thead><tbody id='schedule-list'></tbody</table>");
                $("#schedule-list").append("<tr><td class='" + index + "'>" + index + "</td><td>" + courseName + "</td><td>" + courseType + "</td><td>" + credit + "</td><td>" + teacher + "</td><td>" + exam + "</td><td>" + period + "</td><td>" + time + "</td><td>" + capacity + "</td></tr>");
            }           
        }
    });
}
