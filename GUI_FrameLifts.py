# David Lindsey - GISC 6389 - Master's Project
# Contact: dcl160230@utdallas.edu
# The following code represents the functionality for FrameLifts.
import tkinter

# For Python 2.7 consideration:
# import Tkinter as tkinter

class FrameLifts(tkinter.Frame):

    # The purpose of this class is to "lift" a user-specified hazard option's
    # layout into view within the GUI window.

    def __init__(self, *args, **kwargs):

        tkinter.Frame.__init__(self, *args, **kwargs)

    def show(self):

        self.lift()