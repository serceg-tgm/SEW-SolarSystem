from panda3d.core import TextNode, Vec3, Vec4

class RuntimeHandler(object):

    """ Stellt die sichtbaren Elemente des Solarsystems dar. Diese sind der Weltraum, die Planeten und andere Himmelskoerper

    :ivar dictionary rootList: Liste der Nodepath eines Himmelskoerper
    :ivar dictionary orbitList: Liste der Laufbahnen eines Himmelskoerpers
    :ivar dictionary selfRotateList: Liste der Selbstrotationen eines Himmelskoerpers
    :ivar dictionary luminaryList: Liste der Himmelskoerper

    """

    def __init__(self):

        """ Initialisiert die Runtime

        """

        self.rootList = {}
        self.orbitList = {}
        self.selfRotateList = {}
        self.luminaryList = {}


    def addLuminary(self, render, luminary):

        """ Fuegt einen neuen Himmelskoerper, der einen neuen Namen haben muss, in das Solarsystem ein.
        Dabei kann ein Himmelskoerper aber noch "Kinder" haben. Die um diesen kreisen.

        :param render: Gesamte Umgebung des Raumes
        :param luminary: der hinzuzufuegende Himmelskoerper
        """

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

        """ Laesst alle Himmelskoerper rotieren/starten

        """

        for orbit in self.orbitList:
            self.orbitList[orbit].loop()

        for selfRotate in self.selfRotateList:
            self.selfRotateList[selfRotate].loop()

    def togglePlaying(self):

        """ Schaltet das Solarsystem ein oder aus. Falls das System resetet wurde, wird es bei Betaetigung wieder eingeschaltet

        """

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

        """ Addiert die angegebene Geschwindigkeit zu der aktuellen. Sollte die Geschwindigkeit aber 0 ergeben, wuerde
        sich die Simulation zuruecksetzen und deswegen wird dann das doppelte addiert

        :param int speed: Geschwindigkeit, die addiert werden soll
        """

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

        """ Beschleunigt die Simulation um 1

        """

        self.editSpeedPlaying(1)

    def slowerPlaying(self):

        """ Verlangsamt die Simulation um 1

        """

        self.editSpeedPlaying(-1)

    def restartSimulation(self):

        """ Setzt die Simulation zurueck

        """

        for orbit in self.orbitList:
            self.orbitList[orbit].setPlayRate(0)

        for selfRotate in self.selfRotateList:
            self.selfRotateList[selfRotate].setPlayRate(0)

    def getAllLuminaries(self):

        """ Gibt alle Luminaries, die hinzugefuegt wurden, zurueck

        :return: Alle Luminaries die hinzugefuegt wurden
        """

        return self.luminaryList

    def getLuminary(self, name):

        """ Gibt den gesuchten Himmelskoerper zurueck

        :param name: Der Name des gesuchten Himmelskoerpers
        :return: Der gesuchte Himmelskoerper
        """

        return self.luminaryList[name]