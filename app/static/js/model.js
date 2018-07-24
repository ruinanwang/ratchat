
//model.js 

// Create model and add a tile to it
var model = L.map('model', {
    center: [33.7590, -84.3880],
    zoom: 13
});

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    id: 'mapbox.streets',
    accessToken: 'pk.eyJ1IjoibWljaGFlbC1rMTAxIiwiYSI6ImNqajBkMXNmbDBnbzAza2x6Mnp1Mjl5YWIifQ.K5e1fvORu0_ZfSPH4cGlNA'
}).addTo(model);

// Create geoJson object from shapefile
var geo = L.geoJson({
    features: []
}, {
    style: style,
    onEachFeature: function popUp(f, l) {
        var out = [];
        if (f.properties) {
            for (var key in f.properties) {
                if (key === 'cnszrnf') {
                    if (isNaN(f.properties[key])) {
                        out.push('Rat Infestations' + ": " + 'N/A');
                    } else {
                        out.push('Rat Infestations' + ": " + f.properties[key]);
                    }
                }
            }
            l.bindPopup(out.join("<br />"));
        }
    }
});

// Extract data from shapefile
var base = 'static/model/model.zip';
shp(base).then(function (data) {
    geo.addData(data);
});

geo.addTo(model);

// Assigns color to geoJson objects based on magnitude of rat counts
function getColor(d) {
    return d > 0.27 ? '#800026' :
        d > 0.24 ? '#BD0026' :
        d > 0.21 ? '#E31A1C' :
        d > 0.18 ? '#FC4E2A' :
        d > 0.15 ? '#FD8D3C' :
        d > 0.12 ? '#FEB24C' :
        d > 0.09 ? '#FED976' :
        d > 0.06 ? '#fff4c9' :
        d > 0.03 ? '#FFEDA0' :
                    '#fff2ba';
}

// Applies style to geoJson object
function style(feature) {
    return {
        fillColor: getColor(feature.properties['cnszrnf']),
        weight: 2,
        opacity: 1,
        color: 'white',
        fillOpacity: 0.7
    };
}