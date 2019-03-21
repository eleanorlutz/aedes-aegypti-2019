import numpy as np
import pandas as pd
import math, random
from copy import deepcopy
from A_model_diagnostics import *

def anosmic_averse(speedlist, anglelist, width, radius_food, food_x, food_y, origin, sensitivity):
    '''
    Explore the arena in an anosmic manner for 15 minutes. 
    Returns time spent near poison (in %) and trajectory path (xlist, ylist)
    '''
    poison_count = 0
    valid_check = False # Check if current position is within arena bounds
    
    if origin == None:
        while valid_check == False:
            x0, y0 = np.random.uniform(0, width), np.random.uniform(0, width)
            valid_check = check_if_valid(x0, y0, width)
    else:
        x0, y0 = origin[0], origin[1]
    
    xlist, ylist, prev_angle = [x0], [y0], random.uniform(0, 360)
    
    # Continue moving for 15 minutes, in 2fps increments
    for n in range(0, 1801):
        
        curr_concentration = get_concentration(x0, y0, width/2, radius_food, food_x, food_y)
        if curr_concentration >= 50:
            poison_count += 1
        
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
        
    # Check the last frame that wasn't checked within the loop
    curr_concentration = get_concentration(xlist[-1], ylist[-1], width/2, radius_food, food_x, food_y)
    if curr_concentration >= 50:
        poison_count += 1
    
    return(poison_count/len(xlist), xlist, ylist)


def orthokinesis_averse(speedlist, anglelist, width, radius_food, food_x, food_y, origin, sensitivity):
    '''
    Explore the arena in an orthokinetic manner for 15 minutes. 
    Returns time spent near poison (in %) and trajectory path (xlist, ylist)
    '''
    poison_count = 0
    
    # Split the given speedlist into fast and slow segments
    prop_slow = 0.5
    speedlist.sort()
    list_num_slow = int(len(speedlist)*prop_slow)
    speedlist_slow = speedlist[0:list_num_slow]
    speedlist_fast = speedlist[list_num_slow:]

    c_limit = 50 # Changes behavior at 50% concentration
    valid_check = False # Check if current position is within arena bounds
    
    if origin == None:
        while valid_check == False:
            x0, y0 = np.random.uniform(0, width), np.random.uniform(0, width)
            valid_check = check_if_valid(x0, y0, width)
    else:
        x0, y0 = origin[0], origin[1]

    xlist, ylist, prev_angle = [x0], [y0], random.uniform(0, 360)
    
    # Continue moving for 15 minutes, in 2fps increments
    for n in range(0, 1801):
        
        curr_concentration = get_concentration(x0, y0, width/2, radius_food, food_x, food_y)
        if curr_concentration >= 50:
            poison_count += 1
        valid_check = False

        while valid_check == False:
            angle = get_angle(anglelist, prev_angle)

            # if concentration is detectable increase speed
            if curr_concentration >= c_limit:
                stepsize = get_curr_speed_exp(speedlist_fast)
            else:
                stepsize = get_curr_speed_exp(speedlist_slow)

            x1, y1 = get_next_xy(x0, y0, angle, stepsize)
            valid_check = check_if_valid(x1, y1, width)

        xlist.append(x1)
        ylist.append(y1)

        x0, y0 = deepcopy(x1), deepcopy(y1) # update saved previous point 
        prev_angle = deepcopy(angle)
    
    # Check the last frame that wasn't checked within the loop
    curr_concentration = get_concentration(xlist[-1], ylist[-1], width/2, radius_food, food_x, food_y)
    if curr_concentration >= 50:
        poison_count += 1

    return(poison_count/len(xlist), xlist, ylist)

def chemotaxis_averse(speedlist, anglelist, width, radius_food, food_x, food_y, origin, sensitivity):
    '''
    Explore the arena in an chemotactic manner for 15 minutes. 
    Returns time spent near poison (in %) and trajectory path (xlist, ylist)
    '''
    poison_count = 0
    radius = width/2
    valid_check = False # Check if current position is within arena bounds
    
    if origin == None:
        while valid_check == False:
            x0, y0 = np.random.uniform(0, width), np.random.uniform(0, width)
            valid_check = check_if_valid(x0, y0, width)
    else:
        x0, y0 = origin[0], origin[1]

    xlist, ylist, prev_angle = [x0], [y0], random.uniform(0, 360)
    prev_concentration = get_concentration(x0, y0, width/2, radius_food, food_x, food_y)
    
    # Continue moving for 15 minutes, in 2fps increments
    for n in range(0, 1801):
        
        curr_concentration = get_concentration(x0, y0, width/2, radius_food, food_x, food_y)
        if curr_concentration >= 50:
            poison_count += 1
        valid_check = False
        
        # Check the delta in concentration
        diff_concentration = curr_concentration - prev_concentration
        center_dist = np.hypot(np.abs(radius-y0), np.abs(radius-x0))
        wall_dist = radius - center_dist
            
        while valid_check == False:
            # If collision is imminent change behavior even if concentration-based
            if (diff_concentration <= -sensitivity) and (wall_dist > 3):
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
        
    # Check the last frame that wasn't checked within the loop
    curr_concentration = get_concentration(xlist[-1], ylist[-1], width/2, radius_food, food_x, food_y)
    if curr_concentration >= 50:
        poison_count += 1
        
    return(poison_count/len(xlist), xlist, ylist)

def klinokinesis_averse(speedlist, anglelist, width, radius_food, food_x, food_y, origin, sensitivity):
    '''
    Explore the arena in an klinokinetic manner for 15 minutes. 
    Returns time spent near poison (in %) and trajectory path (xlist, ylist)
    '''
    poison_count = 0
    radius = width/2
    c_limit = 50 # Changes behavior at 50% concentration
    valid_check = False # Check if current position is within arena bounds
    
    if origin == None:
        while valid_check == False:
            x0, y0 = np.random.uniform(0, width), np.random.uniform(0, width)
            valid_check = check_if_valid(x0, y0, width)
    else:
        x0, y0 = origin[0], origin[1]

    xlist, ylist, prev_angle = [x0], [y0], random.uniform(0, 360)
    
    # Continue moving for 15 minutes, in 2fps increments
    for n in range(0, 1801):
        
        curr_concentration = get_concentration(x0, y0, width/2, radius_food, food_x, food_y)
        if curr_concentration >= 50:
            poison_count += 1
        valid_check = False

        center_dist = np.hypot(np.abs(radius-y0), np.abs(radius-x0))
        wall_dist = radius - center_dist

        while valid_check == False:
            # If collision is imminent change behavior even if concentration-based
            if (curr_concentration < c_limit) and (wall_dist > 3):
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
        
    # Check the last frame that wasn't checked within the loop
    curr_concentration = get_concentration(xlist[-1], ylist[-1], width/2, radius_food, food_x, food_y)
    if curr_concentration >= 50:
        poison_count += 1
        
    return(poison_count/len(xlist), xlist, ylist)