mpl-modest-image
================

*Friendlier matplotlib interaction with larger images*

ModestImage extends the matplotlib AxesImage class, and avoids unnecessary
calculation when rendering large-ish images (where most image pixels
aren't visible on the screen).