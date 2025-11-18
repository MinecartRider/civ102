import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def centroidal_axis(rectangles):
    A_times_d = 0
    A = 0
    for rectangle in list(rectangles.values()):
        h = rectangle["height"]
        w = rectangle["width"]
        top_left_corner = rectangle["location"]
        A_times_d += h * w * top_left_corner[1]
        A += h * w
    y = A_times_d / A
    return y

def second_moment(rectangles):
    I = 0 
    y = centroidal_axis(rectangles)
    for rectangle in list(rectangles.values()):
        h = rectangle["height"]
        w = rectangle["width"]
        top_left_corner = rectangle["location"]
        I += w * h**3 / 12
        I += h * w * (top_left_corner[1] - y)^2
    return I
        