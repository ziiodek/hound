function load_profiles(assigned_id,economic_no,trailer_no){
if (assigned_id != "0"){
 var driver = document.getElementById('id_assigned_id');
 driver.value = assigned_id;
 }


 var vehicle = document.getElementById('id_vehicle_no');
 vehicle.value = economic_no;


var trailer = document.getElementById('id_trailer_no');
trailer.value = trailer_no;
}







