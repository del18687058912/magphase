#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: Felipe Espic

DESCRIPTION:
This script extracts low-dimensional acoustic parameters from a wave file.
Then, it resynthesises the signal from these features.
Features:
- m_mag_mel_log: Mel-scaled Log-Mag (dim=nbins_mel,   usually 60).
- m_real_mel:    Mel-scaled real    (dim=phase_dim, usually 45).
- m_imag_mel:    Mel-scaled imag    (dim=phase_dim, usually 45).
- v_lf0:         Log-F0 (dim=1).

INSTRUCTIONS:
This demo should work out of the box. Just run it by typing: python <script name>
If wanted, you can modify the input options and/or perform some modification to the
extracted features before re-synthesis. See the main function below for details.
"""
import sys, os
this_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.realpath(this_dir + '/../src'))
import numpy as np
import libutils as lu
import libaudio as la
from libplot import lp
import magphase as mp

def plots(m_mag_mel_log, m_real_mel, m_imag_mel, v_lf0):
    lp.plotm(m_mag_mel_log)
    lp.title(' Mel-scaled Log-Magnitude Spectrum')
    lp.xlabel('Time (frames)')

    lp.ylabel('Mel-scaled frequency bins')

    lp.plotm(m_real_mel)
    lp.title('"R" Feature Phase Spectrum')
    lp.xlabel('Time (frames)')
    lp.ylabel('Mel-scaled frequency bins')

    lp.plotm(m_imag_mel)
    lp.title('"I" Feature Phase Spectrum')
    lp.xlabel('Time (frames)')
    lp.ylabel('Mel-scaled frequency bins')

    lp.figure()
    lp.plot(np.exp(v_lf0)) # unlog for better visualisation
    lp.title('F0')
    lp.xlabel('Time (frames)')
    lp.ylabel('F0')
    lp.grid()
    return


if __name__ == '__main__':  
    # CONSTANTS:==========================================================================
    out_dir       = 'data_48k/wavs_syn'             # Where the synthesised waveform will be stored.
    b_plots       = True                            # True if you want to plot the extracted parameters.

    # INPUT:==============================================================================
    wav_file_orig = 'data_48k/wavs_nat/hvd_593.wav' # Original natural wave file. You can choose anyone provided in the /wavs_nat directory.
    b_const_rate  = False
    mag_dim       = 100
    phase_dim     = 45

    # PROCESS:============================================================================
    lu.mkdir(out_dir)

    # ANALYSIS:
    print("Analysing.....................................................")
    m_mag_mel_log, m_real_mel, m_imag_mel, v_lf0_smth, v_shift, fs, fft_len = mp.analysis_compressed(wav_file_orig, mag_dim=mag_dim, phase_dim=phase_dim,
                                                                                                                    b_const_rate=b_const_rate)

    # MODIFICATIONS:
    # You can modify the parameters here if wanted.

    # SYNTHESIS:
    print("Synthesising.................................................")
    v_syn_sig = mp.synthesis_from_compressed(m_mag_mel_log, m_real_mel, m_imag_mel, v_lf0_smth, fs, b_const_rate=b_const_rate, b_out_hpf=False)

    # SAVE WAV FILE:
    print("Saving wav file..............................................")
    wav_file_syn = out_dir + '/' + lu.get_filename(wav_file_orig) + ('_copy_syn_low_dim_mag_dim_%d_ph_dim_%d_const_rate_%d.wav' % (mag_dim, phase_dim, b_const_rate))
    la.write_audio_file(wav_file_syn, v_syn_sig, fs)

    # PLOTS:===============================================================================
    if b_plots:
        plots(m_mag_mel_log, m_real_mel, m_imag_mel, v_lf0_smth)
        raw_input("Press Enter to close de figs and finish...")
        lp.close('all')

    print('Done!')



