import RPi.GPIO as gpio
import time

class Controls:
    def __init__(self):
        self.pinout = []
        self.pinout.append([17, 27])
        self.pinout.append([22, 10])
        self.pinout.append([9, 11])
        self.pinout.append([0, 5])
        gpio.cleanup()
        gpio.setmode(gpio.BCM)
        for i in range(len(self.pinout)):
            gpio.setup(self.pinout[i][0], gpio.OUT)
            gpio.output(self.pinout[i][0], gpio.LOW)
            gpio.setup(self.pinout[i][1], gpio.OUT)
            gpio.output(self.pinout[i][1], gpio.LOW)
            
    def __del__(self):
        #self.reset_all()
        gpio.cleanup()

    def move_forward(self, box_pins):
        gpio.output(box_pins[0], gpio.HIGH)
        gpio.output(box_pins[1], gpio.LOW)
        time.sleep(1)

    def move_backward(self, box_pins):
        gpio.output(box_pins[0], gpio.LOW)
        gpio.output(box_pins[1], gpio.HIGH)
        time.sleep(1)
        
    def reset(self, box_pins):
        gpio.output(box_pins[0], gpio.LOW)
        gpio.output(box_pins[1], gpio.LOW)
        time.sleep(1)
        
    def reset_all(self):
        for i in range(len(self.pinout)):
            gpio.output(self.pinout[i][0], gpio.LOW)
            gpio.output(self.pinout[i][1], gpio.LOW)
            
    def move_box(self, box_num):
        time.sleep(0.2)
        self.move_forward(self.pinout[box_num])
        #self.reset(self.pinout[box_num])
        self.move_backward(self.pinout[box_num])
        self.reset(self.pinout[box_num])


