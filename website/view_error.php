<?php
// Disabilita la visualizzazione degli errori

ini_set('display_errors', 0);  //disabilita visualizzazione gli errori direttamente nella pagina web visualizzata dal browser. 

/* // Registra i potenziali errori in un file di log
ini_set('log_errors', E_ERROR);
ini_set('error_log', './view_error/error_log.txt');

// Registra i warning su un file di log separato
ini_set('error_reporting', E_WARNING);
ini_set('error_log', './view_error/warning_log.txt');

// Registra i notice su un file di log separato
ini_set('error_reporting', E_NOTICE);
ini_set('error_log', './view_error/notice_log.txt'); */

// Abilita la registrazione degli errori, dei warning e dei notice su file di log separati
ini_set('log_errors', 1);

// Registra gli errori su file error_log.txt
ini_set('error_log', './view_error/error_log.txt');
error_reporting(E_ERROR);

// Registra i warning su file warning_log.txt
ini_set('error_log', './view_error/warning_log.txt');
error_reporting(E_WARNING);

// Registra i notice su file notice_log.txt
ini_set('error_log', './view_error/notice_log.txt');
error_reporting(E_NOTICE);

// Abilita la registrazione degli errori su file di log separati
ini_set('log_errors', 1);


/* error_reporting(E_ALL);
ini_set('display_errors', 1);

// Test per vedere se gli errori vengono registrati nel file di log
error_log("Test log message", 3, "./error_log.txt"); */
?>