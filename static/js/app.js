function init(){
    d3.json("http://127.0.0.1:5000/api/v1.0/app_rankings_data").then((incomingdata)=>{
        var name = incomingdata[0].platform;
        console.log(name);
        // var metadata = incomingdata[0].metadata;
        // //console.log(metadata);
        // var sample = incomingdata[0].samples;
        // //console.log(sample);
        // var choice = d3.select("#selDataset");
        // var index = 0;
        // name.forEach(element => {
        //     //console.log(element);
        //     var specimen = choice.append("option");
        //     specimen.attr("value",index).text(element);
        //     index = index + 1;
        // });
        // horizontalbar(sample[0]);
        // bubblegraph(sample[0]);
        // createmeta(metadata[0]);
    
    });
};

//init();

var dateParser = d3.timeParse("%Y-%m-%d");

// d3.selectAll("#selDataset").on("change", optionChanged);
// function optionChanged(){
//     var dropdown = d3.select("#selDataset");
//     var dataset = dropdown.property("value");
//     d3.json("../samples.json").then((incomingdata)=>{
//         var metadata = incomingdata[0].metadata;
//         var sample = incomingdata[0].samples;
//         horizontalbar(sample[dataset]);
//         bubblegraph(sample[dataset]);
//         createmeta(metadata[dataset]);
//     });
// };

function horizontalbar(value){
    var otu = "OTU ";
    var yaxis = [];
    value.otu_ids.slice(0,10).forEach(y => yaxis.push(otu.concat(y)));
    var trace = {
        x: value.sample_values.slice(0,10).reverse(),
        y: yaxis.reverse(),
        text: value.otu_labels.slice(0,10).reverse(),
        type: "bar",
        orientation: "h"
    };
    var chartdata = [trace];


    Plotly.newPlot("bar", chartdata);
};

function bubblegraph(value){
    var trace = {
        x: value.otu_ids,
        y: value.sample_values,
        text: value.otu_labels,
        mode: "markers",
        marker:{
            color: value.otu_ids,
            size: value.sample_values
        }
    };

    var chartdata = [trace];

    Plotly.newPlot("bubble", chartdata);
};


d3.selectAll("#platformSelection").on("change", platformSelect);
function platformSelect(){
    var dropdown = d3.select("#platformSelection");
    var dataset = dropdown.property("value");
    //console.log(dataset);
    var selectedPlatform = d3.select(".publishdiv");
    selectedPlatform.style("display","block");
    var choice = selectedPlatform.select("#selDataset");
    choice.selectAll("option").remove();
    d3.json("http://127.0.0.1:5000/api/v1.0/app_rankings_data").then((incomingdata)=>{
        //console.log(dataset);
        choice.html("<option disabled selected value>-- choose one --</option>");
        for (var i = 0; i < incomingdata.length; i++){
            if(incomingdata[i].platform == dataset){
                choice.append("option").attr("value", incomingdata[i].publisher_name).text(incomingdata[i].publisher_name);
            };
        };
    });
};



d3.selectAll("#selDataset").on("change", optionChanged);
function optionChanged(){
    var platformselection = d3.select("#platformSelection").property("value");
    var publisherselection = d3.select("#selDataset").property("value");
    d3.select("tbody").selectAll("tr").remove();
    d3.json("http://127.0.0.1:5000/api/v1.0/app_rankings_data").then((incomingdata)=>{
        for (var i = 0; i < incomingdata.length; i++){
            if(incomingdata[i].platform == platformselection && incomingdata[i].publisher_name == publisherselection){
                //console.log(incomingdata[i].app[1].app_name);
                makeTable(incomingdata[i].app)
                var seriesData = createSeries(incomingdata[i].app);
                // for (var j = 0; j < incomingdata[i].app.length; j++){
                //     console.log(incomingdata[i].app[j].app_name);
                //     console.log(incomingdata[i].app[j].date);
                //};
            };
        };
    // CHART CONFIG
// -----------------------------
let myConfig = {
    type: 'line',
    title: {
      text: publisherselection,
      fontSize: 24,
    },
    legend: {
      draggable: true,
    },
    scaleX: {
      // Set scale label
      label: { text: 'Date' },
      // Convert text on scale indices
      labels: [ '2021-01-26', '2021-01-27']
    },
    scaleY: {
        mirrored: true,
      // Scale label with unicode character
      label: { text: 'Grossing Ranking' }
    },
    plot: {
      // Animation docs here:
      // https://www.zingchart.com/docs/tutorials/styling/animation#effect
      animation: {
        effect: 'ANIMATION_EXPAND_BOTTOM',
        method: 'ANIMATION_STRONG_EASE_OUT',
        sequence: 'ANIMATION_BY_NODE',
        speed: 275,
      }
    },
    series: seriesData
  };
  // Render Method[3]
zingchart.render({
    id: 'myChart',
    data: myConfig,
  });
    });
};

// Function for appending rows and columns to table based on filtered applications
// filteredApps.forEach((filteredApp) => {
//     var row = tbody.append("tr");
//     Object.entries(filteredApp).forEach(([key, value]) => {
//       var cell = row.append("td");
//       cell.text(value);
//     });
//   });

// Function for calculating the current quarter average ranking
function currentQ(appData){
    var returnSeries = []
    for (var j = 0; j < appData.length; j++){
        returnSeries.push(appData[j].date[appData[j].date.length - 1]);
        // for (var k = 0; k < appData[j].date.length; k++){
        //     console.log(appData[j].date[k])
        //     console.log(dateParser(appData[j].date[k].date))
        //     console.log(appData[j].date[k].Grossing)
        // };
    };
    return returnSeries;
};

// d3.max(hairData, d => d.num_hits


// When the browser loads, makeResponsive() is called.
//makeResponsive();

// When the browser window is resized, makeResponsive() is called.
d3.select(window).on("resize", makeResponsive);

function makeTable(Data){
    //var publisherName = Data[0].app_name;
    //console.log(publisherName);
    //console.log(Data);
    d3.select("tbody").selectAll("tr")
    .data(Data)
    .enter() // creates placeholder for new data
    .append("tr") // appends a div to placeholder
    .html(function(d) {
        return `<td>${d.app_name}</td><td>${d.date[d.date.length-1].date}</td><td>${d.date[d.date.length-1].Grossing}</td>`});  // sets the html in the div to an image tag with the link
};

function createSeries(dataSeries){
    var backColors = ['#E34247','#FEB32E', '#31A59A', '#6A0DAD', '#FF007F']
    var seriesResult = [];
    var arrayLength = dataSeries.length;
    for (var i = 0; i < arrayLength; i++) {
        var dataDict = dataSeries[i];
        var app_name = dataDict['app_name'];
        var rank_date = dataDict['date'];
        var value = [];
        if (rank_date[0]['date'] == "2021-01-27" ){
            value.push(null);
            value.push(+rank_date[0]['Grossing']);
        }
        else if (rank_date[0]['date'] == "2021-01-26" && rank_date.length < 2){
            value.push(+rank_date[0]['Grossing']);
            value.push(null);
        }
        else {
            for (var j = 0; j < 2; j++) {
                value.push(+rank_date[j]['Grossing']);
            };
        };
        var lineColor =  backColors[i];
        var marker = {'backgroundColor': backColors[i]};
        var text = app_name;
        var unit_dict = {'values': value, 'text':text};
        seriesResult.push(unit_dict);
    };
    return seriesResult

};
