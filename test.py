import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

load_position = [-52, -228, -392, -568, -732, -908]
P = [-91, -91, -67.5, -67.5, -67.5, -67.5]
max_length = 1250
reaction_locations = (25, 1225)

def get_loads(total_load):
    normal_load = total_load/6.7
    heavy_load = normal_load*1.35
    P = [heavy_load, heavy_load, normal_load, normal_load, normal_load, normal_load]
    return P

# Takes in x (the position of the front of the car), P (an array that represents the magnitude of the loads)
# P_locations (the position of the loads relative to the front of the car), max_length (the length of the bridge)
# Returns a dictionary with (position of load):(magnitude of load)
def find_loads(x, P, P_locations, max_length):
    loads = {}
    for i in range(len(P)):
        P_location = x + P_locations[i]
        if P_location >= 0 and P_location <= max_length:  
            loads[P_location] = P[i]
    return loads

def find_reaction(loads, reaction_locations):
    left_reaction_loc, right_reaction_loc = reaction_locations
    left_reaction_mag, right_reaction_mag = 0,0
    moment = 0
    force = 0
    for load in loads:
        moment += loads[load] * (load - left_reaction_loc)
        force += loads[load]
    right_reaction_mag = -1 * moment / (right_reaction_loc - left_reaction_loc)
    left_reaction_mag = -(force + right_reaction_mag)
    reactions = {left_reaction_loc: left_reaction_mag, right_reaction_loc: right_reaction_mag}
    return reactions

def find_shear(shear_forces, max_length):
    current_shear = 0
    shear = {}
    for i in range(max_length):
        shear[i] = current_shear
        if i in shear_forces:
            current_shear += shear_forces[i]
    return shear
    
def find_moment(shear_forces, max_length):
    current_shear = 0
    current_moment = 0
    moments = {}
    for i in range(max_length):
        current_moment += current_shear
        moments[i] = current_moment
        if i in shear_forces:
            current_shear += shear_forces[i]
    return moments

def plot(data, xlabel, ylabel, filename):
    # Extract x and y values
    x = list(data.keys())
    y = list(data.values())

    # Create scatterplot
    plt.scatter(x, y, color='black', s=3, alpha=0.8)

    # Add labels and title
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # Show the plot
    plt.savefig(filename)
    plt.show()
    
loads_mag = get_loads(-452)
loads = find_loads(1105, loads_mag, load_position, max_length)
reactions = find_reaction(loads,reaction_locations)
shear = loads | reactions
moments = find_moment(shear, max_length)
plot(shear, "position (mm)", "shear (N)", "shear.png")
plot(moments, "position (mm)", "moments (N * mm)", "moment.png")
