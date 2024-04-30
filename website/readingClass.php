<?php

    class Reading {
        private  $date;
        private  $temperature;
        // nullable (?) perchè le variabili non sempre necessarie 
        private $pm25; 
        private $pm1;
        private $humidity;
        private $air_pressure;
        private $co;
        private $nh3;
        private $pm10;
        private $no2;
        private $dBA;
        private $id_location;

            //viene usata su readings()
        public function __construct($date, $temperature,  $pm10,  $no2,  $pm25,  $pm1,  $humidity, $air_pressure, $co, $nh3, $dBA, $id_location) {
            $this->date = $date;
            $this->temperature = $temperature;
            $this->pm10 = $pm10;
            $this->no2 = $no2;
            $this->pm25 = $pm25;
            $this->pm1 = $pm1;
            $this->humidity = $humidity;
            $this->air_pressure = $air_pressure;
            $this->co = $co;
            $this->nh3 = $nh3;
            $this->dBA = $dBA;
            $this->id_location = $id_location;
        }

        // ritorno l'ultima Misurazione effettuata 
        public static function readingIndex(){
            require_once("connection.php");
            $connection = connOpen();

            $querySQL = "SELECT * FROM readings WHERE date_time=(SELECT max(date_time) FROM readings)";
            $result = $connection->query($querySQL);
            $aux = $result->fetch_assoc();
            $reading = new Reading($aux["date_time"], $aux["temperature"], $aux["pm10"], $aux["no2"], $aux["pm25"], $aux["pm1"], $aux["humidity"], $aux["air_pressure"], $aux["co"], $aux["nh3"], $aux["dBA"], $aux["id_location"]);
            
            connClose($connection);
            return $reading;
        }
        
        // ritorna la Misurazione specificata da giorno e ora
        public static function readingFromSpecificDay($date){
            require_once("connection.php");
            $connection = connOpen();
            // SQL query per ottenere una Misurazione specifica
            $querySQL = "SELECT * FROM readings WHERE date_time LIKE '" . $date . "%'";
            $result = $connection->query($querySQL);
            $aux = $result->fetch_assoc();
            if($aux == null){return null;}
            $reading = new Reading($aux["date_time"], $aux["temperature"], $aux["pm10"], $aux["no2"], $aux["pm25"], $aux["pm1"], $aux["humidity"], $aux["air_pressure"], $aux["co"], $aux["nh3"], $aux["dBA"],  $aux["id_location"]);
            
            connClose($connection);

            return $reading;
        }

        // ritorna un array con le Misurazioni effettuate in una giornata specifica
        public static function readingFromDays($day){
            require_once("connection.php");
            $connection = connOpen();
            // SQL query per ottenere le Misurazioni di un giorno specifico
            $querySQL = "SELECT * FROM readings WHERE date_time LIKE '" . $day . "%'";
            $result = $connection->query($querySQL);
            $reading_list = [];
            while ($reading = $result->fetch_assoc()) {
                $reading_list[] = new Reading($reading["date_time"], $reading["temperature"], $reading["pm10"], $reading["no2"], $reading["pm25"], $reading["pm1"], $reading["humidity"], $reading["air_pressure"], $reading["co"], $reading["nh3"], $reading["dBA"], $reading["id_location"]);
            }

            connClose($connection);

            return $reading_list;
        }

        // ritorna un array con tutte le Misurazioni
        public static function readings ($query){
            require_once("connection.php");
            $connection = connOpen();
            $result = $connection->query($query);
            $readings = array();
            while ($aux = $result->fetch_assoc()) {
                $readings[] = new Reading($aux["date_time"], $aux["temperature"], $aux["pm10"], $aux["no2"], $aux["pm25"], null, null, null, null, null, $aux["dBA"], $aux["id_location"]);
            }

            connClose($connection);

            return $readings;
        }


        /* public static function readingsForChart (String $query) : array {
            $connection = new mysqli("194.5.156.94", "u487620786_aqs", "cbITT143+");
            $connection -> select_db("u487620786_aqs");
            $result = $connection->query($query);
            $readings = array();
            while ($aux = $result->fetch_assoc()) {
                $readings[] = new Reading($aux["date_time"], $aux["temperature"], $aux["pm10"], $aux["no2"], null, null, null, null, null, null);
            }
            return $readings;
        } */

        // ritorna un array con le Misurazioni medie per ogni giorno dell'ultimo mese
        public static function readingsForChart() {
            require_once("connection.php");
            $connection = connOpen();
            // SQL query per ottenere l'ultima Misurazione effettuata
            $query1 = "SELECT * FROM readings ORDER BY date_time DESC";
            $aux_mese = $connection -> query($query1) -> fetch_assoc();
            $last_reading = new Reading($aux_mese["date_time"], $aux_mese["temperature"], $aux_mese["pm10"], $aux_mese["no2"], null, null, null, null, null, null, null, null);
            $date = $last_reading->getDate();
            $year = date('Y', strtotime($date));
            $month = date('m', strtotime($date));
            // SQL query per ottenere la temperatura media, il PM10 medio e l'NO2 medio di ogni giorno in un mese
            $query2 = "SELECT DATE(date_time) as dt, avg(temperature) as avg_temp, avg(pm10) as avg_pm10, avg(no2) as avg_no2 FROM readings WHERE date_time LIKE '" . $year . "-" . $month . "%' GROUP BY DATE(date_time) ORDER BY dt DESC";
            $result = $connection -> query($query2);
            $readings_current_month = [];
            while ($aux = $result -> fetch_assoc()) {
                $readings_current_month[] = new Reading($aux["dt"], intval($aux["avg_temp"]), intval($aux["avg_pm10"]), intval($aux["avg_no2"]), null, null, null, null, null, null, null, null);
            }
            // se sono presenti due Misurazioni medie, viene restituito l'array contenente le Misurazioni stesse
            if (isset($readings_current_month[1])) {
                $final_readings = $readings_current_month;
            } else {
                $month = intval($month) - 1;
                $month = strval($month);
                $query2 = "SELECT DATE(date_time) as date_time, avg(temperature) as avg_temp, avg(pm10) as avg_pm10, avg(no2) as avg_no2 FROM readings WHERE date_time LIKE '" . $year . "-" . $month . "%' GROUP BY DATE(date_time) ORDER BY date_time DESC";
                $result = $connection -> query($query2);
                $readings = null;
                while ($aux = $result -> fetch_assoc()) {
                    $readings[] = new Reading($aux["date_time"], intval($aux["avg_temp"]), intval($aux["avg_pm10"]), intval($aux["avg_no2"]), null, null, null, null, null, null, null, null);
                }
                $final_readings = $readings;
            }

            connClose($connection);

            return $final_readings;
        }

        public static function getCSV($query, $fname, $n_readings){
            require_once("connection.php");
            $connection = connOpen();

            $res = $connection->query($query);
            $readings = array();
            while($reading = $res->fetch_assoc()){
                $readings[] = $reading; 
            }
            array_unshift($readings, array_keys($readings[0]));
            $file = fopen($fname, "w");
            if($n_readings){
                for($i = 0; $i < $n_readings; $i++){
                    fputcsv($file, $readings[$i], ",");
                }
            }else{
                foreach($readings as $reading){
                    fputcsv($file, $reading, ",");                 
                }
            }
            
            fclose($file);
            connClose($connection);
            return $fname;
        }

        public static function getPDF ( $result, $mode)  {
            require_once("connection.php");
            require "./pdf/pdf.php";
            //$connection = connOpen();

            $res = $result;
            $readings = array();
            while($aux = $res->fetch_assoc()){
                $readings[] = new Reading($aux["date_time"], $aux["temperature"], $aux["pm10"], $aux["no2"], $aux["pm25"], $aux["pm1"], $aux["humidity"], $aux["air_pressure"], $aux["co"], $aux["nh3"], $aux["dBA"], $aux["id_location"]);
            }
            
            $pdf = new PDF();
            // Column headings
            $header = array('Data misurazione', 'Temperatura', 'PM2.5', 'PM1', 'PM10', 'NO2','Umidita','Pressione','CO','NH3','dBA');
            $pdf->AddPage('L', 'A4');
            $pdf->FancyTable($header, $readings);
            //true => scarica tutti i dati, false => scarica i dati mostrati
            if($mode){
                $pdf->Output('D', 'letture.pdf', true);
            }else{
                $pdf->Output('D', 'letture_mostrate.pdf', true);
            }

            //connClose($connection);
        }

        public function getDate() {
            return $this->date;
        }

        public function getPm10() {
            return $this->pm10;
        }

        public function getTemperature() {
            return $this->temperature;
        }

        public function getNO2()            
        {
            return $this->no2;
        }

        public function getPm25() {
            return $this->pm25;
        }

        public function getCo() {
            return $this->co;
        }

        public function getNh3() {
            return $this->nh3;
        }

        public function getPm1() {
            return $this->pm1;
        }

        public function getAirPressure() {
            return $this->air_pressure;
        }

        public function getHumidity() {
            return $this->humidity;
        }

        public function getDBA(){
            return $this->dBA;
        }

        public function setQueryPDF(){
            $this->$query_pdf;
        }

    }

?>