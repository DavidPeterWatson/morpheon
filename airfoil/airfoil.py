from airfoils import Airfoil
import numpy
import numpy as np
import matplotlib.pyplot as plt


def create(nacas, flex_distance):
    foils = []
    for naca in nacas:
        foil = Airfoil.NACA4(naca)
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

def gen_NACA4_airfoil(p, m, xx, n_points):
    """
    Generate upper and lower points for a NACA 4 airfoil

    Args:
        :p:
        :m:
        :xx:
        :n_points:

    Returns:
        :upper: 2 x N array with x- and y-coordinates of the upper side
        :lower: 2 x N array with x- and y-coordinates of the lower side
    """

    def yt(xx, xsi):
        # Thickness distribution

        a0 = 1.4845
        a1 = 0.6300
        a2 = 1.7580
        a3 = 1.4215
        a4 = 0.5075

        return xx*(a0*np.sqrt(xsi) - a1*xsi - a2*xsi**2 + a3*xsi**3 - a4*xsi**4)

    def yc(p, m, xsi):
        # Camber line

        def yc_xsi_lt_p(xsi):
            return (m/p**2)*(2*p*xsi - xsi**2)

        def dyc_xsi_lt_p(xsi):
            return (2*m/p**2)*(p - xsi)

        def yc_xsi_ge_p(xsi):
            return (m/(1 - p)**2)*(1 - 2*p + 2*p*xsi - xsi**2)

        def dyc_xsi_ge_p(xsi):
            return (2*m/(1 - p)**2)*(p - xsi)

        yc = np.array([yc_xsi_lt_p(x) if x < p else yc_xsi_ge_p(x) for x in xsi])
        dyc = np.array([dyc_xsi_lt_p(x) if x < p else dyc_xsi_ge_p(x) for x in xsi])

        return yc, dyc

    xsi = np.linspace(0, 1, n_points)

    yt = yt(xx, xsi)
    yc, dyc = yc(p, m, xsi)
    theta = np.arctan(dyc)

    x_upper = xsi - yt*np.sin(theta)
    y_upper = yc + yt*np.cos(theta)
    x_lower = xsi + yt*np.sin(theta)
    y_lower = yc - yt*np.cos(theta)

    upper = np.array([x_upper, y_upper])
    lower = np.array([x_lower, y_lower])

    return upper, lower


def plot(foils):

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlim([0, 1])
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.axis('equal')
    ax.grid()

    for foil in foils:
        ax.plot(foil._x_upper, foil._y_upper, '-')
        ax.plot(foil._x_lower, foil._y_lower, '-')

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
create(('0021', '5521'), 0.15)
