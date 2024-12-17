
$(document).ready(function(){

    //-----------------------
    // Append data to the dom
    //-----------------------
    //const queryString = window.location.search;
    //const urlParams = new URLSearchParams(queryString);
    //const seqval = urlParams.get('sequence')
    //console.log(seq);
    //$("#seqid").val(seqval);
    var seq = $("#seqid").val();
    //console.log(seq);
    
      $.ajax({
      
      url: "load_sequence.php?sequence="+seq,
      method:"GET",
      dataType: 'json',
      success: function(data){
        console.log(data);
        var active = data[0].active;
        var sequence = data[0].sequence;
        var heure = data[0].heure;
        var minute = data[0].minute;
        
        //$("#modevalue").text(mode);    
        $("#sequence").val(sequence);
        $("#heure").val(heure);
        $("#heurevalue").text(heure);
        $("#minute").val(minute);
        $("#minutevalue").text(minute);
        if (active == 1){
          $("#active").prop('checked', true);
        }else{
          $("#active").prop('checked', false);
        }
                
      }
    });

    // update sliders value on input/change
    $("#heure").on("input",function() {
      $("#heurevalue").text(this.value);
    });

    $("#minute").on("input",function() {
      $("#minutevalue").text(this.value);
    });

    //---------------------
    // Modify sequence
    // on Submit event
    //---------------------

    $("#formseq").submit(function(event) {
      event.preventDefault();
      var form = $(this).serialize();
      console.log("form : "+form);
      $.post("update_sequence.php",form,function(data){
        console.log(data);
        if (data == "ok") {
            window.location = "arrosage.html";
          }else{
            $("#status").append("<div class='alert alert-danger'>There is an error !</div>");
          }
      });
    });
  

});
