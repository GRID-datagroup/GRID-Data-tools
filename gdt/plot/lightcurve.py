import numpy as np
from gbm.plot import Lightcurve
from gbm.data.primitives import TimeBins


def remove_zero_bins(data: TimeBins):
    idx = np.where(data.counts > 0)
    counts = data.counts[idx]
    lo_edges = data.lo_edges[idx]
    hi_edges = data.hi_edges[idx]
    return TimeBins(counts, lo_edges, hi_edges, hi_edges - lo_edges)


class LightCurveGRID(Lightcurve):
    def __init__(self, figsize=(12, 4), **kwargs):
        super().__init__(figsize=figsize, **kwargs)

    def plot_curve(self, count, edges, weight=None, color="orange", **kwargs):
        """Plot curve

        Parameters
        ----------
        count : array(int)
            count per bin
        edges: array(float)
            low and high edge of per bin
        color: str
            color of curve
        """
        weight = np.ones_like(count) if weight is None else weight
        data = TimeBins(count * weight, edges[:-1], edges[1:], edges[1:] - edges[:-1])
        for seg in remove_zero_bins(data).contiguous_bins():
            edges = np.concatenate(
                ([seg.lo_edges[0]], seg.lo_edges, [seg.hi_edges[-1]])
            )
            rates = np.concatenate(([seg.rates[0]], seg.rates, [seg.rates[-1]]))

            self._ax.step(edges, rates, where="post", color=color, **kwargs)

    def plot_light_curve(self, count, edges):
        """Plot light curve

        Parameters
        ----------
        count : array(int)
            count per bin
        edges: array(float)
            low and high edge of per bin
        dire: bool, optional
            if true, draw points to indicate direction, from red to blue, default true.
        """
        data = TimeBins(count, edges[:-1], edges[1:], edges[1:] - edges[:-1])
        self.set_data(data)

    def save(self, title, path):
        self._ax.set_title(title)
        self._figure.savefig(path)
