$(document).ready(function(){



            $.get("load_kpi.php", function(data, status){
                if (status == "success") {
                 var prccuve = 0;
                 var mcube = 0;
                  $.each(data, function(index) {
                        if (data[index].sensor == 'Niveau Cuve'){
                                prccuve = data[index].mesure;
                        }else if (data[index].sensor == 'Niveau Cuve m3'){
                                mcube = data[index].mesure;
                        }
                  });

                  var width = 500;
                  var height = 600;
              
                  //Create SVG element
                  var svg = d3.select("#cuve")
                          .append("svg")
                          .attr("width", width)
                          .attr("height", height)
                          .attr("opacity", 0.5);
              
        
                //Create and append rectangle element
                svg.append("line")
                .attr('x1', 100)
                .attr('y1', 50)
                .attr('x2', 100)
                .attr('y2', 500)
                .attr('stroke', 'black')
                .attr("stroke-width", 3);
        
                svg.append("line")
                .attr('x1', 400)
                .attr('y1', 50)
                .attr('x2', 400)
                .attr('y2', 500)
                .attr('stroke', 'black')
                .attr("stroke-width", 3);
        
                svg.append("line")
                .attr('x1', 100)
                .attr('y1', 50)
                .attr('x2', 400)
                .attr('y2', 50)
                .attr('stroke', 'black')
                .attr("stroke-width", 3);
        
                svg.append("line")
                .attr('x1', 100)
                .attr('y1', 500)
                .attr('x2', 400)
                .attr('y2', 500)
                .attr('stroke', 'black')
                .attr("stroke-width", 3);
              
              
                svg.append('text')
                        .attr('x', 40)
                        .attr('y', 55)
                        .attr('stroke', 'black')
                        .style("font-size", 17)
                        .text("100 %");
                
                        svg.append("line")
                        .attr('x1', 90)
                        .attr('y1', 50)
                        .attr('x2', 110)
                        .attr('y2', 50)
                        .attr('stroke', 'black')
                        .attr("stroke-width", 3);
                
                        svg.append('text')
                        .attr('x', 40)
                        .attr('y', 162.5)
                        .attr('stroke', 'black')
                        .style("font-size", 17)
                        .text("75 %");
                
                        svg.append("line")
                        .attr('x1', 85)
                        .attr('y1', 162.5)
                        .attr('x2', 110)
                        .attr('y2', 162.5)
                        .attr('stroke', 'black')
                        .attr("stroke-width", 3);
                
                        svg.append('text')
                        .attr('x', 40)
                        .attr('y', 275)
                        .attr('stroke', 'black')
                        .style("font-size", 17)
                        .text("50 %");
                
                        svg.append("line")
                        .attr('x1', 85)
                        .attr('y1', 275)
                        .attr('x2', 110)
                        .attr('y2', 275)
                        .attr('stroke', 'black')
                        .attr("stroke-width", 3);
                
                        svg.append('text')
                        .attr('x', 40)
                        .attr('y', 500)
                        .attr('stroke', 'black')
                        .style("font-size", 17)
                        .text("0 %");
                        
                        svg.append("line")
                        .attr('x1', 85)
                        .attr('y1', 500)
                        .attr('x2', 110)
                        .attr('y2', 500)
                        .attr('stroke', 'black')
                        .attr("stroke-width", 3);
                
                
                        svg.append('text')
                        .attr('x', 40)
                        .attr('y', 387.5)
                        .attr('stroke', 'black')
                        .style("font-size", 17)
                        .text("25 %");
                        
                        svg.append("line")
                        .attr('x1', 85)
                        .attr('y1', 387.5)
                        .attr('x2', 110)
                        .attr('y2', 387.5)
                        .attr('stroke', 'black')
                        .attr("stroke-width", 3);
                
                        recx = 101;
                        recy = (50+450)-(450 *prccuve/100);
                        recw = 298;
                        rech = 449 *prccuve/100;          //Create and append rectangle element
                        
                        svg.append("rect")
                                .attr("x", recx)
                                .attr("y", recy)
                                .attr("width", recw)
                                .attr("height", rech)
                                .attr('fill', '#3C81DF');
                        
                        $("#kpi").text(prccuve+' % / '+mcube+' m3');

                }
        },"json");


            $.get("load_cuve.php", function(data, status){
                if (status == "success") {
                               
                  $.each(data, function(index) {
                    
                  });
                  var chart = bb.generate({
                        data: {
                          x: "x",
                          columns: [
                              ["x", "2013-01-01", "2013-01-02", "2013-01-03", "2013-01-04", "2013-01-05", "2013-01-06"],
                              ["data1", 30, 200, 100, 400, 150, 250],
                              ["data2", 130, 340, 200, 500, 250, 350]
                          ],
                          type: "line", // for ESM specify as: line()
                        },point: {
                                show: false
                        },
                        axis: {
                          x: {
                            type: "timeseries",
                            tick: {
                              format: "%Y-%m-%d"
                            }
                          }
                        },
                        bindto: "#evocuve"
                      });
                }
                },"json");
             

});