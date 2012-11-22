$(document).ready(function (){
    $("#logout").click(function (){
        logout();
    })
});

function logout()
{
    $.ajax({
        url: '/user/logout',
		data: 'username=' + $("#user-id").val() + "&rid=" + Math.random(),
        type: 'get'
    });
}
