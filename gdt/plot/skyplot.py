import numpy as np
from gbm.plot import SkyPlot
from gbm.data import HealPix
from pyquaternion import Quaternion

from ..utils.coords import get_sun_pos, xyz_to_radec, get_geocenter_pos


class SkyPlotGRID(SkyPlot):
    """Plot on the sky in equatorial coordinates

    Attributes
    ----------
    _radius : float
        radius of earth, in meter
    _normal : array-like
        normal direction of detector
    """

    _radius = 6378137.0
    _normal = np.array([0, 0, -1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def plot_sun_d(self, utc, **kwargs):
        """Plot the sun

        Parameters
        ----------
        utc : float
            utc time
        """
        ra, dec = get_sun_pos(utc)
        self.plot_sun(ra, dec, **kwargs)

    def plot_earth_d(self, coord, altitude):
        """Plot the earth

        Parameters
        ----------
        coord : (float, float, float)
            coordinate tuple of detector in eic
        altitude: float
            altitudes of detector in eic
        """
        ra, dec = get_geocenter_pos(coord)
        radius = np.rad2deg(np.arcsin(self._radius / (self._radius + altitude)))
        self.plot_earth(ra, dec, radius)

    def plot_detector_d(self, quat):
        """Plot detector pointing

        Parameters
        ----------
        quat : (float, float, float, float)
            quaternion of detector
        """
        Q = Quaternion(quat)
        dire = Q.rotate(self._normal)
        ra, dec = xyz_to_radec(dire)
        self._ax.plot(
            -np.deg2rad(ra - 180), np.deg2rad(dec), "p", color="red", markersize=10
        )
        self.plot_detector(ra, dec, "10", radius=10)
        self.plot_detector(ra, dec, "30", radius=30)
        self.plot_detector(ra, dec, "60", radius=60)

    def plot_source(self, ra, dec, error, color="purple"):
        """Plot the direction of the GRB source

        Parameters
        ----------
        ra : float
            right ascension (degree)
        dec : float
            declination (degree)
        error : float
            error with a confidence of 1 sigma
        color : str
            color
        """
        self._ax.plot(
            -np.deg2rad(ra - 180), np.deg2rad(dec), "*", color="red", markersize=10
        )
        self.plot_detector(ra, dec, "source", radius=error, color=color)
        # gauss_map = HealPix.from_gaussian(ra, dec, error)
        # self.add_healpix(gauss_map)

    def save(self, title, path):
        self._ax.set_title(title)
        self._figure.savefig(path)
