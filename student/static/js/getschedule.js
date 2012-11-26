//JavaScript Document

$(document).ready(function(){
    $("#view-schedule-btn").click(function(){
        getSchedule();
    });
});

function getSchedule()
{
    $.ajax({
        url: '/take/getTakeCourses/',
        data: 'school-year=' + $("#school-year-3").val() + '&school-term=' + (document.getElementById("school-term-3").selectedIndex + 1),
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
            var i = 0;
            var j = 0;
            var k = 0;
            var list = msg.courses;
            var total = list.length;
            var week_map = new Array("世界末日","周一","周二","周三","周四","周五","周六","周日");
            var time_map = new Array("08:00~08:45","08:55~09:40","09:50~10:35","10:45~11:30","11:40~12:25","12:35~13:20","13:30~14:15","14:25~15:10","15:20~16:05","16:15~17:00","17:10~17:55","18:05~18:50","19:00~19:45","19:55~20:40","20:50~21:35");
            $("#schedule-result").empty();
            $("#schedule-result").append("<table class='table table-bordered'><thead><tr><th width='100'>上课时段</th><th width='200'>周一</th><th width='200'>周二</th><th width='200'>周三</th><th width='200'>周四</th><th width='200'>周五</th><th width='200'>周六</th><th width='200'>周日</th></tr></thead><tbody id='schedule-list'></tbody</table>");
            for (i = 0;i < 15;i++)
            {
                $("#schedule-list").append("<tr class='" + i + " schedule'><td class='schedule withajaxpopover' rel='popover' title='详细时间' data-content='" + time_map[i] + "' data-placement='bottom'>" + String.fromCharCode(i + 65) + "</td><td class='Monday schedule'></td><td class='Tuesday schedule'></td><td class='Wednesday schedule'></td><td class='Thursday schedule'></td><td class='Friday schedule'></td><td class='Saturday schedule'></td><td class='Sunday schedule'></td></tr>");
                if (i == 5 || i == 11)
                  $("tr." + i).addClass("warning");
            }
            for (i = 0;i < total;i++)
            {
                var id = list[i].id;
                var courseName = list[i].name;
                var courseType = list[i].course_type;
                var credit = list[i].credit;
                var teacher = list[i].teacher;
                if (teacher.img_addr == null)
                  teacher.img_addr = "/static/img/default_user.jpg";
                if (teacher.site == null)
                  teacher.site = "#";
                var exam = list[i].exam_method;
                var period = list[i].from_week + "~" + list[i].to_week + "周";
                var course_time = list[i].course_time;
                var capacity = list[i].capacity;
                for (j = 0;j < course_time.length;j++)
                {
                    var place = list[i].place;
                    var week = course_time[j].week;
                    var time = course_time[j].time;
                    for (k = 1;k < time.length;k++)
                      $("tr." + (time.charCodeAt(k) - 65) + " td:eq(" + week + ")").remove();
                    $("tr." + (time.charCodeAt(0) - 65) + " td:eq(" + week + ")").replaceWith("<td rowspan='" + time.length + "' style='background: #d9edf7;' class='withajaxpopover' rel='popover' title='课程信息' data-content='课程类型：" + courseType + "<br>学分：" + credit + "<br>任课教师：" + teacher.teacher_name + "<br>考核方式：" + exam + "' data-placement='bottom'>" + courseName + "<br>" + place + "<br>" + period + "</td>");
                }
            }
            $("#schedule-result").append("<div id='msg-area'></div>");
        }
    });
    $("[rel = 'popover']").popover();
}
