import numpy as np
from matplotlib import pyplot as plt


class Significance(object):
    """
    https://iopscience.iop.org/article/10.3847/1538-4365/aab780/meta#apjsaab780s3-4
    """

    def __init__(self):
        pass

    def __sgn(self, x):
        return -1 if x < 0 else 1

    def __maximum_B(self, n, b, sigma):
        B = b**2 - 2 * b * sigma**2 + 4 * n * sigma**2 + sigma**4
        return (b - sigma**2 + np.sqrt(B)) / 2

    def __call__(self, n, b, sigma):
        B = self.__maximum_B(n, b, sigma)
        S = n * np.log(n / B) + (b - B) ** 2 / (2 * sigma**2) + B - n
        return self.__sgn(n - b) * np.sqrt(2 * S)


def binary_search(data, t):
    l, r = 0, len(data) - 1
    res = r
    while l <= r:
        mid = (l + r) // 2
        if data[mid] >= t:
            r, res = mid - 1, mid
        else:
            l = mid + 1

    if data[res] >= t:
        return res
    return len(data)


def latex_string(command: list[str]):
    fig = plt.figure(figsize=(0.1, 0.1))

    n = len(command)
    ax = fig.add_subplot(1, 1, 1)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)

    for k in range(n):
        ax.text(0, -5 * k, command[k], fontsize=20)

    plt.show()


def T90_string(yp, ypn, ypp):
    def get_rs(data):
        sum_ = 0
        for d in data:
            sum_ += d**2
        return np.sqrt(d)

    t_fmt = "{:>5.2f}^{{+{:>5.2f}}}_{{-{:>5.2f}}}"
    s_total = t_fmt.format(yp[1] - yp[0], get_rs(ypn - yp), get_rs(ypp - yp))
    s_start = t_fmt.format(yp[0], ypn[0] - yp[0], abs(ypp[0] - yp[0]))
    s_end = t_fmt.format(yp[1], ypn[1] - yp[1], abs(ypp[1] - yp[1]))
    return "$T_{90}\ =\ " + s_total + "\ from\ " + s_start + "\ to\ " + s_end + "$"
