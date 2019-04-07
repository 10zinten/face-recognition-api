<!DOCTYPE html>
<html>
<head>
    <title>Login Check</title>
</head>
<body>
<?php

    $url="<url>/register";
    
    //Initialise the cURL var
    $ch = curl_init();
   
    //Get the response from cURL
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);

    //Set the Url
    curl_setopt($ch, CURLOPT_URL, $url);

    //Create a POST array with the file in it
    $postData = array(
	    'userid' => 'tenzin',
	    'image' => new CURLFile('./' . 'test.png', 'image/jpeg', 'image')
    );

    //set POST fields
    curl_setopt($ch, CURLOPT_POSTFIELDS, $postData);

    // Execute the request
    $response = curl_exec($ch);
    echo "<h3>API Response</h3>";
    echo "</p>".$response."</p>"; 

    // Decode the API response
    $result = json_decode($response);
    $userid = $result->userid;
    $status = $result->status;
    $type = $result->type;
    
    echo "<h3>Decoded API response (In php object)</h3>";
    echo "<p><b>Userid :</b> ".$userid."</p>";
    echo "<p><b>Request type :</b> ".$type."</p>";
    echo "<p><b>Status :</b> ".$status."</p>";

    curl_close($ch);

?>
</body>
</html>
