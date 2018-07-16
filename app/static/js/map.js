
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

//Create latlng objects for each data set
var sightingCoords = (function() {
    var sightings = [];
    for(var i = 0; i < data.length; i++) {
        if (data[i].report_type == 'sighting') {
            latlng = [data[i].lat, data[i].lon]
            sightings.push(latlng)
        }
    }
    return sightings
})();

var evidenceCoords = (function() {
    var evidence = [];
    for(var i = 0; i < data.length; i++) {
        if (data[i].report_type == 'evidence') {
            latlng = [data[i].lat, data[i].lon]
            evidence.push(latlng)
        }
    }
    return evidence
})();

// Create layer groups for markers
var sightingsHeat = L.heatLayer(sightingCoords, {radius: 100});
var evidenceHeat = L.heatLayer(evidenceCoords, {radius: 100});
var overlays = {
    "Sightings": sightingsHeat,
    "Evidence": evidenceHeat
}

// Create map and activate sighting layer
var map = L.map('mapsection', {
    center: [33.7590, -84.3880],
    zoom: 12,
    layers: [sightingsHeat]
});

// Add tile from mapbox to map
L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: 'pk.eyJ1IjoibWljaGFlbC1rMTAxIiwiYSI6ImNqajBkMXNmbDBnbzAza2x6Mnp1Mjl5YWIifQ.K5e1fvORu0_ZfSPH4cGlNA',
}).addTo(map);
L.control.layers(null, overlays).addTo(map);


// Derive statistics from data set
var sightingCounter = sightingData.length
var evidenceCounter = evidenceData.length
var deadRatCounter = (function() {
    var counter = 0;
    for(var i = 0; i < sightingData.length; i++) {
        if (data[i].dead_alive == 'dead') {
            counter += 1;
        }
    }
    return counter
})();
var liveRatcounter = (function() {
    var counter = 0;
    for(var i = 0; i < sightingData.length; i++) {
        if (data[i].dead_alive == 'alive') {
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


