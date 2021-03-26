import numpy as np

b=1.4826 


def rescale(scores_list, threshold = 2.5):
    """ takes a numpy array of scores (or any numbers),
    and returns a rescaled array """
    median = np.median(scores_list)
    devs =  abs(scores_list - median)
    mad = np.median(devs) * b
    rescaled  = abs(scores_list -  median)/mad  
    return rescaled  

def is_outlier(scores_list, threshold = 2.5):
    """ takes a numpy array of scores (or any numbers),
    and returns a Boolean array indicating if the score is an outlier """ 
    rescaled  = rescale(scores_list, threshold = 2.5)
    outliers = rescaled > 2.5 
    return outliers
