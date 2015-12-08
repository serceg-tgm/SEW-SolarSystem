from panda3d.core import TextNode, Vec3, Vec4
from direct.task.Task import Task
from pandac.PandaModules import WindowProperties
from math import *


class Camera(object):
    def __init__(self, render, size):
        base.win.movePointer(0, 0, 0)
        base.disableMouse()
        self.size = size
        self.focus = Vec3(-14, -31, 10)
        self.heading = -45
        self.pitch = -35
        self.mousex = 0
        self.mousey = 0
        self.last = 0
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
        # figure out how much the mouse has moved (in pixels)


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
        elapsed = task.time - self.last
        if (self.last == 0): elapsed = 0

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

        self.last = task.time
        self.lastX = base.camera.getX()
        self.lastY = base.camera.getY()
        self.lastZ = base.camera.getZ()
        return Task.cont

    def birdPerspective(self):
        self.pitch = -90
        self.focus = Vec3(0, 0, self.size-10)

    def setMouseBtn(self, btn, value):
        self.mousebtn[btn] = value

    def checkArea(self, size):

        # Satz des Pythagoras
        xy = sqrt(base.camera.getX() ** 2 + base.camera.getY() ** 2)
        xyz = sqrt(xy ** 2 + base.camera.getZ() ** 2)

        # print("Size: %f", size)
        # print("X: %f", base.camera.getX())
        # print("Y: %f", base.camera.getY())
        # print("Z: %f", base.camera.getZ())
        # print("r: %f", xyz)

        if xyz > size:
            base.camera.setX(self.lastX)
            base.camera.setY(self.lastY)
            base.camera.setZ(self.lastZ)
            # self.focus = Vec3(self.lastX, self.lastY, self.lastZ)
