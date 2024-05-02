# Raspberry Pi Voice-Persona Camera

![cover image](https://github.com/theguaz/openAI-rpi-11labs-test/blob/main/portada.png?raw=true)

Welcome to my repository! I'm Luis Guajardo, a Senior Creative Technologist currently working at [Mediamonks LABS](https://labs.monks.com/), and this is not just any camera—it's a Raspberry Pi-based camera that narrates the content of images it captures using a variety of engaging voices and personas. Each persona offers a unique perspective and style, enriching the visual experience with dynamic, auditory feedback.

##About This Project
This idea began as a part of a demo at Mediamonks Labs where I explored the potential of virtual AI synthetic avatars for Twitch streaming. Inspired to push the boundaries of AI integration in practical devices, I adapted these cutting-edge technologies into this Raspberry Pi camera project. By leveraging OpenAI's Vision API for image analysis and elevenLabs' voice synthesis technology, the camera brings each captured scene to life with distinct narrative voices.

##From the Developer
⚠️ Please note: The setup instructions and deployment details are currently being finalized. I encourage you to experiment with the camera and share your feedback. Your insights are crucial to refining this project. Please let me know if you encounter any issues or if certain aspects of the project setup are unclear. I'm especially keen to hear your thoughts on potential new features or personas to include.

## Software and API Requirements

To get started with the Raspberry Pi Voice-Persona Camera, you'll need to install and configure several software tools and APIs. Here is a comprehensive list of what you'll need:

### Programming and APIs
- **Python**: This project is primarily developed in Python.
- **OpenAI API**: We utilize the OpenAI API for image recognition capabilities. You will need to create an account to access the API keys. [Sign up for OpenAI](https://www.openai.com/)
- **elevenLabs API**: This API is used for generating the synthetic voices for the camera's personas. Please create an account to obtain your API keys. [Register with elevenLabs](https://elevenlabs.io/)

### Modeling and Printing
- **Autodesk Fusion360**: This software is used for designing the physical case of the camera. If you plan to modify the case or need to view the designs, you'll need this installed. [Get Autodesk Fusion360](https://www.autodesk.com/products/fusion-360/overview)
- **Ultimaker Cura**: After designing your case, use Ultimaker Cura to slice the models for 3D printing. This is essential for preparing your print files. [Download Ultimaker Cura](https://ultimaker.com/software/ultimaker-cura)

### Setup and Installation
Follow the individual installation guides provided by each software to properly set up your development environment. Make sure to keep your API keys secure and only use them as described in the project documentation.




## Parts and bits
### 1. The brain: [Raspberry Pi Zero 2 W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/) with headers

I ordered a pre-soldered rpi with male headers so I could plug an Audio Interface to it 

### 2. 
  
    
### 3. Camera: 


### 4. Audio Interface (s)
I used teh Audio AMP Shim because it does not add much bulk and it also has no solder friction fit header:) 
[PIMORONI](https://shop.pimoroni.com/products/audio-amp-shim-3w-mono-amp?variant=32341591064659)

### 5. Rpi UPS:
[A sleek UPS with battery and micro usb connector](https://www.amazon.nl/gp/product/B0BQ3X2W2S/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1)


### 6. Speaker
[Speaker with the almost same dimensions as the rpi zero](https://www.amazon.nl/gp/product/B0822Z4LPH/ref=ppx_yo_dt_b_asin_title_o03_s00?ie=UTF8&psc=1)


### 7. 3D printed case

## How It works

Currently, the `main.py` script running on the Pi:
- Select a voice using the encoder
- Takes a photo when you click the encoder button
- Sends the photo to GPT-4 for analysis based on prompt and gets a string with AI-generated answer
- Send string to eleven labs with the selected voice as option
- Play the answer using the speaker


## How to set up

1 - Connect to your pi (use a keyboard & monitor or just SSH into it) and update the system on your rpi:
```shell
$ sudo apt-get update
$ sudo apt-get install git cups build-essential libcups2-dev libcupsimage2-dev python3-serial python-pil python-unidecode
```

2. Clone this repo, install python modules:
```shell
$ cd
$ git clone https://github.com/theguaz/openAI-rpi-11labs-test.git
$ cd openAI-rpi-11labs-test 
$ pip install -r requirements.txt

```

3. Connect the Audio interface and setup:
Plug the interface and connect a speaker to it, then follow the instructions from [Pimoroni website](https://shop.pimoroni.com/products/audio-amp-shim-3w-mono-amp?variant=32341591064659):
```shell
git clone https://github.com/pimoroni/pirate-audio
cd pirate-audio/mopidy
sudo ./install.sh 
```
Test your speaker:
```shell
speaker-test -c2 -twav -l7
```

4. Connect and set the camera:


5. Create your credentials file, for security I have not included any API keys, so what is expected in main.py is to get the credentials from a config.py file located at the same level as the main file, to do this you need to get your openAI Api key and Eleven labs key and paste them inside your config file:
```shell

sudo nano config.py

#paste this then replace values:
api_key = "my_key_xxxxxxxxxxxxxx"
elevenLabsAPiKey = "my_key_xxxxxxxxxxxxxx"

#ctrl+X to save

```

6. Test your API keys :


7. Run the poetry camera script.
```shell
$ python main.py
```

## TODO instructions for connect everything
