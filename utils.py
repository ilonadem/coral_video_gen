import os
import numpy as np
import csv
import glob

import pandas as pd
from ast import literal_eval

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import FFMpegWriter

from functools import partial

def est_to_pst(pst_h, pst_d):
    est_hour = str((int(pst_h)-5)%24)
    if int(est_hour) < 10:
        est_hour = '0' + est_hour
    if int(pst_h)<6:
        est_day = '0' + str(int(pst_d)-1)
    else:
        est_day = pst_d

    return est_hour, est_day

def listdir(path):
    return glob.glob(os.path.join(path, '*'))

def create_df_from_hour(hourdir):

    def create_df(file):
        print(file)
        raw_df = pd.read_csv(file)
        f_df = pd.DataFrame(columns=keypoints)
        for kp in keypoints:
            f_df[kp] = literal_eval(raw_df[kp][0])
        
        return f_df
            
    
    data_files = listdir(hourdir)
    data_files.sort()
    
    df_full = create_df(data_files[0])

    for f in data_files[1:]:
        df_new = create_df(f)
        df_full = pd.concat([df_full, df_new])
        
    return df_full

def make_detailed_df(clean_coral_df):

    for kp in keypoints:
        clean_coral_df[kp] = clean_coral_df.apply(lambda row: [np.float(row[kp][0]), 
                                                               np.float(row[kp][1]),
                                                               np.float(row[kp][2])], 
                                                  axis=1)

    clean_coral_df['FOOT'] = clean_coral_df.apply(lambda row: [0.5*row.LEFT_ANKLE[0] + 0.5*row.RIGHT_ANKLE[0],
                                                              0.5*row.LEFT_ANKLE[1] + 0.5*row.RIGHT_ANKLE[1]], 
                                                  axis=1)

    clean_coral_df['LEFT_SHANK'] = clean_coral_df.apply(lambda row: [0.5*row.LEFT_KNEE[0] + 0.5*row.LEFT_ANKLE[0],
                                                                    0.5*row.LEFT_KNEE[1] + 0.5*row.LEFT_ANKLE[1]],
                                                        axis=1)

    clean_coral_df['RIGHT_SHANK'] = clean_coral_df.apply(lambda row: [0.5*row.RIGHT_KNEE[0] + 0.5*row.RIGHT_ANKLE[0],
                                                                       0.5*row.RIGHT_KNEE[1] + 0.5*row.RIGHT_ANKLE[1]], 
                                                           axis=1)

    clean_coral_df['SHANK'] = clean_coral_df.apply(lambda row: [0.5*row.LEFT_SHANK[0] + 0.5*row.RIGHT_SHANK[0],
                                                                 0.5*row.LEFT_SHANK[1] + 0.5*row.RIGHT_SHANK[1]],
                                                     axis=1)

    clean_coral_df['LEFT_THIGH'] = clean_coral_df.apply(lambda row: [0.5*row.LEFT_KNEE[0] + 0.5*row.LEFT_HIP[0],
                                                                    0.5*row.LEFT_KNEE[1] + 0.5*row.LEFT_HIP[1]],
                                                        axis=1)
    clean_coral_df['RIGHT_THIGH'] = clean_coral_df.apply(lambda row: [0.5*row.RIGHT_KNEE[0] + 0.5*row.RIGHT_HIP[0],
                                                                     0.5*row.RIGHT_KNEE[1] + 0.5*row.RIGHT_HIP[1]], 
                                                         axis=1)

    clean_coral_df['THIGH'] = clean_coral_df.apply(lambda row: [0.5*row.LEFT_THIGH[0] + 0.5*row.RIGHT_THIGH[0],
                                                               0.5*row.LEFT_THIGH[1] + 0.5*row.RIGHT_THIGH[1]],
                                                   axis=1)

    clean_coral_df['HAND'] = clean_coral_df.apply(lambda row: [0.5*row.LEFT_WRIST[0] + 0.5*row.RIGHT_WRIST[0],
                                                                0.5*row.LEFT_WRIST[1] + 0.5*row.RIGHT_WRIST[1]],
                                                    axis=1)

    clean_coral_df['LEFT_FOREARM'] = clean_coral_df.apply(lambda row: [0.5*row.LEFT_WRIST[0] + 0.5*row.LEFT_ELBOW[0],
                                                                      0.5*row.LEFT_WRIST[1] + 0.5*row.LEFT_ELBOW[1]],
                                                          axis=1)
    clean_coral_df['RIGHT_FOREARM'] = clean_coral_df.apply(lambda row: [0.5*row.RIGHT_WRIST[0] + 0.5*row.RIGHT_ELBOW[0],
                                                                         0.5*row.RIGHT_WRIST[1] + 0.5*row.RIGHT_ELBOW[1]], 
                                                             axis=1)

    clean_coral_df['FOREARM'] = clean_coral_df.apply(lambda row: [0.5*row.LEFT_WRIST[0] + 0.5*row.RIGHT_WRIST[0],
                                                                 0.5*row.LEFT_WRIST[1] + 0.5*row.RIGHT_WRIST[1]],
                                                     axis=1)

    clean_coral_df['LEFT_UPARM'] = clean_coral_df.apply(lambda row: [0.5*row.LEFT_SHOULDER[0] + 0.5*row.LEFT_ELBOW[0],
                                                                    0.5*row.LEFT_SHOULDER[1] + 0.5*row.LEFT_ELBOW[1]],
                                                        axis=1)
    clean_coral_df['RIGHT_UPARM'] = clean_coral_df.apply(lambda row: [0.5*row.RIGHT_SHOULDER[0] + 0.5*row.RIGHT_ELBOW[0],
                                                                     0.5*row.RIGHT_SHOULDER[1] + 0.5*row.RIGHT_ELBOW[1]],
                                                         axis=1)

    clean_coral_df['UPARM'] = clean_coral_df.apply(lambda row: [0.5*row.LEFT_UPARM[0] + 0.5*row.RIGHT_UPARM[0],
                                                               0.5*row.LEFT_UPARM[1] + 0.5*row.RIGHT_UPARM[1]],
                                                   axis=1)

    clean_coral_df['PELVIS'] = clean_coral_df.apply(lambda row: [0.5*row.LEFT_HIP[0] + 0.5*row.RIGHT_HIP[0],
                                                                  0.5*row.LEFT_HIP[1] + 0.5*row.RIGHT_HIP[1]], 
                                                      axis=1)

    clean_coral_df['LEFT_THORAX'] = clean_coral_df.apply(lambda row: [0.5*row.LEFT_SHOULDER[0] + 0.5*row.LEFT_HIP[0],
                                                                       0.5*row.LEFT_SHOULDER[1] + 0.5*row.LEFT_HIP[1]],
                                                           axis=1)
    clean_coral_df['RIGHT_THORAX'] = clean_coral_df.apply(lambda row: [0.5*row.RIGHT_SHOULDER[0] + 0.5*row.RIGHT_HIP[0],
                                                                      0.5*row.RIGHT_SHOULDER[1] + 0.5*row.RIGHT_HIP[1]],
                                                          axis=1)

    clean_coral_df['THORAX'] = clean_coral_df.apply(lambda row: [0.5*row.LEFT_THORAX[0] + 0.5*row.RIGHT_THORAX[0],
                                                                0.5*row.LEFT_THORAX[1] + 0.5*row.RIGHT_THORAX[1]], 
                                                    axis=1)

    clean_coral_df['HEAD'] = clean_coral_df['NOSE']

    clean_coral_df['TRUNK'] = clean_coral_df['THORAX']

    clean_coral_df['COM'] = clean_coral_df.apply(lambda row: [(1/1.286)*(0.0145*row.FOOT[0] + 
                                                                          0.0465*row.SHANK[0] + 
                                                                          0.10*row.THIGH[0] + 
                                                                          0.006*row.HAND[0] + 
                                                                          0.016*row.FOREARM[0] + 
                                                                          0.028*row.UPARM[0] + 
                                                                          0.142*row.PELVIS[0] + 
                                                                          0.355*row.THORAX[0] + 
                                                                          0.081*row.HEAD[0] + 
                                                                          0.497*row.TRUNK[0]),
                                                               (1/1.286)*(0.0145*row.FOOT[1] + 
                                                                          0.0465*row.SHANK[1] + 
                                                                          0.10*row.THIGH[1] + 
                                                                          0.006*row.HAND[1] + 
                                                                          0.016*row.FOREARM[1] + 
                                                                          0.028*row.UPARM[1] + 
                                                                          0.142*row.PELVIS[1] + 
                                                                          0.355*row.THORAX[1] + 
                                                                          0.081*row.HEAD[1] + 
                                                                          0.497*row.TRUNK[1])] , axis=1)


    return clean_coral_df

def add_time(df):
    df['time'] = df.apply(lambda row: row.NOSE[-1], axis=1)
    df['time_int'] = df.apply(lambda row: int(row.time[:2])+ int(row.time[-5:-3])/60 + int(row.time[-2:])/6000, axis=1)
    return df

keypoints = ['NOSE', 'LEFT_EYE', 'RIGHT_EYE', 'LEFT_EAR', 'RIGHT_EAR', 
             'LEFT_SHOULDER', 'RIGHT_SHOULDER', 'LEFT_ELBOW', 
             'RIGHT_ELBOW', 'LEFT_WRIST', 'RIGHT_WRIST', 'LEFT_HIP', 
             'RIGHT_HIP', 'LEFT_KNEE', 'RIGHT_KNEE', 'LEFT_ANKLE', 
             'RIGHT_ANKLE']

# indeces of keypoints between which we want to draw a line
num_edges = ((0, 1),(0, 2),(0, 3),(0, 4),(3, 1),(4, 2),
             (1, 2),(5, 6),(5, 7),(5, 11),(6, 8),(6, 12),
             (7, 9),(8, 10),(11, 12),(11, 13),(12, 14),
             (13, 15),(14, 16),)

# same list but as keypoint names 
EDGES = (
    ('NOSE', 'LEFT_EYE'),
    ('NOSE', 'RIGHT_EYE'),
    ('NOSE', 'LEFT_EAR'),
    ('NOSE', 'RIGHT_EAR'),
    ('LEFT_EAR', 'LEFT_EYE'),
    ('RIGHT_EAR', 'RIGHT_EYE'),
    ('LEFT_EYE', 'RIGHT_EYE'),
    ('LEFT_SHOULDER', 'RIGHT_SHOULDER'),
    ('LEFT_SHOULDER', 'LEFT_ELBOW'),
    ('LEFT_SHOULDER', 'LEFT_HIP'),
    ('RIGHT_SHOULDER', 'RIGHT_ELBOW'),
    ('RIGHT_SHOULDER', 'RIGHT_HIP'),
    ('LEFT_ELBOW', 'LEFT_WRIST'),
    ('RIGHT_ELBOW', 'RIGHT_WRIST'),
    ('LEFT_HIP', 'RIGHT_HIP'),
    ('LEFT_HIP', 'LEFT_KNEE'),
    ('RIGHT_HIP', 'RIGHT_KNEE'),
    ('LEFT_KNEE', 'LEFT_ANKLE'),
    ('RIGHT_KNEE', 'RIGHT_ANKLE'),
)
