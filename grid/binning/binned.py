import numpy as np

from gbm.data.primitives import TimeBins


def remove_zero_bins(data: TimeBins):
    idx = np.where(data.counts > 0)
    counts = data.counts[idx]
    lo_edges = data.lo_edges[idx]
    hi_edges = data.hi_edges[idx]
    return TimeBins(counts, lo_edges, hi_edges, hi_edges - lo_edges)


def get_edges(data: TimeBins):
    return np.sort(np.unique(np.hstack((data.lo_edges, data.hi_edges))))
