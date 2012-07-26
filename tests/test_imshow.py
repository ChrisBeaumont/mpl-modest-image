import numpy as np
import matplotlib.pyplot as plt

from modest_image import ModestImage, imshow


def default_data():
    x, y = np.mgrid[0:100, 0:100]
    return np.sin(x / 25) * np.cos(y / 50)


def check_props(obj1, obj2, props):
    for p in props:
        v1 = obj1.__getattribute__('get_%s' % p)()
        v2 = obj2.__getattribute__('get_%s' % p)()
        assert v1 == v2


def check_artist_props(art1, art2):
    """Assert that properties of two artists are equal"""

    props = ['alpha', 'clim', 'clip_on', 'clip_path',
             'interpolation', 'label', 'rasterized',
             'resample', 'snap', 'url', 'visible', 'zorder']
    check_props(art1, art2, props)


def check_axes_props(ax1, ax2):
    props = ['aspect']
    check_props(ax1, ax2, props)


def setup_function(func):
    plt.clf()
    plt.cla()


def teardown_function(func):
    plt.close()


def test_imshow_creates_modest_image():
    """returns a modestImage"""
    data = default_data()
    fig = plt.figure()
    ax = fig.add_subplot(111)

    artist = imshow(ax, data)

    assert isinstance(artist, ModestImage)
    assert artist in artist.axes.images


def test_imshow_mimics_mpl():
    """properties of two axes and artists objects should be same"""

    data = default_data()
    fig = plt.figure()
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)

    artist1 = ax1.imshow(data)
    artist2 = imshow(ax2, data)

    check_artist_props(artist1, artist2)
    check_axes_props(ax1, ax2)
