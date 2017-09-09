function onload_select(vacation_id){
 checkboxes = document.getElementsByName('select');
   for(var i in checkboxes){
    if(checkboxes[i].value == vacation_id){
        checkboxes[i].checked = true;
        }
        }
}





