  function select_profiles(){
        var lenguage = document.getElementById('lenguage').value;
        var driver = document.getElementById('id_assigned_id');
        var vehicle =  document.getElementById('id_vehicle_no');
        if (vehicle.value== ''){
            vehicle.value = '0';
        }

        if (driver.value== ''){
            driver.value = '0';
        }

        if (parseInt(driver.value) > 0 || parseInt(vehicle.value) > 0){
             document.location.href='/assign_trip/'+lenguage+'/'+driver.value+'/'+vehicle.value+'/';
        }




    }






