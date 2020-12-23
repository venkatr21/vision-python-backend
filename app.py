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

def languagevalidation(input_str):
    arr = ['english','tamil']
    for lang in arr:
        if re.search(lang,input_str):
            return lang
    return 'english'
    
def wav2text():
    speech_config = speechsdk.SpeechConfig(subscription="//KEY", region="eastus")
    audio_input = speechsdk.AudioConfig(filename="temp.m4a")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)
    result = speech_recognizer.recognize_once_async().get()
    return result.text

def b64towav(input_str):
    decode_string = base64.b64decode(input_str)
    wav_file = open("temp.m4a", "wb")
    wav_file.write(decode_string)
    wav_file.close()

@app.route('/stt',methods=['POST'])
def final():
    input_string = request.form['data']
    b64towav(input_string)
    output = wav2text()
    output = languagevalidation(output.lower())
    print(output)
    return output

if __name__=="__main__":
    app.run(host="localhost",port=5000)
