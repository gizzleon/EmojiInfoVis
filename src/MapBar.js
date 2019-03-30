       
       /*--------------------- SETTING UP CANVAS FOR BAR CHARTS -------------------------------------- */	   
	   var margin = {top: 10, right: 20, bottom: 30, left: 50},
		width = window.innerWidth - margin.left - margin.right,
		height = 300 - margin.top - margin.bottom;
		// height2 = 500 - margin.top - margin.bottom;
	   
	   var x = d3.scale.ordinal()
		.rangeRoundBands([0, width]);

	   var y = d3.scale.linear()
		.range([height, 0]);

	   var xAxis = d3.svg.axis()
		.scale(x)
		.orient("bottom");

	   var yAxis = d3.svg.axis()
		.scale(y)
		.orient("left");
	
	   var svg = d3.select("#bar")
		.attr("width", 800)
		.attr("height", 300)
		.append("g")
		.attr("transform", "translate(" + margin.left + "," + margin.top + ")");
	   //To sort data from the highest frequency to the lowest frequency
	   	function sortData(data){
			return data.sort(function(a,b){return b.frequency-a.frequency});
		}
	   //Draw Bar Charts
	   function drawBar(data) {  
			data = sortData(data);	

			x.domain(data.map(function(d) { return d.letter; }));
			y.domain([0, d3.max(data, function(d) { return d.frequency; })]);

			svg.append("g")
				.attr("class", "x axis")
				.attr("transform", "translate(0," + height + ")")
				.call(xAxis);

			svg.append("g")
				.attr("class", "y axis")
				.call(yAxis);

			svg.selectAll(".bar")
				.data(data)
			.enter().append("rect")
				.attr("height", 0)
				.attr("y", height)
				.transition()
				.duration(1000)
				.attr("class", "bar")
				.attr("x", function(d) { return x(d.letter)+x.rangeBand()/2-7.5; })
				.attr("width", 15) //x.rangeBand()
				.attr("y", function(d) { return y(d.frequency); })
				.attr("height", function(d) { return height - y(d.frequency); })
				.style("fill", function(d,i) { return 'rgb(240, 30, ' + ((i * 20) -100) + ')'});
			};
	   	 
        /*----------------------------------------------SETTING UP MAP--------------------------------------------------------*/		 
		var mapboxAccessToken = 'pk.eyJ1IjoicXNodHlrb28iLCJhIjoiY2phYjFmNm12MHZxZjMzbG8wb240MTA0YiJ9.hBXHIWM9mEUJouY6Fl2t_Q';
		var map = L.map('mapid').setView([37.8, -96], 3);

		L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=' + mapboxAccessToken, {
			id: 'mapbox.light'
		}).addTo(map);
		
		L.geoJson(statesData).addTo(map); //importing data onto map
		
		
		var colorScale = d3.scale.linear()
                        .domain([0,260]) //defines the original range
                        .range(["blue", "red"]); // the range of colors in this case where "red" is the min and "blue" is the max
						
		function getColor(d) {
			return colorScale(d)
        }
		
		/*----------------------------------------- modify filled-in colors on the map -------------------------------------- */
		
		function style(features)  {
		        return {
			        fillColor: getColor(features.properties.density),
					weight: 2, //line width
					opacity: 1, 
					color: 'white', //line color
					dashArray: '3',
					fillOpacity: 0.7
		            };
			}
				L.geoJson(statesData, {style: style}).addTo(map);
        
        /*---------------------------------------- setting interactive functions on the map ----------------------------------*/
		function highlightFeature(e) {
		    var layer = e.target;
		    layer.setStyle({
				weight: 5,
				color: 'white',
				dashArray: '',
				fillOpacity: 0.7
			});

			if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
				layer.bringToFront();
			}
			
			
		}
		
		function resetHighlight(e) {
           geojson.resetStyle(e.target);
        }
		
		function showGraph(e) {
			var layer = e.target;
			showBar(0);
			d3.select("#bar").attr("width", window.innerWidth)
			x.rangeRoundBands([0, window.innerWidth - margin.left - margin.right]);
			console.log(window.innerWidth - margin.left - margin.right);
			showBar(layer.feature.properties.num);
		}
		
		function onEachFeature(feature, layer) {
			layer.on({
				mouseover: highlightFeature,
				mouseout: resetHighlight,
				click: showGraph, highlightFeature
			});
		}

		geojson = L.geoJson(statesData, {
			style: style,
			onEachFeature: onEachFeature
		}).addTo(map);
		
		
		

			
	    
		
					