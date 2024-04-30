<?php
require("readingClass.php");
require_once("view_error.php");

if ($_SERVER["REQUEST_METHOD"] === "GET" && isset($_GET['mode'])) {
    require_once("connection.php");
    $connection = connOpen();
    
    if ($_GET['mode'] === 'true') {
        // Scarica tutti i dati
        $query = "SELECT * FROM readings WHERE date_time BETWEEN ? AND ? ORDER BY " . $_GET['order_by'] . " " . $_GET['desc'];
    } else {
        // Scarica solo i visualizzati
        $query = "SELECT * FROM readings WHERE date_time BETWEEN ? AND ? ORDER BY " . $_GET['order_by'];
        if (!empty($_GET['desc'])) {
            $query .= " " . $_GET['desc'];
        }
        $query .= " LIMIT ?";
    }
    $stmt = mysqli_prepare($connection, $query);

    if ($stmt === false) {
        die('Errore nella preparazione della query: ' . mysqli_error($connection));
    }

    // Associare i parametri alla query
    if ($_GET['mode'] === 'true') {
        $stmt->bind_param("ss", $_GET['readings_from'], $_GET['readings_to']);
    } else {
        $stmt->bind_param("sss", $_GET['readings_from'], $_GET['readings_to'], $_GET['n']);
    }
    
    // Eseguire la query
    $stmt->execute();

    // Ottenere i risultati
    $result = $stmt->get_result();
}   

if ($_GET["mode"] == "true") {
    $mode = true;
} else {
    $mode = false;
}

Reading::getPDF($result, $mode);

connClose($connection);
?>
