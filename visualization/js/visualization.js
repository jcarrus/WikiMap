var color = d3.scale.quantize()
    .range(["#156b87", "#876315", "#543510", "#872815"]);

var size = 960;

var pack = d3.layout.pack()
    .sort(function(a, b){ return a.separation - b.separation;})
    .size([size, size])
    .value(function(d) { return d.importance; })
    .padding(5);

var svg = d3.select("body").append("svg")
    .attr("width", size)
    .attr("height", size);

color.domain(d3.extent(links, function(d) { return d.separation; }));

svg.selectAll("circle")
      .data(pack.nodes({children: links}))
    .enter().append("circle")
      .attr( "r",    function(d){ return d.importance;        })
      .attr( "cx",   function(d){ return d.x;                 })
      .attr( "cy",   function(d){ return d.y;                 })
      .style("fill", function(d){ return color(d.separation); })
    .append("title")
      .text(function(d){ return d.name;});
d3.select(self.frameElement).style("height", size + "px");
