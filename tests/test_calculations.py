import pytest
import aerodynamic_calculations.aerodynamic_calculations as ac
import math
import json

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
    wingspan = 1.2
    root_chord = 0.400
    tip_chord = 0.160
    # when
    aspect_ratio = ac.calculate_aspect_ratio(wingspan, root_chord, tip_chord)
    # then
    assert round(aspect_ratio, 4) == 4.2857


def test_taper_ratio_calculation():
    # given
    root_chord = 2
    tip_chord = 1
    # when
    taper_ratio = ac.calculate_taper_ratio(root_chord, tip_chord)
    # then
    assert taper_ratio == 0.5


def test_ideal_taper_ratio_calculation():
    # when
    taper_ratio = ac.calculate_ideal_taper_ratio()
    # then
    assert taper_ratio == 0.4


def test_tip_chord_calculation():
    # given
    root_chord = 400
    taper_ratio = 0.4
    # when
    tip_chord = ac.calculate_tip_chord(root_chord, taper_ratio)
    # then
    assert tip_chord == 160


def test_calculate_mean_aerodynamic_chord():
    root_chord = 110
    tip_chord = 60
    taper_ratio = tip_chord / root_chord
    mean_aerodynamic_chord = ac.calculate_mean_aerodynamic_chord(root_chord, taper_ratio)
    assert round(mean_aerodynamic_chord, 3) == 87.451


def test_calculate_mean_aerodynamic_chord_distance():
    wingspan = 600
    root_chord = 110
    mean_aerodynamic_chord = 87.451
    tip_chord = 60
    mean_aerodynamic_chord_distance = ac.calculate_mean_aerodynamic_chord_distance(wingspan, root_chord, mean_aerodynamic_chord, tip_chord)
    assert round(mean_aerodynamic_chord_distance, 3) == 135.294


def test_calculate_sweep():
    mean_aerodynamic_chord = 87.451
    nuetral_point = 120
    mean_aerodynamic_chord_distance = 135.294
    sweep_angle = ac.calculate_sweep(nuetral_point, mean_aerodynamic_chord_distance, mean_aerodynamic_chord)
    assert round(sweep_angle, 5) == 0.62755


def test_calculate_sweep_distance():
    wingspan = 600
    sweep_angle =  0.62755
    sweep_distance = ac.calculate_sweep_distance(wingspan, sweep_angle)
    assert round(sweep_distance, 3) == 217.611


def test_calculate_center_of_gravity():
    nuetral_point = 0.24571
    static_margin = 0.1
    center_of_gravity = ac.calculate_center_of_gravity(nuetral_point, static_margin)
    assert center_of_gravity == 0.196568


def test_calculate_wing_area():
    wingspan = 1.2
    root_chord = 0.4
    tip_chord = 0.16
    wing_area = ac.calculate_wing_area(wingspan, root_chord, tip_chord)
    assert round(wing_area, 3) == 0.336


def test_calculate_wing_loading():
    wing_area = 0.336
    gross_weight = 3
    wing_loading = ac.calculate_wing_loading(gross_weight, wing_area)
    assert wing_loading == 5


def test_calculate_lift():
    coefficient_of_lift = 0.5
    wing_area = 0.336
    density = 1.204
    velocity = 20
    lift = ac.calculate_lift(coefficient_of_lift, wing_area, density, velocity)
    assert lift == 40.4544 # Newtons


# https://www.omnicalculator.com/physics/lift-coefficient
def test_calculate_lift_coefficient():
    lift = 800
    wing_area = 1
    density = 1.225
    velocity = 100
    lift_coefficient = ac.calculate_lift_coefficient(lift, wing_area, density, velocity)
    assert round(lift_coefficient, 4) == 0.1306

def test_calculate_velocity():
    coefficient_of_lift = 1.0
    wing_area = 0.336
    density = 1.204
    lift = 30
    velocity = ac.calculate_velocity(coefficient_of_lift, wing_area, density, lift)
    assert round(velocity, 3) == 12.178 # meters per second


def test_calculate_reynolds_number():
    velocity = 20.0
    chord = 0.4
    kinematic_viscosity = 1.5111E-5
    reynolds_number = ac.calculate_reynolds_number(velocity, chord, kinematic_viscosity)
    assert reynolds_number == 529416


def test_calculate_oswald_effeciency_number():
    aspect_ratio = 4.2857
    oswald_effeciency_number = ac.calculate_oswald_effeciency_number(aspect_ratio)
    assert round(oswald_effeciency_number, 4) == 0.9245


def test_calculate_induced_drag_coefficient():
    lift_coefficient = 0.1306
    aspect_ratio = 4.2857
    oswald_efficiency_number = 0.85
    induced_drag_coefficient = ac.calculate_induced_drag_coefficient(lift_coefficient, aspect_ratio, oswald_efficiency_number)
    assert round(induced_drag_coefficient, 5) == 0.00149


def test_calculate_induced_drag():
    lift = 30
    density = 1.204
    velocity = 10
    wingspan = 1.2
    induced_drag = ac.calculate_induced_drag(lift, density, velocity, wingspan)
    assert round(induced_drag, 4) == 3.3047


def test_select_max_lift_good_stall_airfoil():
    low_speed_lift_coefficient = 1.0
    low_speed_root_reynolds = 112,621
    low_speed_root_airfoil = ac.select_max_lift_good_stall_airfoil(low_speed_lift_coefficient, low_speed_root_reynolds)
    assert low_speed_root_airfoil == 'NACA 2418'


def test_select_select_lowest_drag_airfoil():
    high_speed_lift_coefficient = 1.0
    high_speed_root_reynolds = 112,621
    lowest_thickness = 0.1
    high_speed_root_airfoil = ac.select_max_lift_good_stall_airfoil(high_speed_lift_coefficient, high_speed_root_reynolds, lowest_thickness)
    assert high_speed_root_airfoil == 'NACA 64-008A'


def test_calculate_angle_of_attack():
    angle_of_attack = ac.calculate_angle_of_attack('NACA 2418', 317649, 1.029966250065918)
    assert angle_of_attack == 7


def test_design():
    wingspan = 1.2
    root_chord = 0.4
    wing_area = root_chord * wingspan
    nuetral_point = root_chord
    static_margin = 0.1
    taper_ratio = ac.calculate_ideal_taper_ratio()
    tip_chord = ac.calculate_tip_chord(root_chord, taper_ratio)
    aspect_ratio = ac.calculate_aspect_ratio(wingspan, root_chord, tip_chord)
    oswald_efficiency_number = ac.calculate_oswald_efficiency_number(aspect_ratio)
    
    wing_area = ac.calculate_wing_area(wingspan, root_chord, tip_chord)
    mean_aerodynamic_chord = ac.calculate_mean_aerodynamic_chord(root_chord, taper_ratio)
    mean_aerodynamic_chord_distance = ac.calculate_mean_aerodynamic_chord_distance(wingspan, root_chord, mean_aerodynamic_chord, tip_chord)
    sweep_angle = ac.calculate_sweep_angle(nuetral_point, mean_aerodynamic_chord_distance, mean_aerodynamic_chord)
    center_of_gravity = ac.calculate_center_of_gravity(nuetral_point, static_margin)


    kinematic_viscosity = 1.5111E-5
    density = 1.204
    required_lift = 30 # Newtons

    low_speed_velocity = 12
    low_speed_angle_of_attack = math.radians(10)
    low_speed_lift_coefficient = ac.calculate_lift_coefficient(required_lift, wing_area, density, low_speed_velocity)
    low_speed_induced_drag_coefficient = ac.calculate_induced_drag_coefficient(low_speed_lift_coefficient, aspect_ratio, oswald_efficiency_number)
    low_speed_induced_drag = ac.calculate_induced_drag(required_lift, density, low_speed_velocity, wingspan)
    
    low_speed_root_reynolds_number = ac.calculate_reynolds_number(low_speed_velocity, root_chord, kinematic_viscosity)
    low_speed_root_airfoil = ac.select_max_lift_good_stall_airfoil(low_speed_lift_coefficient, low_speed_root_reynolds_number)
    low_speed_root_angle_of_attack = ac.calculate_angle_of_attack(low_speed_root_airfoil, low_speed_root_reynolds_number, low_speed_lift_coefficient)

    low_speed_tip_reynolds_number = ac.calculate_reynolds_number(low_speed_velocity, tip_chord, kinematic_viscosity)
    low_speed_tip_airfoil = ac.select_max_lift_good_stall_airfoil(low_speed_lift_coefficient, low_speed_tip_reynolds_number)
    low_speed_tip_angle_of_attack = ac.calculate_angle_of_attack(low_speed_tip_airfoil, low_speed_tip_reynolds_number, low_speed_lift_coefficient)

    low_speed = {
        'velocity': low_speed_velocity,
        'angle_of_attack': low_speed_angle_of_attack,
        'induced_drag': low_speed_induced_drag,
        'lift_coefficient': low_speed_lift_coefficient,
        'root_reynolds_number': low_speed_root_reynolds_number,
        'low_speed_root_airfoil': low_speed_root_airfoil,
        'low_speed_root_angle_of_attack': low_speed_root_angle_of_attack,
        'tip_reynolds_number': low_speed_tip_reynolds_number,
        'low_speed_tip_airfoil': low_speed_tip_airfoil,
        'low_speed_tip_angle_of_attack': low_speed_tip_angle_of_attack
    }
    expected_low_speed = {
        'velocity': 12,
        'angle_of_attack': 0.17453292519943295,
        'induced_drag': 2.294939078821396,
        'lift_coefficient': 1.029966250065918,
        'root_reynolds_number': 317649,
        'low_speed_root_airfoil': 'NACA 2418',
        'low_speed_root_angle_of_attack': 7,
        'tip_reynolds_number': 127060,
        'low_speed_tip_airfoil': 'NACA 2418',
        'low_speed_tip_angle_of_attack': 7,
    }
    assert low_speed == expected_low_speed

    high_speed_velocity = 40
    lowest_thickness = 0.1
    high_speed_lift_coefficient = ac.calculate_lift_coefficient(required_lift, wing_area, density, high_speed_velocity)
    high_speed_induced_drag_coefficient = ac.calculate_induced_drag_coefficient(high_speed_lift_coefficient, aspect_ratio, oswald_efficiency_number)
    high_speed_induced_drag = ac.calculate_induced_drag(required_lift, density, high_speed_velocity, wingspan)

    high_speed_root_reynolds_number = ac.calculate_reynolds_number(high_speed_velocity, root_chord, kinematic_viscosity)
    high_speed_root_airfoil = ac.select_lowest_drag_airfoil(high_speed_lift_coefficient, high_speed_root_reynolds_number, lowest_thickness)
    high_speed_root_angle_of_attack = ac.calculate_angle_of_attack(high_speed_root_airfoil, high_speed_root_reynolds_number, high_speed_lift_coefficient)

    high_speed_tip_reynolds_number = ac.calculate_reynolds_number(high_speed_velocity, tip_chord, kinematic_viscosity)
    high_speed_tip_airfoil = ac.select_lowest_drag_airfoil(high_speed_lift_coefficient, high_speed_tip_reynolds_number, lowest_thickness)
    high_speed_tip_angle_of_attack = ac.calculate_angle_of_attack(high_speed_tip_airfoil, high_speed_tip_reynolds_number, high_speed_lift_coefficient)

    high_speed = {
        'velocity': high_speed_velocity,
        'induced_drag': high_speed_induced_drag,
        'lift_coefficient': high_speed_lift_coefficient,
        'root_reynolds_number': high_speed_root_reynolds_number,
        'high_speed_root_airfoil': high_speed_root_airfoil,
        'high_speed_root_angle_of_attack': high_speed_root_angle_of_attack,
        'tip_reynolds_number': high_speed_tip_reynolds_number,
        'high_speed_tip_airfoil': high_speed_tip_airfoil,
        'high_speed_tip_angle_of_attack': high_speed_tip_angle_of_attack
    }
    expected_high_speed = {
        'velocity': 40,
        'induced_drag': 0.20654451709392563,
        'lift_coefficient': 0.09269696250593261,
        'root_reynolds_number': 1058831,
        'high_speed_root_airfoil': 'NACA 63A010',
        'high_speed_root_angle_of_attack': 1,
        'tip_reynolds_number': 423533,
        'high_speed_tip_airfoil': 'NACA 63A010',
        'high_speed_tip_angle_of_attack': 1
    }
    assert high_speed == expected_high_speed