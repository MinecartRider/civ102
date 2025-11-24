# A collection of all helper functions we wrote, sorted by document name.

# These packages were imported:
import numpy as np # for calculations, and better definitions of constants like pi
import pandas as pd # for dictionary handling
import matplotlib.pyplot as plt # for plotting graphs

# flexural_stress.py:
# This module is primarily used to find the flexural stresses.

def flexural_tens(I,centroid,M_max=85910):
    flex_tens_stress=(M_max*centroid/I)
    print("Flexural Tensile Stress: " + str(flex_tens_stress))
    FOS=30/flex_tens_stress
    print("FOS(Flexural Tension) = "+str(FOS))
    return flex_tens_stress

def flexural_comp(I,centroid, y_max, M_max=85910):
    flex_comp_stress=(M_max*(y_max-centroid))/I
    print("Flexural Compressive Stress: " + str(flex_comp_stress))
    FOS=6/flex_comp_stress
    print("FOS(Flexural Compression) = "+str(FOS))
    return flex_comp_stress

# properties.py:
# This module was originally a file that mirrored the capabilities of the cross_section.py
# file, and was used to calculate the cross sectional properties of various designs.
# Most functions here are now obsolete and not used, except for the buckling and FOS helpers.

def local_buckling(t, b, k, mu=0.2, E=4000):
    beta = np.pi**2 * E / (12 * (1 - mu**2))
    critical_stress = beta * k * (t/b)**2
    return critical_stress

def shear_buckling(t, b, a, k=5, mu=0.2, E=4000):
    beta = np.pi**2 * E / (12 * (1 - mu**2))
    critical_shear = beta * k * ((t/b)**2 + (t/a)**2)
    return critical_shear

def calculate_fos(sigma_applied, sigma_critical):
    return sigma_critical / sigma_applied
    
# cross_section.py:
# This module is used to calculate the cross sectional properties of various designs.
# Most functions take in the design as a dictionary consisting multiple rectangles
# which are defined by height, width, and position of its top-left point.

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

# shear_helpers.py:
# This module is used to calculate the shear and moments of a given loading.
# It is also used to calculate and graph the envelopes for shear and moment diagrams.

# This function associates the position of the train to the load and its locations.
def find_loads(x, P, P_locations, max_length):
    loads = {}
    for i in range(len(P)):
        P_location = x + P_locations[i]
        if P_location >= 0 and P_location <= max_length:  
            loads[P_location] = P[i]
    return loads

# This function finds the reactions at the supports given the applied loads and their locations.
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

# This function uses the change in shear forces to calculate the shear force diagram.
def find_shear(shear_forces, max_length):
    current_shear = 0
    shear = {}
    for i in range(max_length):
        if i in shear_forces:
            current_shear += shear_forces[i]
        shear[i] = current_shear
    return shear

# This function uses the change in shear forces to calculate the bending moment diagram.
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

# Given a train position x, this function calculates the shear or moment diagram at that position.
def calculate_at_train_position(func, x, load, load_position, reaction_locations, max_length):
    loads = find_loads(x, load, load_position, max_length)
    reactions = find_reaction(loads, reaction_locations)
    shear = {k: loads.get(k, 0) + reactions.get(k, 0) for k in set(loads) | set(reactions)}
    data = func(shear, max_length)
    return data
    
# This function finds the maximum and minimum (maximum negative) values of each position for every load case.
# It then stores these values in four different dictionaries, which for each position returns:
# its maximum value, the position of the train where the value occurs, and the same for minimum values.
def envelope(func, load, load_position, reaction_locations, max_length, train_length=0):
    load_mag = load
    maximum = {}
    x_at_max = {}
    minimum = {}
    x_at_min = {}
    for x in range(max_length + train_length):
        loads = find_loads(x, load_mag, load_position, max_length)
        reactions = find_reaction(loads, reaction_locations)
        shear = {k: loads.get(k, 0) + reactions.get(k, 0) for k in set(loads) | set(reactions)}
        data_at_pos = func(shear, max_length)
        for pos in data_at_pos:
            if pos not in maximum:
                maximum[pos] = data_at_pos[pos]
                x_at_max[pos] = x
                minimum[pos] = data_at_pos[pos]
                x_at_min[pos] = x
            elif maximum[pos] < data_at_pos[pos]:
               maximum[pos] = data_at_pos[pos]
               x_at_max[pos] = x 
            elif minimum[pos] > data_at_pos[pos]:
                minimum[pos] = data_at_pos[pos]
                x_at_min[pos] = x
    return maximum, x_at_max, minimum, x_at_min

# This function plots the envelope by graphing all load cases. Takes longer and is only used for graphical representation.
def plot_all_load_cases(func, load, load_position, reaction_locations, max_length, train_length=0, xlabel="", ylabel="", filename="file.png"):
    data = []
    load_mag = load
    for x in range(max_length + train_length):
        loads = find_loads(x, load_mag, load_position, max_length)
        reactions = find_reaction(loads, reaction_locations)
        shear = {k: loads.get(k, 0) + reactions.get(k, 0) for k in set(loads) | set(reactions)}
        data_at_pos = func(shear, max_length)
        for pos in data_at_pos:
            data.append([pos, data_at_pos[pos]])

    # Plotting
    plot_x = []
    plot_y = []
    for i in data:
        plot_x.append(i[0])
        plot_y.append(i[1])

    plt.scatter(plot_x, plot_y, color='black', s=3, alpha=0.8)
    # Add labels and title
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # Show the plot
    plt.savefig(filename)
    plt.show()


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


def plot_envelope(envelope_max, envelope_min, xlabel, ylabel, filename):
    # Extract x and y values
    x_max = list(envelope_max.keys())
    y_max = list(envelope_max.values())
    x_min = list(envelope_min.keys())
    y_min = list(envelope_min.values())

    # Create scatterplot
    plt.scatter(x_max, y_max, color='black', s=3, alpha=0.8)
    plt.scatter(x_min, y_min, color='black', s=3, alpha=0.8)


    # Add labels and title
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # Show the plot
    plt.savefig(filename)
    plt.show()