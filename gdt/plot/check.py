from matplotlib import pyplot as plt

from .earthplot import EarthPlotGRID
from .lightcurve import LightCurveGRID


class CheckGRID(object):
    """Draw lightcurve and map to check

    Paramaters
    ----------
    id : str, optional
        id of satellite
    hia : bool, optional
        whether to draw high ion area
    figsize : tuple, optional
        figure size
    """

    def __init__(self, id="G02", hia=True, figsize=(13, 11)):
        self._figure = plt.figure(figsize=figsize, dpi=100)
        self._ax1 = self._figure.add_subplot(2, 1, 1)
        self._ax2 = self._figure.add_subplot(2, 1, 2)
        self._canvas = self._figure.canvas
        self.curve = LightCurveGRID(canvas=self._canvas, axis=self._ax1)
        self.earthplot = EarthPlotGRID(
            id=id, hia=hia, canvas=self._canvas, axis=self._ax2
        )

    @property
    def ax1(self):
        return self._ax1

    @property
    def ax2(self):
        return self._ax2

    def plot_curve(self, count, edges, weight=None, color="b", **kwargs):
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
        self.curve.plot_curve(count, edges, weight, color, **kwargs)

    def plot_light_curve(self, count, edges):
        """Plot light curve

        Parameters
        ----------
        count : array(int)
            count per bin
        edges: array(float)
            low and high edge of per bin
        """
        self.curve.plot_light_curve(count, edges)

    def plot_orbit(self, lon, lat, dire=True):
        """Plot orbit

        Parameters
        ----------
        lon/lat : array(float)
            longitude or latitude of detector
        dire: bool, optional
            if true, draw two points to indicate direction, from red point to green point, default true.
        """
        self.earthplot.plot_orbit(lon, lat, dire)

    def plot_hia_orbit(self, lon, lat, color="blue"):
        """Plot hia orbit

        Parameters
        ----------
        lon/lat : array(float)
            longitude or latitude of detector
        color: string, optional
            color of orbit, default black.
        """
        self.earthplot.plot_hia_orbit(lon, lat, color)

    def plot_high_ion_area(self, nx=720, ny=360):
        """Plot high ion area

        Parameters
        ----------
        nx/ny: int, optional
            grid number of longitude/latitude
        """
        self.earthplot.plot_high_ion_area(nx, ny)

    def save(self, title, path):
        self._ax1.set_title(title + "\n Light Curve")
        self._ax2.set_title("Orbit")
        self._figure.savefig(path)
