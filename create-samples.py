import base64
import requests
import os
import picamera
import time
import os
import datetime
import uuid
import subprocess

import json
import random
import smbus2


#create your config accordingly:
#api_key = "your_api_key_here"
#elevenLabsAPiKey = "your_elevenLabs_api_key_here"
#voice_id = "your_voice_id_here"
from playsound import playsound


import config
import RPi.GPIO as GPIO
import sys

from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont

import openai
from elevenlabs import generate, play, stream, voices, save
from elevenlabs import set_api_key


promptsFile = 'prompts.json'


def loadPrompts(filename):
    # Load the JSON data from a file
    with open(filename, 'r') as file:
        data = json.load(file)
        for e in data:
        	print(f"char: {e['character']} id: {e['id']}")
        	print(e["id"])


def saveTalk(str, voice_id):
  audiogen = generate(text =  str, voice=voice_id)
  print(f"playing {str} \n\n")
  save(audiogen,)



loadPrompts(promptsFile)