function toggle(source,lenguage,assigned_id) {
    checkboxes = document.getElementsByName('select');
    if (source.checked == true){
    for(var i in checkboxes){
        checkboxes[i].checked = false;
        }
   source.checked = true;
   document.location.href="/vacations_dates/"+lenguage+"/"+assigned_id+"/"+source.value+"/";
        }
}






