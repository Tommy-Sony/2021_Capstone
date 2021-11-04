function removeMarker(markers) {
    for ( var i = 0; i < markers.length; i++ ) {
        markers[i].setMap(null);
    }   
    //markers = [];
}

function createMarker(markers) {
    for ( var i = 0; i < markers.length; i++ ) {
        markers[i].setMap(map);
    }   
}

function removeInfoWindow(infoWindows){
    for ( var i = 0; i < infoWindows.length; i++ ) {
        infoWindows[i].close();
    }   
    //infoWindows = [];
}

function createInfoWindow(infoWindows){
    for ( var i = 0; i < infoWindows.length; i++ ) {
        infoWindows[i].open(map,marker);
    }   
}

