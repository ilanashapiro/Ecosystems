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
import random, time, threading, os, math
from threading import Thread


import sys


#create a screenmanager for the UI, and set the background window color to white
sm = ScreenManager()
Window.clearcolor = (.95, .95, .95, 1) #background white

currentCol = 0
currentRow = 0

class LabelSquare(Label):
    def __init__(self, row, col, green, **kwargs):
        super(LabelSquare, self).__init__(**kwargs)
        with self.canvas:
            Color(0, green, 0, 1)
            Rectangle(pos=(row * (self.getWindowWidth() / EcosystemsUI().numRowsColsInJungleGrid), col * (self.getWindowHeight() / EcosystemsUI().numRowsColsInJungleGrid)), size=(10, 10)) #EcosystemsUI().numRowsColsInJungleGrid, self.getWindowHeight() / (EcosystemsUI().numRowsColsInJungleGrid)))
            print(str(row) + " " + str(col))
    def getWindowWidth(self):
        return Window.width

    def getWindowHeight(self):
        return Window.height

#define the class for the first scene in the UI, which (in the Kivy code)
# allows for song selection
class EcosystemSelectionScene(Screen):
    def getWindowWidth(self):
        return Window.width

    def getWindowHeight(self):
        return Window.height

    def quitUI(self):
        quit()


#define the class for the second  scene in the UI, which (in the Kivy code) will display the beats of the song currently playing in the background as scrolling rectangles;
# a dynamic graphic of the current guitar fret (with the strings in use lit up) that also includes the finger numbers for that chord;
# and a triangle in the bottom center of the screen that changes color when a beat hits it, indicating that the user should strum the guitar at this time
class AmazonScene(Screen):


    #beat_1, triangle, and triangle are of type ObjectProperty, which means they are of any object type, therefore they can be assigned to any object of any kind later in the code
    #in these cases, in the kivy code, beat_1, triangle, and toggle are assigned to be different labels in the kivy. See the kivy for more instructions

    triangle = ObjectProperty(None)
    toggle = ObjectProperty(None)
    tree = ObjectProperty(None)
    grid = ObjectProperty(None)

    angle = NumericProperty(0)



    pathSize = 0




    fileName = ""

#constructor for AmazonScene. the song that will play in the background is loaded here
    def __init__(self, name, **kwargs):
        self.name = name
        super(Screen, self).__init__()
        print("super")


    def doNothing(self, *args):
        pass

    #the following access the width and height of the current screen using the width and height properties of the Window object. These methods are used in the Kivy and below in other Python methods for positioning
    def getWindowWidth(self):
        return Window.width

    def getWindowHeight(self):
        return Window.height


    #plays the song
    def playSound(self, *args):
        self.audioFile.play()


    def start(self, *args):
        # if(self.name == "deforestation"):
        #     t = threading.Timer(0, self.playSound)
        #     t.start()


        self.animation = Animation(x=self.getWindowWidth(), y=0, duration=3.0, t = "out_circ")
        self.animation &= Animation(size=(0, 0))
        #self.animation += Animation(x=self.getWindowWidth(), y=0, duration=0.0)
        #self.animation += Animation(size=(10, self.getWindowHeight()), duration=0.0)

        self.animation.start(self.tree)
        self.animation.bind(on_complete = self.toDeforestation)
        print("anim")



    def toDeforestation(self, *args):
        sm.current = "deforestation"
        sm.on_enter = DeforestationScene.startAnim()
        print("started anim and song")


#stop the song, the animation, set all the strings in the guitar tab graphic to black (implemented later in the Kivy), set all the tab text to empty strings, and home the carriage motor
    def stopSong(self):
        if(self.audioFile.state == 'play'):
            self.audioFile.stop()


    def quitUI(self):
        quit()

class DeforestationScene(Screen):
    def __init__(self, name, pathToSong, fileName, **kwargs):
        self.name = name
        self.pathToSong = pathToSong
        self.fileName = fileName
        DeforestationScene.audioFile = SoundLoader.load(pathToSong)
        self.pathSize = os.path.getsize(self.pathToSong)

        super(Screen, self).__init__()



        box = ObjectProperty(None)
        grid = ObjectProperty(None)


    #def on_float(self, *args):
        green = 1
        for i in range(EcosystemsUI().numTreesInJungle):
            currentRow = (i + EcosystemsUI().numRowsColsInJungleGrid) // EcosystemsUI().numRowsColsInJungleGrid
            currentCol = (i + 1) % EcosystemsUI().numRowsColsInJungleGrid
            if(currentCol == 0):
                currentCol = 5
            green = -1 * green
            self.float.add_widget(LabelSquare(currentRow, currentCol, green))
            #self.grid.add_widget(Button(text=str(i)))
            print(currentRow)
            print(currentCol)
            print(i)
            print("")



    # def show_tasks(self):
    #     tasks = {("0", "1"), ("1", "0"), ("0", "1"), ("1", "0"), ("0", "1"), ("1", "0")} # Returns an array of tuples
    #     for task in tasks:
    #         self.grid.add_widget(Label(text=task[1], color = (0, 0, 0, 1), width = 200, font_size = 20))

    def doNothing(self, *args):
        pass

    #the following access the width and height of the current screen using the width and height properties of the Window object. These methods are used in the Kivy and below in other Python methods for positioning
    def getWindowWidth(self):
        return Window.width

    def getWindowHeight(self):
        return Window.height


    #plays the song
    @staticmethod
    def playSound(*args):
        DeforestationScene.audioFile.play()

    @staticmethod
    def startAnim(*args):
        print("deforested")
        t = threading.Timer(0, DeforestationScene.playSound)
        t.start()

    def stopSong(self):
        if(self.audioFile.state == 'play'):
            self.audioFile.stop()


    def quitUI(self):
        quit()






Builder.load_string("""
<EcosystemSelectionScene>:
    name: 'ecosystem_selection'
    FloatLayout:
        size_hint: None, None  #Needed to be able to define define height and width of widgets
    #     Label:
    #         size: 400, 100
    #         id: selection
    #         size_hint: None,None
    #         center_x: root.center_x
    #         center_y: root.center_y * 1.8
    #         font_size: 75
    #         text: 'Ecosystem Selection'
    #         color: 0.5, 0, 1, 1

        Label:
            #assign the id _triangle to this label
            #id: _tree
            size_hint: None,None
            center_x: root.getWindowWidth() / 2
            center_y: root.getWindowHeight() / 10 + 5 * root.getWindowWidth() / 25
            #use canvas to "re-draw" the label as a solid triangle, giving it color and fill which it wouldn't normally have
            color: 0.5, 0, 1, 1
            canvas:
                Color:
                    rgba: 0.25, 0.25, 0.25, 1
                Rectangle
                    pos: root.getWindowWidth() / 2 , 0
                    size: root.getWindowWidth() / 50, root.getWindowHeight() / 10 + 3 * root.getWindowWidth() / 25
                Rectangle
                    pos: root.getWindowWidth() / 2 - root.getWindowWidth() / 50, 0
                    size: root.getWindowWidth() / 50, root.getWindowHeight() / 10 + 3 * root.getWindowWidth() / 25


                Color:
                    rgba: 0, 0.5, 0, 1  #green

                #re-draws the label, custom, to be a triangle. It draws the triangle by supplying the coordinates (x, y) of all 3 points of the triangle. It does this b referencing the label's id, _triangle.
                Triangle
                    points: [root.getWindowWidth() / 2 - root.getWindowWidth() / 10, 3 * root.getWindowWidth() / 25,                          root.getWindowWidth() / 2 + root.getWindowWidth() / 10, 3 * root.getWindowWidth() / 25,                  root.getWindowWidth() / 2 , 3 * root.getWindowHeight() / 10]

                Color:
                    rgba: 0, 1, 0.25, 1  #blueish green
                Triangle
                    points: [root.getWindowWidth() / 2 - root.getWindowWidth() / 10, 4 * root.getWindowWidth() / 25,                 root.getWindowWidth() / 2 + root.getWindowWidth() / 10, 4 * root.getWindowWidth() / 25,                    root.getWindowWidth() / 2 , root.getWindowHeight() / 10 + 4 * root.getWindowWidth() / 25]

                Color:
                    rgba: 0, 0.75, 0.25, 1  #blue green
                Triangle
                    points: [root.getWindowWidth() / 2 - root.getWindowWidth() / 10, 5 * root.getWindowWidth() / 25,                 root.getWindowWidth() / 2 + root.getWindowWidth() / 10, 5 * root.getWindowWidth() / 25,                    root.getWindowWidth() / 2 , root.getWindowHeight() / 10 + 5 * root.getWindowWidth() / 25]

        Button:
            size_hint: None,None
            text: 'Enter the Amazon'
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

<AmazonScene>:
    name: 'amazon'
    #assign the ObjectProperty triangle defined above in the Python to the id _triangle, which belongs to the triangular label a few lines down
    tree: _tree

    FloatLayout:
        size_hint: None, None  #Needed to be able to define define height and width of widgets
        canvas.before:
            PushMatrix
            Rotate:
                angle: root.angle
                axis: 0, 0, 1
                origin: root.center
        canvas.after:
            PopMatrix
        Image:
            id: _tree
            source: 'Pictures/tree.png'
            size_hint: None, None
            size: 500, 500
            pos: 0, 0






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
                root.manager.current = 'ecosystem_selection'

<DeforestationScene>:
    name: 'deforestation'
    #box: box
    #grid: grid
    float:float
    FloatLayout:
        id: float
        # BoxLayout:
        #     id: box
        #     orientation: "horizontal"
        #     pos_hint: {"x": 0, "y": 0}
        #     GridLayout:
        #         id: grid
        #         #rows: 4
        #         cols: app.numRowsColsInJungleGrid
        #         padding: 10
        #         spacing: 10
        #         row_force_default: True
        #         row_default_height: 40
        #         # Label:
        #         #     text: 'Deforestation'
        #         #     color: 0, 0, 0, 1
        #         #     size_hint_x: None
        #         #     width: 200
        #         #     font_size: 24


    # grid: root.grid
    # FloatLayout:
    #     BoxLayout:
    #         orientation: "horizontal"
    #         pos_hint: {"x": 0, "y": 0}
    #         GridLayout:
    #             id: _grid
    #             # rows: 4
    #             cols: 1
    #             padding: 10
    #             spacing: 10
    #             row_force_default: True
    #             row_default_height: 40
    #             Label:
    #                 text: 'Your Tasks:'
    #                 color: 0, 0, 0, 1
    #                 size_hint_x: None
    #                 width: 200
    #                 font_size: 24
""")


'''build the UI'''
class EcosystemsUI(App):
    numTreesInJungle = 5*5
    numRowsColsInJungleGrid = 5
    def build(self):
        return sm


ecosystemsPathToSong = 'Music/ecosystems.mp3'




sm.add_widget(EcosystemSelectionScene(name='ecosystem_selection')) # adds MainScene to screenmanager
sm.add_widget(AmazonScene(name='amazon'))
sm.add_widget(DeforestationScene(name='deforestation', pathToSong = ecosystemsPathToSong, fileName = 'ecosystems'))




if __name__ == '__main__':
    EcosystemsUI().run()
