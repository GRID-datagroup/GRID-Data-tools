import numpy as np


def get_edge(events, delta_t=1):
    tstart = np.min(events)
    tstop = np.max(events)
    return np.arange(tstart, np.ceil(tstop) + 1, delta_t)
