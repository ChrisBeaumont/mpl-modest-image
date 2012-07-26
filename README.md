mpl-modest-image
================

*Friendlier matplotlib interaction with larger images*

ModestImage extends the matplotlib AxesImage class, and avoids
unnecessary calculation when rendering large-ish images (where most
image pixels aren't visible on the screen).

I bet there's some way to achieve the same effect with native
matplotlib objects, but I couldn't figure it out. If you know of a
way, let me know!


Why is AxesImage Slow?
----------------------

For the first draw request after a changing the color mapping or data
array, the AxesImage class calculates the RGBA value for every pixel
in the data array. That's a lot of work for large images, and usually
overkill given that the final rendering is limited by screen
resolution (usually 100K-1M pixels) and not image resolution (often
much more).

Matplotlib compensates for this by saving the results of this scaling
for as long as the data array and color mapping stay the same. This
means that subsequent renderings that only change the position or zoom
level are very fast. However, in interactive situations where the data
array or intensity scale change often, AxesImage wastes lots of time
calculating RGBA values for every pixel in a (potentially large) data
set.

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
          time_move: 25 ms per operation
     time_move_zoom: 35 ms per operation


``time_draw`` is the render time after the cache has been cleared
(e.g. after ``set_data`` has been called, or the colormap has been
changed). ModestImage is typically 5-10x faster for images of this
size. It is slightly slower than, though still competetive with,
AxesImage for move and zoom operations that do not clear the cache.

Unit tests can be found in the ``tests`` directory. ModestImage does not
always produce results identical to AxesImage at the pixel level, due to
how it downsamples images. The discrepancy is minor, however, and disappears
if no downsampling takes place (i.e. a screen pixel samples <= 1 data pixel)

