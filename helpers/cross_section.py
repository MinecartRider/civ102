import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt

def centroidal_axis(rectangles):
    A_times_d = 0
    A = 0
    for rectangle in list(rectangles.values()):
        h = rectangle["height"]
        w = rectangle["width"]
        top_left_corner = rectangle["location"]
        centroid = top_left_corner[1] - h / 2
        A_times_d += h * w * centroid
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
        centroid = top_left_corner[1] - h / 2
        I += w * h**3 / 12
        I += h * w * (centroid - y)**2
    return I

def first_moment(rectangles, depth_of_interest=None):
    Q = 0
    y = centroidal_axis(rectangles)
    if depth_of_interest == None:
        depth_of_interest = y
    for rectangle in list(rectangles.values()):
        h = rectangle["height"]
        w = rectangle["width"]
        top_left_corner = rectangle["location"]
        if top_left_corner[1] > depth_of_interest:
            bottom_edge = top_left_corner[1] - h
            if bottom_edge < depth_of_interest:
                bottom_edge = depth_of_interest
            centroid = (top_left_corner[1] + bottom_edge)/2
            d = y - centroid
            Q += (top_left_corner[1] - bottom_edge) * w * d
    return Q
# T_beam = {"rect1":{"height": 1.27, "width": 100, "location": (-50, 0)}, "rect2":{"height": 78.73, "width": 1.27, "location": (-1.27/2, -1.27)}}
# print(second_moment(T_beam))
# print(centroidal_axis(T_beam))   
# print(first_moment(T_beam))         
        