  function select_profiles(){

        var driver = document.getElementById('id_assigned_id');
        var vehicle =  document.getElementById('id_vehicle_no');
        var trip_id = document.getElementById('trip_id').value;
         var lenguage = document.getElementById('lenguage').value;
        if (vehicle.value== ''){
            vehicle.value = '0';
        }

        if (driver.value== ''){
            driver.value = '0';
        }

        if (parseInt(driver.value) > 0 || parseInt(vehicle.value) > 0){
             document.location.href='/edit_trip/'+lenguage+'/'+trip_id+'/'+driver.value+'/'+vehicle.value+'/';
        }




    }






