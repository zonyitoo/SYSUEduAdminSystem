//JavaScript Document

$(document).ready(function(){
    $("#view-student-btn").click(function(){
        manageSchoolRoll();
    });
    $("#download-template-btn").click(function(){
        var url = "/administrator/getStudentSheet/中山大学学生名单_" + $("#school-1").val() + ".xls?school=" + $("#school-1").val();
        window.open(url);
    });
    $("#browse").click(function(){
        $("#file").trigger("click");
    });
    $("#view-student-btn").trigger("click");
    $("#school-1").change(function(){
        $("#view-student-btn").trigger("click");
    });
});

function manageSchoolRoll(){
    $.ajax({
        url: '/administrator/getStudentSheet/',
        data: 'school=' + $("#school-1").val(),
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
                $("#student-list").append("<tr><td>" + student.user.username + "</td><td>" + student.student_name + "</td><td>" + student.student_meta.major.department.school.name + "</td><td>" + student.student_meta.major.department.name + "</td><td>" + student.student_meta.major.name + "</td><td>" + attendance + "%</td><td>" + usual_score + "</td><td>" + final_score + "</td><td>" + score + "</td></tr>");
            }
            $("#student-result").append("<div class='msg-area'></div>");
        }
    });
    $("[rel = 'popover']").popover();
}

function fileSelected()
{
    var file = document.getElementById("file").files[0];
    if (file)
    {
        var file_size = 0;
        if (file.size >= 1024 * 1024)
          file_size = (Math.round(file.size * 100 / (1024 * 1024)) / 100).toString() + "MB";
        else file_size = (Math.round(file.size * 100 / 1024) / 100).toString() + "KB";
    }
    $("#path").text($("#file").val());
    $("#property").empty();
    $("#property").append("文件名称：" + file.name + "<br>文件大小：" + file_size + "<br>文件类型：" + file.type);
    $("#progressbar").css("width","0");
    $("#progressbar").removeClass("progress-success");
    $("#progressbar").text("");
}

function uploadFile()
{
    $("#progressbar").css("width","0");
    $("#progressbar").removeClass("progress-success");
    $("#progressbar").text("");
    var data = new FormData();
    data.append("file",document.getElementById("file").files[0]);
    var xhr = new XMLHttpRequest();
    xhr.upload.addEventListener("progress",uploadProgress,false);
    xhr.addEventListener("load",uploadComplete,false);
    xhr.addEventListener("error",uploadFailed,false);
    xhr.addEventListener("abort",uploadCanceled,false);
    xhr.open("POST","/administrator/uploadScoreSheet/");
    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    xhr.send(data);
    return false;
}

function uploadProgress(evt)
{
    var me = $("#progressbar");
    var total = me.attr("data-percentage");
    var current = 0;
    var progress = setInterval(function() {
        if (current >= total)
        {
            clearInterval(progress);
            me.addClass("progress-success");
        }
        else
        {
            current++;
            me.css("width",current + "%");
        }
        me.text(current + "%");
    }, 100);
}

function uploadComplete(evt) {
    var msg = eval("(" + evt.target.responseText + ")");
    var valid = msg.valid;
    if (valid == false)
    {
    }
    else
    {
        manageScore();
        $("#progress").addClass("progress-success");
    }
}
 
function uploadFailed(evt) {
    alert("There was an error attempting to upload the file.");
}

function uploadCanceled(evt) {
    alert("The upload has been canceled by the user or the browser dropped the connection.");
}

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i ++) {
      var cookie = jQuery.trim(cookies[i]);
      if (cookie.substring(0, name.length + 1) == (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
