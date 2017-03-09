#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 17/02/17 at 12:15 PM

Based on code from here:
http://matplotlib.org/examples/pylab_examples/cursor_demo.html

@author: neil

Program description here

Version 0.0.0
"""

from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np

# =============================================================================
# Define variables
# =============================================================================


# -----------------------------------------------------------------------------



# =============================================================================
# Define functions
# =============================================================================
class Cursor(object):
    def __init__(self, ax, kwargs=None):


        # Deal with kwargs
        if kwargs is None:
            kwargs = dict()
        # Extract variables from kwargs
        self.display_y = kwargs.get('display_y', True)
        self.display_x = kwargs.get('display_x', True)
        self.posx = kwargs.get('posx', 0.7)
        self.posy = kwargs.get('posy', 0.9)

        self.ax = ax
        self.lx = ax.axhline(color='k')  # the horiz line
        self.ly = ax.axvline(color='k')  # the vert line

        # text location in axes coords
        self.txt = ax.text(self.posx, self.posy, '', transform=ax.transAxes)

    def mouse_move(self, event):
        if not event.inaxes:
            return

        x, y = event.xdata, event.ydata
        # update the line positions
        self.lx.set_ydata(y)
        self.ly.set_xdata(x)

        if self.display_y and self.display_x:
            self.txt.set_text('x={0:.2f}, y={1:.2f}'.format(x, y))
        elif self.display_y:
            self.txt.set_text('y={1:.2f}'.format(x, y))
        elif self.display_x:
            self.txt.set_text('x={0:.2f}'.format(x, y))
        plt.draw()


class SnaptoCursor(object):
    """
    Like Cursor but the crosshair snaps to the nearest x,y point
    For simplicity, I'm assuming x is sorted
    """

    def __init__(self, ax, x, y):
        self.ax = ax
        self.lx = ax.axhline(color='k')  # the horiz line
        self.ly = ax.axvline(color='k')  # the vert line
        self.x = x
        self.y = y
        # text location in axes coords
        self.txt = ax.text(0.7, 0.9, '', transform=ax.transAxes)


    def mouse_move(self, event):

        if not event.inaxes:
            return

        x, y = event.xdata, event.ydata

        indx = np.searchsorted(self.x, [x])[0]

        x = self.x[indx]
        y = self.y[indx]
        # update the line positions
        self.lx.set_ydata(y)
        self.ly.set_xdata(x)

        self.txt.set_text('x=%1.2f, y=%1.2f' % (x, y))
        # print('x=%1.2f, y=%1.2f' % (x, y))
        plt.draw()



class RegionSelect(object):
    def __init__(self, ax, kwargs=None):

        # Deal with kwargs
        if kwargs is None:
            kwargs = dict()




if __name__ == '__main__':

    fig, frame = plt.subplots(ncols=1, nrows=1)

    fig.canvas.mpl_connect()



def use_measurement_cursor(ax=None, **kwargs):
    """
    Use measurement cursor on matplotlib.pyplot.show

    :param ax: matplotlib axis (frame), i.e. plt.subplot() plt.gca()
    :param kwargs: dictionary, key word arguments to pass to cursors

        currently accepted keywords arguments are:

            - display_x     bool, default True, if False does not display
                            x coordinate
            - display_y     bool, default False, if False does not display
                            x coordinate
            - posx          float, default=0.7, location in plot between 0
                            and 1 on the x axis to display cursor
                            measurement text
            - posy          float, default=0.9, location in plot between 0
                            and 1 on the y axis to display cursor
                            measurement text
    :return:
    """
    if ax is None:
        ax = plt.gca()

    cursor = Cursor(ax, kwargs)
    plt.connect('motion_notify_event', cursor.mouse_move)
    return cursor

# ----------------------------------------------------------------------

# =============================================================================
# End of code
# =============================================================================
