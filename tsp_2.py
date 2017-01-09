__author__ = 'David'
__author__ = 'David'
import numpy as np
import random as r
import matplotlib.pylab as plt
import math

lengths = []
no_switch = 0

def dis(a, b):
    # gives us the distance between point a and b
    return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)


def city_generator(x_lim, y_lim):
    # generates a single point inside a given limits
    city = (r.randint(0, x_lim), r.randint(0, y_lim))
    return city


def city_list_generator(number, x_lim, y_lim):
    # generates the number of cites wanted in a given boundary
    list_of_cites = np.zeros(number * 2)
    list_of_cites = list_of_cites.reshape((number, 2))

    for i in range(number):
        list_of_cites[i] = city_generator(x_lim, y_lim)

    return list_of_cites


def circuit_distance(cites):
    # gives the total distance of a given route
    total_distance = dis(cites[0], cites[len(cites) - 1])  # closing the route

    for i in range(len(cites) - 1):
        total_distance = total_distance + dis(cites[i], cites[i + 1])
    return total_distance


def plot_route(cites):
    # generates plot of a given route
    x_cords = []
    y_cords = []

    for i in range(len(cites)):
        # temporary is a point(two values)
        temporary = cites[i]
        x_cords.append(temporary[0])
        y_cords.append(temporary[1])

    # joins the first city up to the last
    temporary = cites[0]
    x_cords.append(temporary[0])
    y_cords.append(temporary[1])

    plt.plot(x_cords, y_cords, ".")
    plt.plot(x_cords, y_cords, "-")
    plt.show()


def new_route(cites):
    # generates a new route by swapping the positions of two points in the list
    new = np.copy(cites)
    x = r.randint(0, len(new) - 1)
    y = r.randint(0, len(new) - 1)
    new[x] = cites[y]
    new[y] = cites[x]
    return new


def temperature_schedule(temp, cooling_factor):
    # this gives us a specific colling scheme
    return temp * cooling_factor


def swap_route(cities, x, y):
    # swappes the position of two cities in the list
    temp_x = np.copy(cities[x])
    temp_y = np.copy(cities[y])
    cities[x] = temp_y
    cities[y] = temp_x

number_of_no_switches = 0

def cooling(cites, temp):
    # picks to random cities and swaps there position in the list and
    # then accepts them if there with in some finite range
    n = len(cites)
    x = r.randint(0, n - 1)
    y = x
    while y == x:
        y = r.randint(0, n - 1)

    global number_of_no_switches

    # this code is accounting for the fact that if x and/or y is the first
    # and/or last item on the list then we have boundary problems
    if x == 0 and y == n - 1 or x == n - 1 and y == 0:
        if y == 0:
            y = x
            x = 0
        ordinal_distance = dis(cites[x % n], cites[(x + 1) % n]) + dis(cites[(y - 1) % n], cites[y % n])
        new_distance = dis(cites[y % n], cites[(x + 1) % n]) + dis(cites[(y - 1) % n], cites[x % n])
        delta_distance = new_distance - ordinal_distance

    elif x == y - 1 or y == x - 1:
        if y == x - 1:
            x = x - 1
            y = y + 1
        ordinal_distance = dis(cites[(x - 1) % n], cites[x % n]) + dis(cites[y % n], cites[(y + 1) % n])
        new_distance = dis(cites[y % n], cites[(x - 1) % n]) + dis(cites[(y + 1) % n], cites[x % n])
        delta_distance = new_distance - ordinal_distance

    else:
        ordinal_distance = dis(cites[(x - 1) % n], cites[x % n]) + dis(cites[x % n], cites[(x + 1) % n]) + dis(
            cites[(y - 1) % n], cites[y % n]) + dis(cites[y % n], cites[(y + 1) % n])
        new_distance = dis(cites[(x - 1) % n], cites[y % n]) + dis(cites[y % n], cites[(x + 1) % n]) + dis(
            cites[(y - 1) % n], cites[x % n]) + dis(cites[x % n], cites[(y + 1) % n])
        delta_distance = new_distance - ordinal_distance

    # changeing to the new order if its within the acceptable probability
    if delta_distance < 0 or np.exp(-delta_distance / temp) > r.random():
        swap_route(cites, x, y)
        number_of_no_switches = 0
    else:
        number_of_no_switches += 1


def main():
    # initialising variables
    iterations = 0
    temperature = 1000
    x_limit = 100
    y_limit = 100
    number_of_cities_wanted = 10
    finishing_temperature = .0000000000001
    cooling_factor = .9999
    total_iterations=math.log(finishing_temperature/temperature, cooling_factor)

    global number_of_no_switches
    cites = city_list_generator(number_of_cities_wanted, x_limit, y_limit)

    print 'original distance is %f' % circuit_distance(cites)

    # plot of the original route
    plot_route(cites)

    while temperature > finishing_temperature:
        iterations += 1
        cooling(cites, temperature)
        temperature = temperature_schedule(temperature, cooling_factor)

        # prints parentage finished
        if iterations % 10000 == 0:
            print "%.1f" % ((iterations/total_iterations)*100), "%"

        if number_of_no_switches>10000 and number_of_no_switches > total_iterations/10:
            temperature=finishing_temperature
            print"cut of early"




    print 'final distance is %f' % circuit_distance(cites)
    print iterations
    plot_route(cites)


if __name__ == "__main__":
    main()