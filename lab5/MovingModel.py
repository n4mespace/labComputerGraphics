import numpy as np
from BaseModel import BaseModel


class MovingModel():
    '''
    Simulate movement of figure with time
    '''
    def __init__(
            self, canvas, formulaXY: dict, speed: dict,
            center: tuple, timeon: int, color='black'):
        '''
        Initialize parameters for figure drawing

        :param canvas:TK object to draw in
        :param formulaXY: dict with formulas like {x: ..., y: ...}
        :param speed: dict with values which changes figure
            coords like {x: ..., y: ...}
        :param center: step from origin (0 + centerX, 0 + centerY)
        :param timeon: delay for drawing
        :param color: color to fill the figure
        '''
        self.canvas = canvas

        # Model which gives starting coords
        self.model = BaseModel(formulaXY)
        self.coords = self.model.get_coords(N=300, center=center)

        self.center = center
        self.time = timeon
        self.angle = np.pi / 3
        self.speed = speed
        self.color = color

        # Main object which changes on canvas
        self.poligone = self.canvas.create_polygon(
            self.coords, outline=self.color)

        # Call recursive draw of self.poligone
        self.movement()

    def get_center(self) -> tuple:
        '''
        Using to know figure coords on canvas in particular time

        :return: tuple of center coords
        '''
        return self.center

    def _move(self, x: float, y: float) -> tuple:
        '''
        Add speed to one tuple of coords

        :param x, y: tuple of coords
        :return: tuple of moved x, y
        '''
        return (
            x + self.speed['x'],
            y + self.speed['y'])

    def _move_coords(self) -> list:
        '''
        Apply move to all coords

        :return: moved with self.speed coords
        '''
        moved_coords = [
            self._move(x, y)
            for x, y
            in self.coords
            ]

        return moved_coords

    def _transform_for_rotation(
            self, x: float, y: float, angle: float) -> tuple:
        '''
        Add transform one tuple of coords

        :param x, y: tuple of coords
        :param angle: value of total rotation
        :return: tuple of transformed coords
        '''
        # Move coords to the center
        x = x - self.center[0]
        y = y - self.center[1]

        # Perform rotation
        transformed_x = x * np.cos(angle) - y * np.sin(angle)
        transformed_y = x * np.sin(angle) + y * np.cos(angle)

        # Move coords back
        transformed_x += self.center[0]
        transformed_y += self.center[1]

        return (transformed_x, transformed_y)

    def _rotate(self, angle: float) -> list:
        '''
        Apply rotation on all coords

        :param angel: value of total rotation
        :return: rotated tuples of coords
        '''
        rotated_coords = [
            self._transform_for_rotation(x, y, angle)
            for x, y
            in self.coords
            ]

        return rotated_coords

    def movement(self) -> None:
        '''
        Recursively clears self.canvas and add scheduled move to figure
        '''
        self.canvas.delete(self.poligone)
        self.canvas.after(self.time, self.movement)
        self.canvas.after(self.time, self._default_movement)
        self.canvas.after(self.time, self._rotation_movement)

    def _near_border_X(self, x) -> bool:
        '''
        Checks for border out on x axis

        :param x: coord of center
        :return: true if x is out or false
        '''
        return x >= 1150 or x <= 50

    def _near_border_Y(self, y) -> bool:
        '''
        Checks for border out on y axis

        :param x: coord of center
        :return: true if y is out or false
        '''
        return y >= 850 or y <= 50

    def _default_movement(self) -> None:
        '''
        Perform single move with self.speed
        and refresh self.coords
        '''
        self.canvas.move(self.poligone, self.speed['x'], self.speed['y'])

        c = self.center

        # Check borders
        if self._near_border_X(x=c[0]):
            self.change_direction(x=True)
        if self._near_border_Y(y=c[1]):
            self.change_direction(y=True)

        # Move coords and center of figure
        self.coords = self._move_coords()
        self.center = self._move(c[0], c[1])

    def _rotation_movement(self) -> None:
        '''
        Perform single rotation and refresh self.pol
        '''
        self.coords = self._rotate(self.angle, N=300)

        # Initialize new self.pol with rotated coords
        self.poligone = self.canvas.create_polygon(
            self.coords, outline=self.color)

    def change_direction(self, x=False, y=False) -> None:
        '''
        Change speed direction to opposite when borders near
        or other figure near

        :param x, y: show which speed axis to change
        '''
        if x:
            self.speed['x'] = -self.speed['x']
        if y:
            self.speed['y'] = -self.speed['y']

    def change_color(self, color) -> None:
        '''
        Change color of figure

        :param color: some new color
        '''
        self.color = color
