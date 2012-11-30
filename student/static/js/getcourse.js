//JavaScript Document

$(document).ready(function(){
    $("#view-course-btn").click(function(){
        getCourse();
    });
});

function toggleCourse(n)
{
    var course_id = $("tr." + n + " td:eq(1)").attr("id");
    var current = $("." + n + ".btn").val();
    var state = 0;
    if (current == "选课" || current == "补选")
      state = 1;
    if (sendRequest(n,course_id,state))
    {
        if ($("#schedule-result").text() != "")
            $("#view-schedule-btn").trigger("click");
        if (state == 1)
        {
            $("." + n + ".btn").removeClass("btn-primary").removeClass("btn-btn-danger").removeClass("btn-success").addClass("btn-inverse");
            $("." + n + ".btn").val("退课(待筛选)");
        }
        else
        {
            $("." + n + ".btn").removeClass("btn-danger").removeClass("btn-success").removeClass("btn-inverse").addClass("btn-primary");
            $("." + n + ".btn").val("选课");
        }
    }
}

function getCourse()
{
    var cultivate = $("#cultivate-1 option:selected").val();
    var po = !($("#po").hasClass("active"));
    var pr = !($("#pr").hasClass("active"));
    var mo = !($("#mo").hasClass("active"));
    var mr = !($("#mr").hasClass("active"));
    $.ajax({
        url: '/course/getAvailableList/',
        data: 'cultivate=' + cultivate +'&po=' + po + '&pr=' + pr + '&mo=' + mo + '&mr=' + mr + '&school-year=' + $(".current-year").text() + '&school-term=' + $(".current-term").text(),
        datatype: 'json',
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
            var list = msg.courses;
            var week_map = new Array("世界末日","周一","周二","周三","周四","周五","周六","周日");
            $("#course-result").empty();
            $("#course-result").append("<table class='table table-hover table-bordered table-condensed'><thead><tr class='head'><th>序号</th><th class='very-wide-block'>课程名称</th><th>类别</th><th>学分</th><th>任课教师</th><th>考核方式</th><th>起止时间</th><th>上课时段</th><th>上课地点</th><th>当前人数</th><th class='wide-block'>是否选择</th></tr></thead><tbody id='course-list'></tbody</table>");
            var index,id,courseName,courseType,credit,exam,period,course_time,capacity,take,hastaken,week,time,place;
            for (var i = 0;i < list.length;i++)
            {
                index = i + 1;
                id = list[i].id;
                courseName = list[i].name;
                courseType = list[i].course_type;
                credit = list[i].credit;
                teacher = list[i].teacher;
                if (teacher.img_addr == null || teacher.img_addr == "")
                  teacher.img_addr = "/static/img/default_user.jpg";
                if (teacher.site == null)
                  teacher.site = "#";
                exam = list[i].exam_method;
                period = list[i].from_week + "~" + list[i].to_week + "周";
                course_time = list[i].course_time;
                capacity = list[i].capacity;
                take = list[i].take;
                hastaken = list[i].hastaken;
                $("#course-list").append("<tr class='" + index + "'><td>" + index + "</td><td id='"+ id + "'>" + courseName + "</td><td>" + courseType + "</td><td>" + credit + "</td><td><a target='_blank' href='" + teacher.site + "' class='withajaxpopover' rel='popover' data-placement='bottom' title='教师信息' data-content='姓名：" + teacher.teacher_name + "<img src=" + teacher.img_addr + " width=68 height=68 style=float:right><br>学系：" + teacher.department.name + "<br>职称：" + teacher.title + "<br>主页：" + teacher.site + "'>" + teacher.teacher_name + "</a></td><td>" + exam + "</td><td>" + period + "</td><td class='" + index + " course-time-1'></td><td class='" + index + " course-locate-1'></td><td>" + hastaken + "/" + capacity + "</td><td><input type='button' class='btn btn-primary " + index + "' onclick='toggleCourse(" + index + ")' value='选课'/></td></tr>");
                for (var j = 0;j < course_time.length;j++)
                {
                    week = week_map[course_time[j].week];
                    time = course_time[j].time;
                    place = course_time[j].place;
                    $("." + index + ".course-time-1").append("<a class='" + index + "'>" + week + "</a><br><a class='" + index + "'>" + time + "</a>");
                    if ($("#course-result tr." + index).hasClass(week) == false)
                       $("#course-result tr." + index).addClass(week);
                    if ($("#course-result tr." + index).hasClass(time) == false)
                        $("#course-result tr." + index).addClass(time);
                    $("#course-result a." + index).click(function() {
                        var filter = $(this).text();
                        if ($(this).hasClass("filter"))
                        {
                            $("#course-result tr:not('." + filter + "')").show();
                            $(this).removeClass("filter");
                        }
                        else
                        {
                            $("#course-result tr:not('." + filter + "')").hide();
                            $(this).addClass("filter");
                        }
                        $("#course-result tr." + filter).show();
                        $("#course-result tr.head").show();
                    });
                    $("." + index + ".course-locate-1").append(place);
                }
                if (take == 0)
                {
                    $("." + index + ".btn").removeClass("btn-danger").removeClass("btn-inverse").removeClass("btn-success").addClass("btn-primary");
                    $("." + index + ".btn").val("选课");
                }
                else if (take == 1)
                {
                    $("." + index + ".btn").removeClass("btn-primary").removeClass("btn-inverse").removeClass("btn-success").addClass("btn-danger");
                    $("." + index + ".btn").val("退课");
                }
                else if (take == 2)
                {
                    $("." + index + ".btn").removeClass("btn-primary").removeClass("btn-danger").removeClass("btn-inverse").addClass("btn-success");
                    $("." + index + ".btn").val("补选");
                }
                else
                {
                    $("." + index + ".btn").removeClass("btn-primary").removeClass("btn-danger").removeClass("btn-success").addClass("btn-inverse");
                    $("." + index + ".btn").val("退课(待筛选)");
                }
            }
            $("#course-result").append("<div class='msg-area'></div>");
        }
    });
    $("[rel = 'popover']").popover();
}

function sendRequest(n,course_id,state)
{
    var flag = false;
    $.ajax({
        url: '/student/toggleCourse/',
        data: 'course_id=' + course_id + '&state=' + state,
        datatype: 'json',
        type: 'post',
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
            flag = false;
        },
        success: function(msg,textStatus,jqXHR)
        {
            var valid = msg.valid;
            var hastaken = msg.hastaken;
            var msg_area = $("#course-result .msg-area");
            if (valid == false)
            {
                msg_area.empty();
                msg_area.append("<div class='alert alert-error'><strong>对<" + $('td#' + course_id).text() + ">操作失败！</strong></div>");
                msg_area.show();
                var t = setTimeout("msg_area.fadeOut();",5000);
                flag = false;
            }
            else
            {
                var pos = ($("#course-result tr." + n + " td:eq(9)").text()).indexOf("/");
                var total = ($("#course-result tr." + n + " td:eq(9)").text()).substring(pos + 1);
                $("#course-result tr." + n + " td:eq(9)").text(hastaken + "/" + total);
                msg_area.empty();
                msg_area.append("<div class='alert alert-success'><strong>对<" + $('td#' + course_id).text() + ">操作成功！</strong></div>");
                msg_area.show();
                var t = setTimeout("msg_area.fadeOut();",5000);
                flag = true;
            }
        }
    });
    return flag;
}
