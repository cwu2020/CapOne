// Google Map
let map;

// Markers for map
let markers = [];

// Info window
let info = new google.maps.InfoWindow();


// Execute when the DOM is fully loaded
$(document).ready(function() {

    // Styles for map
    // https://developers.google.com/maps/documentation/javascript/styling
    let styles = [

        // Hide Google's labels
        {
            featureType: "all",
            elementType: "labels",
            stylers: [
                {visibility: "off"}
            ]
        },

        {
            featureType: "administrative.neighborhood",
            elementType: "labels",
            stylers: [
                {visibility: "on"}
            ]
        },

        // Hide roads
        {
            featureType: "road",
            elementType: "geometry",
            stylers: [
                {visibility: "off"}
            ]
        }

    ];

    // Options for map
    // https://developers.google.com/maps/documentation/javascript/reference#MapOptions
    let options = {
        center: {lat: 37.7749, lng: -122.399}, // Cambridge, MA
        disableDefaultUI: true,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        maxZoom: 18,
        minZoom: 12,
        panControl: true,
        styles: styles,
        zoom: 13,
        zoomControl: true
    };

    // Get DOM node in which map will be instantiated
    let canvas = $("#map-canvas").get(0);

    // Instantiate map
    map = new google.maps.Map(canvas, options);

    // Configure UI once Google Map is idle (i.e., loaded)
    google.maps.event.addListenerOnce(map, "idle", configure);

    google.charts.load('current', {'packages':['corechart']});


    google.charts.setOnLoadCallback(drawChart);
    google.charts.setOnLoadCallback(drawOtherChart);


});

function drawChart()
{
    var dataset = [];

    var req = $.getJSON("/datapoints", function(data, textStatus, jqXHR) {

        for (let i = 0; i < data.length; i++)
        {
           var obj = [data[i].price, data[i].reviews_per_month];
           dataset.push(obj);

        }

    });



    req.success(function(response){
        dataset.sort(function(a, b)
        {
            var a_number = Number(a[0].replace(/[^0-9\.]+/g,""));
            var b_number = Number(b[0].replace(/[^0-9\.]+/g,""));
            return a_number - b_number;
        });



        console.log(dataset);

        dataset.unshift(['price', 'bookings per month']);
        var data1 = google.visualization.arrayToDataTable(dataset);

        var options = {
          title: 'Price vs Bookings',
          curveType: 'function',
          legend: { position: 'bottom' },
          width: 475,
          height: 300,
          chartArea:{left:40, right: 20}
        };

        var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

        chart.draw(data1, options);
    });

}

function drawOtherChart()
{
    var dataset = [];

    var req = $.getJSON("/otherdatapoints", function(data, textStatus, jqXHR) {

        for (let i = 0; i < data.length; i++)
        {
           var obj = [data[i].review_scores_rating, data[i].reviews_per_month];
           dataset.push(obj);

        }

    });


    req.success(function(response){
        dataset.sort(function(a,b) {
          return a[0] - b[0];
        });
        console.log(dataset);

        dataset.unshift(['review score', 'bookings per month']);
        var data1 = google.visualization.arrayToDataTable(dataset);

        var options = {
          title: 'Review Score vs Bookings',
          curveType: 'function',
          legend: { position: 'bottom' },
          width: 475,
          height: 300,
          chartArea:{left:40, right: 20}
        };

        var chart = new google.visualization.ScatterChart(document.getElementById('curve_chart2'));


        chart.draw(data1, options);
    });

}


function addHouse(listing)
{
    var myLatlng = new google.maps.LatLng(listing["latitude"], listing["longitude"]);
    var image = "https://www.waltersnissan.com/assets/d1772/img/btn_map_pointer.png";

    //https://www.yarraranges.vic.gov.au/files/content/public/lists/do-it-online-listing/rates/rates-icon.png
    // house icon for later

    var marker = new google.maps.Marker({
        position: myLatlng,
        map: map,
        label: listing["name"] + ", " + listing["price"],
        title: listing["name"] + ", " + listing["price"],
        icon: image
    });


    // To add the marker to the map, call setMap();
    markers.push(marker);

    google.maps.event.addListener(marker, 'click', function(event)
    {
        let list = "<ul>";
        list += "Neighborhood: " + listing["neighbourhood_cleansed"] + ", ";
        list += "Accommodates: " + listing["accommodates"];
        list+="</ul>";
        showInfo(marker, list);
    });
}


function addProperty(lat, long, data)
{
    var myLatlng = new google.maps.LatLng(lat, long);


    var image = "https://www.yarraranges.vic.gov.au/files/content/public/lists/do-it-online-listing/rates/rates-icon.png";


    var marker = new google.maps.Marker({
        position: myLatlng,
        map: map,
        label: "YOUR PROPERTY",
        title: "home",
        icon: image
    });


    // To add the marker to the map, call setMap();
    markers.push(marker);

    var sum = 0;
    var weeklyrevenue;
    var maxweeklyrevenue = 0;
    var maxindex = 0;
    var secondmaxindex = 0;
    var avgweeklyrevenue;
    var optimal;

    console.log(data);
    for (let i = 0; i<data.length; i++)
    {
        weeklyrevenue = Number(data[i].price.replace(/[^0-9\.]+/g,"")) * data[i].reviews_per_month / 4.2857;
        sum += weeklyrevenue;

        if (weeklyrevenue > maxweeklyrevenue)
        {
            secondmaxindex = maxindex;
            maxweeklyrevenue = weeklyrevenue;
            maxindex =i;
        }
    }
    avgweeklyrevenue = sum / data.length;
    optimal = (Number(data[maxindex].price.replace(/[^0-9\.]+/g,"")) + Number(data[secondmaxindex].price.replace(/[^0-9\.]+/g,""))) /2;
    console.log(data[maxindex].price);
    console.log(data[secondmaxindex].price);

    let div = "<div id='info'><p>The average weekly revenue is $" + avgweeklyrevenue + ". You can maximize revenue at a price per night of " + optimal + ".</p></div>";

    // Set info window's content
    info.setContent(div);

    // Open info window (if not already open)
    info.open(map, marker);

}

$(function() {
    $('form').submit(function() {
        $.ajax({
            type: 'POST',
            url: '/search',
            data: { lat: $( "#la" ).val(),
                    lng: $( "#lng" ).val() },
            success: function(response) {
                addProperty($( "#la" ).val(), $( "#lng" ).val(), response);
            }
        });

        return false;
    });
})




// Configure application
function configure()
{
    // Update UI after map has been dragged
    google.maps.event.addListener(map, "dragend", function() {

        // If info window isn't open
        // http://stackoverflow.com/a/12410385
        if (!info.getMap || !info.getMap())
        {
            update();
        }

        //stay in SF
        var strictBounds = new google.maps.LatLngBounds(
            new google.maps.LatLng(36.00, -124.00),
            new google.maps.LatLng(40.00, -120.00)
        );

        if (strictBounds.contains(map.getCenter())) return;

         // We're out of bounds - Move the map back within the bounds

         var c = map.getCenter(),
             x = c.lng(),
             y = c.lat(),
             maxX = strictBounds.getNorthEast().lng(),
             maxY = strictBounds.getNorthEast().lat(),
             minX = strictBounds.getSouthWest().lng(),
             minY = strictBounds.getSouthWest().lat();

         if (x < minX) x = minX;
         if (x > maxX) x = maxX;
         if (y < minY) y = minY;
         if (y > maxY) y = maxY;

         map.setCenter(new google.maps.LatLng(y, x));
    });


    // Update UI after zoom level changes
    google.maps.event.addListener(map, "zoom_changed", function() {
        update();
        if (map.getZoom() < 13) map.setZoom(13);
    });



    // Hide info window when text box has focus
    $("#q").focus(function(eventData) {
        info.close();
    });

    // Re-enable ctrl- and right-clicking (and thus Inspect Element) on Google Map
    // https://chrome.google.com/webstore/detail/allow-right-click/hompjdfbfmmmgflfjdlnkohcplmboaeo?hl=en
    document.addEventListener("contextmenu", function(event) {
        event.returnValue = true;
        event.stopPropagation && event.stopPropagation();
        event.cancelBubble && event.cancelBubble();
    }, true);


    // Update UI
    update();

    // Give focus to text box
    $("#q").focus();
}


// Remove markers from map
// function removeMarkers()
// {
//     for(var i = 0; i < markers.length; i++)
//     {
//         markers[i].setMap(null);
//     }
//     markers = [];
// }




// Show info window at marker with content
function showInfo(marker, content)
{
    // Start div
    let div = "<div id='info'>";
    if (typeof(content) == "undefined")
    {
        // http://www.ajaxload.info/
        div += "<img alt='loading' src='/static/ajax-loader.gif'/>";
    }
    else
    {
        div += content;
    }

    // End div
    div += "</div>";

    // Set info window's content
    info.setContent(div);

    // Open info window (if not already open)
    info.open(map, marker);
}


// Update UI's markers
function update()
{
    // Get map's bounds
    let bounds = map.getBounds();
    let ne = bounds.getNorthEast();
    let sw = bounds.getSouthWest();

    // Get places within bounds (asynchronously)
    let parameters = {
        ne: `${ne.lat()},${ne.lng()}`,
        q: $("#q").val(),
        sw: `${sw.lat()},${sw.lng()}`
    };
    $.getJSON("/update", parameters, function(data, textStatus, jqXHR) {

       // Remove old markers from map
    //   removeMarkers();

       // Add new markers to map
       for (let i = 0; i < data.length; i++)
       {
           addHouse(data[i]);
       }

    });
}