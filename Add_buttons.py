#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 17/02/17 at 11:48 PM

@author: neil

Program description here

Version 0.0.1
"""

import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import sys
# detect python version
# if python 3 do this:
if (sys.version_info > (3, 0)):
    import tkinter
    import tkinter.simpledialog as tksimpledialog
else:
    import Tkinter as tkinter
    import tkSimpleDialog as tksimpledialog

# =============================================================================
# Define Class. Methods and Functions
# =============================================================================
class Add_Buttons(object):
    def __init__(self, ax=None, **kwargs):
        """
        Adds a select rectangle feature to any matplotlib axis, with select,
        clear all, and finish buttons

        :param ax: matplotlib axis, the frame to add the selector to
        :param kwargs: kwargs passed to the rectangle selector

        Current allowed kwargs are:

            button_labels    - list of strings
                               defines the name of each button to be displayed
                               Must be of length 1 or greater
            
            button_actions   - list of strings
                               defines the action of each button. Must be same
                               length as button_labels

                               currently supported actions are:
                               
                               "NEXT" - sends a return statement to move to
                                        next plot  
                                        self.result set to 1
                               
                               "PREVIOUS" - sends a return statement to move to
                                            previous plot
                                            self.result set to -1
                               
                               "CLOSE" - closes the plot
                               
                               "OPTION" - sends the button_label string
                                          self.result set to button_label
                                          
                               "UINPUT" - asks user for an input

            button_params    - list of dictionaries (optional)
                               if defined must be same length as button_labels
                               
                               a dictionary for each button
                               
                               keywords of each dictionary:
                               
                               "close" - when used with "OPTION" action will
                               close the plot after OPTION is clicked

        """
        # set supported actions (and link to function)
        self.actions = dict(NEXT=self.next,
                            PREVIOUS=self.previous,
                            CLOSE=self.end,
                            OPTION=self.option,
                            UINPUT=self.uinput)
        self.supported_actions = list(self.actions.keys())
        # current button params
        self.buttons = []
        self.regions = []
        # result (1, 0, -1, or string)
        self.result = 0
        # storage
        self.data = dict()
        # Deal with having no matplotlib axis
        if ax is None:
            self.ax = plt.gca()
        else:
            self.ax = ax
        # load keyword arguments
        if kwargs is None:
            kwargs = dict()
        self.button_labels = kwargs.get('button_labels', ['Close'])
        self.num_buttons = len(self.button_labels)
        self.button_actions = kwargs.get('button_actions', ['CLOSE'])
        dparams = [dict()]*self.num_buttons
        self.button_params = kwargs.get('button_params', dparams)
        # check inputs are correct
        self.validate_inputs()
        # create buttons
        self.create_buttons()

    def validate_inputs(self):
        # Make sure button labels is in correct format
        try:
            self.button_labels = list(self.button_labels)
            for it in self.button_labels:
                if type(it) != str:
                    raise TypeError()
        except TypeError:
            raise TypeError("Button labels must be a list of strings")
        # Make sure button actions is in correct format
        try:
            self.button_actions = list(self.button_actions)
            for it in self.button_labels:
                if type(it) != str:
                    raise TypeError()
        except TypeError:
            raise TypeError("Button labels must be a list of strings")
        # Make sure button actions is in correct format
        try:
            self.button_actions = list(self.button_actions)
            for it in self.button_params:
                if type(it) != dict:
                    raise TypeError()
        except TypeError:
            raise TypeError("Button params must be a dictionary")
        # Make sure list are not empty and same length
        if len(self.button_labels) < 1:
            raise ValueError("'button_labels' Must have at least one button "
                             "label in list.")
        if len(self.button_actions) != len(self.button_labels):
            raise ValueError("'button_actions' must be the same length "
                             "as 'button_labels")
        self.num_buttons = len(self.button_labels)
        # Make sure all button actions are supported
        sstr = self.supported_actions[0]
        for it in range(len(self.supported_actions)):
            if it > 0:
                sstr += ', {0}'.format(self.supported_actions[it])
        for it in range(len(self.button_actions)):
            e1 = "Action '{0}' not currently".format(self.button_actions[it])
            e2 = "supported. \n Currently supported actions are: \n"
            if self.button_actions[it] not in self.supported_actions:
                raise ValueError(e1 + e2 + sstr)

    def create_buttons(self, width=0.2):
        """
        Create a set of buttons along the bottom axis of the figure

        Need to re-write this to be generic based on used input
        (might not be possible as user need to define events)

        :param N: int, Number of buttons, default 3
        :param width: float, width of the buttons in x, must be less than
                      1.0/N
        :return:
        """
        b_N, b_length = self.num_buttons, width
        b_sep = (1. / (b_N + 1)) * (1 - b_N * b_length)
        for b in range(b_N):
            start = (b + 1) * b_sep + b * b_length
            r = [start, 0.05, b_length, 0.075]
            self.regions.append(r)

        # adjust the figure
        plt.subplots_adjust(bottom=0.25)
        # populate buttons
        for b in range(b_N):
            axbutton = plt.axes(self.regions[b])
            button = Button(axbutton, self.button_labels[b])
            button.on_clicked(self.actions[self.button_actions[b]])
            self.buttons.append(button)

    def next(self, event):
        """
        Event for clicking a button with action "NEXT"
        
        Sets self.result to 1
        
        :param event: 
        :return: 
        """
        self.result = 1

    def previous(self, event):
        """
        Event for clicking a button with action "PREVIOUS"

        Sets self.result to -1

        :param event: 
        :return: 
        """
        self.result = -1

    def option(self, event):
        """
        Event for clicking a button with action "OPTION"

        Sets self.result to button_label[i]  where i is the position in
        button_label and button_action of the button clicked

        :param event: 
        :return: 
        """
        pos = self.button_region(event)
        if pos is not None:
            self.result = self.button_labels[pos]

            close = self.button_params[pos].get('close', False)
            func = self.button_params[pos].get('func', None)
            if func is not None:
                func()
            if close:
                plt.close()

    def uinput(self, event):
        pos = self.button_region(event)
        if pos is not None:
            props = self.button_params[pos]
            title = props.get('title', 'Enter a Value')
            startvalue = props.get('comment', 'Message')
            name = props.get('name', 'x')
            fmt = props.get('fmt', None)
            minval = props.get('minval', None)
            maxval = props.get('maxval', None)

            root = tkinter.Tk()
            root.withdraw()
            if fmt == int:
                value = tksimpledialog.askinteger(title, startvalue,
                                                  minvalue=minval,
                                                  maxvalue=maxval)
            elif fmt == float:
                value = tksimpledialog.askfloat(title, startvalue,
                                                minvalue=minval,
                                                maxvalue=maxval)
            else:
                value = tksimpledialog.askstring(title, startvalue)
            self.data[name] = value
            root.destroy()


    def end(self, event):
        """
        Event for clicking the finish button - closes the graph

        :param event: event passed to function
        :return:
        """
        plt.close()

    def button_region(self, event):
        if len(self.regions) == 0:
            return None
        # get mouse click location in pixels
        x, y = event.x, event.y
        # get the current canvas width and height (in pixels)
        width = event.canvas.geometry().width()
        height = event.canvas.geometry().height()
        # loop round each button region
        for r, rn in enumerate(self.regions):
            # convert region to pixels
            rn1 = [rn[0]*width, rn[1]*height,
                   (rn[0] + rn[2])*width, (rn[1] + rn[3])*height]
            # test whether x, y are in region
            cond1 = (x > rn1[0]) & (x < rn1[2])
            cond2 = (y > rn1[1]) & (y < rn1[3])
            if cond1 and cond2:
                return r
        return None


# =============================================================================
# Start of code
# =============================================================================
# Main code to test the rectangle selector
if __name__ == '__main__':
    import numpy as np
    # plt.close()
    # fig, frame = plt.subplots(ncols=1, nrows=1)
    # x = np.random.rand(100)
    # y = np.random.rand(100)
    # plt.scatter(x, y, color='k', marker='o', s=20)
    # odict = dict(close=True)
    # a = Add_Buttons(ax=frame,
    #                 button_labels=['A', 'B'],
    #                 button_actions=['OPTION', 'OPTION'],
    #                 button_params=[odict, odict])
    # plt.show()
    # plt.close()

    plt.close()
    fig, frame = plt.subplots(ncols=1, nrows=1)
    x = np.random.rand(100)
    y = np.random.rand(100)
    plt.scatter(x, y, color='k', marker='o', s=20)
    odict = dict(close=True)
    udict = dict(name='x', fmt=int, title='Enter value',
                 comment='Please enter x in meters.', minval=4, maxval=10)
    a = Add_Buttons(ax=frame,
                    button_labels=['Enter value', 'Close'],
                    button_actions=['UINPUT', 'OPTION'],
                    button_params=[udict, odict])
    plt.show()
    plt.close()

# =============================================================================
# End of code
# =============================================================================
