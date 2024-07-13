import keyboard
import time
import json
import os


current_dir = os.getcwd()
file_path = os.path.join(current_dir, "kp.json") 
recorded_dicts = []
recorded =None
record= None
runes_amt = 0

def dict_to_event(event_dict):
        return keyboard.KeyboardEvent(
            event_type=event_dict["event_type"],
            scan_code=event_dict["scan_code"],
            name=event_dict["name"],
            time=event_dict["time"],
            device=event_dict.get("device"),
            modifiers=event_dict.get("modifiers", [])
        )

def event_to_dict(event):
    if event.name != "esc":
        return {
            "event_type": event.event_type,
            "name": event.name,
            "scan_code": event.scan_code,
            "time": event.time,
            "device": event.device,
            "modifiers": event.modifiers
        }

def countdown():
     count = 3
     while count > 0:
        print(count)
        count -= 1
        time.sleep(1)

def get_input():
    global record
    record = input("Record new keys?: y/n ").lower()


while record != "n" or record != "y":
    get_input()
    if record == "y" or record == "n":
         break
   

def load_file():
        global recorded_dicts
        try:
            with open(file_path, "r") as file:
                recorded_dicts = json.load(file)
        except (FileNotFoundError, IOError) as e:
            print(f"Failed to load file: {e}")
        return None


def play_rec():
    global runes_amt
    recorded_events = [dict_to_event(event) for event in recorded_dicts]

    if recorded_events:
        while recorded_events: 
            start_time = recorded_events[0].time 
            for event in recorded_events:
                if keyboard.is_pressed('esc'):
                    break
                time.sleep(event.time - start_time)
                if event.event_type == 'down':
                    keyboard.press(event.name)
                elif event.event_type == 'up':
                    keyboard.release(event.name)
                start_time = event.time
            if keyboard.is_pressed('esc'):
                print("stopping...")
                break
            runes_amt = runes_amt + 36000
            print(f"approximate rune farmed: ~{runes_amt}")
        
    else:
        print("No events to play.")

if record == "y":
    countdown()
    print("Go")
    recorded = keyboard.record(until='esc')

    if recorded:

        recorded_dicts = [event_to_dict(event) for event in recorded]

        with open(file_path, "w") as file:
            json.dump(recorded_dicts, file, indent=4)
    
        print("saved")
    time.sleep(1)
    
else:
    load_file()
    print("file loaded")
    countdown()
    print("playing file")
    play_rec()
   


    