ModestImage
===========

*Friendlier matplotlib interaction with large images*

ModestImage extends the matplotlib AxesImage class, and avoids
unnecessary calculation and memory when rendering large images (where most
image pixels aren't visible on the screen). It has the following
benefits over AxesImage:

 * Draw time is (roughly) independent of image size
 * Large ``numpy.memmap`` arrays can be visualized, without making an
   in-memory copy of the entire array. This enables visualization of
   images too large to fit in memory.

Using ModestImage
-----------------

The easiest way is to use the modified ``imshow`` function:

    import matplotlib.pyplot as plt
    from modest_image import ModestImage, imshow

    ax = plt.gca()
    imshow(ax, image_array, vmin=0, vmax=10)
    plt.show()

``imshow`` accepts all the keyword arguments that the matplotlib
function does. The ``vmin`` and ``vmax`` keywords aren't necessary
but, if they are not provided, the entire image will be scanned to
determine the min/max values. This can be slow if the array is huge.

To create a ModestImage artist directly:

    artist = ModestImage(data=array)

Looking at very big FITS images
-------------------------------

    import matplotlib.pyplot as plt
    import pyfits
    from modest_image import imshow

    huge_array = pyfits.open('file_name.fits', memmap=True)[0].data
    artist = imshow(ax, huge_array, vmin=0, vmax=10)
    plt.show()

This opens almost instantly, with a modest memory footprint.

Why is Matplotlib Image Drawing Slow?
-------------------------------------

For the first draw request after setting the color mapping or data
array, AxesImage (the default matplotlib image class) calculates the
RGBA value for every pixel in the data array. That's a lot of work for
large images, and usually overkill given that the final rendering is
limited by screen resolution (usually 100K-1M pixels) and not image
resolution (often much more).

AxesImage compensates for this by saving the results of this
scaling. This means that subsequent renderings that only change the
position or zoom level are very fast. However, in interactive
situations where the data array or intensity scale change often,
AxesImage wastes lots of time calculating RGBA values for every pixel
in a (potentially large) data set. It also makes several temporary
arrays with size comparable to the original array, wasting memory.

How is ModestImage faster?
--------------------------

ModestImage resamples the image array at each draw request, extracting
a smaller image whose resolution and extent are matched to the screen
resolution. Thus, the RGBA scaling step is much faster, since it takes
place only for pixels relevant for the current rendering.

This scheme does not take advantage of AxesImage's caching, and thus
redraws after move and zoom operations are slightly slower. However,
draws after colormap and data changes are substantially faster, and most
redraws are fast enough for interactive use.

Performance and Tests
---------------------

``speed_test.py`` compares the peformance of ModestImage and
AxesImage. For a 1000x1000 pixel image::

    Performace Tests for AxesImage

           time_draw: 186 ms per operation
           time_move: 19 ms per operation
      time_move_zoom: 28 ms per operation

    Performace Tests for ModestImage

          time_draw: 25 ms per operation
          time_move: 20 ms per operation
     time_move_zoom: 28 ms per operation


``time_draw`` is the render time after the cache has been cleared
(e.g. after ``set_data`` has been called, or the colormap has been
changed). ModestImage is slightly slower than, though still
competetive with, AxesImage for move and zoom operations where
AxesImage uses cached data.

Unit tests can be found in the ``tests`` directory. ModestImage does not
always produce results identical to AxesImage at the pixel level, due to
how it downsamples images. The discrepancy is minor, however, and disappears
if no downsampling takes place (i.e. a screen pixel samples <= 1 data pixel)
