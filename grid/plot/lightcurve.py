import numpy as np

from gbm.plot import Lightcurve

from ..binning.binned import remove_zero_bins


class LightCurveGRID(Lightcurve):
    def __init__(self, figsize=(12, 4), **kwargs):
        super().__init__(figsize=figsize, **kwargs)

    def plot_curve(self, data, color="blue", **kwargs):
        """Plot extra curve

        Parameters
        ----------
        data: :class:`~gbm.data.primitives.TimeBins:
            The lightcurve data to plot
        color: str
            color of curve
        """
        for seg in remove_zero_bins(data).contiguous_bins():
            edges = np.concatenate(
                ([seg.lo_edges[0]], seg.lo_edges, [seg.hi_edges[-1]])
            )
            rates = np.concatenate(([seg.rates[0]], seg.rates, [seg.rates[-1]]))
            self._ax.step(edges, rates, where="post", color=color, **kwargs)

    def save(self, title, path):
        self._ax.set_title(title)
        self._figure.savefig(path)
