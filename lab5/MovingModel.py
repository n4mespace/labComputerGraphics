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
        self.coords = self.model.get_coords(center=center)

        # This one is for projection curve
        self.COORDS = self.model.get_coords(center=center)

        # Counter for projection curve drawing
        self.i = 0

        # Some needed params for calc
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

    def _move(self, x: float, y: float, i: int) -> tuple:
        '''
        Add speed to one tuple of coords

        :param x, y: tuple of coords
        :param i: self.i which move to next coord
        :return: tuple of moved x, y
        '''
        # Update counter and curve gen
        if self.i == 299:
            self.COORDS = self.model.get_coords(center=self.center)
            self.i = 0

            # Refreshing figure's 'path'
            self.canvas.delete('all')
        return (
            x + self.speed['x'] + (self.COORDS[i][0] - self.COORDS[i-1][0]),
            y + self.speed['y'] + (self.COORDS[i][1] - self.COORDS[i-1][1]))

    def _move_coords(self) -> list:
        '''
        Apply move to all coords

        :return: moved with self.speed coords
        '''
        self.i += 1  # Update movement state
        moved_coords = [
            self._move(x, y, self.i)
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
        Recursively clears self.canvas and add scheduled movements
        '''
        # Clearing from outdated objects
        self.canvas.delete(self.poligone)

        # Draw a movement curve
        self.canvas.create_oval(
            self.center[0]-1,
            self.center[1]-1,
            self.center[0]+1,
            self.center[1]+1,
            width=3, outline='grey'
        )

        # Setting timers on next movements
        self.canvas.after(self.time, self.movement)
        self.canvas.after(self.time, self._default_movement)
        self.canvas.after(self.time, self._rotation_movement)

    def _near_border_X(self, x) -> bool:
        '''
        Checks for border out on x axis

        :param x: coord of center
        :return: true if x is out or false
        '''
        return x >= 1120 or x <= 80

    def _near_border_Y(self, y) -> bool:
        '''
        Checks for border out on y axis

        :param x: coord of center
        :return: true if y is out or false
        '''
        return y >= 820 or y <= 80

    def _default_movement(self) -> None:
        '''
        Perform single move with self.speed
        and refresh self.coords
        '''
        c = self.center

        # Check borders
        if self._near_border_X(x=c[0]):
            self.change_direction(x=True)
        if self._near_border_Y(y=c[1]):
            self.change_direction(y=True)

        # Move coords and center of figure
        self.coords = self._move_coords()
        self.center = self._move(c[0], c[1], self.i)

    def _rotation_movement(self) -> None:
        '''
        Perform single rotation and refresh self.pol
        '''
        self.coords = self._rotate(self.angle)

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
