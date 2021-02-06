<!DOCTYPE html>
<html>
<head>  
    <!--Script Reference[1] -->  
    <script src="https://cdn.zingchart.com/zingchart.min.js"></script>
</head>
<body>  
    <!-- Chart Placement[2] -->  
    <div id="myChart"></div>  
    
    <script>    
        let myConfig = {      
            type: 'bar',      
            title: {        
                text: 'Data Basics',        
                fontSize: 24,      
            },      
            legend: {        
                draggable: true,      
            },      
            scaleX: {        
                // Set scale label        
                label: { text: 'Days' },        
                // Convert text on scale indices        
                labels: [ 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun' ]      
            },      
            scaleY: {        
                // Scale label with unicode character        
                label: { text: 'Temperature (°F)' }      
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
            series: [        
                {          
                    // Plot 1 values, linear data          
                    values: [23,20,27,29,25,17,15],          
                    text: 'Week 1',        
                },        
                {          
                    // Plot 2 values, linear data          
                    values: [35,42,33,49,35,47,35],          
                    text: 'Week 2'        
                },        
                {          
                    // Plot 2 values, linear data          
                    values: [15,22,13,33,44,27,31],          
                    text: 'Week 3'        
                }      
            ]    
        };    
        // Render Method[3]    
        zingchart.render({      
            id: 'myChart',      
            data: myConfig,    
        });  
    </script>
</body>
</html>