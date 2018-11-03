#@author Ilana Shapiro, updated spring 2018
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import *
from kivy.properties import *
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader
from kivy.base import EventLoopBase
from kivy.event import EventDispatcher
from kivy.animation import Animation
from kivy.clock import Clock
from datetime import datetime
from functools import partial
import random, time, threading, os
from threading import Thread


import sys


#create a screenmanager for the UI, and set the background window color to white
sm = ScreenManager()
Window.clearcolor = (.95, .95, .95, 1) #background white




#define the class for the first scene in the UI, which (in the Kivy code)
# allows for song selection
class SongSelectionScene(Screen):
    def getWindowWidth(self):
        return Window.width

    def getWindowHeight(self):
        return Window.height

    def quitUI(self):
        quit()


#define the class for the second  scene in the UI, which (in the Kivy code) will display the beats of the song currently playing in the background as scrolling rectangles;
# a dynamic graphic of the current guitar fret (with the strings in use lit up) that also includes the finger numbers for that chord;
# and a triangle in the bottom center of the screen that changes color when a beat hits it, indicating that the user should strum the guitar at this time
class AnimateScene(Screen):
    #beat_1, triangle, and triangle are of type ObjectProperty, which means they are of any object type, therefore they can be assigned to any object of any kind later in the code
    #in these cases, in the kivy code, beat_1, triangle, and toggle are assigned to be different labels in the kivy. See the kivy for more instructions
    beat_1 = ObjectProperty(None)
    triangle = ObjectProperty(None)
    toggle = ObjectProperty(None)

    #r, g, b are variables of type NumericProperty, which means they can later be assigned to any integer or float. Right now, they're all initialized to 0
    r = NumericProperty(0)
    g = NumericProperty(0)
    b = NumericProperty(0)


    E1g = NumericProperty(0)
    A2g = NumericProperty(0)
    D3g = NumericProperty(0)
    G4g = NumericProperty(0)
    B5g = NumericProperty(0)
    E6g = NumericProperty(0)

#the following are variables of type StringProperty, which means they can later be assigned to any string. Right now, they're all initialized to empty strings
    E1text = StringProperty('')
    A2text = StringProperty('')
    D3text = StringProperty('')
    G4text = StringProperty('')
    B5text = StringProperty('')
    E6text = StringProperty('')

    textArray = ['', '', '', '', '', '']
    colorArray = [0, 0, 0, 0, 0, 0]

    animationState = False
    start_time = 0
    index = 0
    pathSize = 0
    tupleNum = 0



    fileName = ""

#constructor for AnimateScene. the song that will play in the background is loaded here
    def __init__(self, name, pathToSong, fileName, **kwargs):

        self.name = name
        self.pathToSong = pathToSong
        self.fileName = pathToSong
        self.audioFile = SoundLoader.load(pathToSong)
        self.pathSize = os.path.getsize(self.pathToSong)
        super(Screen, self).__init__()

    def doNothing(self, *args):
        pass

    def playJingleBells(self):
        self.animate()

    #the following access the width and height of the current screen using the width and height properties of the Window object. These methods are used in the Kivy and below in other Python methods for positioning
    def getWindowWidth(self):
        return Window.width

    def getWindowHeight(self):
        return Window.height


    #plays the song
    def playSound(self, *args):
        self.audioFile.play()


    def start(self, *args):
        self.animationState = True

#if the song is not already running, start the song after a delay based on the size of the file to coordinate with the guitar's pistons pressing down the chord

        if(self.name == "amazon"):
            t = threading.Timer(0, self.playSound)
            t.start()

        # if(self.index == 1):
        #    self.playSound()



#set r, g, b to random values between 0 and 1, which will later be used for colors in the UI
        self.r = random.uniform(0.0, 1.0)
        self.g = random.uniform(0.0, 1.0)
        self.b = random.uniform(0.0, 1.0)



#sets the following NumericPropertes defined above to be the corresponding values (0 or 1) of the array colorArray
#below, in the Kivy, a value of zero means the corresponding graphic of the guitar string on the UI stays black (is not being fingered), and a value of 1 means the guitar string on the UI lights up green (indicating it is being fingered)
        self.E1g = self.colorArray[0]
        self.A2g = self.colorArray[1]
        self.D3g = self.colorArray[2]
        self.G4g = self.colorArray[3]
        self.B5g = self.colorArray[4]
        self.E6g = self.colorArray[5]

#sets the following StringProperties defined above to be the corresponding string values (which are numbers indidcating the fret poisition for the piston fingering the string) of the array textArray
#if the string is being pressed, the number will appear above the green lit-up string to indicate the fret position of the piston "finger" on that string
        self.E1text = self.textArray[0]
        self.A2text = self.textArray[1]
        self.D3text = self.textArray[2]
        self.G4text = self.textArray[3]
        self.B5text = self.textArray[4]
        self.E6text = self.textArray[5]

#this next section takes care of the animation of the recangle "beats" scrolling across the screen in time to the rhythm of the music
#it calculates the time each beat will take to scroll across the screen (this will be different for each beat)
#if the current mode is play = "p" for that beat (Defined in the tuples in the beats arrays), then the rectangle representing the beat will scroll across the screen
#if the current mode is rest = "r", then the rectangle will not scroll across the screen and an empty graphic will take its place for that time slot
        # if(self.index < len(self.beats)):
        #     self.beatTime = 1/(self.bpm * self.beats[self.index][0])
        #     if(tuple[4] == "p"):
        #         self.animation = Animation(x=self.getWindowWidth()/2, y=0, duration=self.beatTime)
        #         self.animation += Animation(size=(0, 0), duration=0.0)
        #         self.animation += Animation(x=self.getWindowWidth(), y=0, duration=0.0)
        #         self.animation += Animation(size=(10, self.getWindowHeight()), duration=0.0)
        #     elif(tuple[4] == "r"):
        #         self.animation = Animation(size=(0, 0), duration=0.0)
        #         self.animation += Animation(x=self.getWindowWidth(), y=0, duration=self.beatTime)
        #         self.animation += Animation(size=(10, self.getWindowHeight()), duration=0.0)
        #     else:
        #         print("ERROR IN PLAY STATE")
        #         quit()
            #print(self.beatTime)

#start the animation and run this method again when each animation completes
#"runNextFrame" takes place over a single song beat and a single chord
            # self.animation.start(self.beat_1)
            # self.animation.bind(on_complete = self.runNextFrame)
            #
            # self.index += 1
            # self.tupleNum += 1


#stop the song, the animation, set all the strings in the guitar tab graphic to black (implemented later in the Kivy), set all the tab text to empty strings, and home the carriage motor
    def stopSong(self):
        if(self.audioFile.state == 'play'):
            self.audioFile.stop()


    def quitUI(self):
        quit()



Builder.load_string("""
<EcosystemSelectionScene>:
    name: 'song_selection'
    FloatLayout:
        size_hint: None, None  #Needed to be able to define define height and width of widgets
        Label:
            size: 400, 100
            id: selection
            size_hint: None,None
            center_x: root.center_x
            center_y: root.center_y * 1.8
            font_size: 75
            text: 'Song Selection'
            color: 0.5, 0, 1, 1

        Button:
            size_hint: None,None
            text: 'Amazon'
            font_size: 40
            size: 500, 60
            background_color: 0.4, 0, 0.5, 0.8
            center: root.center_x, root.center_y * (3/3)
            on_release:
                root.manager.transition.direction = 'left'
                root.manager.current = 'amazon'

        Button:
            text: 'Exit'
            font_size: 40
            size: root.getWindowWidth()/20, root.getWindowWidth()/40
            center_x: root.center_x/5
            center_y: root.center_y/1.5
            background_color: 0, 0, 0, 1
        #start the animation by pressing the button
            on_release:
                root.quitUI()
<AnimateScene>:
    #assign the ObjectProperty beat_1 defined above in the Python to the id _beat_1, which belongs to the rectangular label a few lines down. You can do this because variables of type ObjectProperty can refer to any object
    beat_1: _beat_1

    #assign the ObjectProperty triangle defined above in the Python to the id _triangle, which belongs to the triangular label a few lines down
    triangle: _triangle
    toggle: _toggle
    FloatLayout:
        size_hint: None, None  #Needed to be able to define define height and width of widgets

        #the beat that will scroll across the screen in each frame
        Label:
            #assign the id _beat_1 to this label
            id: _beat_1
            size_hint: None,None
            size: 10, root.getWindowHeight()
            center_x: root.center_x*2
            center_y: root.center_y
            #use canvas to "re-draw" the label as a solid rectangle, giving it color and fill which it wouldn't normally have
            canvas:
                #gives the label a red color
                Color:
                    rgba: 0,0.5,0.75,1
                #re-draws the label, custom, to be a rectangle of the size and position defined right above canvas. It does this b referencing the label's id, _beat_1, which you can think of being "a level above the canvas" (like how the canvas is another layer of definion because it's indented more, etc, so you can access _beat_1's properties directly from canvas without the id)
                Rectangle
                    pos: _beat_1.pos
                    size: _beat_1.size


        #THE FOLLOWING LABELS CREATE THE GRAPHIC OF THE GUITAR TAB IN THE UPPER LEFT PART OF THE SCREEN, UPDATED DYNAMICALLY TO REFLECT CHORD AND FINGER POSITION
        Label:
            id: _E1
            size_hint: None,None
            size: 200, 3
            center_x: root.center_x / 2
            center_y: 3 * root.center_y / 7 + root.center_y / 2
            #use canvas to "re-draw" the label as a solid rectangle, giving it color and fill which it wouldn't normally have
            canvas:
                Color:
                    rgba: 0, root.E1g, 0, 1 #this graphic representing a guitar string will turn green when E1g has a value of 1 (defined above in runNextFrame)
                Rectangle
                    pos: _E1.pos
                    size: _E1.size
        Label:
            id: _A2
            size_hint: None,None
            size: 200, 3
            center_x: root.center_x / 2
            center_y: 4 * root.center_y / 7 + root.center_y / 2
            #use canvas to "re-draw" the label as a solid rectangle, giving it color and fill which it wouldn't normally have
            canvas:
                Color:
                    rgba: 0, root.A2g, 0, 1 #this graphic representing a guitar string will turn green when A2g has a value of 1 (defined above in runNextFrame)
                Rectangle
                    pos: _A2.pos
                    size: _A2.size
        Label:
            #assign the id _beat_1 to this label
            id: _D3
            size_hint: None,None
            size: 200, 3
            center_x: root.center_x / 2
            center_y: 5 * root.center_y / 7  + root.center_y / 2
            #use canvas to "re-draw" the label as a solid rectangle, giving it color and fill which it wouldn't normally have
            canvas:
                Color:
                    rgba: 0, root.D3g, 0, 1 #this graphic representing a guitar string will turn green when D3g has a value of 1 (defined above in runNextFrame)
                Rectangle
                    pos: _D3.pos
                    size: _D3.size
        Label:
            #assign the id _beat_1 to this label
            id: _G4
            size_hint: None,None
            size: 200, 3
            center_x: root.center_x / 2
            center_y: 6 * root.center_y / 7  + root.center_y / 2
            #use canvas to "re-draw" the label as a solid rectangle, giving it color and fill which it wouldn't normally have
            canvas:
                Color:
                    rgba: 0, root.G4g, 0, 1 #this graphic representing a guitar string will turn green when G4g has a value of 1 (defined above in runNextFrame)
                Rectangle
                    pos: _G4.pos
                    size: _G4.size
        Label:
            #assign the id _beat_1 to this label
            id: _B5
            size_hint: None,None
            size: 200, 3
            center_x: root.center_x / 2
            center_y: 7 * root.center_y / 7  + root.center_y / 2
            #use canvas to "re-draw" the label as a solid rectangle, giving it color and fill which it wouldn't normally have
            canvas:
                Color:
                    rgba: 0, root.B5g, 0, 1 #this graphic representing a guitar string will turn green when B5g has a value of 1 (defined above in runNextFrame)
                Rectangle
                    pos: _B5.pos
                    size: _B5.size
        Label:
            id: _E6
            size_hint: None,None
            size: 200, 3
            center_x: root.center_x / 2
            center_y: 8 * root.center_y / 7 + root.center_y / 2
            #use canvas to "re-draw" the label as a solid rectangle, giving it color and fill which it wouldn't normally have
            canvas:
                Color:
                    rgba: 0, root.E6g, 0, 1 #this graphic representing a guitar string will turn green when E6g has a value of 1 (defined above in runNextFrame)
                Rectangle
                    pos: _E6.pos
                    size: _E6.size


    #THE FOLLOWING LABELS IMPLEMENT THE TEXT THAT WILL BE SHOWN ABOVE EACH STRING IN THE GUITAR TAB GRAPHIC, UPDATED DYNICALLY. THE TEXT IS NUMBERS THAT INDICATE FINGER POSITION OF THE FRETS FOR THE CURRENT CHORD
        Label:
            size_hint: None,None
            size: 50, 50
            text: 'E'
            color: 0, 0, 0, 1
            font_size: 25
            center_x: root.center_x / 4.4
            center_y: 3 * root.center_y / 7 + root.center_y / 2
        Label:
            size_hint: None,None
            size: 50, 50
            text: 'A'
            color: 0, 0, 0, 1
            font_size: 25
            center_x: root.center_x / 4.4
            center_y: 4 * root.center_y / 7 + root.center_y / 2
        Label:
            size_hint: None,None
            size: 50, 50
            text: 'D'
            color: 0, 0, 0, 1
            font_size: 25
            center_x: root.center_x / 4.4
            center_y: 5 * root.center_y / 7 + root.center_y / 2
        Label:
            size_hint: None,None
            size: 50, 50
            text: 'G'
            color: 0, 0, 0, 1
            font_size: 25
            center_x: root.center_x / 4.4
            center_y: 6 * root.center_y / 7 + root.center_y / 2
        Label:
            size_hint: None,None
            size: 50, 50
            text: 'B'
            color: 0, 0, 0, 1
            font_size: 25
            center_x: root.center_x / 4.4
            center_y: 7 * root.center_y / 7 + root.center_y / 2
        Label:
            size_hint: None,None
            size: 50, 50
            text: 'E'
            color: 0, 0, 0, 1
            font_size: 25
            center_x: root.center_x / 4.4
            center_y: 8 * root.center_y / 7 + root.center_y / 2
        Label:
            id: _E1text
            size_hint: None,None
            size: 50, 50
            text: root.E1text
            color: 0, 0, 0, 1
            font_size: 25
            center_x: root.center_x / 2
            center_y: 3 * root.center_y / 7 + root.center_y / 2
        Label:
            id: _A2text
            size_hint: None,None
            size: 50, 50
            text: root.A2text
            color: 0, 0, 0, 1
            font_size: 25
            center_x: root.center_x / 2
            center_y: 4 * root.center_y / 7 + root.center_y / 2
        Label:
            id: _D3text
            size_hint: None,None
            size: 50, 50
            text: root.D3text
            color: 0, 0, 0, 1
            font_size: 25
            center_x: root.center_x / 2
            center_y: 5 * root.center_y / 7 + root.center_y / 2
        Label:
            id: _G4text
            size_hint: None,None
            size: 50, 50
            text: root.G4text
            color: 0, 0, 0, 1
            font_size: 25
            center_x: root.center_x / 2
            center_y: 6 * root.center_y / 7 + root.center_y / 2
        Label:
            id: _B5text
            size_hint: None,None
            size: 50, 50
            text: root.B5text
            color: 0, 0, 0, 1
            font_size: 25
            center_x: root.center_x / 2
            center_y: 7 * root.center_y / 7 + root.center_y / 2
        Label:
            id: _E6text
            size_hint: None,None
            size: 50, 50
            text: root.E6text
            color: 0, 0, 0, 1
            font_size: 25
            center_x: root.center_x / 2
            center_y: 8 * root.center_y / 7 + root.center_y / 2




    #THE FOLLOWING LABEL CREATES THE TWO VERTICAL LINES THAT FORM THE LEFT AND RIGHT BOUNDARIES OF THE GUITAR TAB GRAPHIC (E.G. "ENCLOSES" THE 6 STRINGS IN THE GRAPHIC)
        Label:
            id: tabBars
            size_hint: None,None
            size: 3, 5 * root.center_y / 7
            center_x: root.center_x
            center_y: root.center_y
            #use canvas to "re-draw" the label as a solid rectangle, giving it color and fill which it wouldn't normally have
            canvas:
                Color:
                    rgba: 0, 0, 0, 1
                Rectangle
                    pos: root.center_x / 2 - 100, 3 * root.center_y / 7 + root.center_y / 2
                    size: tabBars.size
                Rectangle
                    pos: root.center_x / 2 + 100, 3 * root.center_y / 7 + root.center_y / 2
                    size: tabBars.size

    #CREATES THE START AND EXIT BUTTONS FOR THE SCENE
        Button:
            id: _toggle
            text: 'Start'
            font_size: 40
            size: root.getWindowWidth()/20, root.getWindowWidth()/40
            center_x: root.center_x/5
            center_y: root.center_y/5
            background_color: 0, 0, 0, 1
        #start the animation song by pressing the button
            on_release: root.start()
        Button:
            text: 'Exit'
            font_size: 40
            size: root.getWindowWidth()/20, root.getWindowWidth()/40
            center_x: root.center_x/5
            center_y: root.center_y/1.5
            background_color: 0, 0, 0, 1
        #stop the animation, song, and reset the UI by pressing the button
            on_release:
                root.stopSong()
                root.manager.transition.direction = 'right'
                root.manager.current = 'song_selection'


    #CREATES THE CENTRAL TRIANGLE THAT SERVES AS A MARKER FOR THE BEATS. WHEN A BEAT HITS THE TRIANGLE, THE TRIANGLE CHANGES COLOR TO A RANDOM HUE. THIS IS WHEN THE USER KNOWS WHEN TO STRUM THE GUITAR
        Label:
            #assign the id _triangle to this label
            id: _triangle
            size_hint: None,None
            center_x: root.center_x
            center_y: root.center_y
            #use canvas to "re-draw" the label as a solid triangle, giving it color and fill which it wouldn't normally have
            canvas:
                #gives the label a color which is defined above using the variables r, g, and b in the uppermost, or "root," class. Recall that these variables are "NumericProperties" and can be set to any integer or float, just like how objects of type ObjectProperty can be set to any object of any type
                #r, g, and b are originally set to 0, 0, 0 (which you'll see above in the Python as each is set to NumbericProperty(0), which gives the triangle label an initial black color)
                #the reason this is done is so the color of the triangle can be changed dynamically, whenever the animation of the scrolling rectangles (as you'll see in the GUI) is complete
                #so once the rectangles disappear halfway across the page, where the triangle is placed, it's like the triangle changes color whenever it's hit by a rectangle
                Color:
                    rgba: root.r, root.g, root.b, 1

                #re-draws the label, custom, to be a triangle. It draws the triangle by supplying the coordinates (x, y) of all 3 points of the triangle. It does this b referencing the label's id, _triangle.
                Triangle
                    points: [root.getWindowWidth() / 2 - root.getWindowWidth() / 10, 0, root.getWindowWidth() / 2 + root.getWindowWidth() / 10, 0, root.getWindowWidth() / 2 , root.getWindowHeight() / 10]
""")


'''build the UI'''
class GuitarUI(App):
    def build(self):
        return sm


ecosystemsPathToSong = 'Music/ecosystems.mp3'



sm.add_widget(SongSelectionScene(name='song_selection')) # adds MainScene to screenmanager
sm.add_widget(AnimateScene(name='amazon', pathToSong = ecosystemsPathToSong, fileName = 'temp'))




if __name__ == '__main__':
    GuitarUI().run()
