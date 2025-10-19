import time
import pydirectinput

def moveRel(x, y, duration):
    if(float(duration) == 0.0):
        pydirectinput.moveRel(x, y)
    else:
        current_x, current_y = pydirectinput.position()
        step_x = x / int(duration / 0.01)
        step_y = y / int(duration / 0.01)
        for i in range(int(duration / 0.01)):
            current_x += step_x
            current_y += step_y
            pydirectinput.moveTo(int(current_x), int(current_y))
            time.sleep(0.01)