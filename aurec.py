from aip import AipSpeech

""" 你的 APPID AK SK """
APP_ID = ''
API_KEY = ''
SECRET_KEY = ''

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY) 


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

# 识别本地文件
result = client.asr(get_file_content('rec.wav'), 'wav', 16000, {
    'dev_pid': 1537,
})

print(result)