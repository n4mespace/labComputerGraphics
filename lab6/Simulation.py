from numpy import mean
import sys
import pygame
from operator import itemgetter
from Point3D import Point3D


class Simulation:
    def __init__(self, angle_X, angle_Y, angle_Z,
                 win_width=1000, win_height=720):
        pygame.init()

        self.screen = pygame.display.set_mode((win_width, win_height))
        pygame.display.set_caption(
            'Simulation of rotating 3D Cube + Pyramid')
        self.screen.set_alpha(None)

        self.clock = pygame.time.Clock()

        move_to_center = 2  # Makes figure rotate over pyramid's top
        self.vertices = [
            Point3D(move_to_center-1, 1, -1),
            Point3D(move_to_center+1, 1, -1),
            Point3D(move_to_center+1, -1, -1),
            Point3D(move_to_center-1, -1, -1),
            Point3D(move_to_center-1, 1, 1),
            Point3D(move_to_center+1, 1, 1),
            Point3D(move_to_center+1, -1, 1),
            Point3D(move_to_center-1, -1, 1),

            # Pyramid top Point
            Point3D(move_to_center-2, 0, 0),
        ]

        # Define the vertices that compose each of the 6 faces(sides).
        # These numbers are indices to the vertices list defined above
        self.faces = [
            # Cube's sides
            (0, 1, 2, 3), (1, 5, 6, 2), (5, 4, 7, 6),
            (0, 4, 5, 1), (3, 2, 6, 7),

            # Pyramid's sides
            (8, 0, 4, 4), (8, 0, 3, 3), (8, 7, 3, 3), (8, 7, 4, 4)
        ]

        # Define colors for each face
        self.colors = [
            # Pyramid's side colors
            (250, 0, 0), (210, 0, 0), (170, 0, 0),
            (130, 0, 0), (90, 0, 0),

            # Pyramid's side colors
            (0, 250, 0), (0, 180, 0), (0, 110, 0), (0, 30, 0),
        ]

        # Starting angles
        self.angleX = 0
        self.angleY = 0
        self.angleZ = 0

        # Value which will update angle on each iteration
        self.angle_rotation_X = angle_X
        self.angle_rotation_Y = angle_Y
        self.angle_rotation_Z = angle_Z

    def run(self):
        ''' Main Loop '''
        while True:
            events = pygame.event.get()
            if any(event.type == pygame.QUIT for event in events):
                pygame.quit()
                sys.exit()

            self.clock.tick(100)
            self.screen.fill((0, 0, 0))

            # It will hold transformed vertices
            t = []

            for v in self.vertices:
                # Rotate the point around X axis, then around Y axis
                # and finally around Z axis
                rotation = v

                # Checking which axes needs rotation
                if self.angle_rotation_X:
                    rotation = rotation.rotateX(self.angleX)
                if self.angle_rotation_Y:
                    rotation = rotation.rotateY(self.angleY)
                if self.angle_rotation_Z:
                    rotation = rotation.rotateZ(self.angleZ)

                # Transform the point from 3D to 2D
                p = rotation.project(self.screen.get_width(),
                                     self.screen.get_height(), 256, 4)

                # Put the point in the list of transformed vertices
                t.append(p)

            # Calculate the average Z values of each face
            avg_z = [
                [i, mean(t[f[0]].z + t[f[1]].z + t[f[2]].z + t[f[3]].z)]
                for i, f
                in enumerate(self.faces)
            ]

            # Draw the faces using the Painter's algorithm:
            #   distant faces are drawn before the closer ones
            key = itemgetter(1)
            for index_and_avg in sorted(avg_z, key=key, reverse=True):
                face_index = index_and_avg[0]  # Getting index
                f = self.faces[face_index]

                point_list = [
                    (t[f[0]].x, t[f[0]].y), (t[f[1]].x, t[f[1]].y),
                    (t[f[1]].x, t[f[1]].y), (t[f[2]].x, t[f[2]].y),
                    (t[f[2]].x, t[f[2]].y), (t[f[3]].x, t[f[3]].y),
                    (t[f[3]].x, t[f[3]].y), (t[f[0]].x, t[f[0]].y),
                    ]

                pygame.draw.polygon(
                    self.screen, self.colors[face_index], point_list)

            # Updating rotation angles
            self.angleX += self.angle_rotation_X
            self.angleY += self.angle_rotation_Y
            self.angleZ += self.angle_rotation_Z

            pygame.display.update()
