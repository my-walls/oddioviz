import pyaudio
import wave
import sys
import terminalplot as tp
from scipy import signal

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
    f, P = signal.periodogram(data, fs)
    tp.plot(f.tolist(), P.tolist(), rows=50, columns=150)

# Stop and close the stream
stream.stop_stream()
stream.close()
# Terminate the PortAudio interface
p.terminate()
