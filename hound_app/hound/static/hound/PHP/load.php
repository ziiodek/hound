<?php
$server = "localhost";
$user = "root";
$password = "";
$database = "hound";


function load_profile($user_id,$assigned_id){
	global $server,$user,$password,$database;
	$con = new mysqli($server,$user,$password,$database);
	$profile="";
	if ($con->connect_errno){
		echo $con->connect_error;
	}	

	$query = "select profile from profile_images where user_id='$user_id' and assigned_id=$assigned_id";
	if($result = $con->query($query)){
		$row = $result->fetch_assoc();
		$profile=$row["profile"];
		$result->close();
	}
	$con->close();
	return $profile;
}


  
  
?>