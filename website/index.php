<?php
  session_start();
?>

<!DOCTYPE html>
<html lang="it">
  <head>
    <link rel="stylesheet" href="css/index.css">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">  <!-- link al Bootsrap -->
    <script src="https://cdn.jsdelivr.net/npm/apexcharts"></script> <!-- link a ApexChart API-->
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
        <h1>Ultima misurazione effettuata</h1>
      </div>

      <?php

        // variabili di sessione per ordinare
        $_SESSION['date_time_desc'] = true;
        $_SESSION['pm10_desc'] = true;
        $_SESSION['temperature_desc'] = true;
        $_SESSION['co2_desc'] = true;
        require_once("readingClass.php");
        // ultima Misurazione effettuata
        $reading = Reading::readingIndex();
        // eliminazione secondi dalla data della Misurazione
        $date = strval($reading->getDate());
        $day = date('d-m-Y H:i', strtotime($date));
        // ottiene i valori del PM2.5 e del PM10
        $pm25 = $reading -> getPm25();
        $pm10 = $reading -> getPm10();
        // ottiene il valore del dBA della Misurazione
        $dBA = $reading -> getDBA();
        // calcolo del AQI per PM2.5 e per PM10
        $dBA = intval($dBA*100/120); // converte il valore del dBA in centesimi
        $aqi_pm25 = $pm25*100/25; // 25: valore limite per PM2.5
        $aqi_pm10 = $pm10*100/50; // 50: valore limite per PM10
        // sceglie il valore più alto
        if ($aqi_pm10 > $aqi_pm25) {
          if ($aqi_pm10 < 50) {
            $str_aqi = "Buona"; // concentrazione sotto la metà del valore limite
          } else if ($aqi_pm10 < 100) {
            $str_aqi = "Discreta"; // concentrazione uguale al valore limite
          } else if ($aqi_pm10 < 150) {
            $str_aqi = "Mediocre"; // concentrazione ugale al valore limite e mezzo
          } else if ($aqi_pm10 < 200) {
            $str_aqi = "Scadente"; // concentrazione uguale al doppio del valore limite
          } else {
            $str_aqi = "Pessima"; // concentrazione oltre al doppio del valore limite
          }
        } else {
          if ($aqi_pm25 < 50) {
            $str_aqi = "Buona"; // concentrazione sotto la metà del valore limite
          } else if ($aqi_pm25 < 100) {
            $str_aqi = "Discreta"; // concentrazione uguale al valore limite
          } else if ($aqi_pm25 < 150) {
            $str_aqi = "Mediocre"; // concentrazione uguale al valore limite e mezzo
          } else if ($aqi_pm25 < 200) {
            $str_aqi = "Scadente"; // concentraazione uguale al doppio del valore limite
          } else {
            $str_aqi = "Pessima"; // concentrazione oltre al doppio del valore limite
          }
        }
        echo "<div class='container'><p>Data Ora: " . $day . "</p></div><div class='container'<p> Qualità dell'aria: $str_aqi</p></div>";
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
            radialBar:{
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
                  formatter: function () { return <?php echo $reading -> getDBA() ?> }
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
    <!-- div con la tabella che contiene i dati dell'ultima Misurazione-->
    <div class="container">
      <table class="table table-striped table-hover table-bordered table-responsive">
      <?php
        echo "\t<tr><th>PM1 (<b>µg</b>/m<sup>3</sup>)</th><th>PM2.5 (<b>µg</b>/m<sup>3</sup>)</th><th>PM10 (<b>µg</b>/m<sup>3</sup>)</th></tr>\n\t\t";
        echo "<tr><td>" . $reading->getPm1() . "</td><td>" . $reading->getPm25() . "</td><td>" . $reading->getPm10() . "</td></tr>\n\t\t";
        echo "<tr><th>Temperatura (<b>°</b>C)</th><th>Umidità (%)</th><th>Pressione atmosferica (Pa)</th></tr>\n\t\t";
        echo "<tr><td>" . $reading->getTemperature() . "</td><td>" . $reading->getHumidity() . "</td><td>" . $reading->getAirPressure() . "</td></tr>\n\t\t";
        echo "<tr><th>CO (Ω)</th><th>NO<sub>2</sub> (Ω)</th><th>NH<sub>3</sub> (Ω)</th></tr>\n\t\t";
        echo "<tr><td>" . $reading->getCo() . "</td><td>" . $reading->getNo2() . "</td><td>" . $reading->getNh3() . "</td></tr>\n\t\t";
      ?>
      </table>
    </div>
    <!-- div con il link alla lista con le ultime 10 Misurazioni -->
    <div class="container text-right">
      <p id='readings'><a href="readings.php">Storico misurazioni</a></p>
    </div>

    <div id="explan" class="container-fluid jumbotron">
      <!--<img src="qualchecosa" alt="qualchecosa">-->
      <h2 id="project" class="text-center">Il Progetto</h2><br>
      <p class="expText">Air Quality Station è una centralina per la rilevazione di inquinanti, creata in collaborazione con il Comune di Vittorio Veneto.</p><br>
      <p class="expText">Il progetto è a cura di un gruppo di studenti della classe 5B, indirizzo informatico, dell'Istituto di Istruzione Superiore "Vittorio Veneto" Città della Vittoria nell'anno scolastico 2021/22.</p><br><br>
      <h2 class="expText"><u id="pollutant">Inquinanti rilevati</u></h2><br>
      <ul class="expText">
        <li><b class="pollutant">PM:</b> insieme di particelle solide e liquide polveri di diametro variabile (comunque dell’ordine dei millimetri) dispersi in atmosfera. Il particolato è considerato il maggior inquinante nelle città</li>
        <li><b class="pollutant">Temperatura:</b> condizione termica dell'atmosfera in un determinato periodo</li>
        <li><b class="pollutant">Pressione:</b> carico esercitato dall'atmosfera sulla superficie terrestre</li>
        <li><b class="pollutant">Umidità:</b> quantità di vapore acqueo presente nell'aria</li>
        <li><b class="pollutant">Monossido di carbonio (CO):</b> gas prodotto ogni volta che si brucia qualcosa che contenga carbonio. Per le sue caratteristiche può essere inalato in modo subdolo ed impercettibile, fino a raggiungere nell’organismo concentrazioni letali</li>
        <li><b class="pollutant">Diossido di azoto (NO<sub>2</sub>):</b> inquinante che viene normalmente generato a seguito di processi di combustione. In particolare, il traffico veicolare ne è uno dei maggiori responsabili</li>
        <li><b class="pollutant">Ammoniaca (NH<sub>3</sub>):</b> gas che gioca un ruolo importante nel nostro ambiente, in quanto partecipa al ciclo dell’azoto, contribuisce alla neutralizzazione degli acidi e partecipa alla formazione di particolato atmosferico secondario</li>
        <li><b class="pollutant">Inquinamento acustico (dBA):</b> livello di rumore, se elevato può causare effetti nocivi sull’attività, sulla salute delle persone, degli animali e dell’ambiente circostante.</li>
      </ul><br>
      <p class="expText"><b class="pollutant">NB:</b> CO, NO<sub>2</sub> e NH<sub>3</sub> sono rappresentati in resistenza elettrica esercitata nell'aria.</p>
    </div>

    <div id="video" class="container-fluid jumbotron text-center">
      <div class="text-left" id="videoit">
        <video width="384" height="218" controls>
          <source src="video/italian.mp4" type="video/mp4">
        </video>
        <p class="text-center">Italiano</p>
      </div>
      <div class="text-right" id="videoen">
        <video width="384" height="218" controls>
          <source src="video/english.mp4" type="video/mp4">
        </video>
        <p class="text-center">English</p>
      </div>
    </div>
  </body>
</html>
