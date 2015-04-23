<?php
if(isset($_FILES['uploadedimg']['name'])){
$target_path = "uploads/img/";


$target_path = $target_path . basename( $_FILES['uploadedimg']['name']); 

if(move_uploaded_file($_FILES['uploadedimg']['tmp_name'], $target_path)) {
    $msg_img =  "<td><br><br>ไฟล์ ".  basename( $_FILES['uploadedimg']['name']). 
    "COMPLETE</td>";
	$check_img = true ;
} else{
    $msg_img = "<td><br><br> UNCOMPLETE</td>";
	$check_img =false ;
}

//$mas = shell_exec (////test.py);
//$mas = $target_path;
//echo "<img src=\"$mas\" height=\"400\" width=\"400\"></img>"
}
else{
	$target_path = "media/choose.jpg";
	
}

?>



<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"><head>

<meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="SHORTCUT ICON" href="icon.jpg" />
	<link rel="icon" href="icon.jpg" type="image/ico" />
    <link href="css/bootstrap.min.css" rel="stylesheet">
     <link href="css/dashboard.css" rel="stylesheet">


	<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
	<script src="my_jquery_functions.js"></script>
	<script src="js/bootstrap.min.js"></script>

<meta http-equiv="Content-Script-Type" content="text/javascript" />
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8;charset=utf-8" />
<meta name="robots" content="index, follow" />
<meta name="keywords" content="" />
<meta name="title" content="" />
<meta name="description" content="" />
<title>DETECT IMAGE</title>
<link href="media/style000.css" rel="stylesheet" type="text/css" />
<link href="media/inner000.css" rel="stylesheet" type="text/css" />

<script type="text/javascript" src="media/jquery-1.js"></script>
<script type="text/javascript" src="media/cufon-yu.js"></script>
<script type="text/javascript" src="media/Cicle_Se.js"></script>
<script type="text/javascript">
Cufon.replace('h1') ('h1 a') ('h2') ('h3') ('h4') ('h5') ('h6') ('.middle-text p');
</script>
<script type="text/javascript" src="media/jquery00.js"></script>
<script type="text/javascript" src="media/contact0.js"></script>


</head>


<body>


	<form enctype="multipart/form-data" action="algae.php" method="POST">

	<div id="top_container">
		
	<div id="title-desc-inner">
	<div id="title-desc-inner-centercolumn">
		<div id="title-desc-left">
			<h1>CS402 : The Classification of Algae Using Image Recognition on Private Cloud</h1>
			<br></br>
		</div>
	</div>
	</div>
		<div class="centercolumn">
			<div id="maincontent ">
				<h3 style="color:#333333; padding-left: 2em">DETECT ALGAE</h3>
				<div id="">
					<p style="padding-left: 5em"> การทำงาน : ระบบจะรับภาพที่ท่านเลือกเพื่อนำไปเปรียบเทียบกับตัวจำแนกในขั้นตอนการเรียนรู้ของเครื่อง เพื่อระบุคำอธิบาย (label) และแสดงผลระบุว่าตำแหน่งไหนในภาพที่เป็นสาหร่ายประเภทอะไร</p>

			
					
					
					
					<?php if($target_path == "media/choose.jpg"){
						
						echo "
					<img src=\"$target_path\" class=\"alignleft\" style=\"width:400px; height:300px\" />
					
					
					
					</br><input name=\"uploadedimg\" type=\"file\" />
			<br>
			<button type=\"submit\" id=\"myButton\" data-loading-text=\"Loading...\" class=\"btn btn-primary\" autocomplete=\"off\">Upload</button></br>
			<div id=\"loading\"></div>
				";}
				else{
					echo "<div class=\"row\">
					<div class=\"col-md-6 \"> <img src=\"$target_path\"  style=\"width:400px; height:300px \" /></br></div>
					<div class=\"col-md-6 \"> <img src=\"$target_path\"  style=\"width:400px; height:300px \" /></br></div></div>";
					
					echo "</br><div class=\"row\"> <div class=\"col-md-6 col-md-offset-5\">";
					print $_FILES['uploadedimg']['name']."</br>";
					$text = file('uploads/detail.txt');
					foreach($text as $value){
						print $value.'<br/>';
					}
					echo "</div>";
				}
					
					?>
					
					
				</div>	
			</div>	
			
		</div>
	</div>
	
	

			
<script>
  $('#myButton').on('click', function () {
    var $btn = $(this).button('loading')
    // business logic...
    $btn.button('reset')
	
	// add loading image to div
    $('#loading').html('<img src="loading.jpg"> loading...');
    
    // run ajax request
    $.ajax({
        type: "GET",
        dataType: "json",
        url: "",
        success: function (d) {
            // replace div's content with returned data
            $('#loading').html(d);
        }
    });
	
  });
</script>

 
<script type="text/javascript">
    	$(document).ready(function() {
 			$('[data-toggle=offcanvas]').click(function() {
    		$('.row-offcanvas').toggleClass('active');
  		});});
 </script>

  </form>


</body>

<!--
<div style="text-align: center;">Copyright &copy; 2015. cs402_project. All rights reserved.</div>
-->

</html>
