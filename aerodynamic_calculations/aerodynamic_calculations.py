import math


def calculate_aspect_ratio(wingspan, area):
    return wingspan * wingspan / area


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


def calculate_sweep(nuetral_point, mean_aerodynamic_chord_distance, mean_aerodynamic_chord):
    mean_chord_leading_edge_point = nuetral_point - 1 / 4 * mean_aerodynamic_chord
    return math.atan(mean_chord_leading_edge_point / mean_aerodynamic_chord_distance)
    