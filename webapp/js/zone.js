
$(document).ready(function(){

    //-----------------------
    // Append data to the dom
    //-----------------------
    var id = $("#idsv").val();
    var type = $("#typesv").val();
    //console.log(id);
    
      $.ajax({
      
      url: "load_zone.php?idsv="+id+"&typesv="+type,
      method:"GET",
      dataType: 'json',
      success: function(data){
        console.log(data);
        var active = data[0].active;
        var code = data[0].sv;
        var open = data[0].open;
        var gpio = data[0].gpio;
        var nom = data[0].name;
        var seq = data[0].sequence;
        var coef = data[0].coef;
        var duree = data[0].duration;
        var numero = data[0].order;
        
        var lundi = data[0].monday;
        var mardi = data[0].tuesday;
        var mercredi = data[0].wednesday;
        var jeudi = data[0].thursday;
        var vendredi = data[0].friday;
        var samedi = data[0].saturday;
        var dimanche = data[0].sunday;
        var even = data[0].even;
        var odd = data[0].odd;
        
        //$("#modevalue").text(mode);    
        $("#sequence").val(seq);

        $("#code").val(code);
        console.log(code);
        $("#nom").val(nom);
        console.log(nom);
        
        $("#gpio").val(gpio);
        $("#gpiovalue").text(gpio);
        console.log(gpio);

        $("#duree").val(duree);
        $("#dureevalue").text(duree);
        
        $("#coef").val(coef);
        $("#coefvalue").text(coef);

        $("#numero").val(numero);
        $("#numerovalue").text(numero);

      
        if (open == 1){
          $("#open").prop('checked', true);
        }else{
          $("#open").prop('checked', false);
        }
        if (lundi == 1){
            $("#lundi").prop('checked', true);
        }else{
            $("#lundi").prop('checked', false);
        }
        if (mardi == 1){
          $("#mardi").prop('checked', true);
        }else{
          $("#mardi").prop('checked', false);
        } 
        if (mercredi == 1){
          $("#mercredi").prop('checked', true);
        }else{
          $("#mercredi").prop('checked', false);
        }
        if (jeudi == 1){
          $("#jeudi").prop('checked', true);
        }else{
          $("#jeudi").prop('checked', false);
        }
        if (vendredi == 1){
          $("#vendredi").prop('checked', true);
        }else{
          $("#vendredi").prop('checked', false);
        }
        if (samedi == 1){
          $("#samedi").prop('checked', true);
        }else{
          $("#samedi").prop('checked', false);
        }
        if (dimanche == 1){
          $("#dimanche").prop('checked', true);
        }else{
          $("#dimanche").prop('checked', false);
        }
        
        var week = lundi+mardi+mercredi+jeudi+vendredi+samedi+dimanche;
        if (week == 7){
          $("#touslesjours").prop('checked', true);
        }else{
          $("#touslesjours").prop('checked', false);
        }
        
        if (even == 1){
          $("#even").prop('checked', true);
        }else{
          $("#even").prop('checked', false);
        }
        if (odd == 1){
          $("#odd").prop('checked', true);
        }else{
          $("#odd").prop('checked', false);
        }
        if (active == 1){
          $("#active").prop('checked', true);
        }else{
          $("#active").prop('checked', false);
        }
                
      }
    });

    // update sliders value on input/change
    $("#duree").on("input",function() {
      $("#dureevalue").text(this.value);
    });

    $("#coef").on("input",function() {
      $("#coefvalue").text(this.value);
    });

    $("#numero").on("input",function() {
      $("#numerovalue").text(this.value);
    });

    $("#gpio").on("input",function() {
      $("#gpiovalue").text(this.value);
    });


    //---------------------
    // Modify global parameter
    // on Submit event
    //---------------------

    $("#formzone").submit(function(event) {
      event.preventDefault();
      var form = $(this).serialize();
      console.log("form : "+form);
      $.post("update_zone.php",form,function(data){
        console.log(data);
        if (data == "ok") {
            window.location = "arrosage.html";
          }else{
            $("#status").append("<div class='alert alert-danger'>There is an error !</div>");
          }
      });
    });
  

});
