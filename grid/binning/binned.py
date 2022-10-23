import numpy as np
from gbm.data.primitives import Bins


def remove_zero_bins(data: Bins):
    idx = np.where(data.counts > 0)
    counts = data.counts[idx]
    lo_edges = data.lo_edges[idx]
    hi_edges = data.hi_edges[idx]
    return Bins(counts, lo_edges, hi_edges, hi_edges - lo_edges)


def get_edges(data: Bins):
    return np.sort(np.unique(np.hstack((data.lo_edges, data.hi_edges))))
