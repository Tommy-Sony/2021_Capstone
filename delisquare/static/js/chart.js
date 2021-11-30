var ctx = document.getElementById('myChart').getContext('2d');

var myChart = new Chart(ctx,{
    type: 'doughnut',
    data:{
    labels: ['긍정', '부정'],   //위치 상단 고정인듯
    datasets: [{
        label: '# 긍-부정치',
        data: [8, 2],  //긍정치, 부정치(tatal-긍정)
        backgroundColor:['#ff9f24', '#777777'],
        borderWidth: 2,
        borderColor:['#ffffff', '#ffffff'],
        scaleBeginAtZero: true,
        }]
    },
});