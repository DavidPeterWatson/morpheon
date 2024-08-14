
import numpy
import numpy as np
import matplotlib.pyplot as plt

from airfoils import Airfoil


def create(nacas, flex_distance):
    foils = []
    foil = Airfoil.NACA4(nacas[0])
    reference_length = get_length(foil._x_upper, foil._y_upper)
    for naca in nacas:
        foil = Airfoil.NACA4(naca)
        length = get_length(foil._x_upper, foil._y_upper)
        scale = length/reference_length
        foil.scale_data_points(scale)
        flex_foil = get_flex_foil(foil, flex_distance)
        foils.append(foil)
        foils.append(flex_foil)


    plot(foils)


def get_flex_foil(foil: Airfoil, flex_distance):
    x_upper_flex_points, y_upper_flex_points = get_flex_points(foil._x_upper, foil._y_upper, flex_distance)
    x_lower_flex_points, y_lower_flex_points = get_flex_points(foil._x_lower, foil._y_lower, flex_distance)
    upper = np.array((x_upper_flex_points, y_upper_flex_points))
    lower = np.array((x_lower_flex_points, y_lower_flex_points))
    return Airfoil(upper, lower)


def get_length(x_points, y_points):
    array_length = x_points.shape[0]
    previouspoint = np.array((0, 0))
    accumulated_dist = 0
    for i in range(array_length):
        x = x_points[i]
        y = y_points[i]
        point = np.array((x, y))
        accumulated_dist += distance(previouspoint, point)
        previouspoint = point
    return accumulated_dist


def get_flex_points(x_points, y_points, spacing):
    array_length = x_points.shape[0]
    previouspoint = np.array((0, 0))
    accumulated_dist = 0
    x_flex_points = np.array(0)
    y_flex_points = np.array(0)
    for i in range(array_length):
        x = x_points[i]
        y = y_points[i]
        point = np.array((x, y))
        accumulated_dist += distance(previouspoint, point)
        previouspoint = point
        if accumulated_dist > spacing:
            x_flex_points = np.append(x_flex_points, x)
            y_flex_points = np.append(y_flex_points, y)
            accumulated_dist = 0
    x_flex_points = np.append(x_flex_points, x_points[-1])
    y_flex_points = np.append(y_flex_points, y_points[-1])
    return x_flex_points, y_flex_points


def distance(point_a, point_b):
    return np.linalg.norm(point_a-point_b)


def plot(foils):

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlim([0, 1])
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.axis('equal')
    ax.grid()

    for foil in foils:
        ax.plot(foil._x_upper, foil._y_upper, marker='o', linewidth=1)
        ax.plot(foil._x_lower, foil._y_lower, marker='o', linewidth=1)

    # if settings.get('points', False):
    #     ax.plot(self.all_points[0, :], self.all_points[1, :], '.', color='grey')

    # if settings.get('camber', False):
        x = np.linspace(0, 1, int(200/2))
        ax.plot(x, foil.camber_line(x), '--')

    # if settings.get('chord', False):
    #     pass

    plt.subplots_adjust(left=0.10, bottom=0.10, right=0.98, top=0.98, wspace=None, hspace=None)

    plt.show()

# create(('0006', '4021', '0021'), 0.15)
# create(('3321', '3121', '5321', '5121'), 0.15)
create(('0021', '0006'), 0.15)
