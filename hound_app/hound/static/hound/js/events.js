function hide_element(element_id){
var element = document.getElementById(element_id);
var status = element.style.display;
var button = document.getElementById("link");
if(status == "none"){
element.style.display="block";
button.innerHTML = "RFC/CURP";
	
}else{
	element.style.display="none";	
	button.innerHTML = "ID";
}
}





