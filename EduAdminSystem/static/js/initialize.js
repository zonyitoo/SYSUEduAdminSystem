//JavaScript Document

$(document).ready(function() {
    $("#modify").on('show', function(){
        $(document).keydown(function(e){
            if (e.which == 27)
            {
                $("#modify").modal('hide');
                refresh();
            }
        });
    });
    $("#contact").on('show', function(){
        $(document).keydown(function(e){
            if (e.which == 27)
                $("#contact").modal('hide');
        });
    });
    $("#calendar").on('show', function(){
        $(document).keydown(function(e){
            if (e.which == 27)
                $("#calendar").modal('hide');
        });
    });
    $("#about").on('show', function(){
        $(document).keydown(function(e){
            if (e.which == 27)
                $("#about").modal('hide');
        });
    });
});
