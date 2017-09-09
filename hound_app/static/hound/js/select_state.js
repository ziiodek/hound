 function display_states(){

        var element = document.getElementById("id_country_select");
        var value = element.options[element.selectedIndex].text;


        if(value == "USA"){
            document.getElementById("usa").style.display="block";
             document.getElementById("mx").style.display="none";

        }else if(value == "MX"){

             document.getElementById("mx").style.display="block";
              document.getElementById("usa").style.display="none";
        }else{

             document.getElementById("mx").style.display="none";
              document.getElementById("usa").style.display="none";
        }
    }




