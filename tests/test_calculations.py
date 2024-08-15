import pytest
import aerodynamic_calculations.aerodynamic_calculations as aerodynamic_calculations

# Arrange
@pytest.fixture
def test_design():
    design_requirements = {
        'aerodynamics': {
            'max-speed': 50, # meters per second
            'min-speed': 5, # meters per second
            'max-g-force': 20,
            'min-altitude': 0, # meters
            'max-altitude': 500, # meters
            'max-payload': 1, # kilograms
            'max-net-weight': 2, # kilograms
            'max_root-chord': 0.4, # meters
            'max_wingspan': 1.2 # meters
        }
    }
    return design_requirements

def test_aspect_ratio_calculation():
    # given
    wingspan = 10
    chord = 2
    area = chord * wingspan
    # when
    aspect_ratio = aerodynamic_calculations.calculate_aspect_ratio(wingspan, area)
    # then
    assert aspect_ratio == 5


def test_taper_ratio_calculation():
    # given
    root_chord = 2
    tip_chord = 1
    # when
    taper_ratio = aerodynamic_calculations.calculate_taper_ratio(root_chord, tip_chord)
    # then
    assert taper_ratio == 0.5


def test_ideal_taper_ratio_calculation():
    # when
    taper_ratio = aerodynamic_calculations.calculate_ideal_taper_ratio()
    # then
    assert taper_ratio == 0.4


def test_tip_chord_calculation():
    # given
    root_chord = 400
    taper_ratio = 0.4
    # when
    tip_chord_length = aerodynamic_calculations.calculate_tip_chord(root_chord, taper_ratio)
    # then
    assert tip_chord_length == 160


def test_calculate_mean_aerodynamic_chord():
    root_chord = 110
    tip_chord = 60
    taper_ratio = tip_chord / root_chord
    mean_aerodynamic_chord = aerodynamic_calculations.calculate_mean_aerodynamic_chord(root_chord, taper_ratio)
    assert round(mean_aerodynamic_chord, 3) == 87.451


def test_calculate_mean_aerodynamic_chord_distance():
    wingspan = 600
    root_chord = 110
    mean_aerodynamic_chord = 87.451
    tip_chord = 60
    mean_aerodynamic_chord_distance = aerodynamic_calculations.calculate_mean_aerodynamic_chord_distance(wingspan, root_chord, mean_aerodynamic_chord, tip_chord)
    assert round(mean_aerodynamic_chord_distance, 3) == 135.294


def test_calculate_sweep():
    mean_aerodynamic_chord = 87.451
    desired_nuetral_point = 120
    mean_aerodynamic_chord_distance = 135.294
    sweep = aerodynamic_calculations.calculate_sweep(desired_nuetral_point, mean_aerodynamic_chord_distance, mean_aerodynamic_chord)
    assert round(sweep, 5) == 0.62755


# def test_aerodynamic_sweep_calculation():
#     sweep = aerodynamic_calculations.calculate_sweep(root_chord_length, wing_span, nuetral_point)

# https://dergipark.org.tr/tr/download/article-file/629766