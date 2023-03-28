from matplotlib import pyplot as plt

from .earthplot import EarthPlotGRID
from .lightcurve import LightCurveGRID


class CheckPlotGRID(object):
    """Draw lightcurve and map to check

    Paramaters
    ----------
    lc: :class:`~gbm.data.primitives.TimeBins`
        light curve data to plot
    orb: :class:`~grid.data.PosAtt`
        A Position History fits file
    trigtime: float, optional
        set trigtime to a particular time of interest to plot detector's orbital location
    hia: bool, optional
        whether to draw high ion area
    figsize: tuple, optional
        figure size
    """

    def __init__(self, lc, orb, trigtime=None, hia=True, figsize=(13, 11)):
        self._figure = plt.figure(figsize=figsize, dpi=100)
        self._ax1 = self._figure.add_subplot(2, 1, 1)
        self._ax2 = self._figure.add_subplot(2, 1, 2)
        self._canvas = self._figure.canvas
        self.curve = LightCurveGRID(data=lc, canvas=self._canvas, axis=self._ax1)
        self.earth = EarthPlotGRID(canvas=self._canvas, axis=self._ax2)
        self.earth.add_poshist(orb, trigtime=trigtime, hia=hia)

    @property
    def fig(self):
        return self._figure

    @property
    def ax1(self):
        return self._ax1

    @property
    def ax2(self):
        return self._ax2

    def plot_curve(self, data, color="blue", **kwargs):
        """Plot extra curve

        Parameters
        ----------
        data: :class:`~gbm.data.primitives.TimeBins`
            The lightcurve data to plot
        color: str
            color of curve
        """
        self.curve.plot_curve(data, color, **kwargs)

    def plot_orbit(self, data, color="blue", numpts=1000):
        """Plot extra orbit

        Parameters
        ----------
        data: :class:`~grid.data.PosAtt`
            A Position History fits file
        color: string, optional
            color of orbit, default blue.
        numpts: int, optional
            The number of interpolation points for plotting the orbit. Default is 1000.
        """
        self.earth.plot_orbit(data, color, numpts)

    def save(self, title, path):
        self.ax1.set_title(title + "\n Light Curve")
        self.ax2.set_title("Orbit")
        self.fig.savefig(path)
        plt.close(self.fig)
