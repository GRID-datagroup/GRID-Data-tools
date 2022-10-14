import numpy as np
from astropy.io import fits

from gbm.data import TTE, Cspec
from gbm.data.primitives import EventList

from ..detector import Detector


class Evt(TTE):
    def __init__(self, d: Detector):
        """PosAtt object

        Parameters
        ----------
        detector: :class:`~grid.detector.Detector`
            detector to plot the pointing on the sky
        """
        super().__init__()
        self._detector = d

    @property
    def detector(self):
        return self._detector

    @classmethod
    def open(cls, filename, d: Detector):
        """Open a TTE FITS file and return the TTE object

        Parameters
        ----------
        filename: str
            The filename of the FITS file
        detector: :class:`~grid.detector.Detector`
            detector to plot the pointing on the sky

        Returns
        -------
        : :class:`Evt`
            The Evt object
        """
        obj = cls(d)
        obj._file_properties(filename)

        with fits.open(filename, mmap=False) as hdul:
            for hdu in hdul:
                obj._headers.update({hdu.name: hdu.header})

            obj._headers["PRIMARY"]["TRIGTIME"] = 0.0

            EVENTS0 = hdul["EVENTS0"].data.view(np.recarray)
            EVENTS1 = hdul["EVENTS1"].data.view(np.recarray)
            EVENTS2 = hdul["EVENTS2"].data.view(np.recarray)
            EVENTS3 = hdul["EVENTS3"].data.view(np.recarray)

            ebounds = hdul["EBOUNDS"].data
            events = np.hstack((EVENTS0, EVENTS1, EVENTS2, EVENTS3))
            events.dtype = [
                ("TIME", ">f8"),
                ("PHA", ">i2"),
                ("DEAD_TIME", "u1"),
                ("EVT_TYPE", "u1"),
            ]

            # Do this for GTI as well
            gti = hdul["GTI"].data
            gti = np.vstack((gti["START"], gti["STOP"])).squeeze().T

            # create the EventList, the core of the TTE class
            obj._data = EventList.from_fits_array(events, ebounds)
            obj._gti = gti

        return obj

    def to_phaii(
        self,
        bin_method,
        *args,
        time_range=None,
        energy_range=None,
        channel_range=None,
        **kwargs
    ):
        """Utilizing a binning function, convert the data to a PHAII object

        Parameters
        ----------
        bin_method: <function>
            A binning function
        time_range: [(float, float), ...], optional
            The time range of the spectrum. If omitted, uses the entiretime range of the data.
        energy_range: (float, float), optional
            The energy range of the spectrum. If omitted, uses the entireenergy range of the data.
        channel_range: (int, int), optional
            The channel range of the spectrum. If omitted, uses the entireenergy range of the data.

        Returns
        -------
        : class:`Cspec`
            The PHAII object
        """
        # slice to desired energy or channel range
        if (channel_range is not None) or (energy_range is not None):
            if channel_range is not None:
                self._assert_range(channel_range)
                energy_range = (
                    self._data.emin[channel_range[0]],
                    self._data.emax[channel_range[1]],
                )
            temp = self._data.energy_slice(*self._assert_range(energy_range))
        else:
            temp = self._data

        # do the time binning to create the TimeEnergyBins
        if time_range is None:
            tstart, tstop = None, None
        else:
            tstart, tstop = time_range

        bins = temp.bin(
            bin_method,
            *args,
            tstart=tstart,
            tstop=tstop,
            event_deadtime=self._detector.deadtime,
            **kwargs
        )

        # create the Cspec object
        if "OBJECT" in self.headers["PRIMARY"]:
            obj = self.headers["PRIMARY"]["OBJECT"]
            ra_obj = self.headers["PRIMARY"]["RA_OBJ"]
            dec_obj = self.headers["PRIMARY"]["DEC_OBJ"]
            err_rad = self.headers["PRIMARY"]["ERR_RAD"]
        else:
            obj, ra_obj, dec_obj, err_rad = None, None, None, None

        obj = Cspec.from_data(
            bins,
            gti=self.gti,
            trigtime=self.trigtime,
            detector=self.detector,
            object=obj,
            ra_obj=ra_obj,
            dec_obj=dec_obj,
            err_rad=err_rad,
        )
        return obj
