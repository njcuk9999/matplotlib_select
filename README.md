# Cook et al. 2017 Matplotlib data selection functions


## Class ```Select_Rectange(ax=None, kwargs=None)```

Constructor ```__init__(self, ax=None, kwargs=None)```

Adds a select rectangle feature to any matplotlib axis

will allow user to select regions of a matplotlib graph and get the data 
back for each region (x start, x end, y start, y end)

with select, clear all, and finish buttons

__:param ax:__ matplotlib axis, the frame to add the selector to

__:param kwargs:__ kwargs passed to the rectangle selector

Current allowed kwargs are:

* __current_rect_color__   colour to be sent to the selector rectangle
                           default: 'r'
* __current_rect_alpha__   float, alpha to be send to the selector
                           rectangle, default: 0.125
* __current_rect_zorder__  int, zorder of the selector rectangle
                           default: 5
* __current_rect_color__   colour to be sent to the saved rectangles
                           default: 'b'
* __current_rect_alpha__   float, alpha to be send to the saved
                           rectangles, default: 0.125
* __current_rect_zorder__  int, zorder of the saved rectangle
                           default: 4
                               
a.data returns list of (x start, x end, y start, y end) for each rectangle selected

i.e. if 3 rectangles are selected:
```python
a.data = [ [xstart1, xend1, ystart1, yend1], 
           [xstart2, xend2, ystart2, yend2], 
           [xstart3, xend3, ystart3, yend3] ]
```   
This can then be used to create a mask of the data:
```python
mask = (x > rec[0]) & (x < rec[1]) & (y > rec[2]) & (y < rec[3])
```   
where x and y are the data used in the matplotlib plot
    

### Example of use

    import numpy as np
    plt.close()
    fig, frame = plt.subplots(ncols=1, nrows=1)
    x = np.random.rand(100)
    y = np.random.rand(100)
    plt.scatter(x, y, color='k', marker='o', s=20)
    a = Select_Rectange(frame)
    plt.show()
    plt.close()
    # ----------------------------------------------------------------------
    
    plt.scatter(x, y, color='k', marker='o', s=20, 'All data')
    for r, rec in enumerate(a.data):
        # Print the data
        print ('Selected region {0} was:'.format(r)
        print(Coords x=({0:.2f}, {1:.2f})  y=({2:.2f}, {3:.2f})'.format(*rec))
        
        # select the data and plot it in red
        mask = (x > rec[0]) & (x < rec[1]) & (y > rec[2]) & (y < rec[3])
        plt.scatter(x[mask], y[mask], color='r', marker='o', s=20, label='Selected')

    plt.legend(loc=0)
    plt.show()
    plt.close()
    # ----------------------------------------------------------------------
    
    
    
## Measuring cursor 

Original basis of code above (here for reference)

Based on code from here:  http://matplotlib.org/examples/pylab_examples/cursor_demo.htm

This example shows how to use matplotlib to provide a data cursor.  It
uses matplotlib to draw the cursor and may be a slow since this
requires redrawing the figure with every mouse move.

Faster cursoring is possible using native GUI drawing, as in
wxcursor_demo.py.

The mpldatacursor and mplcursors third-party packages can be used to achieve a
similar effect.  

See https://github.com/joferkington/mpldatacursor and https://github.com/anntzer/mplcursors
