import picamera
import time
import os

def capture_image(save_dir="/home/pi/captured_images"):
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

# Example usage
captured_image_path = capture_image()
print(f"Captured image path: {captured_image_path}")
