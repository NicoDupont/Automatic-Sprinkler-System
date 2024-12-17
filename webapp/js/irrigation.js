
$(document).ready(function(){

    //-----------------------
    // Append data to the dom
    //-----------------------
    function LoadData(){

      $.get("load_parameter.php", function(data, status){
          if (status == "success") {
            
            //---------------------
            // Add a message error if needeed
            //---------------------
            var mode = data[0].mode;
           
            if (mode == 'Manuel' || mode == 'Domotique') {
                $("#status").append("<div class='alert alert-danger'>Irrigation en mode Manuel / Domotique</div>");
            }
            if (mode == 'Hivernage' || mode == 'Stop') {
              $("#status").append("<div class='alert alert-danger'>Irrigation en mode Hiver/Stop</div>");
            }
            if (mode == 'Test') {
              $("#status").append("<div class='alert alert-danger'>Irrigation en mode Test</div>");
            }

          }
        },"json");

      $.get("load_last_events.php", function(data, status){
        if (status == "success") {
          $.each(data, function(index) {
            $("#events").append('<li>'+data[index].zone+'</li>');
          });
        }
      },"json");

      $.get("load_sequence_zone.php", function(data, status){
        if (status == "success") {
          $.each(data, function(index) {
            $("#sequence").append('<li>'+data[index].seq+'</li>');
          });
        }
      },"json");


      $.get("load_zone.php", function(data, status){
        if (status == "success") {
          $.each(data, function(index) {

            if (data[index].manual == 1){
              var manual = '<span class="svred">Manuel</span>';
            }else{
              var manual = '<span class="svgray">Manuel</span>';
            }

            if (data[index].active == 1){
              var active = '';
            }else{
              var active = '';
            } 

            if (data[index].active == 0){
              var open = 'style="background-color:#FC5642; border-color:#FC5642"';
            }else if (data[index].open == 1){
              var open = 'style="background-color:#338d59; border-color:#338d59"'; 
            }else{
              var open = 'style="background-color:#027ac5; border-color:#027ac5"'; 
            }

            if (data[index].monday == 1 && data[index].even==0 && data[index].odd==0){
              var l = '<span class="svred">L</span>';
            }else{
              var l = '<span class="svgray">L</span>';
            } 

            if (data[index].tuesday == 1 && data[index].even==0 && data[index].odd==0){
              var m = '<span class="svred">M</span>';
            }else{
              var m = '<span class="svgray">M</span>';
            } 

            if (data[index].wednesday == 1 && data[index].even==0 && data[index].odd==0){
              var me = '<span class="svred">M</span>';
            }else{
              var me = '<span class="svgray">M</span>';
            } 

            if (data[index].friday == 1 && data[index].even==0 && data[index].odd==0){
              var v = '<span class="svred">V</span>';
            }else{
              var v = '<span class="svgray">V</span>';
            }

            if (data[index].thursday == 1 && data[index].even==0 && data[index].odd==0){
              var j = '<span class="svred">J</span>';
            }else{
              var j = '<span class="svgray">J</span>';
            }

            if (data[index].saturday == 1 && data[index].even==0 && data[index].odd==0){
              var s = '<span class="svred">S</span>';
            }else{
              var s = '<span class="svgray">S</span>';
            }

            if (data[index].sunday == 1 && data[index].even==0 && data[index].odd==0){
              var d = '<span class="svred">D</span>';
            }else{
              var d = '<span class="svgray">D</span>';
            }

            if (data[index].even==1){
              var even = '<span class="svred">2</span>';
            }else{
              var even = '<span class="svgray">2</span>';
            } 

            if (data[index].odd==1){
              var odd = '<span class="svred">1</span>';
            }else{
              var odd = '<span class="svgray">1</span>';
            } 

            var idsv = data[index].id_sv;
            var typesv = data[index].type_sv;
            var dur = data[index].duration;
            var coeff = data[index].coef;
            var seq = data[index].sequence;

            $("#sv").append('<li class="lizone"'+open+' ><div class="row"><div class="col-10"><div class="row"><div class="col-12">'+data[index].sv+' | <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-play-fill" viewBox="0 0 16 16"> <path d="m11.596 8.697-6.363 3.692c-.54.313-1.233-.066-1.233-.697V4.308c0-.63.692-1.01 1.233-.696l6.363 3.692a.802.802 0 0 1 0 1.393z"/> </svg> '+seq+' | '+data[index].name+'</div></div><div class="row"><div class="col-12 ">  # '+data[index].order+'  |  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-cpu" viewBox="0 0 16 16"><path d="M5 0a.5.5 0 0 1 .5.5V2h1V.5a.5.5 0 0 1 1 0V2h1V.5a.5.5 0 0 1 1 0V2h1V.5a.5.5 0 0 1 1 0V2A2.5 2.5 0 0 1 14 4.5h1.5a.5.5 0 0 1 0 1H14v1h1.5a.5.5 0 0 1 0 1H14v1h1.5a.5.5 0 0 1 0 1H14v1h1.5a.5.5 0 0 1 0 1H14a2.5 2.5 0 0 1-2.5 2.5v1.5a.5.5 0 0 1-1 0V14h-1v1.5a.5.5 0 0 1-1 0V14h-1v1.5a.5.5 0 0 1-1 0V14h-1v1.5a.5.5 0 0 1-1 0V14A2.5 2.5 0 0 1 2 11.5H.5a.5.5 0 0 1 0-1H2v-1H.5a.5.5 0 0 1 0-1H2v-1H.5a.5.5 0 0 1 0-1H2v-1H.5a.5.5 0 0 1 0-1H2A2.5 2.5 0 0 1 4.5 2V.5A.5.5 0 0 1 5 0zm-.5 3A1.5 1.5 0 0 0 3 4.5v7A1.5 1.5 0 0 0 4.5 13h7a1.5 1.5 0 0 0 1.5-1.5v-7A1.5 1.5 0 0 0 11.5 3h-7zM5 6.5A1.5 1.5 0 0 1 6.5 5h3A1.5 1.5 0 0 1 11 6.5v3A1.5 1.5 0 0 1 9.5 11h-3A1.5 1.5 0 0 1 5 9.5v-3zM6.5 6a.5.5 0 0 0-.5.5v3a.5.5 0 0 0 .5.5h3a.5.5 0 0 0 .5-.5v-3a.5.5 0 0 0-.5-.5h-3z"/></svg> '+data[index].gpio+'   |     <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-clock" viewBox="0 0 16 16"><path d="M8 3.5a.5.5 0 0 0-1 0V9a.5.5 0 0 0 .252.434l3.5 2a.5.5 0 0 0 .496-.868L8 8.71V3.5z"/><path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm7-8A7 7 0 1 1 1 8a7 7 0 0 1 14 0z"/></svg> '+dur+' | <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-percent" viewBox="0 0 16 16"><path d="M13.442 2.558a.625.625 0 0 1 0 .884l-10 10a.625.625 0 1 1-.884-.884l10-10a.625.625 0 0 1 .884 0zM4.5 6a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm0 1a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5zm7 6a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm0 1a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5z"/></svg>'+coeff+' </div></div><div class="row"><div class="col-12">'+l+'   '+m+'   '+me+'   '+j+'   '+v+'   '+s+'   '+d+'  |  '+odd+'   '+even+' </div></div></div><div class="col-2" style="padding-top: 15px;"><a href="zone.php?zone='+idsv+'&type='+typesv+'" class="btn btn-link btn-sm" role="button" name="updatesv"><svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-gear" viewBox="0 0 16 16"><path d="M8 4.754a3.246 3.246 0 1 0 0 6.492 3.246 3.246 0 0 0 0-6.492zM5.754 8a2.246 2.246 0 1 1 4.492 0 2.246 2.246 0 0 1-4.492 0z"/><path d="M9.796 1.343c-.527-1.79-3.065-1.79-3.592 0l-.094.319a.873.873 0 0 1-1.255.52l-.292-.16c-1.64-.892-3.433.902-2.54 2.541l.159.292a.873.873 0 0 1-.52 1.255l-.319.094c-1.79.527-1.79 3.065 0 3.592l.319.094a.873.873 0 0 1 .52 1.255l-.16.292c-.892 1.64.901 3.434 2.541 2.54l.292-.159a.873.873 0 0 1 1.255.52l.094.319c.527 1.79 3.065 1.79 3.592 0l.094-.319a.873.873 0 0 1 1.255-.52l.292.16c1.64.893 3.434-.902 2.54-2.541l-.159-.292a.873.873 0 0 1 .52-1.255l.319-.094c1.79-.527 1.79-3.065 0-3.592l-.319-.094a.873.873 0 0 1-.52-1.255l.16-.292c.893-1.64-.902-3.433-2.541-2.54l-.292.159a.873.873 0 0 1-1.255-.52l-.094-.319zm-2.633.283c.246-.835 1.428-.835 1.674 0l.094.319a1.873 1.873 0 0 0 2.693 1.115l.291-.16c.764-.415 1.6.42 1.184 1.185l-.159.292a1.873 1.873 0 0 0 1.116 2.692l.318.094c.835.246.835 1.428 0 1.674l-.319.094a1.873 1.873 0 0 0-1.115 2.693l.16.291c.415.764-.42 1.6-1.185 1.184l-.291-.159a1.873 1.873 0 0 0-2.693 1.116l-.094.318c-.246.835-1.428.835-1.674 0l-.094-.319a1.873 1.873 0 0 0-2.692-1.115l-.292.16c-.764.415-1.6-.42-1.184-1.185l.159-.291A1.873 1.873 0 0 0 1.945 8.93l-.319-.094c-.835-.246-.835-1.428 0-1.674l.319-.094A1.873 1.873 0 0 0 3.06 4.377l-.16-.292c-.415-.764.42-1.6 1.185-1.184l.292.159a1.873 1.873 0 0 0 2.692-1.115l.094-.319z"/></svg></a></div></div></li>');
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
      window.location = "arrosage.html";
    });

});
