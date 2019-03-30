// tooltip
var div = d3.select("body").append("div")	
        .attr("class", "tooltip")				
        .style("opacity", 0);

function showHeatmap(){
    var itemsize = 20,
        cellsize = itemsize-1,
        width = itemsize * 30,
        height = 550,
        margin = {top:50, right:50, bottom:20, left:50};

    var emojiList = null,
        emojiPair = null;
    var dataExtent = null;
    var rect = null;

    var svg = d3.select("#heatmap")
                    .attr("width", width)
                    .attr("height", height),
        heatmap = svg.append("g")
                    .attr("width", width-margin.left-margin.right)
                    .attr("height", height-margin.top-margin.bottom)
                    .attr("transform", "translate("+margin.left+","+margin.top+")");

        // data
        emojiList = insight_data.emoji_list;
        emojiPair = insight_data.emoji_pair;

        dataExtent = d3.extent(emojiPair, function(d){
            return d.PMI;
        })

        var xScale = d3.scale.ordinal()
                    .domain(emojiList)
                    .rangePoints([0+itemsize/2, itemsize*emojiList.length-itemsize/2]),
            xAxis = d3.svg.axis()
                    .scale(xScale)
                    .orient("top");
        var yScale = xScale,
            yAxis = d3.svg.axis()
                    .scale(yScale)
                    .orient("left");

        heatmap.append('g')
                .attr("class", "x axis insight")
                .call(xAxis);
        d3.select(".x").selectAll("text")
            .attr("id", function(d){
                return "column_" + d
            })
        
        heatmap.append('g')
                .attr("class", "y axis insight")
                .call(yAxis);

        d3.select(".y").selectAll("text")
            .attr("id", function(d){
                    return "row_" + d
            })
        rect = heatmap.selectAll("rect")
            .data(insight_data.emoji_pair)
            .enter().append("rect")
                .attr("width", cellsize)
                .attr("height", cellsize)
                .attr("x", function(d){
                    return emojiList.indexOf(d["emoji_1"])*itemsize;
                })
                .attr("y", function(d){
                    return emojiList.indexOf(d["emoji_2"])*itemsize;
                })
                .attr("fill", function(d){
                    var grayScale = d3.scale.linear()
                                    .domain([dataExtent[0],dataExtent[1]])
                                    .interpolate(d3.interpolateRgb)
                                    .range(["white", "black"]);
                    return grayScale(d.PMI)
                })
                .on("mouseover", function(d){
                    //enlarge the emoji-pair
                    d3.select("#column_"+d["emoji_1"]).classed("hover", true);
                    d3.select("#row_"+d["emoji_2"]).classed("hover", true);
                    //tooltip
                    div.transition()
                        .delay(700)
                        .duration(500)
                        .style("opacity", .9);
                    div.text("count: "+d.count+"\nPMI:"+d.PMI)
                        .style("left", (d3.event.pageX) + "px")		
                        .style("top", (d3.event.pageY - 28) + "px");
                })
                .on("mouseout", function(d){
                    //emoji-pair
                    d3.select("#column_"+d["emoji_1"]).classed("hover", false);
                    d3.select("#row_"+d["emoji_2"]).classed("hover", false);
                    //tooltip
                    div.style("opacity", 0);
                });
    
}

showHeatmap();