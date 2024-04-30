<?php
include('fpdf.php');

class PDF extends FPDF {
    // Colored table
    function FancyTable(array $header, array $data) {
        // Colors, line width and bold font
        $this->SetFillColor(255,0,0);
        $this->SetTextColor(0,0,0);
        $this->SetDrawColor(0,0,0);
        $this->SetLineWidth(.3);
        $this->SetFont('Helvetica', 'B', 12);
        // Header
        $misure = array (42, 30, 20, 20, 20, 20, 25, 30, 20, 20, 20);
        $i = 0;
        // altezza celle 
        $altezza_celle = 10;
        foreach ($header as $campo) {
            $this->Cell($misure[$i], $altezza_celle, $campo, 1, 0, 'C');
            $i++;
        }
        $this->Ln();
        // Color and font restoration
        $this->SetFillColor(224,235,255);
        $this->SetTextColor(0);
        $this->SetFont('Helvetica', '', 12);
        // Data
        foreach ($data as $row) {
            $this->Cell(42,$altezza_celle, $row->getDate(),1, 0, 'C');
            $this->Cell(30,$altezza_celle, $row->getTemperature(), 1, 0, 'C');
            $this->Cell(20,$altezza_celle, $row->getPm25(), 1, 0, 'C');
            $this->Cell(20,$altezza_celle, $row->getPm1(), 1, 0, 'C');
            $this->Cell(20,$altezza_celle, $row->getPm10(), 1, 0, 'C');
            $this->Cell(20,$altezza_celle, $row->getNo2(), 1, 0, 'C');
            $this->Cell(25,$altezza_celle, $row->getHumidity(), 1, 0, 'C');
            $this->Cell(30,$altezza_celle, $row->getAirPressure(), 1, 0, 'C');
            $this->Cell(20,$altezza_celle, $row->getCo(), 1, 0, 'C');
            $this->Cell(20,$altezza_celle, $row->getNh3(), 1, 0, 'C');
            $this->Cell(20,$altezza_celle, $row->getDBA(), 1, 0, 'C');
            $this->Ln();
        }
    }
}
?>
