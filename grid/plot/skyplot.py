import numpy as np
from matplotlib import pyplot as plt

from gbm.plot import SkyPlot
from gbm.data import HealPix
from gbm.coords import get_sun_loc

from ..data import PosAtt
from ..utils.coords import xyz_to_radec


class SkyPlotGRID(SkyPlot):
    """Plot on the sky in equatorial coordinates

    Attributes
    ----------
    _radius : float
        radius of earth, in meter
    _normal : array-like
        normal direction of detector
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_poshist(self, data: PosAtt, trigtime, geo=True, sun=True):
        """Add a Position History to plot the location of the Earth, Sun, and detector pointing

        Parameters
        ----------
        data: :class:`~grid.data.PosAtt`
            A Position History or Trigdat object
        trigtime: float, optional:
            The Trigdat trigger time overrides this
        geo: bool, optional
            If True, plot the Earth. Default is True.
        sun: bool, optional
            If True, plot the Sun. Default is True.
        """
        if sun:
            sun_loc = get_sun_loc(trigtime)
            self.plot_sun(*sun_loc)
        if geo:
            geo_ra, geo_dec = data.get_geocenter_radec(trigtime)
            radius = data.get_earth_radius(trigtime)
            self.plot_earth(geo_ra, geo_dec, radius)

        ra, dec = data.detector_pointing(trigtime)
        self.plot_detector(ra, dec, data.detector.id + "-10", radius=10)
        self.plot_detector(ra, dec, data.detector.id + "-30", radius=30)
        self.plot_detector(ra, dec, data.detector.id + "-60", radius=60)

    def plot_source(self, ra, dec, error=1, color="purple"):
        """Plot the direction of the GRB source

        Parameters
        ----------
        ra : float
            right ascension (degree)
        dec : float
            declination (degree)
        error : float
            error with a confidence of 1 sigma (in deg)
        color : str
            color
        """
        self._ax.plot(
            -np.deg2rad(ra - 180), np.deg2rad(dec), "*", color="red", markersize=10
        )
        self.plot_detector(ra, dec, "source", radius=error, color=color)
        gauss_map = HealPix.from_gaussian(ra, dec, error)
        self.add_healpix(gauss_map)

    def save(self, title, path):
        self.ax.set_title(title)
        self.fig.savefig(path)
        plt.close(self.fig)
