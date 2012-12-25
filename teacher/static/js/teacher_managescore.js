//JavaScript Document

$(document).ready(function(){
    $("#view-student-btn").click(function(){
        manageScore();
    });
    $("#download-template-btn").click(function(){
        var url = "/teacher/getScoreSheet/中山大学学生成绩录入模板_" + $("#course-2").val() + ".xls?course=" + $("#course-2").val();
        window.open(url);
    });
    $("#browse").click(function(){
        $("#file").trigger("click");
    });
    $("#view-student-btn").trigger("click");
    $("#course-2").change(function(){
        $("#view-student-btn").trigger("click");
    });
});

function manageScore(){
    $.ajax({
        url: '/teacher/getTakenInfoList/',
        data: 'course=' + $("#course-2").val(),
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
            var takes = msg.takes;
            $("#student-result").empty();
            if (takes.length == 0)
                $("#student-result").append("暂无学生选课。");
            else
            {
                $("#student-result").append("<table class='table table-hover table-bordered table-condensed'><thead><tr><th>学号</th><th>姓名</th><th>学院</th><th>学系</th><th>专业</th><th>出勤率</th><th>平时成绩</th><th>期末成绩</th><th>总评</th><th>排名</th></tr></thead><tbody id='student-list'></tbody></table>");
                var course,student,school,major,usual_score,final_score,score;
                for (var i = 0;i < takes.length;i++)
                {
                    course = takes[i].course;
                    student = takes[i].student;
                    attendance = takes[i].attendance;
                    usual_score = takes[i].usual_score;
                    final_score = takes[i].final_score;
                    score = takes[i].score;
                    rank = takes[i].rank;
                    $("#student-list").append("<tr><td>" + student.user.username + "</td><td>" + student.student_name + "</td><td>" + student.student_meta.major.speciality.department.school.name + "</td><td>" + student.student_meta.major.speciality.department.name + "</td><td>" + student.student_meta.major.speciality.name + "</td><td>" + attendance + "%</td><td>" + usual_score + "</td><td>" + final_score + "</td><td>" + score + "</td><td>"+ rank +"</td></tr>");
                }
                $("#student-result").append("<div class='msg-area'></div>");
            }
            if ($(".current-state").text() == "false")
                $("#upload-score-btn").attr("disabled",true);
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
    $("#progressbar").text("");
    $("#progress").removeClass("progress-success");
    $("#progress").removeClass("progress-danger");
}

function uploadFile()
{
    $("#progressbar").css("width","0");
    $("#progressbar").text("");
    $("#progress").removeClass("progress-success");
    $("#progress").removeClass("progress-danger");
    var data = new FormData();
    data.append("file",document.getElementById("file").files[0]);
    var filename = ($("#file").val()).split(".");
    if (filename[filename.length - 1] == "xls")
    {
        var xhr = new XMLHttpRequest();
        xhr.upload.addEventListener("progress",uploadProgress,false);
        xhr.addEventListener("load",uploadComplete,false);
        xhr.addEventListener("error",uploadFailed,false);
        xhr.addEventListener("abort",uploadCanceled,false);
        xhr.open("POST","/teacher/uploadScoreSheet/");
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        xhr.send(data);
    }
    else
    {
        $("#score-msg").removeClass("hide");
        $("#score-msg").empty();
        $("#score-msg").append("文件格式必须为*.xls");
    }
    return false;
}

function uploadProgress(evt)
{
    var bar = $("#progressbar");
    if (evt.lengthComputable){
        var percent = Math.round(evt.loaded / evt.total * 100);
        bar.css("width",percent + "%");
        bar.attr("width",percent + "%");
        bar.text(bar.attr("width"));
    }
}

function uploadComplete(evt) {
    var msg = eval("(" + evt.target.responseText + ")");
    var valid = msg.status;
    if (valid == "error")
    {
        $("#progressbar").text("上传失败");
        $("#progress").addClass("progress-danger");
        $("#score-msg").removeClass("hide");
        $("#score-msg").empty();
        $("#score-msg").append("<h3>注意事项</h3><div style='margin-left:5%'><ul><li>请不要对表格模板中的格式进行任何修改</li><li>请不要对表格模板中的内容进行任何省略或缩写</li><li>请确保填写完表格模板中的所有条目</li><li>请确保每个单元格中的内容类型正确（如数值、文字等）</li></ul></div>");
    }
    else
    {
        manageScore();
        $("#progressbar").text("上传成功");
        $("#progress").addClass("progress-success");
        $("#score-msg").addClass("hide");
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
