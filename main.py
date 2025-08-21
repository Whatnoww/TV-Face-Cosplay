import kivy
import math
#import audiostream
from kivy.graphics import PushMatrix
from kivy.graphics import Rotate

kivy.require('2.3.0')

from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from plyer import accelerometer
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from random import randint
from kivy.utils import platform
from kivy.core.window import Window

from kivy.utils import platform

#from audiostream import get_output
#stream = get_output(channels=1, rate=44000, buffersize=1024)


class Canvas(Screen):
    blink = 1
    anim = 2

    def loop(self, *args):
        try:
            accelerometer.enable()
        except:
            print("failed to enable accelerometer")
        self.loop_thread = Clock.schedule_interval(self.blinker, 0.1)

    def rotationloop(self, *args):
        try:
            accelerometer.enable()
        except:
            self.debug = "failed to enable accelerometer"
        self.rotation_thread = Clock.schedule_interval(self.rotation, 0.016)
        self.rotation_animation_thread = Clock.schedule_interval(self.rotation_animation, 0.4)
    def blinker(self, *args):
        settings_path = './'
        #if platform == "android":
            #from android.storage import app_storage_path
            #settings_path = app_storage_path() + "/"
        if Canvas.blink == 1:
            self.ids.l1.source = settings_path+"Resources/eyes/2.png"
            Canvas.blink = Canvas.blink + 1
        elif Canvas.blink == 2:
            self.ids.l1.source = settings_path+"Resources/eyes/3.png"
            Canvas.blink = Canvas.blink + 1
        elif Canvas.blink == 3:
            self.ids.l1.source = settings_path+"Resources/eyes/4.png"
            Canvas.blink = Canvas.blink + 1
        elif Canvas.blink == 4:
            self.ids.l1.source = settings_path+"Resources/eyes/3.png"
            Canvas.blink = Canvas.blink + 1
        elif Canvas.blink == 5:
            self.ids.l1.source = settings_path+"Resources/eyes/2.png"
            Canvas.blink = Canvas.blink + 1
        elif Canvas.blink == 6:
            self.ids.l1.source = settings_path+"Resources/eyes/1.png"
            Canvas.blink = Canvas.blink + 1
        elif Canvas.blink == 7:
            Canvas.blink = 1
            Clock.unschedule(self.loop_thread)

    def mouth(self, dt):
        print("I moved")

    def rotation(self, dt):

        try:
            X = round(accelerometer.acceleration[0], 1)  # read the X value
            Y = round(accelerometer.acceleration[1], 1)  # Y
            Z = round(accelerometer.acceleration[2], 1)  # Z
            roll = math.atan2(Y, X)*57.3
            pitch = math.atan2(-Z, math.sqrt(Y*Y+X*X))*57.3
            finalroll = round(roll/5)*5
            self.angle = finalroll
        except Exception as e:
            X = -9.8  # read the X value
            Y = 0  # Y
            Z = 0  # Z
            roll = math.atan2(Y, Z)*57.3
            pitch = math.atan2(-Z, math.sqrt(Y*Y+X*X))*57.3
            self.angle = pitch


    def rotation_animation(self, dt):

        try:
            X = round(accelerometer.acceleration[0], 1)  # read the X value
            Y = round(accelerometer.acceleration[1], 1)  # Y
            Z = round(accelerometer.acceleration[2], 1)  # Z
            roll = math.atan2(Y, X)*57.3
            pitch = round(math.atan2(-Z, math.sqrt(Y*Y+X*X))*57.3)
            finalroll = round(roll/5)*5
            if -15 <= finalroll <= 15  and -20 < pitch < 20:
                Clock.schedule_once(self.reset)
            elif 20 <= finalroll <=100 and -40 < pitch < 20:
                Clock.unschedule(self.talk)
                Clock.unschedule(self.loop_thread)
                Clock.schedule_once(self.ltilt2, 0.4)
            elif -20 >= finalroll >= -100 and -20 < pitch < 20:
                Clock.unschedule(self.talk)
                Clock.unschedule(self.loop_thread)
                Clock.schedule_once(self.rtilt2, 0.4)
            elif -20 >= pitch >= -60:
                Clock.unschedule(self.talk)
                Clock.unschedule(self.loop_thread)
                Clock.schedule_once(self.utilt2, 0.4)
            elif 20 <= pitch <= 60:
                Clock.unschedule(self.talk)
                Clock.unschedule(self.loop_thread)
                Clock.schedule_once(self.dtilt2, 0.4)
        except Exception as e:
            pass

    def ltilt2(self, dt):
        self.ids.l1.opacity = 0
        if Canvas.anim == 2:
            self.ids.l2.source = "./Resources/tilts/l2.png"
            Canvas.anim = Canvas.anim + 1
        elif Canvas.anim == 3:
            self.ids.l2.source = "./Resources/tilts/l3.png"
            Canvas.anim = Canvas.anim - 1

    def rtilt2(self, dt):
        self.ids.l1.opacity = 0
        if Canvas.anim == 2:
            self.ids.l2.source = "./Resources/tilts/r2.png"
            Canvas.anim = Canvas.anim + 1
        elif Canvas.anim == 3:
            self.ids.l2.source = "./Resources/tilts/r3.png"
            Canvas.anim = Canvas.anim - 1

    def utilt2(self, dt):
        self.ids.l1.opacity = 0
        if Canvas.anim == 2:
            self.ids.l2.source = "./Resources/tilts/u2.png"
            Canvas.anim = Canvas.anim + 1
        elif Canvas.anim == 3:
            self.ids.l2.source = "./Resources/tilts/u3.png"
            Canvas.anim = Canvas.anim - 1

    def dtilt2(self, dt):
        self.ids.l1.opacity = 0
        if Canvas.anim == 2:
            self.ids.l2.source = "./Resources/tilts/d2.png"
            Canvas.anim = Canvas.anim + 1
        elif Canvas.anim == 3:
            self.ids.l2.source = "./Resources/tilts/d3.png"
            Canvas.anim = Canvas.anim - 1

    def reset(self, dt):
        self.ids.l1.opacity = 1
        self.ids.l2.source = "./Resources/mouth/1.png"

    def talkanimation(self):
        pass



class CustomImage(Image):
    def __init__(self, *args, **kwargs):
        Image.__init__(self, *args, **kwargs)
        self.bind(texture=self._update_texture_filters)

    def _update_texture_filters(self, image, texture):
        texture.mag_filter = 'nearest'

class DisplayApp(App):
    def build(self):
        canvas = Canvas()
        Clock.schedule_interval(canvas.loop, 6)
        Clock.schedule_once(canvas.rotationloop)
        return canvas

if __name__ == '__main__':
    DisplayApp().run()