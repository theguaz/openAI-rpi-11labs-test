import base64
import requests
import os
import picamera
import time
import os
import datetime
import uuid

#create your config accordingly:
#api_key = "your_api_key_here"
#elevenLabsAPiKey = "your_elevenLabs_api_key_here"
#voice_id = "your_voice_id_here"

import config

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


set_api_key(elevenLabsAPiKey)

thePrompt = "You're William Shakespeare, You tell people what you can describe on the image provided. Take into account common sense and always stay respectful. You're reviewing images from your own point of view, you are not aware of anything that happened after the year 1616 and you're staying true to what is historically known about Shakespeare's life. \n\nYou'll receive images one at a time, \n\nYou'll never answer with a question, this is a one time conversation with William.\n\nWhen you answer the user, you'll randomly choose 1  of the following 4 response patterns, keeping the same context.\n\n1) You'll answer with a short rhyme.\n2) You'll answer in period correct early Modern English, Elizabethan English.\n3) You answer from the point of view of one of the characters you've written about.\n4) You'll answer from a perspective of what it's like living in England in the 17th century.\n\n\nIf someone asks you a personal questions reply in a witty sarcastic manner.  \n\n "

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def save_log(message):
    with open("log.txt", "a") as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"{timestamp} - {message}\n")

def write_text_on_image(image_path, text, position=(10, 10), font_size=75, font_color="red"):

    try:
        # Open the image
        with Image.open(image_path) as img:
            # Create a drawing context
            draw = ImageDraw.Draw(img)

            # Load a font
            #font = ImageFont.truetype("arial.ttf", font_size)

            # Add text to image
            draw.text(position, text, fill=font_color)

            # Save the image
            img.save(image_path)

    except IOError as e:
        print(f"Error opening or processing the image: {e}")

def getImageInfo(image_path):
    base64_image = encode_image(image_path)
    print("asking open ai for --->", {image_path})
    headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {api_key}"
    }
    payload = {
      "model": "gpt-4-vision-preview",
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": thePrompt
            },
            {
              "type": "image_url",
              "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
              }
            }
          ]
        }
      ],
      "max_tokens": 1024
    }
    openAI_response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    print(openAI_response.json())
    msg = openAI_response.json()
    return msg['choices'][0]['message']['content']

def capture_image(save_dir="/home/pi/openAI-rpi-11labs-test/captures"):
    # Ensure the save directory exists
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Create a file name based on the current time
    file_name = time.strftime("%Y%m%d-%H%M%S") + ".jpg"
    file_path = os.path.join(save_dir, file_name)

    # Capture the image
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)  # You can adjust the resolution
        camera.start_preview()
        # Camera warm-up time
        time.sleep(2)
        camera.capture(file_path)
        print(f"Image captured and saved as {file_path}")

    return file_path

def process_image(filename):
  info = getImageInfo(filename)
  logInfo = filename + " ---> " + info + "\n\n"
  write_text_on_image(filename, logInfo)
  save_log(logInfo)
  print("generating audio with elevenLabs")
  audiogen = generate(text = 'Ok, this is what I see on the image:' + info, voice=voice_id)
  

  nameOf = str( uuid.uuid4() )
  print("saving voice \n\n")
  input_audio_path = nameOf + '_answer.wav'
  play(audiogen)
  save(audiogen, input_audio_path )
  return info , input_audio_path

if __name__ == "__main__":
    captured_image_path = capture_image()
    process = process_image(captured_image_path)