from consts import NECK_WIDTH

def calculate_target_fps(particles, minutes):

    efficiency = 0.55

    particles_per_frame = NECK_WIDTH * efficiency

    total_frames_needed = particles / particles_per_frame

    target_seconds = minutes * 60

    target_fps = total_frames_needed / target_seconds

    return target_fps

