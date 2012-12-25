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
    $("#grade-1").change(function(){
        $("#view-student-btn").trigger("click");
    });
});

function manageSchoolRoll(){
    $.ajax({
        url: '/student/getStudentList/',
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
            var students = msg.students;
            $("#student-result").empty();
            if (students.length == 0)
                $("#student-result").append("学生名单未录入。");
            else
            {
                $("#student-result").append("<table class='table table-hover table-bordered table-condensed'><thead><tr><th class='wide-block'>学号</th><th class='wide-block'>姓名</th><th class='very-wide-block'>学院</th><th class='very-wide-block'>学系</th><th class='very-wide-block'>专业</th></thead><tbody id='student-list'></tbody></table>");
                for (var i = 0;i < students.length;i++)
                {
                    $("#student-list").append("<tr><td>" + students[i].user.username + "</td><td>" + students[i].student_name + "</td><td>" + students[i].student_meta.major.speciality.department.school.name + "</td><td>" + students[i].student_meta.major.speciality.department.name + "</td><td>" + students[i].student_meta.major.speciality.name + "</tr>");
                }
                $("#student-result").append("<div class='msg-area'></div>");
            }
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
    $("#progressbar-student").text("");
    $("#progress-student").removeClass("progress-success");
    $("#progress-student").removeClass("progress-danger");
}

function uploadStudent()
{
    $("#progressbar-student").css("width","0");
    $("#progressbar-student").text("");
    $("#progress-student").removeClass("progress-success");
    $("#progress-student").removeClass("progress-danger");
    var file = document.getElementById("file-student").files[0];
    var data = new FormData();
    data.append("file-student",file);
    var filename = (file.name).split(".");
    if (filename[filename.length - 1] == "xls")
    {
        var xhr = new XMLHttpRequest();
        xhr.upload.addEventListener("progress",uploadStudentProgress,false);
        xhr.addEventListener("load",uploadStudentComplete,false);
        xhr.addEventListener("error",uploadStudentFailed,false);
        xhr.addEventListener("abort",uploadStudentCanceled,false);
        xhr.open("POST","/administrator/uploadStudentSheet/");
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        xhr.send(data);
    }
    else
    {
        $("#student-msg").removeClass("hide");
        $("#student-msg").empty();
        $("#student-msg").append("文件格式必须为*.xls");
    }
    return false;
}

function uploadStudentProgress(evt)
{
    var bar = $("#progressbar-student");
    if (evt.lengthComputable){
        var percent = Math.round(evt.loaded / evt.total * 100);
        bar.css("width",percent + "%");
        bar.attr("width",percent + "%");
        bar.text(bar.attr("width"));
    }
}

function uploadStudentComplete(evt) {
    var msg = eval("(" + evt.target.responseText + ")");
    var valid = msg.status;
    if (valid == "error")
    {
        $("#progressbar-student").text("上传失败");
        $("#progressbar-student").text("上传失败");
        $("#progress-student").addClass("progress-danger");
        $("#student-msg").removeClass("hide");
        $("#student-msg").empty();
        $("#student-msg").append("<h3>注意事项</h3><div style='margin-left:5%'><ul><li>请不要对表格模板中的格式进行任何修改</li><li>请不要对表格模板中的内容进行任何省略或缩写</li><li>请确保填写完表格模板中的所有条目</li><li>请确保每个单元格中的内容类型正确（如数值、文字等）</li></ul></div>");
    }
    else
    {
        manageSchoolRoll();
        $("#progressbar-student").text("上传成功");
        $("#progress-student").addClass("progress-success");
        $("#view-student-btn").trigger("click");
        $("#student-msg").addClass("hide");
    }
}

function uploadStudentFailed(evt) {
    alert("There was an error attempting to upload the file.");
}

function uploadStudentCanceled(evt) {
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
