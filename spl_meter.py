#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  spl_meter.py
#  
#  Copyright 2021  <pi@raspberrypi-4>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

"""Based on the northcliff_spl_monitor.py Version 0.7 - Monitor and display approximate Sound Pressure Levels

Disclaimer: Not to be used for accurate sound level measurements.
Only measures a limited bandwidth, has a limited method of frequency compensation and requires calibration.

incorporating Pimoroni code to allow switch between views (normal & log2) using proximity sensor

"""

import ST7735
from PIL import Image, ImageDraw, ImageFont
from fonts.ttf import RobotoMedium as UserFont
import sounddevice
import numpy
import math
import time
import sys
try:
    # Transitional fix for breaking change in LTR559
    from ltr559 import LTR559
    ltr559 = LTR559()
except ImportError:
    import ltr559

class Noise():
    # From https://github.com/pimoroni/enviroplus-python/blob/master/library/enviroplus/noise.py
    # with a change from mean to RMS amplitude measurements in the get_amplitudes_at_frequency_ranges method and
    # the addition of device = "dmic_sv" in the _record method
    
    def __init__(self,
                 sample_rate=16000,
                 duration=0.5):
        """Noise measurement.

        :param sample_rate: Sample rate in Hz
        :param duraton: Duration, in seconds, of noise sample capture

        """

        self.duration = duration
        self.sample_rate = sample_rate

    def get_amplitudes_at_frequency_ranges(self, ranges):
        """Return the RMS amplitude of frequencies in the given ranges.

        :param ranges: List of ranges including a start and end range

        """
        recording = self._record()
        magnitude = numpy.square(numpy.abs(numpy.fft.rfft(recording[:, 0], n=self.sample_rate)))
        result = []
        for r in ranges:
            start, end = r
            result.append(numpy.sqrt(numpy.mean(magnitude[start:end])))
        return result


    def _record(self):
        return sounddevice.rec(
            int(self.duration * self.sample_rate),
            samplerate=self.sample_rate,
            device = "dmic_sv",
            blocking=True,
            channels=1,
            dtype='float64'
        )

noise = Noise()


"""
Examples of Noise Measurements...
Near-total silence - 0 dB
A whisper - 15 dB
A library - 45 dB
A normal conversation - 60 dB
A toilet flushing 75-85 dB
A noisy restaurant - 90 dB
Peak noise on a hospital ward - 100dB
A baby crying - 110 dB
A jet engine - 120 dB
A balloon popping - 157 dB
A SaturnV Rocket - 204 dB
"""
print("Sound Meter")
print("Press Ctrl+C to exit")

print_values = False

disp = ST7735.ST7735(
    port=0,
    cs=ST7735.BG_SPI_CS_FRONT,
    dc=9,
    backlight=12,
    rotation=270)

disp.begin()

img = Image.new('RGB', (disp.width, disp.height), color=(0, 0, 0))
draw = ImageDraw.Draw(img)
font_size_small = 8
font_size_med = 10
font_size_large = 24
font_size_xlarge = 32
xlgefont = ImageFont.truetype(UserFont, font_size_xlarge)
lgefont = ImageFont.truetype(UserFont, font_size_large)
medfont = ImageFont.truetype(UserFont, font_size_med)
smallfont = ImageFont.truetype(UserFont, font_size_small)


"""
1/1 Octave Band Noise Measurements
31Hz, 63Hz, 125Hz, 250Hz, 500Hz, 1kHz, 2kHz, 4kHz, 8kHz and 16kHz
Calculating the Lower Band Limit: Centre Frequency x 0.707
Calculating the Upper Band Limit: Centre Frequency x 1.412
"""
lower_multiplier = 0.707
upper_multiplier = 1.412

max_spl = 450 # tune the graph display
log2_max_spl = math.log(max_spl,2)

l_margin = 29
t_margin = 10
gap = 1

count = 1
last_page = 0
delay = 0.5  # Debounce the proximity tap
display_type = 'n' # Set default display type

aww_go_on = True

try:
    while aww_go_on == True:
        proximity = ltr559.get_proximity()
        
        # If the proximity crosses the threshold, toggle the mode
        if proximity > 1500 and time.time() - last_page > delay:
            if display_type == 'n':
                display_type = 'l'
            elif display_type == 'l':
                display_type = 'n'
            last_page = time.time()

        if print_values:
            print('========== Measurement No. ' + str(count) + '  ==========')
            count+=1
        # Mems Microphone has a range of ~ 50Hz to 15kHz, so miss out 1st & last octaves
        bands=[8000, 4000, 2000, 1000, 500, 250, 125, 63]
        no_of_measurements = len(bands)
        # Approximate weightings of A curve at the mid frequencies of each band
        # frequency/dba curve taken from: http://sengpielausio.com/calculator-dba-spl.htm
        # dba weightings converted to factors using: www.mogami.com/e/cad/db.html
        a_weightings=[1.2, 1.6, 1.6, 1.0, 0.5, 0.1, 0.02, 0.003]
        amps = noise.get_amplitudes_at_frequency_ranges([(round(b*lower_multiplier), round(b*upper_multiplier)) for b in bands ])

        weighted_amps=[]

        for b in range (no_of_measurements):
            weighted_amps.insert(b, round(2*(amps[b]*a_weightings[b]), 2))


        bar_height = round((disp.height-no_of_measurements+1)/(no_of_measurements+1))

        # can use log2 of the value to show dynamics at lower values, and less at the hieghest values
        # convert the value to a percentage of the available width on the screen
        if display_type == 'l':
            bar_values = [round((disp.width-l_margin) * ((max(0,math.log(s,2))*(100/log2_max_spl)/100)), 2) for s in weighted_amps]
            x_label = 'Log(2) Ampilitude RMS(A)'
            bar_fill=(251,164,9)
        elif display_type == 'n':
            bar_values = [round((disp.width-l_margin) * (s/max_spl), 2) for s in weighted_amps]
            x_label = 'Ampilitude RMS(A)'
            bar_fill = (58,68,238)
        else:
            draw.text((25, 3), "Oops!", font=xlgefont, fill=(255,0,0))
            draw.text((13,37), "Option n or l", font=lgefont, fill=(180,180,180))
            aww_go_on = False

        if aww_go_on:
            draw.rectangle((0, 0, disp.width, disp.height), (0, 0, 0))
            draw.text((0,0), 'Freq', font=medfont, fill=(255, 255, 255))
            draw.text((l_margin, 0), x_label, font=medfont, fill=(255, 255, 255))
            for i in range(no_of_measurements):

                if print_values:
                    print('------------------------- Data for ' + str(bands[i]))
                    print('Raw Amps\t' + 'Weighted Amps\t' + 'Chart Value')
                    print( str(round(amps[i], 3)) + '\t\t' + str(weighted_amps[i]) + '\t\t'  + str(bar_values[i]) )

                top_x = l_margin
                top_y = ((i*bar_height)+(gap+1) + t_margin)
                bot_x = l_margin + bar_values[i]
                bot_y = ((i*bar_height)+(bar_height+t_margin))-gap
                w, h = draw.textsize(str(bands[i]), font=smallfont)
                txt_pos = ((l_margin)-(w+7), ((i*bar_height)+t_margin))
        #        txt_pos = (0, ((i*bar_height)+t_margin))
                draw.rectangle((top_x, top_y, bot_x, bot_y), fill=bar_fill) #251,164,9 | 60,116,216 | 239,11,23
                draw.text(txt_pos, str(bands[i]), font=smallfont, fill=(255, 255, 255))

        disp.display(img)
# Exit cleanly
except KeyboardInterrupt:
    sys.exit(0)
