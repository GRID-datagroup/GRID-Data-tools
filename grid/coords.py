from astropy import coordinates


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
