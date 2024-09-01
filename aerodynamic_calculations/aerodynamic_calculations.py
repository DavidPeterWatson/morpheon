import math


def calculate_aspect_ratio(wingspan, root_chord, tip_chord):
    area = (root_chord + tip_chord) / 2 * wingspan
    return pow(wingspan, 2) / area


def calculate_taper_ratio(root_chord, tip_chord):
    return tip_chord / root_chord


def calculate_ideal_taper_ratio():
    return 0.4


def calculate_tip_chord(root_chord, taper_ratio):
    return root_chord * taper_ratio


# https://www.airfieldmodels.com/information_source/math_and_science_of_model_aircraft/formulas/mean_aerodynamic_chord.htm
def calculate_mean_aerodynamic_chord(root_chord, taper_ratio):
    return root_chord * 2 / 3 * ((1 + taper_ratio + pow(taper_ratio, 2)) / (1 + taper_ratio))


def calculate_mean_aerodynamic_chord_distance(wingspan, root_chord, mean_aerodynamic_chord, tip_chord):
    return wingspan / 2 * (root_chord - mean_aerodynamic_chord) / (root_chord - tip_chord)


def calculate_sweep_angle(nuetral_point, mean_aerodynamic_chord_distance, mean_aerodynamic_chord):
    mean_chord_leading_edge_point = nuetral_point - 1 / 4 * mean_aerodynamic_chord
    return math.atan(mean_chord_leading_edge_point / mean_aerodynamic_chord_distance)


def calculate_sweep_distance(wingspan, sweep_angle):
    return math.tan(sweep_angle) * wingspan / 2 
    

def calculate_center_of_gravity(nuetral_point, static_margin):
    return nuetral_point * 0.9 - nuetral_point * static_margin


def calculate_wing_area(wingspan, root_chord, tip_chord):
    return (root_chord + tip_chord) / 2 * wingspan


def calculate_wing_loading(gross_weight, wing_area):
    return gross_weight / wing_area


def calculate_lift(coefficient_of_lift, wing_area, density, velocity):
    return coefficient_of_lift * wing_area * 0.5 * density * pow(velocity, 2)


def calculate_velocity(coefficient_of_lift, wing_area, density, lift):
    return math.sqrt(lift * 2 / density / wing_area / coefficient_of_lift)


def calculate_reynolds_number(velocity, chord, kinematic_viscosity):
    return int(round(velocity * chord / kinematic_viscosity, 0))


def calculate_lift_coefficient(lift, wing_area, density, velocity):
    return 2 * lift / (wing_area * density * pow(velocity, 2))


def calculate_oswald_efficiency_number(aspect_ratio):
    return 1.78 * (1 - 0.045 * pow(aspect_ratio, 0.68)) - 0.64


def calculate_induced_drag_coefficient(lift_coefficient, aspect_ratio, oswald_efficiency_number):
    return pow(lift_coefficient, 2) / (math.pi * aspect_ratio * oswald_efficiency_number)


def calculate_induced_drag(lift, density, velocity, wingspan):
    return pow(lift, 2) / (0.5 * density * pow(velocity, 2) * math.pi  * pow(wingspan, 2))

# optimises for max lift and good stall characteristics
def select_max_lift_good_stall_airfoil(lift_coefficient, reynolds_number):
    return 'NACA 2418'
    

# optimises for max lift and good stall characteristics
def select_lowest_drag_airfoil(lift_coefficient, reynolds_number, lowest_thickness):
    return 'NACA 63A010'


def calculate_angle_of_attack(airfoil, reynolds_number, lift_coefficient):
    airfoil_data = {
        'NACA 2418': {
            '317649' : {
                '1.029966250065918': 7
            },
            '127060' : {
                '1.029966250065918': 7
            }
        },
        'NACA 63A010': {
            '1058831' : {
                '0.09269696250593261': 1
            },
            '423533' : {
                '0.09269696250593261': 1
            } 
        },
        'NACA 64-008A': {
            '1058831' : {
                '0.017453292519943295': 1
            },
            '423533' : {
                '0.017453292519943295': 1
            } 
        }
    }
    return airfoil_data[airfoil][str(reynolds_number)][str(lift_coefficient)]