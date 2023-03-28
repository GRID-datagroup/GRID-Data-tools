import numpy as np

from gbm.binning.unbinned import bin_by_time


def bin_by_max_count(times, dt=1, maxN=50, normalize=True):
    """Binned by the boundary of histogram that the maximum count is bigger than threshold

    Parameters
    ----------
    times: np.array
        time of each event
    dt: int, optional
        Minimum bin width. The bin width is an integer multiple of step, by default 1
    maxN: int, optional
        Maximum count threshold, by default 50
    normalize: bool, optional
        whether to normalize the counts, by default True

    Returns
    -------
    :class:`~gbm.data.primitives.TimeBins`
        binned data
    """
    delta = dt
    edge = bin_by_time(times, delta)
    count, _ = np.histogram(times, bins=edge)
    if normalize:
        count = count / (edge[1:] - edge[:-1])
    try:
        while count.max() <= maxN:
            delta += dt
            edge = bin_by_time(times, delta)
            count, _ = np.histogram(times, bins=edge)
            if normalize:
                count = count / (edge[1:] - edge[:-1])
    except:
        edge = bin_by_time(times, dt)

    return edge
