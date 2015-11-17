from panda3d.core import TextNode, Vec3, Vec4
from direct.task.Task import Task
from pandac.PandaModules import WindowProperties

class Camera(object):
    def __init__(self):
        self.focus = Vec3(55,-55,20)
        self.heading = 180
        self.pitch = 0
        self.mousex = 0
        self.mousey = 0
        self.last = 0
        self.mousebtn = [0,0,0,0,0,0]
        base.camera.setPos(-14, -31, 10)
        WindowProperties().setCursorHidden(True)


    def controlCamera(self, task):
        # figure out how much the mouse has moved (in pixels)
        md = base.win.getPointer(0)
        x = md.getX()
        y = md.getY()
        if base.win.movePointer(0, 100, 100):
            self.heading = self.heading - (x - 100) * 0.2
            self.pitch = self.pitch - (y - 100) * 0.2
        if (self.pitch < -90): self.pitch = -90
        if (self.pitch >  90): self.pitch =  90
        base.camera.setHpr(self.heading,self.pitch,0)
        dir = base.camera.getMat().getRow3(1)
        elapsed = task.time - self.last
        if (self.last == 0): elapsed = 0
        if (self.mousebtn[0]):
            self.focus = self.focus + dir * elapsed*30
        if self.mousebtn[1]:
            self.focus = self.focus - dir * elapsed*30

        base.camera.setPos(self.focus - (dir*5))

        if self.mousebtn[2]:
            base.camera.setX(base.camera, -elapsed*30)
        if self.mousebtn[3]:
            base.camera.setX(base.camera, elapsed*30)
        if self.mousebtn[4]:
            base.camera.setZ(base.camera, elapsed*30)
        if self.mousebtn[5]:
            base.camera.setZ(base.camera, -elapsed*30)

        self.focus = base.camera.getPos() + (dir*5)
        self.last = task.time
        return Task.cont

    def setMouseBtn(self, btn, value):
        self.mousebtn[btn] = value