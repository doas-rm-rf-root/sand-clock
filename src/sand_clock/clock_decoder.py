import numpy
import taichi
from PIL import Image
from importlib import resources

from sand_clock.consts import *

def load_clock() -> numpy.array:
    grid = taichi.field(dtype=taichi.i32, shape=(W, H))

    path = resources.files("sand_clock.assets").joinpath(IMAGE_NAME)

    image = Image.open(path).convert("RGBA")

    array = numpy.array(image)

    alpha = array[:, :, 3].transpose()
    alpha = alpha[:, ::-1]

    for x in range(H):
        for y in range(W):
            if alpha[x, y] > 0:
                grid[x, y] = BLOCK
    
    return grid 
