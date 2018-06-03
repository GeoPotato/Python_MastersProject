import tkinter
from tkinter import ttk
from tkinter import messagebox
import os

# For Python 2.7 consideration:
# import Tkinter as tkinter
# import ttk
# import tkMessageBox as messagebox

from GUI_FrameLifts import FrameLifts

# User-defined parameters for width/height of GUI
guiWindow_HazardMenu_Width = 300
guiWindow_HazardMenu_Height = 150

# Hazard values that will populate the combobox.
hazardValues = "Select...", "Earthquake", "Hail", "Hurricane","Tornado", "Wind"

class HazardsMenu(FrameLifts):
    def __init__(self, *args, **kwargs):
        FrameLifts.__init__(self, *args, **kwargs)

        self.winfo_toplevel().title("Select Hazard Type")
        self.winfo_toplevel().wm_geometry("%dx%d" % (
            guiWindow_HazardMenu_Width, guiWindow_HazardMenu_Height))

        # Create GUI window frame for Hazard Menu widgets and buttons.
        self.winFrame = tkinter.Frame(self)
        self.winFrame.grid(column=0, row=0, padx=0, pady=0)

        # Frame for icon frame within winFrame.
        iconFrame = ttk.Frame(self.winFrame)
        iconFrame.grid(column=0, row=0, padx=25, pady=10)

        # UT-Dallas GIF logo used within the GUI.
        dirFolder = os.path.dirname(__file__)
        gifPath = os.path.join(dirFolder, "Icon_UTD.gif")
        self.photo_UTDallas_Icon = tkinter.PhotoImage(file=gifPath)
        colorCode_UTD_Orange = "#C75B12"
        self.subSampleImage = self.photo_UTDallas_Icon.subsample(4, 4)
        self.label_for_icon = ttk.Label(iconFrame, borderwidth=2,
                                        relief="solid",
                                        background=colorCode_UTD_Orange,
                                        image=self.subSampleImage)
        self.label_for_icon.photo = self.photo_UTDallas_Icon
        self.label_for_icon.grid(column=0, row=0, padx=0,
                                 pady=0, sticky=tkinter.EW)

        # Frame for widgets within winFrame.
        widgetFrame = ttk.Frame(self.winFrame)
        widgetFrame.grid(column=0, row=1, padx=25, pady=10)

        # Adding a label to widgetFrame.
        widgetLabel_HazardTypes = \
            ttk.Label(widgetFrame,text="Please select hazard type:  ")
        widgetLabel_HazardTypes.grid(column=0, row=1, padx=0, pady=0)

        # Creating/adding the combobox to the widgetFrame.
        self.stringHazardTypes = tkinter.StringVar()
        widgetCombo_HazardTypes = ttk.Combobox(widgetFrame, width=14,
                                    textvariable=self.stringHazardTypes,
                                    state="readonly")
        widgetCombo_HazardTypes["values"] = (hazardValues)
        widgetCombo_HazardTypes.grid(column=1, row=1, padx=0, pady=0)

        # Display first index of hazardValues list.
        widgetCombo_HazardTypes.current(0)

        # Frame for buttons within winFrame.
        buttonFrame = ttk.Frame(self.winFrame)
        buttonFrame.grid(column=0, row=2, padx=0, pady=10)

        # Exit button ends the application.
        buttonExit = \
            ttk.Button(buttonFrame,text="Exit",command=self.func_ExitClick)
        buttonExit.grid(column=0, row=1, padx=15, pady=0)

        # Next button takes combobox selection and proceeds to affiliated GUI.
        buttonNext = \
            ttk.Button(buttonFrame,text="Next",command=self.func_NextClick)
        buttonNext.grid(column=1, row=1, padx=15, pady=0)

    # Exits the application.
    def func_ExitClick(self):
        self.quit()
        self.destroy()
        exit()

    #Button click event for Next button
    def func_NextClick(self):

        if self.stringHazardTypes.get() == "Earthquake":

            from GUI_EarthquakeOptions import EarthquakeOptions

            earthquake_Op = EarthquakeOptions(self)
            earthquake_Op.place(in_= self, x=0, y=0, relwidth=1, relheight=1)
            earthquake_Op.lift()

        elif self.stringHazardTypes.get() == "Hail":

            from GUI_HailOptions import HailOptions

            hail_Op = HailOptions(self)
            hail_Op.place(in_=self, x=0, y=0, relwidth=1, relheight=1)
            hail_Op.lift()

        elif self.stringHazardTypes.get() == "Hurricane":

            from GUI_HurricaneOptions import HurricaneOptions

            hurricane_Op = HurricaneOptions(self)
            hurricane_Op.place(in_=self, x=0, y=0, relwidth=1, relheight=1)
            hurricane_Op.lift()

        elif self.stringHazardTypes.get() == "Tornado":

            from GUI_TornadoOptions import TornadoOptions

            tornado_Op = TornadoOptions(self)
            tornado_Op.place(in_=self, x=0, y=0, relwidth=1, relheight=1)
            tornado_Op.lift()

        elif self.stringHazardTypes.get() == "Wind":

            from GUI_WindOptions import WindOptions

            wind_Op = WindOptions(self)
            wind_Op.place(in_=self, x=0, y=0, relwidth=1, relheight=1)
            wind_Op.lift()

        else:

            messagebox.showwarning("",
                                   "Oops! You must make a selection from list.")