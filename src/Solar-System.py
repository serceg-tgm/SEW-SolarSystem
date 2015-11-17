# Author: Shao Zhang and Phil Saltzman
# Last Updated: 4/20/2005
#
# This tutorial will cover events and how they can be used in Panda
# Specifically, this lesson will use events to capture keyboard presses and
# mouse clicks to trigger actions in the world. It will also use events
# to count the number of orbits the Earth makes around the sun. This
# tutorial uses the same base code from the solar system tutorial.

import direct.directbase.DirectStart
from direct.showbase import DirectObject
from panda3d.core import TextNode, Vec3, Vec4
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from direct.showbase.DirectObject import DirectObject
import sys
from RuntimeHandler import *
from Planet import *
from Camera import *
from EventHandler import *



# We start this tutorial with the standard class. However, the class is a
# subclass of an object called DirectObject. This gives the class the ability
# to listen for and respond to events. From now on the main class in every
# tutorial will be a subclass of DirectObject

class World(DirectObject):
    # Macro-like function used to reduce the amount to code needed to create the
    # on screen instructions
    def genLabelText(self, text, i):
        return OnscreenText(text=text, pos=(-1.3, .95 - .05 * i), fg=(1, 1, 1, 1),
                            align=TextNode.ALeft, scale=.05, mayChange=1)

    def __init__(self):

        self.runtime = RuntimeHandler()
        self.eventHandler = EventHandler(self.runtime)
        self.camera = Camera()
        # The standard camera position and background initialization
        base.setBackgroundColor(0, 0, 0)
        base.disableMouse()
        camera.setPos(0, 0, 45)
        camera.setHpr(0, -90, 0)

        # The global variables we used to control the speed and size of objects
        self.yearscale = 60
        self.dayscale = self.yearscale / 365.0 * 5
        self.orbitscale = 10
        self.sizescale = 0.6

        self.loadPlanets()  # Load, texture, and position the planets
        self.runtime.rotatePlanets()  # Set up the motion to start them moving

        # The standard title text that's in every tutorial
        # Things to note:
        # -fg represents the forground color of the text in (r,g,b,a) format
        # -pos  represents the position of the text on the screen.
        #      The coordinate system is a x-y based wih 0,0 as the center of the
        #      screen
        # -align sets the alingment of the text relative to the pos argument.
        #      Default is center align.
        # -scale set the scale of the text
        # -mayChange argument lets us change the text later in the program.
        #       By default mayChange is set to 0. Trying to change text when
        #       mayChange is set to 0 will cause the program to crash.
        self.title = OnscreenText(text="Solarsystem",
                                  style=1, fg=(1, 1, 1, 1),
                                  pos=(0.9, -0.95), scale=.07)

        self.spaceEventText = self.genLabelText(
            "Space: Toggle entire Solar System [RUNNING]", 0)

        self.tEventText = self.genLabelText(
            "T: Toggle the Texture", 1)

        self.simRunning = True  # boolean to keep track of the
        # state of the global simulation

        # Events
        # Each self.accept statement creates an event handler object that will call
        # the specified function when that event occurs.
        # Certain events like "mouse1", "a", "b", "c" ... "z", "1", "2", "3"..."0"
        # are references to keyboard keys and mouse buttons. You can also define
        # your own events to be used within your program. In this tutorial, the
        # event "newYear" is not tied to a physical input device, but rather
        # is sent by the function that rotates the Earth whenever a revolution
        # completes to tell the counter to update


        taskMgr.add(self.camera.controlCamera, "camera-task")
        self.accept("escape", sys.exit)  # Exit the program when escape is pressed
        self.accept("space", self.handleMouseClick)
        self.accept("t", self.eventHandler.toggleTexture)

        self.accept("mouse1", self.camera.setMouseBtn, [0, 1])
        self.accept("mouse1-up", self.camera.setMouseBtn, [0, 0])
        self.accept("mouse2", self.camera.setMouseBtn, [1, 1])
        self.accept("mouse2-up", self.camera.setMouseBtn, [1, 0])
        self.accept("mouse3", self.camera.setMouseBtn, [2, 1])
        self.accept("mouse3-up", self.camera.setMouseBtn, [2, 0])

    # end __init__

    def handleMouseClick(self):
        # When the mouse is clicked, if the simulation is running pause all the
        # planets and sun, otherwise resume it
        if self.simRunning:
            # changing the text to reflect the change from "RUNNING" to "PAUSED"
            self.spaceEventText.setText(
                "Mouse Button 1: Toggle entire Solar System [PAUSED]")
        else:
            self.spaceEventText.setText(
                "Mouse Button 1: Toggle entire Solar System [RUNNING]")

        self.runtime.togglePlaying()
        # toggle self.simRunning
        self.simRunning = not self.simRunning

    # end handleMouseClick

    #########################################################################
    # Except for the one commented line below, this is all as it was before #
    # Scroll down to the next comment to see an example of sending messages #
    #########################################################################

    def loadPlanets(self):
        sky = Planet("sky", "models/stars_1k_tex.jpg", "models/solar_sky_sphere", None, 40, None, None, None, False)

        mercury = Planet("mercury", "models/mercury_1k_tex.jpg", "models/planet_sphere", 0.38 * self.orbitscale, 0.385 * self.sizescale, None, 59 * self.dayscale, 0.241 * self.yearscale, True)
        venus = Planet("venus", "models/venus_1k_tex.jpg", "models/planet_sphere", 0.72 * self.orbitscale, 0.923 * self.sizescale, None, 243 * self.dayscale, 0.615 * self.yearscale, True)
        mars = Planet("mars", "models/mars_1k_tex.jpg", "models/planet_sphere", 1.52 * self.orbitscale, 0.515 * self.sizescale, None, 1.03 * self.dayscale, 1.881 * self.yearscale, True)
        moon = Planet("moon", "models/moon_1k_tex.jpg", "models/planet_sphere", 0.1 * self.orbitscale, 0.1 * self.sizescale, None, .0749 * self.yearscale, .0749 * self.yearscale, True)
        earth = Planet("earth", "models/earth_1k_tex.jpg", "models/planet_sphere", self.orbitscale, self.sizescale, [moon], self.dayscale, self.yearscale, True)
        sun = Planet("sun", "models/sun_1k_tex.jpg", "models/planet_sphere", 0, 2 * self.sizescale, None, 20, None, True)

        self.runtime.addPlanet(render, mercury)
        self.runtime.addPlanet(render, venus)
        self.runtime.addPlanet(render, mars)
        self.runtime.addPlanet(render, earth)
        self.runtime.addPlanet(render, sun)
        self.runtime.addPlanet(render, sky)

# end class world

w = World()

run()
