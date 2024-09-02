<form method="Post">
<h3>Enter your mobile number: </h3>
<input type="text" name="number"><br><br>
<input type="submit" name="submit" value="Submit">
</form> 


<?php
session_start();

// Update the path below to your autoload.php,
// see https://getcomposer.org/doc/01-basic-usage.md
require_once "C:/Users/bhave/vendor/autoload.php";

use Twilio\Rest\Client;
if(isset($_POST["submit"]))
{
	if(isset($_POST["number"]))

	{
		$m_no=$_POST["number"];
		$_SESSION["m_no"]=$m_no;
	}
	$otp=rand(1000,10000);
	$_SESSION["otp"]=$otp;
	echo $otp;
	$msg='Your OTP is '.$otp." to verify your mobile number";

// Your Account SID and Auth Token from twilio.com/console


$account_sid = 'AC2a7133ca6310269e6a19b82f59be5111';
$auth_token = '2c9cb5f56a55d6b2aff49e1d4a9b8e64';

// In production, these should be environment variables. E.g.:
// $auth_token = '118a7e3a2f4b430586d6e3a592b86af8';

// A Twilio number you own with SMS capabilities
$twilio_number = "+12518423064";

$client = new Client($account_sid, $auth_token);
$client->messages->create(
    // Where to send a text message (your cell phone?)
    $_SESSION["m_no"],
    array(
        'from' => $twilio_number,
        'body' => $msg
    )
);
header("Location:sms.php");
}
?>