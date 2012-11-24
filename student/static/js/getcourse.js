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
}
