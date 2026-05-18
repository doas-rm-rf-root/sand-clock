import taichi

import random

import time

from sand_clock.clock_decoder import load_clock
from sand_clock.consts import *
from sand_clock.sand_spawner import spawn_particles
from sand_clock.particle_calculation import calculate_target_fps

taichi.init(arch=taichi.cpu)

grid = taichi.field(dtype=taichi.i32, shape=(W, H))
image = taichi.Vector.field(3, dtype=taichi.f32, shape=(W, H))

frame_counter = 0

@taichi.kernel
def update(frame_idx: int):
    for _ in range(1):
        for y in range(1, H):
            
            for scan_x in range(W):
                x = scan_x
                if frame_idx % 2 == 1:
                    x = (W - 1) - scan_x

                if grid[x, y] == SAND:
                    if grid[x, y - 1] == AIR:
                        grid[x, y - 1] = SAND
                        grid[x, y] = AIR

                    else:
                        move_left = taichi.random() < 0.5
                        if move_left:
                            if x > 0 and grid[x - 1, y - 1] == AIR:
                                grid[x - 1, y - 1] = SAND
                                grid[x, y] = AIR
                            elif x < W - 1 and grid[x + 1, y - 1] == AIR:
                                grid[x + 1, y - 1] = SAND
                                grid[x, y] = AIR
                        else:
                            if x < W - 1 and grid[x + 1, y - 1] == AIR:
                                grid[x + 1, y - 1] = SAND
                                grid[x, y] = AIR
                            elif x > 0 and grid[x - 1, y - 1] == AIR:
                                grid[x - 1, y - 1] = SAND
                                grid[x, y] = AIR

@taichi.kernel
def render():
    for x, y in grid:
        if grid[x, y] == SAND:
            image[x, y] = taichi.Vector(SAND_COLOR)
        elif grid[x, y] == AIR:
            image[x, y] = taichi.Vector(AIR_COLOR)
        elif grid[x, y] == BLOCK:
            image[x, y] = taichi.Vector(BLOCK_COLOR)

def run_window(minutes: int):
    global frame_counter
    window = taichi.ui.Window("Sand clock", (600, 600), vsync=False)
    canvas = window.get_canvas()

    global grid
    grid.copy_from(load_clock())
    
    spawn_particles(MAX_PARTICLES, grid)

    frame_duration = 1.0 / calculate_target_fps(minutes) 

    print(frame_duration)

    while window.running:
        frame_start = time.perf_counter()

        update(frame_counter)
        frame_counter += 1
        
        render()
        canvas.set_image(image)
        window.show()

        elapsed = time.perf_counter() - frame_start
        sleep_time = frame_duration - elapsed

        if sleep_time > 0:
            time.sleep(sleep_time)

def spawn_test_sand(grid):
    cx = W // 2  

    cy = int(H * 0.80)  

    radius = 40
    for i in range(-radius, radius + 1):
        for j in range(-radius, radius + 1):
            if 0 <= cx + i < W and 0 <= cy + j < H:
                if random.random() < 0.4: 
                    if grid[cx + i, cy + j] == AIR:
                        grid[cx + i, cy + j] = SAND