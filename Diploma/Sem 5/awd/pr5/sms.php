<form action="" method="POST">
<h3> Enter OTP</h3>
<input type="text" name="otp"><br><br>
<input type="submit" name="submit" value="Submit">
</form>
<?php
session_start();
if(isset($_POST["submit"]))
{
	$sotp=$_SESSION["otp"];
	$fotp=$_POST["otp"];
	if($sotp==$fotp)
	{
		echo "OTP verified";
	}
	else
	{
		echo "Invalid OTP";
	}
}
?>