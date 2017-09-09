<?php
$server = "localhost";
$user = "root";
$password = "";
$database = "hound_db";


function save_profile($user_id,$assigned_id,$file,$state){
	global $server,$user,$password,$database;
	$con = new mysqli($server,$user,$password,$database);
	if ($con->connect_errno){
		echo $con->connect_error;
	}	
		$query = "update tmp_profile_images set profile='$file' where user_id='$user_id' and assigned_id=$assigned_id";
		
	$result = $con->query($query);
		
	$con->close();
}

function save_prints($user_id,$assigned_id,$file,$state){
	global $server,$user,$password,$database;
	$con = new mysqli($server,$user,$password,$database);
	if ($con->connect_errno){
		echo $con->connect_error;
	}	
	
		$query = "update tmp_prints_images set prints='$file' where user_id='$user_id' and assigned_id=$assigned_id";
			
	$result = $con->query($query);
		
	$con->close();
}


  
?>