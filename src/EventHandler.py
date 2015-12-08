from panda3d.core import AmbientLight, PointLight, VBase4, TextNode
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import WindowProperties
import sys

class EventHandler(DirectObject):
    def __init__(self, runtime, camera, middle):
        self.runtime = runtime
        self.camera = camera
        self.middle = middle
        self.pointlightOn = True
        self.textureOn = True
        self.initializeLight()
        self.lightOn = True

        self.setEvents()
        self.setLegend()

    def initializeLight(self):

        self.sunLight = AmbientLight('slight')
        self.sunLight.setColor(VBase4(1, 1, 1, 1))
        sun = self.middle
        slnp = sun.model.attachNewNode(self.sunLight)
        sun.model.setLight(slnp)

        alight = AmbientLight('alight')
        alight.setColor(VBase4(0.2, 0.2, 0.2, 1))
        self.alnp = render.attachNewNode(alight)

        plight = PointLight('plight')
        plight.setColor(VBase4(1, 1, 1, 1))
        self.plnp = render.attachNewNode(plight)
        self.plnp.setPos(0, 0, 0)
        render.setLight(self.plnp)

    def setEvents(self):
        self.accept("escape", sys.exit)
        self.accept("space", self.toggleSimulation)
        self.accept("t", self.toggleTexture)
        self.accept("l", self.toggleLight)
        self.accept("+", self.fasterSimulation)
        self.accept("-", self.slowerSimulation)
        self.accept("r", self.restartSimulation)
        self.accept("b", self.camera.birdPerspective)

        self.accept("w", self.camera.setMouseBtn, [0, 1])
        self.accept("arrow_up", self.camera.setMouseBtn, [0, 1])
        self.accept("w-up", self.camera.setMouseBtn, [0, 0])
        self.accept("arrow_up-up", self.camera.setMouseBtn, [0, 0])

        self.accept("s", self.camera.setMouseBtn, [1, 1])
        self.accept("arrow_down", self.camera.setMouseBtn, [1, 1])
        self.accept("s-up", self.camera.setMouseBtn, [1, 0])
        self.accept("arrow_down-up", self.camera.setMouseBtn, [1, 0])

        self.accept("a", self.camera.setMouseBtn, [2, 1])
        self.accept("arrow_left", self.camera.setMouseBtn, [2, 1])
        self.accept("a-up", self.camera.setMouseBtn, [2, 0])
        self.accept("arrow_left-up", self.camera.setMouseBtn, [2, 0])

        self.accept("d", self.camera.setMouseBtn, [3, 1])
        self.accept("arrow_right", self.camera.setMouseBtn, [3, 1])
        self.accept("d-up", self.camera.setMouseBtn, [3, 0])
        self.accept("arrow_right-up", self.camera.setMouseBtn, [3, 0])

        self.accept("u", self.camera.setMouseBtn, [4, 1])
        self.accept("u-up", self.camera.setMouseBtn, [4, 0])
        self.accept("wheel_up", self.camera.setMouseBtn, [4, 1])

        self.accept("j", self.camera.setMouseBtn, [5, 1])
        self.accept("j-up", self.camera.setMouseBtn, [5, 0])
        self.accept("wheel_down", self.camera.setMouseBtn, [5, 1])

    def genLabelText(self, text, i):
        return OnscreenText(text=text, pos=(-1.3, .95 - .05 * i), fg=(1, 1, 1, 1),
                            align=TextNode.ALeft, scale=.05, mayChange=1)

    def setLegend(self):
        self.escEventText = self.genLabelText(
            "ESC: Quit program", 0)
        self.spaceEventText = self.genLabelText(
            "Space: Toggle entire Solar System", 1)
        self.tEventText = self.genLabelText(
            "T: Toggle the Texture", 2)
        self.lEventText = self.genLabelText(
            "L: Toggle the Point-Light Source", 3)
        self.nEventText = self.genLabelText(
            "+: Make the simulation faster", 4)
        self.mEventText = self.genLabelText(
            "-: Make the simulation slower", 5)
        self.lEventText = self.genLabelText(
            "W|Arrow-up: Go forward", 6)
        self.bEventText = self.genLabelText(
            "B: Bird's-eye view", 7)
        self.lEventText = self.genLabelText(
            "S|Arrow-down: Go backward", 8)
        self.lEventText = self.genLabelText(
            "A|Arrow-left: Go left", 9)
        self.lEventText = self.genLabelText(
            "D|Arrow-right: Go right", 10)
        self.lEventText = self.genLabelText(
            "U: Go upward", 11)
        self.lEventText = self.genLabelText(
            "J: Go downward", 12)

    def toggleLight(self):

        if self.lightOn == True:
            self.sunLight.setColor(VBase4(0.2, 0.2, 0.2, 1))
            render.setLightOff()
            render.setLight(self.alnp)
            self.lightOn = False
        else:
            self.sunLight.setColor(VBase4(1, 1, 1, 1))
            render.setLightOff()
            render.setLight(self.plnp)
            self.lightOn = True

    def toggleTexture(self):
        luminary = self.runtime.getAllLuminaries()
        if self.textureOn == True:
            for luminary in luminary:
                if luminary[luminary].textureToggle==True:
                    luminary[luminary].disableTexture()
            self.textureOn = False
        else:
            for luminary in luminary:
                if luminary[luminary].textureToggle==True:
                    luminary[luminary].enableTexture()
            self.textureOn = True

    def restartSimulation(self):
        self.runtime.restartSimulation()

    def toggleSimulation(self):
        self.runtime.togglePlaying()

    def fasterSimulation(self):
        self.runtime.fasterPlaying()

    def slowerSimulation(self):
        self.runtime.slowerPlaying()

