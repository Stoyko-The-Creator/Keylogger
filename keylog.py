from pynput import mouse, keyboard
from time import time
import json
import os
#mouse listener, starts manually because otherwise the listeners would run sequentially instead of simulteaneously is a global so both can be stopped by escape key at once
mouse_listener = None
#declare start time globally so all callbacks can reference it
start_time = time()

unreleased_keys=[]
#storing all inputs
input_events=[]

OUTPUT_FILENAME= 'runefarm2'


class EventType():
    KEYDOWN = 'keyDown'
    KEYUP = 'keyUp'
    CLICK = 'click'
    MOVE = 'move'


def main():
    runListeners()
    print("Recording duration {} seconds.".format(elapsed_time()))
    global input_events
    print(json.dumps(input_events))
    
    script_dir = os.path.dirname(__file__)
    filepath= os.path.join(script_dir, 'recordings', '{}.json'.format(OUTPUT_FILENAME))
    
    with open(filepath, 'w') as outfile:
        json.dump(input_events, outfile, indent=4)
    
def elapsed_time():
    global start_time
    return time()-start_time

def record_event(event_type, event_time, button,pos=None):
    global input_events
    input_events.append({
    'time': event_time,
    'type':event_type,
    'button': str(button),
    'pos': pos})
    
def on_move(x, y):
    record_event(EventType.MOVE, elapsed_time(), None,(x,y))

def on_click(x, y, button, pressed):
    if not pressed:
        try:
            record_event(EventType.CLICK, elapsed_time(),button)
        except AttributeError:
            record_event(EventType.CLICK, elapsed_time(), button, pos)
      #  if not pressed:
            # Stop listener
       #     return False sdfasdfasdf
 
 
# asdsdfsd
 

    
def on_press(key):
    #we only want to record first key press and how long it was held. So we add it to unreleased_keys we can exit   sdfsdssasd
    global unreleased_keys
    if key in unreleased_keys:
        return
    else:
        unreleased_keys.append(key)
    
    try:
        record_event(EventType.KEYDOWN, elapsed_time(),key.char)
    except AttributeError:
        record_event(EventType.KEYDOWN, elapsed_time(), key)

def on_release(key):
    # remove the key from the golabl unreleased keys   asda
    global unreleased_keys
    try: 
        unreleased_keys.remove(key)
    except ValueError:
        print('ERROR: {} not in unreleased_keys '.format(key))
    try:
        record_event(EventType.KEYUP, elapsed_time(),key.char)
    except AttributeError:
        record_event(EventType.KEYUP, elapsed_time(), key)

    if key == keyboard.Key.esc:
        #Stop mouse listner
        global mouse_listener
        mouse_listener.stop()
        # Stop keyboard listener
        return False
    
def runListeners():
    global mouse_listener
    
    mouse_listener = mouse.Listener(on_click=on_click)# on_move=on_move)    Removed for now
    mouse_listener.start()
    mouse_listener.wait() # makes mouse_listener wait until the main listener is started
    #Simple Keyboard listener
    with keyboard.Listener( on_press=on_press,
            on_release=on_release) as listener:
        global start_time
        start_time=time()
        listener.join()
    
if __name__=="__main__":
    main()
