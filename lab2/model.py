import numpy as np


class Model():
    '''
    Default class for using in ornament
    '''
    def __init__(self, formulaXY: dict):
        self.formula_x = formulaXY['x']
        self.formula_y = formulaXY['y']

    def get_coords(self, N: int) -> dict:
        return {
            'x': [
                self.formula_x(t)
                for t
                in np.linspace(0, 60 * np.pi, N)
                ],
            'y': [
                self.formula_y(t)
                for t
                in np.linspace(0, 60 * np.pi, N)
                ],
        }

    def _get_center_coords(self) -> tuple:
        return (400, 400)  # for window 800x800

    def _transform(self, x: float, y: float, angle: float) -> tuple:
        transformed_x = x * np.cos(angle) - y * np.sin(angle)
        transformed_y = x * np.sin(angle) + y * np.cos(angle)

        return transformed_x, transformed_y

    def rotate(self, angle: float, N: int) -> list:
        coords = self.get_coords(N)

        rotated_coords = [
            self._transform(x, y, angle)
            for x, y
            in zip(coords['x'], coords['y'])
            ]

        return rotated_coords

    def create_model(self, canv, angle: float, color: str, N: int):
        m = self.rotate(angle, N)
        center = self._get_center_coords()

        for i in range(1, len(m)):
            canv.create_line(
                m[i-1][0] + center[0],
                m[i-1][1] + center[0],
                m[i][0] + center[0],
                m[i][1] + center[0],
                fill=color
                )

        canv.pack(fill='both', expand=True)
