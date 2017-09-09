<?php
include 'commit.php';
$user_id = $_POST['user_id'];
$assigned_id = $_POST['assigned_id'];
$type=$_GET['type'];
$state=$_GET['state'];
$dir = "";
mkdir ("tmp".$user_id,0700);

if(!file_exists($user_id)){
	mkdir($user_id,0700);
	mkdir($user_id."/drivers/",0700);
	mkdir($user_id."/drivers/profile/",0700);
	mkdir($user_id."/drivers/prints",0700);
}

echo $type;

if($type == 0){
	$dir = $user_id."/drivers/profile"; 

}else if($type  == 1){
	$dir = $user_id."/drivers/prints"; 

}else{
	exit();
	
}
echo $dir."/".$assigned_id;
if(!file_exists($dir."/".$assigned_id)){
	mkdir ($dir."/".$assigned_id,0700);
}
$dir = $dir."/".$assigned_id."/";

$files = glob($dir.'*');
foreach($files as $file){ // iterate files
  if(is_file($file))
    unlink($file); // delete file
}

if(isset($_FILES['img'])){
      $errors= array();
      $file_name = $_FILES['img']['name'];
      $file_size = $_FILES['img']['size'];
      $file_tmp = $_FILES['img']['tmp_name'];
      $file_type = $_FILES['img']['type'];
      $file_ext=strtolower(end(explode('.',$_FILES['img']['name'])));
      
      $expensions= array("jpeg","jpg","png");
      
      if(in_array($file_ext,$expensions)=== false){
         $errors[]="extension not allowed, please choose a JPEG or PNG file.";
      }
      
      if($file_size > 2097152) {
         $errors[]='File size must be excately 2 MB';
      }
     
      if(empty($errors)==true) {
         move_uploaded_file($file_tmp,"tmp".$user_id."/".$file_name);
		 rename("tmp".$user_id."/".$file_name, $dir.$file_name);
		 rmdir ("tmp".$user_id);
		 if($type == 0){
		 save_profile($user_id,$assigned_id, "hound/PHP/".$dir.$file_name,$state);
		 }else if($type == 1){
			 save_prints($user_id,$assigned_id, "hound/PHP/".$dir.$file_name,$state);
		 }
         //echo "Success";
		 if($state == 0){
		 header('Location:http://127.0.0.1:8000/add_driver/');
		 }else if($state==1){
			  header('Location:http://127.0.0.1:8000/edit_driver/'.$assigned_id.'/');
			 
		 }
      }else{
         print_r($errors);
      }
   }
      
?>