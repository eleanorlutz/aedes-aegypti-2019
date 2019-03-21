import numpy as np
import pandas as pd
import math, random
from copy import deepcopy
from A_model_diagnostics import *

def anosmic(speedlist, anglelist, width, radius_food, food_x, food_y, origin, sensitivity):
    '''
    Explore the arena in an anosmic manner until finding the food source. 
    Returns time spent searching (in seconds) and trajectory path (xlist, ylist)
    '''
    finish_check = False # Check if the food has been reached
    valid_check = False # Check if current position is within arena bounds
    
    if origin == None:
        while valid_check == False:
            x0, y0 = np.random.uniform(0, width), np.random.uniform(0, width)
            valid_check = check_if_valid(x0, y0, width)
    else:
        x0, y0 = origin[0], origin[1]
    
    xlist, ylist, prev_angle = [x0], [y0], random.uniform(0, 360)
    finish_check = check_if_done(x0, y0, radius_food, food_x, food_y)

    # Continue moving until food has been found
    while finish_check == False:
        valid_check = False
        while valid_check == False:
            stepsize = get_curr_speed_exp(speedlist) 
            angle = get_angle(anglelist, prev_angle)
            x1, y1 = get_next_xy(x0, y0, angle, stepsize)
            valid_check = check_if_valid(x1, y1, width)
            
        xlist.append(x1)
        ylist.append(y1)

        x0, y0 = deepcopy(x1), deepcopy(y1) # update saved previous point 
        prev_angle = deepcopy(angle)
        finish_check = check_if_done(x0, y0, radius_food, food_x, food_y)
        
    return(len(xlist)/2, xlist, ylist)

def orthokinesis(speedlist, anglelist, width, radius_food, food_x, food_y, origin, sensitivity):
    '''
    Explore the arena in an orthokinetic manner until finding the food source. 
    Returns time spent searching (in seconds) and trajectory path (xlist, ylist)
    '''
    # Split the given speedlist into fast and slow segments
    prop_slow = 0.5
    speedlist.sort()
    list_num_slow = int(len(speedlist)*prop_slow)
    speedlist_slow = speedlist[0:list_num_slow]
    speedlist_fast = speedlist[list_num_slow:]

    c_limit = 50 # Changes behavior at 50% concentration
    finish_check = False # Check if the food has been reached
    valid_check = False # Check if current position is within arena bounds
    
    if origin == None:
        while valid_check == False:
            x0, y0 = np.random.uniform(0, width), np.random.uniform(0, width)
            valid_check = check_if_valid(x0, y0, width)
    else:
        x0, y0 = origin[0], origin[1]

    xlist, ylist, prev_angle = [x0], [y0], random.uniform(0, 360)
    finish_check = check_if_done(x0, y0, radius_food, food_x, food_y)
    curr_concentration = get_concentration(x0, y0, width/2, radius_food, food_x, food_y)
    
    # Continue moving until food has been found
    while finish_check == False:
        valid_check = False
        
        while valid_check == False:
            angle = get_angle(anglelist, prev_angle)

            # if concentration is detectable decrease speed
            if curr_concentration >= c_limit:
                stepsize = get_curr_speed_exp(speedlist_slow)
            else:
                stepsize = get_curr_speed_exp(speedlist_fast)

            x1, y1 = get_next_xy(x0, y0, angle, stepsize)
            valid_check = check_if_valid(x1, y1, width)

        xlist.append(x1)
        ylist.append(y1)

        x0, y0 = deepcopy(x1), deepcopy(y1) # update saved previous point 
        prev_angle = deepcopy(angle)
        curr_concentration = get_concentration(x0, y0, width/2, radius_food, food_x, food_y)
        finish_check = check_if_done(x0, y0, radius_food, food_x, food_y)
        
    return(len(xlist)/2, xlist, ylist)

def chemotaxis(speedlist, anglelist, width, radius_food, food_x, food_y, origin, sensitivity):
    '''
    Explore the arena in an chemotactic manner until finding the food source. 
    Returns time spent searching (in seconds) and trajectory path (xlist, ylist)
    '''
    radius = width/2
    finish_check = False # Check if the food has been reached
    valid_check = False # Check if current position is within arena bounds
    
    if origin == None:
        while valid_check == False:
            x0, y0 = np.random.uniform(0, width), np.random.uniform(0, width)
            valid_check = check_if_valid(x0, y0, width)
    else:
        x0, y0 = origin[0], origin[1]

    xlist, ylist, prev_angle = [x0], [y0], random.uniform(0, 360)
    finish_check = check_if_done(x0, y0, radius_food, food_x, food_y)
    prev_concentration = get_concentration(x0, y0, width/2, radius_food, food_x, food_y)
    curr_concentration = get_concentration(x0, y0, width/2, radius_food, food_x, food_y)
    
    # Continue moving until food has been found
    while finish_check == False:
        valid_check = False
        
        # Check the delta in concentration
        diff_concentration = curr_concentration - prev_concentration
        center_dist = np.hypot(np.abs(radius-y0), np.abs(radius-x0))
        wall_dist = radius - center_dist
 
        while valid_check == False:
            # If collision is imminent change behavior even if concentration-based
            if (diff_concentration >= sensitivity) and (wall_dist > 3):
                angle = prev_angle
            else:
                angle = get_angle(anglelist, prev_angle)

            stepsize = get_curr_speed_exp(speedlist)
            x1, y1 = get_next_xy(x0, y0, angle, stepsize)
            valid_check = check_if_valid(x1, y1, width)

        xlist.append(x1)
        ylist.append(y1)

        x0, y0 = deepcopy(x1), deepcopy(y1) # update saved previous point 
        prev_angle = deepcopy(angle)
        prev_concentration = deepcopy(curr_concentration)
        curr_concentration = get_concentration(x0, y0, width/2, radius_food, food_x, food_y)
        finish_check = check_if_done(x0, y0, radius_food, food_x, food_y)
        
    return(len(xlist)/2, xlist, ylist)

def klinokinesis(speedlist, anglelist, width, radius_food, food_x, food_y, origin, sensitivity):
    '''
    Explore the arena in an klinokinetic manner until finding the food source. 
    Returns time spent searching (in seconds) and trajectory path (xlist, ylist)
    '''
    radius = width/2
    c_limit = 50 # Changes behavior at 50% concentration
    finish_check = False # Check if the food has been reached
    valid_check = False # Check if current position is within arena bounds
    
    if origin == None:
        while valid_check == False:
            x0, y0 = np.random.uniform(0, width), np.random.uniform(0, width)
            valid_check = check_if_valid(x0, y0, width)
    else:
        x0, y0 = origin[0], origin[1]

    xlist, ylist, prev_angle = [x0], [y0], random.uniform(0, 360)
    finish_check = check_if_done(x0, y0, radius_food, food_x, food_y)
    
    # Continue moving until food has been found
    while finish_check == False:
        valid_check = False
        
        # IF CONCENTRATION INCREASED BY % OF TOTAL RANGE LOCK ANGLE
        curr_concentration = get_concentration(x0, y0, width/2, radius_food, food_x, food_y)
        center_dist = np.hypot(np.abs(radius-y0), np.abs(radius-x0))
        wall_dist = radius - center_dist
        
        while valid_check == False:
            # If collision is imminent change behavior even if concentration-based
            if (curr_concentration >= c_limit) and (wall_dist > 3):
                angle = prev_angle
            else:
                angle = get_angle(anglelist, prev_angle)

            stepsize = get_curr_speed_exp(speedlist)
            x1, y1 = get_next_xy(x0, y0, angle, stepsize)
            valid_check = check_if_valid(x1, y1, width)

        xlist.append(x1)
        ylist.append(y1)

        x0, y0 = deepcopy(x1), deepcopy(y1) # update saved previous point 
        prev_angle = deepcopy(angle)
        finish_check = check_if_done(x0, y0, radius_food, food_x, food_y)
        
    return(len(xlist)/2, xlist, ylist)