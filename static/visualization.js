( function () {
    var margin = { top:50, left:50, right:50, bottom:50},
        height = 600 - margin.top - margin.bottom,
        width = 1600 - margin.left - margin.right;

    var svg = d3.select("#map")
            .append("svg")
            .attr("height",height+margin.top+margin.bottom)
            .attr("width", width + margin.left+ margin.right)
            .append("g")
            .attr("transform","translate("+margin.left+","+margin.top + ")");
    var tooltip = d3.select("div.tooltip");
    d3.queue()
        .defer(d3.json,"static/world.json")
        .defer(d3.csv, "static/world-country-names.csv")
        .defer(d3.csv,"static/asn_loc.csv")
        .defer(d3.csv,"static/asn_links.csv")
        .await(ready)
    
    //create a new projection using mercator(geoMercator)
    //translate btn round globe to flat globe
    var projection = d3.geoMercator()
        .translate([width/2,height/2])
        .scale(150)

    //create path(geoPath)
    //shape is build from points this is like a line generator
    var path = d3.geoPath()
        .projection(projection)


    // Create data: coordinates of start and end
    var link = [
  {type: "LineString", coordinates: [[100, 60], [-60, -30],[-10, 10],[35, -9]]},
  {type: "LineString", coordinates: [[10, -20], [-60, -30]]},
  {type: "LineString", coordinates: [[10, -20], [130, -30]]}
]
    //function ready(error,data,tracerti){
    function ready(error,data,names,tracerti,asnlinks){
        console.log(data)

        //converting raw geo data into usable geo data
        //find what you wanna extract
        //.features allows one to get the features out of that topojson
        var countries1 = topojson.feature(data, data.objects.countries).features
        countries = countries1.filter(function(d) {
        return names.some(function(n) {
          if (d.id == n.id) return d.name = n.name;
        })});

        //add path for each country shapes ->path
        //.country is a path
        svg.selectAll(".country")
            .data(countries)  //binding our countries
            .enter().append("path") //path for every single country
            .attr("class","country") //set it to be class of country
            .attr("d",path) //attribute for countries to show up list of coordinates (d)
            .on("mouseover",function(d,i){
                d3.select(this).classed("selected",true)
                return tooltip.style("hidden", false).html(d.name);
            })
            .on("mousemove",function(d){
                tooltip.classed("hidden", false)
                       .style("top", (d3.event.pageY) + "px")
                       .style("left", (d3.event.pageX + 10) + "px")
                       .html(d.name);
            })
            .on("mouseout",function(d,i){
                d3.select(this).classed("selected",false)
                tooltip.classed("hidden", true);
            });


        // //add links
        // svg.selectAll(".links")
        //     .data(link)
        //     .enter()
        //     .append("path")
        //         .attr("d",function (d) {
        //             console.log(d)
        //             return path(d)
        //         })
        //         .style("fill", "none")
        //         .style("stroke", "orange")
        //         .style("stroke-width", 2)

        //add the connections between asns
        svg.selectAll(".asn-circles") //call them asn circles
            .data(tracerti)
            .enter().append("circle") // circle like
            .attr("r",1.5) // radius
            //circle has a cx and a cy (lat and long)
            //since they are different for each throw a function
            .attr("cx",function(d) {
                //console.log(d)
                var coord = projection([d.Longitude,d.Latitude]) //feeding lat and long to mecator to convert it to somethin we can see
                return coord[0];
            })
            .attr("cy",function (d) {
                var coord = projection([d.Longitude,d.Latitude]) //feeding lat and long to mecator to convert it to somethin we can see
                return coord[1];
            })
            .append("title")
            .text(function(d) { return d.ASN; });

        // svg.selectAll(".asn-label") //call them asn circles
        //     .data(tracerti)
        //     .enter().append("text") // circle like
        //     .attr("class","asn-label")
        //     //circle has a cx and a cy (lat and long)
        //     //since they are different for each throw a function
        //     .attr("x",function(d) {
        //         //console.log(d)
        //         var coord = projection([d.Longitude,d.Latitude]) //feeding lat and long to mecator to convert it to somethin we can see
        //         return coord[0];
        //     })
        //     .attr("y",function (d) {
        //         var coord = projection([d.Longitude,d.Latitude]) //feeding lat and long to mecator to convert it to somethin we can see
        //         return coord[1];
        //     })
        //     .on('mouseover',function(d) {
        //            d3.select(this).
        //         })
        //     })
            
        //     .attr("dx",5) //offset
        //     .attr("dy",2)


        var d = tracerti
        var l = asnlinks
        var links = [];
        var ASN_loc = [];
        for (x of d) {
            asn = {Name: x.ASN, Long: x.Longitude, Lat: x.Latitude}
            ASN_loc.push(asn)

        }
        var counter = 0;
        source = []
        target = []
        for( x of l){
            for(p of ASN_loc){
                if (p.Name == x.source) {
                    source = [p.Long, p.Lat]
                    counter += 1;
                }
                if (p.Name == x.target) {
                    target = [p.Long, p.Lat]
                    counter += 1;
                }
                if (counter==2){
                    topush = {type: "LineString", coordinates: [source, target]}
                    links.push(topush)
                    counter = 0
                    break
                }
                
            }
            counter = 0
            
            
        }
       svg.selectAll(".links")
            .data(links)
            .enter()
            .append("path")
                .attr("d",function (d) {
                    //console.log(d)
                    return path(d)
                })
                //.attr("moveTo")
                .style("fill", "none")
                .style("stroke", "red")
                .style("stroke-width", 0.5)
            //.call(d3.drag().on("drag", move))
            .call(d3.drag().on("drag", dragged))
            // .call(d3.drag()
            //     .on('start', dragstarted)
            //     .on('drag', dragged)
            //     .on('end', dragended));

        // // drag nodes
        // function dragstarted(d) {
        //   //if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        //   d.fx = d.x;
        //   d.fy = d.y;
        // }

        // function dragged(d) {
        //   d.fx = d3.event.x;
        //   d.fy = d3.event.y;
        //   fix_nodes(d);
        // }

        // function dragended(d) {
        //   //if (!d3.event.active) simulation.alphaTarget(0);
        //   d.fx = d.x;
        //   d.fy = d.y;
        // }

        // // Preventing other nodes from moving while dragging one node
        // function fix_nodes(this_node) {
        //   node.each(function(d) {
        //     if (this_node != d) {
        //       d.fx = d.x;
        //       d.fy = d.y;
        //     }
        //   });
        // }

        // function move(d){
        //     var d = d3.path()
        //         .moveTo(0,0)
        //         .lineTo(d3.event.dx,0)
        //         .lineTo(d3.event.x,10)
        //         .lineTo(20,10)
        //     path.attr('d',d.toString());
        //     }
        

        function dragged(d) {

              // Current position:
              this.x = this.x || 0;
              this.y = this.y || 0;
              // Update thee position with the delta x and y applied by the drag:
              this.x += d3.event.dx;
              this.y += d3.event.dy;

              // Apply the translation to the shape:
              d3.select(this)
                .attr("transform", "translate(" + this.x + "," + this.y + ")");
            }


    }
})()