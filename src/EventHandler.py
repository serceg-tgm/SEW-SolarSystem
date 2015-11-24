from panda3d.core import AmbientLight, PointLight, VBase4

class EventHandler(object):
    def __init__(self, runtime):
        self.runtime = runtime
        self.pointlightOn = True
        self.textureOn = True
        self.initializeLight()
        self.lightOn = True

    def initializeLight(self):

        alight = AmbientLight('alight')
        alight.setColor(VBase4(0.2, 0.2, 0.2, 1))
        self.alnp = render.attachNewNode(alight)

        sunLight = AmbientLight('slight')
        sunLight.setColor(VBase4(0.7, 0.7, 0.7, 1))
        sun = self.runtime.getPlanet('sun')
        self.slnp = sun.model.attachNewNode(sunLight)
        sun.model.setLight(self.slnp)

        plight = PointLight('plight')
        plight.setColor(VBase4(0.7, 0.7, 0.7, 1))
        self.plnp = render.attachNewNode(plight)
        self.plnp.setPos(0, 0, 0)
        render.setLight(self.plnp)

    def toggleLight(self):

        sun = self.runtime.getPlanet('sun')
        if self.lightOn == True:
            sun.model.setLightOff()
            render.setLightOff()
            # render.setLight(self.alnp)
            self.lightOn = False
        else:
            sun.model.setLightOff()
            sun.model.setLight(self.slnp)
            render.setLightOff()
            render.setLight(self.plnp)
            self.lightOn = True

        print(self.lightOn)

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

