import numpy as np
from astropy import units as u
from astropy.coordinates import SkyCoord

# WGS84 Earth Radius
# WGS84 模型地球半径
WGS_R = 6378137

# WGS84 Earth Flattening
# WGS84 模型地球扁率
WGS_F = 1 / 298.257223563


def xyz_to_radec(X_t):
    """
    Transform xyz coordinate to Ra & Dec
    笛卡尔坐标系坐标转天球坐标系坐标

    Parameters
    ----------
    X_t : array_like
        xyz coordinate array(unnormalized array) in Cartesian coordinate system
        笛卡尔坐标系中的坐标指向, 未进行归一化

    Returns
    -------
    radec : array_like
        Ra & Dec (array) in Celestial coordinate system
        天球坐标系中的坐标指向, Ra & Dec
    """
    X = SkyCoord(x=X_t[0], y=X_t[1], z=X_t[2], representation_type="cartesian")
    X.representation_type = "unitspherical"
    return (X.ra.degree, X.dec.degree)


def radec_to_xyz(X_t):
    """
    Transform Ra & Dec to xyz coordinate
    天球坐标系坐标转笛卡尔坐标系坐标

    Parameters
    ----------
    X_t : array_like
        Ra & Dec (array) in Celestial coordinate system
        天球坐标系中的坐标指向, Ra & Dec (以deg为单位)

    Returns
    -------
    xyz : array_like
        xyz coordinate array(unnormalized array) in Cartesian coordinate system
        笛卡尔坐标系中的坐标指向, 未进行归一化
    """
    # X_t is 2*n array
    X = SkyCoord(ra=X_t[0, :] * u.rad, dec=X_t[1, :] * u.rad)
    X.representation_type = "cartesian"
    return X.x.value, X.y.value, X.z.value


def WGS84_XYZ_to_BLH(X, Y, Z):
    """
    convert WGS84 X, Y, Z to B, L, H
    将WGS84地球模型大地坐标系的X, Y, Z转化为纬度、经度、高度

    Parameters
    ----------
    X : float
        X坐标(米)
    Y : float
        Y坐标(米)
    Z : float
        Z坐标(米)

    Returns
    -------
    B : float
        latitude(deg)
        纬度(度)
    L : float
        longitude(deg)
        经度(度)
    H : float
        height(m)
        高度(米)
    """
    a = WGS_R
    b = a * (1 - WGS_F)
    esq = (a**2 - b**2) / a**2
    p = np.sqrt(X**2 + Y**2)
    theta = np.arctan(Z * a / (p * b))
    L = np.arctan2(Y, X)
    B = np.arctan(
        (Z + esq / (1 - esq) * b * np.sin(theta) ** 3)
        / (p - esq * a * np.cos(theta) ** 3)
    )
    N = a / np.sqrt(1 - esq * np.sin(B) ** 2)
    H = p / np.cos(B) - N
    return B * 180 / np.pi, L * 180 / np.pi, H


def WGS84_BLH_to_XYZR(B, L, H):
    """
    convert WGS84 B, L, H to X, Y, Z, R
    将WGS84地球模型大地坐标系的纬度、经度、高度转化为X、Y、Z、R

    Parameters
    ----------
    B : float
        latitude(deg)
        纬度(度)
    L : float
        longitude(deg)
        经度(度)
    H : float
        height(m)
        高度(米)

    Returns
    -------
    X : float
        X坐标(米)
    Y : float
        Y坐标(米)
    Z : float
        Z坐标(米)
    R : float
        distance to the center of the earth(m)
        到地心的距离(米)
    """
    a = WGS_R
    b = a * (1 - WGS_F)
    esq = (a**2 - b**2) / a**2

    v = a / np.sqrt(1 - esq * np.sin(B * np.pi / 180) ** 2)

    X = (v + H) * np.cos(B * np.pi / 180) * np.cos(L * np.pi / 180)
    Y = (v + H) * np.cos(B * np.pi / 180) * np.sin(L * np.pi / 180)
    Z = ((1 - esq) * v + H) * np.sin(B * np.pi / 180)
    R = np.sqrt(((v + H) * np.cos(B * np.pi / 180)) ** 2 + Z**2)

    return X, Y, Z, R


def J2000_RaDecR_to_XYZ(Ra, Dec, R):
    """
    convert J2000 Ra, Dec, R to X, Y, Z
    将J2000天球标系的赤经、赤纬、到地心的距离转化为X、Y、Z

    Parameters
    ----------
    Ra : float
        right ascension(deg)
        赤经(度)
    L : float
        declination(deg)
        赤纬(度)
    R : float
        distance from the center of the earth(m)
        到地心的距离(米)

    Returns
    -------
    X : float
        X坐标(米)
    Y : float
        Y坐标(米)
    Z : float
        Z坐标(米)
    """

    X = R * np.cos(Ra * np.pi / 180) * np.cos(Dec * np.pi / 180)
    Y = R * np.sin(Ra * np.pi / 180) * np.cos(Dec * np.pi / 180)
    Z = R * np.sin(Dec * np.pi / 180)

    return X, Y, Z
