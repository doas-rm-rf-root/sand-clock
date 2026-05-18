# Sand Clock

A falling sand simulation that creates a visual hourglass timer using cellular automata physics.

## Installation

```bash
pipx install git+https://github.com/yourusername/sand-clock.git
```

## Usage

```bash
sand-clock 5
```

## Implementation

Sand Clock uses the Taichi computing framework to model granular material physics in a 300x300 grid. The simulation implements cellular automata with:

- At the moment the simulation is actually single threaded on CPU, which is a bummer
- Vertical scanning from bottom to top for gravity propagation
- Alternating horizontal scan direction each frame to prevent visual skewing
- Movement priority matrix for realistic sand behavior
- Time-based FPS calculation precise timing control

Dependencies:
- taichi
- numpy
- pillow