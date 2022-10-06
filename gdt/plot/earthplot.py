import os
import numpy as np
from gbm.plot import EarthPlot
from gbm.plot.gbmplot import EarthLine
from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter

from ..utils import HIA
from .. import data_path


def format_func(x, pos):
    return r"$10^{:.0f}$".format(x)


class EarthPlotGRID(EarthPlot):
    """Draw map

    Paramaters
    ----------
    id : str, optional
        id of satellite
    hia : bool, optional
        whether to draw high ion area
    lat_range/lon_range : tuple, optional
        range of latitude/longitude on the map
    """

    def __init__(
        self,
        id="G02",
        hia=True,
        lat_range=(-90, 90),
        lon_range=(-180.0, 180.0),
        **kwargs
    ):
        super().__init__(
            lat_range=lat_range,
            lon_range=lon_range,
            saa=False,
            mcilwain=False,
            **kwargs
        )
        if hia:
            coord_path = os.path.join(data_path, id, "coord.txt")
            flux_path = os.path.join(data_path, id, "flux.txt")
            self._hia = HIA(coord_path, flux_path)

    def plot_orbit(self, lon, lat, dire=True):
        """Plot orbit

        Parameters
        ----------
        lon/lat : array(float)
            longitude or latitude of detector
        dire: bool, optional
            if true, draw points to indicate direction, from red to blue, default true.
        """
        self._orbit = EarthLine(
            lat, lon, self._m, self._ax, color="black", alpha=0.4, lw=5.0
        )
        self._orbit.show()

        if dire:
            len_ = len(lat)
            arrow_ind = [int(len_ / 4), int(len_ * 3 / 4)]
            for ind in arrow_ind:
                self._ax.arrow(
                    x=lon[ind],
                    y=lat[ind],
                    dx=lon[ind + int(len_ / 50)] - lon[ind],
                    dy=lat[ind + int(len_ / 50)] - lat[ind],
                    head_width=10.0,
                    width=0.1,
                    head_length=5,
                    overhang=0.5,
                    fc="lightskyblue",
                    ec="magenta",
                )

    def plot_hia_orbit(self, lon, lat, color="blue"):
        """Plot hia orbit

        Parameters
        ----------
        lon/lat : array(float)
            longitude or latitude of detector
        color: string, optional
            color of orbit, default black.
        """
        self._hia_orbit = EarthLine(
            lat, lon, self._m, self._ax, color=color, alpha=0.6, lw=5.0
        )
        self._hia_orbit.show()

    def plot_high_ion_area(self, nx=720, ny=360):
        """Plot high ion area

        Parameters
        ----------
        nx/ny: int, optional
            grid number of longitude/latitude
        """
        grid_lon = np.linspace(-180, 180, nx)
        grid_lat = np.linspace(-90, 90, ny)
        grid_lon, grid_lat = np.meshgrid(grid_lon, grid_lat)

        flux = np.log10(self._hia.mapping(grid_lat, grid_lon).reshape(grid_lon.shape))
        cs = self._ax.contourf(grid_lon, grid_lat, flux, cmap=plt.cm.RdBu_r)
        cbar = self._figure.colorbar(
            cs, ax=self._ax, label=r"Flux($cm^{-2}s^{-1}$)", orientation="vertical"
        )
        cbar.formatter = FuncFormatter(format_func)
        cbar.update_ticks()
        cbar.draw_all()

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
        return self._hia.indmapping(lat, lon)

    def save(self, title, path):
        self._ax.set_title(title)
        self._figure.savefig(path)
