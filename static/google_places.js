/*portion of code from Bobby Stearman
    scope: autocompletion of addresses/places.
  https://github.com/bobby-didcoding/did_django_google_maps_api/static/google_places.js
  Date Published:  July 20th 2021*/


/* below is where the call to the api is made */
$.getScript( "https://maps.googleapis.com/maps/api/js?key=" + google_api_key + "&libraries=places") 
.done(function( script, textStatus ) {
    google.maps.event.addDomListener(window, "load", initAutocomplete())

})


/* below is the functionality to autocomplete the searching for the addresses */
let autocomplete_a;
let autocomplete_b;

function initAutocomplete() {

  autocomplete_a = new google.maps.places.Autocomplete(
   document.getElementById('id-google-address-a'),
   {
       types: ['address'],
       componentRestrictions: {'country': ['uk']},
   })
  
  autocomplete_a.addListener('place_changed', function(){
    onPlaceChanged('a')
  });


  autocomplete_b = new google.maps.places.Autocomplete(
   document.getElementById('id-google-address-b'),
   {
       types: ['address'],
       componentRestrictions: {'country': ['uk']},
   })
  
  autocomplete_b.addListener('place_changed', function(){
    onPlaceChanged('b')
  });

}

/* gets latitude and longitude coordinates using google maps api and updates fields on the web page */
function onPlaceChanged (addy){

    let auto
    let el_id
    let lat_id
    let long_id

    if ( addy === 'a'){
        auto = autocomplete_a
        el_id = 'id-google-address-a'
        lat_id = 'id-lat-a'
        long_id = 'id-long-a'
    }
    else{
        auto = autocomplete_b
        el_id = 'id-google-address-b'
        lat_id = 'id-lat-b'
        long_id = 'id-long-b'
    }

    var geocoder = new google.maps.Geocoder()
    var address = document.getElementById(el_id).value

    geocoder.geocode( { 'address': address}, function(results, status) {

        if (status == google.maps.GeocoderStatus.OK) {
            var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();

            $('#' + lat_id).val(latitude) 
            $('#' + long_id).val(longitude) 

            CalcRoute()
        } 
    }); 
}

/* below is where form is validated */
function validateForm() {
    var valid = true;
    $('.geo').each(function () {
        if ($(this).val() === '') {
            valid = false;
            return false;
        }
    });
    return valid
}

/* calculates a route based on the latitude and longitude coordinates of two addresses */
function CalcRoute(){

    if ( validateForm() == true){
      var params = {
          lat_a: $('#id-lat-a').val(),
          long_a: $('#id-long-a').val(),
          lat_b: $('#id-lat-b').val(),
          long_b: $('#id-long-b').val(),
      };

      var esc = encodeURIComponent;
      var query = Object.keys(params)
          .map(k => esc(k) + '=' + esc(params[k]))
          .join('&');

      url = '/map?' + query
      window.location.assign(url)
    }

}
