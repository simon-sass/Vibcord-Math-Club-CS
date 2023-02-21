import numpy as np
import random
import matplotlib.pyplot as plt
import math
import pandas as pd

# Find average number of people who walk out with less balls than they start out with (1 -> 0)

# Person Matrix:
# [[Whether or not they will steal]
#  [If they will steal, which person in the room they will target]
#  [Whether or not they have balls to start out with]
#  [After operation is performed how many balls the person has]]

# Probability a person feels the need to steal a ball before entering the room
STEAL_P = .50

# Probability a person has balls before entering the room
BALL_START_P = .50

def create_person(id, size, steal_p, ball_start_p):
    will_steal = True if (random.random() <= steal_p) else False
    target = id
    # This is to ensure a person does not try to steal their own balls
    while target == id: target = random.randrange(0, size)
    starting_balls = True if (random.random() <= ball_start_p) else False
    person = [will_steal, target, starting_balls, starting_balls]
    return person

def create_room(size, steal_p, ball_start_p):
    room = np.zeros((4, size), dtype=int)
    for i in range(size):
        room[:, i] = create_person(i, size, steal_p, ball_start_p)
    return room

def zip_process(size):
    room = create_room(size, STEAL_P, BALL_START_P)
    for i in range(size):
        if room[0][i] == 1:
            target = room[1][i]
            if room[3][target] >= 1:
                room[3][target] -= 1
                room[3][i] += 1
    less_balls = 0
    for i in range(size):
        if room[3][i] < room[2][i]:
            less_balls += 1
    return room, less_balls

def trials(reps, size):
    less_balls_data = np.zeros(reps, dtype=int)
    for i in range(reps):
        less_balls_data[i] = zip_process(size)[1]
    return less_balls_data

def trials_averages(a_reps, reps, size):
    averages = np.zeros(a_reps, dtype=int)
    for i in range(a_reps):
        averages[i] = np.average(trials(reps, size))
    return averages

# Confidence interval for determing number of trialss per room size
# Z_SCORE = 3.291
# TRIALS = 10
# ROOM_SIZE = 1000
# a = trials_averages(10, TRIALS, ROOM_SIZE)
# std = np.std(a)
# mean = np.average(a)
# ci = Z_SCORE*(std/math.sqrt(ROOM_SIZE))

# Finding the average amount of people who come out of the zip room with less balls than they went in with from room size 2-1000 and exporting it to a csv
# size_cap = 1000
# final_averages = np.zeros([size_cap-1, 2])
# for i in range(1, size_cap):
#     final_averages[i-1][0] = i+1
#     final_averages[i-1][1] = np.average(trials_averages(10, 10, i+1))
# df = pd.DataFrame(final_averages, columns=["Room Size", "Average"])
# print(df)
# df.to_csv('rooms2x1000-10x10trials.csv', index=None)
