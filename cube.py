import pygame
from OpenGL.raw.GLU import gluPerspective
from pygame.locals import *

from OpenGL.GL import *

def welcome():
    pygame.init()
    display = (800, 600)
    welcome_screen = pygame.display.set_mode(display)
    coverimage = pygame.image.load('welcomeimage.png')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 40 < x < 200 and 150 < y < 300:
                    main()
                if 40 < x < 200 and 350 < y < 500:
                    guide()
                if 600 < x < 760 and 150 < y < 300:
                    about()
                if 600 < x < 760 and 350 < y < 500:
                    pygame.quit()
                    quit()
        welcome_screen.blit(coverimage, (0, 0))
        pygame.display.update()


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    NewcompleteCube = completeCube(3, 1.5)
    NewcompleteCube.mainloop()


def guide():
    pygame.init()
    display = (800, 600)
    guide_screen = pygame.display.set_mode(display)
    guideimage = pygame.image.load('guideImage.png')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 10 < y < 100 and 700 < x < 800:
                    welcome()
        guide_screen.blit(guideimage, (0, 0))
        pygame.display.update()


def about():
    pygame.init()
    display = (800, 600)
    about_screen = pygame.display.set_mode(display)
    aboutimage = pygame.image.load('aboutimage.png')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 10 < y < 100 and 700 < x < 800:
                    welcome()
        about_screen.blit(aboutimage, (0, 0))
        pygame.display.update()

vertices = ((1, -1, -1),
            (1, 1, -1),
            (-1, 1, -1), 
            (-1, -1, -1),
            (1, -1, 1),
            (1, 1, 1), 
            (-1, -1, 1),
            (-1, 1, 1))
edges = ((0, 1), 
        (0, 3),
        (0, 4), 
        (2, 1),
        (2, 3), 
        (2, 7),
        (6, 3),
        (6, 4),
        (6, 7),
        (5, 1), 
        (5, 4), 
        (5, 7))
surfaces = ((0, 1, 2, 3), 
            (3, 2, 7, 6), 
            (6, 7, 5, 4), 
            (4, 5, 1, 0),
            (1, 5, 7, 2), 
            (4, 0, 3, 6))
colors = ((1, 0, 0), 
            (0, 1, 0), 
            (1, 0.5, 0),
            (1, 1, 0), 
            (1, 1, 1), 
            (0, 0, 1))


class Cube():
    def __init__(self, pos, N, scale):
        self.N = N
        self.scale = scale
        self.init_pos = [*pos]
        self.current_pos = [*pos]
        self.rot = [[1 if i == j else 0 for i in range(3)] for j in range(3)]

    def isRotated(self, axis, slice, dir):
        return self.current_pos[axis] == slice

    def update(self, axis, slice, dir):

        if not self.isRotated(axis, slice, dir):
            return

        i, j = (axis + 1) % 3, (axis + 2) % 3
        for k in range(3):
            self.rot[k][i], self.rot[k][j] = -self.rot[k][j] * dir, self.rot[k][i] * dir

        self.current_pos[i], self.current_pos[j] = (
            self.current_pos[j] if dir < 0 else self.N - 1 - self.current_pos[j],
            self.current_pos[i] if dir > 0 else self.N - 1 - self.current_pos[i])

    def transformationMatrix(self):
        scale1 = [[s * self.scale for s in a] for a in self.rot]
        scaleT = [(p - (self.N - 1) / 2) * 2.1 * self.scale for p in self.current_pos]
        return [*scale1[0], 0, *scale1[1], 0, *scale1[2], 0, *scaleT, 1]

    def draw(self, col, surf, vert, animate, angle, axis, slice, dir):

        glPushMatrix()
        if animate and self.isRotated(axis, slice, dir):
            glRotatef(angle * dir, *[1 if i == axis else 0 for i in range(3)])
        glMultMatrixf(self.transformationMatrix())

        glBegin(GL_QUADS)
        for i in range(len(surf)):
            glColor3fv(colors[i])
            for j in surf[i]:
                glVertex3fv(vertices[j])
        glEnd()

        glPopMatrix()


class completeCube:
    def __init__(self, N, scale):
        self.N = N
        createCube = range(self.N)
        self.cubes = [Cube((x, y, z), self.N, scale) for x in createCube for y in createCube for z in createCube]

    def mainloop(self):

        rot_cube_map = {K_UP: (-1, 0), K_DOWN: (1, 0), K_LEFT: (0, -1), K_RIGHT: (0, 1)}
        rot_slice_map = {
            K_1: (0, 0, 1), K_2: (0, 1, 1), 
            K_3: (0, 2, 1), K_4: (1, 0, 1), 
            K_5: (1, 1, 1), K_6: (1, 2, 1), 
            K_7: (2, 0, 1), K_8: (2, 1, 1), 
            K_9: (2, 2, 1),K_F1: (0, 0, -1),
            K_F2: (0, 1, -1), K_F3: (0, 2, -1),
             K_F4: (1, 0, -1), K_F5: (1, 1, -1),
            K_F6: (1, 2, -1), K_F7: (2, 0, -1), 
            K_F8: (2, 1, -1), K_F9: (2, 2, -1),
        }

        ang_x, ang_y, rot_cube = 0, 0, (0, 0)
        animate, animate_ang, animate_speed = False, 0, 5
        action = (0, 0, 0)
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == KEYDOWN:
                    if event.key in rot_cube_map:
                        rot_cube = rot_cube_map[event.key]
                    if not animate and event.key in rot_slice_map:
                        animate, action = True, rot_slice_map[event.key]
                if event.type == KEYUP:
                    if event.key in rot_cube_map:
                        rot_cube = (0, 0)

            ang_x += rot_cube[0] * 2
            ang_y += rot_cube[1] * 2

            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            glTranslatef(0, 0, -40)
            glRotatef(ang_y, 0, 1, 0)
            glRotatef(ang_x, 1, 0, 0)

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            if animate:
                if animate_ang >= 90:
                    for cube in self.cubes:
                        cube.update(*action)
                    animate, animate_ang = False, 0

            for cube in self.cubes:
                cube.draw(colors, surfaces, vertices, animate, animate_ang, *action)
            if animate:
                animate_ang += animate_speed

            pygame.display.flip()
            pygame.time.wait(10)


if __name__ == '__main__':
    welcome()

