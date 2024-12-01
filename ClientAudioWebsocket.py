import websocket
import threading
import pyaudio
import time
from datetime import datetime
from pydub import AudioSegment
from io import BytesIO
import os
import argparse

def setupMic():
    import sounddevice as sd
    devices = sd.query_devices()
    for index, device in enumerate(devices):
        print(f"Index {index}: {device['name']} (Input Channels: {device['max_input_channels']}, Output Channels: {device['max_output_channels']})")

    return int(input("Please enter a Microphone index : "))

class voicebotClient:
    def __init__(self, url, token):
        self.url = url
        self.token = token
        self.skip_mic = False
        self.ws = None
        self.audio_format = pyaudio.paInt16
        self.channels = 1
        self.sample_rate = 16000
        self.chunk = 40
        self.customer_wav_buf = b''
        #self.input_device_index = 5
        self.input_device_index = mic_index

    def save_audio_file(self, audio_data):
        file_name = "saved_audio/tts/" + str(int(time.time()*1000)) + ".wav"
        audio_io = BytesIO(audio_data)
        audio = AudioSegment.from_file(audio_io, format="wav") 
        if not os.path.exists("saved_audio/tts/"):
            os.mkdir("saved_audio/tts/")
        audio.export(file_name, format="wav")   
        return audio
    
    def on_message(self, ws, message):
        print(message)
        if type(message) == str:
            print(message)
        elif type(message) == bytes:
            print(datetime.now(), "Received audioBytes")
            self.customer_wav_buf += message
        else:
            print(message)

    def on_error(self, ws, error):
        print(datetime.now(), "Error:", error)

    def on_close(self, ws, close_status_code, close_msg):
        print(datetime.now(), "Connection closed:", close_status_code, close_msg)

    
    def on_open(self, ws):
        def run(*args):
            def sendAudioChunk(in_data, frame_count, time_info, status):
                ws.send(in_data, websocket.ABNF.OPCODE_BINARY)
                # print("Sending Audio")
                return (in_data, pyaudio.paContinue)

            audio = pyaudio.PyAudio()
            stream = audio.open(format=self.audio_format,
                                channels=self.channels,
                                rate=self.sample_rate,
                                input=True,
                                frames_per_buffer=self.chunk,
                                input_device_index=self.input_device_index,
                                stream_callback=sendAudioChunk)

            print(datetime.now(), "Recording...")
            stream.start_stream()
            try:
                while stream.is_active():
                    pass
            except KeyboardInterrupt:
                print(datetime.now(), "Recording stopped")
        
        threading.Thread(target=run).start()

    def connect(self):
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        self.ws = websocket.WebSocketApp(
            self.url,
            header=headers,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )
        self.ws.run_forever()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument('--mic', type=int, help='Microphone Index')

    args = parser.parse_args()

    mic_index = 0
    if args.mic is None:
        mic_index = setupMic()
    else:
        mic_index = args.mic

    voicebot_client = voicebotClient("ws://147.185.221.23:16712", "your-auth-token")
    voicebot_client.connect()