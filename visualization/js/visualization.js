var color = d3.scale.quantize()
    .range(["#156b87", "#876315", "#543510", "#872815"]);

var size = 960, padding = 5;

var pack = d3.layout.pack()
    .sort(null)
    .size([size, size])
    .value(function(d) { return d.importance; })
    .padding(padding);

var svg = d3.select("body").append("svg")
    .attr("width", size)
    .attr("height", size);

d3.csv("http://web.mit.edu/jcarrus/Public/links.csv", undefined, function(error, links){
    console.log(links);
    console.log(pack.nodes());

    color.domain(d3.extent(exoplanets, function(d) { return d.distance; }));
});
    // svg.selectAll("circle")
    // 	.data(pack.nodes({c
	
