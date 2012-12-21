//JavaScript Document

$(document).ready(function(){
    $("#course-result").text(""); 
    $("#view-course-btn").click(function(){
        getCourse();
    });
    $(".course-type").click(function(){
        if ($("#course-result").text() != "")
        {
            $(".course-type").removeClass("active");
            $(this).addClass("active");
            getCourse();
        }
    });
});

function toggleCourse(n)
{
    var course_id = $("tr." + n + " td:eq(0)").attr("id");
    var current = $("." + n + ".btn");
    var state = 0;
    if (current.val() == "选课" || current.val() == "补选")
        state = 1;
    current.attr("disabled",true);
    if (sendRequest(n,course_id,state))
    {
        if ($("#schedule-result").text() != "")
        {
            $("#view-schedule-btn").trigger("click");
        }
        $("#view-assessment-btn").trigger("click");
        if (state == 1)
        {
            current.removeClass("btn-primary").removeClass("btn-btn-danger").removeClass("btn-success").addClass("btn-inverse");
            current.val("退筛选");
        }
        else
        {
            current.removeClass("btn-danger").removeClass("btn-success").removeClass("btn-inverse").addClass("btn-primary");
            current.val("选课");
        }
    }
    current.attr("disabled",false);
}

function getCourse()
{
    var cultivate = $("#cultivate-1 option:selected").val();
    var select_type;
    if ($("#po").hasClass("active"))
        select_type = 0;
    else if ($("#pr").hasClass("active"))
        select_type = 1;
    else if ($("#mo").hasClass("active"))
        select_type = 2;
    else if ($("#mr").hasClass("active"))
        select_type = 3;
    else if ($("#pe").hasClass("active"))
        select_type = 4;
    $.ajax({
        url: '/course/getAvailableList/',
        data: 'cultivate=' + cultivate + '&course_type=' + select_type,
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
            if (list.length == 0)
                $("#course-result").append("暂未开设该类课程。");
            else
            {
                $("#course-result").append("<table class='table table-hover table-bordered table-condensed'><thead><tr class='head'><th>课程名称</th><th class='hidden-phone'>类别</th><th class='hidden-phone'>学分</th><th>任课教师</th><th class='hidden-phone'>考核方式</th><th class='hidden-phone'>起止时间</th><th>上课时段</th><th class='hidden-phone'>上课地点</th><th class='hidden-phone'>当前人数</th><th class=''>是否选择</th></tr></thead><tbody id='course-list'></tbody</table>");
                var index,id,course_name,course_type,credit,exam,period,course_time,capacity,take,hastaken,week,time,start_time,end_time,place;
                for (var i = 0;i < list.length;i++)
                {
                    index = i + 1;
                    id = list[i].id;
                    course_name = list[i].name;
                    course_type = list[i].course_type;
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
                    $("#course-list").append("<tr class='" + index + "'><td id='"+ id + "'>" + course_name + "<a class='withajaxpopover visible-phone' rel='popover' title='课程信息' data-content='类别：" + course_type + "<br>学分：" + credit + "<br>考核方式：" + exam + "<br>起止时间：" + period + "<br>当前人数：" + hastaken + "/" + capacity + "'><i class='icon-info-sign'></i></a></td><td class='hidden-phone'>" + course_type + "</td><td class='hidden-phone'>" + credit + "</td><td><a target='_blank' href='" + teacher.site + "' class='withajaxpopover' rel='popover' data-placement='bottom' title='教师信息' data-content='姓名：" + teacher.teacher_name + "<img src=" + teacher.img_addr + " width=68 height=68 style=float:right><br>学系：" + teacher.department.name + "<br>职称：" + teacher.title + "<br>主页：" + teacher.site + "'>" + teacher.teacher_name + "</a></td><td class='hidden-phone'>" + exam + "</td><td class='hidden-phone'>" + period + "</td><td class='" + index + " course-time-1'></td><td class='" + index + " course-locate-1 hidden-phone'></td><td class='hidden-phone'>" + hastaken + "/" + capacity + "</td><td><input type='button' class='select btn btn-primary " + index + "' onclick='toggleCourse(" + index + ")' value='选课'/></td></tr>");
                    for (var j = 0;j < course_time.length;j++)
                    {
                        week = week_map[course_time[j].week];
                        time = course_time[j].time;
                        start_time = time.charCodeAt(0) - 64;
                        end_time = time.charCodeAt(time.length - 1) - 64;
                        place = course_time[j].place;
                        $("." + index + ".course-time-1").append(week + "<br>" + start_time + "~" + end_time + "节");
                        $("." + index + ".course-locate-1").append(place);
                    }
                    var current_button = $("." + index + ".btn");
                    if (take == 0)
                    {
                        current_button.removeClass("btn-danger").removeClass("btn-inverse").removeClass("btn-success").addClass("btn-primary");
                        current_button.val("选课");
                    }
                    else if (take == 1)
                    {
                        current_button.removeClass("btn-primary").removeClass("btn-inverse").removeClass("btn-success").addClass("btn-danger");
                        current_button.val("退课");
                    }
                    else if (take == 2)
                    {
                        current_button.removeClass("btn-primary").removeClass("btn-danger").removeClass("btn-inverse").addClass("btn-success");
                        current_button.val("补选");
                    }
                    else if (take == 3)
                    {
                        current_button.removeClass("btn-primary").removeClass("btn-danger").removeClass("btn-success").addClass("btn-inverse");
                        current_button.val("退筛选");
                    }
                }
                if ($(".current-state").text() == "false")
                    $(".select").attr("disabled",true);
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
            var err = msg.err;
            var hastaken = msg.hastaken;
            var msg_area = $("#course-result .msg-area");
            var name = $("td#" + course_id).text();
            if (valid == false)
            {
                msg_area.empty();
                switch (err)
                {
                    case 41:
                        msg_area.append("<div class='alert alert-error'><strong>您已选修过［" + name + "］！</strong></div>");
                        break;
                    case 42:
                        msg_area.append("<div class='alert alert-error'><strong>［" + name + "］的课程时间出现冲突！</strong></div>");
                        break;
                    case 43:
                        msg_area.append("<div class='alert alert-error'><strong>［" + name + "］的课程人数已满！</strong></div>");
                        break;
                    case 44:
                        msg_area.append("<div class='alert alert-error'><strong>学生每学期最多只能选修最多两门公共选修课！</strong></div>");
                        break;
                    default:
                        msg_area.append("<div class='alert alert-error'><strong>对［" + name + "］操作失败！</strong></div>");
                }
                msg_area.show();
                flag = false;
            }
            else
            {
                var pos = ($("#course-result tr." + n + " td:eq(8)").text()).indexOf("/");
                var total = ($("#course-result tr." + n + " td:eq(8)").text()).substring(pos + 1);
                $("#course-result tr." + n + " td:eq(8)").text(hastaken + "/" + total);
                msg_area.empty();
                msg_area.append("<div class='alert alert-success'><strong>对［" + name + "］操作成功！</strong></div>");
                msg_area.show();
                flag = true;
            }
        }
    });
    return flag;
}
