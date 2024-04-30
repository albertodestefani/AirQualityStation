<!DOCTYPE html>
<html lang="it">
  <head>
    <link rel="stylesheet" href="css/specific_reading.css">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css"> <!-- link al Bootstrap API -->
    <script src="https://cdn.jsdelivr.net/npm/apexcharts"></script> <!-- link a ApexChart API -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.7.1/chart.min.js"></script>  <!-- link a Chart.js API -->
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
    
    <div class="container">
      <div class="container">
        <h1>Specifica rilevazione</h1>
      </div>

      <?php
        include("readingClass.php");
        //si puo cambiare mettendo solo un !empty
        if (isset($_GET['reading_datetime']) and $_GET['reading_datetime'] != "") {
          // sostituisce le T dalle date con uno spazio
          $reading_datetime = $_GET['reading_datetime'];
          $date = str_replace("T", " ", $reading_datetime);
          // separa [giorno-mese-anno][ore][minuti]
          $day = date('Y-m-d', strtotime($date));
          $formatted_day = date('d-m-Y', strtotime($date));
          $hours_minutes = date('H:i', strtotime($date));
          $hours_minutes_seconds = date('H:i:s', strtotime($date));
          // Misurazione di un giorno e ora specifico
          $specific_reading = Reading::readingFromSpecificDay($date);
          // array con tutte le Misurazioni di un giorno specifico
          $daily_readings = Reading::readingFromDays($day);
        }else{
          echo "<h2>ERRORE :( : nessuna data selezionata</h2>";
        }
        // stampa le informazioni di AQI e data
        if ($specific_reading != null) {
          // ottiene i valori del PM2.5 e PM10
          $pm25 = $specific_reading->getPm25();
          $pm10 = $specific_reading->getPm10();
          // calcolo il valore AQI per PM2.5 e PM10
          $aqi_pm25 = $pm25*100/25; // 25: valore limite per PM2.5
          $aqi_pm10 = $pm10*100/50; // 50: valore limite per PM10

          $dBA = $specific_reading -> getDBA();
          // calcolo del AQI per PM2.5 e per PM10
          $dBA = intval($dBA*100/120); // converte il valore del dBA in centesimi

          // sceglie il valore peggiore
          if ($aqi_pm10 > $aqi_pm25) {
            if ($aqi_pm10 < 50) {
              $str_aqi = "Buona"; // concentrazione sotto la metà del valore limite
            } else if ($aqi_pm10 < 100) {
              $str_aqi = "Discreta"; // concentrazione fino al valore limite
            } else if ($aqi_pm10 < 150) {
              $str_aqi = "Mediocre"; // concentrazione fino al valore limite e mezzo
            } else if ($aqi_pm10 < 200) {
              $str_aqi = "Scadente"; // concentrazione fino al doppio del valore limite
            } else {
              $str_aqi = "Pessima"; // concentrazione oltre al doppio del valore limite
            }
          } else {
            if ($aqi_pm25 < 50) {
              $str_aqi = "Buona"; // concentrazione sotto alla metà del valore limite
            } else if ($aqi_pm25 < 100) {
              $str_aqi = "Discreta"; // concentrazione fino al valore limite
            } else if ($aqi_pm25 < 150) {
              $str_aqi = "Mediocre"; // concentrazione fino al valore limite e mezzo
            } else if ($aqi_pm25 < 200) {
              $str_aqi = "Scadente"; // concentrazione fino al doppio del valore limite
            } else {
              $str_aqi = "Pessima"; // concentrazione oltre al doppio del valore limite
            }
          }
        echo "<div class='container'><p>Data Ora: " . $formatted_day . " " . $hours_minutes . "</p></div><div class='container'><p> Qualità dell'aria: $str_aqi</p></div>";
      ?>
      </div>

      <div id="chart" class="container">
        <!-- Grafico a cerchio con ApexChart API dell' AQI-->
        <div class = "radialBar" id="radialBarAQI"></div>
        <!-- Grafico a cerchio con ApexChart API del dBA-->
        <div class = "radialBar" id="radialBarDBA"></div>
      </div>

      <script>
        var options = {
        chart: {
          height: 220,
          type: "radialBar"
        },
        colors: [function({value}) {
            if (value < 20) {
              return '#1DADEA' // blu chiaro
            } else if (value < 40) {
              return '#46A64A' // verde
            } else if (value < 60) {
              return '#D87C2E' // arancione
            } else if (value < 80) {
              return '#D61E29' // rosso
            } else {
              return '#792978' // viola
            }
        }],
        
        series: [<?php if($aqi_pm10>$aqi_pm25) {echo $aqi_pm10*2/5;} else {echo $aqi_pm25*2/5;}?>],

          plotOptions: {
            radialBar: {
              hollow: {
                margin: 15,
                size: "70%"
              },
              
              dataLabels: {
                showOn: "always",
                name: {
                  offsetY: -10,
                  show: true,
                  color: "#888",
                  fontSize: "25px"
                },
                value: {
                  color: "#111",
                  fontSize: "30px",
                  fontFamily: "coves-light",
                  show: true,
                  formatter: function (val) { return val }
                }
              }
            }
          },
          stroke: {
            lineCap: "round",
          },
          labels: ["AQI"]
        };
        var aqi_chart = new ApexCharts(document.querySelector("#radialBarAQI"), options);
        aqi_chart.render();

        var options1 = {
        chart: {
          height: 220,
          type: "radialBar"
        },
        colors: [function({value}) {
            if (value < 33) {
              return '#1DADEA' // blu chiaro
            } else if (value < 50) {
              return '#46A64A' // verde
            } else if (value < 67) {
              return '#F0A010' // arancione
            } else if (value < 91) {
              return '#D61E29' // rosso
            } else {
              return '#792978' // viola
            }
            /* conversione dBA
              100 : 120 = valore : limiteValore 
            
              0-40 -> 0-33  blu
              40-60 -> 33-50  verde
              60-80 -> 50-67  giallo/arancione
              80-110 -> 67-91 rosso
              110-120 -> 91 > viola
            */
        }],
        
        series: [<?php echo $dBA?>],

          plotOptions: {
            radialBar: {
              hollow: {
                margin: 15,
                size: "70%"
              },
              
              dataLabels: {
                showOn: "always",
                name: {
                  offsetY: -10,
                  show: true,
                  color: "#888",
                  fontSize: "25px"
                },
                value: {
                  color: "#111",
                  fontSize: "30px",
                  fontFamily: "coves-light",
                  show: true,
                  formatter: function () { return <?php echo $specific_reading -> getDBA() ?> }
                }
              }
            }
          },
          stroke: {
            lineCap: "round",
          },
          labels: ["dBA"]
        };
        var dba_chart = new ApexCharts(document.querySelector("#radialBarDBA"), options1);
        dba_chart.render();
      </script>
    </div>
    <!-- div con una tabella contenente una Misurazione specifica -->
    <div class="container">
      <table class="table table-striped table-hover table-bordered table-responsive">
        <?php
          echo "\t<tr><th>PM1 (<b>µg</b>/m<sup>3</sup>)</th><th>PM2.5 (<b>µg</b>/m<sup>3</sup>)</th><th>PM10 (<b>µg</b>/m<sup>3</sup>)</th><th>Location</th></tr>\n\t\t";
          echo "<tr><td>" . $specific_reading->getPm1() . "</td><td>" . $specific_reading->getPm25() . "</td><td>" . $specific_reading->getPm10() . "</td></tr>\n\t\t";
          echo "<tr><th>Temperatura (<b>°</b>C)</th><th>Umidità (%)</th><th>Pressione atmosferica (Pa)</th></tr>\n\t\t";
          echo "<tr><td>" . $specific_reading->getTemperature() . "</td><td>" . $specific_reading->getHumidity() . "</td><td>" . $specific_reading->getAirPressure() . "</td></tr>\n\t\t";
          echo "<tr><th>CO (Ω)</th><th>NO<sub>2</sub> (Ω)</th><th>NH<sub>3</sub> (Ω)</th></tr>\n\t\t";
          echo "<tr><td>" . $specific_reading->getCo() . "</td><td>" . $specific_reading->getNo2() . "</td><td>" . $specific_reading->getNh3() . "</td></tr>\n\t\t";
        ?>
      </table>
    </div>

    <div id="contenitore-grafici" class="container text-center">
      <canvas id="day_chart_1"></canvas>
      <canvas id="day_chart_2"></canvas>
    </div>

    <script>
      // opzioni globali
      Chart.defaults.font.family = 'coves-light';
      Chart.defaults.font.size = 20;
      // etticchette del grafico
      const labels = [
        <?php
            foreach($daily_readings as $reading) {
              $date = strval($reading->getdate());
              $day_date = date('d/m/Y', strtotime($date));
              $day_time = date('H:i', strtotime($date));
              // ottiene il giorno e l'ora di ogni Misurazione dello stesso giorno
              echo "'" . $day_time . "',";
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
                foreach($daily_readings as $reading) {
                  // ottiene il PM10 per ogni Misurazione dello stesso giorno
                  echo "'" . strval($reading->getPm10()) . "',";
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
                foreach($daily_readings as $reading) {
                  // ottiene la Temperatura per ogni Misurazione dello stesso giorno
                  echo "'" . strval($reading->getTemperature()) . "',";
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
                foreach($daily_readings as $reading) {
                  // ottiene l'NO2 per ogni Misurazione dello stesso giorno
                  echo "'" . strval($reading->getNo2()) . "',";
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
      
      // configurazioni del grafico
      const config = {
        type: 'line',
        data: data,
        options: {
          plugins: {
            title: {
              display: true,
              text: <?php echo '"Andamento PM10 e Temperatura ' . $day_date . '"'?>,
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

      // configurazioni del grafico dell'NO2
      const config_no2 = {
        type: 'line',
        data: data_no2,
        options: {
          plugins: {
            title: {
              display: true,
              text: <?php echo '"Andamento NO2 ' . $day_date . '"'?>,
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

      // ottiene lo spazio per disegnare il grafico
      let chart = document.getElementById('day_chart_1').getContext('2d');

      // disegna il grafico
      let day_chart_1 = new Chart(
        chart,
        config
      );
      

      // ottiene lo spazio per disegnare il grafico dell'NO2
      let chart_no2 = document.getElementById('day_chart_2').getContext('2d');

      // disegna il grafico dell'NO2
      let day_chart_2 = new Chart(
        chart_no2,
        config_no2
      );
    </script>
    <?php
        // viene stampato un messaggio informativo se non ci sono Misurazioni nella data specificata
        } else {
          echo "<p>Non è stata effettuata una rilevazione nella data inserita.</br>Tornare alla pagina precedente e riprovare.</p>";
        }
    ?>
  </body>
</html>