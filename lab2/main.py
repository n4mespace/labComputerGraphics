import tkinter as tk
import numpy as np
import argparse
from model import Model as model


def main(n, colors, preset, A, B, D, size):
    window = tk.Tk()

    formula_for_coords = {
        'x': lambda t: ( (A - B) * np.cos(t) + D * np.cos((A / B) * t) ) * size,
        'y': lambda t: ( (A - B) * np.sin(t) - D * np.sin((A / B) * t) ) * size,
    }

    mdl = model(formula_for_coords)
    canv = tk.Canvas(window, width=800, height=800)
    switch = False

    for angle in [np.pi / n * i for i in range(0, n)]:
        mdl.create_model(canv, angle, colors[switch], N=300)
        switch = not switch

    window.mainloop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        'Built different charts with sqaures acording to params')
    parser.add_argument(
        '--n', help='Initialize num for corner rotation', type=int, default=1)
    parser.add_argument(
        '--colors', help='Initialize colors for center rotation',
        type=str, default=['black', 'black'], nargs=2)
    parser.add_argument(
        '--preset', help='Initialize some default charts',
        type=int, default=None)
    parser.add_argument(
        '--A', type=float, default=200)
    parser.add_argument(
        '--B', type=float, default=1)
    parser.add_argument(
        '--D', type=float, default=195)
    parser.add_argument(
        '--size', help="Scale your chart", type=float, default=0.5)
    
    args = parser.parse_args()
    
    main(
        args.n, args.colors, 
        args.preset, args.A, 
        args.B, args.D, args.size
        )
