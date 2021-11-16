function displayStore(loc,name,markers,customOverlays){
            
    geocoder.addressSearch(loc, function(result, status) {

        // 정상적으로 검색이 완료됐으면 
         if (status === kakao.maps.services.Status.OK) {
            var coords = new kakao.maps.LatLng(result[0].y, result[0].x);
            // 결과값으로 받은 위치를 마커로 표시합니다
            var marker = new kakao.maps.Marker({
                map: map,
                position: coords
                //clickable: true // 마커를 클릭했을 때 지도의 클릭 이벤트가 발생하지 않도록 설정합니다
            });
            
            marker.setMap(null);
            markers.push(marker);

            var content = '<div class="overlaybox">' +
    '    <div class="boxtitle">가게 정보</div>' +
    '    <div class="first">' +
    '        <div class="triangle text">1</div>' +
    '        <div class="movietitle text">'+name+'</div>' +
    '    </div>' +
    '    <ul>' +
    '        <li class="up">' +
    '            <span class="number">2</span>' +
    '            <span class="title">명량</span>' +
    '            <span class="arrow up"></span>' +
    '            <span class="count">2</span>' +
    '        </li>' +
    '        <li>' +
    '            <span class="number">3</span>' +
    '            <span class="title">해적(바다로 간 산적)</span>' +
    '            <span class="arrow up"></span>' +
    '            <span class="count">6</span>' +
    '        </li>' +
    '        <li>' +
    '            <span class="number">4</span>' +
    '            <span class="title">해무</span>' +
    '            <span class="arrow up"></span>' +
    '            <span class="count">3</span>' +
    '        </li>' +
    '        <li>' +
    '            <span class="number">5</span>' +
    '            <span class="title">안녕, 헤이즐</span>' +
    '            <span class="arrow down"></span>' +
    '            <span class="count">1</span>' +
    '        </li>' +
    '    </ul>' +
    '</div>';

            //var content = '<div style="width:150px;text-align:center;padding:6px 0;">'+ name+ '<a href="https://map.kakao.com/link/map/'+ result[0].y+','+result[0].x+'" style="color:blue" target="_blank">카카오맵 이동</a></div>'
            //커스텀 오버레이로 장소에 대한 설명 표시
            var overlay = new kakao.maps.CustomOverlay({
                map: map,
                position: coords,
                content: content,
                xAnchor: 0.3,
                yAnchor: 0.91,
                removable: true
            });
            // 인포윈도우로 장소에 대한 설명을 표시합니다
            /*
            var infowindow = new kakao.maps.InfoWindow({
                map: map,
                position: coords,
                //content: '<div style="width:150px;text-align:center;padding:6px 0;">불고기<br><a href="https://map.kakao.com/link/map/Hello World!," style="color:blue" target="_blank">카카오맵 이동</a></div>',
                //content: '<div style="width:150px;text-align:center;padding:6px 0;">'+ name+ '<a href="https://map.kakao.com/link/map/" style="color:blue" target="_blank">카카오맵 이동</a></div>',
                content: content,
                xAnchor: 0.3,
                yAnchor: 0.91,
                removable: true
            });
            */

            overlay.setMap(null);
            customOverlays.push(overlay);
            //infoWindows.push(infowindow);

            //infoWindows.push(infowindow);
            //infowindow.close();

            //infowindow.open(map, marker); 꺼둔 상태 유지
    
            // 지도의 중심을 결과값으로 받은 위치로 이동시킵니다


            kakao.maps.event.addListener(marker, 'click', function() {
                //infowindow.close();
                //infowindow.open(map, marker);

                removeCustomOverlay(customOverlays);
                overlay.setMap(map,marker);
            });

        } 
    });    
}

