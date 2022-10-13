import numpy as np
from astropy.io import fits


def read_evt_fits(fits_file, E_bound=(30, 2000)):
    hdul = fits.open(fits_file)

    EBOUNDS = hdul[1].data
    EVENTS_0 = hdul[3].data
    EVENTS_1 = hdul[4].data
    EVENTS_2 = hdul[5].data
    EVENTS_3 = hdul[6].data

    evt_t_0, evt_E_0 = EVENTS_0["TIME"], EVENTS_0["PI"]
    evt_t_1, evt_E_1 = EVENTS_1["TIME"], EVENTS_1["PI"]
    evt_t_2, evt_E_2 = EVENTS_2["TIME"], EVENTS_2["PI"]
    evt_t_3, evt_E_3 = EVENTS_3["TIME"], EVENTS_3["PI"]
    channel, E_min, E_max = EBOUNDS["CHANNEL"], EBOUNDS["E_MAX"], EBOUNDS["E_MIN"]

    events = np.hstack([evt_t_0, evt_t_1, evt_t_2, evt_t_3])
    ebounds = np.hstack([evt_E_0, evt_E_1, evt_E_2, evt_E_3])

    cid_lower = channel[np.where(E_min >= E_bound[0])[0][0]]
    cid_upper = channel[np.where(E_max <= E_bound[1])[0][-1]]
    events = events[(ebounds > cid_lower) & (ebounds < cid_upper)]
    ebounds = ebounds[(ebounds > cid_lower) & (ebounds < cid_upper)]

    return events, ebounds
