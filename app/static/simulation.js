function () {
            var positioning = 'map'
            var margin = { top:50, left:50, right:50, bottom:50},
            height = 600 - margin.top - margin.bottom,
            width = 1600 - margin.left - margin.right;


            var projection = d3.geoMercator()
                .translate([width/2,height/2])
                .scale(150)

            var svg = d3.select('body')
                .append('svg')
                .attr('width', width)
                .attr('height', height)

            var map = svg.append('g')

            var path = d3.geoPath()
                .projection(projection)


            console.log("hey")
            var linkForce = d3.forceLink()
                .id(function (d) { return d.Name })
                .distance(10)

            var simulation = d3.forceSimulation()
                .force('link', linkForce)
                .force('charge', d3.forceManyBody()) //.strength(-160))
                //.force('center', d3.forceCenter(width / 2, height / 2))
                .stop()



            var tooltip = d3.select("div.tooltip");

            d3.queue()
                .defer(d3.json,"static/world.json") //0
                .defer(d3.csv, "static/world-country-names.csv") //1
                .defer(d3.csv,"static/asn_loc.csv")  //2
                .defer(d3.csv,"static/asn_links.csv")  //3
                .awaitAll(ready)

            function ready(error,data){
                if (error) { throw error }

                var temp = data[2]
                var graph_nodes = [];
                for (x of temp) {
                    asn = {Name: parseInt(x.ASN), Long: parseFloat(x.Longitude), Lat: parseFloat(x.Latitude)}
                    graph_nodes.push(asn)

                }

                temp = data[3]
                var graph_links = [];
                var counter = 0;
                source = []
                var s1 = ""
                var t1 = ""
                target = []
                for( x of temp){
                    for(p of graph_nodes){
                        if (p.Name == x.Source) {
                            source = [p.Long, p.Lat]
                            s1 = parseInt(p.Name)
                            counter += 1;
                        }
                        if (p.Name == x.Target) {
                            target = [p.Long, p.Lat]
                            t1 = parseInt(p.Name)
                            counter += 1;
                        }
                        if (counter==2){
                            //topush = {type: "LineString", coordinates: [source, target]}
                            linked = {source: parseInt(s1), target: parseInt(t1), count: 0.5}
                            graph_links.push(linked)
                            counter = 0
                            break
                        }

                    }
                    counter = 0


                }
                console.log(graph_links)
                var countries1 = topojson.feature(data[0], data[0].objects.countries).features
                countries = countries1.filter(function(d) {
                return data[1].some(function(n) {
                  if (d.id == n.id) return d.name = n.name;
                })});


                 simulation
                   .nodes(graph_nodes)
                   .on('tick', ticked)
                   .force('link')
                   .links(graph_links)


                 map.attr('class', 'map')
                    .selectAll('path')
                    .data(countries)
                    .enter().append('path')
                    .attr('d', path)
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

                var zoom = d3.zoom()
                      .on("zoom",function() {
                        svg.attr("transform", d3.event.transform)
                      });


                //console.log(links)
                var links = svg.append('g')
                    .attr('class', 'links')
                    .selectAll('line')
                    .data(graph_links)
                    .enter().append('line')
                    .attr('stroke-width', function (d) { return d.count })

                var drag = d3.drag()
                    .on('start', dragstarted)
                    .on('drag', dragged)
                    .on('end', dragended)

                var nodes = svg.append('g')
                    .attr('class', 'nodes')
                    .selectAll('circle')
                    .data(graph_nodes)
                    .enter().append('circle')
                    .attr('r', 1.5)
                    .attr("cx",function(d) {
                        //console.log(d)
                        var coord = projection([d.Long,d.Lat]) //feeding lat and long to mecator to convert it to somethin we can see
                        return coord[0];
                    })
                    .attr("cy",function (d) {
                        var coord = projection([d.Long,d.Lat]) //feeding lat and long to mecator to convert it to somethin we can see
                        return coord[1];
                    })
                    .call(drag)

                nodes.append("title")
                        .text(function(d) { return d.Name; })


                fixed(true)
                d3.select('#toggle').on('click', toggle)

                function fixed(immediate) {
                    graph_nodes.forEach(function (d) {
                        var pos = projection([d.Long,d.Lat])
                        d.x = pos[0]
                        d.y = pos[1]
                    })

                    var t = d3.transition()
                        .duration(immediate ? 0 : 600)
                        .ease(d3.easeElastic.period(0.5))

                    update(links.transition(t), nodes.transition(t))
                }

                function ticked() {

                    update(links, nodes)
                }

                function update(links, nodes) {

                    links
                        .attr('x1', function (d) {
                            return d.source.x })
                        .attr('y1', function (d) {
                            return d.source.y })
                        .attr('x2', function (d) {
                            return d.target.x })
                        .attr('y2', function (d) {
                            return d.target.y })

                    nodes
                        .attr('cx', function (d) {

                            return d.x })
                        .attr('cy', function (d) { return d.y })
                }

                function toggle() {
                    if (positioning === 'map') {
                        positioning = 'sim'
                        //map.attr('opacity', 0.25)
                        simulation.alpha(0).restart()
                    } else {
                        positioning = 'map'
                        //map.attr('opacity', 1)
                        simulation.stop()
                        fixed(true)
                    }
                }

                // drag nodes
                function dragstarted(d) {
                    if (positioning === 'map') { return }
                    simulation.alphaTarget(0.3).restart()
                    d.fx = d.x
                    d.fy = d.y
                }

                function dragged(d) {
                    if (positioning === 'map') { return }
                    d.fx = d3.event.x
                    d.fy = d3.event.y
                    fix_nodes(d);
                }

                function dragended(d) {
                    if (positioning === 'map') { return }
                    simulation.alphaTarget(0)
                    d.fx = d.x
                    d.fy = d.y
                }

                // Preventing other nodes from moving while dragging one node
                function fix_nodes(this_node) {
                  nodes.each(function(d) {
                    if (this_node != d) {
                      d.fx = d.x;
                      d.fy = d.y;
                    }
                  });
                }

                svg.call(zoom)
            }

    


}