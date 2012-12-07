//JavaScript Document

$(document).ready(function(){
    $("#view-student-btn").click(function(){
        manageSchoolRoll();
    });
    $("#download-student-template-btn").click(function(){
        var url = "/administrator/getStudentSheet/中山大学学生名单_" + $("#school-1").val() + "_" + $("#grade-1").val() + ".xls?school=" + $("#school-1").val() + "&grade=" + $("#grade-1").val();
        window.open(url);
    });
    $("#browse-student").click(function(){
        $("#file-student").trigger("click");
    });
    $("#school-1").change(function(){
        $("#view-student-btn").trigger("click");
    });
});

function manageSchoolRoll(){
    $.ajax({
        url: '/administrator/getStudentList/',
        data: 'school=' + $("#school-1").val() + "&grade=" + $("#grade-1").val(),
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
            $("#student-result").append("<table class='table table-hover table-bordered table-condensed'><thead><tr><th class='wide-block'>学号</th><th class='wide-block'>姓名</th><th class='very-wide-block'>学院</th><th class='very-wide-block'>学系</th><th class='very-wide-block'>专业</th></thead><tbody id='student-list'></tbody></table>");
            var students = msg.students;
            for (var i = 0;i < students.length;i++)
            {
                $("#student-list").append("<tr><td>" + students[i].user.username + "</td><td>" + students[i].student_name + "</td><td>" + students[i].student_meta.major.department.school.name + "</td><td>" + students[i].student_meta.major.department.name + "</td><td>" + students[i].student_meta.major.name + "</tr>");
            }
            $("#student-result").append("<div class='msg-area'></div>");
        }
    });
    $("[rel = 'popover']").popover();
}

function studentSheetSelected()
{
    var file = document.getElementById("file-student").files[0];
    if (file)
    {
        var file_size = 0;
        if (file.size >= 1024 * 1024)
          file_size = (Math.round(file.size * 100 / (1024 * 1024)) / 100).toString() + "MB";
        else file_size = (Math.round(file.size * 100 / 1024) / 100).toString() + "KB";
    }
    $("#path-student").text($("#file-student").val());
    $("#property-student").empty();
    $("#property-student").append("文件名称：" + file.name + "<br>文件大小：" + file_size + "<br>文件类型：" + file.type);
    $("#progressbar-student").css("width","0");
    $("#progressbar-student").removeClass("progress-success");
    $("#progressbar-student").text("");
}

function uploadStudent()
{
    $("#progressbar-student").css("width","0");
    $("#progressbar-student").removeClass("progress-success");
    $("#progressbar-student").text("");
    var data = new FormData();
    data.append("file",document.getElementById("file-student").files[0]);
    var xhr = new XMLHttpRequest();
    xhr.upload.addEventListener("progress",uploadProgress,false);
    xhr.addEventListener("load",uploadComplete,false);
    xhr.addEventListener("error",uploadFailed,false);
    xhr.addEventListener("abort",uploadCanceled,false);
    xhr.open("POST","/administrator/uploadStudentSheet/");
    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    xhr.send(data);
    return false;
}

function uploadProgress(evt)
{
    var bar = $("#progressbar-student");
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
        manageSchoolRoll();
        $("#progress-student").addClass("progress-success");
        $("#view-student-btn").trigger("click");
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
