from vosk import Model, KaldiRecognizer
import pyaudio
import json
import socket

model = Model(r"/Users/eudgen/Desktop/Robotic Arm/VCR/vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 16000)

mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()

# Set up socket connection
rec_host = '192.168.106.2'
port = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((rec_host, port))

while True:
    data = stream.read(4096)

    if recognizer.AcceptWaveform(data):
        result = recognizer.Result()
        result_dict = json.loads(result)
        text = result_dict.get("text", "")
        print(text)

        # Send the recognized text to Raspberry Pi
        sock.sendall(text.encode())