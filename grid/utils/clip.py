import numpy as np


class SigmaClip:
    """Perform sigma-clipping on the provided data
    对数据进行`sigma clip`

    Parameters
    ----------
    model : str, optional
        The model to sigma clip, default 'single'.
        If 'single', all the data will share the mean and standard deviation.
        If 'array', each data will use it's own mean and standard deviation by calculating baseline.

    type_ : str, optional
        type of sigma clip, default 'bilateral'.
        if 'bilateral', upper and lower bound will be calculate.
        if 'upper' or 'lower', only compute upper or lower bound.

    sigma: float, optional
        The number of standard deviations to use for both the lower and upper clipping limit.

    maxiters: int or None, optional
        The maximum number of sigma-clipping iterations to perform or None to clip until convergence is achieved.
        If convergence is achieved prior to maxiters iterations, the clipping iterations will stop.

    cenfunc: callable(), optional
        The statistic or callable function/object used to compute the center value for the clipping.

    stdfunc: callable(), optional
        The statistic or callable function/object used to compute the standard deviation about the center value.

    Method
    ----------
    _compute_bounds :
        Compute the upper and lower bounds
    __call__ :
        real function
    """

    def __init__(
        self,
        model="single",
        type_="bilateral",
        sigma=3.0,
        maxiters=5,
        cenfunc=np.mean,
        stdfunc=np.std,
    ):
        self.model = model
        self.type_ = type_
        self.sigma = sigma
        self.maxiters = maxiters or np.inf
        self.cenfunc = cenfunc
        self.stdfunc = stdfunc
        self._min_value = np.nan
        self._max_value = np.nan

    def _compute_bounds(self, data):
        """Compute the upper and lower bounds
        计算上下界

        Parameters
        ----------
        data : array_like
            The data to be sigma clipped.
            被裁减的数据
        """
        mean_value = self.cenfunc(data)
        std = self.stdfunc(data)
        if self.type_ == "bilateral":
            self._min_value = mean_value - (std * self.sigma)
            self._max_value = mean_value + (std * self.sigma)
        elif self.type_ == "upper":
            self._min_value = np.full(mean_value.shape, -np.inf)
            self._max_value = mean_value + (std * self.sigma)
        else:
            self._min_value = mean_value - (std * self.sigma)
            self._max_value = np.full(mean_value.shape, np.inf)

    def __call__(
        self, data, baseline=None, masked=True, return_bounds=False, copy=True
    ):
        """
        Perform sigma-clipping on the provided data
        进行`Sigma-clip`

        Parameters
        ----------
        data : array_like
            The data to be sigma clipped
            被裁减的数据

        baseline: array_like or None, optional
            Reference baseline
            参考的基线

        masked: bool, optional
            If True, then a MaskedArray is returned, where the mask is True for clipped values.
            If False, then a ndarray and the minimum and maximum clipping thresholds are returned.
            The default is True.

        return_bounds: bool, optional
            If True, then the minimum and maximum clipping bounds are also returned.

        copy: bool, optional
            If True, then the data array will be copied.
            If False and masked=True, then the returned masked array data will contain the same array as the input data
            If False and masked=False, the input data is modified in-place.
            The default is True.
        """
        data = np.asanyarray(data)
        filtered_data = data.ravel()

        # remove masked values and convert to ndarray
        if isinstance(filtered_data, np.ma.MaskedArray):
            filtered_data = filtered_data.data[~filtered_data.mask]

        # remove invalid values
        good_mask = np.isfinite(filtered_data)
        if np.any(~good_mask):
            filtered_data = filtered_data[good_mask]

        nchanged = 1
        iteration = 0

        while nchanged != 0 and (iteration < self.maxiters):
            iteration += 1
            size = filtered_data.size
            if self.model == "single":
                self._compute_bounds(filtered_data)
                filtered_data = filtered_data[
                    (filtered_data >= self._min_value)
                    & (filtered_data <= self._max_value)
                ]
                nchanged = size - filtered_data.size
            if self.model == "array":
                self._compute_bounds(baseline)
                idx = np.where(
                    ~(
                        (filtered_data >= self._min_value)
                        & (filtered_data <= self._max_value)
                    )
                    & (filtered_data > 0)
                )[0]
                filtered_data[idx] = np.full(len(idx), 0)
                baseline[idx] = np.full(len(idx), 0)
                nchanged = len(idx)

        if masked:
            # return a masked array and optional bounds
            filtered_data = np.ma.masked_invalid(data, copy=copy)
            if self.model == "array":
                self._min_value = np.ma.masked_invalid(self._min_value, copy=copy)
                self._max_value = np.ma.masked_invalid(self._max_value, copy=copy)

            # update the mask in place, ignoring RuntimeWarnings for
            # comparisons with NaN data values
            with np.errstate(invalid="ignore"):
                if self.model == "array":
                    self._min_value.mask |= (
                        (data < self._min_value)
                        | (data > self._max_value)
                        | (filtered_data == 0)
                    )
                    self._max_value.mask |= (
                        (data < self._min_value)
                        | (data > self._max_value)
                        | (filtered_data == 0)
                    )
            filtered_data.mask |= (
                (data < self._min_value)
                | (data > self._max_value)
                | (filtered_data == 0)
            )

        if return_bounds:
            return filtered_data, self._min_value, self._max_value
        else:
            return filtered_data
