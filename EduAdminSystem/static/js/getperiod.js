//JavaScript Document

$(document).ready(function() {
    var date = new Date()
    var year = date.getFullYear();
    var month = date.getMonth() + 1;
    var term = 0;
    if (month < 9)
        year--;
    if (month >= 9 || month < 2)
        term = 1;
    else if (month >= 2 && month < 7)
        term = 2;
    else term = 3;
    for (var i = year;i >= 2005;i--)
        $(".school-year").append("<option class='" + i + "'>" + i + "-" + (i + 1) + "</option>");
    $(".school-term option[value='" + term + "']").attr("selected","selected");
    $(".current-year").text(year + "-" + (year + 1));
    $(".current-term").text(term);
});
