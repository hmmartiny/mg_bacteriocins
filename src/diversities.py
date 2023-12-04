import numpy as np

def shannon_diversity(y):
    notabs = ~np.isnan(y)
    t = y[notabs] / np.sum(y[notabs])
    t = t[t!=0]
    H = -np.sum(t * np.log(t))
    return H

def gini_simpson_diversity(y):
    notabs = ~np.isnan(y)
    t = y[notabs] / np.sum(y[notabs])
    D = 1 - np.sum(t**2)
    return D

def richness_diversity(y):
    notabs = ~np.isnan(y)
    t = y[notabs]
    return np.sum(t!=0)