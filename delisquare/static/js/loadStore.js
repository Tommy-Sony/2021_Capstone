$.getJSON("static/map_resources/카카오_서초구.json",function(store){
    var data = store;
    var loc = '';
    var name = '';
    var url = '';

    //requestOK = true;
    $.each(data,function(index,val){

        loc=val.address_name;
        name = val.place_name;
        url = val.place_url;

        displayStore(loc,name,markers,customOverlays,url);
    })
})
/*
$.getJSON("static/map_resources/강남구_모범음식점.json",function(store){
    var data = store;
    var loc = '';
    var name = '';
    //requestOK = true;
    $.each(data,function(index,val){

        loc=val.소재지지번;
        name = val.업소명;

        displayStore(loc,name,markers_2,customOverlays_2);
    })
})
*/

$.getJSON("static/map_resources/카카오_강남구.json",function(store){
    var data = store;
    var loc = '';
    var name = '';
    var url = '';
    //requestOK = true;
    $.each(data,function(index,val){

        loc=val.address_name;
        name = val.place_name;
        url = val.place_url;

        displayStore(loc,name,markers_2,customOverlays_2,url);
    })
})