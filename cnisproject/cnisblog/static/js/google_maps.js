function initMap() {
  var center = {lat: 14.5648, lng: 120.9931};
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 10,
    center: center
  });
  var marker = new google.maps.Marker({
    position: center,
    map: map
  });
}
