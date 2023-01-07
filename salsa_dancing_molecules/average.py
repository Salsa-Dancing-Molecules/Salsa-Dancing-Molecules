"""Calculate time-average of an array."""

import numpy as np


def average(t0, array):
    """Calculate time average of array.

    Example: average(2, [0,1,2,3,4,5]) -> [2, 2.5, 3, 3.5]

    Input:
        t0: int      - timstep when steady state starts
        array: array - array to output time average for

    Output:
        array        - array of evolution of the mean over time.
                       Each element in the array, n=t0...len(array),
                       is the average over the interval [t0,n].
                       Value of the last element corresponds to the
                       time average over interval [t0, len(array)].
    """
    array = array[t0::]
    average = []
    for n in array:
        n_average = (np.sum(array[0:(len(average))]) + n) / (len(average) + 1)
        average.append(n_average)
    return average
