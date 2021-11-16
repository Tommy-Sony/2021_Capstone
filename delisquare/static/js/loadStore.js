$.getJSON("static/map_resources/서초구음식점.json",function(store){
    var data = store;
    var loc = '';
    var name = '';
    //requestOK = true;
    $.each(data,function(index,val){

        loc=val.전체주소;
        name = val.업소명;

        displayStore(loc,name,markers,customOverlays);
    })
})

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
