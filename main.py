import pyautogui
from PIL import Image, ImageGrab
from pytesseract import pytesseract
from playsound import playsound
import yaml
import time
import re
import tkinter as tk
from tkinter import StringVar

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
    #maybe in the future

    # Define path to tessaract.exe and Point tessaract_cmd to tessaract.exe
    path_to_tesseract = r'Tesseract-OCR\tesseract.exe'
    pytesseract.tesseract_cmd = path_to_tesseract

    # Extract text from image
    text = pytesseract.image_to_string(screenshot, config='--psm 6')

    # Remove incorrect characters
    current_time = re.sub('[^0-9:]+','',text)

    # Check if colon (:) is missing, and add it if it is
    if ":" not in current_time:
        if len(current_time) == 3:
            current_time = current_time[:1] + ":" + current_time[1:]
        elif len(current_time) == 4:
            current_time = current_time[:2] + ":" + current_time[2:]

    # Check if there are to many numbers
    # Assume the very first ones are incorrect and remove them
    if ":" in current_time:
        m, s = current_time.split(':')
        if len(m) > 2:
            m = m[len(m)-2:]
        current_time = m + ":" + s

    # Output the current time
    return current_time

# Get second from time
def get_seconds(time_str):
    """Get seconds from time."""
    m, s = time_str.split(':')
    return int(m) * 60 + int(s)

def find_next_timers(current_time, call_before):
    current_seconds = get_seconds(current_time)
    next_occurrences = []

    for i in range(1, timers["total_timers"] + 1):
        timer = timers[f"timer_{i}"]
        start_seconds = get_seconds(timer["start"])
        next_in_seconds = timer["next_in_seconds"]
        occurrence = timer["occurrence"]
        
        # Calculate the next occurrence
        time_since_start = current_seconds - start_seconds
        if time_since_start < 0:
            next_occurrence = start_seconds
        else:
            occurrences_passed = time_since_start // next_in_seconds
            if occurrence != -1 and occurrences_passed >= occurrence:
                continue
            next_occurrence = start_seconds + (occurrences_passed + 1) * next_in_seconds
        
        next_occurrences.append((next_occurrence, timer))

        # Add playsound feature
        # Skip callouts at 0:00
        if (get_seconds(current_time) + timers["call_before"] == 0):   
            continue
        # Not 0:00
        else:
            if (get_seconds(current_time) + timers["call_before"] - start_seconds) % next_in_seconds == 0:
                # Occurrence check
                if occurrence == -1 or (get_seconds(current_time) + timers["call_before"] - start_seconds) // next_in_seconds < occurrence:
                    # Write to console
                    print(timer['name'] + " soon. Playing " + timer['soundfile'])
                    # Play soundfile
                    playsound(f"resources/{timers['voice_pack']}/{timer['soundfile']}")


    # Find the minimum next occurrence time
    next_occurrences.sort(key=lambda x: x[0])
    next_time = next_occurrences[0][0]

    # Get all timers with this next occurrence time
    next_timers = [timer for occ_time, timer in next_occurrences if occ_time == next_time]

    return next_timers, next_time

def update_gui():
    global next_call_time, next_call_name

    # Get the current ingame time
    current_time = readIngameClock()

    # Check if a time could be read
    try:
        x = get_seconds(current_time)
    except:
        print("Failed to read ingame time")
        root.after(0, update_gui)  # Schedule the next call to update_gui immediately
        return

    # Write current time to console
    print("Ingame time: " + current_time)

    # Find the next timers
    next_timers, next_time = find_next_timers(current_time, timers["call_before"])
    
    # Set text for window
    if next_timers:
        next_call_text = "Next Call:\n - " + "\n- ".join([timer['name'] for timer in next_timers])
        next_call_name.set(next_call_text)
        next_call_time.set(f"At: {next_time // 60:02}:{next_time % 60:02}")

    # Wait 0.5s before checking again
    root.after(500, update_gui)

# Initialize Tkinter window
root = tk.Tk()
root.title("Dota 2 Coach")

# Set the window background to black
root.configure(bg='black')

# Set window transparency to 50%
root.attributes('-alpha', 1)

next_call_name = StringVar()
next_call_time = StringVar()

# Create a frame to hold the labels, making the frame transparent and labels opaque
frame = tk.Frame(root, bg='black')
frame.pack(pady=10, padx=100)

# Create labels with white text and a black background
label1 = tk.Label(frame, textvariable=next_call_name, font=("Helvetica", 16), fg="white", bg="black")
label2 = tk.Label(frame, textvariable=next_call_time, font=("Helvetica", 16), fg="white", bg="black")

label1.pack(pady=10)
label2.pack(pady=10)

# Start the GUI update loop
root.after(0, update_gui)

# Run the Tkinter main loop
root.mainloop()