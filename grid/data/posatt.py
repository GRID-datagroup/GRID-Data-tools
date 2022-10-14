import os
import numpy as np
from astropy.io import fits
from pyquaternion import Quaternion
from scipy.interpolate import interp1d

from gbm import coords
from gbm.data import PosHist
from gbm.coords import geocenter_in_radec

from .. import data_path
from ..utils import HIA
from ..detector import Detector
from ..coords import xyz_to_radec


class PosAtt(PosHist):
    def __init__(self, d: Detector):
        """PosAtt object

        Parameters
        ----------
        detector: :class:`~grid.detector.Detector`
            detector to plot the pointing on the sky
        """
        super().__init__()

        coord_path = os.path.join(data_path, d.id, "coord.txt")
        flux_path = os.path.join(data_path, d.id, "flux.txt")

        self._detector = d
        self._hia = HIA(coord_path, flux_path)

    @property
    def detector(self):
        return self._detector

    def detector_pointing(self, times):
        """Retrieve the pointing of a detector in equatorial coordinates

        Parameters
        ----------
        times: float or np.array
            Time(s) in MET

        Returns
        -------
        : np.array, np.array
            The RA, Dec of the detector pointing
        """
        quat = Quaternion(self.get_quaternions(times))
        dire = quat.rotate(self._detector.normal)
        ra, dec = xyz_to_radec(dire)
        return ra, dec

    @classmethod
    def open(cls, filename: str, d: Detector):
        """Open and read a position history file

        Parameters
        ----------
        filename: str
            The filename of the FITS file
        detector: :class:`~grid.detector.Detector`
            detector to plot the pointing on the sky

        Returns
        -------
        : :class:`PosAtt`
            The PosAtt object
        """
        obj = cls(d)
        obj._file_properties(filename)
        # open FITS file
        with fits.open(filename) as hdulist:
            for hdu in hdulist:
                obj._headers.update({hdu.name: hdu.header})
            data = hdulist["ORBIT_ATTITUDE"].data

        times = data["TIME"]
        obj._times = times
        obj._data = data

        # set the interpolators
        obj._set_interpolators()

        return obj

    def _set_interpolators(self):
        data = self._data
        times = self._times

        # Earth inertial coordinates interpolator
        eic = np.array((data["X_J2000"], data["Y_J2000"], data["Z_J2000"]))
        self._eic_interp = interp1d(times, eic)

        # quaternions interpolator
        quat = np.array((data["Q1"], data["Q2"], data["Q3"], data["Q4"]))
        self._quat_interp = interp1d(times, quat)

        # Orbital position interpolator
        # mark TODO: poshist uses the "simple" version of lat/lon calc

        self._lat_interp = interp1d(times, data["Latitude"])
        self._lon_interp = interp1d(times, data["Longitude"])
        self._alt_interp = interp1d(times, data["Altitude"])

        # Earth radius and geocenter interpolators
        self._earth_radius_interp = interp1d(
            times, self._geo_half_angle(data["Altitude"])
        )
        self._geocenter_interp = interp1d(times, coords.geocenter_in_radec(eic))

        # Angular velocity interpolator
        angvel = np.array((data["wx"], data["wy"], data["wz"]))
        self._angvel_interp = interp1d(times, angvel)

        # velocity and angular velocity interpolators
        vel = self._velocity_from_scpos(times, eic)
        self._vel_interp = interp1d(times, vel, fill_value="extrapolate")

        # sun visibility
        sun_visible = self._sun_visible_from_times(times)
        self._sun_interp = interp1d(times, sun_visible, fill_value="extrapolate")
        self._sun_occulted = self._split_bool_mask(sun_visible, times)

        # Interpolators for sun visibility and SAA passage
        in_saa = self._hia.in_hia(data["Longitude"], data["Latitude"])
        self._saa_interp = interp1d(times, in_saa)

        # set GTI based on SAA passages
        self._gti = self._split_bool_mask(in_saa, times)
