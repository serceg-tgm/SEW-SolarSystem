from panda3d.core import AmbientLight
from panda3d.core import Point3,Vec3,Vec4

class EventHandler(object):
    def __init__(self, runtime):
        self.runtime = runtime
        self.pointlightOn = True
        self.textureOn = True

    def toggleLight(self):
        alight = AmbientLight('alight')
        alight.setColor(Vec4(0.2, 0.2, 0.2, 1))
        alnp = render.attachNewNode(alight)
        self.sun = self.runtime.getPlanet('sun')
        self.sun.reparentTo(render)
        self.sun.setLight(alnp)

    def toggleTexture(self):
        planets = self.runtime.getAllPlanets()
        if self.textureOn == True:
            for planet in planets:
                if planets[planet].textureToggle==True:
                    planets[planet].disableTexture()
            self.textureOn = False
        else:
            for planet in planets:
                if planets[planet].textureToggle==True:
                    planets[planet].enableTexture()
            self.textureOn = True

    def restartSimulation(self):
        self.runtime.restartSimulation()

    def toggleSimulation(self):
        self.runtime.togglePlaying()

    def fasterSimulation(self):
        self.runtime.fasterPlaying()

    def slowerSimulation(self):
        self.runtime.slowerPlaying()

