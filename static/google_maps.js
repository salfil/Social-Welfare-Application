/*portion of code from Bobby Stearman  
  scope: caclculation of directions
  https://github.com/bobby-didcoding/did_django_google_maps_api/static/google_maps.js
  Date Published:  July 20th 2021*/


/* below is where the api call is made */
$.getScript( "https://maps.googleapis.com/maps/api/js?key=" + google_api_key + "&libraries=places") 
.done(function( script, textStatus ) {
    google.maps.event.addDomListener(window, "load", initMap)

})

/* below is a function to display the route and actual directions */
function initMap() {
    var directionsService = new google.maps.DirectionsService;
    var directionsDisplay = new google.maps.DirectionsRenderer;
    var map = new google.maps.Map(document.getElementById('map-route'), {
        zoom: 7,
        center: {lat: lat_a, lng: long_a}
    });
    directionsDisplay.setMap(map);
    calculateAndDisplayRoute(directionsService, directionsDisplay);

}

/* below is a function to form the calculation and display the route based on mode of travel */
function calculateAndDisplayRoute(directionsService, directionsDisplay) {
    directionsService.route({
        origin: origin,
        destination: destination,
        travelMode: 'DRIVING'
    }, function(response, status) {
      if (status === 'OK') {
        directionsDisplay.setDirections(response);


      } else {

        alert('Directions request failed due to ' + status);
        window.location.assign("/route")
      }
    });
}
