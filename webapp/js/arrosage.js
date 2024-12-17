
$(document).ready(function(){

    //-----------------------
    // Append data to the dom
    //-----------------------
    function LoadData(){

      $.get("load_parameter.php", function(data, status){
          if (status == "success") {
            //---------------------
            // Add a message error 
            //---------------------
            var mode = data[0].mode;
           
            if (mode == 'Manuel' || mode == 'Domotique') {
                $("#status").append("<div class='alert alert-danger'>Irrigation en mode Manuel !</div>");
            }
            if (mode == 'Hivernage' || mode == 'Stop') {
              $("#status").append("<div class='alert alert-danger'>Irrigation en mode Stop !</div>");
            }
            if (mode == 'Test') {
              $("#status").append("<div class='alert alert-danger'>Irrigation en mode Test !</div>");
            }
            if (mode == 'Auto') {
              $("#status").append("<div class='alert alert-success' role='alert'>Irrigation en mode Automatique</div>");
            }
            if (mode == 'Demande') {
              $("#status").append("<div class='alert alert-warning' role='alert'>Irrigation en mode à la Demande !</div>");
            }
            if (mode == '') {
              $("#status").append("<div class='alert alert-danger'>ATTENTION PAS DE MODE PARAMETRE !!!!</div>");
            }

          }
        },"json");

      $.get("load_last_events.php?type=sv", function(data, status){
        if (status == "success") {
          $.each(data, function(index) {
           
              if (data[index].val4.trim().substring(0, 15) == 'Désactivation'){
                var open = 'style="background-color:#FC5642; border-color:#FC5642"'; 
              }else if (data[index].val4.trim().substring(0, 15) == 'Activation'){
                var open = 'style="background-color:#027ac5; border-color:#027ac5"'; 
              }
              $("#eventszone").append('<li class="lizone"'+open+' >'+data[index].dateeve+' - '+data[index].val1+' - '+data[index].val3+' - '+data[index].val4.trim().substring(0, 15)+'</li>');        
          });
        }
      },"json");

      $.get("load_last_events.php?type=other", function(data, status){
        if (status == "success") {
          $.each(data, function(index) {
            if (data[index].val5.trim() == 'mqtt'){
                var open = 'style="background-color:#58CE95; border-color:#58CE95"';
                $("#eventsother").append('<li class="lizone"'+open+' >Mqtt - '+data[index].dateeve+' - '+data[index].val1+' - '+data[index].val2+'</li>');
            }else if (data[index].val5.trim() == 'ano'){
                var open = 'style="background-color:#CEB058; border-color:#CEB058"';
                $("#eventsother").append('<li class="lizone"'+open+' >Ano - '+data[index].dateeve+' - '+data[index].val1+' - '+data[index].val2+'</li>');
            }
            
          });
        }
      },"json");

      $.get("load_sequence_zone.php", function(data, status){
        if (status == "success") {
          $.each(data, function(index) {
            if (data[index].open == 0 && data[index].planned==0){
              var open = 'style="text-decoration: line-through; background-color: #C0782F; border-color:#C0782F"'; 
            }
            else if (data[index].open == 0 && data[index].reste==0){
              var open = 'style="background-color:#908F8E; border-color:#908F8E"'; 
            }
            else if (data[index].open == 1){
              var open = 'style="background-color:#338d59; border-color:#338d59"'; 
            }else{
              var open = 'style="background-color:#027ac5; border-color:#027ac5"'; 
            }
            $("#sequence").append('<li class="lizone"'+open+' >'+data[index].seq+' <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-hourglass-split" viewBox="0 0 16 16"><path d="M2.5 15a.5.5 0 1 1 0-1h1v-1a4.5 4.5 0 0 1 2.557-4.06c.29-.139.443-.377.443-.59v-.7c0-.213-.154-.451-.443-.59A4.5 4.5 0 0 1 3.5 3V2h-1a.5.5 0 0 1 0-1h11a.5.5 0 0 1 0 1h-1v1a4.5 4.5 0 0 1-2.557 4.06c-.29.139-.443.377-.443.59v.7c0 .213.154.451.443.59A4.5 4.5 0 0 1 12.5 13v1h1a.5.5 0 0 1 0 1zm2-13v1c0 .537.12 1.045.337 1.5h6.326c.216-.455.337-.963.337-1.5V2zm3 6.35c0 .701-.478 1.236-1.011 1.492A3.5 3.5 0 0 0 4.5 13s.866-1.299 3-1.48zm1 0v3.17c2.134.181 3 1.48 3 1.48a3.5 3.5 0 0 0-1.989-3.158C8.978 9.586 8.5 9.052 8.5 8.351z"/></svg> '+data[index].reste+' Min </li>');
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

      $.get("load_sequence.php", function(data, status){
        if (status == "success") {
          //console.log("succes sequence");
          $.each(data, function(index) {
            
            if (data[index].active == 0){
              var open = 'style="background-color:#FC5642; border-color:#FC5642"';
            }else if (data[index].open == 1){
              var open = 'style="background-color:#338d59; border-color:#338d59"'; 
            }else{
              var open = 'style="background-color:#027ac5; border-color:#027ac5"'; 
            }


            var seq = data[index].seq;
            var heure = data[index].heure;
            var minute = data[index].minute;

            $("#seq").append('<li class="liseq"'+open+'><div class="row"><div class="col-10" style="padding-top: 9px;"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-play-fill" viewBox="0 0 16 16"> <path d="m11.596 8.697-6.363 3.692c-.54.313-1.233-.066-1.233-.697V4.308c0-.63.692-1.01 1.233-.696l6.363 3.692a.802.802 0 0 1 0 1.393z"/> </svg> '+seq+' | <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-clock" viewBox="0 0 16 16"><path d="M8 3.5a.5.5 0 0 0-1 0V9a.5.5 0 0 0 .252.434l3.5 2a.5.5 0 0 0 .496-.868L8 8.71z"/><path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16m7-8A7 7 0 1 1 1 8a7 7 0 0 1 14 0"/></svg> '+heure+' H : '+minute+' Min</div><div class="col-2"> <div style="padding-top: 0px;"><a href=sequence.php?sequence='+seq+' class="btn btn-link btn-sm" role="button" name="updatesv"><svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-gear" viewBox="0 0 16 16"><path d="M8 4.754a3.246 3.246 0 1 0 0 6.492 3.246 3.246 0 0 0 0-6.492zM5.754 8a2.246 2.246 0 1 1 4.492 0 2.246 2.246 0 0 1-4.492 0z"/><path d="M9.796 1.343c-.527-1.79-3.065-1.79-3.592 0l-.094.319a.873.873 0 0 1-1.255.52l-.292-.16c-1.64-.892-3.433.902-2.54 2.541l.159.292a.873.873 0 0 1-.52 1.255l-.319.094c-1.79.527-1.79 3.065 0 3.592l.319.094a.873.873 0 0 1 .52 1.255l-.16.292c-.892 1.64.901 3.434 2.541 2.54l.292-.159a.873.873 0 0 1 1.255.52l.094.319c.527 1.79 3.065 1.79 3.592 0l.094-.319a.873.873 0 0 1 1.255-.52l.292.16c1.64.893 3.434-.902 2.54-2.541l-.159-.292a.873.873 0 0 1 .52-1.255l.319-.094c1.79-.527 1.79-3.065 0-3.592l-.319-.094a.873.873 0 0 1-.52-1.255l.16-.292c.893-1.64-.902-3.433-2.541-2.54l-.292.159a.873.873 0 0 1-1.255-.52l-.094-.319zm-2.633.283c.246-.835 1.428-.835 1.674 0l.094.319a1.873 1.873 0 0 0 2.693 1.115l.291-.16c.764-.415 1.6.42 1.184 1.185l-.159.292a1.873 1.873 0 0 0 1.116 2.692l.318.094c.835.246.835 1.428 0 1.674l-.319.094a1.873 1.873 0 0 0-1.115 2.693l.16.291c.415.764-.42 1.6-1.185 1.184l-.291-.159a1.873 1.873 0 0 0-2.693 1.116l-.094.318c-.246.835-1.428.835-1.674 0l-.094-.319a1.873 1.873 0 0 0-2.692-1.115l-.292.16c-.764.415-1.6-.42-1.184-1.185l.159-.291A1.873 1.873 0 0 0 1.945 8.93l-.319-.094c-.835-.246-.835-1.428 0-1.674l.319-.094A1.873 1.873 0 0 0 3.06 4.377l-.16-.292c-.415-.764.42-1.6 1.185-1.184l.292.159a1.873 1.873 0 0 0 2.692-1.115l.094-.319z"/></svg></div></div></div></li>');

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

    //---------------------
    // bilboard grah based on d3js
    //---------------------

    $.get("load_kpi.php", function(data, status){
      if (status == "success") {
        
        var amont = "Amont";
        var aval = "Aval";
        var pcaam = 0;
        var pcaav = 0;
        var pcuam = 0;
        var pcuav = 0;
        var debcuve = 0;
        var debarr = 0;
        var pdcuve = 0;
        var pdcanal = 0;
        
        $.each(data, function(index) {
          if (data[index].sensor == 'Pression Eau Canal Amont'){
            pcaam = data[index].mesure;
          }else if (data[index].sensor == 'Pression Eau Canal Aval'){
                  pcaav = data[index].mesure;
          }else if (data[index].sensor == 'Pression Eau Cuve Amont'){
                  pcuam = data[index].mesure;
          }else if (data[index].sensor == 'Pression Eau Cuve Aval'){
                  pcuav = data[index].mesure;
          }else if (data[index].sensor == 'Debimetre Cuve'){
                  debcuve = data[index].mesure;
          }else if (data[index].sensor == 'Debimetre Arrosage'){
                  debarr = data[index].mesure;
          }else if (data[index].sensor == 'Pression Differentielle Cuve'){
                  pdcuve = data[index].mesure;
          }else if (data[index].sensor == ' Pression Differentielle Canal'){
                  pdcanal = data[index].mesure;
          }
        });
        //---------------------------------------------------------
        //---------------------------------------------------------
        //---------------------------------------------------------
        // gauge pression canal
        var chart1 = bb.generate({
          data: {
            columns: [
            [amont, pcaam],
            [aval, pcaav]
            ],
            type: "gauge", // for ESM specify as: gauge()
          },
          colors: {
            data1: "#ff0000",
            data2: "#00ff00"
          },
          arc: {
            cornerRadius: {
              ratio: 0.5
            }
          },
          gauge: {
            type: "multi",
            arcLength: 95,
            min:0,
            max:3.5,
            enforceMinMax: false,
            fullCircle: true,
            label: {
              format: function (value, ratio) { return value + " Bar"; }
            },
            startingAngle: -3,
            width: 55
          },
          arc: {
            cornerRadius: {
              ratio: 0.5
            },
            rangeText: {
              values: [
                0,
                0.5,
                1,
                1.5,
                2,
                2.5,
                3,
                3.5
              ],
              unit: "absolute"
            }
          },
          legend: {
            item: {
              tile: {
                type: "circle",
                r: 7
              }
            }
          },
          tooltip: {
            show: false
          },
          bindto: "#gaugecanal"
        });
        //---------------------------------------------------------
        //---------------------------------------------------------
        //---------------------------------------------------------
        // gauge pression cuve
    
        var chart2 = bb.generate({
          data: {
            columns: [
              [amont, pcuam],
              [aval, pcuav]
            ],
            type: "gauge", // for ESM specify as: gauge()
          },
          colors: {
            data1: "#ff0000",
            data2: "#00ff00"
          },
          arc: {
            cornerRadius: {
              ratio: 0.5
            }
          },
          gauge: {
            type: "multi",
            arcLength: 95,
            min:0,
            max:3.5,
            enforceMinMax: false,
            fullCircle: true,
            label: {
              format: function (value, ratio) { return value + " Bar"; }
            },
            startingAngle: -3,
            width: 55
          },
          arc: {
            cornerRadius: {
              ratio: 0.5
            },
            rangeText: {
              values: [
                0,
                0.5,
                1,
                1.5,
                2,
                2.5,
                3,
                3.5
              ],
              unit: "absolute"
            }
          },
          legend: {
            item: {
              tile: {
                type: "circle",
                r: 7
              }
            }
          },
          tooltip: {
            show: false
          },
          bindto: "#gaugecuve"
        });

//---------------------------------------------------------
        //---------------------------------------------------------
        //---------------------------------------------------------
        // gauge pression cuve
    
        var chart2 = bb.generate({
          data: {
            columns: [
              ["Canal", pdcanal],
              ["Cuve", pdcuve]
            ],
            type: "gauge", // for ESM specify as: gauge()
          },
          colors: {
            data1: "#ff0000",
            data2: "#00ff00"
          },
          arc: {
            cornerRadius: {
              ratio: 0.5
            }
          },
          gauge: {
            type: "multi",
            arcLength: 95,
            min:0,
            max:1.5,
            enforceMinMax: false,
            fullCircle: true,
            label: {
              format: function (value, ratio) { return value + " Bar"; }
            },
            startingAngle: -3,
            width: 55
          },
          arc: {
            cornerRadius: {
              ratio: 0.5
            },
            rangeText: {
              values: [
                0,
                0.25,
                0.5,
                0,75,
                1,
                1.25,
                1.5
              ],
              unit: "absolute"
            }
          },
          legend: {
            item: {
              tile: {
                type: "circle",
                r: 7
              }
            }
          },
          tooltip: {
            show: false
          },
          bindto: "#pressionfiltre"
        });


        //---------------------------------------------------------
        //---------------------------------------------------------
        //---------------------------------------------------------
        // gauge debit cuve
        var chart3 = bb.generate({
          data: {
            columns: [
          ["Cuve m3/h", debcuve]
            ],
            type: "gauge", // for ESM specify as: gauge()
          },
          arc: {
            cornerRadius: 15,
            rangeText: {
              values: [
                0,
                0.5,
                1,
                1.5,
                2,
                2.5,
                3,
                3.5,
                4,
                4.5,
                5
              ],
              unit: "absolute"
            }
          },
          gauge: {
            arcLength: 70,
            fullCircle: true,
            min:0,
            max:5,
            label: {
              format: function (value, ratio) { return value + " m3/h"; }
            },
            startingAngle: -2.2,
            width: 25
          },
          legend:{
            show: false
          },
          size:{
            width: 196,
            height: 215
        },
          bindto: "#gaugedebitcuve"
        });

        //---------------------------------------------------------
        //---------------------------------------------------------
        //---------------------------------------------------------
        // gauge debit arrosage
        var chart4 = bb.generate({
          data: {
            columns: [
          ["Arrosage m3/h", debarr]
            ],
            type: "gauge", // for ESM specify as: gauge()
          },
          arc: {
            cornerRadius: 15,
            rangeText: {
              values: [
                0,
                0.5,
                1,
                1.5,
                2,
                2.5,
                3,
                3.5,
                4,
                4.5,
                5
              ],
              unit: "absolute"
            }
          },
          gauge: {
            arcLength: 70,
            fullCircle: true,
            min:0,
            max:5,
            label: {
              format: function (value, ratio) { return value + " m3/h"; }
            },
            startingAngle: -2.2,
            width: 25
          },
          legend:{
            show: false
          },
          size:{
              width: 196,
              height: 215
          },
          bindto: "#gaugedebitarrosage"
        });
      
      }
    },"json");

});
