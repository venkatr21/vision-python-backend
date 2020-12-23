import azure.cognitiveservices.speech as speechsdk
import base64
from flask import Flask, render_template, Response, jsonify, request
import os
import requests
import time
import re
from os import path
from pydub import AudioSegment

sound = AudioSegment.from_file("temp.m4a", format="m4a")
sound.export("temp.wav", format="wav")