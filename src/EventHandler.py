class EventHandler(object):
    def __init__(self, runtime):
        self.runtime = runtime
        self.texture = True

    def toggleLight(self):
        pass

    def toggleTexture(self):
        planets = self.runtime.getAllPlanets()
        if (self.texture == True):
            for planet in planets:
                planets[planet].disableTexture()
            self.texture = False
        else:
            for planet in planets:
                planets[planet].enableTexture()
            self.texture = True

    def toggleSimulation(self):
        pass

    def fasterSimulation(self):
        pass

    def slowerSimulation(self):
        pass
