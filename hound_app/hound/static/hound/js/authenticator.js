function compare_passwords(){
	 var password1 = document.getElementById('password');
	 var password2 = document.getElementById('password2');
	
	  if(password1.value != '' && password2.value!= ''){	
			 
		if(password1.value != password2.value){
			alert("The retyped password must be the same");
			window.location = "http://127.0.0.1:8000/registration/";
		}	
	  }
	
}

