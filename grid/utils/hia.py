import numpy as np
from scipy.interpolate import NearestNDInterpolator


class HIA:
    """High Ion Area

    Attributes
    ----------
    _mapping : method
        coordinate - flux function
    _indmapping : method
        Nearest-neighbor interpolation

    Parameters
    ----------
    coord_path : str
        coordinate file path
    flux_path: str
        flux file path
    """

    def __init__(self, coord_path, flux_path):
        """Generate coordinate - flux functions"""
        coord = np.loadtxt(coord_path, comments="'", skiprows=26, delimiter=",")[
            :, 1:3
        ].astype(np.float)
        flux = np.loadtxt(flux_path, comments="'", skiprows=30, delimiter=",")[:, 2]
        flux[flux <= 0] = 0

        ind = np.zeros_like(flux).astype(np.bool)
        ind[flux > 0] = 1

        ind = ind.reshape(90 * 121)
        self._mapping = NearestNDInterpolator(coord, flux)
        self._indmapping = NearestNDInterpolator(coord, ind)

    def flux(self, lat, lon):
        """Get flux
        Parameters
        ----------
        lon/lat : array(float)
            longitude or latitude of detector

        Returns
        -------
         : array
            float array for each point's flux
        """
        return self._mapping(lat, lon)

    def in_hia(self, lon, lat):
        """Check if a point or points is inside the HIA

        Parameters
        ----------
        lon/lat : array(float)
            longitude or latitude of detector

        Returns
        -------
         : array
            Boolean array for each point where True indicates the point is in the HIA.
        """
        return self._indmapping(lat, lon)
