import direct.directbase.DirectStart
from pandac.PandaModules import WindowProperties
from RuntimeHandler import *
from Luminary import *
from Camera import *
from EventHandler import *



# We start this tutorial with the standard class. However, the class is a
# subclass of an object called DirectObject. This gives the class the ability
# to listen for and respond to events. From now on the main class in every
# tutorial will be a subclass of DirectObject

class World(DirectObject):

    def __init__(self):

        props = WindowProperties()
        props.setTitle('Solarsystem')
        base.win.requestProperties(props)
        base.setBackgroundColor(0, 0, 0)

        # The global variables we used to control the speed and size of objects
        self.yearscale = 60
        self.dayscale = self.yearscale / 365.0 * 5
        self.orbitscale = 10
        self.sizescale = 0.6
        self.skySize = 80

        self.runtime = RuntimeHandler()
        self.camera = Camera(render, self.skySize)

        self.loadLuminaries()
        self.runtime.rotateLuminaries()

        self.eventHandler = EventHandler(self.runtime, self.camera, self.runtime.getLuminary('sun'))

    def loadLuminaries(self):
        mercury = Luminary("mercury", "models/mercury_1k_tex.jpg", "models/planet_sphere", 0.38 * self.orbitscale, 0.385 * self.sizescale, None, 59 * self.dayscale, 0.241 * self.yearscale, True)
        venus = Luminary("venus", "models/venus_1k_tex.jpg", "models/planet_sphere", 0.72 * self.orbitscale, 0.923 * self.sizescale, None, 243 * self.dayscale, 0.615 * self.yearscale, True)
        mars = Luminary("mars", "models/mars_1k_tex.jpg", "models/planet_sphere", 1.52 * self.orbitscale, 0.515 * self.sizescale, None, 1.03 * self.dayscale, 1.881 * self.yearscale, True)
        moon = Luminary("moon", "models/moon_1k_tex.jpg", "models/planet_sphere", 0.1 * self.orbitscale, 0.1 * self.sizescale, None, .0749 * self.yearscale, .0749 * self.yearscale, True)
        asteroid = Luminary("asteroid", "models/asteroid.jpg", "models/planet_sphere", 0.3 * self.orbitscale, 0.5 * self.sizescale, None, .0749 * self.yearscale, .0749 * self.yearscale, True)
        earth = Luminary("earth", "models/earth_1k_tex.jpg", "models/planet_sphere", self.orbitscale, self.sizescale, [moon], self.dayscale, self.yearscale, True)
        gas = Luminary("gas", "models/gas-planet.png", "models/planet_sphere", 2 * self.orbitscale, 1.5 * self.sizescale, [asteroid], 300*self.dayscale, 3*self.yearscale, True)
        ice = Luminary("ice", "models/ice.jpg", "models/planet_sphere", 1.4 * self.orbitscale, 3 * self.sizescale, None, 0.5*self.dayscale, 4*self.yearscale, True)
        brown = Luminary("brown", "models/brown.jpg", "models/planet_sphere", 2.5 * self.orbitscale, 0.7 * self.sizescale, None, self.dayscale, 0.5*self.yearscale, True)
        sun = Luminary("sun", "models/sun_1k_tex.jpg", "models/planet_sphere", 0, 3 * self.sizescale, [mercury, venus, mars, earth, gas, ice, brown], 20, None, True)

        sky = Luminary("sky", "models/stars_1k_tex.jpg", "models/solar_sky_sphere", 0, self.skySize, [sun], None, None, False)

        self.runtime.addLuminary(render, sky)

w = World()
run()
