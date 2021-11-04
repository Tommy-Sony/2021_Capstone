
            var placeOverlay = new kakao.maps.CustomOverlay({zIndex:1}), 
            contentNode = document.createElement('div'), // 커스텀 오버레이의 컨텐츠 엘리먼트 입니다 
            markers = [], // 마커를 담을 배열입니다
            markers_2 = [],
            currCategory = ''; // 현재 선택된 카테고리를 가지고 있을 변수입니다

            var infoWindows = [];
            var infoWindows_2 = [];

            var mapContainer = document.getElementById('map'), // 지도를 표시할 div 
            mapOption = { 
                center: new kakao.maps.LatLng(37.566826, 126.9786567), // 지도의 중심좌표
                level: 8 // 지도의 확대 레벨,숫자 작을수록 확대됨
            };
        
            // 지도를 생성합니다

            var map = new kakao.maps.Map(mapContainer, mapOption),
            customOverlay = new kakao.maps.CustomOverlay({}),
            infowindow = new kakao.maps.InfoWindow({removable: true});

            //지오코더 켜면 폴리곤이 안 됨 (왜 ㅠㅠ?)
            //var geocoder = new kakao.maps.services.Geocoder();
             
            var geocoder = new kakao.maps.services.Geocoder();
            var ps = new kakao.maps.services.Places(map); 

        

        