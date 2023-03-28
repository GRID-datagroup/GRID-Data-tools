import warnings
import datetime
from datetime import timezone
from astropy.time import Time
from astropy.time.formats import TimeFromEpoch

from gbm.time import Met

#: GRID-01 launch date 2018-10-29
#: GRID-01 入轨时间 2018-10-29
DT_LAUNCH_REAL = datetime.datetime(2018, 10, 29, tzinfo=timezone.utc)

#: GRID MET date 2018-01-01T00:00:00, UTC+0
#: GRID 项目参考时间 2018-01-01T00:00:00, UTC+0
DT_MET = datetime.datetime(2018, 1, 1, tzinfo=timezone.utc)

#: GRID-01 MET date Unix timestamp
#: GRID-01 项目参考时间 Unix 时间戳
UTC_MET = DT_MET.timestamp()
assert UTC_MET == 1514764800, "Error in utc of the lauch date"

#: timedelta 8 hours
#: 8小时时间差
TZ_UTC_8 = timezone(datetime.timedelta(hours=8))


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


def utc_to_days(time_u):
    """
    Convert UTC time to days from ``UTC_MET`` in UTC+0
    将 **UTC+0** 时间戳转化为GRID自项目参考时间 ``UTC_MET`` 起的天数

    Parameters
    ----------
    time_u : float
        UTC timestamp in UTC+0
        **UTC+0** 时间戳

    Returns
    -------
    days_i : int
        number of days since MET in UTC+0, int
        自GRID-01自项目参考时间 ``UTC_MET`` 起的天数
    date_str : str
        date str in UTC+0, example: 181029
        自GRID-01自项目参考时间 ``UTC_MET`` 起的格式化天数字符串 ``yymmdd``
    """
    # the 0th day is 2018.10.29 00:00 (1540771200) - 2018.10.30 00:00 in UTC+0
    days_i = int((time_u - UTC_MET) // (24 * 60 * 60))
    dt_time_u = datetime.datetime.utcfromtimestamp(time_u)
    date_str = dt_time_u.strftime("%y%m%d")  # time in string format

    return days_i, date_str


def utc_to_str(time_u):
    """
    Convert utc time to string
    将 **UTC+0** 时间戳转化为字符串

    Parameters
    ----------
    time_u : float
        UTC timestamp in UTC+0
        **UTC+0** 时间戳

    Returns
    -------
    str_u : str
        time str in UTC+0 with accuracy of seconds
        格式化的时间字符串 ``yymmddHHMMSS``
    """
    time_u_0 = datetime.datetime.utcfromtimestamp(time_u)
    str_u = time_u_0.strftime("%y%m%d%H%M%S")  # 12 characters
    return str_u


def days_to_date(days):
    """
    Output the date of number of days after MET
    由 GRID MET后的天数输出格式化的日期

    Parameters
    ----------
    days : int
        number of days in UTC+0 after MET
        GRID MET后的天数任务起始后的天数

    Returns
    -------
    date_str : str
        formatted date string
        格式化的日期, ``yymmdd``
    """
    time_d_s = days * 24 * 60 * 60
    time_date = datetime.datetime.utcfromtimestamp(UTC_MET + time_d_s)
    date_str = time_date.strftime("%y%m%d")
    return date_str


def date_to_days(date_str):
    """
    Output the number of days after MET of given date
    由格式化的日期, 输出 GRID MET 后的天数

    Parameters
    ----------
    date_str : str
        formatted date in UTC+0 string
        格式化的日期, ``yymmdd``

    Returns
    -------
    days : int
        number of days in UTC+0 after MET
        GRID MET 后的天数, 任务起始后的天数
    """
    dt = datetime.datetime(
        int("20" + date_str[0:2]),
        int(date_str[2:4]),
        int(date_str[4:6]),
        tzinfo=timezone.utc,
    )
    utc = dt.timestamp()

    days, _ = utc_to_days(utc)
    return days


def cn2en_time(s):
    """
    convert time in Chinese to time in isot format
    将中文表达的时间转换为isot格式

    Parameters
    ----------
    s : array
        time in Chinese
        中文时间（****年**月**日**时**分**秒）

    Returns
    -------
    s1 : array
        time in isot format
        isot格式时间
    """
    # year   month  day    hour   minute  second
    # \u5e74 \u6708 \u65e5 \u65f6 \u5206 \u79d2
    s1 = []
    for s0 in s:
        s0 = s0.replace("\u5e74", "-")
        s0 = s0.replace("\u6708", "-")
        s0 = s0.replace("\u65e5", "T")
        s0 = s0.replace("\u65f6", ":")
        s0 = s0.replace("\u5206", ":")
        s0 = s0.replace("\u79d2", "")
        s1.append(s0.strip())
    return s1
