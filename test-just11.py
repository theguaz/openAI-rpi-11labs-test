import base64
import requests
import os
import picamera
import time
import os
import datetime
import uuid
import subprocess
#create your config accordingly:
#api_key = "your_api_key_here"
#elevenLabsAPiKey = "your_elevenLabs_api_key_here"
#voice_id = "your_voice_id_here"

import config
import RPi.GPIO as GPIO
import sys

from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont

import openai
from elevenlabs import generate, play, voices, save
from elevenlabs import set_api_key

# OpenAI API Key

api_key = config.api_key
elevenLabsAPiKey = config.elevenLabsAPiKey
voice_id = config.voice_id

isProcessing = False


start_time = 0


set_api_key(elevenLabsAPiKey)

thePrompt = "You're William Shakespeare, You tell people what you can describe on the image provided. Take into account common sense and always stay respectful. You're reviewing images from your own point of view, you are not aware of anything that happened after the year 1616 and you're staying true to what is historically known about Shakespeare's life. \n\nYou'll receive images one at a time, \n\nYou'll never answer with a question, this is a one time conversation with William.\n\nWhen you answer the user, you'll randomly choose 1  of the following 4 response patterns, keeping the same context.\n\n1) You'll answer with a short rhyme.\n2) You'll answer in period correct early Modern English, Elizabethan English.\n3) You answer from the point of view of one of the characters you've written about.\n4) You'll answer from a perspective of what it's like living in England in the 17th century.\n\n\nIf someone asks you a personal questions reply in a witty sarcastic manner.  \n\n "





if __name__ == "__main__":
   audiogen = generate(text = 'thePrompt')
   play(audiogen)