__author__ = 'David'
import numpy as np
import random as r
import matplotlib.pylab as plt

lengths = []


def dis(a, b):
    # gives us the distance between point a and b
    return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)


def city_generator(x_lim, y_lim):
    # generates a single point inside a given limits
    city = (r.randint(0, x_lim), r.randint(0, y_lim))
    return city


def city_list_generator(number, x_lim, y_lim):
    # generates the number of cites wanted in a given boundary
    list_of_cites = np.zeros(number*2)
    list_of_cites = list_of_cites.reshape((number, 2))

    for i in range(number):
        list_of_cites[i]=city_generator(x_lim, y_lim)

    return list_of_cites


def circuit_distance(cites):
    # gives the total distance of a given route
    total_distance = dis(cites[0], cites[len(cites)-1])  # closing the route

    for i in range(len(cites)-1):
        total_distance = total_distance+ dis(cites[i], cites[i+1])
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
    x = r.randint(0, len(new)-1)
    y = r.randint(0, len(new)-1)
    new[x] = cites[y]
    new[y] = cites[x]
    return new


def new_route_accept(new_rout, old_route, temperature):
    # finds the length of the new route and the old route
    new_length = circuit_distance(new_rout)
    old_length = circuit_distance(old_route)

    # accepts if new length is shorter then the old
    if new_length <= old_length:
        lengths.append(new_length)
        return new_rout

    # if not it accepts if the exp of the difference in distance divided by the current temperature
    # is great then some random number between 0 and 1
    else:
        difference = new_length-old_length

        if np.exp(-difference/temperature) > r.random():
            lengths.append(new_length)
            return new_rout
        else:
            lengths.append(old_length)
            return old_route


def temperature_schedule(temp, cooling_factor):
    # this gives us a specific colling scheme
    return temp * cooling_factor


def main():
    # initialising variables
    temps = []
    iterations = 0
    temperature = 10
    x_limit = 100
    y_limit = 100
    number_of_cities_wanted = 25
    finishing_temperature = .1
    cooling_factor = .9990
    cites = city_list_generator(number_of_cities_wanted, x_limit, y_limit)

    print 'original distance is %f' % circuit_distance(cites)

    # plot of the original route
    plot_route(cites)

    while temperature > finishing_temperature:
        temps.append(temperature)
        iterations += 1
        new_rout = new_route(cites)
        cites = new_route_accept(new_rout, cites, temperature)
        temperature = temperature_schedule(temperature, cooling_factor)

    print 'final distance is %f' % circuit_distance(cites)

    plt.plot(np.arange(iterations), temps)
    plt.plot(np.arange(iterations), lengths)
    plt.show()
    plot_route(cites)


if __name__ == "__main__":
    main()