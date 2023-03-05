
import pyaudio
import numpy as np
from scipy import fftpack
import wave




def recording(filename, time=0, threshold=7000):

    CHUNK = 1024  # 块大小
    FORMAT = pyaudio.paInt16  # 每次采集的位数
    CHANNELS = 1  # 声道数
    RATE = 16000  # 采样率：每秒采集数据的次数
    RECORD_SECONDS = time  # 录音时间
    WAVE_OUTPUT_FILENAME = filename  # 文件存放位置
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print("请讲话：。。。")
    frames = []
    if time > 0:
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
    else:
        stopflag = 0
        stopflag2 = 0
        while True:
            data = stream.read(CHUNK)
            rt_data = np.frombuffer(data, np.dtype('<i2'))

            fft_temp_data = fftpack.fft(rt_data, rt_data.size, overwrite_x=True)
            fft_data = np.abs(fft_temp_data)[0:fft_temp_data.size // 2 + 1]


            if sum(fft_data) // len(fft_data) > threshold:
                stopflag += 1
            else:
                stopflag2 += 1
            oneSecond = int(RATE / CHUNK)
            if stopflag2 + stopflag > oneSecond :
                if stopflag2 > oneSecond // 3 * 2:
                    break
                else:
                    stopflag2 = 0
                    stopflag = 0
            frames.append(data)
    print("结束")
    stream.stop_stream()
    stream.close()
    p.terminate()
    with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
    



while True:
    recording('./rec.wav')  # 没有声音自动停止，自动停止

    f = wave.open('./rec.wav', 'rb')
    time_count = f.getparams().nframes/f.getparams().framerate #判断是否大于4s
    print(time_count)
    if time_count > 4:
        break