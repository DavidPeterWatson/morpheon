def calculate_aspect_ratio(wingspan, area):
    return wingspan * wingspan / area

def calculate_taper_ratio(root_chord, tip_chord):
    return tip_chord / root_chord

def calculate_ideal_taper_ratio():
    return 0.4