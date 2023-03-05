# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import openai
openai.api_key = ''

mes=[
      {"role": "system", "content": "你是一个AI机器人助手。"},
  ]
# print(mes)

userin = input()

while userin != "!exit()" :

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

  userin = input()