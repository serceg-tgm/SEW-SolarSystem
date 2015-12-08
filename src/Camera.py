from panda3d.core import TextNode, Vec3, Vec4
from direct.task.Task import Task
from pandac.PandaModules import WindowProperties
from math import *


class Camera(object):

    """ Ermoeglich die Bewegung im dreidimensionalen Raum

    :ivar int size: Groesse des Weltraums
    :ivar Vec3 focus: Definiert die Position der Kamera
    :ivar int heading: Der aktuelle Drehwinkel
    :ivar int pitch: Der aktuelle Neigungswinkel
    :ivar int mousex: Die Position der Maus auf der x-Achse
    :ivar int mousey: Die Position der Maus auf der y-Achse
    :ivar int lastTime: Gibt die Zeit an, wann die Methode controlCamera zuletzt ausgefuehrt wurde
    :ivar list mousebtn: Liste in der die getaetigten Tastendruecke festgehalten werden
    :ivar int lastX: Letzte Position auf der x-Achse
    :ivar int lastY: Letzte Position auf der y-Achse
    :ivar int lastZ: Letzte Position auf der z-Achse

    """

    def __init__(self, render, size):


        """ Definiert die Mouseposition und den Startpunkt der Kamera

        :param render: Gesamte Umgebung des Raumes
        :param size: Groesse des Weltraums
        """


        base.win.movePointer(0, 0, 0)
        base.disableMouse()
        self.size = size
        self.focus = Vec3(-14, -31, 10)
        self.heading = -45
        self.pitch = -35
        self.mousex = 0
        self.mousey = 0
        self.lastTime = 0
        self.mousebtn = [0, 0, 0, 0, 0, 0]
        self.lastX = -14
        self.lastY = -31
        self.lastZ = 10
        # base.camera.setPos(-14, -31, 10)
        base.camera.reparentTo(render)
        base.camera.setHpr(0, 0, 0)
        WindowProperties().setCursorHidden(True)

        taskMgr.add(self.controlCamera, "camera-task")

    def controlCamera(self, task):

        """ Steuert die Camera aufgrund von getaetigten Tasten oder Mausbewegungen. Diese Methode wird aufgrund
        des Tasks sehr oft ausgefuehrt

        :param task: Gibt an, welche Funktion diese Methode uebernehmen soll
        """

        md = base.win.getPointer(0)
        x = md.getX()
        y = md.getY()
        if base.win.movePointer(0, 100, 100):
            self.heading = self.heading - (x - 100) * 0.2
            self.pitch = self.pitch - (y - 100) * 0.2
        if (self.pitch < -90): self.pitch = -90
        if (self.pitch > 90): self.pitch = 90
        base.camera.setHpr(self.heading, self.pitch, 0)
        dir = base.camera.getMat().getRow3(1)
        elapsed = task.time - self.lastTime
        if (self.lastTime == 0): elapsed = 0

        if (self.mousebtn[0]):
            self.focus = self.focus + dir * elapsed * 30
        if self.mousebtn[1]:
            self.focus = self.focus - dir * elapsed * 30

        base.camera.setPos(self.focus - (dir * 5))

        if self.mousebtn[2]:
            base.camera.setX(base.camera, -elapsed * 30)
        if self.mousebtn[3]:
            base.camera.setX(base.camera, elapsed * 30)
        if self.mousebtn[4]:
            base.camera.setZ(base.camera, elapsed * 30)
        if self.mousebtn[5]:
            base.camera.setZ(base.camera, -elapsed * 30)

        self.focus = base.camera.getPos() + (dir * 5)

        self.checkArea(self.size)

        self.lastTime = task.time
        return Task.cont


    def birdPerspective(self):

        """ Setzt die Kamera in die Vogelperspektive

        """

        self.pitch = -90
        self.focus = Vec3(0, 0, self.size-10)

    def setMouseBtn(self, btn, value):

        """ Ermoeglicht das setzen von Tastendruecken

        :param btn: welche Taste betroffen ist
        :param value: welcher Wert (0 oder 1) die Taste haben soll
        """

        self.mousebtn[btn] = value

    def checkArea(self, size):

        """ Ueberprueft ob sich die Camera aus dem eingeschraengtem Raum bewegt. Der Radius wird als size uebergeben.
        Sollte sich die Camera hinausbewegen wird sie auf den letzten gueltigen Wert gesetzt

        :param size: Groesse des zu ueberpruefenden Raumes
        :return:
        """

        xy = sqrt(base.camera.getX() ** 2 + base.camera.getY() ** 2)
        xyz = sqrt(xy ** 2 + base.camera.getZ() ** 2)

        if xyz > size:
            base.camera.setX(self.lastX)
            base.camera.setY(self.lastY)
            base.camera.setZ(self.lastZ)
        else:
            self.lastX = base.camera.getX()
            self.lastY = base.camera.getY()
            self.lastZ = base.camera.getZ()
