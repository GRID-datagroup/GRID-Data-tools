import numpy as np


def bin_by_max_count(times, dt=1, maxN=50):
    """Gets the boundary of histogram that the maximum count is bigger than threshold
    Parameters
    ----------
    times: np.array
        time of each event
    dt: int, optional
        Minimum bin width. The bin width is an integer multiple of step.
    maxN: int, optional
        Maximum count threshold
    """
    delta = dt
    edge = np.arange(times.min(), times.max() + 1, delta)
    count, _ = np.histogram(times, bins=edge)
    try:
        while count.max() <= maxN:
            delta += dt
            edge = np.arange(times.min(), times.max() + 1, delta)
            count, _ = np.histogram(times, bins=edge)
    except:
        edge = np.arange(times.min(), times.max() + 1, dt)

    return edge
