import pyautogui
from PIL import Image, ImageGrab
from pytesseract import pytesseract
from playsound import playsound
import yaml
import time
import re

# screen resolution
screenWidth, screenHeight = pyautogui.size()

# Timers
with open("resources/timers.yaml", "r") as yamlfile:
    timers = yaml.safe_load(yamlfile)

def readIngameClock():
    # screenshot creation
    screenshot = ImageGrab.grab(bbox=(screenWidth/2 - 50, 20, screenWidth/2 + 50, 50))
    #screenshot.save("screenshot.png", 'PNG')

    # Image Optimizations
    # maybe in the future

    # Define path to tessaract.exe and Point tessaract_cmd to tessaract.exe
    path_to_tesseract = r'Tesseract-OCR\tesseract.exe'
    pytesseract.tesseract_cmd = path_to_tesseract

    # Extract text from image
    text = pytesseract.image_to_string(screenshot, config='--psm 6')
    
    # Remove incorrect characters
    current_time = text.replace(" ","").replace("\n","").replace("_","").replace("—","").replace("-","").replace("~","").replace("\\","").replace(".","").replace(",","").replace(";",":").replace("#","").replace("+","")
    current_time = re.sub('[a-zA-Z]','',current_time)

    # Check if colon (:) is missing, and add it if it is
    if ":" not in current_time:
        if len(current_time) == 3:
            current_time = current_time[:1] + ":" + current_time[1:]
        elif len(current_time) == 4:
            current_time = current_time[:2] + ":" + current_time[2:]

    # Output the current time
    return current_time

# Get second from time
def get_seconds(time_str):
    """Get seconds from time."""
    m, s = time_str.split(':')
    return int(m) * 60 + int(s)

while(1):
    # Get the current ingame time
    current_time = readIngameClock()
    
    # Write current time to console
    print(current_time)

    # Check if a time could be read
    try:
        x = get_seconds(current_time) 
    except:
        continue

    # Check if any timers match
    for i in range(1, timers["total_timers"]+1):
        # Skip callouts at 0
        if get_seconds(current_time) + timers["call_before"] == 0:
            continue
        # Else not the first occurnec
        else:
            if (get_seconds(current_time) + timers["call_before"] - get_seconds(timers[f"timer_{i}"]["start"])) % timers[f"timer_{i}"]["next_in_seconds"] == 0:
                # Occurence check
                if timers[f"timer_{i}"]["occurrence"] == -1 or (get_seconds(current_time) + timers["call_before"] - get_seconds(timers[f"timer_{i}"]["start"])) / timers[f"timer_{i}"]["next_in_seconds"] <= timers[f"timer_{i}"]["occurrence"]:
                    # Write to console
                    print(timers[f'timer_{i}']['name'] + " soon. Playing "+ timers[f'timer_{i}']['soundfile'])

                    # Play soundfile
                    playsound(f"resources/{timers[f'voice_pack']}/{timers[f'timer_{i}']['soundfile']}")
    
    # Wait 0.5s before checking again
    time.sleep(0.5)
