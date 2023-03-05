
import pyaudio
import numpy as np
from scipy import fftpack
import wave
from aip import AipSpeech
import openai
import pyttsx3

 
engine = pyttsx3.init() #语音读出初始化

#将下面引号内填入对应的内容

openai.api_key = '' #openai的key

""" 你的 APPID AK SK """  #百度语音识别
APP_ID = ''
API_KEY = ''
SECRET_KEY = ''

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY) 


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


# 录音

def recording(filename, time=0, threshold=8000):

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
            waitSecond = int(RATE / CHUNK * 2) #无声音2S后结束录音
            if stopflag2 + stopflag > waitSecond:
                if stopflag2 > waitSecond // 3 * 2:
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
    


def readin():
    i = 0
    while True:
        recording('./rec.wav')  # 没有声音自动停止，自动停止

        f = wave.open('./rec.wav', 'rb')
        time_count = f.getparams().nframes/f.getparams().framerate
        print(time_count)
        if time_count > 4: #判断声音是否长于4s，避免上传空白声音
            break
        else:
            i += 1
        
        if i == 5:
            print('语音已超时') #尝试5次后结束对话
            exit(0)



def aurec():
    rec_result = client.asr(get_file_content('rec.wav'), 'wav', 16000, {
        'dev_pid': 1537,
    })

    if rec_result['err_no'] == 0:
        rec_res = rec_result['result'][0]
        print(rec_res)
        return rec_res
    else:
        print('err at recognise')
        return '!err()'


def readout(str):
    engine.say(str) #开始朗读
    engine.runAndWait() #等待语音播报完毕

def main():
    mes=[
        {"role": "system", "content": "你是一个AI机器人助手。"},
    ]
    # print(mes)

    # userin = input()

    # while userin != "!exit()" :
    while True:
        readin()
        userin = aurec()
        while userin == '!err()':
            print('语音识别错误')
            readin()
            userin = aurec()

        mes.append({"role": "user", "content": userin})
        # print(mes)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=mes
        )
        # print(response)
        res = response['choices'][0]['message']['content']

        print(res)

        mes.append({"role": "assistant", "content": res})

        readout(res)

        # userin = input()

if __name__ == '__main__':
    main()