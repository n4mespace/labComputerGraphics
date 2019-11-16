from numpy import cos, sin, pi


class Point3D:
    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = float(x), float(y), float(z)

    def rotateX(self, angle):
        '''
        Rotates the point around the X axis by the given angle in degrees.
        '''
        cosa, sina = self.__get_cosa_sina(angle)
        y = self.y * cosa - self.z * sina
        z = self.y * sina + self.z * cosa
        return Point3D(self.x, y, z)

    def rotateY(self, angle):
        '''
        Rotates the point around the Y axis by the given angle in degrees.
        '''
        cosa, sina = self.__get_cosa_sina(angle)
        z = self.z * cosa - self.x * sina
        x = self.z * sina + self.x * cosa
        return Point3D(x, self.y, z)

    def rotateZ(self, angle):
        '''
        Rotates the point around the Z axis by the given angle in degrees.
        '''
        cosa, sina = self.__get_cosa_sina(angle)
        x = self.x * cosa - self.y * sina
        y = self.x * sina + self.y * cosa
        return Point3D(x, y, self.z)

    def __get_cosa_sina(self, angle):
        rad = angle * pi / 180
        cosa = cos(rad)
        sina = sin(rad)
        return cosa, sina

    def project(self, win_width, win_height, fov, viewer_distance):
        '''
        Transforms this 3D point to 2D using a perspective projection.
        '''
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2
        return Point3D(x, y, self.z)
