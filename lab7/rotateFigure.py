from numpy import pi
from Simulation import Simulation


if __name__ == '__main__':
    # Speed of rotation can be changed with
    # different angles for axes
    Simulation(
        angle_X=pi/9,
        angle_Y=pi/3,
        angle_Z=pi/6,
    ).run()
