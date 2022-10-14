import numpy as np
from matplotlib.path import Path
from matplotlib.patches import PathPatch

from gbm.plot.gbmplot import EarthPoints


class GRIDIcon(EarthPoints):
    """Plot a Fermi icon on the Earth.

    Parameters:
        lat (np.array): The latitude value
        lon (np.array): The longitude value
        m (:class:`mpl_toolkits.basemap.Basemap`):
            The basemap reference
        ax (:class:`matplotlib.axes`): The axis on which to plot
        alpha (float, optional): The alpha opacity of the line
        **kwargs: Other plotting options

    Attributes:
        alpha (float): The alpha opacity value.
        coordinates (list of str): The formatted coordinate list of the points
        visible (bool): True if the element is shown on the plot,
                        False otherwise
    """

    def __init__(self, lat, lon, m, ax, color=None, alpha=None, **kwargs):
        self._norm_width = 31.4 * 2.0
        self._norm_height = 7.0 * 2.0
        super().__init__(lat, lon, m, ax, color=None, alpha=alpha, **kwargs)

    @property
    def lat(self):
        return self._normalize(self._lat())

    @property
    def gbm_side(self):
        return self._normalize(self._gbm_side())

    @property
    def left_panel(self):
        return self._normalize(self._left_panel())

    @property
    def right_panel(self):
        return self._normalize(self._right_panel())

    @property
    def antenna(self):
        return self._normalize(self._antenna())

    def _create(self, lat, lon, m, ax):
        lon[(lon > 180.0)] -= 360.0
        x, y = m(lon, lat)
        z = 10
        factor = 100.0
        fermilat = self.lat * factor
        fermilat[:, 0] += x
        fermilat[:, 1] += y
        path1 = Path(fermilat, closed=True)
        patch1 = PathPatch(path1, facecolor="#DCDCDC", zorder=z)
        ax.add_patch(patch1)

        gbm = self.gbm_side * factor
        gbm[:, 0] += x
        gbm[:, 1] += y
        path2 = Path(gbm, closed=True)
        patch2 = PathPatch(path2, facecolor="#B79241", zorder=z)
        ax.add_patch(patch2)

        panel = self.left_panel * factor
        panel[:, 0] += x
        panel[:, 1] += y
        path3 = Path(panel, closed=True)
        patch3 = PathPatch(path3, facecolor="#45597C", zorder=z)
        ax.add_patch(patch3)

        panel = self.right_panel * factor
        panel[:, 0] += x
        panel[:, 1] += y
        path4 = Path(panel, closed=True)
        patch4 = PathPatch(path4, facecolor="#45597C", zorder=z)
        ax.add_patch(patch4)

        antenna = self.antenna * factor
        antenna[:, 0] += x
        antenna[:, 1] += y
        path5 = Path(antenna, closed=True)
        patch5 = PathPatch(path5, facecolor="#546165", zorder=z)
        ax.add_patch(patch5)

        return [patch1, patch2, patch3, patch4, patch5]

    def _normalize(self, pts):
        return pts / self._norm_width

    def _lat(self):
        pts = [[-2.5, 3.5], [-2.5, 1.2], [2.5, 1.2], [2.5, 3.5], [-2.5, 3.5]]
        pts = np.array(pts)
        return pts

    def _gbm_side(self):
        pts = [[-2.5, 1.2], [-2.5, -2.1], [2.5, -2.1], [2.5, 1.2], [-2.5, 1.2]]
        pts = np.array(pts)
        return pts

    def _left_panel(self):
        pts = [
            [-2.5, 0.5],
            [-4.5, -1],
            [-9.0, -1],
            [-9.0, 2.0],
            [-4.5, 2.0],
            [-2.5, 0.5],
        ]
        pts = np.array(pts)
        return pts

    def _right_panel(self):
        pts = [[2.5, 0.5], [4.5, -1], [9.0, -1], [9.0, 2.0], [4.5, 2.0], [2.5, 0.5]]
        pts = np.array(pts)
        return pts

    def _antenna(self):
        pts = [[0.5, -2.1], [0.5, -3.5], [1.5, -3.5], [1.5, -2.1], [0.5, -2.1]]
        pts = np.array(pts)
        return pts
