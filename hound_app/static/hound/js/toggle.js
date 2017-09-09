function toggle(source) {
    checkboxes = document.getElementsByName('select');
    for(var i in checkboxes)
        checkboxes[i].checked = source.checked;
}






