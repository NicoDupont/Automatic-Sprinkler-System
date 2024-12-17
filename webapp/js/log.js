
$(document).ready(function(){

    //-----------------------
    // Append data to the dom
    //-----------------------
    function LoadData(){

      $.get("load_last_events.php", function(data, status){
        if (status == "success") {
          $.each(data, function(index) {
            $("#events").append('<li>'+data[index].zone+'</li>');
          });
        }
      },"json");


    }
    LoadData();


    //---------------------
    // Refresh data on click
    //---------------------

    $("#refreshdata").click(function() {
      //LoadData();
      window.location = "log.html";
    });

});
