import math


class Square():
    '''
    Default class for using in ornament
    '''
    def __init__(
        self, a1: tuple, a2: tuple, a3: tuple, a4: tuple
    ):
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3
        self.a4 = a4

    def get_coords(self) -> tuple:
        return self.a1, self.a2, self.a3, self.a4

    def _get_diag_coords(self) -> tuple:
        return self.a1[0], self.a1[1], self.a4[0], self.a4[1]

    def _get_center_coords(self) -> tuple:
        diag = self._get_diag_coords()
        return (diag[0] + diag[2]) / 2, (diag[1] + diag[3]) / 2

    def _get_corner_coords(self) -> tuple:
        diag = self._get_diag_coords()
        return diag[-2], diag[-1]

    def _transform(
        self, x: tuple, y: tuple, center: tuple, angle: float
    ) -> tuple:
        x -= center[0]
        y -= center[1]

        temp_x = x * math.cos(angle) - y * math.sin(angle)
        temp_y = x * math.sin(angle) + y * math.cos(angle)

        return temp_x + center[0], temp_y + center[1]

    def rotate(self, angle: float, center=True) -> list:
        center = (self._get_corner_coords(), self._get_center_coords())[center]

        rotated_coords = [
            self._transform(x, y, center, angle)
            for x, y
            in self.get_coords()
            ]

        return rotated_coords
