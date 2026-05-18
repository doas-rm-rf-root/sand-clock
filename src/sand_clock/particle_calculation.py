from sand_clock.consts import NECK_WIDTH, MAX_PARTICLES

def calculate_target_fps(minutes):
    particles_per_frame = NECK_WIDTH

    total_frames_needed = MAX_PARTICLES / particles_per_frame

    target_seconds = minutes * 60

    target_fps = total_frames_needed / target_seconds

    return target_fps

