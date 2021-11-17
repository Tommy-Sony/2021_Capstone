var settings = {
    "url": "https://dapi.kakao.com/v2/local/search/keyword.json?query=카카오프렌즈",
    "method": "GET",
    "timeout": 0,
    "headers": {
      "Authorization": "KakaoAK 561701d221ab033a2c93b8042eaecff6"
    },
  };
  
  $.ajax(settings).done(function (response) {
    console.log(response);
  });