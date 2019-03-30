/*----------------------------------------------to add markers on the map----------------------------------------------------*/
		//assign data to three variables: iPhone, Android, Instagram
		var iPhone = [];
			for (var i = 0; i < iPhone1.coordinates.length; i++) {              
				iPhone[i] = [iPhone1.coordinates[i][1],iPhone1.coordinates[i][0]]
				};	
		var Android = [];
					for (var i = 0; i < Android1.coordinates.length; i++) {              
						Android[i] = [Android1.coordinates[i][1],Android1.coordinates[i][0]]
						};	 
		var Instagram = [];
					for (var i = 0; i < Instagram1.coordinates.length; i++) {              
						Instagram[i] = [Instagram1.coordinates[i][1],Instagram1.coordinates[i][0]]
						};	 
		var ds1 = iPhone; //[[36.13787, -98.12988],[36.88593, -102.30469]];
		var ds2 = Android;//[[34.88593, -102.30469],[30.88593, -97.30469]];
		var ds3 = Instagram;//[[33.39476, -93.51563],[40.88593, -97.30469]];
		var ds8 = 0; //for the option "clear all"
		
		var popup = L.popup();
		
		//To Initialize the markers
		var marker = [];
			for (var i = 0; i < ds1.length; i++) {              
					marker[i] = [ds1[i][0],ds1[i][1]]
					};	
		
	    //update Data on animatedMarker
		var animatedMarker;
		var markersLayer = new L.LayerGroup();
		function updateLegend(oldData, newData) {
				var line;
				for (var i=0; i<newData.length; i++){ 
				/* ------------ CASE 1 ------------- */
				if(oldData.length < newData.length && i<oldData.length){ 
				line = L.polyline([ oldData[i], [newData[i][0],newData[i][1]]]);
				map.addLayer(line);
				animatedMarker = L.animatedMarker(line.getLatLngs());

				markersLayer.addLayer(animatedMarker);
				markersLayer.addTo(map);
				map.removeLayer(line);} 
				/* ------------ CASE 2 ------------- */
				if(oldData.length < newData.length && i>=oldData.length){
				line = L.polyline([ [0,0], [newData[i][0],newData[i][1]]]);
				map.addLayer(line);
				animatedMarker = L.animatedMarker(line.getLatLngs());

				markersLayer.addLayer(animatedMarker);
				markersLayer.addTo(map);
				map.removeLayer(line);}; 
                /* ------------ CASE 3 ------------- */
				if(oldData.length > newData.length && i<=newData.length){ 
				line = L.polyline([ oldData[i], [newData[i][0],newData[i][1]]]);
				map.addLayer(line);
				animatedMarker = L.animatedMarker(line.getLatLngs());

				markersLayer.addLayer(animatedMarker);
				markersLayer.addTo(map);
				map.removeLayer(line);} 
                /* ------------ CASE 4 ------------- */
				if(oldData.length == newData.length){
				line = L.polyline([ oldData[i], [newData[i][0],newData[i][1]]]);
				map.addLayer(line);
				animatedMarker = L.animatedMarker(line.getLatLngs());
				
				markersLayer.addLayer(animatedMarker);
				markersLayer.addTo(map);
				map.removeLayer(line);} 
				}
			};
			
		//Options to show markers on the map		
		d3.select('#opts')
			  .on('change', function() {	
				if (markersLayer) {
				markersLayer.clearLayers();}		
				var newData = eval(d3.select(this).property('value'));
				if(newData != 0){
				updateLegend(marker, newData);
				marker = newData;}
				else{markersLayer.clearLayers();}
			});