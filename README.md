Falling Sand Simulation Framework
This document provides a comprehensive technical overview and reference manual for the cellular automaton physics engine implemented using the Taichi language.

Overview
Technical Note: This engine simulates granular materials (similar to mechanics found in games like Noita). The primary goal is to ensure realistic downward gravity propagation and natural sideways cascading to form stable sand mounds.

Table of Contents
1. [Vertical Scanning Logic](https://www.google.com/search?q=%231-vertical-scanning-logic)
2. [Horizontal Scanning Parity](https://www.google.com/search?q=%232-horizontal-scanning-parity)
3. [Movement Priority Matrix](https://www.google.com/search?q=%233-movement-priority-matrix)
4. [Taichi Parallelization Control](https://www.google.com/search?q=%234-taichi-parallelization-control)

Core Simulation Architecture
1. Vertical Scanning Logic
The grid processing execution loop iterates through the vertical axis strictly from the bottom rows upward to the top:

/Sequential Execution: Scanning starts at y = 1 and increments up to H.
/Anti-Teleportation Control: When a grain of sand at height y drops down to y - 1, it occupies a cell that the loop has already processed in the current frame.

~~Incorrect implementation (Top-Down):~~ If processed from top to bottom, a single particle would be continuously re-evaluated, resulting in instantaneous teleportation to the grid floor within a single frame.

Correct implementation (Bottom-Up): Guarantees a terminal velocity constraint of exactly 1 pixel per frame.

2. Horizontal Scanning Parity
To prevent visual skewing and asymmetric sand build-ups, the horizontal scan direction alternates dynamically based on the frame index:

/Even Frames (frame_idx % 2 == 0): Iterates from left to right (0 to W - 1).
/Odd Frames (frame_idx % 2 == 1): Iterates from right to left (W - 1 down to 0).

Without this alternation, the left side of the grid would always claim empty diagonal spaces first, causing all sand pyramids to unnaturally slide towards the right.

3. Movement Priority Matrix
When a cell updates, its behavior follows a strict hierarchical rule-set evaluated sequentially:

Priority	     Condition	                    Target Cell	                  Action Taken
1	       Immediate bottom cell is empty	      [x, y - 1]	         Falls straight down under pure gravity
2	       Primary diagonal is empty	         [x ± 1, y - 1]  	     Cascades diagonally (50% random choice left/right)
3	       Secondary diagonal is empty.  	     [x ∓ 1, y - 1]	       Cascades to the alternative side if primary is blocked
4	       All downward paths obstructed	         None	             Particle becomes static and stops moving


4. Taichi Parallelization Control
The kernel implementation overrides the default multi-threaded execution behavior of the compiler using a dummy loop wrapper.

@taichi.kernel
def update(frame_idx: taichi.i32):
    # Dummy loop forcing sequential single-threaded GPU/CPU execution
    for _ in range(1):
        for y in range(1, H):
            for scan_x in range(W):
                # Core cellular automaton logic goes here
                pass
Why this is necessary:
1.By default, the Taichi compiler automatically parallelizes the outermost loop inside any @taichi.kernel across available GPU cores.
2.Parallelizing coordinate loops directly would induce massive race conditions, as multiple concurrent threads would attempt to modify identical cell data arrays simultaneously.
3.The for _ in range(1): wrapper safely tricks the compiler into executing the nested physics loops sequentially and predictably
