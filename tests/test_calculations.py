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
    wingspan = 600
    root_chord = 110
    tip_chord = 60
    # when
    aspect_ratio = aerodynamic_calculations.calculate_aspect_ratio(wingspan, root_chord, tip_chord)
    # then
    assert round(aspect_ratio, 4) == 7.0588


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
    tip_chord = aerodynamic_calculations.calculate_tip_chord(root_chord, taper_ratio)
    # then
    assert tip_chord == 160


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
    nuetral_point = 120
    mean_aerodynamic_chord_distance = 135.294
    sweep_angle = aerodynamic_calculations.calculate_sweep(nuetral_point, mean_aerodynamic_chord_distance, mean_aerodynamic_chord)
    assert round(sweep_angle, 5) == 0.62755


def test_calculate_sweep_distance():
    wingspan = 600
    sweep_angle =  0.62755
    sweep_distance = aerodynamic_calculations.calculate_sweep_distance(wingspan, sweep_angle)
    assert round(sweep_distance, 3) == 217.611


def test_calculate_center_of_gravity():
    nuetral_point = 0.24571
    static_margin = 0.1
    center_of_gravity = aerodynamic_calculations.calculate_center_of_gravity(nuetral_point, static_margin)
    assert center_of_gravity == 0.196568


def test_calculate_wing_area():
    wingspan = 1.2
    root_chord = 0.4
    tip_chord = 0.16
    wing_area = aerodynamic_calculations.calculate_wing_area(wingspan, root_chord, tip_chord)
    assert round(wing_area, 3) == 0.336


def test_calculate_wing_loading():
    wing_area = 0.336
    gross_weight = 3
    wing_loading = aerodynamic_calculations.calculate_wing_loading(gross_weight, wing_area)
    assert wing_loading == 5


def test_calculate_lift():
    coefficient_of_lift = 0.5
    wing_area = 0.336
    density = 1.204
    velocity = 20
    lift = aerodynamic_calculations.calculate_lift(coefficient_of_lift, wing_area, density, velocity)
    assert lift == 40.4544 # Newtons

def test_calculate_velocity():
    coefficient_of_lift = 0.5
    wing_area = 0.336
    density = 1.204
    lift = 30
    velocity = aerodynamic_calculations.calculate_velocity(coefficient_of_lift, wing_area, density, lift)
    assert round(velocity, 3) == 17.223 # meters per second


def test_design():
    wingspan = 1.2
    root_chord = 0.4
    area = root_chord * wingspan
    nuetral_point = root_chord
    static_margin = 0.1
    aspect_ratio = aerodynamic_calculations.calculate_aspect_ratio(wingspan, area)
    taper_ratio = aerodynamic_calculations.calculate_ideal_taper_ratio()
    tip_chord = aerodynamic_calculations.calculate_tip_chord(root_chord, taper_ratio)
    mean_aerodynamic_chord = aerodynamic_calculations.calculate_mean_aerodynamic_chord(root_chord, taper_ratio)
    mean_aerodynamic_chord_distance = aerodynamic_calculations.calculate_mean_aerodynamic_chord_distance(wingspan, root_chord, mean_aerodynamic_chord, tip_chord)
    sweep_angle = aerodynamic_calculations.calculate_sweep(nuetral_point, mean_aerodynamic_chord_distance, mean_aerodynamic_chord)
    center_of_gravity = aerodynamic_calculations.calculate_center_of_gravity(nuetral_point, static_margin)
    take_off_flight_profile = {
        'angle_of_attack': 10,
        'speed': 20
    }

    lift = aerodynamic_calculations.calculate_lift()
