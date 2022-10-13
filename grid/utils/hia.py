import numpy as np
from scipy.interpolate import NearestNDInterpolator


class HIA:
    """High Ion Area

    Parameters
    ----------
    coord_path : str
        coordinate file path
    flux_path: str
        flux file path
    """

    def __init__(self, coord_path, flux_path):
        self.mapping, self.indmapping = self.generate_func(coord_path, flux_path)

    def generate_func(self, coord_path, flux_path):
        """Generate coordinate - flux functions

        Parameters
        ----------
        coord_path : str
            coordinate file path
        flux_path: str
            flux file path

        Returns
        -------
        mapping : object
            coordinate - flux function
            某种坐标 - 粒子通量函数
        indmapping : object
            Nearest-neighbor interpolation
            最近邻插值函数
        """
        coord, flux = self.read_file(coord_path, flux_path)
        ind = np.zeros_like(flux).astype(np.bool)
        ind[flux > 0] = 1

        ind = ind.reshape(90 * 121)
        mapping = NearestNDInterpolator(coord, flux)
        indmapping = NearestNDInterpolator(coord, ind)

        return mapping, indmapping

    def read_file(self, coord_path, flux_path):
        """Read coordinate & flux file

        Parameters
        ----------
        coord_path : str
            coordinate file path
        flux_path: str
            flux file path

        Returns
        -------
        coord : array_like
            coordinate
        flux : array_like
            flux

        """
        coord = np.loadtxt(coord_path, comments="'", skiprows=26, delimiter=",")[
            :, 1:3
        ].astype(np.float)
        flux = np.loadtxt(flux_path, comments="'", skiprows=30, delimiter=",")[:, 2]
        flux[flux <= 0] = 0
        return coord, flux
