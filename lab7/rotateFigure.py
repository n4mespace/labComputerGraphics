from numpy import pi
from Simulation import Simulation


if __name__ == '__main__':
    # Speed of rotation can be changed with
    # different angles for axes
    Simulation(
        angle_X=pi/3,
        angle_Y=pi/6,
        angle_Z=pi/9,
    ).run()
