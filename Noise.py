#personalized noise class based on roscoe81's northcliff_spl_monitor.py
#https://github.com/roscoe81/northcliff_spl_monitor/tree/dc4250232c812a7fa13c9bc0ab9fe82af0d76b38


import ST7735
from PIL import Image, ImageDraw, ImageFont
from fonts.ttf import RobotoMedium as UserFont
import sounddevice as sd
import numpy as np
from numpy import pi, log10
import math
import sys
import matplotlib.pyplot as plt
import json
import time
from datetime import datetime
from scipy.signal import zpk2tf, zpk2sos, freqs, sosfilt
from waveform_analysis.weighting_filters._filter_design import _zpkbilinear
try:
    # Transitional fix for breaking change in LTR559
    from ltr559 import LTR559
    ltr559 = LTR559()
except ImportError:
    import ltr559


print("""northcliff_spl_monitor.py Version 2.9 - Gen Monitor and display approximate Sound Pressure Levels with improved A-Curve weighting. alsamixer Mic at 10% (2.40dB Gain)

Disclaimer: Not to be used for accurate sound level measurements.

Press Ctrl+C to exit

""")



class Noise():
    def __init__(self, spl_ref_level, log_sound_data, debug_recording_capture, sample_rate=48000, duration=0.25):
        print("ghe sen")
        self.sample_counter = 0
        self.previous_sample_count = 0
        self.spl_ref_level = spl_ref_level
        self.log_sound_data = log_sound_data
        self.debug_recording_capture = debug_recording_capture
        self.duration = duration
        self.sample_rate = sample_rate
        self.max_spl = 0
        self.max_spl_datetime = None
        self.recording = []
        self.stream = sd.InputStream(samplerate=self.sample_rate, channels=1, blocksize = 12000, device = "dmic_sv", callback=self.process_frames)
        print("OK")
        

        
    def process_frames(self, recording, frames, time, status):
        self.recording = recording
        self.sample_counter += 1
                
    def restart_stream(self):
        sd.abort()
        sd.start()

    def ABC_weighting(self, curve='A'):
        """
        Design of an analog weighting filter with A, B, or C curve.
        Returns zeros, poles, gain of the filter.
        """
        if curve not in 'ABC':
            raise ValueError('Curve type not understood')

        # ANSI S1.4-1983 C weighting
        #    2 poles on the real axis at "20.6 Hz" HPF
        #    2 poles on the real axis at "12.2 kHz" LPF
        #    -3 dB down points at "10^1.5 (or 31.62) Hz"
        #                         "10^3.9 (or 7943) Hz"
        #
        # IEC 61672 specifies "10^1.5 Hz" and "10^3.9 Hz" points and formulas for
        # derivation.  See _derive_coefficients()

        z = [0, 0]
        p = [-2*pi*20.598997057568145,
             -2*pi*20.598997057568145,
             -2*pi*12194.21714799801,
             -2*pi*12194.21714799801]
        k = 1

        if curve == 'A':
            # ANSI S1.4-1983 A weighting =
            #    Same as C weighting +
            #    2 poles on real axis at "107.7 and 737.9 Hz"
            #
            # IEC 61672 specifies cutoff of "10^2.45 Hz" and formulas for
            # derivation.  See _derive_coefficients()

            p.append(-2*pi*107.65264864304628)
            p.append(-2*pi*737.8622307362899)
            z.append(0)
            z.append(0)

        elif curve == 'B':
            # ANSI S1.4-1983 B weighting
            #    Same as C weighting +
            #    1 pole on real axis at "10^2.2 (or 158.5) Hz"

            p.append(-2*pi*10**2.2)  # exact
            z.append(0)
        b, a = zpk2tf(z, p, k)
        k /= abs(freqs(b, a, [2*pi*1000])[1][0])

        return np.array(z), np.array(p), k



    def A_weighting(self, fs, output='ba'):
        """
        Design of a digital A-weighting filter.
        Designs a digital A-weighting filter for
        sampling frequency `fs`.
        Warning: fs should normally be higher than 20 kHz. For example,
        fs = 48000 yields a class 1-compliant filter.
        Parameters
        ----------
        fs : float
            Sampling frequency
        output : {'ba', 'zpk', 'sos'}, optional
            Type of output:  numerator/denominator ('ba'), pole-zero ('zpk'), or
            second-order sections ('sos'). Default is 'ba'.
        Since this uses the bilinear transform, frequency response around fs/2 will
        be inaccurate at lower sampling rates.
        """
        z, p, k = self.ABC_weighting('A')

        # Use the bilinear transformation to get the digital filter.
        z_d, p_d, k_d = _zpkbilinear(z, p, k, fs)

        if output == 'zpk':
            return z_d, p_d, k_d
        elif output in {'ba', 'tf'}:
            return zpk2tf(z_d, p_d, k_d)
        elif output == 'sos':
            return zpk2sos(z_d, p_d, k_d)
        else:
            raise ValueError("'%s' is not a valid output form." % output)

    def A_weight(self, signal, fs):
        sos = self.A_weighting(fs, output='sos')
        return sosfilt(sos, signal)
   
    def get_rms_at_frequency_ranges(self, recording, ranges):
        """Return the RMS levels of frequencies in the given ranges.

        :param ranges: List of ranges including a start and end range

        """
        magnitude = np.square(np.abs(np.fft.rfft(recording[:, 0], n=self.sample_rate)))
        result = []
        for r in ranges:
            start, end = r
            result.append(np.sqrt(np.mean(magnitude[start:end])))
        return result

    def spl(self):
        try:
            with self.stream:
                while self.sample_counter < 30:
                    if self.sample_counter != self.previous_sample_count: # Only process new sample
                        self.previous_sample_count = self.sample_counter
                        if self.sample_counter > 10: # Wait for microphone stability
                            recording_offset = np.mean(self.recording)
                            self.recording = self.recording - recording_offset # Remove remaining microphone DC Offset
                            if self.debug_recording_capture: # Option to plot recording sample capture when debugging microphone
                                plt.plot(self.recording)
                                plt.show()
                            weighted_recording = self.A_weight(self.recording, self.sample_rate)
                            weighted_rms = np.sqrt(np.mean(np.square(weighted_recording)))
                            spl_ratio = weighted_rms/self.spl_ref_level
                            if spl_ratio > 0:
                                spl = 20*math.log10(spl_ratio)
                                return spl
        except:
            self.stream.abort()
            print("meow")
			
# Acknowledgements
# A-Weighting from https://github.com/endolith/waveform_analysis/blob/master/waveform_analysis/weighting_filters/ABC_weighting.py#L29
# get_rms_at_frequency_ranges from https://github.com/pimoroni/enviroplus-python/blob/master/library/enviroplus/noise.py
        

