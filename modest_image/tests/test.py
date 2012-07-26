import pytest

from matplotlib import pyplot as plt
import matplotlib.image as mi

import numpy as np

from modest_image import ModestImage

x, y = np.mgrid[0:300, 0:300]
_data = np.sin(x / 10.) * np.cos(y / 30.)

def setup_function(func):
    plt.clf()
    plt.cla()

def default_data():
    return _data

def init(img_cls, data):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    artist = img_cls(ax, data=data)
    ax.add_artist(artist)
    ax.set_aspect('equal')
    artist.norm.vmin = -1
    artist.norm.vmax = 1
    ax.set_xlim(0, data.shape[1])
    ax.set_ylim(0, data.shape[0])

    return artist

def check(label, modest, axes):
    """ Assert that images are identical, else save and fail """
    modest.figure.canvas.draw()
    axes.figure.canvas.draw()
    str1 = modest.figure.canvas.tostring_rgb()
    str2 = axes.figure.canvas.tostring_rgb()

    if str1 == str2:
        return

    result = 'PASS' if str1 == str2 else 'FAIL'
    modest_label = 'test_%s_modest' % label
    axes_label = 'test_%s_default' % label

    modest.axes.set_title(modest_label + " " + result)
    axes.axes.set_title(axes_label + " " + result)

    axes.figure.canvas.draw()
    modest.figure.canvas.draw()

    modest.figure.savefig(modest_label+'.pdf')
    axes.figure.savefig(axes_label+'.pdf')

    assert str1 == str2

def test_default():
    """ Zoomed out view """
    data = default_data()
    modest = init(ModestImage, data)
    axim = init(mi.AxesImage, data)
    check('default', modest.axes, axim.axes)

def test_move():
    """ move at default zoom """
    data = default_data()
    modest = init(ModestImage, data)
    axim = init(mi.AxesImage, data)
    xlim = modest.axes.get_xlim()
    delta = 50

    modest.axes.set_xlim(xlim[0] + delta, xlim[1] + delta)
    axim.axes.set_xlim(xlim[0] + delta, xlim[1] + delta)
    check('move', modest.axes, axim.axes)

def test_zoom():
    """ zoom in """
    data = default_data()
    modest = init(ModestImage, data)
    axim = init(mi.AxesImage, data)
    lohi = 200, 250
    modest.axes.set_xlim(lohi)
    axim.axes.set_xlim(lohi)
    modest.axes.set_ylim(lohi)
    axim.axes.set_ylim(lohi)

    check('zoom', modest.axes, axim.axes)


INTRP_METHODS = ('nearest', 'bilinear', 'bicubic',
                 'spline16', 'spline36', 'hanning',
                 'hamming', 'hermite', 'kaiser',
                 'quadric', 'catrom', 'gaussian',
                 'bessel', 'mitchell', 'sinc', 'lanczos',
                 'none')

@pytest.mark.parametrize(('method'), INTRP_METHODS)
def test_interpolate(method):
    """ change interpolation """
    data = default_data()
    modest = init(ModestImage, data)
    axim = init(mi.AxesImage, data)

    lohi = 100, 150
    modest.axes.set_xlim(lohi)
    axim.axes.set_xlim(lohi)
    modest.axes.set_ylim(lohi)
    axim.axes.set_ylim(lohi)
    modest.set_interpolation(method)
    axim.set_interpolation(method)
    check('interp_%s' % method, modest.axes, axim.axes)

def test_scale():
    """change color scale"""

    data = default_data()
    modest = init(ModestImage, data)
    axim = init(mi.AxesImage, data)

    for im in [modest, axim]:
        im.norm.vmin = .7
        im.norm.vmin = .8

    check("cmap", modest.axes, axim.axes)

def test_unequal_limits():
    """Test different x/y scalings"""
    data = default_data()
    modest = init(ModestImage, data)
    axim = init(mi.AxesImage, data)

    for im in [modest, axim]:
        im.axes.set_aspect('auto')
        im.axes.set_xlim(20, 30)
        im.axes.set_ylim(10, 80)

    check('unequal_limits', modest.axes, axim.axes)

def test_alpha():
    """alpha changes """
    data = default_data()
    modest = init(ModestImage, data)
    axim = init(mi.AxesImage, data)

    for im in [modest, axim]:
        im.set_alpha(.3)

    check('alpha', modest.axes, axim.axes)
