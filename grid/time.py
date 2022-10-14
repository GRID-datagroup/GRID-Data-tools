import warnings
from astropy.time import Time
from astropy.time.formats import TimeFromEpoch

from gbm.time import Met


class TimeGRIDSec(TimeFromEpoch):
    """Represents the number of seconds elapsed since Jan 1, 2018 00:00:00 UTC including leap seconds"""

    name = "grid"
    unit = 1.0 / 86400  # in days (1 day == 86400 seconds)
    epoch_val = "2018-01-01 00:00:00.000"
    epoch_val2 = None
    epoch_scale = "tt"  # Scale for epoch_val class attribute
    epoch_format = "iso"  # Format for epoch_val class attribute


class MetGRID(Met):
    def __init__(self, secs):
        """Creates a Met object with the time set to the number of seconds since Jan 1, 2018 00:00:00 UTC including the leap seconds"""
        if secs < 0:
            warnings.warn("Time before GRID mission epoch")
        self.__time = Time(secs, format="grid")

    @property
    def met(self):
        return self.__time.grid
