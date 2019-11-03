import tkinter as tk
import numpy as np
import argparse
import random

from MovingModel import MovingModel as MV_model


def main(A, B, D, size) -> None:
    '''
    Load window with 2 moving figures

    :param A, B, D, size: figure formula params
    '''

    # Creating root and canvas
    window = tk.Tk()
    canvas = tk.Canvas(window, width=1200, height=900, bg='lightgrey')
    canvas.pack()

    # Formula for figure coords
    formula_for_coords = {
        'x': lambda t: ((A - B) * np.cos(t) + D * np.cos((A / B) * t)) * size,
        'y': lambda t: ((A - B) * np.sin(t) - D * np.sin((A / B) * t)) * size,
    }

    # Some figures's params
    speed_1 = {'x': 10, 'y': 5}
    speed_2 = {'x': 5, 'y': 10}

    # Color for random choosing
    colors = ['black', 'yellow', 'red', 'brown', 'blue', 'violet', 'orange']

    # Create 2 models with different start points
    model1 = MV_model(
        canvas, formula_for_coords, speed_1,
        center=(random.randint(100, 400), random.randint(100, 300)),
        timeon=50)
    model2 = MV_model(
        canvas, formula_for_coords, speed_2,
        center=(random.randint(600, 1000), random.randint(500, 800)),
        timeon=50)

    def check_distance():
        '''
        Check if figures are close enough
        and change their speed to opposite by direction
        '''
        center1 = model1.get_center()
        center2 = model2.get_center()

        if (
            abs(center1[0] - center2[0]) <= 180 and
            abs(center1[1] - center2[1]) <= 180
        ):
            model1.change_direction(x=True, y=True)
            model1.change_color(
                colors[random.randint(0, len(colors))-1])

            model2.change_direction(x=True, y=True)
            model2.change_color(
                colors[random.randint(0, len(colors)-1)])

        canvas.after(50, check_distance)

    # Set timer for checking
    canvas.after(50, check_distance)

    # Start program
    window.mainloop()


# Some cli params handles
if __name__ == '__main__':
    parser = argparse.ArgumentParser('Built 2 moving figures')

    parser.add_argument(
        '--A', type=float, default=200)
    parser.add_argument(
        '--B', type=float, default=1)
    parser.add_argument(
        '--D', type=float, default=195)
    parser.add_argument(
        '--size', help="Scale your chart", type=float, default=0.5)

    args = parser.parse_args()

    # Starting point of main script with given params
    main(args.A, args.B, args.D, args.size)
