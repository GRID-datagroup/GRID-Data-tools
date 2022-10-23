import numpy as np
from astropy.io import fits

from gbm.data import TTE, Cspec
from gbm.data import headers as hdr
from gbm.data.primitives import EventList

from ..detector import Detector


class Evt(TTE):
    def __init__(self, d: Detector):
        """Evt object

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

    @property
    def energy_range(self):
        data = self._data
        if data.size > 0:
            emin = data._ebounds[data.pha.min() - 1]['E_MIN']
            emax = data._ebounds[data.pha.max() - 1]['E_MAX']
            return (emin, emax)

    @classmethod
    def from_data(
        cls,
        data,
        detector,
        gti=None,
        trigtime=0.0,
        object=None,
        ra_obj=None,
        dec_obj=None,
        err_rad=None,
    ):
        """Create a Evt object from an EventList data object.

        Parameters
        ----------
        data: :class:`~.primitives.EventList`
            The event data
        detector: :class:`~grid.detector.Detector`
            detector to plot the pointing on the sky
        gti: [(float, float), ...], optional
            The list of tuples representing the good time intervals (start, stop). If omitted, the GTI is assumed to be [(tstart, tstop)].
        trigtime: float, optional:
            The trigger time, if applicable. If provided, the data times will be shifted relative to the trigger time.
        object: str, optional
            The object being observed
        ra_obj: float, optional
            The RA of the object
        dec_obj: float, optional
            The Dec of the object
        err_rad: float, optional
            The localization error radius of the object

        Returns
        -------
        : :class:`Evt`
            The newly created Evt object
        """
        obj = cls(detector)
        filetype = "GBM PHOTON LIST"
        obj._data = data
        detchans = data.numchans
        tstart, tstop = data.time_range

        try:
            trigtime = float(trigtime)
        except:
            raise TypeError("trigtime must be a float")

        if trigtime < 0.0:
            raise ValueError("trigtime must be non-negative")

        obj._trigtime = trigtime
        tstart += trigtime
        tstop += trigtime

        detector = None if detector == "" else detector
        object = None if object == "" else object
        ra_obj = None if ra_obj == "" else ra_obj
        dec_obj = None if dec_obj == "" else dec_obj
        err_rad = None if err_rad == "" else err_rad

        # create the primary extension
        primary_header = hdr.primary(
            detnam=detector,
            filetype=filetype,
            tstart=tstart,
            tstop=tstop,
            trigtime=trigtime,
            object=object,
            ra_obj=ra_obj,
            dec_obj=dec_obj,
            err_rad=err_rad,
        )
        headers = [primary_header]
        header_names = ["PRIMARY"]

        # ebounds extension
        ebounds_header = hdr.ebounds(
            detnam=detector,
            tstart=tstart,
            tstop=tstop,
            trigtime=trigtime,
            object=object,
            ra_obj=ra_obj,
            dec_obj=dec_obj,
            err_rad=err_rad,
            detchans=detchans,
        )
        headers.append(ebounds_header)
        header_names.append("EBOUNDS")

        # spectrum extension
        events_header = hdr.events(
            detnam=detector,
            tstart=tstart,
            tstop=tstop,
            trigtime=trigtime,
            object=object,
            ra_obj=ra_obj,
            dec_obj=dec_obj,
            err_rad=err_rad,
            detchans=detchans,
        )
        headers.append(events_header)
        header_names.append("EVENTS")

        # gti extension
        if gti is None:
            gti = [data.time_range]
        ngti = len(gti)
        gti_rec = np.recarray(ngti, dtype=[("START", ">f8"), ("STOP", ">f8")])
        gti_rec["START"] = [one_gti[0] for one_gti in gti]
        gti_rec["STOP"] = [one_gti[1] for one_gti in gti]
        gti_header = hdr.gti(
            detnam=detector,
            tstart=tstart,
            tstop=tstop,
            trigtime=trigtime,
            object=object,
            ra_obj=ra_obj,
            dec_obj=dec_obj,
            err_rad=err_rad,
        )
        headers.append(gti_header)
        header_names.append("GTI")
        obj._gti = gti_rec

        # store headers and set data properties
        obj._headers = {name: header for name, header in zip(header_names, headers)}

        # set file info
        trig = None if obj.trigtime == 0.0 else obj.trigtime
        obj.set_properties(
            detector=detector,
            trigtime=trig,
            tstart=obj.time_range[0],
            datatype="tte",
            extension="fit",
        )
        return obj

    @classmethod
    def open(cls, filename, d: Detector):
        """Open a Evt FITS file and return the Evt object

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
            events = np.array(
                list(zip(events["TIME"], events["PHA"])),
                dtype=[("TIME", ">f8"), ("PHA", ">i2")],
            )

            # Do this for GTI as well
            gti = hdul["GTI"].data
            gti = np.vstack((gti["START"], gti["STOP"])).squeeze().T

            # create the EventList, the core of the Evt class
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
