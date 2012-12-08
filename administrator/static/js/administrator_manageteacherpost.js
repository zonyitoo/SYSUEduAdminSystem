//JavaScript Document

$(document).ready(function(){
    $("#view-teacher-btn").click(function(){
        manageTeacherPost();
    });
    $("#download-teacher-template-btn").click(function(){
        var url = "/administrator/getTeacherSheet/中山大学教师名单_" + $("#school-1").val() + ".xls?school=" + $("#school-2").val();
        window.open(url);
    });
    $("#browse-teacher").click(function(){
        $("#file-teacher").trigger("click");
    });
    $("#school-2").change(function(){
        $("#view-teacher-btn").trigger("click");
    });
});

function manageTeacherPost(){
    $.ajax({
        url: '/teacher/getTeacherList/',
        data: 'school=' + $("#school-2").val(),
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
            $("#teacher-result").empty();
            $("#teacher-result").append("<table class='table table-hover table-bordered table-condensed'><thead><tr><th class='wide-block'>工号</th><th class='wide-block'>姓名</th><th class='wide-block'>职称</th><th class='very-wide-block'>学院</th><th class='very-wide-block'>学系</th></thead><tbody id='teacher-list'></tbody></table>");
            var teachers = msg.teachers;
            for (var i = 0;i < teachers.length;i++)
            {
                $("#teacher-list").append("<tr><td>" + teachers[i].user.username + "</td><td>" + teachers[i].teacher_name + "</td><td>" + teachers[i].title + "</td><td>" + teachers[i].department.school.name + "</td><td>" + teachers[i].department.name + "</tr>");
            }
            $("#teacher-result").append("<div class='msg-area'></div>");
        }
    });
    $("[rel = 'popover']").popover();
}

function teacherSheetSelected()
{
    var file = document.getElementById("file-teacher").files[0];
    if (file)
    {
        var file_size = 0;
        if (file.size >= 1024 * 1024)
          file_size = (Math.round(file.size * 100 / (1024 * 1024)) / 100).toString() + "MB";
        else file_size = (Math.round(file.size * 100 / 1024) / 100).toString() + "KB";
    }
    $("#path-teacher").text($("#file-teacher").val());
    $("#property-teacher").empty();
    $("#property-teacher").append("文件名称：" + file.name + "<br>文件大小：" + file_size + "<br>文件类型：" + file.type);
    $("#progressbar-teacher").css("width","0");
    $("#progressbar-teacher").removeClass("progress-success");
    $("#progressbar-teacher").text("");
}

function uploadStudent()
{
    $("#progressbar-teacher").css("width","0");
    $("#progressbar-teacher").removeClass("progress-success");
    $("#progressbar-teacher").text("");
    var data = new FormData();
    data.append("file",document.getElementById("file-teacher").files[0]);
    var xhr = new XMLHttpRequest();
    xhr.upload.addEventListener("progress",uploadProgress,false);
    xhr.addEventListener("load",uploadComplete,false);
    xhr.addEventListener("error",uploadFailed,false);
    xhr.addEventListener("abort",uploadCanceled,false);
    xhr.open("POST","/administrator/uploadTeacherSheet/");
    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    xhr.send(data);
    return false;
}

function uploadProgress(evt)
{
    var bar = $("#progressbar-teacher");
    if (evt.lengthComputable){
        var percent = Math.round(evt.loaded / evt.total * 100);
        bar.css("width",percent + "%");
        bar.attr("width",percent + "%");
        bar.text(bar.attr("width"));
    }
}

function uploadComplete(evt) {
    var msg = eval("(" + evt.target.responseText + ")");
    var valid = msg.valid;
    if (valid == false)
    {
    }
    else
    {
        manageTeacherPost();
        $("#progress-teacher").addClass("progress-success");
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
