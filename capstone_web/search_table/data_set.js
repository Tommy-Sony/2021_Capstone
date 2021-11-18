
d3.csv("senti_result_test.csv").then(function(data){
    var result = data;
    var button = d3.select("#button");
    var form = d3.select("#form");
    button.on("click", runEnter);
    form.on("submit", runEnter);

    function runEnter(){
        d3.select("tbody").html("");
    
        d3.event.preventDefault();
    
        var inputValue = d3.select("#user-input").property("value");
    
        var filterName = result.filter(result => reslut.name.includes(inputValue));
        
        for(var i=0;i<filterName.length;i++){
            d3.select("tbody").insert("tr").html(
                "<td>" + (output[i]['name'])+"</td>"+
                "<td>" + (output[i]['percp'])+"</td>"+
                "<td>" + (output[i]['percn'])+"</td>"+
                "<td>" + (output[i]['total'])+"</td>"+
                "<td>" + (output[i]['preview'])+"</td>"+
                "<td>" + (output[i]['nreview'])+"</td>")
        }
        
    };
    
});

// Defining the function
