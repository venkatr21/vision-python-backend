import azure.cognitiveservices.speech as speechsdk
import base64
from flask import Flask, render_template, Response, jsonify, request
import os
import requests
import time
import re
from os import path
from pydub import AudioSegment
app = Flask(__name__)

langarr = open("lang.txt","r").readlines()
codes = open("codes.txt","r").readlines()

langcodes = {}


for i in range(0,len(langarr)):
    langarr[i] = langarr[i][:-1].strip()
    codes[i] = codes[i].strip()
    langcodes[langarr[i]] = codes[i]    

print(langcodes)

def languagevalidation(input_str):
    global langarr
    for lang in langarr:
        if re.search(lang,input_str):
            return lang,langcodes[lang]
    return 'default','def'
    
def wav2text():
    speech_config = speechsdk.SpeechConfig(subscription="b84e809f86864f4b8205a37880991a61", region="eastus")
    audio_input = speechsdk.AudioConfig(filename="temp.wav")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)
    result = speech_recognizer.recognize_once_async().get()
    return result.text

def b64towav(input_str):
    decode_string = base64.b64decode(input_str)
    wav_file = open("temp.m4a", "wb")
    wav_file.write(decode_string)
    wav_file.close()
    sound = AudioSegment.from_file("temp.m4a", format="m4a")
    sound.export("temp.wav", format="wav")


@app.route('/',methods=['POST','GET'])
def temp():
    return "Reached the server"
    

@app.route('/stt',methods=['GET','POST'])
def final():
    input_string = request.form['data']
    b64towav(input_string)
    output = wav2text()
    print(output.lower())
    lang,code = languagevalidation(output.lower())
    ret = {'lang':lang, 'code':code}
    return jsonify(ret)


if __name__=="__main__":
    app.run(host='0.0.0.0',port=8000)
