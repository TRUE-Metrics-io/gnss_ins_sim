# -*- coding: utf-8 -*-
# Filename: demo_free_integration.py

"""
A simple free integration (strapdown inertial navigation) demo of Sim.
Created on 2018-01-23
@author: dongxiaoguang
"""

import os
import math
import numpy as np
from sim import imu_model
from sim import imu_sim

# globals
D2R = math.pi/180

data_path = os.path.abspath('.//motion_def_files//')
fs = 100.0          # IMU sample frequency

def test_free_integration():
    '''
    test Sim
    '''
    #### IMU model, typical for IMU381
    imu_err = {'gyro_b': np.array([0.0, 0.0, 0.0]),
               'gyro_arw': np.array([0.25, 0.25, 0.25]) * 1.0,
               'gyro_b_stability': np.array([3.5, 3.5, 3.5]) * 1.0,
               'gyro_b_corr': np.array([100.0, 100.0, 100.0]),
               'accel_b': np.array([0.0e-3, 0.0e-3, 0.0e-3]),
               'accel_vrw': np.array([0.03119, 0.03009, 0.04779]) * 1.0,
               'accel_b_stability': np.array([4.29e-5, 5.72e-5, 8.02e-5]) * 1.0,
               'accel_b_corr': np.array([200.0, 200.0, 200.0]),
               'mag_std': np.array([0.2, 0.2, 0.2]) * 1.0
              }
    # do not generate GPS and magnetometer data
    imu = imu_model.IMU(accuracy=imu_err, axis=6, gps=False)

    #### Algorithm
    # Free integration in a virtual inertial frame
    from algorithm import free_integration
    '''
    Free integration requires initial states (position, velocity and attitude). You should provide
    theses values when you create the algorithm object.
    '''
    ini_pos_vel_att = np.genfromtxt(data_path+"//motion_def-90deg_turn.csv",\
                                    delimiter=',', skip_header=1, max_rows=1)
    ini_pos_vel_att[0] = ini_pos_vel_att[0] * D2R
    ini_pos_vel_att[1] = ini_pos_vel_att[1] * D2R
    ini_pos_vel_att[6:9] = ini_pos_vel_att[6:9] * D2R
    # add initial states error if needed
    ini_vel_err = np.array([0.0, 0.0, 0.0]) # initial velocity error in the body frame, m/s
    ini_att_err = np.array([0.0, 0.0, 0.0]) # initial Euler angles error, deg
    ini_pos_vel_att[3:6] += ini_vel_err
    ini_pos_vel_att[6:9] += ini_att_err * D2R
    # create the algorith object
    algo = free_integration.FreeIntegration(ini_pos_vel_att)

    #### start simulation
    sim = imu_sim.Sim([fs, 0.0, 0.0], imu, data_path+"//motion_def-90deg_turn.csv",
                      ref_frame=1,
                      mode=None,
                      env=None,
                      algorithm=algo)
    sim.run(1000)
    # generate simulation results, summary
    # do not save data since the simulation runs for 1000 times and generates too many results
    sim.results()

if __name__ == '__main__':
    test_free_integration()
