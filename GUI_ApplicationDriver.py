# David Lindsey - GISC 6389 - Master's Project
# Contact: dcl160230@utdallas.edu
# The following code represents the functionality for GUI_ApplicationDriver.

import tkinter
from tkinter import messagebox
from GUI_HazardsMenu import HazardsMenu

# For Python 2.7 consideration:
# import Tkinter as tkinter
# import tkMessageBox as messagebox

# User-defined parameters for width/height of GUI
guiWindow_HazardMenu_Width = 300
guiWindow_HazardMenu_Height = 150

class AppDriver(tkinter.Frame):

    # This class represents the primary Python code that user's will execute
    # to drive the entire application.

    def __init__(self, *args, **kwargs):

        tkinter.Frame.__init__(self, *args, **kwargs)

        # Executes HazardsMenu class within the AppDriver
        hazMenu = HazardsMenu(self)
        hazMenu.grid(column=0, row=0, padx=0, pady=0)

        # Shows the GUI parameters from HazardsMenu within the AppDriver frame.
        hazMenu.show()

if __name__ == "__main__":

    # Creates the tkinter GUI window as win.
    win = tkinter.Tk()

    # Title of GUI Window
    win.title("Select Hazard Type")

    # Pixel width/height of the user's screen
    screenWidth = win.winfo_screenwidth()
    screenHeight = win.winfo_screenheight()

    # Calculates X/Y start position for the GUI window to appear.
    # The following formula will open the GUI window at center of user's screen.
    guiWindow_x = (screenWidth / 2) - (guiWindow_HazardMenu_Width / 2)
    guiWindow_y = (screenHeight / 3) - (guiWindow_HazardMenu_Height / 3)

    # Geometry parameters for the GUI window.
    win.geometry("%dx%d+%d+%d" % (guiWindow_HazardMenu_Width,
                                  guiWindow_HazardMenu_Height, guiWindow_x,
                                  guiWindow_y))

    # GUI Window is locked and non-resizable.
    win.resizable(False, False)

    # Execute AppDriver class within the GUI window.
    mainGUI = AppDriver(win)
    mainGUI.grid(column=0, row=0, padx=0, pady=0)

    # ArcPy module is imported at this location so as to check for any runtime
    # errors (due to internet connectivity issues and/or licensing issues).
    try:

        import arcpy

    except RuntimeError:  # Example: "Not signed into Portal."

        # In the event of a "Runtime Error", the user is given an error message.
        # The user will be given a choice to continue with the application or
        # to exit.
        userSelection = messagebox.askyesno("Runtime Error Message",
            "WARNING: Unable to verify ArcGIS licensing.\n"
            "As a result, you will not be able to utilize any ArcGIS or ArcPy "
            "functionality.\n"
            "This could be the result of internet connectivity issues or "
            "licensing problems.\n\n"
            "Do you wish to continue running this application?\n"
            "Additional, unexpected problems may be encountered if you choose "
            "to proceed.")

        if userSelection == True:

            pass

        else:

            exit()

    # Run mainloop to execute/display the GUI.
    win.mainloop()