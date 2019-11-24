class Node {
  constructor(longitude, latitude, address, googlePlaceid) {
    this.longitude = longitude;
    this.latitude = latitude;
    this.address = address;
    this.googlePlaceid = googlePlaceid;
  }
}


class mileStoneView{

  constructor() {
      this.mileStones = [50,100,200,0]
      this.stepsCovered = 0;
      this.requiredSteps = 0;
      this.equipment_list = [];

      this.displayCountDownSet = false;
      this.displayCountDown;
      this.resetStepProgress();
  }
  
  resetStepProgress(){
    
    localStorage.lastMileStoneUpdate = lastMileStoneUpdate;
    localStorage.mileStonesCovered = 0;
    localStorage.stepsCovered = 0;
    this.displayCountDownSet = false;
    clearInterval(this.displayCountDown); 

    var lastMileStoneUpdate = moment(localStorage.lastMileStoneUpdate);

    if (lastMileStoneUpdate.isValid() == false){
        lastMileStoneUpdate = moment();
    }

    if(lastMileStoneUpdate.isSame(new Date(), "day") == false || localStorage.getItem("lastMileStoneUpdate") === null) {
      localStorage.lastMileStoneUpdate = lastMileStoneUpdate;
      localStorage.mileStonesCovered = 0;
      localStorage.stepsCovered = 0;
      this.displayCountDownSet = false;
      clearInterval(this.displayCountDown);
    }

    this.updateStepProgress();
  }

  async getNextMileStone(){
    
    if(2 >= localStorage.mileStonesCovered){
      localStorage.stepsCovered = 0;
      localStorage.mileStonesCovered = parseInt(localStorage.mileStonesCovered) + 1;
      var data = {};
      data.userID = localStorage.userID;
      var response = await post_to_server("reachedMilestone/", data);

      this.equipment_list.push(response['EQUIPMENT_OBJ']);

        if (response["ERROR_CODE"] == 0){
          Swal.fire({
            title: 'You earned '+ response["EQUIPMENT_OBJ"]['NAME'],
            imageUrl: response["EQUIPMENT_OBJ"]["IMG"],
            html: response["EQUIPMENT_OBJ"]['DESCRIPTION']
          })
        }
        else{
          Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Error geting next milestone'
          })
        }
    

    }
  }

  updateStepProgress(){
     var oThis = this;

      let percentage = Math.round((localStorage.stepsCovered/this.mileStones[localStorage.mileStonesCovered])*100);
      if(this.displayCountDownSet == false){
        if(localStorage.mileStonesCovered == 3){
          this.displayCountDown = setInterval(function(){oThis.updateTimeTillMileStoneReset(oThis);}, 1000);
          this.displayCountDownSet = true;
        } 
        else{
          this.displayCountDownSet = false;
          $('#step_progress').html("Steps Left: " + localStorage.stepsCovered +"/" + this.mileStones[localStorage.mileStonesCovered] +" Steps");
          $('#progress_bar_bar').css("width", percentage+"%");
          document.getElementById("progress_bar_bar").innerHTML = percentage+"%";
        }
      }
  }

  updateTimeTillMileStoneReset(oThis){
    var now = moment(),
    tomorrow = moment().add(1, 'day').startOf('day'),
    difference = moment.duration(tomorrow.diff(now))
    $('#step_progress').html("MileStone Resets After: " + difference.hours() + "h " + difference.minutes() + "m " + difference.seconds() +"s");
    $('#progress_bar_bar').css("width", "100%");
    document.getElementById("progress_bar_bar").innerHTML = "100%";
    this.resetStepProgress();
  }

  incrementSteps(distance){

    if(isNaN(distance) == false){
      localStorage.stepsCovered = parseInt(localStorage.stepsCovered) + distance;
      if(parseFloat(localStorage.stepsCovered) >= parseInt(this.mileStones[localStorage.mileStonesCovered])){ 
        this.getNextMileStone();
      }
      this.updateStepProgress();
    }
    
  }
}


class RouteManager {

  constructor() {

    this.timeStart;

    this.googleRouteResponse;
    this.selectedGoogleRouteIndex;
    this.navigationStarted = false;

    this.startNode = new Node();
    this.endNode = new Node();
    this.previousLocation = new Node();
    this.mileStoneView = new mileStoneView();
    this.distanceCovered = 0;
    this.selectRouteIndex = 0;
    this.currentRouteInstructionIndex = 0;
    this.gpsStepsErrorThreshold = 2;
    this.gpsStart();
    this.currentLocationSetted = false;
    

    window.addEventListener('deviceorientationabsolute', function(event) {
      var alpha = null;
      //Check for iOS property
      if (event.webkitCompassHeading) {
          alpha = event.webkitCompassHeading;
      }
      //non iOS
      else {
          alpha = event.alpha;
      }
      var locationIcon = myloc.get('icon');
      locationIcon.rotation = 360 - alpha;
      myloc.set('icon', locationIcon);
      }, false);
  
  }

  gpsStart(){
    var oThis = this;
    navigator.geolocation.watchPosition(
      function(pos){oThis.gpsSuccess(pos,oThis);},
      function(pos){oThis.gpsError(pos,oThis);},
      { maximumAge:50000, timeout:5000, enableHighAccuracy: true }
    ); 
  }

  gpsSuccess(pos,oThis) {
      
      var newPosition = new Node(pos.coords.longitude, pos.coords.latitude, 'undefined', 'undefined');

      if(oThis.navigationStarted){ // check if navigationGame has started
        let stepsChange = Math.floor(oThis.calulateDistance(oThis.previousLocation,newPosition) * 1312.3359580052); //Convert Km To Steps
        
        if(oThis.gpsStepsErrorThreshold > stepsChange){
          stepsChange = 0;
        }else{
          stepsChange -= oThis.gpsStepsErrorThreshold;
        }

        oThis.distanceCovered += stepsChange;
        oThis.mileStoneView.incrementSteps(stepsChange);
        
        if(oThis.approximate(newPosition, oThis.endNode)){
          oThis.navigationStarted = false;
          oThis.endGame();
        }

        let routeInstructionNode = new Node(oThis.routeInstruction[oThis.currentRouteInstructionIndex].end_location.lng(), oThis.routeInstruction[oThis.currentRouteInstructionIndex].end_location.lat(), 'undefined', 'undefined');
        let distanceToCheckpoint = oThis.calulateDistance(newPosition, routeInstructionNode);
  
        if(distanceToCheckpoint > 0.1){
          document.getElementById("direction_distance").innerHTML = " | " + distanceToCheckpoint.toFixed(1) + " Km";
        }else{
          document.getElementById("direction_distance").innerHTML = " | " + (distanceToCheckpoint * 1000).toFixed(0) + " Meters";
        }

        

          for (let j = 0; j < oThis.routeInstruction.length; j++){
            routeInstructionNode = new Node(oThis.routeInstruction[j].end_location.lng(), oThis.routeInstruction[j].end_location.lat(), 'undefined', 'undefined');
  
            if(oThis.approximate(newPosition, routeInstructionNode)){
              
              if(oThis.routeInstruction.length-1 != j){
                oThis.currentRouteInstructionIndex = j + 1; 
                oThis.updateRouteDirectionInstruction();
              }
            } 
          }
      }

      myloc.setPosition(new google.maps.LatLng(pos.coords.latitude, pos.coords.longitude));
      oThis.previousLocation = newPosition;

      if(!this.currentLocationSetted){
        oThis.setOriginAsCurrentLocation();
        oThis.currentLocationSetted = true;
      }
  }

  // onError Callback receives a PositionError object
  //
  gpsError(error) {
    console.error("Accuracy request failed: error code="+error.code+"; error message="+error.message);
    Swal.fire({
      icon: 'error',
      title: 'GPS Error',
      text: 'Unable get your location. Please reenable your GPS to continue'
    });
  }

  updateRouteDirectionInstruction(){
    
    nextStepMarker.setPosition(new google.maps.LatLng(this.routeInstruction[this.currentRouteInstructionIndex].end_location.lat(), this.routeInstruction[this.currentRouteInstructionIndex].end_location.lng()));
    document.getElementById("direction_step").innerHTML = (this.currentRouteInstructionIndex + 1)+". "+this.routeInstruction[this.currentRouteInstructionIndex].instructions;

  }

  centerCurrentLocation(){
    map.panTo(myloc.getPosition());
  }

  validateAddress() {

    var oThis = this;
    var route_orgin = $('#route_origin').val();
    var route_destination = $('#route_destination').val();
    var startNode;
    var endNode;
  
    //Check if origin address is valid
    geocoder.geocode({ 'address': route_orgin}, function (results, status) { 
      if (status === 'OK') { 
     
         startNode = new Node(results[0].geometry.location.lng(), results[0].geometry.location.lat(), results[0].formatted_address, results[0].place_id);
         oThis.startNode = startNode;
         if(endNode) { 
          oThis.startNode = startNode;
          oThis.getRoutes();
        }
      }
      else {
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'Origin address Does not exists'
        });
        return;
      }
    });

    //Check if route destination address is valid
    geocoder.geocode({ 'address': route_destination}, function (results, status) {
      if (status === 'OK') {
          endNode = new Node(results[0].geometry.location.lng(), results[0].geometry.location.lat(), results[0].formatted_address, results[0].place_id);
          if(startNode) {  
            oThis.endNode = endNode;
            oThis.getRoutes(); 
          }
      }
      else {
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'Destination address does not exists'
        });

        return;
      }
    });

  }

  setOriginAsCurrentLocation(){
    var latlng = {lat:this.previousLocation.latitude, lng: this.previousLocation.longitude };
    geocoder.geocode({ 'location': latlng}, function (results, status) {
      if (status === 'OK') {
         document.getElementById("route_origin").value = results[0].formatted_address;
      }
      else {

        return;
      }
    });
  }

  async getRoutes() {

    var oThis = this;
    //Get routes from google direction service api
    let request = {
      origin: this.startNode.address,
      destination: this.endNode.address,
      travelMode: 'WALKING',
      provideRouteAlternatives: true,
    };

    //Get routes from google direction service api
    directionsService.route(request, async function (response, status) {
      if (status === 'OK') {

        oThis.googleRouteResponse = response;

        let number_of_checked_stars = 0;
        var htmlString = "";

        htmlString += "<li class='list-group-item rounded-0  border-left-0  border-right-0' style='vertical-align: middle; line-height: 40px;'> Rating: ";
        
        var data = {};
        data.userID = localStorage.userID;
        data.starting_address = oThis.startNode.googlePlaceid;
        data.ending_address = oThis.endNode.googlePlaceid;
        //data.starting_address = "abcdefg";
        //data.ending_address = "jklmnop";
        var response2 = await post_to_server("getRatings/", data);
        if (response2["ERROR_CODE"] == 0){
           number_of_checked_stars = Math.round(parseFloat(response2.DETAILS.AVG_RATING));
        }
        
        for (let i = 0; i < 5; i++) {
          if(number_of_checked_stars > i){
            htmlString += "<span class='fa fa-star checked'></span>";
          }else{
            htmlString += "<span class='fa fa-star'></span>";
          }
        }
        
        htmlString += '<button type="button" class="btn btn-primary float-right" onclick="routemanager.bookmarkRoutes();">Bookmark</button></li>';
        
        //List out the different routes the user can take in the plan route view
        for (let k in response['routes']) {
          let route_description = ""; 
          let v = response['routes'][k]['legs'][0];
          route_description += "Distance: " + v['distance']['text'] + "<br>";
          route_description += "Duration: " + v['duration']['text'] + "<br>";
          htmlString += "<li class='list-group-item rounded-0  border-left-0  border-right-0' onclick='routemanager.renderRoute("+k+")'>"+route_description+"</li>";
        }
        document.getElementById("route_list").innerHTML = htmlString;

      }
      else {
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'No address combination not possible'
        });
        return;
      }
    });
  }
  startGame(){
    this.distanceCovered = 0;
    this.currentRouteInstructionIndex = 0;
    this.navigationStarted = true;
    this.timeStart = moment();

    this.routeInstruction = this.googleRouteResponse.routes[this.selectRouteIndex].legs[0].steps;
    this.updateRouteDirectionInstruction();
    nextStepMarker.setVisible(true);
    $('#map_bottom').hide();
    $('#stop_game').show();
    animateMapZoomTo(map, 19); // call smoothZoom, parameters map, final zoomLevel, and starting zoom level
    map.panTo(new google.maps.LatLng(this.previousLocation.latitude,this.previousLocation.longitude));
    console.log("End: " + this.endNode.latitude + ", " + this.endNode.longitude);
  }
  endGame(){
    

    var duration = moment.duration(moment().diff(this.timeStart));

    let htmlString = "Time Taken: " + duration.get('hours') +" Hours " + duration.get('minutes')+" Mins " + duration.get('seconds') + " Sec";
    htmlString += "<br>Steps Covered: " + this.distanceCovered + " steps";
    htmlString += "<br>Equipment Earned: ";

    for (let i = 0; i < this.mileStoneView.equipment_list.length; i++) {
      htmlString +=  '<img src="' + this.mileStoneView.equipment_list[i]['IMG'] + '" height="40" width="40">';
    }
    if(this.mileStoneView.equipment_list.length == 0){
      htmlString += "No equipment earned";
    }

    this.mileStoneView.equipment_list = [];
    this.distanceCovered = 0;
    this.navigationStarted = false;
    document.getElementById("direction_step").innerHTML = "";
    document.getElementById("direction_distance").innerHTML = "";

    document.getElementById("modal_stats_body").innerHTML = htmlString;
    $('#modal_stats').modal('toggle');
    $('#map_bottom').show();
    $('#stop_game').hide();
    nextStepMarker.setVisible(false);
    this.returnToRoute();
  }

  renderRoute(selectRouteIndex) {
    this.selectRouteIndex = selectRouteIndex;
    directionsRenderer.setDirections(this.googleRouteResponse);
    directionsRenderer.setRouteIndex(this.selectRouteIndex);
    document.getElementById("direction_step").innerHTML = "";

    //console.log(this.googleRouteResponse.routes[0].legs[0].steps[0]);
    //console.log(this.googleRouteResponse.routes[0].legs[0].steps[0].end_location.lng());
    
    $('#map_wrapper').css("left", "0");     
    $('#route_selector').hide();
  }

  returnToRoute(){
    $('#map_wrapper').css("left", "-100%");
    $('#route_selector').show();
  }

  // Returns value in KM
  calulateDistance(node1, node2) {
    var p = 0.017453292519943295;    // Math.PI / 180
    var c = Math.cos;
    var a = 0.5 - c((node2.latitude - node1.latitude) * p) / 2 +
      c(node1.latitude * p) * c(node2.latitude * p) *
      (1 - c((node2.longitude - node1.longitude) * p)) / 2;
    return 12742 * Math.asin(Math.sqrt(a)); // 2 * R; R = 6371 km
  }

  approximate(node1,node2){

    //if within 100m return true
    //console.log("dis diff:" + this.calulateDistance(node1, node2));
    //console.log(0.1 >= this.calulateDistance(node1, node2));
    if(0.05  >= this.calulateDistance(node1, node2) ){
      return true;
    }
    return false;

  }
  


  
  bookmarkRoutes(){
    var oThis = this;

      Swal.fire({
        title: 'Bookmark Route',
        input: 'text',
        inputAttributes: {
          autocapitalize: 'off'
        },
        showCancelButton: true,
        confirmButtonText: 'Add',
        showLoaderOnConfirm: true,
        preConfirm: (label) => {

          var data = {};
          data.userID = localStorage.userID;
          data.starting_address = oThis.startNode.address;
          data.ending_address = oThis.endNode.address;
          data.bookmark_name = label;


          var response = post_to_server("add_bookmark/", data);

          
        }
      })
    }

}




