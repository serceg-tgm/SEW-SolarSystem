class EventHandler(object):
    def __init__(self, runtime):
        self.runtime = runtime
        self.textureOn = True

    def toggleLight(self):
        pass

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

    def toggleSimulation(self):
        pass

    def fasterSimulation(self):
        pass

    def slowerSimulation(self):
        pass
