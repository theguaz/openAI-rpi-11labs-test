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

from RPi_GPIO_Rotary import rotary


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



# Array of items to select from
current_item = 0  # Start with the first item
projectFolder = '/home/pi/openAI-rpi-11labs-test/'
promptsFile = 'prompts.json'
items = []

CLK = 17
DT = 27
SW = 22 #THE BUTTON


#2e9f2738-4bf3-4b61-b2a6-aab341e2c2e7
#2e9f2738-4bf3-4b61-b2a6-aab341e2c2e7_answer.wav


def read_battery_soc(bus, address=0x32):
    try:
        # Open the I2C bus
        with smbus2.SMBus(bus) as smbus:
            # Read two bytes from the SOC register (0x04)
            # MAX17040G typically uses 2 bytes for SOC, with MSB first
            data = smbus.read_i2c_block_data(address, 0x04, 2)
            soc = (data[0] << 8 | data[1]) / 256  # Convert the 16-bit value to a percentage
            return soc
    except Exception as e:
        print(f"Error reading from UPS: {e}")
    return None

# OpenAI API Key

api_key = config.api_key
elevenLabsAPiKey = config.elevenLabsAPiKey


isProcessing = False


start_time = 0

promptsFile = 'prompts.json'
projectFolder = '/home/pi/openAI-rpi-11labs-test/'

set_api_key(elevenLabsAPiKey)

#thePrompt = "You're a character from a Guy Ritchie movie, you describe by creating a rhyme in shakespearerian style what you see on the image taken by the device it contains you. Take into account common sense and always stay respectful. You're reviewing images from your own point of view, answer as you were browsing social media. \n\nYou'll receive images one at a time, \n\nYou'll never answer with a question, this is a one time conversation with you\n\n It's very important that you begin each answer with a variation of this: \n 'Ok, this is what I see on the image ' "

def read_battery_soc(bus, address=0x32):
    try:
        # Open the I2C bus
        with smbus2.SMBus(bus) as smbus:
            # Read two bytes from the SOC register (0x04)
            # MAX17040G typically uses 2 bytes for SOC, with MSB first
            data = smbus.read_i2c_block_data(address, 0x04, 2)
            soc = (data[0] << 8 | data[1]) / 256  # Convert the 16-bit value to a percentage
            return soc
    except Exception as e:
        print(f"Error reading from UPS: {e}")
        return None

def load_and_select_random_prompt(filename):
    # Load the JSON data from a file
    with open(filename, 'r') as file:
        data = json.load(file)
    # Randomly select one of the prompts
    random_prompt = random.choice(data['prompts'])
    
    return random_prompt

def select_random_phrase(character):
    analysisPhrases = [
        "Analyzing image details",
        "Decoding visual data...",
        "Interpreting the pixels",
        "Rendering insights",
        "Examining the snapshot",
        "Unpacking image content",
        "Image analysis underway",
        "Breaking down the picture",
        "Reading visual information",
        "Fetching image details ",
        "Extracting data from image",
        "Converting image to insights",
        "Processing visual input",
        "Scanning image content",
        "Evaluating pictorial elements",
        "Assessing image composition",
        "Compiling image analysis",
        "Deriving insights from image",
        "Crunching image data",
        "Dissecting the frame"
    ]
    whoIM = random.choice(analysisPhrases) + ", like a  " + character + " ..."
    # Select a random phrase from the list
    return whoIM

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def save_log(message):
    with open("log.txt", "a") as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"{timestamp} - {message}\n")

def write_text_on_image(image_path, text, position=(10, 10), font_size=5, font_color="white"):

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

def getImageInfo(image_path, thePrompt):
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

def create_video_from_image_and_audio(image_path, audio_path, output_video_path):
    try:
        command = [
            'ffmpeg',
            '-loop', '1',
            '-framerate', '1',
            '-i', image_path,
            '-i', audio_path,
            '-c:v', 'libx264',
            '-tune', 'stillimage',
            '-c:a', 'aac',
            '-b:a', '192k',
            '-shortest',
            '-pix_fmt', 'yuv420p',
            output_video_path
        ]

        subprocess.run(command, check=True)
        print(f"Video created successfully: {output_video_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")

def capture_image(uuidID, save_dir="/home/pi/openAI-rpi-11labs-test/captures"):
    # Ensure the save directory exists
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Create a file name based on the current time
    file_name = uuidID + ".jpg"
    file_path = os.path.join(save_dir, file_name)

    # Capture the image
    with picamera.PiCamera() as camera:
        camera.resolution = (1280, 720)  # You can adjust the resolution
        camera.hflip = True
        camera.rotation = 90
        camera.start_preview()
        # Camera warm-up time
        print("warming camera")
        time.sleep(.25)
        camera.capture(file_path)
        print(f"Image captured and saved as {file_path}")

    return file_path

def process_image(filename, uuidID, prompt, voiceID):
  info = getImageInfo(filename, prompt)
  
  logInfo = filename + " ---> " + info + "\n\n"
  write_text_on_image(filename, logInfo)
  save_log(logInfo)
  print("generating audio with elevenLabs")
  encodedSTR = info.encode('utf-8')
  audiogen = generate(text =  encodedSTR, voice=voiceID)

  nameOf = uuidID
  
  input_audio_path = projectFolder + "audios/" + nameOf + '_answer.wav'
  print("playing msg \n\n")
  print("saving msg \n\n")
  save(audiogen, input_audio_path )
  
  return info , input_audio_path, audiogen


def justTalk(str, voice_id):
  encodedSTR = str.encode('utf-8')
  audiogen = generate(text =  encodedSTR, voice=voice_id)
  print(f"playing {str} \n\n")
  play(audiogen,)


def simpleMSG(thePrompt):
    headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": "gpt-4-turbo",
        "messages": [
          {
            "role": "user",
            "content": [
              {
                "type": "text",
                "text": thePrompt
              }
            ]
          }
        ],
        "temperature":1.15,
        "max_tokens":128,
        "top_p":1,
        "frequency_penalty":0,
        "presence_penalty":0
      }
    openAI_response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    msg = openAI_response.json()
    return msg['choices'][0]['message']['content']

def shootImage():

  playsound('/home/pi/openAI-rpi-11labs-test/shutter.wav')
  
  start_time = time.time()
  isProcessing = True
  print("shooting....")

  #selected_prompt = load_and_select_random_prompt(promptsFile)
  selected_prompt = items[current_item]

  uuidID = str( uuid.uuid4() )
  
  captured_image_path = capture_image(uuidID)

  justTalk( select_random_phrase(selected_prompt['character']), selected_prompt['id'] )

  process = process_image(captured_image_path, uuidID, selected_prompt['prompt'], selected_prompt['id'])
  
  #create_video_from_image_and_audio(captured_image_path, process[1], 'videos/' + uuidID + ".mp4" )
  
  end_time = time.time()
  elapsed_time = end_time - start_time
  print("task completed for UUID--> " + uuidID + " in exactly " + str(elapsed_time) + " secs")
  
  play(process[2])
  
  isProcessing = False


with open(projectFolder + promptsFile, 'r') as file:
    items = json.load(file)['prompts']


def tellpos():
    global current_item, currentFile, canread
    
    current_item %= len(items)  # Ensure the current_item index wraps around
    
    audio_id = items[current_item]['character'].replace(' ', '-')
    audio_id = audio_id.lower()

    currentFile = projectFolder + "init_audios/" +  + "_select.wav"
    print("Selected:", currentFile)
    print("current_item:", current_item)
    print("character selected:", items[current_item]['character'])
    playsound(currentFile)

def cwTurn():
    global current_item
    current_item += 1
    print("CW Turn")
    tellpos()

def ccwTurn():
    global current_item
    current_item -= 1
    print("CCW Turn")
    tellpos()

def buttonPushed():
    print("Button Pushed")
    shootImage()

def valueChanged(count):
    print(count)


## Initialise (clk, dt, sw, ticks)
obj = rotary.Rotary(CLK,DT,SW,2)

obj.register(increment=cwTurn, decrement=ccwTurn)
obj.register(pressed=buttonPushed, onchange=valueChanged)
obj.start()




if __name__ == "__main__":
    print("initializing persona camera")
    initialVoice  = load_and_select_random_prompt(promptsFile)["id"]
    
    bus_number = 1  # Raspberry Pi I2C bus 1
    battery_soc = read_battery_soc(bus_number)

    if battery_soc is not None:
        print(f"Battery SOC: {battery_soc:.2f}%")
    else:
        print("Could not read battery SOC.")
    
    justTalk( simpleMSG(f"You are an AI camera that sees the world with robotic eyes, now write a 20 words message in a playful tone like a joke, the message informs that you have internet access and you are ready to start analyzing images of anything around you, talk about the {battery_soc:.2f} percentage of battery you have right now. Make funny remarks every time about your energy level.\n\nNever use any special characters or emojis, be very very imaginative and funny, never forget you are an AI based camera, talk about that at the beginning of the answer\n") , initialVoice)

try:
    # Keep your main program running
    while True:
        time.sleep(0.1)  # Reduces CPU load
finally:
    GPIO.cleanup()  # Clean up GPIO on exit