import numpy as np


class BaseModel():
    '''
    Default class for drawing a figure by formula
    '''
    def __init__(self, formulaXY: dict):
        '''
        Get formulas for X and Y

        :param formulaXY: {x: ..., y: ...}
        '''
        self.formula_x = formulaXY['x']
        self.formula_y = formulaXY['y']

    def get_coords(self, center: tuple, N=300, n=60) -> list:
        '''
        Generate coords with given formulas

        :param N: generation step
        :param n: how many coords to generate
        :param center: step from origin (0 + centerX, 0 + centerY)

        :return: list of tuples (x, y)
        '''
        coords = [
            [  # list of X
                self.formula_x(t) + center[0]
                for t
                in np.linspace(0, n * np.pi, N)
                ],
            [  # list of Y
                self.formula_y(t) + center[1]
                for t
                in np.linspace(0, n * np.pi, N)
                ]
        ]

        return list(zip(coords[0], coords[1]))
