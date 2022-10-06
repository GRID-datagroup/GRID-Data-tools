import numpy as np
from astropy import coordinates, time


def xyz_to_radec(coord):
    """Transform xyz coordinate to Ra & Dec

    Parameters
    ----------
    coord : (float, float, float)
        coordinate tuple

    Returns
    -------
    anonymous : (float, float)
        Ra & Dec tuple
    """
    X = coordinates.SkyCoord(
        x=coord[0], y=coord[1], z=coord[2], representation_type="cartesian"
    )
    X.representation_type = "unitspherical"
    return (X.ra.degree, X.dec.degree)


def get_sun_pos(utc):
    """Calculate sun location in RA/Dec for a given utc time.

    Parameters
    ----------
    utc : float
        utc time

    Returns
    -------
    anonymous : (float, float)
        RA and Dec of the sun
    """
    utc = time.Time(utc, format="unix").utc
    sun = coordinates.get_sun(utc)
    return sun.ra.degree, sun.dec.degree


def get_geocenter_pos(coord):
    """Calculate the location of the Earth center RA and Dec

    Parameters
    ----------
    coord : (float, float, float)
        coordinate tuple of detector in eic

    Returns
    -------
    anonymous: (float, float)
        RA and Dec of Earth center as viewed in degrees
    """
    if type(coord) != np.ndarray:
        coord = np.array(coord)
    unit_vec = -coord / np.linalg.norm(-coord, axis=0)
    dec = np.pi / 2.0 - np.arccos(unit_vec[2, np.newaxis])
    ra = np.arctan2(unit_vec[1, np.newaxis], unit_vec[0, np.newaxis])
    ra[ra < 0.0] += 2.0 * np.pi
    return np.squeeze(np.rad2deg(ra)), np.squeeze(np.rad2deg(dec))
