from sand_clock.consts import *

# With planned calculations with set maximum particles N is kinda semi-useless
def spawn_particles(n, grid):
    cx = W // 2
    cap_y = None 
    
    for y_check in range(H // 2, H):
        if cap_y == None: 
            if grid[cx, y_check] == BLOCK:
                cap_y = y_check - 1

    vertical_span = (H // 2) - cap_y

    circle_center = cap_y + int(vertical_span * 0.4)

    spawned_count = 0

    for j in range(-SAND_SPAWN_CIRCLE_R, SAND_SPAWN_CIRCLE_R + 1):
        for i in range(-SAND_SPAWN_CIRCLE_R, SAND_SPAWN_CIRCLE_R + 1):
            
            if i * i + j * j <= SAND_SPAWN_CIRCLE_R ** 2:
                x = cx + i
                y = circle_center + j
                
                if spawned_count < n:
                    if grid[x, y] == AIR:
                        grid[x, y] = SAND
                        spawned_count += 1 

    print(f"Spawned: {spawned_count}")