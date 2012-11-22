$(document).ready(function (){
    $("#logoff").click(function (){
        //logoff();
    })
});

function logoff()
{
    $.ajax({
        url: '/user/logoff/',
		    data: 'username=' + $("#user-id").val() + "&rid=" + Math.random(),
        type: 'get',
        success: function(msg) {
            alert(msg);
            window.location = msg;
        }
    });
}
