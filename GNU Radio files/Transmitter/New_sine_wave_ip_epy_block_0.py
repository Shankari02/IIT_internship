import numpy
from gnuradio import gr
import serial

class blk(gr.basic_block):
    def __init__(self):
        gr.basic_block.__init__(
            self,
            name="UART IQ TX (Interleaved)",
            in_sig=[numpy.uint8, numpy.uint8],  # I and Q streams
            out_sig=[]
        )
        self.ser = serial.Serial(
	port='/dev/ttyUSB1',   # Set your correct UART port
	baudrate=4096000,      # 1 Mbps
	timeout = 0.001
        )

    def __del__(self):
        if self.ser and self.ser.is_open:
            self.ser.close()

    def general_work(self, input_items, output_items):
        I = input_items[0]
        Q = input_items[1]

        n = min(len(I), len(Q))
        # Interleave I and Q
        interleaved = numpy.empty(2 * n, dtype=numpy.uint8)
        interleaved[0::2] = I[:n]
        interleaved[1::2] = Q[:n]

        try:
            self.ser.write(interleaved.tobytes())
        except Exception as e:
            print("UART Write Error:", e)

        # Tell GNU Radio we consumed the items
        self.consume(0, n)
        self.consume(1, n)
        return 0  # Let GNU Radio schedule again

