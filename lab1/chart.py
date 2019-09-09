import tkinter as tk
import math
import argparse
from square import Square as model


def create_square(
    canv: tk.Canvas, models: model,
    angle: float, color: str,
    center=True, k=0
):
    m = models[0].rotate(angle, center=center)

    canv.create_line(
        m[0][0]-k, m[0][1]-k, m[1][0]-k, m[1][1]-k, fill=color)
    canv.create_line(
        m[0][0]-k, m[0][1]-k, m[2][0]-k, m[2][1]-k, fill=color)
    canv.create_line(
        m[2][0]-k, m[2][1]-k, m[-1][0]-k, m[-1][1]-k, fill=color)
    canv.create_line(
        m[1][0]-k, m[1][1]-k, m[-1][0]-k, m[-1][1]-k, fill=color)

    canv.pack()


def main(n, m, k):
    app = tk.Tk()

    coords = [  # (x1, y1), (x2, y2), (x3, y3), (x4, y4)
        (
            (100 * k, 100 * k), (100 * k, 300 * k),
            (300 * k, 100 * k), (300 * k, 300 * k)
        ),
    ]

    models = [
        model(a1, a2, a3, a4) for (a1, a2, a3, a4) in coords
    ]

    canv = tk.Canvas(app, width=700, height=700)
    switch = True

    for angle in [math.pi / m * i for i in range(-m, m)]:
        create_square(
            canv, models, angle, 'red' if switch else 'white', center=False)
        switch = not switch

    for angle in [math.pi / n * i for i in range(-n, n)]:
        create_square(
            canv, models, angle, 'black' if switch else 'red', k=-120)
        switch = not switch

    app.mainloop()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        'Built different charts with sqaures acording to params')
    parser.add_argument(
        '--n', help='Initialize num for center rotation', type=int, default=10)
    parser.add_argument(
        '--m', help='Initialize num for corner rotation', type=int, default=10)
    parser.add_argument(
        '--k', help='Initialize scale for chart', type=float, default=1.2)

    args = parser.parse_args()
    main(args.n, args.m, args.k)
