#! /usr/bin/python
# -*- coding: utf-8 -*-
import cPickle as pickle
import matplotlib.pyplot as plt
import numpy as np
import seaborn
import pandas as pd
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import Axes3D

def pitch(height):
    """ Calculate pitch of given height. """
    cde_list = ["c","d","e","f","g","a","b"]
    return cde_list[height % 7]

def doremi(cde):
    """ (c, d, e,...) to (do, re, mi...) """
    cde_list = ["c","d","e","f","g","a","b"]
    doremi_list = ["do","re","mi","fa","sol","la","si"]
    if not cde.lower() in cde_list:
        print "Error: " + cde.lower() + " not in cde list. "
    return doremi_list[cde_list.index(cde.lower())]


def plot_var(times, pitches, ends, var_n):
    """ Show time series graph of variation [var_n]. """
    # var_n: 0 to 30 (0: Aria)
    n_data = filter(lambda x:(ends[var_n] < x[0] <= ends[var_n+1]),
                    zip(times, pitches))
    # seaborn
    df = pd.DataFrame(n_data)
    df.columns = ["time","height"]
    seaborn.jointplot('time', 'height', data=df)
    plt.show()

def make_mat(times, pitches, full=False):
    """ Make t->t+a matrix from times, pitches. """
    tset = sorted(list(set(times)))
    if full:
        p_list = sorted(list(set(pitches)))
        z = zip(times, pitches)
        pitch_grouped = [[i[1] for i in z if i[0]==t] for t in tset]
        ret_mat = np.zeros([len(p_list), len(p_list)])
        for t in range(len(pitch_grouped)-1):
            for p in pitch_grouped[t]:
                for q in pitch_grouped[t+1]:
                    ret_mat[p_list.index(p)][p_list.index(q)] += 1
    else:# not full
        cde_list = ["c","d","e","f","g","a","b"]
        z = zip(times, [pitch(i) for i in pitches])
        pitch_grouped = [[i[1] for i in z if i[0]==t] for t in tset]
        ret_mat = np.zeros([len(cde_list), len(cde_list)])
        for t in range(len(pitch_grouped)-1):
            for p in pitch_grouped[t]:
                for q in pitch_grouped[t+1]:
                    ret_mat[cde_list.index(p)][cde_list.index(q)] += 1

    return ret_mat

def show_heatmap(mat, pitches, full=False):
    """ Show heatmap of matrix. """
    if full:
        i_list = [doremi(pitch(i)) for i in sorted(list(set(pitches)))]
        df = pd.DataFrame(mat)
        df.columns = i_list
        df.index = i_list
    else:
        doremi_list = ["do","re","mi","fa","sol","la","si"]
        df = pd.DataFrame(mat)
        df.columns = doremi_list
        df.index = doremi_list
    seaborn.heatmap(df, cmap='Blues')
    plt.show()

def show_3d(mat, pitches, full=False):
    if full:
        p_list = sorted(list(set(pitches)))
        x = np.array(p_list)
        y = np.array(p_list)
    else:
        x = np.arange(0, 7, 1)
        y = np.arange(0, 7, 1)
    X, Y = np.meshgrid(x, y)
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.plot_surface(X, Y, mat, cmap=plt.cm.jet, 
                    rstride=1, cstride=1, linewidth=0)
    plt.show()

if __name__ == "__main__":
    # load pickle
    pickle_file = 'goldberg_full.pickle'
    with open(pickle_file, 'rb') as f:
        g_pickle = pickle.load(f)

    # extract data from pickle
    times = g_pickle["times"]
    pitches = g_pickle["pitches"]
    end_times = g_pickle["end_times"]

    # Show times series graph
    plot_var(times, pitches, end_times, 30)

    # t -> t+1  Matrix
    mat = make_mat(times, pitches)
    show_heatmap(mat, pitches)

    full_mat = make_mat(times,pitches, True)
    show_heatmap(full_mat, pitches, True)

    show_3d(full_mat, pitches, True)
