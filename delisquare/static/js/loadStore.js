$.getJSON("static/map_resources/서초구_테스트.json",function(store){
    var data = store;
    var loc = '';
    var name = '';
    var url = '';
    var img_url='';

    //requestOK = true;
    $.each(data,function(index,val){

        loc=val.address_name;
        name = val.place_name;
        url = val.place_url;
        img_url = val.place_img;

        displayStore_test(loc,name,markers,customOverlays,url,img_url);
    })
})

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

$.getJSON("static/map_resources/카카오_광진구.json",function(store){
    var data = store;
    var loc = '';
    var name = '';
    var url = '';
    //requestOK = true;
    $.each(data,function(index,val){

        loc=val.address_name;
        name = val.place_name;
        url = val.place_url;

        displayStore(loc,name,markers_3,customOverlays_3,url);
    })
})