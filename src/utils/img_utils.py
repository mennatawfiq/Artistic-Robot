from PIL import Image
import numpy as np


def image_to_rgb_array(path, n):
    # returns an n * n matrix of rgb values
    img = Image.open(path).convert("RGB")
    img = img.resize((n, n), Image.BILINEAR)  # downscale w/ averaging
    arr = np.array(img)  # arr[n][n][3]
    return arr

    

