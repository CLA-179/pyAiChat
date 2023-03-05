
import pyttsx3
 
engine = pyttsx3.init() #创建engine并初始化

# voices = engine.getProperty('voices')
# engine.setProperty('voice',voices[2].id)

engine.say('') #开始朗读
engine.runAndWait() #等待语音播报完毕