$.getJSON("static/map_resources/test_loc2.json",function(geojson){
    var data = geojson.features;
    var coordinates = [];
    var name = '';
    //requestOK = true;
    $.each(data,function(index,val){

        coordinates=val.geometry.coordinates;
        name = val.properties.SGG_NM;

        displayArea(coordinates, name);
    })

})

var polygons=[];
        var checkArea ; 
        var checkClick = false;
        var checkPolygon = new kakao.maps.Polygon({
            map : map,
            path : path,
            strokeWeight : 4,
            strokeColor: '#00ff00',
            strokeOpacity: 0.8,
            fillColor: '#fff',
            fillOpacity: 0.5 
        });

//행정구역 폴리곤
function displayArea(coordinates, name){
    var path = [];
    var points = [];
    //var area_name = [];

    $.each(coordinates[0],function(index,coordinate){
        var point= new Object();
        point.x = coordinate[1];
        point.y = coordinate[0];
        //area_name = [];
        points.push(point);
        path.push(new kakao.maps.LatLng(coordinate[1],coordinate[0]));
    })

    var polygon = new kakao.maps.Polygon({
        map : map,
        path : path,
        strokeWeight : 4,
        strokeColor: '#ff0000',
        strokeOpacity: 0.8,
        fillColor: '#fff',
        fillOpacity: 0.5 
    });

    polygons.push(polygon); //폴리곤 제거 위한 배열 

    kakao.maps.event.addListener(polygon,'mouseover',function(mouseEvent){
        polygon.setOptions({
            fillColor : '#ffff00'
        });
        if (checkClick==true){
            polygon.setOptions({
                strokeColor: '#00ff00',
                fillColor: '#ffff00'
            });
            checkClick=false;
        }

        if (checkArea !=name){
            polygon.setOptions({
                strokeColor: '#ff0000'
            });
            checkArea =name;
        }
    });

    kakao.maps.event.addListener(polygon,'mousemove',function(mouseEvent){

    });

    kakao.maps.event.addListener(polygon,'mouseout',function(){
        polygon.setOptions({
            fillColor : '#fff'
        });
        //infowindow.close();
        //customOverlay.setMap(null);
    });

    //서초구 1 강남구 2 광진구 3
    kakao.maps.event.addListener(polygon, 'click', function(mouseEvent) {
        checkClick=true;
        checkArea=name;

        //행정구역을 나타내는 infowindow
        infowindow.setContent(checkArea);
        infowindow.setPosition(mouseEvent.latLng);
        infowindow.setMap(map);
        //customOverlay.setMap(map);
        
        if (name =='강남구'){
            removeMarker(markers);
            removeMarker(markers_3);
            //removeInfoWindow(infoWindows);

            removeCustomOverlay(customOverlays);
            removeCustomOverlay(customOverlays_3);
            
            createMarker(markers_2);
            //createCustomOverlay(customOverlays_2);
        }
        else if (name=='서초구'){
            removeMarker(markers_2);
            removeMarker(markers_3);

            removeCustomOverlay(customOverlays_2);
            removeCustomOverlay(customOverlays_3);

            createMarker(markers);
        }
        else{ //광진구
            removeMarker(markers);
            removeMarker(markers_2);
            //removeInfoWindow(infoWindows_2);

            removeCustomOverlay(customOverlays);
            removeCustomOverlay(customOverlays_2);

            createMarker(markers_3);
            //createCustomOverlay(customOverlays);
        }
       
    });

}