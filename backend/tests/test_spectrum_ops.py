from app.services.spectrum_ops import minmax_normalize, swir_subset


def test_swir_subset():
    w, v = swir_subset([800, 900, 1100, 2600], [1, 2, 3, 4], 900, 2500)
    assert w == [900, 1100]
    assert v == [2, 3]


def test_minmax_normalize():
    out = minmax_normalize([2, 4, 6])
    assert out == [0.0, 0.5, 1.0]
