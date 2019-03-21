import numpy as np
import pandas as pd
import math, random

def get_curr_speed_exp(speedlist):
    sample = random.choice(speedlist)
    return(sample)

def check_if_valid(x, y, width):
    ''' Returns bool whether or not this point is valid '''
    radius = width/2
    leg1 = np.abs(radius-y)
    leg2 = np.abs(radius-x)
    distance = np.hypot(leg1, leg2)
    if distance > radius:
        return False
    return True

def get_angle(anglelist, prev_angle):
    ''' Returns random angle between 0 and 360 '''
    sample = random.choice(anglelist)
    return prev_angle + sample

def get_next_xy(x0, y0, angle, stepsize):
    ''' Return next point as a function of angle and speed '''
    radian = np.deg2rad(angle)
    x1 = x0 + stepsize * math.cos(radian)
    y1 = y0 + stepsize * math.sin(radian)
    return x1, y1

def check_if_done(x0, y0, radius_food, food_x, food_y):
    ''' Returns true if the animal has found the food '''
    leg1 = np.abs(food_x-x0)
    leg2 = np.abs(food_y-y0)
    distance = np.hypot(leg1, leg2)
    if distance <= radius_food:
        return True
    return False

def get_concentration_based_on_distance(distance, a, b):
    ''' Use best fit line to return concentration estimate '''
    if distance <= 0:
        c = 100
    elif distance <= np.hypot(80, 30):
        c = np.exp(b)*np.exp(a*distance)
    else:
        c = 0
    return(c)

def get_concentration(x, y, radius, radius_food, food_x, food_y, 
                      a=-0.08046986117494856, b=4.897119830335053):
    leg1 = np.abs(food_x-x)
    leg2 = np.abs(food_y-y)
    distance = np.hypot(leg1, leg2)
    distance = distance-radius_food 
    c = get_concentration_based_on_distance(distance, a, b)
    return(c)

def get_radius_food(width, perc_area=0.03):
    '''
    perc_area = proportion of arena that should be taken up by food. width = width of arena. 
    '''
    r = width/2
    arena_a = math.pi * r * r
    food_a = arena_a * perc_area
    food_r = np.sqrt(food_a / math.pi)
    return food_r

def run_simulations(n_trials, widths, savename, speedlist, anglelist, function, 
                    origin=None, sensitivity=1):
    # Initialize DF to save values into
    colnames = [str(int(x)) for x in widths]
    rownames = np.arange(0, n_trials)
    rownames = [str(int(x))+'_trial' for x in rownames]
    df_out = pd.DataFrame(index=rownames, columns=colnames)
    
    for width in widths: 
        tlist = []
        radius_food = get_radius_food(width)
        food_x = width/2 # x position of food center
        food_y = width/2 # y position of food center

        for n in range(n_trials):
            timecount, xlist, ylist = function(speedlist, anglelist, 
                                                 width, radius_food, food_x, food_y, origin, sensitivity)
            tlist.append(timecount)

        df_out[str(width)] = tlist

    df_out.to_csv(savename, index=False)
    df_out.head()