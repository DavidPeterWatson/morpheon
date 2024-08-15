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
            'root-chord': 0.4 # meters
        }
    }
    return design_requirements

def test_aspect_ratio_calculation():
    wingspan = 10
    chord = 2
    area = chord * wingspan
    aspect_ratio = aerodynamic_calculations.calculate_aspect_ratio(wingspan, area)
    assert aspect_ratio == 5


def test_taper_ratio_calculation():
    root_chord = 2
    tip_chord = 1
    taper_ratio = aerodynamic_calculations.calculate_taper_ratio(root_chord, tip_chord)
    assert taper_ratio == 0.5


def test_ideal_taper_ratio_calculation():
    taper_ratio = aerodynamic_calculations.calculate_ideal_taper_ratio()
    assert taper_ratio == 0.4

# def test_tip_chord_length_calculation():
#     root_chord_length = 400
#     tip_chord_length = aerodynamic_calculations.calculate_tip_chord_length(root_chord_length)
#     assert tip_chord_length = 




# def test_aerodynamic_sweep_calculation():
#     sweep = aerodynamic_calculations.calculate_sweep(root_chord_length, wing_span, nuetral_point)