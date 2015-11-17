from panda3d.core import TextNode, Vec3, Vec4

class RuntimeHandler(object):
    def __init__(self):
        self.rootList = {}
        self.orbitList = {}
        self.selfRotateList = {}
        self.planetList = {}

    def addPlanet(self, render, planet):
        self.planetList[planet.name] = planet
        if planet.name not in self.rootList:
            self.rootList[planet.name] = render.attachNewNode(planet.name)

        if (planet.children):
            for child in planet.children:
                self.rootList[child.name] = (self.rootList[planet.name].attachNewNode(child.name))
                self.rootList[child.name].setPos(planet.initPosition, 0, 0)
                self.addPlanet(render,child)
                # if (child.orbitRotate):
                #     self.orbitList[child.name] = self.rootList[child.name].hprInterval((child.orbitRotate), Vec3(360, 0, 0))
                #     self.selfRotateList[child.name] = child.hprInterval((child.selfRotate), Vec3(360, 0, 0))

        if (planet.selfRotate):
            self.selfRotateList[planet.name] = planet.model.hprInterval((planet.selfRotate), Vec3(360, 0, 0))

        if (planet.orbitRotate):
            planet.model.reparentTo(self.rootList[planet.name])
            self.orbitList[planet.name] = self.rootList[planet.name].hprInterval((planet.orbitRotate), Vec3(360, 0, 0))
        else:
            planet.model.reparentTo(render)

    def rotatePlanets(self):
        for orbit in self.orbitList:
            self.orbitList[orbit].loop()

        for selfRotate in self.selfRotateList:
            self.selfRotateList[selfRotate].loop()

    def togglePlaying(self):
        for orbit in self.orbitList:
            if self.orbitList[orbit].isPlaying():
                self.orbitList[orbit].pause()
            else:
                self.orbitList[orbit].resume()

        for selfRotate in self.selfRotateList:
            if self.selfRotateList[selfRotate].isPlaying():
                self.selfRotateList[selfRotate].pause()
            else:
                self.selfRotateList[selfRotate].resume()

    def getAllPlanets(self):
        return self.planetList

    def getPlanet(self, name):
        return self.planetList[name]