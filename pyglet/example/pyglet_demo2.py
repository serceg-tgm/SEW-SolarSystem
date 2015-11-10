#!/usr/bin/env python
"""This script shows another example of using the PyWavefront module."""
# This example was created by intrepid94
import sys
sys.path.append('..')
import ctypes

import pyglet
from pyglet.gl import *
from pyglet.window import key

from pywavefront import Wavefront

rotation = 0
meshes = Wavefront('earth.obj')
window = pyglet.window.Window(1024, 720, caption = 'Demo', resizable = True)
lightfv = ctypes.c_float * 4
label = pyglet.text.Label('Hello, world', font_name = 'Times New Roman', font_size = 12, x = 800, y = 700, anchor_x = 'center', anchor_y = 'center')

def opengl_init():
    """ Initial OpenGL configuration.
    """
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glDepthFunc(GL_LEQUAL)


class camera(object):
    """ A camera.
    """
    mode = 1
    x, y, z = 0, 0, 512
    rx, ry, rz = 30, -45, 0
    w, h = 640, 480
    far = 8192
    fov = 60

    def view(self, width, height):
        """ Adjust window size.
        """
        self.w, self.h = width, height
        glViewport(0, 0, width, height)
        print("Viewport " + str(width) + "x" + str(height))
        if self.mode == 2:
            self.isometric()
        elif self.mode == 3:
            self.perspective()
        else:
            self.default()

    def default(self):
        """ Default pyglet projection.
        """
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.w, 0, self.h, -1, 1)
        glMatrixMode(GL_MODELVIEW)

    def isometric(self):
        """ Isometric projection.
        """
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-self.w/2., self.w/2., -self.h/2., self.h/2., 0, self.far)
        glMatrixMode(GL_MODELVIEW)

    def perspective(self):
        """ Perspective projection.
        """
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.fov, float(self.w)/self.h, 0.1, self.far)
        glMatrixMode(GL_MODELVIEW)

    def key(self, symbol, modifiers):
        """ Key pressed event handler.
        """
        if symbol == key.F1:
            self.mode = 1
            self.default()
            print("Projection: Pyglet default")
        elif symbol == key.F2:
            print("Projection: 3D Isometric")
            self.mode = 2
            self.isometric()
        elif symbol == key.F3:
            print("Projection: 3D Perspective")
            self.mode = 3
            self.perspective()
        elif self.mode == 3 and symbol == key.NUM_SUBTRACT:
            self.fov -= 1
            self.perspective()
        elif self.mode == 3 and symbol == key.NUM_ADD:
            self.fov += 1
            self.perspective()
        else: print("KEY " + key.symbol_string(symbol))

    def drag(self, x, y, dx, dy, button, modifiers):
        """ Mouse drag event handler.
        """
        if button == 1:
            self.x -= dx*2
            self.y -= dy*2
        elif button == 2:
            self.x -= dx*2
            self.z -= dy*2
        elif button == 4:
            self.ry += dx/4.
            self.rx -= dy/4.

    def apply(self):
        """ Apply camera transformation.
        """
        glLoadIdentity()
        if self.mode == 1: return
        glTranslatef(-self.x, -self.y, -self.z)
        glRotatef(self.rx, 1, 0, 0)
        glRotatef(self.ry, 0, 1, 0)
        glRotatef(self.rz, 0, 0, 1)

opengl_init()
cam = camera()
on_resize = cam.view
on_key_press = cam.key
on_mouse_drag = cam.drag

@window.event
def on_resize(width, height):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(40.0, float(width)/height, 1, 100.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)
    return True

@window.event
def on_draw():
    window.clear()
    glLoadIdentity()
    glLightfv(GL_LIGHT0, GL_POSITION, lightfv(-40, 200, 100, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, lightfv(0.2, 0.2, 0.2, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightfv(0.5, 0.5, 0.5, 1.0))
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glMatrixMode(GL_MODELVIEW)
    # glTranslated(0, 4, -8)
 #    glRotatef(90, 0, 1, 0)
 #    glRotatef(-60, 0, 0, 1)
   # Rotations for sphere on axis - useful
    glTranslated(0, .8, -20)
    glRotatef(-66.5, 0, 0, 1)
    glRotatef(rotation, 1, 0, 0)
    glRotatef(90, 0, 0, 1)
    glRotatef(0, 0, 1, 0)
    meshes.draw()

    # glEnable(GL_DEPTH_TEST)
    # glDisable(GL_DEPTH_TEST)


    on_resize = cam.view
    on_key_press = cam.key
    on_mouse_drag = cam.drag

def update(dt):
    global rotation
    rotation += 45 * dt
    if rotation > 720: 
       rotation = 0







def x_array(list):
    """ Converts a list to GLFloat list.
    """
    return (GLfloat * len(list))(*list)

def draw_vertex_array(vertices, colors, mode=GL_LINES):
    """ Draw a vertex array.
    """
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)
    glColorPointer(4, GL_FLOAT, 0, colors)
    glVertexPointer(3, GL_FLOAT, 0, vertices)
    glDrawArrays(GL_QUADS, 0, round(len(vertices)/3))
    # glDrawArrays(GL_QUADS, 0, 0)
    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_COLOR_ARRAY)


pyglet.clock.schedule(update)

print("OpenGL Projections")
print("---------------------------------")
print("Projection matrix -> F1, F2, F3")
print("Camera -> Drag LMB, CMB, RMB")
print("")
pyglet.app.run()
