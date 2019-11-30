import pyaudio
import wave
import sys
import terminalplot as tp
from scipy import signal

import matplotlib.pyplot as plt
import numpy as np

plt.ion()

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
fs = 44100  # Record at 44100 samples per second
seconds = 10
filename = "output.wav"

p = pyaudio.PyAudio()  # Create an interface to PortAudio

print('Recording')

stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

# Store data in chunks for 3 seconds
for i in range(0, int(fs / chunk * seconds)):
    data = list(stream.read(chunk, exception_on_overflow=False))
    f, Pxx_spec = signal.periodogram(data, fs, 'flattop', scaling='spectrum')

    plt.semilogy(f, np.sqrt(Pxx_spec))
    plt.ylim([1e-4, 1e1])
    plt.xlabel('frequency [Hz]')
    plt.ylabel('Linear spectrum [V RMS]')
    plt.draw()
    plt.pause(0.0001)
    plt.clf()

    # tp.plot(f.tolist(), P.tolist(), rows=50, columns=150)

# Stop and close the stream
stream.stop_stream()
stream.close()
# Terminate the PortAudio interface
p.terminate()
