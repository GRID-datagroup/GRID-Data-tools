import os
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter

from gbm.plot import EarthPlot
from gbm.plot.gbmplot import EarthLine

from ..utils import HIA
from .. import data_path
from ..data import PosAtt
from ..icon import GRIDIcon


def format_func(x, pos):
    return r"$10^{:.0f}$".format(x)


class EarthPlotGRID(EarthPlot):
    """Draw map

    Paramaters
    ----------
    lat_range/lon_range : tuple, optional
        range of latitude/longitude on the map
    """

    def __init__(self, lat_range=(-90, 90), lon_range=(-180.0, 180.0), **kwargs):
        super().__init__(
            lat_range=lat_range,
            lon_range=lon_range,
            saa=False,
            mcilwain=False,
            **kwargs
        )

    def add_poshist(
        self,
        data: PosAtt,
        time_range=None,
        trigtime=None,
        numpts=1000,
        hia=True,
        nx=720,
        ny=360,
    ):
        """Add a Position History to plot the orbital path
        of Fermi and optional the position of Fermi at a particular time.

        Parameters
        ----------
        data: :class:`~grid.data.PosAtt`
            A Position History fits file
        time_range: (float, float), optional
            The time range over which to plot the orbit. If omitted, plots the orbit over the entire time range of the file.
        trigtime: float, optional
            If data is PosHist, set trigtime to a particular time of interest to plot Fermi's orbital location. The Trigdat trigger time overrides this.
        numpts: int, optional
            The number of interpolation points for plotting the orbit. Default is 1000.
        hia : bool, optional
            whether to draw high ion area
        nx/ny: int, optional
            grid number of longitude/latitude
        """
        if time_range is None:
            time_range = data.time_range

        # get latitude and longitude over the time range and produce the orbit
        times = np.linspace(*time_range, numpts)
        lat = data.get_latitude(times)
        lon = data.get_longitude(times)
        self._orbit = EarthLine(
            lat, lon, self._m, self._ax, color="black", alpha=0.4, lw=5.0
        )
        self._orbit.show()

        arrow_ind = [int(len(lat) / 4), int(len(lat) * 3 / 4)]
        for ind in arrow_ind:
            self._ax.arrow(
                x=lon[ind],
                y=lat[ind],
                dx=lon[ind + int(len(lat) / 50)] - lon[ind],
                dy=lat[ind + int(len(lat) / 50)] - lat[ind],
                head_width=10.0,
                width=0.1,
                head_length=5,
                overhang=0.5,
                fc="lightskyblue",
                ec="magenta",
            )

        # if trigtime is set or Trigdat, produce Fermi location
        if hasattr(data, "trigtime"):
            trigtime = data.trigtime
        if trigtime is not None:
            lat = data.get_latitude(trigtime)
            lon = data.get_longitude(trigtime)
            self._fermi = GRIDIcon(lat, lon, self._m, self._ax)

        if hia:
            coord_path = os.path.join(data_path, data.detector.id, "coord.txt")
            flux_path = os.path.join(data_path, data.detector.id, "flux.txt")
            self._hia = HIA(coord_path, flux_path)
            self._plot_hia(nx, ny)

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
        times = np.linspace(*data.time_range, numpts)
        lat = data.get_latitude(times)
        lon = data.get_longitude(times)

        self._extra_orbit = EarthLine(
            lat, lon, self._m, self._ax, color=color, alpha=0.6, lw=5.0
        )
        self._extra_orbit.show()

    def _plot_hia(self, nx=720, ny=360):
        """Plot high ion area

        Parameters
        ----------
        nx/ny: int, optional
            grid number of longitude/latitude
        """
        np.seterr(divide="ignore")

        grid_lon = np.linspace(-180, 180, nx)
        grid_lat = np.linspace(-90, 90, ny)
        grid_lon, grid_lat = np.meshgrid(grid_lon, grid_lat)

        flux = self._hia.flux(grid_lat, grid_lon)
        flux = np.log10(flux)
        cs = self._ax.contourf(grid_lon, grid_lat, flux, cmap=plt.cm.RdBu_r)
        cbar = self._figure.colorbar(
            cs, ax=self._ax, label=r"Flux($cm^{-2}s^{-1}$)", orientation="vertical"
        )
        cbar.formatter = FuncFormatter(format_func)
        cbar.update_ticks()
        cbar.draw_all()

    def save(self, title, path):
        self._ax.set_title(title)
        self._figure.savefig(path)
