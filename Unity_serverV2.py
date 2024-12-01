import asyncio
import websockets
import wave
import time
import struct
import threading

class AudioRecorder:
    def __init__(self):
        self.received_audio_data = []
        self.lock = threading.Lock()
        self.start_time = time.time()
        self.file_counter = 1  # ตัวนับสำหรับชื่อไฟล์
        self.recording_interval = 120  # 120 วินาที = 2 นาที

    def add_audio_data(self, data):
        with self.lock:
            self.received_audio_data.append(data)

    def save_audio_data(self):
        with self.lock:
            if not self.received_audio_data:
                return
            audio_data = b''.join(self.received_audio_data)
            num_samples = len(audio_data) // 4  # float32 มีขนาด 4 ไบต์
            fmt = '<' + 'f' * num_samples  # Little-endian float32
            print(f"Total samples: {num_samples}")
            try:
                samples = struct.unpack(fmt, audio_data)
            except struct.error as e:
                print(f"Error unpacking audio data: {e}")
                return
            # แปลง float เป็น int16 PCM
            pcm_samples = [int(max(min(s, 1.0), -1.0) * 32767) for s in samples]
            pcm_data = struct.pack('<' + 'h' * len(pcm_samples), *pcm_samples)
            # สร้างชื่อไฟล์ที่ไม่ซ้ำกัน
            filename = f'output_{self.file_counter}.wav'
            with wave.open(filename, 'wb') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)  # 2 ไบต์สำหรับ int16
                wav_file.setframerate(8000)
                wav_file.writeframes(pcm_data)
            print(f"Audio data saved to {filename}")
            # รีเซ็ตข้อมูลและเพิ่มตัวนับไฟล์
            self.received_audio_data = []
            self.file_counter += 1

    def start_timer(self):
        threading.Thread(target=self._timer_thread, daemon=True).start()

    def _timer_thread(self):
        while True:
            time.sleep(self.recording_interval)
            self.save_audio_data()

async def handler(websocket, path):
    print("Client connected")
    recorder = AudioRecorder()
    recorder.start_timer()
    try:
        async for message in websocket:
            if isinstance(message, str):
                print(f"Received text message: {message}")
            else:
                recorder.add_audio_data(message)
                print(f"Received audio data chunk of size: {len(message)} bytes")
    except websockets.exceptions.ConnectionClosedOK:
        print("Connection closed by client")
    except websockets.exceptions.ConnectionClosedError:
        print("Connection closed with error")
    finally:
        # บันทึกข้อมูลเสียงที่เหลือก่อนปิดการเชื่อมต่อ
        recorder.save_audio_data()
        print("Connection closed")

start_server = websockets.serve(handler, "0.0.0.0", 8000)

print("Server started on port 8000")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
