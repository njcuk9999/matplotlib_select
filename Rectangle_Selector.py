#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 17/02/17 at 11:48 PM

@author: neil

Program description here

Version 0.0.1
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.widgets import Button

# =============================================================================
# Define variables
# =============================================================================


# =============================================================================
# Define Class. Methods and Functions
# =============================================================================
class Select_Rectange(object):
    def __init__(self, ax=None, kwargs=None):
        """
        Adds a select rectangle feature to any matplotlib axis, with select,
        clear all, and finish buttons

        :param ax: matplotlib axis, the frame to add the selector to
        :param kwargs: kwargs passed to the rectangle selector

        Current allowed kwargs are:

            - current_rect_color,  colour to be sent to the selector rectangle
                                   default: 'r'
            - current_rect_alpha   float, alpha to be send to the selector
                                   rectangle, default: 0.125
            - current_rect_zorder  int, zorder of the selector rectangle
                                   default: 5
            - current_rect_color   colour to be sent to the saved rectangles
                                   default: 'b'
            - current_rect_alpha   float, alpha to be send to the saved
                                   rectangles, default: 0.125
            - current_rect_zorder  int, zorder of the saved rectangle
                                   default: 4


        """
        # Deal with having no matplotlib axis
        if ax is None:
            self.ax = plt.gca()
        else:
            self.ax = ax
        # load keyword arguments
        if kwargs is None:
            kwargs = dict()
        self.crectprops = dict()
        self.crectprops['color'] = kwargs.get('current_rect_color', 'r')
        self.crectprops['alpha'] = kwargs.get('currentrect_alpha', 0.125)
        self.crectprops['zorder'] = kwargs.get('currentrect_zorder', 5)
        self.srectprops = dict()
        self.srectprops['color'] = kwargs.get('saved_rect_color', 'b')
        self.srectprops['alpha'] = kwargs.get('saved_rect_alpha', 0.125)
        self.srectprops['zorder'] = kwargs.get('saved_rect_zorder', 4)

        # define default attributes
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.rect = None
        self.pressed = False
        self.in_main_axes = True
        self.regions = []
        self.save_rectangles = []
        self.data = []

        # Set title
        self.ax.set_title('Click and draw to select rectangle region')

        # create buttons
        self.create_buttons()

        # Event handling
        self.ax.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.ax.figure.canvas.mpl_connect('motion_notify_event', self.on_move)
        self.ax.figure.canvas.mpl_connect('button_release_event',
                                          self.on_release)
        self.ax.figure.canvas.mpl_connect('axes_enter_event', self.enter_axes)
        self.ax.figure.canvas.mpl_connect('axes_leave_event', self.leave_axes)

    # -------------------------------------------------------------------------
    # Mouse movement and click function
    # -------------------------------------------------------------------------
    def on_press(self, event):
        """
        Event for clicking of the mouse in the main axis (ax) window (
        i.e. selects the first corner of the rectangle)

        :param event: event passed to function
        :return:
        """
        # if we are not in the main axis don't continue
        if not self.in_main_axes:
            return
        # if toolbar is active don't continue
        if self.ax.figure.canvas.manager.toolbar._active is not None:
            return
        # set the starting points from mouse location
        self.x0 = event.xdata
        self.y0 = event.ydata
        # highlight that we have started the selection rectangle
        self.pressed = True

    def on_move(self, event):
        """
        Event for moving the mouse in the main axis (ax) window once a on_press
        event has taken place (i.e. allows the rectangle to be dragged)

        :param event: event passed to function
        :return:
        """
        # if we are not in the main axis don't continue
        if not self.in_main_axes:
            return
        # if toolbar is active don't continue
        if self.ax.figure.canvas.manager.toolbar._active is not None:
            return
        # do not draw if mouse has not been clicked
        if not self.pressed:
            return
        # set the end points of the selection rectangle (whilst moving)
        self.x1 = event.xdata
        self.y1 = event.ydata
        # Redraw the rectangle selection
        self.draw_current_rec()

    def on_release(self, event):
        """
        Event for clicking of the mouse in the main axis (ax) window (
        i.e. selects the last corner of the rectangle)

        :param event: event passed to function
        :return:
        """
        # if we are not in the main axis don't continue
        if not self.in_main_axes:
            return
        # if toolbar is active don't continue
        if self.ax.figure.canvas.manager.toolbar._active is not None:
            return
        # highlight that we have ended the selection rectangle
        self.pressed = False
        # set the end points of the selection rectangle (whilst moving)
        self.x1 = event.xdata
        self.y1 = event.ydata
        # Redraw the rectangle selection
        self.draw_current_rec()

    def leave_axes(self, event):
        """
        Event for leaving an axes

        :param event: event passed to function
        :return:
        """
        self.in_main_axes = False

    def enter_axes(self, event):
        """
        Event for entering an axis, if this is main axis then flag it as such

        :param event: event passed to function
        :return:
        """
        # Only want to be entering the main window
        if event.inaxes.axis() == self.ax.axis():
            self.in_main_axes = True

    def create_buttons(self, N=3, width=0.2):
        """
        Create a set of buttons along the bottom axis of the figure

        Need to re-write this to be generic based on used input
        (might not be possible as user need to define events)

        :param N: int, Number of buttons, default 3
        :param width: float, width of the buttons in x, must be less than
                      1.0/N
        :return:
        """
        b_N, b_length = N, width
        b_sep = (1. / (b_N + 1)) * (1 - b_N * b_length)
        for b in range(b_N):
            start = (b + 1) * b_sep + b * b_length
            r = [start, 0.05, b_length, 0.075]
            self.regions.append(r)
        plt.subplots_adjust(bottom=0.25)
        self.axselect = plt.axes(self.regions[0])
        self.axclear = plt.axes(self.regions[1])
        self.axfinish = plt.axes(self.regions[2])
        self.bselect = Button(self.axselect, 'Select Region')
        self.bselect.on_clicked(self.select)
        self.bclear = Button(self.axclear, 'Clear all regions')
        self.bclear.on_clicked(self.clear)
        self.bfinish = Button(self.axfinish, 'Finish')
        self.bfinish.on_clicked(self.end)

    def select(self, event):
        """
        Event for clicking the select button - selects the currently draw
        selector rectangle, saves the corners to self.data and draws a saved
        rectangle in the place of the selector rectangle

        :param event: event passed to function
        :return:
        """
        if self.x0 is None:
            return
        args = [self.x0, self.x1, self.y0, self.y1]
        if args in self.data:
            return
        print('Coords x=({0:.2f}, {1:.2f})  y=({2:.2f}, {3:.2f})'.format(*args))
        self.record_points()
        self.draw_saved_rec()

    def clear(self, event):
        """
        Event for clicking the clear button - clears all rectangle selectors
        and the data associated with them

        :param event: event passed to function
        :return:
        """
        # Clear data
        self.data = []
        # if self.x0 is None then we don't need to clear (already clear)
        if self.x0 is None:
            return
        # Clear canvas
        start = (self.x0, self.y0)
        width, height = self.x1 - self.x0, self.y1 - self.y0
        for it in range(len(self.save_rectangles)):
            self.save_rectangles[it].set_width(1.e-9)
            self.save_rectangles[it].set_height(1.e-9)
            self.save_rectangles[it].set_xy(start)
            self.ax.add_patch(self.save_rectangles[it])
        self.rect.set_width(1.e-9)
        self.rect.set_height(1.e-9)
        self.rect.set_xy(start)
        self.ax.figure.canvas.draw()

    def end(self, event):
        """
        Event for clicking the finish button - closes the graph

        :param event: event passed to function
        :return:
        """
        plt.close()

    # -------------------------------------------------------------------------
    # Draw and record functions
    # -------------------------------------------------------------------------
    def draw_current_rec(self):
        """
        Draws the selector rectangle using the corners (x0, y0) and (x1, y1)
        :param self:
        :return:
        """
        start = (self.x0, self.y0)
        width, height = self.x1 - self.x0, self.y1 - self.y0

        if self.rect is None:
            self.rect = Rectangle(start, width, height, **self.crectprops)
            self.ax.add_patch(self.rect)
        else:
            self.rect.set_width(width)
            self.rect.set_height(height)
            self.rect.set_xy(start)
            self.ax.figure.canvas.draw()

    def draw_saved_rec(self):
        """
        Draws the saved rectangle using the corners (x0, y0) and (x1, y1)

        :param self:
        :return:
        """
        start = (self.x0, self.y0)
        width, height = self.x1 - self.x0, self.y1 - self.y0
        Rec = Rectangle(start, width, height, **self.srectprops)
        self.save_rectangles.append(Rec)
        self.ax.add_patch(Rec)
        self.rect.set_width(1.e-9)
        self.rect.set_height(1.e-9)
        self.rect.set_xy(start)
        self.ax.figure.canvas.draw()

    def record_points(self):
        """
        Records the data of the selected rectangle to self.data

        :return:
        """
        self.data.append([self.x0, self.x1, self.y0, self.y1])


# =============================================================================
# Start of code
# =============================================================================
# Main code to test the rectangle selector
if __name__ == '__main__':
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
    
    plt.scatter(x, y, color='k', marker='o', s=20, label='All data')
    for r, rec in enumerate(a.data):
        # Print the data
        print ('Selected region {0} was:'.format(r))
        print('Coords x=({0:.2f}, {1:.2f})  y=({2:.2f}, {3:.2f})'.format(*rec))
        
        # select the data and plot it in red
        mask = (x > rec[0]) & (x < rec[1]) & (y > rec[2]) & (y < rec[3])
        plt.scatter(x[mask], y[mask], color='r', marker='o', s=20, label='Selected')

    plt.legend(loc=0)
    plt.show()
    plt.close()
    # ----------------------------------------------------------------------

# =============================================================================
# End of code
# =============================================================================
