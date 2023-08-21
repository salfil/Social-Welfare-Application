/*portion of code from Bobby Stearman, scope: directions functionality  
  https://github.com/bobby-didcoding/did_django_google_maps_api/static/main.js
  Date Published:  July 20th 2021*/

/*below is a functionality which facilitates the visibility of the directions table based on the users actions.  */
function DirectionsToggle(){
    var el = $('#dir-toggle');
    var dir_table = $('#dir-table')
    if (dir_table.attr("hidden") == "hidden") {
      dir_table.fadeIn()
      dir_table.removeAttr("hidden")
      el.html('hide <a href="javascript:void(0)" onclick="DirectionsToggle()">here')
    } else {
      dir_table.fadeOut()
      dir_table.attr("hidden", "hidden")
      el.html('click <a href="javascript:void(0)" onclick="DirectionsToggle()">here')
    }
  }
  
  