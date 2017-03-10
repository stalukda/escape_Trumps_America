
  <div class="country-chart">    <canvas id="barChart"></canvas>
    <div id="barLegend" class="chart-legend"></div>
  </div>

<script>

    // This code below creates a JS array (good) but of the whole row, inlcuding TRs...table rows (bad)
    // var allCountries = [];
    // allCountries.push($('.allCountries').get());

    //This code is much better.. 
    //Creates a jquery array by mapping to javascript array bc Ajax does not recognize JQuery arrays 
    //Alternative implementation: session
    var countriesArray = $.map($('.allCountries'), function(item) {
         return $(item).data('country-id')
    });

    var options = {
      responsive: true
    };

    var ctx_bar = $("#barChart").get(0).getContext("2d");

    console.log('countries array', countriesArray);

    $.get("/country_picks.json", {countryList: countriesArray}, function (data) {

      console.log("data", data);

    var myBarChart = new Chart(ctx_bar, {
                                  type: 'bar',
                                  data: data,
                                  options: options
    });

      $("#barLegend").html(myBarChart.generateLegend());
    });


WORKING templates/cost_of_living_map.html
<!DOCTYPE html>
<html>

  <head>
      <!-- <link rel="stylesheet" href="/resources/demos/style.css"> -->
      <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
      <script type='text/javascript' src='https://www.google.com/jsapi'></script>
      <title> Cost of Living Index 2017</title>

  </head>

  <body>
    <h2> Cost of Living Index Throughout the World </h1>

    <div class="container">
    <div class="page-header">
    </div>


       <div style="width:100%;" id="header_gmaps" >
        <form>
             General filters:  <select id="generalFilter" class="mapFilter">
            <option value="col_index" selected="selected">Cost of Living Index</option>           
            <option value="bread_price"> Average Bread Price</option>
            <option value="meal_price"> Average Restaurant Meal Price </option>
            <option value="apt_price"> Average Monthly Apt Rental Price </option>
            <option value="health_care_index"> Health Care Index </option>
            <option value="crime_index"> Crime Index </option>
            <option value="pollution_index"> Pollution Index </option>
            <option value="traffic_index"> Traffic Index </option>
            <option value="groceries_index"> Groceries Index </option>
            <option value="rent_index"> Rent Index </option>   
            <option value="property_price_to_income_ratio"> Property Price to Income Ratio  </option>         
            </select>
        </form>

        <div id="customFilterForm">
        <form id = "customFilter">
            Filter by: <input type="text" id="maxAmount" value="max value"><br>
            <input type="submit" id="customFilterSubmit">
        </form>

        <div id="multiFilterForm">
        <form id = "multiFilter">
            Cost of Living Index: <input type="text" id="col_index_multi" onmouseover=""><br>
            Bread Price: <input type="text" id="bread_price_multi"><br>

            Inexpensive Restaurant Meal Price: <input type="text" id="meal_price_multi"><br>
            Monthly Apt Rental Price: <input type="text" id="apt_price_multi"><br>
            Groceries Index: <input type="text" id="groceries_index_multi"><br>
            Rent Index: <input type="text" id="rent_index_multi"><br>
            Property Price to Income Ratio: <input type="text" id="property_price_to_income_ratio_multi"><br>
            <br>
            <br>
            <p> Quality of Life Factors </p>            
            Health Care Index: <input type="text" id="health_care_index_multi"><br>
            Crime Index: <input type="text" id="crime_index_multi"><br>
            Pollution Index: <input type="text" id="pollution_index_multi"><br>
            Traffic Index: <input type="text" id="traffic_index_multi"><br>
            <input type="submit" id="multiFilterSubmit">
        </form>
      
     <div class="indices_info">
        <a href="/indices_info" title="About these indices" class="indices_info">
        <img src="https://www.numbeo.com/images/information.png" class="image_help" alt="Info"/> Explain these indices</a></div>


      <div id="chart_div" class="country_gmaps_rankings"></div>

      <table id="table_id" class="display">
    
        <tr>
          <th>Countries to Consider</th>
        </tr>
    
        <tr>
          <td>France</td>
        </tr>

        <tr>
          <td>Germany</td>
        </tr>

      </table>

</div>
       <script type='text/javascript'>
        google.load('visualization', '1', {'packages': ['geochart']});
        google.setOnLoadCallback(updateMapData);
       
        function drawMap(results) {
            var data = new google.visualization.DataTable();
            data.addColumn('string', 'Country');
            data.addColumn('number', $( "select#generalFilter option:selected" ).val());
            data.addRows(results.items);
            var options = {
            colorAxis: {colors: [ '#551a8b', '#17e617', '#ffff00', '#e6e617', '#ffa500', '#ff0000']}}
            var chart = new google.visualization.GeoChart(document.getElementById('chart_div'));
            
            chart.draw(data, options);
        };
        
        function updateMapData(){
          
            var currentOptionRoute = $( "select#generalFilter option:selected" ).val();
            $.get("/" + currentOptionRoute + ".json", drawMap)
            };
        $('#generalFilter').on('change', updateMapData);
        function filterMapData(evt){
            evt.preventDefault();
            var currentOptionRoute = $( "select#generalFilter option:selected" ).val();
            var formInputs = {
              "filterMax": $("#maxAmount").val() 
              };
            $.get("/" + currentOptionRoute + "Filter" + ".json", formInputs, drawMap);        
            };
        $('#customFilter').on('submit', filterMapData);
        function drawMultiFilterMap(results) {
            var data = new google.visualization.DataTable();
            data.addColumn('string', 'Country');
            data.addColumn('number', 'Cost of Living Index');
            data.addRows(results.items);
            var options = {
            colorAxis: {colors: [ '#551a8b', '#17e617', '#ffff00', '#e6e617', '#ffa500', '#ff0000']}}
            var chart = new google.visualization.GeoChart(document.getElementById('chart_div'));
            
            chart.draw(data, options);
        };
        
        function MultiFilterMapData(evt){
            evt.preventDefault();
            var formInputs = {
              "colindex": $("#col_index_multi").val(),
              "breadprice": $("#bread_price_multi").val(),
              "mealprice": $("#meal_price_multi").val(),
              "apt_price": $("#apt_price_multi").val(),
              "groceries_index": $("#groceries_index_multi").val(),
              "rent_index": $("#rent_index_multi").val(),
              "property_price_to_income_ratio": $("#property_price_to_income_ratio_multi").val(),
              "health_care_index": $("#health_care_index_multi").val(),
              "crime_index": $("#crime_index_multi").val(),
              "pollution_index": $("#pollution_index_multi").val(),
              "traffic_index": $("#traffic_index_multi").val()
              };
            $.get("/multiFormPick.json", formInputs, drawMultiFilterMap);        
            };
        $('#multiFilterSubmit').on('click', MultiFilterMapData);
        </script>


   </body>
</html>



WORKING JUMBOTRON

<div class="container">
  <div class="jumbotron">
    <h1> Escape Trump's America</h1>

    <p class="lead">Find a home for the next 4 years.</p>

    <p>
      <a class="btn btn-lg btn-primary" href="/login" role="button">
        Log in &raquo;
      </a>
    </p>
  </div>
</div>