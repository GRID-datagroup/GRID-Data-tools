import numpy as np
from matplotlib import pyplot as plt

from gbm.plot import Lightcurve
from gbm.plot.gbmplot import Histo, HistoErrorbars

from ..binning.binned import remove_zero_bins


class LightCurveGRID(Lightcurve):
    def __init__(self, figsize=(12, 4), **kwargs):
        self._minC = np.inf
        self._maxC = -1
        super().__init__(figsize=figsize, **kwargs)

    def set_data(self, data):
        """Set the lightcurve plotting data. If a lightcurve already exists,
        this triggers a replot of the lightcurve.

        Parameters
        ----------
        data: :class:`~gbm.data.primitives.TimeBins`
            The lightcurve data to plot
        """
        lc_color, lc_alpha, lc_kwargs = self._lc_settings()
        self._lc = Histo(data, self._ax, color=lc_color, alpha=lc_alpha, **lc_kwargs)
        eb_color, eb_alpha, eb_kwargs = self._eb_settings()
        self._errorbars = HistoErrorbars(
            data, self._ax, color=eb_color, alpha=eb_alpha, **eb_kwargs
        )

        self._minC = min(self._minC, np.min(data.rates))
        self._maxC = max(self._maxC, np.max(data.rates))

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

        self._minC = min(self._minC, np.min(data.rates))
        self._maxC = max(self._maxC, np.max(data.rates))

        self._ax.set_ylim(0.9 * self._minC, 1.1 * self._maxC)

    def save(self, title, path):
        self.ax.set_title(title)
        self.fig.savefig(path)
        plt.close(self.fig)
