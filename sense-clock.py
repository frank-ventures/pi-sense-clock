#!/usr/bin/env python
# Lovingly taken from https://pimylifeup.com/raspberry-pi-sense-hat-digital-clock/

# The current code runs permanently. This allows us to see a blinking seconds display.
# A more power efficient version would be to only have the minutes display, 
# and to run a cronjob for this script on the system.

from sense_hat import SenseHat
import time

sense = SenseHat()

# Numbers to display
number = [
[[0,1,1,1], # Zero
[0,1,0,1],
[0,1,0,1],
[0,1,1,1]],
[[0,0,1,0], # One
[0,1,1,0],
[0,0,1,0],
[0,1,1,1]],
[[0,1,1,1], # Two
[0,0,1,1],
[0,1,1,0],
[0,1,1,1]],
[[0,1,1,1], # Three
[0,0,1,1],
[0,0,1,1],
[0,1,1,1]],
[[0,1,0,1], # Four
[0,1,1,1],
[0,0,0,1],
[0,0,0,1]],
[[0,1,1,1], # Five
[0,1,1,0],
[0,0,1,1],
[0,1,1,1]],
[[0,1,0,0], # Six
[0,1,1,1],
[0,1,0,1],
[0,1,1,1]],
[[0,1,1,1], # Seven
[0,0,0,1],
[0,0,1,0],
[0,1,0,0]],
[[0,1,1,1], # Eight
[0,1,1,1],
[0,1,1,1],
[0,1,1,1]],
[[0,1,1,1], # Nine
[0,1,0,1],
[0,1,1,1],
[0,0,0,1]]
]
noNumber = [0,0,0,0]

# Colours
hourColor = [0,255,0] # Green
minuteColor = [0,255,255] # Cyan
secondColour = [255, 255, 0] # Yellow
empty = [0,0,0] # Black/Off


def createTime():
  # Reset the image being displayed
  clockImage = []

  hour = time.localtime().tm_hour
  minute = time.localtime().tm_min

  for index in range(0, 4):
      if (hour >= 10):
          clockImage.extend(number[int(hour/10)][index])
      else:
          clockImage.extend(noNumber)
      clockImage.extend(number[int(hour%10)][index])
  
  for index in range(0, 4):
      clockImage.extend(number[int(minute/10)][index])
      clockImage.extend(number[int(minute%10)][index])
  
  for index in range(0, 64):
      if (clockImage[index]):
          if index < 32:
              clockImage[index] = hourColor
          else:
              clockImage[index] = minuteColor
      else:
          clockImage[index] = empty
  # Export the time to be displayed
  return clockImage
          



def set_left_strip():
    second = time.localtime().tm_sec
    # Calculates how many LEDs should be on
    leds_on = min(second // 10 + 1, 6)  
    
    for i in range(1, 7):  # LEDs 2 to 7 (index 1 to 6)
        if i < leds_on:
            sense.set_pixel(0, i, secondColour)
            sense.set_pixel(4, i, secondColour)
        elif i == leds_on and blink_on:
            sense.set_pixel(0, i, secondColour)
            sense.set_pixel(4, i, secondColour)
        else:
            sense.set_pixel(0, i, empty)
            sense.set_pixel(4, i, empty)

# Initialise blink state
blink_on = False

while True:
    clockImage = createTime()
    sense.set_rotation(0) # Optionally rotates the time display if you need to
    sense.low_light = True # Optionally dims the LEDs if its too bright
    sense.set_pixels(clockImage)
    
    set_left_strip()
    # Reverse the blink state
    blink_on = not blink_on
    
    time.sleep(1)  # Update every half second for smoother blinking
