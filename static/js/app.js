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
        for (var i = 0; i < incomingdata.length; i++){
            if(incomingdata[i].platform == dataset){
                choice.append("option").attr("value", incomingdata[i].publisher_name).text(incomingdata[i].publisher_name);
            };
        };
    });
};

// Function for appending rows and columns to table based on filtered applications
filteredApps.forEach((filteredApp) => {
    var row = tbody.append("tr");
    Object.entries(filteredApp).forEach(([key, value]) => {
      var cell = row.append("td");
      cell.text(value);
    });
  });

// When the browser loads, makeResponsive() is called.
makeResponsive();

// When the browser window is resized, makeResponsive() is called.
d3.select(window).on("resize", makeResponsive);
