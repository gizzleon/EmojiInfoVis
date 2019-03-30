
        /*----------------------------------------------SETTING UP MAP--------------------------------------------------------*/		 
		/* use your token here */
		var mapboxAccessToken = '';
		var map = L.map('mapid').setView([37.8, -96], 3);
		
		/*----------------------------------------------Custom Pane-----------------------------------------------------------*/   
        map.createPane('labels');
		//a value of 650 will make the TileLayer with the labels show on top of markers but below pop-ups
		map.getPane('labels').style.zIndex = 650; 
		/* One of the problems of having image tiles on top of other map layers is that the tiles will capture clicks and touches. 
		If a user clicks anywhere on the map, the web browser will assume she clicked on the labels tiles, and not on the GeoJSON or on the markers. 
		This can be solved using the pointer-events CSS property: */
		map.getPane('labels').style.pointerEvents = 'none';
		
		
        /* ----- ↓ Adding LabelLayer For Showing Labels ↓ ------ */
		L.tileLayer('http://{s}.basemaps.cartocdn.com/light_only_labels/{z}/{x}/{y}.png', {
		    pane: 'labels'
	    }).addTo(map);
		/* ----- ↑ Adding LabelLayer For Showing Labels ↑ ------ */
		
		/* ----- ↓ Adding Layer For Showing the Map ↓ ----- */
		L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=' + mapboxAccessToken, {
			id: 'mapbox.light'
		}).addTo(map);
		/* ----- ↑ Adding Layer For Showing the Map ↑ ----- */
		
		
		//importing data onto the map
		var geojson = L.geoJson(statesData).addTo(map); 
	
		
		//Pop up names
		geojson.eachLayer(function (layer) {
			layer.bindPopup(layer.feature.properties.name);
		}).addTo(map);
		
		/* ------------------ ↓ Setting up color scale to represent densities on the map ↓ --------------------------- */
		var densityArray = []; //densityArray of iPhone
		var density1Array = []; //densityArray of Android
		var density2Array = []; //densityArray of Instagram
		for(var i = 0; i<52; i++)
		{	densityArray[i] = statesData.features[i].properties.density;
	        density1Array[i] = statesData.features[i].properties.density1;
            density2Array[i] = statesData.features[i].properties.density2;			
		}
			
	    //to calculate the maximum number of density array
		function max(data){
			maxNumber = 0;
			for(var i = 0; i<52; i++)
			{if(maxNumber < data[i])
				{maxNumber = data[i];}
			}
            
            return maxNumber;					
		}
		
		//to set up 3 different colorscales
		var colorScale = d3.scale.linear()
                        .domain([0,max(densityArray)]) //defines the original range
                        .range(["blue", "red"]); // the range of colors in this case where "blue" is the min and "red" is the max
		
		var colorScale1 = d3.scale.linear()
                        .domain([0,max(density1Array)]) 
                        .range(["blue", "red"]); 
		
		var colorScale2 = d3.scale.linear()
                        .domain([0,max(density2Array)])
                        .range(["blue", "red"]); 
		
        //to assign density to different colorscales according to its magnitude		
		function getColor(d) {
			if(d<max(density2Array))
			return colorScale2(d);
		    if(d>=max(density2Array) && d<max(density1Array))
			return colorScale1(d);
		    if(d>=max(density1Array))
			return colorScale(d);
        }
		/* ------------------ ↑ Setting up color scale to represent densities on the map ↑ --------------------------- */
		
		
		
		/*----------------------------------------- modify filled-in colors on the map -------------------------------------- */
		
		//setting up style function for iPhone users
		function style3(features)  {
		        return {
			        fillColor: getColor(features.properties.density),
					weight: 2, //line width
					opacity: 1, 
					color: 'white', //line color
					dashArray: '3',
					fillOpacity: 1
		            };
			}
        //setting up style function for Android users
		function style1(features){
		        return {
	                fillColor: getColor(features.properties.density1),
					weight: 2, //line width
					opacity: 1, 
					color: 'white', //line color
					dashArray: '3',
					fillOpacity: 1
		            };
			}
	    //setting up style function for Instagram users
		function style2(features)  {
		        return {
			        fillColor: getColor(features.properties.density2),
					weight: 2, //line width
					opacity: 1, 
					color: 'white', //line color
					dashArray: '3',
					fillOpacity: 1
		            };
			}
        //setting up style to cover every previous colors on the map
	    function style0(features){
		        return {
	                fillColor: 'white',
					weight: 2, //line width
					opacity: 1, 
					color: 'white', //line color
					dashArray: '3',
					fillOpacity: 1 //in order to cover the previous colors
		            };
			}
		//choosing different styles to add to the map
		function addStyle(style){
			            geojson.clearLayers();
				        L.geoJson(statesData, {style: style}).addTo(map);
		}
        
		
		
        // //Options to add different colors schems on the map
		// d3.select('#opts2')
		// 	  .on('change', function() {
        //         addStyle(style0);				  
		// 		var data = eval(d3.select(this).property('value'));
		// 		addStyle(data);
		// 	});
		
		//Initializing the colors on the map 
		addStyle(style3);

		
	    