import numpy as np
from scipy.signal import savgol_filter


def swir_subset(wavelength_nm: list[float], values: list[float], min_nm: float, max_nm: float):
    pairs = [(w, v) for w, v in zip(wavelength_nm, values) if min_nm <= w <= max_nm]
    if not pairs:
        return [], []
    w, v = zip(*pairs)
    return list(w), list(v)


def minmax_normalize(values: list[float]) -> list[float]:
    if not values:
        return []
    arr = np.array(values)
    denom = arr.max() - arr.min()
    if denom == 0:
        return [0.0 for _ in values]
    return ((arr - arr.min()) / denom).tolist()


def smooth_values(values: list[float], window: int = 9, poly: int = 2) -> list[float]:
    if len(values) < window:
        return values
    return savgol_filter(values, window_length=window, polyorder=poly).tolist()
