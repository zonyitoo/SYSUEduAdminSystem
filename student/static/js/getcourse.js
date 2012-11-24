//JavaScript Document

$(document).ready(function(){
    $("#view-course-btn").click(function(){
        getCourse();
    });
});

function getCourse()
{
    var cultivate = document.getElementById("cultivate-1").selectedIndex;
    var po = !($("#po").hasClass("active"));
    var pr = !($("#pr").hasClass("active"));
    var mo = !($("#mo").hasClass("active"));
    var mr = !($("#mr").hasClass("active"));
    $.ajax({
        url: '/course/getAvailableList/',
        data: 'cultivate=' + cultivate +'&po=' + po + '&pr=' + pr + '&mo=' + mo + '&mr=' + mr,
        datatype: 'json',
        type: 'get',
        error: function()
        {
            alert("链接服务器错误！");
        },
        success: function(msg)
        {
            var total = msg.length;            
            alert(total);
        }
    });
    $("#course-result").append("<table class='table table-bordered table-condensed'><thead><tr><th>序号</th><th width='200'>课程名称</th><th>类别</th><th>学分</th><th>任课教师</th><th>考核方式</th><th>起止时间</th><th>上课时段</th><th width='100'>剩余容量</th><th>是否选择</th></tr></thead></table>");
}
