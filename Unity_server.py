import asyncio
import websockets
import wave
import time
import struct

async def handler(websocket, path):
    print("Client connected")
    received_audio_data = []
    start_time = time.time()
    while True:
        try:
            message = await websocket.recv()
            if isinstance(message, str):
                # จัดการข้อความที่เป็นข้อความธรรมดา
                print(f"Received text message: {message}")
            else:
                # จัดการข้อความที่เป็นไบต์ (ข้อมูลเสียง)
                received_audio_data.append(message)
                print(f"Received audio data chunk of size: {len(message)} bytes")
        except websockets.exceptions.ConnectionClosedOK:
            print("Connection closed by client")
            break
        except websockets.exceptions.ConnectionClosedError:
            print("Connection closed with error")
            break
        if time.time() - start_time > 120:  # 300 วินาที = 5 นาที
            print("Time's up! Closing connection.")
            await websocket.close()
            break
    # หลังจากการเชื่อมต่อถูกปิด บันทึกข้อมูลเสียง
    save_audio_data(received_audio_data)

def save_audio_data(audio_data_chunks):
    # รวมข้อมูลเสียงทั้งหมด
    audio_data = b''.join(audio_data_chunks)
    # แปลงข้อมูลไบต์กลับเป็น float32
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
    # บันทึกเป็นไฟล์ WAV
    with wave.open('output.wav', 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)  # 2 ไบต์สำหรับ int16
        wav_file.setframerate(8000)
        wav_file.writeframes(pcm_data)
    print("Audio data saved to output.wav")

start_server = websockets.serve(handler, "0.0.0.0", 8000)

print("Server started on port 8000")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
