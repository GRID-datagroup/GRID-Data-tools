import numpy as np
import pybaselines as pbl
from astropy.io import fits
from matplotlib import pyplot as plt


def quick_light_curve(
    fits_file,
    ax=None,
    E_bound=(30, 2000),
    baseline_func=None,
    draw_baseline=True,
    minus_baseline=False,
):
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
    events = np.sort(events[(ebounds > cid_lower) & (ebounds < cid_upper)])
    ebounds = ebounds[(ebounds > cid_lower) & (ebounds < cid_upper)]

    t_begin = np.min(events)
    t_end = np.max(events)
    t_edge = np.arange(t_begin, np.ceil(t_end) + 1, 1)

    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)

    if baseline_func is None:
        baseline_func = pbl.morphological.mpspline

    if minus_baseline:
        x = (t_edge[1:] + t_edge[:-1]) / 2
        count, _ = np.histogram(events, t_edge)
        baseline = baseline_func(count)[0]
        ax.hist(
            x, bins=t_edge, weights=(count - baseline), histtype="step", label="Pure"
        )
    else:
        ax.hist(events, bins=t_edge, histtype="step", label="Data")
        if draw_baseline:
            x = (t_edge[1:] + t_edge[:-1]) / 2
            count, _ = np.histogram(events, t_edge)
            baseline = baseline_func(count)[0]
            ax.hist(x, bins=t_edge, weights=baseline, histtype="step", label="baseline")

    ax.legend()
