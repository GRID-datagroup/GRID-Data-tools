import numpy as np


def get_edge(events, delta_t=1):
    t_begin = np.min(events)
    t_end = np.max(events)
    return np.arange(t_begin, np.ceil(t_end) + 1, delta_t)
