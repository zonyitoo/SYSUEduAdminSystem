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
    $(".school-year option." + year).attr("selected","selected");
    $(".school-term option." + term).attr("selected","selected");
});
