from panda3d.core import TextNode, Vec3, Vec4

class RuntimeHandler(object):
    def __init__(self):
        self.rootList = {}
        self.orbitList = {}
        self.selfRotateList = {}
        self.luminaryList = {}

    def addLuminary(self, render, luminary):
        self.luminaryList[luminary.name] = luminary
        if luminary.name not in self.rootList:
            self.rootList[luminary.name] = render.attachNewNode(luminary.name)

        if (luminary.children):
            for child in luminary.children:
                self.rootList[child.name] = (self.rootList[luminary.name].attachNewNode(child.name))
                self.rootList[child.name].setPos(luminary.initPosition, 0, 0)
                self.addLuminary(render,child)

        if (luminary.selfRotate):
            self.selfRotateList[luminary.name] = luminary.model.hprInterval((luminary.selfRotate), Vec3(360, 0, 0))

        if (luminary.orbitRotate):
            luminary.model.reparentTo(self.rootList[luminary.name])
            self.orbitList[luminary.name] = self.rootList[luminary.name].hprInterval((luminary.orbitRotate), Vec3(360, 0, 0))
        else:
            luminary.model.reparentTo(render)

    def rotateLuminaries(self):
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

            if self.orbitList[orbit].getPlayRate()==0:
                self.orbitList[orbit].setPlayRate(1)

        for selfRotate in self.selfRotateList:
            if self.selfRotateList[selfRotate].isPlaying():
                self.selfRotateList[selfRotate].pause()
            else:
                self.selfRotateList[selfRotate].resume()

            if self.selfRotateList[selfRotate].getPlayRate()==0:
                self.selfRotateList[selfRotate].setPlayRate(1)

    def editSpeedPlaying(self, speed):
        for orbit in self.orbitList:
            self.orbitList[orbit].resume()
            if self.orbitList[orbit].getPlayRate() + speed == 0:
                self.orbitList[orbit].setPlayRate(self.orbitList[orbit].getPlayRate() + 2*speed)
                continue

            self.orbitList[orbit].setPlayRate(self.orbitList[orbit].getPlayRate() + speed)

        for selfRotate in self.selfRotateList:
            self.selfRotateList[selfRotate].resume()
            if self.selfRotateList[selfRotate].getPlayRate() + speed == 0:
                self.selfRotateList[selfRotate].setPlayRate(self.selfRotateList[selfRotate].getPlayRate() + 2*speed)
                continue
            self.selfRotateList[selfRotate].setPlayRate(self.selfRotateList[selfRotate].getPlayRate() + speed)

    def fasterPlaying(self):
        self.editSpeedPlaying(1)

    def restartSimulation(self):
        for orbit in self.orbitList:
            self.orbitList[orbit].setPlayRate(0)

        for selfRotate in self.selfRotateList:
            self.selfRotateList[selfRotate].setPlayRate(0)

    def slowerPlaying(self):
        self.editSpeedPlaying(-1)

    def getAllLuminaries(self):
        return self.luminaryList

    def getLuminary(self, name):
        return self.luminaryList[name]