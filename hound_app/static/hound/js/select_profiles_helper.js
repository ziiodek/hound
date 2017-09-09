function load_profiles(assigned_id,economic_no){
if (assigned_id != "0"){
 var driver = document.getElementById('id_assigned_id');
 driver.value = assigned_id;
 }

 if (economic_no != "0"){
 var vehicle = document.getElementById('id_vehicle_no');
 vehicle.value = economic_no;
 }
}







