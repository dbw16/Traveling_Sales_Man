__author__ = 'David'
import numpy as np
import math
import random as r
import matplotlib.pylab as plt

def dis(a, b):
    x_1= a[0]
    x_2= b[0]
    y_1= a[1]
    y_2= b[1]
    return np.sqrt((x_2-x_1)**2+(y_2-y_1)**2)

def city_gen(x_lim,y_lim):
    point=[]
    point.append(r.randint(0, x_lim))
    point.append(r.randint(0, y_lim))
    return point

def city_list_gen(number, x_lim, y_lim):
    list=np.zeros(number*2)
    list= list.reshape((number,2))
    for i in range(number):
        list[i]=city_gen(x_lim, y_lim)
    return list

def curquite_distace(citys):
    total_distnce = dis(citys[0], citys[len(citys)-1])
    for i in range(len(citys)-1):
        total_distnce = total_distnce+ dis(citys[i], citys[i+1])
    return total_distnce

def plot_route(citys):
    x_cords=[]
    y_cords=[]
    
    for i in range(len(citys)):
        tempuray=citys[i]
        x_cords.append(tempuray[0])
        y_cords.append(tempuray[1])
    
    #join n point back up to 0 point
    tempuray=citys[0]
    x_cords.append(tempuray[0])
    y_cords.append(tempuray[1])

    plt.plot(x_cords, y_cords, ".")
    plt.plot(x_cords, y_cords, "-")
    plt.show()

def new_route(citys):
    test= np.copy(citys)
    x=r.randint(0,len(test)-1)
    y=r.randint(0,len(test)-1)
    test[x]=citys[y]
    test[y]=citys[x]
    return test


def new_route_accept(new_rout, old_route,tempature):
    new= curquite_distace(new_rout)
    old= curquite_distace(old_route)
    if new <=old:
        lenths.append(new)
        return new_rout

    else:
        h=new-old

        if np.exp(-h/tempature)> r.random():
            lenths.append (new)
            return new_rout
        else:
            lenths.append(old)
            return old_route


def temp_schedule(temp,cooling_factor=.9999):
    return temp*cooling_factor

def pertange(start_temp, finished_temp, current_temp, cooling_factor,itterations):
    print itterations/math.log(finished_temp/start_temp,cooling_factor)

lenths=[]
def main():
    temps=[]
    itteration=0
    temp=250
    citys=city_list_gen(100, 100, 100)
    #total=math.log(finished_temp/start_temp,cooling_factor)
    #citys= [[ 18.,  11.],[ 68.,  37.],[ 90.,  57.],[ 13.,  81.],[ 19.,  49.],[ 89.,  48.],[ 46.,  97.],[ 68.,  22.],[ 42.,  84.],[ 16.,  67.]]
    print curquite_distace(citys)
    
    plot_route(citys)
    while temp > 0.1:
        temps.append(temp)
        itteration+=1
        new_rout = new_route(citys)
        citys = new_route_accept(new_rout,citys, temp)
        temp= temp_schedule(temp)
        print temp
    print curquite_distace(citys)

    plt.plot(np.arange(itteration),temps)
    plt.plot(np.arange(itteration),lenths)
    plt.show()
    plot_route(citys)


main()