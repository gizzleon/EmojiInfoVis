/*----------------------------------------------to draw bubble charts----------------------------------------------------*/
var ds4 = emoji["Twitter for iPhone"],
	ds5 = emoji["Twitter for Android"],
	ds6 = emoji["Instagram"];

// tooltip for bubble chart
var div = d3.select("body").append("div")	
        .attr("class", "tooltip")				
        .style("opacity", 0);

var width1 = 800;
var height1 = 500;

var center = {x: width1/2, y: height1/2};

var canvas = d3.select("#bubble") 
			.attr("width", width1)
			.attr("height", height1);

//draw Bubble Charts
function bubbleChart(EMOJIs){

var bubbles = null;
var node = null;

var damper = 0.102;

function charge(d) {
	return -Math.pow(sizeScale(d.frequency), 2.0)/12;
}

var force = d3.layout.force()
	.charge(charge)
	.size([width1, height1])
	.gravity(0.01);

var sizeScale = d3.scale.pow()
	.exponent(0.5)
	.range([7, 85]);

function createNodes(rawData) {
	var myNodes = rawData.map(function(d){
		return d;
		// to be finished
	});

	return myNodes;
}

function moveToCenter(e){
	bubbles.each(function(d){
		d.x = d.x + (center.x - d.x)*damper*e.alpha;
		d.y = d.y + (center.y - d.y)*damper*e.alpha;
	})
		.attr("transform", function(d){
			return "translate("+d.x+","+d.y+")";
		});
}


	emoji_data = EMOJIs;

	var maxCount = d3.max(emoji_data, function(d){return d.frequency;});

	sizeScale.domain([0, maxCount]);

	force.nodes(emoji_data) 
		.on("tick", moveToCenter);

	bubbles = canvas.selectAll(".bubble")
		.data(emoji_data)
		.enter().append('g')
			.attr("class", "node")
			.call(force.drag);

	bubbles.append("text")
		.text(function(d){return d.letter;})
		.attr("y", function(d){return sizeScale(d.frequency)/2.75})
		.attr("text-anchor", "middle")
		.attr("font-size", function(d){return sizeScale(d.frequency)+"px";})
		.on("mouseover",function(d){
            // console.log(div);
            div.transition()
                .delay(700)
                .duration(500)
                .style("opacity", .9);
            div.text("emoji: "+d.letter+"\ncount: "+d.frequency)
                .style("left", (d3.event.pageX) + "px")		
                .style("top", (d3.event.pageY - 28) + "px");
        })
        .on("mouseout",function(d){
            div.style("opacity", 0);
        });;

	force.start();

}

//Options to show Bubble Chart on the map		
d3.select('#opts1')
		.on('change', function() {	
		canvas.selectAll("*").remove();	//remove all child elements of svg
		var data = eval(d3.select(this).property('value'));
		bubbleChart(data);

		//map related
		addStyle(style0);			
		var style = d3.select(this).property('value');
		switch(style){
			case "ds4": 
				style = "style3";
				break;
			case "ds5":
				style = "style1";
				break;
			case "ds6":
				style = "style2";
				break;
		}
		var data = eval(style);
		addStyle(data);
	});

bubbleChart(ds4); //Initialize the display of bubbleChart (data of iPhone Users)