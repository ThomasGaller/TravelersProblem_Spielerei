# importing Matplotlib and Numpy Packages
import numpy as np
import matplotlib.pyplot as plt
import random as rndm
import sys
import math

coords = []
if len(sys.argv) != 3:
    max_coord = int(input("Max X/Y Value: "))
    max_num_of_points = pow(max_coord + 1, 2)
    # if pow(max_coord + 1, 2) > 999:
    #     max_num_of_points = 999
    # else:
    #     max_num_of_points = pow(max_coord + 1, 2)

    num_of_points = int(input("Number of Points (Max=" + str(max_num_of_points) + "): "))
    while num_of_points > max_num_of_points:
        print("Can not create more than " + str(max_num_of_points) + " points")
        num_of_points = int(input("Please enter a valid amount of points: "))


else:
    max_coord = int(sys.argv[1])
    num_of_points = int(sys.argv[2])


def sum_list(my_list):
    total_sum = 0
    for element in my_list:
        total_sum += element
    return total_sum


def generate_coord():
    return [rndm.randint(0, max_coord), rndm.randint(0, max_coord)]


def generate_coords():
    for point in range(0, num_of_points):
        new_coord = generate_coord()
        while new_coord in coords:
            new_coord = generate_coord()
        coords.append(new_coord)


def get_v_between_two_points(p1, p2):
    vector = []
    if len(p1) != len(p2):
        print("p1: " + str(p1))
        print("p2: " + str(p2))
        raise ValueError("Both Points must have the same amount of dimensions")
    for position in range(0, len(p1)):
        vector.append(p2[position] - p1[position])

    return vector


def get_vector_distance(vector):
    if vector[0] == 0:
        return vector[1]
    elif vector[1] == 0:
        return vector[0]
    else:
        return math.sqrt(pow(vector[0], 2) + pow(vector[1], 2))


def get_nearest_point(basis_point, old_coords):
    nearest_point = basis_point
    distance = -1
    for oc in old_coords:
        vector = get_v_between_two_points(basis_point, oc)
        v_distance = abs(get_vector_distance(vector))
        if distance == -1 or distance > v_distance:
            distance = v_distance
            nearest_point = oc

    return nearest_point, distance


def sort_points_nearest_neighbour(points):
    next_point = []
    sorted_points = []
    distance = []
    length = len(points)
    for position in range(0, length):
        if position == 0:
            next_point = points[0], 0
        else:
            next_point = get_nearest_point(next_point[0], points)
        sorted_points.append(next_point[0])
        distance.append(next_point[1])
        points.remove(next_point[0])
    return sorted_points, distance


def nearest_neighbour():
    sorted_points_nearest_neighbour, distance_arr = sort_points_nearest_neighbour(coords)
    # The data are given as list of lists (2d list)
    data = np.array(sorted_points_nearest_neighbour)

    # Taking transpose
    x, y = data.T

    # Print Coords
    print("Points:")
    for point in sorted_points_nearest_neighbour:
        print(point)

    # plot our list in X,Y coordinates
    plt.plot(x, y)
    fastest_route_text = "The fastest route is: "

    for i in range(0, len(sorted_points_nearest_neighbour)):
        plt.annotate("P" + str(i), (sorted_points_nearest_neighbour[i][0], sorted_points_nearest_neighbour[i][1]),
                     textcoords="offset points", xytext=(0, 5))
        if i != len(sorted_points_nearest_neighbour) - 1:
            fastest_route_text += str(sorted_points_nearest_neighbour[i]) + "(+" + str(distance_arr[i]) + ") --> "
        else:
            fastest_route_text += str(sorted_points_nearest_neighbour[i]) + "(+" + str(distance_arr[i]) + ")"

    # v = get_v_between_two_points(sorted_points_nearest_neighbour[0], sorted_points_nearest_neighbour[1])
    # plt.arrow(sorted_points_nearest_neighbour[0][0], sorted_points_nearest_neighbour[0][1], v[0], v[1])

    return plt, fastest_route_text, distance_arr


plt.figure(dpi=300)
generate_coords()
plt, fastest_route, distances = nearest_neighbour()
plt.show()
print()
print("Nearest Neighbour:")
print(fastest_route)
print("Total Distance: ", str(sum_list(distances)))
