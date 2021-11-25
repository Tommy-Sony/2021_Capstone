/* const chart = document.querySelector('.doughnut');

const makeChart = (percent, classname, color) => {
    let i =1;
    let chartFn = setInterval(function(){
        if(i <= percent){
            colorFn(i, classname, color);
            i++;
        } else{
            clearInterval(chartFn);
        }
    }, 10);
}

const colorFn = (i, classname, color) => {
    classname.style.background - "conic-gradient(" + color + " 0%" + i + "%, #dedede " + i + "% 100%)";
}

makeChart(80, chart, '#f5b914');
*/

$(window).ready(function(){
    draw(80, 'doughnut', '#f5b914');
})

function draw(max, classname, colorname){
    var i=1;
    var func1 = setInterval(function(){
        if(i<max){
            color1(i, classname, colorname);
            i++;
        }else{
            clearInterval(func1);
        }
    }, 10);
}

function color1(i, classname, colorname){
    $(classname).css({"background":"conic-gradient("+colorname+" 0% "+i+"%, #6c8801"+i+"% 100%)"});
}