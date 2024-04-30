<?php
    function connOpen(){

        // Read the JSON file content
        $jsonData = file_get_contents('../../conn/connection_data.json');

        // Decode the JSON data into an associative array
        $dataArray = json_decode($jsonData, true);

        // Check if decoding was successful
        if ($dataArray === null) {
            echo "Error decoding JSON";
        } else {
            // Access the extracted data
            $user = $dataArray['user'];
            $password = $dataArray['password'];
            $host = $dataArray['host'];
            $database = $dataArray['database'];
        }

        $connection = new mysqli($host, $user, $password);
        $connection->select_db($database);
        return $connection;
    };

    function connClose($connection){
        $connection->close();
    }
?>