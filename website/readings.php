<?php
    // error_reporting(0);
    session_start();
?>

<!DOCTYPE html>
<html lang="it">
  <head>
    <link rel="stylesheet" href="css/readings.css">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">  <!-- link al Bootstrap API -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.7.1/chart.min.js"></script>  <!-- link al Chart.js API -->
    <meta charset="utf-8">
    <title>Air Quality Station</title>
  </head>
  <body>
    <div class="container-fluid text-center bg-1 jumbotron">
      <a href="index.php">
        <img id="logo" class="img-responsive" src="images/logo.svg"></img>
      </a>
      <h1 id="title">Air Quality Station</h1>
      <p id="subtitle">La centralina per il monitoraggio della qualità dell'aria di Vittorio Veneto</p>
	  </div>
    <?php
      require_once("readingClass.php");
      require_once("view_error.php");
      // avvio sessione per la gestione dell'ordine dei dati
      // controlla se REQUEST_METHOD è get

      // Genera un warning
      $undefinedVariable;

      if($_SERVER['REQUEST_METHOD'] === "GET") {
        // controlla la variabile order_by per l'ordine ascendente o discendente
        if(isset($_GET['order_by'])) {
          $orderBy = $_GET['order_by']; //$orderBy = $_GET['order_by'];
          //var_dump($orderBy);
          $_SESSION[$orderBy.'_desc'] = !$_SESSION[$orderBy.'_desc'];
        } else {
          $orderBy = "date_time";
        }
        // controlla la variabile n per sapere il numero di misurazioni
        if(isset($_GET['n'])) {
          $n = $_GET['n'];
        } else {
          $n = 10;  
        }
      } else {
        header('Location: error.php');
      }
      // crea la variabile per l'ordine per la query
      if ($_SESSION[$orderBy.'_desc']) {
        $desc = "DESC";
      } else {
        $desc = "ASC";
      }
      // controlla la variabile per le Misurazioni in un arco di tempo
      if(!empty($_GET['readings_from']) || !empty($_GET['readings_to'])) {
        // sostituisce le T dalle date con spazi

        if(empty($_GET['readings_from'])){
          $readings_from = "2000-01-01 13:00:00";
        }
        else{
          $read_from = $_GET['readings_from'];
          $readings_from = str_replace("T", " ", $read_from);
        }

        if(empty($_GET['readings_to'])) {  
          // mettere l ultima misurazione effettuata
          $last_date = Reading::readingIndex();
          $readings_to =$last_date->getDate(); 
        }
        else{
          //LA QUERY è FORMATTATA LO STESSO DOPO SU DATETIME 
          $read_to = $_GET['readings_to'];
          $readings_to = str_replace("T", " ",  $read_to);
        }
    
        // SQL query per la tabella per selezione le Misurazioni in un arco di tempo
        $querySQL = "SELECT * FROM readings WHERE date_time BETWEEN '$readings_from' AND '$readings_to' ORDER BY $orderBy $desc";
      } else {
        // SQL query per il grafico per ottenere le Misurazioni
        //TODO: si possono concatenare piò order by al posto di fare una subquery
        $querySQL = "SELECT * FROM (SELECT * FROM readings ORDER BY date_time) AS A ORDER BY $orderBy $desc";
      }
      // array con le Misurazioni
      $readings = Reading::readings($querySQL);
      //var_dump($querySQL);
      //die();
      // array con le Misurazioni medie per ogni giorno dell'ultimo mese
      $readingsForChart = Reading::readingsForChart();
    ?>
     <!-- div con un form per selezionare Misurazioni di una specifica data -->
    <div id='reading_datetime' class="container">
      <form method="GET" action="specific_reading.php">
        <label for='reading_datetime'>Cerca la rilevazione effettuata il:</label>
        <input type='datetime-local' id='reading_datetime' name='reading_datetime'>
        <input type='submit' value="Cerca">
      </form>
    </div>
    <!-- div con un form per selezionare Misurazioni in un arco di tempo -->
    <div id='readings_from' class="container">
      <form method="GET" action="readings.php">
        <label for='readings_from'>Cerca le rilevazioni dal:</label>
        <input type='datetime-local' id='readings_from' name='readings_from'>
        <label for='readings_to'>al:</label>
        <input type='datetime-local' id='readings_to' name='readings_to'>
        <input type='submit' value="Cerca">
      </form>
    </div>
    </br>
    <?php
      // controlla se le Misurazioni sono di un arco di tempo
      if(isset($_GET['readings_from'])){
        $formatted_readings_from = date('d-m-Y H:i', strtotime($readings_from));
        
        if(empty($_GET['readings_to'])) {  
          // mettere l ultima misurazione 
          $last_date = Reading::readingIndex();
          $formatted_readings_to = date('d-m-Y H:i', strtotime($last_date->getDate()));
        }
        else{
            //var_dump($readings_to);
            $formatted_readings_to = date('d-m-Y H:i', strtotime($readings_to));
            //var_dump($formatted_readings_to);
        }
        //01-01-1970 01:00 al 02-11-2023 09:39 --> cambiare formato data pk differisce
        echo '<div class="container"> <p>Rilevazioni dal ' . $formatted_readings_from . ' al ' . $formatted_readings_to . '</p> </div>';
      }
        
    ?>
    <!-- div con una tabella contente le Misurazioni-->
    <div class="container">
      <table class="table table-striped table-hover table-bordered table-responsive">
        <thead>
          <tr>
            <th id="btn_col"></th>
            <!-- se le Misurazioni sono relative ad un periodo, la richiesta di sort deve includere il periodo richiesto -->
            <th><a class="orderBy" href="readings.php?n=<?php echo $n . (isset($readings_from) ? "&readings_from=$readings_from&readings_to=$readings_to" : "") ?>&order_by=date_time">Data Ora</a></th>
            <th class="col">Qualità dell'aria</th>
            <th class="col"><a class="orderBy" href="readings.php?n=<?php echo $n . (isset($readings_from) ? "&readings_from=$readings_from&readings_to=$readings_to" : "") ?>&order_by=pm10">PM10 (<b>µg</b>/m<sup>3</sup>)</a></th>
            <th class="col"><a class="orderBy" href="readings.php?n=<?php echo $n . (isset($readings_from) ? "&readings_from=$readings_from&readings_to=$readings_to" : "") ?>&order_by=temperature">Temperatura (<b>°</b>C)</a></th>
            <th class="col"><a class="orderBy" href="readings.php?n=<?php echo $n . (isset($readings_from) ? "&readings_from=$readings_from&readings_to=$readings_to" : "") ?>&order_by=no2">NO<sub>2</sub> (Ω)</a></th>
            <th class="col"><a class="orderBy" href="readings.php?n=<?php echo $n . (isset($readings_from) ? "&readings_from=$readings_from&readings_to=$readings_to" : "") ?>&order_by=dBA"> dBA </a></th> 
            <th class="col"><a class="orderBy" href="readings.php?n=<?php echo $n . (isset($readings_from) ? "&readings_from=$readings_from&readings_to=$readings_to" : "") ?>&order_by=location"> Location </a></th> 
          </tr>
        </thead> 
        <tbody>
        <?php
        $more = true;
        
        for ($i = 0; $i < $n; $i++) { 
          if(isset($readings[$i])) {?>
            <tr>
            <td>
                <!-- link alla Misurazione specifica -->
                <a href="specific_reading.php?reading_datetime=<?php echo $readings[$i]->getDate()?>">
                    <button>Visualizza</button>
                </a>
                </td>
                <td><?php
                    // eliminazione secondi dalle date
                    $date = strval($readings[$i]->getDate());
                    //$day = date('Y-m-d H:i', strtotime($date));
                    $formatted_day = date('d-m-Y H:i', strtotime($date));
                    echo $formatted_day;
                ?></td>

                  <?php 
                    // estrazione valore PM2.5 e PM10
                    $pm25 = $readings[$i]->getPm25();
                    $pm10 = $readings[$i]->getPm10();
                    // calcolo AQI per PM2.5, PM10 e NO2
                    $aqi_pm25 = $pm25*100/25; // 25: valore limite per PM2.5
                    $aqi_pm10 = $pm10*100/50; // 50: valore limite per PM10
                    
                    $valore = max($aqi_pm10, $aqi_pm25);
                    if ($valore <= 30) {
                      $str_aqi = "ottimo";
                    } elseif ($valore <= 67) {
                        $str_aqi = "buono";
                    } elseif ($valore <= 99) {
                        $str_aqi = "discreto";
                    } elseif ($valore <= 150) {
                        $str_aqi = "scadente";
                    } else {
                        $str_aqi = "pessimo";
                    }
                  ?>

                  <td style="color: 
                  <?php 
                      switch ($str_aqi) {
                        case "ottimo":
                            echo "#1DADEA"; // blu chiaro
                            break;
                        case "buono":
                            echo "#46A64A"; // verde
                            break;
                        case "discreto":
                            echo "#D87C2E"; // arancione
                            break;
                        case "scadente":
                            echo "#D61E29"; // rosso
                            break;
                        default:
                            echo "#792978"; // viola
                            break;
                    }
                    ?>
                    "><?php echo $str_aqi?></td>
                    <td><?php echo $readings[$i]->getPm10()?></td>
                    <td><?php echo $readings[$i]->getTemperature()?></td>
                    <td><?php echo $readings[$i]->getNO2()?></td> 
                    <td><?php echo $readings[$i]->getDBA()?></td> 
                  </tr><?php
            } else {
              $more = false;
            }
        }
        ?>
      </tbody>
      </table>
      <div class="container" id="dload_btn">
          <form action="getPDF.php" method="get">
            <input type="hidden" name="readings_from" value="<?php echo htmlspecialchars($readings_from) ?>">
            <input type="hidden" name="readings_to" value="<?php echo htmlspecialchars($readings_to) ?>">
            <input type="hidden" name="order_by" value="<?php echo htmlspecialchars($orderBy)?>">
            <input type="hidden" name="desc" value="<?php echo htmlspecialchars($desc) ?>">
            <input type="hidden" name="mode" value="true">
            <button type="submit">Scarica tutti i dati</button>
          </form>
          <form action="getPDF.php" method="get">
            <input type="hidden" name="readings_from" value="<?php echo htmlspecialchars($readings_from) ?>">
            <input type="hidden" name="readings_to" value="<?php echo htmlspecialchars($readings_to) ?>">
            <input type="hidden" name="order_by" value="<?php echo htmlspecialchars($orderBy) ?>">
            <input type="hidden" name="desc" value="<?php echo htmlspecialchars($desc) ?>">
            <input type="hidden" name="n" value="<?php echo htmlspecialchars($n) ?>">
            <input type="hidden" name="mode" value="false">
            <button type="submit">Scarica i dati mostrati</button>
          </form>
      </div>

      <div class="container" id="footer">
        <?php
        // controlla se ci sono Misurazioni, altrimenti viene stampato un messaggio informativo
        if(empty($readings)) {
          echo "<div class='container'>Nessuna rilevazione trovata nell'intervallo specificato</div>";
        } else if(isset($readings[$n])) {
        ?>
        <div class="container text-right" id = "load_more">
          <?php
            // carica altre 10 Misurazioni, controllando se è incluso un periodo di tempo
            if(isset($readings_from)) {
              echo "<a href='readings.php?n=" . ($n + ($more ? 10 : 0)) . "&readings_from=$readings_from&readings_to=$readings_to'>Carica altre 10 rilevazioni</a>";
            } else {
              echo "<a href='readings.php?n=" . ($n + ($more ? 10 : 0)) . "'>Carica altre 10 rilevazioni</a>";
            }
          ?>
        </div>
      </div>
    <?php
    }

    if ($readingsForChart != null) { ?>
      <div class="container text-center">
        <canvas id="myChart"></canvas>
        <canvas id="myChart_no2"></canvas>
      </div> <?php
    }
    ?>
    <script>
      // opzioni Globali
      Chart.defaults.font.family = 'coves-light';
      Chart.defaults.font.size = 20;
      // etticchette del grafico
      const labels = [
        <?php
          for($i = $n - 1; $i >= 0; $i--) {
            if(isset($readingsForChart[$i])) {
              // eliminazione secondi dalle date
              $date = strval($readingsForChart[$i]->getDate());
              $year_month = date('Y/m', strtotime($date));
              $day_date = date('d/m', strtotime($date));
              // mese e giorno di ogni Misurazione
              echo "'" . $day_date . "',";
            }
          }
        ?>
      ];
      // dati del grafico
      // TODO aggiunta tick configuration
      const data = {
        labels: labels,
        datasets: [{
          label: 'PM10 (µg/m3)',
          data: [
            <?php
              for($i = $n - 1; $i >= 0; $i--) {
                if(isset($readingsForChart[$i])) {
                  // ottiene il valore del PM10 per ogni Misurazione
                  echo "'" . strval($readingsForChart[$i]->getPm10()) . "',";
                }
              }
            ?>
          ],
          borderColor: '#3355ff',
          backgroundColor: '#3355ff',
          hoverBorderWidth: 3,
          hoverBorderColor: '#000000',
          tension: 0.3
        },
        {
          label: 'Temperatura (°C)',
          data: [
            <?php
              for($i = $n - 1; $i >= 0; $i--) {
                if(isset($readingsForChart[$i])) {
                  // ottiene il valore della Temperature per ogni Misurazione
                  echo "'" . strval($readingsForChart[$i]->getTemperature()) . "',";
                }
              }
            ?>
          ],
          borderColor: '#ff2929',
          backgroundColor: '#ff2929',
          hoverBorderWidth: 3,
          hoverBorderColor: '#000000',
          tension: 0.3
        }]
      };

      // dati del grafico per NO2
      const data_no2 = {
        labels: labels,
        datasets: [{
          label: 'NO2 (Ω)',
          data: [
            <?php
              for($i = $n - 1; $i >= 0; $i--) {
                if(isset($readingsForChart[$i])) {
                  // ottiene il valore dell'NO2 per ogni Misurazione
                  echo "'" . strval($readingsForChart[$i]->getNo2()) . "',";
                }
              }
            ?>
          ],
          borderColor: '#039e00',
          backgroundColor: '#039e00',
          hoverBorderWidth: 3,
          hoverBorderColor: '#000000',
          tension: 0.3
        }]
      }
      
      // configurazione del grafico
      const config = {
        type: 'line',
        data: data,
        options: {
          plugins: {
            title: {
              display: true,
              text: <?php echo '"Andamento PM10 e Temperatura del ' . $year_month . '"'; ?>,
              color: "#1abc9c",
              font: {
                size: 30,
                weight: 'bold',
                lineHeight: 1.2
              }
            }
          }
        }
      };

      // configurazione del grafico per NO2
      const config_no2 = {
        type: 'line',
        data: data_no2,
        options: {
          plugins: {
            title: {
              display: true,
              text: <?php echo '"Andamento NO2 del ' . $year_month . '"'; ?>,
              color: "#1abc9c",
              font: {
                size: 30,
                weight: 'bold',
                lineHeight: 1.2
              }
            }
          }
        }
      };

      // ottiene lo spazio per il grafico
      let chart = document.getElementById('myChart').getContext('2d');

      // disegna il grafico
      let myChart = new Chart(
        chart,
        config
      );

      // ottiene lo spazio per il grafico per l'NO2
      let chart_no2 = document.getElementById('myChart_no2').getContext('2d');

      // disegna il grafico per l'NO2
      let myChart_no2 = new Chart(
        chart_no2,
        config_no2
      );
    </script>
  </body>
</html>

