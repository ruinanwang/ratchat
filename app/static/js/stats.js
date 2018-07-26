
// stats.js 

// Sort data into seperate variables
var sightingData = (function () {
    var sightings = [];
    for (var i = 0; i < data.length; i++) {
        if (data[i].report_type == 'sighting') {
            sightings.push(data[i])
        }
    }
    return sightings
})();

var evidenceData = (function () {
    var evidence = [];
    for (var i = 0; i < data.length; i++) {
        if (data[i].report_type == 'evidence') {
            evidence.push(data[i])
        }
    }
    return evidence
})();

// Derive statistics from data set
var sightingCounter = sightingData.length
var evidenceCounter = evidenceData.length
var deadRatCounter = (function () {
    var counter = 0;
    for (var i = 0; i < sightingData.length; i++) {
        if (sightingData[i].dead_alive == 'dead') {
            counter += 1;
        }
    }
    return counter
})();
var liveRatcounter = (function () {
    var counter = 0;
    for (var i = 0; i < sightingData.length; i++) {
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