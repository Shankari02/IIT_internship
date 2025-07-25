#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: shankari
# GNU Radio version: 3.10.1.1

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import freq_range_check_epy_block_0 as epy_block_0  # embedded python block



from gnuradio import qtgui

class freq_range_check(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "freq_range_check")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 44100

        ##################################################
        # Blocks
        ##################################################
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_fff(
                interpolation=2500,
                decimation=441,
                taps=[],
                fractional_bw=0)
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=2500,
                decimation=441,
                taps=[],
                fractional_bw=0)
        self.hilbert_fc_0 = filter.hilbert_fc(125, window.WIN_KAISER, 6.76)
        self.epy_block_0 = epy_block_0.blk()
        self.blocks_wavfile_source_0_0 = blocks.wavfile_source('/home/shankari/Downloads/bsdl/music/sa.wav', True)
        self.blocks_wavfile_sink_0 = blocks.wavfile_sink(
            '/home/shankari/test.wav',
            1,
            samp_rate,
            blocks.FORMAT_WAV,
            blocks.FORMAT_PCM_16,
            False
            )
        self.blocks_throttle_1 = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.blocks_float_to_uchar_0_0 = blocks.float_to_uchar()
        self.blocks_float_to_uchar_0 = blocks.float_to_uchar()
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_float_0, 1), (self.rational_resampler_xxx_0, 0))
        self.connect((self.blocks_complex_to_float_0, 0), (self.rational_resampler_xxx_0_0, 0))
        self.connect((self.blocks_float_to_uchar_0, 0), (self.epy_block_0, 0))
        self.connect((self.blocks_float_to_uchar_0_0, 0), (self.epy_block_0, 1))
        self.connect((self.blocks_throttle_1, 0), (self.hilbert_fc_0, 0))
        self.connect((self.blocks_wavfile_source_0_0, 0), (self.blocks_throttle_1, 0))
        self.connect((self.hilbert_fc_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_float_to_uchar_0_0, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.blocks_float_to_uchar_0, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.blocks_wavfile_sink_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "freq_range_check")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_1.set_sample_rate(self.samp_rate)




def main(top_block_cls=freq_range_check, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
