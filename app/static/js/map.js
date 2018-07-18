
// map.js 

// Sort data into seperate variables

var sightingData = (function() {
    var sightings = [];
    for(var i = 0; i < data.length; i++) {
        if (data[i].report_type == 'sighting') {
            sightings.push(data[i])
        }
    }
    return sightings
})();

var evidenceData = (function() {
    var evidence = [];
    for(var i = 0; i < data.length; i++) {
        if (data[i].report_type == 'evidence') {
            evidence.push(data[i])
        }
    }
    return evidence
})();

//------------------------------------------------------------------------------------------------------

// Create latlng objects for each data set
var sightingCoords = (function() {
    var coords = [];
    for(var i = 0; i < data.length; i++) {
        if (data[i].report_type == 'sighting') {
            latlng = [data[i].lat, data[i].lon]
            coords.push(latlng)
        }
    }
    return coords
})();

var evidenceCoords = (function() {
    var coords = [];
    for(var i = 0; i < data.length; i++) {
        if (data[i].report_type == 'evidence') {
            latlng = [data[i].lat, data[i].lon]
            coords.push(latlng)
        }
    }
    return coords
})();

var allCoords = (function() {
    var coords = [];
    for(var i = 0; i < data.length; i++) {
        latlng = [data[i].lat, data[i].lon]
        coords.push(latlng)
    }
    return coords
})();

// Create markers
var icon = L.icon({
    iconUrl: 'static/img/map_dot.png',
    iconSize:     [100, 100], // size of the icon
    popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
});

var sightingsMarkers = (function() {
    var markers = []
    for (var i = 0; i < sightingData.length; i++) {
        var marker = L.marker([sightingData[i].lat, sightingData[i].lon], {time: sightingData[i].time, icon: icon});
        markers.push(marker)
    }
    return markers
})();

var evidenceMarkers = (function() {
    var markers = []
    for (var i = 0; i < evidenceData.length; i++) {
        var marker = L.marker([evidenceData[i].lat, evidenceData[i].lon], {time: evidenceData[i].time, icon: icon});
        markers.push(marker)
    }
    return markers
})();

var allMarkers = (function() {
    var markers = []
    for(var i = 0; i < data.length; i++) {
        if (data[i].report_type == 'sighting') {
            var m1 = L.marker([data[i].lat, data[i].lon], {time: data[i].time, icon: icon});
            markers.push(m1)
        }
        if (data[i].report_type == 'evidence') {
            var m2 = L.marker([data[i].lat, data[i].lon], {time: data[i].time, icon: icon});
            markers.push(m2)
        }
    }
    return markers
})();

var sightings = L.heatLayer(sightingCoords, {radius: 35});
var evidence = L.heatLayer(evidenceCoords, {radius: 35});
var allReports = L.heatLayer(allCoords, {radius: 35});

// Create map and put tile on top of it
var map = L.map('mapsection', {
    center: [33.7590, -84.3880],
    zoom: 13,
    maxZoom: 16,
    layers: [sightings]
});

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 16,
    id: 'mapbox.streets',
    accessToken: 'pk.eyJ1IjoibWljaGFlbC1rMTAxIiwiYSI6ImNqajBkMXNmbDBnbzAza2x6Mnp1Mjl5YWIifQ.K5e1fvORu0_ZfSPH4cGlNA',
}).addTo(map);

var overlays = {
    "Rat Sightings": sightings,
    "Rat Evidence": evidence
}
L.control.layers(null, overlays, {collapsed: false}).addTo(map);

var markerGroup = L.layerGroup(sightingsMarkers);
var sliderControl = L.control.sliderControl({layer:markerGroup, position: 'topright'});
map.addControl(sliderControl);
sliderControl.startSlider();

var currentLayer = "sightings";

$( "#leaflet-slider" ).on( "slidechange", function( event, ui ) {
    if (currentLayer == "sightings") {
        sightings.setLatLngs(sightingCoords.slice(0, ui.value));
    } else if (currentLayer == "evidence") {
        evidence.setLatLngs(evidenceCoords.slice(0, ui.value));
    } else if (currentLayer =="all") {
        sightings.setLatLngs(allCoords.slice(0, ui.value));
        evidence.setLatLngs([]);
    }
});

map.on('overlayadd', function(layer) {
    if (map.hasLayer(sightings) && layer.name == "Rat Evidence") {
        map.removeControl(sliderControl);
        markerGroup = L.layerGroup(allMarkers);
        sliderControl = L.control.sliderControl({layer:markerGroup, position: 'topright'});
        map.addControl(sliderControl);
        sightings.setLatLngs(allCoords);
        sliderControl.startSlider();
        currentLayer = "all";
        $( "#leaflet-slider" ).on( "slidechange", function( event, ui ) {
            if (currentLayer == "sightings") {
                sightings.setLatLngs(sightingCoords.slice(0, ui.value));
            } else if (currentLayer == "evidence") {
                evidence.setLatLngs(evidenceCoords.slice(0, ui.value));
            } else if (currentLayer =="all") {
                sightings.setLatLngs(allCoords.slice(0, ui.value));
                evidence.setLatLngs([]);
            }
        });
    } else if (map.hasLayer(evidence) && layer.name == "Rat Sightings") {
        map.removeControl(sliderControl);
        markerGroup = L.layerGroup(allMarkers);
        sliderControl = L.control.sliderControl({layer:markerGroup, position: 'topright'});
        map.addControl(sliderControl);
        sightings.setLatLngs(allCoords)
        sliderControl.startSlider();
        currentLayer = "all";
        $( "#leaflet-slider" ).on( "slidechange", function( event, ui ) {
            if (currentLayer == "sightings") {
                sightings.setLatLngs(sightingCoords.slice(0, ui.value));
            } else if (currentLayer == "evidence") {
                evidence.setLatLngs(evidenceCoords.slice(0, ui.value));
            } else if (currentLayer =="all") {
                sightings.setLatLngs(allCoords.slice(0, ui.value));
                evidence.setLatLngs([]);
            }
        });
    } else if (layer.name == "Rat Sightings") {
        map.removeControl(sliderControl);
        markerGroup = L.layerGroup(sightingsMarkers);
        sliderControl = L.control.sliderControl({layer:markerGroup, position: 'topright'});
        map.addControl(sliderControl);
        sliderControl.startSlider();
        sightings.setLatLngs(sightingCoords);
        currentLayer = "sightings";
        $( "#leaflet-slider" ).on( "slidechange", function( event, ui ) {
            if (currentLayer == "sightings") {
                sightings.setLatLngs(sightingCoords.slice(0, ui.value));
            } else if (currentLayer == "evidence") {
                evidence.setLatLngs(evidenceCoords.slice(0, ui.value));
            } else if (currentLayer =="all") {
                sightings.setLatLngs(allCoords.slice(0, ui.value));
                evidence.setLatLngs([]);
            }
        });
    } else if (layer.name == "Rat Evidence") {
        map.removeControl(sliderControl);
        markerGroup = L.layerGroup(evidenceMarkers);
        sliderControl = L.control.sliderControl({layer:markerGroup, position: 'topright'});
        map.addControl(sliderControl);
        sliderControl.startSlider();
        evidence.setLatLngs(evidenceCoords);
        currentLayer = "evidence";
        $( "#leaflet-slider" ).on( "slidechange", function( event, ui ) {
            if (currentLayer == "sightings") {
                sightings.setLatLngs(sightingCoords.slice(0, ui.value));
            } else if (currentLayer == "evidence") {
                evidence.setLatLngs(evidenceCoords.slice(0, ui.value));
            } else if (currentLayer =="all") {
                sightings.setLatLngs(allCoords.slice(0, ui.value));
                evidence.setLatLngs([]);
            }
        });
    }
});

map.on('overlayremove', function(layer) {
    if (map.hasLayer(sightings) && layer.name == "Rat Evidence") {
        map.removeControl(sliderControl);
        markerGroup = L.layerGroup(sightingsMarkers);
        sliderControl = L.control.sliderControl({layer:markerGroup, position: 'topright'});
        map.addControl(sliderControl);
        sliderControl.startSlider();
        sightings.setLatLngs(sightingCoords);
        currentLayer = "sightings";
        $( "#leaflet-slider" ).on( "slidechange", function( event, ui ) {
            if (currentLayer == "sightings") {
                sightings.setLatLngs(sightingCoords.slice(0, ui.value));
            } else if (currentLayer == "evidence") {
                evidence.setLatLngs(evidenceCoords.slice(0, ui.value));
            } else if (currentLayer =="all") {
                sightings.setLatLngs(allCoords.slice(0, ui.value));
                evidence.setLatLngs([]);

            }
        });
    } else if (map.hasLayer(evidence) && layer.name == "Rat Sightings") {
        map.removeControl(sliderControl);
        markerGroup = L.layerGroup(evidenceMarkers);
        sliderControl = L.control.sliderControl({layer:markerGroup, position: 'topright'});
        map.addControl(sliderControl);
        sliderControl.startSlider();
        evidence.setLatLngs(evidenceCoords);
        currentLayer = "evidence";
        $( "#leaflet-slider" ).on( "slidechange", function( event, ui ) {
            if (currentLayer == "sightings") {
                sightings.setLatLngs(sightingCoords.slice(0, ui.value));
            } else if (currentLayer == "evidence") {
                evidence.setLatLngs(evidenceCoords.slice(0, ui.value));
            } else if (currentLayer =="all") {
                sightings.setLatLngs(allCoords.slice(0, ui.value));
                evidence.setLatLngs([]);

            }
        });
    } else if (layer.name == "Rat Sightings") {
        map.removeControl(sliderControl);
    } else if (layer.name == "Rat Evidence") {
        map.removeControl(sliderControl);
    }
});

// -------------------------------------------------------------------------------------------------------------------------------------------------------------

// Derive statistics from data set
var sightingCounter = sightingData.length
var evidenceCounter = evidenceData.length
var deadRatCounter = (function() {
    var counter = 0;
    for(var i = 0; i < sightingData.length; i++) {
        if (sightingData[i].dead_alive == 'dead') {
            counter += 1;
        }
    }
    return counter
})();
var liveRatcounter = (function() {
    var counter = 0;
    for(var i = 0; i < sightingData.length; i++) {
        if (sightingData[i].dead_alive == 'alive') {
            counter += 1;
        }
    }
    return counter
})();
var mostRecentSighting = sightingData[sightingData.length - 1];
var mostRecentEvidence = evidenceData[evidenceData.length - 1];

// Update statistics page with information
document.getElementById('sightingreports').innerHTML = sightingCounter;
document.getElementById('evidencereports').innerHTML = evidenceCounter;
document.getElementById('sightingaddress').innerHTML = mostRecentSighting.address.slice(mostRecentSighting.address.indexOf(' '));
document.getElementById('sightinglocation').innerHTML = mostRecentSighting.out_in.charAt(0).toUpperCase() + mostRecentSighting.out_in.slice(1);
document.getElementById('sightingdeadoralive').innerHTML = mostRecentSighting.dead_alive.charAt(0).toUpperCase() + mostRecentSighting.dead_alive.slice(1);
document.getElementById('deadrats').innerHTML = deadRatCounter;
document.getElementById('liverats').innerHTML = liveRatcounter;
document.getElementById('evidenceaddress').innerHTML = mostRecentEvidence.address.slice(mostRecentEvidence.address.indexOf(' '));
document.getElementById('evidencetype').innerHTML = mostRecentEvidence.chew_drop_hole.charAt(0).toUpperCase() + mostRecentEvidence.chew_drop_hole.slice(1);


