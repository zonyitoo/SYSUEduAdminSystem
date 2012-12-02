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
        data: 'school-year=' + $("#school-year-3").val() + '&school-term=' + $("#school-term-3 option:selected").val(),
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
            var i,j,k;
            var list = msg.courses;
            var week_map = new Array("Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday");
            var time_map = new Array("08:00~08:45","08:55~09:40","09:50~10:35","10:45~11:30","11:40~12:25","12:35~13:20","13:30~14:15","14:25~15:10","15:20~16:05","16:15~17:00","17:10~17:55","18:05~18:50","19:00~19:45","19:55~20:40","20:50~21:35");
            $("#schedule-result").empty();
            $("#schedule-result").append("<table class='table table-bordered'><thead><tr><th class='time medium-block'>上课时段</th><th class='week Monday wide-block'>周一</th><th class='week Tuesday wide-block'>周二</th><th class='week Wednesday wide-block'>周三</th><th class='week Thursday wide-block'>周四</th><th class='week Friday wide-block'>周五</th><th class='week Saturday wide-block'>周六</th><th class='week Sunday wide-block'>周日</th></tr></thead><tbody id='schedule-list'></tbody</table>");
            var date = new Date();
            var today = date.getDay();
            var filter = week_map[today];
            if (today == 0)
              today = 7;
            for (i = 0;i < 15;i++)
            {
                $("#schedule-list").append("<tr class='" + i + " schedule'><td class='time schedule withajaxpopover' rel='popover' title='详细时间' data-content='" + time_map[i] + "'>" + (i + 1) + "</td><td class='week Monday schedule'></td><td class='week Tuesday schedule'></td><td class='week Wednesday schedule'></td><td class='week Thursday schedule'></td><td class='week Friday schedule'></td><td class='week Saturday schedule'></td><td class='week Sunday schedule'></td></tr>");
                if (i == 5 || i == 11)
                  $("tr." + i).addClass("warning");
            }
            for (i = 1;i <= 7;i++)
            {
                if (i != today)
                {
                    $("tr th:eq(" + i + ")").addClass("hidden-phone");
                    $("tr").find("td:eq(" + i + ")").addClass("hidden-phone");
                }
            }
            var id,course_name,course_type,credit,teacher,exam,period,course_time,capacity,week,time,place;
            for (i = 0;i < list.length;i++)
            {
                id = list[i].id;
                course_name = list[i].name;
                course_type = list[i].course_type;
                credit = list[i].credit;
                teacher = list[i].teacher;
                if (teacher.img_addr == null)
                  teacher.img_addr = "/static/img/default_user.jpg";
                if (teacher.site == null)
                  teacher.site = "#";
                exam = list[i].exam_method;
                period = list[i].from_week + "~" + list[i].to_week + "周";
                course_time = list[i].course_time;
                capacity = list[i].capacity;
                for (j = 0;j < course_time.length;j++)
                {
                    place = course_time[j].place;
                    week = course_time[j].week;
                    time = course_time[j].time;
                    for (k = 1;k < time.length;k++)
                      $("#schedule-result tr." + (time.charCodeAt(k) - 65) + " td:eq(" + week + ")").remove();
                    $("#schedule-result tr." + (time.charCodeAt(0) - 65) + " td:eq(" + week + ")").replaceWith("<td rowspan='" + time.length + "' style='background: #d9edf7;' class='current week withajaxpopover schedulepop' rel='popover' title='课程信息' data-content='课程类型：" + course_type + "<br>学分：" + credit + "<br>任课教师：" + teacher.teacher_name + "<br>考核方式：" + exam + "' data-placement='bottom'>" + course_name + "<br>" + place + "<br>" + period + "</td>");
                    if (week != today)
                      $(".current").addClass("hidden-phone");
                    $(".current").removeClass("current");
                }
            }
            $("#schedule-result").append("<div class='msg-area'></div>");
        }
    });
    $("[rel = 'popover']").popover();
}
