import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1),
    (0.333, -1, -1),
    (0.333, 1, -1),
    (0.333, 1, 1),
    (0.333, -1, 1),

    (-0.333, -1, -1),
    (-0.333, 1, -1),
    (-0.333, 1, 1),
    (-0.333, -1, 1),

    (-1, -0.333, -1),
    (1, -0.333, -1),
    (1, -0.333, 1),
    (-1, -0.333, 1),

    (-1, 0.333, -1),
    (1, 0.333, -1),
    (1, 0.333, 1),
    (-1, 0.333, 1),

    (-1, -1, -0.333),
    (1, -1, -0.333),
    (1, 1, -0.333),
    (-1, 1, -0.333),

    (-1, -1, 0.333),
    (1, -1, 0.333),
    (1, 1, 0.333),
    (-1, 1, 0.333),
    )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7),
    (8,9),
    (9,10),
    (10,11),
    (11,8),
    (12,13),
    (13,14),
    (14,15),
    (15,12),

    (16, 17),
    (17, 18),
    (18, 19),
    (19, 16),

    (20, 21),
    (21, 22),
    (22, 23),
    (23, 20),

    (24, 25),
    (25, 26),
    (26, 27),
    (27, 24),

    (28, 29),
    (29, 30),
    (30, 31),
    (31, 28),
    )

def Cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])

    glEnd()

def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Cube()
        pygame.display.flip()
        pygame.time.wait(10)


main()
