## Signal Transmission through UART and IQ Modulation
This project implements a real-time audio transmission system using UART and IQ modulation, with FPGA-based I/Q signal generation and wireless transmission via an IQ modulator. The signal is received and decoded using an RTL-SDR dongle and GNU Radio.

### Project Overview
The goal of this project was to transmit a stereo audio signal by converting it into I/Q samples, sending those samples over UART to an FPGA, which then outputs analog I and Q signals through an R-2R DAC. These signals are modulated using an IQ modulator and transmitted wirelessly to a receiver chain consisting of RTL-SDR and GNU Radio for demodulation and playback.

This work was done as part of a summer internship at **WEL Lab, IIT Bombay**.

### 🧱 System Architecture
1. Transmission Side:
- A WAV file is read in GNU Radio at 44.1 kHz.
- The signal is passed through a Hilbert Transform to create I and Q components.
- I and Q signals are scaled and interleaved into 8-bit unsigned bytes.
- A Python block sends these over UART (baud: 88200) to an Intel MAX 10 FPGA.

2. FPGA:
- A Verilog UART receiver receives the interleaved I and Q bytes.
- Using a toggle logic, it separates I and Q samples.
- Each 8-bit sample is output through GPIO pins and converted to analog using R-2R ladders.
- The analog I and Q signals are fed into an IQ modulator operating at 1.3 GHz.

3. Reception Side:
An RTL-SDR dongle tuned to 1.3 GHz receives the RF signal.

4. GNU Radio flow:
- RTL-SDR block (250 kSps)
- Bandpass filtering
- Complex-to-Real conversion
- Rational resampling (to match audio rate)
- Final filtering and saving to WAV sink

### 🧪 Challenges Faced
- Distorted audio when transmitting multi-tone (music) signals due to timing mismatches.
- UART buffering issues and baudrate constraints.
- Handling synchronization between I and Q channels in FPGA logic.
- Resampling and filtering in GNU Radio to recover clear audio.

Each of these challenges helped in developing a better understanding of system timing, signal integrity, and RF chain synchronization.

#### 📖 Blog
Read more about the motivation, debugging process, and learnings here:
👉 [Blog](https://shankari02.github.io/blog/intern/)

#### 🛠️ Tools & Technologies
- GNU Radio
- RTL-SDR
- Python (Custom GNU Radio blocks)
- Verilog (Intel Quartus for MAX 10)
- UART communication
- IQ Modulation
- R-2R DACs

### 🙏 Acknowledgments
Huge thanks to WEL Lab, IIT Bombay, and my mentors Prof. Siddharth Tallur sir, Amit sir, Maheshwar sir and Mahesh sir for their continuous support and guidance.
