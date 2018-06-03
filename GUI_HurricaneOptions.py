# David Lindsey - GISC 6389 - Master's Project
# Contact: dcl160230@utdallas.edu
# The following code represents the functionality for Hurricane Options.

# All import statements for utilized modules, excluding ArcPy.
# ArcPy module will be imported at a later time.
import tkinter
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
import sys
import os
import shutil
import time
import csv
import numpy
from urllib import request
from urllib.error import HTTPError
from urllib.error import URLError
import zipfile
import calendar
from datetime import datetime
import datetime
from collections import OrderedDict
import traceback
from time import sleep  # careful - this can freeze the GUI
from threading import Thread  # this is used to unfreeze the GUI
from GUI_FrameLifts import FrameLifts
from statistics import mode
from statistics import StatisticsError

# For Python 2.7 consideration:
# import Tkinter as tkinter
# import tkFileDialog as filedialog
# import ttk
# import tkMessageBox as messagebox
# import ScrolledText as scrolledtext
# from urllib2 import HTTPError
# from urllib2 import URLError
# from dummy_threading import Thread
# import pip
# pip.main(["install", "statistics"])
# from statistics import mode, StatisticsError

# Programmer-defined parameters for width/height of GUI
guiWindow_HurricaneOptions_Width = 470
guiWindow_HurricaneOptions_Height = 225

# Formula to acquire date from one year ago in YYYY format.
int_OneYearAgo = int(datetime.datetime.today().strftime("%Y")) - 1

# Integer iterator used for setting all years, starting with value from two
# years ago.
int_YearIterator = int_OneYearAgo

# Tuple for populating hurricane timespan text values within the combo box.
textCombo_HurricaneTimespan = ()
textCombo_HurricaneTimespan = textCombo_HurricaneTimespan + \
                         ("Select...", "All | 1842-" + str(int_OneYearAgo),)

# List for populating the custom year comboboxes with integer values. It will
# be populated in the next While loop.
intList_Years = []

# NOAA began keeping individual yearly CSV files beginning in 1842. These
# choices must be iterated and added to the tuple and list with this While loop.
while int_YearIterator >= 1842:
    textCombo_HurricaneTimespan = \
        textCombo_HurricaneTimespan + (str(int_YearIterator),)
    intList_Years.append(str(int_YearIterator))
    int_YearIterator = int_YearIterator - 1

# Insert "Custom" into tuple for timespan drop-down list.
textCombo_HurricaneTimespan = textCombo_HurricaneTimespan + ("Custom...",)

# Tuple for populating hurricane intensity text values within the combo box.
textCombo_HurricaneIntensity = ("Select...", "All", "Trop. Depression",
                                "Trop. Storm", "Cat. 1", "Cat. 2", "Cat. 3",
                                "Cat. 4", "Cat. 5", "Custom...")

# Tuple for populating the timespan combobox for monthly integer values when
# the custom timespan option is selected.
intCombo_Months = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)

# Tuple for populating the intensity combobox with integer values for the
# custom intensity option.
list_Speed = [0]
int_SpeedIterator = 10
while int_SpeedIterator <= 200:
    list_Speed.append(int_SpeedIterator)
    int_SpeedIterator = int_SpeedIterator + 10

int_Combo_Speeds = list_Speed

# Dictionary showing Census FIPs codes assigned to state abbreviation.
# This is used for the Census-derived polygon shapefile manipulations.
dict_StateName_StateFIPs = {"AL": "01", "AK": "02", "AZ": "04", "AR": "05",
                            "CA": "06", "CO": "08", "CT": "09", "DE": "10",
                            "DC": "11", "FL": "12", "GA": "13", "HI": "15",
                            "ID": "16", "IL": "17", "IN": "18", "IA": "19",
                            "KS": "20", "KY": "21", "LA": "22", "ME": "23",
                            "MD": "24", "MA": "25", "MI": "26", "MN": "27",
                            "MS": "28", "MO": "29", "MT": "30", "NE": "31",
                            "NV": "32", "NH": "33", "NJ": "34", "NM": "35",
                            "NY": "36", "NC": "37", "ND": "38", "OH": "39",
                            "OK": "40", "OR": "41", "PA": "42", "RI": "44",
                            "SC": "45", "SD": "46", "TN": "47", "TX": "48",
                            "UT": "49", "VT": "50", "VA": "51", "WA": "53",
                            "WV": "54", "WI": "55", "WY": "56"}

# Key/Values from Dictionary, sorted by Value (state abbreviation).
# To be used to populate the State combo box under Clipping Options (as string).
dictKeys_StateNames = sorted(dict_StateName_StateFIPs)

# Dictionary remains intact and unchanged (not string), only sorted.
# This is used for dictionary iterations with the UpdateCursor operations.
dictKeys_OrderedDict_StateNames = OrderedDict(dict_StateName_StateFIPs)

# Generic header for any error messages received.
errorMessage_Header = "Error Message"

# This string represents the static portion of the URL path for accessing the
# YEARLY hurricane Shapefile from NOAA website.
hurr_YYYY_siteURL = \
    "ftp://eclipse.ncdc.noaa.gov/pub/ibtracs/v03r10/all/shp/year/"

# This string represents the static portion of the URL path for accessing ALL
# hurricanes Shapefile from NOAA website.
hurr_All_siteURL = \
    "ftp://eclipse.ncdc.noaa.gov/pub/ibtracs/v03r10/all/shp/"

# Text that will display within the URL textbox prior to a web URL link being
# created by the user.
urlDialog_Message = "URL will populate once Timespan and Intensity have been " \
                    "selected."

# Text that will display within the output folder textbox prior to an output
# workspace being selected by the user.
folderDialog_Message = "Output workspace folder path will display here..."

# Various components of output naming conventions to be used.
noaa = "noaa"
hurr = "hurr"
ibtracs = ".ibtracs"
lineVersion = "_all_lines.v03r10"
yearDot = "Year."
fileExtCSV = ".csv"
fileExtZip = ".zip"
fileExtShp = ".shp"
fileExtDbf = ".dbf"
fileExtPrj = ".prj"
fileExtShx = ".shx"
fileExtText = ".txt"

# Color variables for use with ScrolledText box output text.
# Red for errors, orange for warning, and blue for geoprocessing messages.
color_Red = "red"
color_Orange = "orange"
color_Blue = "blue"

# Name/variable used for creating the output File GDB for GIS data creation.
nameFileGDB = "GIS_Output.gdb"

# The current date (__YYYYMMDD) will be attached to the end of most output
# naming conventions.
curDate = "__" + datetime.datetime.today().strftime("%Y%m%d")

# The actual name of the US States shapefile downloaded/utilized from the Census
# Bureau website.
census_URL_CountyShapefile_FileName = "cb_2017_us_county_500k"

# The URL string with combined variables to access the Census Bureau shapefile.
census_URL_CountyShapefile = "http://www2.census.gov/geo/tiger/GENZ2017/shp/" +\
                             census_URL_CountyShapefile_FileName + fileExtZip

# Column header for US state FIPS code found within the Census Bureau shapefile.
census_Shapefile_Field_StateFIPS = "STATEFP"

# Column header for US county names found within the Census Bureau shapefile.
census_Shapefile_Field_CountyName = "NAME"

# Column header for US county names found within the Union between Census
# Shapefile and hurricane line feature class buffers.
census_Shapefile_Field_CountyName_1 = "NAME_1"

# Static output name for the extracted US-and-DC-only polygon feature class.
# This naming convention is used for the Shapefile-to-feature-class conversion.
featureClass_50States_and_DC_only = "USA_50_and_DC_only"

# Column header from hurricane feature class for wind intensity, used as an
# input parameter for the various ArcPy analyses.
analysis_Mag_Field = "wmo_wind"

# Column headers from hurricane feature class for the unique identifier and
# storm name for each system. These will be used during the Output to CSV
# analysis option.
analysis_HurrCode_Field = "Serial_Num"
analysis_HurrName_Field = "Name"

# Column header from hurricane feature class for length of polyline (in meters).
# Used to erase extremely short polylines found within the data.
analysis_Line_Length_Field_InMeters = "Shape_Length"

# These attribute header variables are found within the hurricane feature class.
# They will be later be combined into a single "full_date" field for utilization
# with Custom Timespan choices.
dateField_Year = "year"
dateField_Month = "month"
dateField_Day = "day"

# This is the full_date attribute field that will be added to the hurricane
# feature class. The above date fields will be combined into this field during
# the function for creating/populating the full date.
dateField_FullDate = "full_date"

# Date fields used during an update cursor for populating the aforementioned
# full_date field.
date_fields = [dateField_Year, dateField_Month, dateField_Day,
               dateField_FullDate]

# ArcPy module is imported at this location so as to check for any runtime
# errors (due to internet connectivity issues and/or licensing issues).
# This issue is handled within the GUI_ApplicationDriver.py file.
# If the user chooses to proceed with the application after receiving a
# "Runtime Error", the same error will be ignored/passed within this .py file.
try:

    # If ArcPy available, import it.
    import arcpy

    # Universal parameters for assigning the Projected Coordinate System to the
    # hurricane and polygon feature classes.
    # WGS84 Web Mercator Auxiliary Sphere with -30.0 offset of Central Meridian.
    # These parameters were chosen to fix the extent issues created by Alaska
    # appearing "split". This extent problem was causing issues with some
    # geoprocessing tasks (Spline especially).
    spatialRef = arcpy.SpatialReference()
    # 3857 = WGS_1984_Web_Mercator_Auxiliary_Sphere
    spatialRef.createFromFile(3857)
    spatialRef_3857 = spatialRef.exportToString()
    spatialRef_3857 = \
        spatialRef_3857.replace("PARAMETER['Central_Meridian',0.0]",
                                "PARAMETER['Central_Meridian',-30.0]")
    pcsReference = arcpy.SpatialReference()
    pcsReference.loadFromString(spatialRef_3857)
    pcsReferenceString = "WGS_1984_Web_Mercator_Auxiliary_Sphere"

except RuntimeError:

    # Example: "Not signed into Portal or ArcGIS Pro not installed."

    # If ArcPy not available, skip it.
    # This allows the data to still be downloaded without ArcGIS functionality.
    pass

# Class for the Hurricane Options GUI functionality.
class HurricaneOptions(FrameLifts):

    def __init__(self, *args, **kwargs):
        FrameLifts.__init__(self, *args, **kwargs)

        # Universal parameters used throughout various functions of this class.
        # Setting values to None and later testing for None alleviates potential
        # "Attribute Errors" later on, as some variables will not be used if
        # certain tasks are not needed.
        self.timespan_url = None
        self.intensity_url = None
        self.comboFrame_Custom_Timespan = None
        self.comboFrame_Custom_Intensity = None
        self.custom_intensity_url = None
        self.intCustomTimespan_Year_From = None
        self.intCustomTimespan_Year_To = None
        self.intCustomTimespan_Month_From = None
        self.intCustomTimespan_Month_To = None
        self.intCustom_Intensity_Min = None
        self.intCustom_Intensity_Max = None
        self.textCustomIntensityFrom = None
        self.textCustomIntensityTo = None
        self.custom_Intensity_Naming = None
        self.customSelection_Height = None
        self.folderDialogPath = None
        self.analysisOptionsFrame = None
        self.scrollBoxFrame = None
        self.progressBarFrame = None
        self.radioButton_Selection = None
        self.subFolder_GIS = None
        self.comboFrame_State = None
        self.comboFrame_Counties = None
        self.combo_State_Name = None
        self.combo_County_Name = None
        self.stringState_Name = None
        self.stringCounty_Name = None
        self.nameFeatureClass_FromCSV = None
        self.unzipped_Hurr_RawShapefileName = None
        self.name_Hurr_FeatureClass = None
        self.worldwide_storm_count = None
        self.nationwide_storm_count = None
        self.state_storm_count = None
        self.county_storm_count = None

        # Settings and configuration for the Hurricane Options GUI window.
        self.winfo_toplevel().title("Hurricane Options")
        self.winfo_toplevel().geometry("%dx%d" %
                                       (guiWindow_HurricaneOptions_Width,
                                        guiWindow_HurricaneOptions_Height))

        # The GUI frame that all child frames will be placed.
        self.winFrame = tkinter.Frame(self.winfo_toplevel())
        self.winFrame.grid(
            column=0, row=0, padx=0, pady=0, columnspan=2, sticky=tkinter.NW)

        # Frame that displays the initial Hurricane dialog layout.
        self.initialFrame = tkinter.Frame(self.winFrame)
        self.initialFrame.grid(column=0, row=0, sticky=tkinter.NW)

        # Frame that displays the additional options if the user selects the
        # "More Options" checkbox.
        self.optionsFrame = tkinter.Frame(self.winFrame)
        self.optionsFrame.grid(column=1, row=0, columnspan=2, sticky=tkinter.NW)

        # Frame that displays the scrolled text box and progress bar after a
        # user clicks the OK button.
        self.processingFrame = tkinter.Frame(self.winFrame)
        self.processingFrame.grid(
            column=0, row=1, columnspan=2, sticky=tkinter.SW)

        # Executes the function controlling the Timespan/Intensity comboboxes
        self.func_ComboFrame()

        # Executes the function controlling the URL display text functionality.
        self.func_URLFrame()

        # Executes the function controlling the Workspace Folder dialog/text.
        self.func_WorkspaceFolderFrame()

        # Executes the function controlling the Exit/Back/OK buttons.
        self.func_ButtonFrame()

    def func_ComboFrame(self):

        # This function controls the display of the combobox frame.

        # Widget frame housing the combobox items for Timespan/Intensity.
        self.comboFrame = tkinter.Frame(self.initialFrame)
        self.comboFrame.grid(column=0, row=0, padx=40, pady=5, sticky=tkinter.W)

        # Label for Timespan combobox with Central Standard Time (CST).
        comboLabel_Timespan = ttk.Label(self.comboFrame, text="Timespan (UTC):")
        comboLabel_Timespan.grid(column=0, row=0, sticky=tkinter.W)

        # Label for Intensity combobox.
        comboLabel_Intensity = ttk.Label(self.comboFrame,
                                        text="Intensity:")
        comboLabel_Intensity.grid(column=2, row=0, sticky=tkinter.W)

        # Combobox requirements for Timespan.
        self.stringHurricaneTimespan = tkinter.StringVar()
        self.combo_HurricaneTimespan = ttk.Combobox(self.comboFrame, width=13,
                                    textvariable=self.stringHurricaneTimespan,
                                    state="readonly")
        self.combo_HurricaneTimespan["values"] = (textCombo_HurricaneTimespan)
        self.combo_HurricaneTimespan.grid(column=0, row=1, sticky=tkinter.W)

        # GIF icon to symbolize Hurricane within the GUI.
        dirFolder = os.path.dirname(__file__)
        gifPath = os.path.join(dirFolder, "Icon_Hurricane.gif")
        self.photo_Hurricane_Icon = \
            tkinter.PhotoImage(file=gifPath)
        colorCode_Black = "black"
        self.subSampleImage = self.photo_Hurricane_Icon.subsample(4, 4)
        self.label_for_icon = ttk.Label(self.comboFrame, borderwidth=2,
                                        relief="solid",
                                        background=colorCode_Black,
                                        image=self.subSampleImage)
        self.label_for_icon.photo = self.photo_Hurricane_Icon
        self.label_for_icon.grid(column=1, row=0, padx=0,
                                 pady=5, sticky=tkinter.EW, rowspan=2)

        # Combobox requirements for Intensity.
        self.stringHurricaneIntensity = tkinter.StringVar()
        self.combo_HurricaneIntensity = ttk.Combobox(self.comboFrame, width=12,
                                    textvariable=self.stringHurricaneIntensity,
                                    state="readonly")
        self.combo_HurricaneIntensity["values"] = \
            (textCombo_HurricaneIntensity)
        self.combo_HurricaneIntensity.grid(column=2, row=1, sticky=tkinter.W)

        # Combobox selection binding that will be used to populate URL Field.
        self.combo_HurricaneTimespan.bind("<<ComboboxSelected>>",
                                     self.func_PopulateURLField_Timespan)

        # Combobox selection binding that will be used to populate URL Field.
        self.combo_HurricaneIntensity.bind("<<ComboboxSelected>>",
                                     self.func_PopulateURLField_Intensity)

        # For all items in the comboFrame, configure their grids the same way.
        for child in self.comboFrame.winfo_children():

            child.grid_configure(padx=25, pady=1)

        # Display first index for Timespan (Select...).
        self.combo_HurricaneTimespan.current(0)

        # Display first index for Intensity (Select...).
        self.combo_HurricaneIntensity.current(0)

    def func_ComboCustomTimespan(self):

        # This function controls the display of the custom combobox frame
        # controlling the custom Timespan.

        # If the custom timespan combobox frame already exists (is visible)...
        if self.comboFrame_Custom_Timespan is not None:
            # Remove the frame.
            self.comboFrame_Custom_Timespan.grid_remove()

        # Widget frame for custom timespan.
        self.comboFrame_Custom_Timespan = tkinter.Frame(self.initialFrame)
        self.comboFrame_Custom_Timespan.grid(column=0, row=1, padx=10, pady=5,
                                             sticky=tkinter.W)

        # Label frame for the FROM custom timespan comboboxes.
        self.comboLabelFrameCustomTimespan_From = \
            ttk.LabelFrame(self.comboFrame_Custom_Timespan, text="From:",
                           labelanchor=tkinter.N)
        self.comboLabelFrameCustomTimespan_From.grid(column=0, row=0, padx=5,
                                                     pady=5, sticky=tkinter.W)

        # Label for YEAR FROM combobox.
        comboLabel_CustomTimespan_Year_From = ttk.Label(
            self.comboLabelFrameCustomTimespan_From, text="Year:")
        comboLabel_CustomTimespan_Year_From.grid(column=0, row=0,
                                                 sticky=tkinter.W)

        # Label for MONTH FROM combobox.
        comboLabel_CustomTimespan_Month_From = \
            ttk.Label(self.comboLabelFrameCustomTimespan_From, text="Month:")
        comboLabel_CustomTimespan_Month_From.grid(column=1, row=0,
                                                  sticky=tkinter.E)

        # Combobox requirements for YEAR FROM.
        self.intCustomTimespan_Year_From = tkinter.IntVar()
        self.combo_CustomTimespan_Year_From = ttk.Combobox(
            self.comboLabelFrameCustomTimespan_From, width=4,
            textvariable=self.intCustomTimespan_Year_From, state="readonly")
        self.combo_CustomTimespan_Year_From["values"] = (intList_Years)
        self.combo_CustomTimespan_Year_From.grid(column=0, row=1,
                                                 sticky=tkinter.W)

        # Combobox requirements for MONTH FROM.
        self.intCustomTimespan_Month_From = tkinter.IntVar()
        self.combo_CustomTimespan_Month_From = \
            ttk.Combobox(self.comboLabelFrameCustomTimespan_From, width=2,
                         textvariable=self.intCustomTimespan_Month_From,
                         state="readonly")
        self.combo_CustomTimespan_Month_From["values"] = (intCombo_Months)
        self.combo_CustomTimespan_Month_From.grid(column=1, row=1,
                                                  sticky=tkinter.E)

        # Label frame for the TO custom timespan comboboxes.
        self.comboLabelFrameCustomTimespan_To = ttk.LabelFrame(
            self.comboFrame_Custom_Timespan, text="To:", labelanchor=tkinter.N)
        self.comboLabelFrameCustomTimespan_To.grid(column=1, row=0, padx=5,
                                                   pady=5, sticky=tkinter.W)

        # Label for YEAR TO combobox.
        comboLabel_CustomTimespan_Year_To = ttk.Label(
            self.comboLabelFrameCustomTimespan_To,
            text="Year:")
        comboLabel_CustomTimespan_Year_To.grid(column=0, row=0,
                                               sticky=tkinter.W)

        # Label for MONTH TO combobox.
        comboLabel_CustomTimespan_Month_To = ttk.Label(
            self.comboLabelFrameCustomTimespan_To,
            text="Month:")
        comboLabel_CustomTimespan_Month_To.grid(column=1, row=0,
                                                sticky=tkinter.E)

        # Combobox requirements for YEAR TO.
        self.intCustomTimespan_Year_To = tkinter.IntVar()
        self.combo_CustomTimespan_Year_To = ttk.Combobox(
            self.comboLabelFrameCustomTimespan_To, width=4,
            textvariable=self.intCustomTimespan_Year_To,
            state="readonly")
        self.combo_CustomTimespan_Year_To["values"] = intList_Years
        self.combo_CustomTimespan_Year_To.grid(column=0, row=1,
                                               sticky=tkinter.W)

        # Combobox requirements for MONTH TO.
        self.intCustomTimespan_Month_To = tkinter.IntVar()
        self.combo_CustomTimespan_Month_To = ttk.Combobox(
            self.comboLabelFrameCustomTimespan_To, width=2,
            textvariable=self.intCustomTimespan_Month_To, state="readonly")
        self.combo_CustomTimespan_Month_To["values"] = intCombo_Months
        self.combo_CustomTimespan_Month_To.grid(column=1, row=1,
                                                sticky=tkinter.E)

        # For all items in the custom comboFrame, configure their grids the
        # same way.
        for child in self.comboFrame_Custom_Timespan.winfo_children():
            child.grid_configure(padx=10, pady=1)

        # Display first index for MONTH FROM (01).
        self.combo_CustomTimespan_Month_From.current(0)

        # Display first index for YEAR FROM (current year).
        self.combo_CustomTimespan_Year_From.current(0)

        # Display first index for MONTH TO (01).
        self.combo_CustomTimespan_Month_To.current(0)

        # Display first index for YEAR TO (current year).
        self.combo_CustomTimespan_Year_To.current(0)

        # Combobox selection binding that will be used to populate URL Field.
        self.combo_CustomTimespan_Year_From.bind("<<ComboboxSelected>>",
                                                 self.func_Set_Custom_Timespan)

        # Combobox selection binding that will be used to populate URL Field.
        self.combo_CustomTimespan_Month_From.bind("<<ComboboxSelected>>",
                                                  self.func_Set_Custom_Timespan)

        # Combobox selection binding that will be used to populate URL Field.
        self.combo_CustomTimespan_Year_To.bind("<<ComboboxSelected>>",
                                               self.func_Set_Custom_Timespan)

        # Combobox selection binding that will be used to populate URL Field.
        self.combo_CustomTimespan_Month_To.bind("<<ComboboxSelected>>",
                                                self.func_Set_Custom_Timespan)

    def func_ComboCustomIntensity(self):

        # This function controls the display of the custom combobox frame
        # controlling the custom Intensity.

        # If the custom intensity combobox frame already exists (is visible)...
        if self.comboFrame_Custom_Intensity is not None:
            # Remove the frame.
            self.comboFrame_Custom_Intensity.grid_remove()

        # Widget frame for custom intensity.
        self.comboFrame_Custom_Intensity = tkinter.Frame(self.initialFrame)
        self.comboFrame_Custom_Intensity.grid(column=0, row=1, padx=60, pady=5,
                                             sticky=tkinter.E)

        # Label frame for the intensity range comboboxes.
        self.comboLabelFrame_Custom_Intensity = ttk.LabelFrame(
            self.comboFrame_Custom_Intensity, text="Range (Knots):",
            labelanchor=tkinter.N)
        self.comboLabelFrame_Custom_Intensity.grid(column=0, row=0, padx=5,
                                                  pady=5, sticky=tkinter.E)

        # Label for MINIMUM intensity.
        comboLabel_Custom_Intensity_Min = ttk.Label(
            self.comboLabelFrame_Custom_Intensity, text="Min:        ")
        comboLabel_Custom_Intensity_Min.grid(column=0, row=0, sticky=tkinter.W)

        # Label for MAXIMUM intensity.
        comboLabel_Custom_Intensity_Max = ttk.Label(
            self.comboLabelFrame_Custom_Intensity, text="Max:")
        comboLabel_Custom_Intensity_Max.grid(column=3, row=0, sticky=tkinter.W)

        # Combobox requirements for MINIMUM intensity.
        self.intCustom_Intensity_Min = tkinter.IntVar()
        self.combo_Custom_Intensity_Min = ttk.Combobox(
            self.comboLabelFrame_Custom_Intensity, width=4,
            textvariable=self.intCustom_Intensity_Min, state="readonly")
        self.combo_Custom_Intensity_Min["values"] = (int_Combo_Speeds)
        self.combo_Custom_Intensity_Min.grid(column=0, row=1, sticky=tkinter.W)

        # Combobox requirements for MAXIMUM intensity.
        self.intCustom_Intensity_Max = tkinter.IntVar()
        self.combo_Custom_Intensity_Max = ttk.Combobox(
            self.comboLabelFrame_Custom_Intensity, width=4,
            textvariable=self.intCustom_Intensity_Max, state="readonly")
        self.combo_Custom_Intensity_Max["values"] = (int_Combo_Speeds)
        self.combo_Custom_Intensity_Max.grid(column=3, row=1, sticky=tkinter.E)

        # For all items in the custom intensity comboFrame, configure their
        # grids the same way.
        for child in self.comboFrame_Custom_Intensity.winfo_children():
            child.grid_configure(padx=10, pady=1)

        # Display first index for MINIMUM wind speed of 0.
        self.combo_Custom_Intensity_Min.current(0)

        # Display last index for MAXIMUM wind speed of 200.
        self.combo_Custom_Intensity_Max.current(20)

        # Combobox selection binding that will be used to populate URL field.
        self.combo_Custom_Intensity_Min.bind("<<ComboboxSelected>>",
                                            self.func_Set_Custom_Intensity)

        # Combobox selection binding that will be used to populate URL field.
        self.combo_Custom_Intensity_Max.bind("<<ComboboxSelected>>",
                                            self.func_Set_Custom_Intensity)

    def func_Set_Custom_Timespan(self, event):

        # This function handles events related to the custom Timespan options
        # that a user selects. Based on those selections, this function will
        # assign values and trigger other actions if necessary.

        try:

            # If the FROM YEAR in custom timespan has a value...
            if self.intCustomTimespan_Year_From.get():

                # Convert/assign the integer value to string.
                self.textCustomYearFrom = \
                    str(self.intCustomTimespan_Year_From.get())

            # If the FROM MONTH in custom timespan has a value...
            if self.intCustomTimespan_Month_From.get():

                # Convert/assign the integer value to string.
                self.textCustomMonthFrom = \
                    str(self.intCustomTimespan_Month_From.get())

            # If the TO YEAR in custom timespan has a value...
            if self.intCustomTimespan_Year_To.get():

                # Convert/assign the integer value to string.
                self.textCustomYearTo = \
                    str(self.intCustomTimespan_Year_To.get())

            # If the TO MONTH in custom timespan has a value...
            if self.intCustomTimespan_Month_To.get():

                # Convert/assign the integer value to string.
                self.textCustomMonthTo = \
                    str(self.intCustomTimespan_Month_To.get())

            # If all combobox parameters for custom timespan exist...
            if self.intCustomTimespan_Year_From is not None and \
                    self.intCustomTimespan_Month_From is not None and \
                    self.intCustomTimespan_Year_To is not None and \
                    self.intCustomTimespan_Month_To is not None:

                # Create the timespan file/folder naming convention with values.
                self.timespan_file_folder_naming = \
                    "_" + self.textCustomYearFrom + \
                    self.textCustomMonthFrom.zfill(2) + \
                    "_to_" + self.textCustomYearTo + \
                    self.textCustomMonthTo.zfill(2)

            # Run the function that checks if GUI window needs to be resized.
            self.func_windowResize()

        except Exception as e:

            # Display error message.
            self.func_Scroll_setOutputText("Error Message: " + str(e) + "\n" +
                                           "Traceback: " +
                                           traceback.format_exc(), color_Red)

    def func_Set_Custom_Intensity(self, event):

        # This function handles events related to the custom Intensity options
        # that a user selects. Based on those selections, this function will
        # assign values and trigger other actions if necessary.

        try:

            # If the custom MINIMUM intensity has a value...
            if str(self.intCustom_Intensity_Min.get()):

                # Convert/assign the int value to string.
                self.textCustomIntensityFrom = str(
                    self.intCustom_Intensity_Min.get())

            # If the custom MAXIMUM intensity has a value...
            if self.intCustom_Intensity_Max.get():

                # Convert/assign the int value to string.
                self.textCustomIntensityTo = str(
                    self.intCustom_Intensity_Max.get())

            # If both combobox parameters for custom intensity exist...
            if self.textCustomIntensityFrom is not None and \
                    self.textCustomIntensityTo is not None:

                pass

            # The combined string with adjustments used for file naming and
            # analyses later on in the script.
            self.custom_Intensity_Naming = \
                self.textCustomIntensityFrom.replace(".", "_") + "_to_" + \
                self.textCustomIntensityTo.replace(".", "_")

            # Run the function that checks if GUI window needs to be resized.
            self.func_windowResize()

        except Exception as e:

            # Display error message.
            self.func_Scroll_setOutputText("Error Message: " + str(e) + "\n" +
                                           "Traceback: " +
                                           traceback.format_exc(), color_Red)

    def func_URLFrame(self):

        # This function controls the display of the URL frame within the GUI.

        # Widget frame for displaying the URL hyperlink text.
        self.urlFrame = tkinter.Frame(self.initialFrame)
        self.urlFrame.grid(column=0, row=2, padx=0, pady=5, sticky=tkinter.W)

        # Label for the URL text box.
        urlLabel_HurricaneURL = ttk.Label(self.urlFrame,
                                     text="URL Download File Link:")
        urlLabel_HurricaneURL.grid(column=0, row=0, padx=20, pady=1,
                              sticky=tkinter.W)

        # Parameters for the URL textbox.
        self.textURLTextbox = tkinter.StringVar()
        self.textURLTextbox.set(urlDialog_Message)
        urlTextbox_HurricaneURL = ttk.Entry(self.urlFrame,
                                       textvariable=self.textURLTextbox,
                                       width=70, state="readonly")
        urlTextbox_HurricaneURL.grid(column=0, row=1, padx=20, pady=0)

    def func_PopulateURLField_Timespan(self, event):

        # This function handles the events where a user selects a timespan
        # option from the combobox. The selection will trigger various responses
        # as detailed below.

        try:

            # If the timespan combobox displays "Select..."...
            if self.stringHurricaneTimespan.get() == "Select...":

                # Clear any variable assignments from the following items.
                self.timespan_url = None

                # Display this generic message within the URL textbox.
                self.textURLTextbox.set(urlDialog_Message)

                # Run function that checks if GUI window needs to be resized.
                self.func_windowResize()

                # If the custom timespan comboboxes exist, remove them from GUI.
                if self.comboFrame_Custom_Timespan is not None:
                    self.comboFrame_Custom_Timespan.grid_remove()

            # If the user selects all hurricane data from combobox...
            elif self.stringHurricaneTimespan.get() == \
                    "All | 1842-" + str(int_OneYearAgo):

                # Assign/clear variables as needed.
                self.timespan_url = "Allstorms"

                # Set the URL text of non custom timespan/intensity values.
                self.text_Hurricane_URL = hurr_All_siteURL + \
                                          self.timespan_url + ibtracs + \
                                          lineVersion + fileExtZip

                self.unzipped_Hurr_RawShapefileName = self.timespan_url + \
                                                      ibtracs + lineVersion

                if self.stringHurricaneIntensity.get() != "Select...":

                    self.textURLTextbox.set(self.text_Hurricane_URL)

                # Run function that checks if GUI window needs to be resized.
                self.func_windowResize()

                # If the custom timespan comboboxes exist, remove them from GUI.
                if self.comboFrame_Custom_Timespan is not None:

                    self.comboFrame_Custom_Timespan.grid_remove()

            # If the user selects "Custom..." from the combobox...
            elif self.stringHurricaneTimespan.get() == "Custom...":

                # Assign/clear variables as needed.
                self.timespan_url = "Allstorms"

                # Set the URL text of timespan values.
                self.text_Hurricane_URL = hurr_All_siteURL + \
                                          self.timespan_url + ibtracs + \
                                          lineVersion + fileExtZip

                self.unzipped_Hurr_RawShapefileName = self.timespan_url + \
                                                      ibtracs + lineVersion

                if self.stringHurricaneIntensity.get() != "Select...":

                    self.textURLTextbox.set(self.text_Hurricane_URL)

                # Run function that checks if GUI window needs to be resized.
                self.func_windowResize()

                # Run the function that controls the custom timespan combobox.
                self.func_ComboCustomTimespan()

                # Run the function that sets the custom timespan variables.
                self.func_Set_Custom_Timespan(event)

            # If the user selects any option aside from Select, All, or Custom..
            elif self.stringHurricaneTimespan.get():

                # Assign/clear variables as needed.
                self.timespan_url = str(self.stringHurricaneTimespan.get())

                # Set the URL text of timespan values.
                self.text_Hurricane_URL = hurr_YYYY_siteURL + yearDot + \
                                          self.timespan_url + ibtracs + \
                                          lineVersion + fileExtZip

                self.unzipped_Hurr_RawShapefileName = yearDot + \
                                          self.timespan_url + ibtracs + \
                                          lineVersion

                if self.stringHurricaneIntensity.get() != "Select...":

                    self.textURLTextbox.set(self.text_Hurricane_URL)

                # Run function that checks if GUI window needs to be resized.
                self.func_windowResize()

                # If the custom timespan comboboxes exist, remove them from GUI.
                if self.comboFrame_Custom_Timespan is not None:

                    self.comboFrame_Custom_Timespan.grid_remove()

        except Exception as e:

            # Display error message.
            self.func_Scroll_setOutputText("Error Message: " + str(e) + "\n" +
                                           "Traceback: " +
                                           traceback.format_exc(), color_Red)

    def func_PopulateURLField_Intensity(self, event):

        # This function handles the events where a user selects a intensity
        # option from the combobox. The selection will trigger various responses
        # as detailed below.

        # If the intensity combobox displays "Select..."...
        if self.stringHurricaneIntensity.get() == "Select...":

            # Clear any variable assignments from the following items.
            self.intensity_url = None
            self.mag_naming = None

            # Display this generic message within the URL textbox.
            self.textURLTextbox.set(urlDialog_Message)

            # Run the function that checks if GUI window needs to be resized.
            self.func_windowResize()

            # If the custom intensity comboboxes exist, remove them from GUI.
            if self.comboFrame_Custom_Intensity is not None:

                self.comboFrame_Custom_Intensity.grid_remove()

        # If the user selects "All" from the combobox...
        elif self.stringHurricaneIntensity.get() == "All":

            # Assign/clear variables as needed.
            self.mag_naming = "all"
            self.custom_intensity_url = None

            if self.stringHurricaneTimespan.get() != "Select...":

                self.textURLTextbox.set(self.text_Hurricane_URL)

            # Run the function that checks if GUI window needs to be resized.
            self.func_windowResize()

            # If the custom intensity comboboxes exist, remove them from GUI.
            if self.comboFrame_Custom_Intensity is not None:

                self.comboFrame_Custom_Intensity.grid_remove()

        # If the user selects Tropical Depression from the combobox...
        elif self.stringHurricaneIntensity.get() == "Trop. Depression":

            # Assign/clear variables as needed.
            self.mag_naming = "td"
            self.custom_intensity_url = None

            if self.stringHurricaneTimespan.get() != "Select...":

                self.textURLTextbox.set(self.text_Hurricane_URL)

            # Run the function that checks if GUI window needs to be resized.
            self.func_windowResize()

            # If the custom intensity comboboxes exist, remove them from GUI.
            if self.comboFrame_Custom_Intensity is not None:

                self.comboFrame_Custom_Intensity.grid_remove()

        # If the user selects Tropical Storm from the combobox...
        elif self.stringHurricaneIntensity.get() == "Trop. Storm":

            # Assign/clear variables as needed.
            self.mag_naming = "ts"
            self.custom_intensity_url = None

            if self.stringHurricaneTimespan.get() != "Select...":

                self.textURLTextbox.set(self.text_Hurricane_URL)

            # Run the function that checks if GUI window needs to be resized.
            self.func_windowResize()

            # If the custom intensity comboboxes exist, remove them from GUI.
            if self.comboFrame_Custom_Intensity is not None:

                self.comboFrame_Custom_Intensity.grid_remove()

        # If the user selects Category 1 from the combobox...
        elif self.stringHurricaneIntensity.get() == "Cat. 1":

            # Assign/clear variables as needed.
            self.mag_naming = "cat1"
            self.custom_intensity_url = None

            if self.stringHurricaneTimespan.get() != "Select...":

                self.textURLTextbox.set(self.text_Hurricane_URL)

            # Run the function that checks if GUI window needs to be resized.
            self.func_windowResize()

            # If the custom intensity comboboxes exist, remove them from GUI.
            if self.comboFrame_Custom_Intensity is not None:

                self.comboFrame_Custom_Intensity.grid_remove()

        # If the user selects Category 2 from the combobox...
        elif self.stringHurricaneIntensity.get() == "Cat. 2":

            # Assign/clear variables as needed.
            self.mag_naming = "cat2"
            self.custom_intensity_url = None

            if self.stringHurricaneTimespan.get() != "Select...":

                self.textURLTextbox.set(self.text_Hurricane_URL)

            # Run the function that checks if GUI window needs to be resized.
            self.func_windowResize()

            # If the custom intensity comboboxes exist, remove them from GUI.
            if self.comboFrame_Custom_Intensity is not None:

                self.comboFrame_Custom_Intensity.grid_remove()

        # If the user selects Category 3 from the combobox...
        elif self.stringHurricaneIntensity.get() == "Cat. 3":

            # Assign/clear variables as needed.
            self.mag_naming = "cat3"
            self.custom_intensity_url = None

            if self.stringHurricaneTimespan.get() != "Select...":

                self.textURLTextbox.set(self.text_Hurricane_URL)

            # Run the function that checks if GUI window needs to be resized.
            self.func_windowResize()

            # If the custom intensity comboboxes exist, remove them from GUI.
            if self.comboFrame_Custom_Intensity is not None:

                self.comboFrame_Custom_Intensity.grid_remove()

        # If the user selects Category 4 from the combobox...
        elif self.stringHurricaneIntensity.get() == "Cat. 4":

            # Assign/clear variables as needed.
            self.mag_naming = "cat4"
            self.custom_intensity_url = None

            if self.stringHurricaneTimespan.get() != "Select...":

                self.textURLTextbox.set(self.text_Hurricane_URL)

            # Run the function that checks if GUI window needs to be resized.
            self.func_windowResize()

            # If the custom intensity comboboxes exist, remove them from GUI.
            if self.comboFrame_Custom_Intensity is not None:

                self.comboFrame_Custom_Intensity.grid_remove()

        # If the user selects Category 5 from the combobox...
        elif self.stringHurricaneIntensity.get() == "Cat. 5":

            # Assign/clear variables as needed.
            self.mag_naming = "cat5"
            self.custom_intensity_url = None

            if self.stringHurricaneTimespan.get() != "Select...":

                self.textURLTextbox.set(self.text_Hurricane_URL)

            # Run the function that checks if GUI window needs to be resized.
            self.func_windowResize()

            # If the custom intensity comboboxes exist, remove them from GUI.
            if self.comboFrame_Custom_Intensity is not None:

                self.comboFrame_Custom_Intensity.grid_remove()

        # If the user selects "Custom..." from the combobox...
        elif self.stringHurricaneIntensity.get() == "Custom...":

            # Assign/clear variables as needed.
            # Custom hurricane intensity will default to All, as all data is
            # initially downloaded.
            self.mag_naming = "all"

            if self.stringHurricaneTimespan.get() != "Select...":

                self.textURLTextbox.set(self.text_Hurricane_URL)

            # Run the function that checks if GUI window needs to be resized.
            self.func_windowResize()

            # Run the function that controls the display of the custom
            # intensity comboboxes.
            self.func_ComboCustomIntensity()

            # Run the function that sets the custom intensity variables.
            self.func_Set_Custom_Intensity(event)

    def func_WorkspaceFolderFrame(self):

        # The following function controls the workspace folder frame within the
        # GUI.

        # Widget frame for the workspace folder assignment.
        self.workspaceFolderFrame = tkinter.Frame(self.initialFrame)
        self.workspaceFolderFrame.grid(column=0, row=3, padx=0, pady=5,
                                       sticky=tkinter.W)

        # Label for the assigned workspace.
        workspaceFolderLabel_FolderDialog = ttk.Label(self.workspaceFolderFrame,
                                                      text="Set Workspace:")
        workspaceFolderLabel_FolderDialog.grid(column=0, row=0, padx=20, pady=1)

        # Browse button for the user to select an output folder location.
        self.workspaceFolderButton_FolderDialog = \
            ttk.Button(self.workspaceFolderFrame, text="Browse...",
                       command=self.func_FolderDialog)
        self.workspaceFolderButton_FolderDialog.grid(column=0, row=1, padx=20,
                                                     pady=0, sticky=tkinter.EW)

        # Variables for the folder location to display within a GUI textbox.
        self.textWorkspaceDialogPath = tkinter.StringVar()
        self.textWorkspaceDialogPath.set(folderDialog_Message)
        self.workspaceFolderTextbox_HurricaneFolderDialog = \
            ttk.Entry(self.workspaceFolderFrame,
                      textvariable=self.textWorkspaceDialogPath, width=52,
                      state="readonly")
        self.workspaceFolderTextbox_HurricaneFolderDialog.grid(column=1,
                                                          row=1, padx=0, pady=0,
                                                          sticky=tkinter.W)

    def func_FolderDialog(self):

        # This function controls the assignment of the output file directory
        # via the "Browse..." button.

        # First, the function checks to see if the window needs to be re-sized.
        # The re-size will occur if the Scrollbox and Progressbar are visible.
        self.func_windowResize()

        # Once the "Browse..." button is clicked, the user will be prompted to
        # select an output workspace.
        self.folderDialogPath = \
            filedialog.askdirectory(parent=self.workspaceFolderFrame)

        # If the user clicks Cancel, folderDialogPath becomes an empty string
        # and does not assign a valid workspace.
        if self.folderDialogPath == "":

            # This will cause the workspace text to automatically reset to the
            # original generic message.
            self.textWorkspaceDialogPath.set(folderDialog_Message)

        else:
            # Otherwise, the workspace will be set and display for the user.
            self.textWorkspaceDialogPath.set(self.folderDialogPath)

    def func_ButtonFrame(self):

        # This function controls the laytout of the Exit/Cancel, Back, and OK
        # buttons, as well as the "More Options" checkbox.

        # Button frame for housing all of the buttons.
        self.buttonFrame = tkinter.Frame(self.initialFrame)
        self.buttonFrame.grid(column=0, row=4, padx=0, pady=20,
                              sticky=tkinter.NSEW)

        # Exit button.
        self.buttonExitCancel = ttk.Button(self.buttonFrame, text="Exit",
                                           command=self.func_Exit_Cancel_Click)
        self.buttonExitCancel.grid(column=0, row=0, padx=40, pady=0,
                                   sticky=tkinter.W)

        # Back button.
        self.buttonBack = ttk.Button(self.buttonFrame, text="Back",
                                     command=self.func_BackClick)
        self.buttonBack.grid(column=3, row=0, padx=5, pady=0, sticky=tkinter.E)

        # OK button.
        self.buttonOK = ttk.Button(self.buttonFrame, text="OK",
                                   command=self.func_OKClick_Thread)
        self.buttonOK.grid(column=4, row=0, padx=5, pady=0, sticky=tkinter.E)

        # Variables for the "More Options" checkbox.
        self.statusVar_Checkbutton_Options = tkinter.IntVar()
        self.checkboxOptions = tkinter.Checkbutton(self.buttonFrame,
                                    text="More Options",
                                    variable=self.statusVar_Checkbutton_Options,
                                    command=self.func_CheckboxOptions)
        self.checkboxOptions.grid(column=5, row=0, padx=15, pady=0,
                                  sticky=tkinter.E)
        self.checkboxOptions.deselect()

    def func_BackClick(self):

        # This function controls what happens when the Back button is clicked.

        # The previous screen (to select hazard type appears).
        from GUI_ApplicationDriver import AppDriver
        appDrive = AppDriver(self.winfo_toplevel())
        appDrive.place(in_=self.winfo_toplevel(), x=0, y=0, relwidth=1,
                       relheight=1)
        appDrive.lift()

    def func_Exit_Cancel_Click(self):

        # This function controls what happens when the Exit/Cancel button is
        # clicked.

        # If the user clicks the Exit button...
        if self.buttonExitCancel["text"] == "Exit":
            # Exit/Terminate the program.
            self.quit()
            self.destroy()
            sys.exit(0)

        # If the user clicks the Cancel button after clicking OK...
        if self.buttonExitCancel["text"] == "Cancel":

            # Yes/No Messagebox warning message, verifying the user's choice.
            userSelection = messagebox.askyesno("Are you sure?",
                            "Are you sure you want to cancel?\n" +
                            "This will terminate any unfinished processes and "
                            "exit the program.", icon=messagebox.WARNING)

            # If user selects Yes...
            if userSelection == True:

                # Immediately terminate all processes and exit the program.
                self.quit()
                self.destroy()
                sys.exit(0)

            else:

                # If the user selects No, then do nothing and return to the
                # active program.
                return

    def func_OKClick_Thread(self):

        # This function controls the OKClick function, by running it within a
        # threaded environment. This prevents the GUI from freezing, and allows
        # for the processing messages and progress bar to provide live updates.
        # The daemon setting allows for the application to properly terminate
        # when the user clicks the "Cancel" button.

        self.thread_func_OKClick = Thread(target=self.func_OKClick)
        self.thread_func_OKClick.daemon = True
        self.thread_func_OKClick.start()

        # Disable all GUI selectable items except the "Cancel" button after
        # starting.
        self.func_Disable_Buttons()

    def func_OKClick(self):

        # This function controls what occurs once the user clicks the OK button.

        try:

            # GUI height expansion if no Custom comboboxes have been selected.
            self.okClick_NonCustom_ExpansionHeight = \
                guiWindow_HurricaneOptions_Height + 200

            # If a custom timespan or custom intensity has been selected...
            if self.customSelection_Height is not None:

                # Expand the height of the GUI to accomodate the Custom
                # timespan/intensity height, plus the processing messages and
                # progress bar.
                self.okClick_Custom_ExpansionHeight = \
                    self.customSelection_Height + 200

            # If the scroll box (for processing messages) already exists,
            # remove it.
            if self.scrollBoxFrame is not None:

                self.scrollBoxFrame.grid_remove()

            # If the progress bar already exists, remove it.
            if self.progressBarFrame is not None:

                self.progressBarFrame.grid_remove()

            # If the user has selected a valid timespan, intensity, and assigned
            # an output workspace folder...
            if self.stringHurricaneTimespan.get() != "Select..." and \
                    self.stringHurricaneIntensity.get() != "Select..." and \
                    self.workspaceFolderTextbox_HurricaneFolderDialog.get() != \
                    folderDialog_Message:

                # Start a timer for the script.
                self.start_time = time.time()

                # If the "Options" checkbox is selected...
                if self.statusVar_Checkbutton_Options.get() == 1:

                    # If the user hasn't selected a clipping option...
                    if self.radioButton_Selection is None:

                        # Display error message.
                        messagebox.showerror(errorMessage_Header,
                                        message="Error in Clipping Options.\n" +
                                        "A clipping option must be selected.")

                        # Re-enable all selectable items in the GUI.
                        self.func_Enable_Buttons()

                        # Exit the function.
                        return

                    # If the timespan or intensity combobox is "Custom..."...
                    if self.stringHurricaneTimespan.get() == "Custom..." or \
                            self.stringHurricaneIntensity.get() == "Custom...":

                        # If all custom timespan comboboxes have values...
                        if self.intCustomTimespan_Year_From is not None and \
                            self.intCustomTimespan_Year_To is not None and \
                            self.intCustomTimespan_Month_From is not None and \
                            self.intCustomTimespan_Month_To is not None:

                            # If the YEAR FROM exceeds the YEAR TO value...
                            if self.intCustomTimespan_Year_From.get() > \
                                    self.intCustomTimespan_Year_To.get():

                                # Display error message.
                                messagebox.showerror(errorMessage_Header,
                                        message="Invalid timespan entry.\n" +
                                        "From date exceeds To date.")

                                # Re-enable all selectable items in the GUI.
                                self.func_Enable_Buttons()

                                # Exit the function.
                                return

                            # Else if the FROM MONTH exceeds the TO MONTH within
                            # the same YEAR...
                            elif self.intCustomTimespan_Year_From.get() == \
                                    self.intCustomTimespan_Year_To.get() and \
                                    self.intCustomTimespan_Month_From.get() > \
                                    self.intCustomTimespan_Month_To.get():

                                # Display error message.
                                messagebox.showerror(errorMessage_Header,
                                        message="Invalid timespan entry.\n" +
                                        "From date exceeds To date.")

                                # Re-enable all selectable items in the GUI.
                                self.func_Enable_Buttons()

                                # Exit the function.
                                return

                        # If the custom minimum intensity and the custom
                        # maximum intensity comboboxes have values...
                        if self.intCustom_Intensity_Min is not None and \
                                self.intCustom_Intensity_Max is not None:

                            # If the minimum intensity exceeds the maximum
                            # intensity...
                            if self.intCustom_Intensity_Min.get() > \
                                    self.intCustom_Intensity_Max.get():

                                # Display error message.
                                messagebox.showerror(errorMessage_Header,
                                message="Invalid intensity entry.\n" +
                                "Minimum intensity exceeds Maximum intensity.")

                                # Re-enable all selectable items in the GUI.
                                self.func_Enable_Buttons()

                                # Exit the function.
                                return

                        # If no errors have occurred, adjust the GUI dimensions
                        # as assigned.
                        self.winfo_toplevel().geometry(
                            "%dx%d" % (self.checkboxExpansionWidth,
                                       self.okClick_Custom_ExpansionHeight))

                    else:

                        # If no "Custom..." comboboxes have been selected, and
                        # no errors thrown, adjust the GUI dimensions as
                        # assigned.
                        self.winfo_toplevel().geometry("%dx%d" % (
                            self.checkboxExpansionWidth,
                            self.okClick_NonCustom_ExpansionHeight))

                # Else if the "More Options" checkbox is not selected...
                elif self.statusVar_Checkbutton_Options.get() == 0:

                    # If the timespan or intensity "Custom..." comboboxes are
                    # selected...
                    if self.stringHurricaneTimespan.get() == "Custom..." or \
                            self.stringHurricaneIntensity.get() == "Custom...":

                        # If all custom timespan comboboxes have values...
                        if self.intCustomTimespan_Year_From is not None and \
                            self.intCustomTimespan_Year_To is not None and \
                            self.intCustomTimespan_Month_From is not None and \
                            self.intCustomTimespan_Month_To is not None:

                            # If the YEAR FROM exceeds the YEAR TO value...
                            if self.intCustomTimespan_Year_From.get() > \
                                    self.intCustomTimespan_Year_To.get():

                                # Display error message.
                                messagebox.showerror(errorMessage_Header,
                                        message="Invalid timespan entry.\n" +
                                        "From date exceeds To date.")

                                # Re-enable all selectable items in the GUI.
                                self.func_Enable_Buttons()

                                # Exit the function.
                                return

                            # Else if the FROM MONTH exceeds the TO MONTH within
                            # the same YEAR...
                            elif self.intCustomTimespan_Year_From.get() == \
                                    self.intCustomTimespan_Year_To.get() and \
                                    self.intCustomTimespan_Month_From.get() > \
                                    self.intCustomTimespan_Month_To.get():

                                # Display error message.
                                messagebox.showerror(errorMessage_Header,
                                        message="Invalid timespan entry.\n" +
                                        "From date exceeds To date.")

                                # Re-enable all selectable items in the GUI.
                                self.func_Enable_Buttons()

                                # Exit the function.
                                return

                        # If both the minimum and maximum intensity comboboxes
                        # have values...
                        if self.intCustom_Intensity_Min is not None and \
                                self.intCustom_Intensity_Max is not None:

                            # If the MINIMUM intensity exceeds the MAXIMUM
                            # intensity...
                            if self.intCustom_Intensity_Min.get() > \
                                    self.intCustom_Intensity_Max.get():

                                # Display error message.
                                messagebox.showerror(errorMessage_Header,
                                message="Invalid intensity entry.\n" +
                                "Minimum intensity exceeds Maximum intensity.")

                                # Re-enable all selectable items in the GUI.
                                self.func_Enable_Buttons()

                                # Exit the function.
                                return

                        # If no errors have occurred, adjust the GUI dimensions
                        # as assigned.
                        self.winfo_toplevel().geometry("%dx%d" % (
                            guiWindow_HurricaneOptions_Width,
                            self.okClick_Custom_ExpansionHeight))

                    else:

                        # If no "Custom..." comboboxes have been selected, and
                        # no errors thrown, adjust the GUI dimensions as
                        # assigned.
                        self.winfo_toplevel().geometry("%dx%d" % (
                            guiWindow_HurricaneOptions_Width,
                            self.okClick_NonCustom_ExpansionHeight))

                # If no errors encountered, continue executing the following
                # functions...

                # Run function to activate the scrolled text processing frame.
                self.func_ScrolledTextProcessingFrame()

                # Run function to activate the progress bar frame.
                self.func_ProgressBarFrame()

                # Disable all user-selectable items within the GUI.
                self.func_Disable_Buttons()

                # Run function to start the status bar.
                self.func_StartStatusBar()

                # Run function to create a folder in the user-specified output
                # workspace folder.
                # PLEASE NOTE:
                # Numerous subtasks are executed within this function.
                self.func_CreateFolder()

                # Once all tasks are completed, this function will calculate the
                # time it took for the script to run from start to finish.
                self.func_Calculate_Script_Time()

                # This function will attempt to take all of the text from the
                # scrolled text box and save it to a text file within the
                # user-defined output workspace folder.
                self.func_Scroll_saveOutputText()

                # Re-enable all user-selectable items within the GUI.
                self.func_Enable_Buttons()

                # Run function to stop the status bar.
                self.func_StopStatusBar()

                # Ensure progressbar displays 100%, as the script is now done.
                self.func_ProgressBar_setProgress(100)

            else:

                # If the timespan combobox shows "Select..."...
                if self.stringHurricaneTimespan.get() == "Select...":

                    # Display error message.
                    messagebox.showerror(errorMessage_Header,
                                         message="Invalid timespan entry.\n" +
                                            "Please select an option from the "
                                            "drop-down list and try again.")

                    # Re-enable all selectable intems in the GUI.
                    self.func_Enable_Buttons()

                # Else if the intensity combobox shows "Select..."...
                elif self.stringHurricaneIntensity.get() == "Select...":

                    # Display error message.
                    messagebox.showerror(errorMessage_Header,
                                         message="Invalid intensity entry.\n" +
                                            "Please select an option from "
                                            "the drop-down list and try again.")

                    # Re-enable all selectable intems in the GUI.
                    self.func_Enable_Buttons()

                # Else if the output workspace text is the default message...
                elif self.workspaceFolderTextbox_HurricaneFolderDialog.get() ==\
                                folderDialog_Message:

                    # Display error message.
                    messagebox.showerror(errorMessage_Header,
                                message="Output folder path not specified.\n" +
                                "Please try again.")

                    # Re-enable all selectable intems in the GUI.
                    self.func_Enable_Buttons()

        except Exception as e:

            # Display error message.
            self.func_Scroll_setOutputText("Error Message: " + str(e) + "\n" +
                                           "Traceback: " +
                                           traceback.format_exc(), color_Red)

            # Re-enable all user-selectable options.
            self.func_Enable_Buttons()

            # Stop the status bar.
            self.func_StopStatusBar()

            # Increment progress bar to 100 percent.
            self.func_ProgressBar_setProgress(100)

            # Calculate total script processing time.
            self.func_Calculate_Script_Time()

            # Output scroll text to file.
            self.func_Scroll_saveOutputText()

            # Exit the application's task.
            exit()

    def func_ScrolledTextProcessingFrame(self):

        # This function controls the scrolled text processing frame properties
        # within the GUI.

        # Frame for the scrolled text.
        self.scrollBoxFrame = tkinter.Frame(self.processingFrame)

        # Set the scroll height at 8 lines.
        self.scrollHeight = 8

        # If the "More Options" checkbox is selected...
        if self.statusVar_Checkbutton_Options.get() == 1:
            # Set the scrolled text frame to 90 characters wide.
            self.scrollWidth = 90

            # Set the frame parameters to accommodate the width.
            self.scrollBoxFrame.grid(column=0, row=5, padx=10, pady=5,
                                     columnspan=2)

        # If the "More Options" checkbox is not selected...
        if self.statusVar_Checkbutton_Options.get() == 0:
            # Set the scrolled text frame to 52 characters wide.
            self.scrollWidth = 52

            # Set the frame parameters to accommodate the width.
            self.scrollBoxFrame.grid(column=0, row=5, padx=10, pady=5,
                                     columnspan=1)

        # Scrolledtext box for processing messages to display.
        self.scrollBox = scrolledtext.ScrolledText(self.scrollBoxFrame,
                                                   width=self.scrollWidth,
                                                   height=self.scrollHeight,
                                                   wrap=tkinter.WORD,
                                                   state=tkinter.DISABLED)
        self.scrollBox.grid(column=0, row=0)

        # Sets the text variable to the function for updating the scrolledtext
        # output.
        self.func_Scroll_setOutputText("Beginning assigned tasks...", None)

    def func_ProgressBarFrame(self):

        # This function controls the layout of the progress bar within the GUI.

        # Frame for displaying the progress bar.
        self.progressBarFrame = tkinter.Frame(self.processingFrame)

        # If the "More Options" checkbox is selected...
        if self.statusVar_Checkbutton_Options.get() == 1:
            # Set the pixel width of the progress bar.
            self.progressBar_Length = 740

            # Set the frame parameters to accommodate the width.
            self.progressBarFrame.grid(column=0, row=6, padx=10, pady=5,
                                       columnspan=2)

        # If the "More Options" checkbox is not selected...
        if self.statusVar_Checkbutton_Options.get() == 0:
            # Set the pixel width of the progress bar.
            self.progressBar_Length = 450

            # Set the frame parameters to accommodate the width.
            self.progressBarFrame.grid(column=0, row=6, padx=10, pady=5,
                                       columnspan=1)

        # Status bar showing that the application is running.
        self.statusBar = ttk.Progressbar(self.progressBarFrame,
                                               orient='horizontal',
                                               length=self.progressBar_Length,
                                               mode='determinate')
        self.statusBar.grid(column=0, row=0)

        # Progress bar.
        self.progressBar = ttk.Progressbar(self.progressBarFrame,
                                           orient='horizontal',
                                           length=self.progressBar_Length,
                                           mode='determinate')
        self.progressBar.grid(column=0, row=1)

        # Progress bar starting value.
        self.progressBar["value"] = 0

        # Progress bar maximum value.
        self.progressBar["maximum"] = 100

    def func_RunStatusBar(self):

        # This function controls the appearance of the status bar.

        for i in range(100):
            sleep(0.03)
            self.statusBar["value"] = i  # increment progressbar
            self.statusBar.update()  # have to call update() in loop
        self.statusBar["value"] = 0  # reset/clear progressbar

    def func_StartStatusBar(self):

        # This function starts the status bar.

        self.statusBar.start()

    def func_StopStatusBar(self):

        # This function stops the status bar.

        self.statusBar.stop()

    def func_CheckboxOptions(self):

        # This function controls what happens to the GUI when the "More Options"
        # checkbox is selected/deselected.

        # If the "More Options" checkbox is "checked"...
        if self.statusVar_Checkbutton_Options.get() == 1:

            # Run the window resize function to re-size GUI.
            self.func_windowResize()

            # Run the function to display the Analysis/Clipping Options.
            self.func_AnalysisOptionsFrame()

        else:

            # If the "More Options" checkbox is unchecked, clear the radio
            # button selection, re-size the window, and remove the
            # Analysis/Clipping Options.
            self.radioButton_Selection = None
            self.func_windowResize()
            self.analysisOptionsFrame.grid_remove()

    def func_AnalysisOptionsFrame(self):

        # This function controls the layout of the Analysis/Clipping Options
        # within the GUI.

        # Widget frame for the Analysis Options.
        self.analysisOptionsFrame = tkinter.Frame(self.optionsFrame)
        self.analysisOptionsFrame.grid(column=0, row=0, padx=0, pady=5,
                                       sticky=tkinter.NW)

        # Label frame for the Analysis Options.
        self.analysisOptionsLabelFrame = \
            ttk.LabelFrame(self.analysisOptionsFrame,
                           text="Analysis Options (with Esri defaults)",
                           labelanchor=tkinter.NW)
        self.analysisOptionsLabelFrame.grid(column=0, row=0, padx=0, pady=2,
                                            sticky=tkinter.W, columnspan=3)

        # Label frame for the Clipping Options.
        self.clippingOptionsLabelFrame = \
            ttk.LabelFrame(self.analysisOptionsFrame, text="Clipping Options",
                           labelanchor=tkinter.NW)
        self.clippingOptionsLabelFrame.grid(column=0, row=1, padx=0, pady=0,
                                            sticky=tkinter.W, columnspan=2)

        # Frame for the US clipping option.
        self.clippingOptions_radiobuttonFrame_US = \
            ttk.Frame(self.clippingOptionsLabelFrame)
        self.clippingOptions_radiobuttonFrame_US.grid(column=0, row=0, padx=0,
                                                      pady=0, sticky=tkinter.W)

        # Radio button variables for the USA clipping option.
        self.statusClippingOption = tkinter.IntVar()
        self.radiobuttonClippingOption_US = \
            tkinter.Radiobutton(self.clippingOptions_radiobuttonFrame_US,
                                text="USA", value=1,
                                variable=self.statusClippingOption,
                                command=self.func_RadioButton_Clipping_Command)
        self.radiobuttonClippingOption_US.grid(column=0, row=0, padx=0, pady=0,
                                               sticky=tkinter.W)
        self.radiobuttonClippingOption_US.deselect()

        # Frame for the State clipping option.
        self.clippingOptions_radiobuttonFrame_State = \
            ttk.Frame(self.clippingOptionsLabelFrame)
        self.clippingOptions_radiobuttonFrame_State.grid(column=0, row=1,
                                                         padx=0, pady=0,
                                                         sticky=tkinter.W)

        # Radio button variables for the State clipping option.
        self.radiobuttonClippingOption_State = \
            tkinter.Radiobutton(self.clippingOptions_radiobuttonFrame_State,
                                text="State", value=2,
                                variable=self.statusClippingOption,
                                command=self.func_RadioButton_Clipping_Command)
        self.radiobuttonClippingOption_State.grid(column=0, row=0, padx=0,
                                                  pady=0, sticky=tkinter.W)
        self.radiobuttonClippingOption_State.deselect()

        # Frame for the County clipping option.
        self.clippingOptions_radiobuttonFrame_County = ttk.Frame(
            self.clippingOptionsLabelFrame)
        self.clippingOptions_radiobuttonFrame_County.grid(column=0, row=2,
                                                          padx=0,
                                                          pady=0,
                                                          sticky=tkinter.W)

        # Radio button variables for the County clipping option.
        self.radiobuttonClippingOption_County = \
            tkinter.Radiobutton(self.clippingOptions_radiobuttonFrame_County,
                                text="County", value=3,
                                variable=self.statusClippingOption,
                                command=self.func_RadioButton_Clipping_Command)
        self.radiobuttonClippingOption_County.grid(column=0, row=0, padx=0,
                                                   pady=0, sticky=tkinter.W)
        self.radiobuttonClippingOption_County.deselect()

        # Checkbox variables for the Hot Spot option.
        self.statusAnalysis_HotSpot = tkinter.IntVar()
        self.checkbox_HotSpot = \
            tkinter.Checkbutton(self.analysisOptionsLabelFrame,
                                text="Hot Spot (IDW)",
                                variable=self.statusAnalysis_HotSpot)
        # command=self.func_Controls_For_Analysis_Options)
        self.checkbox_HotSpot.grid(column=0, row=0, padx=0, pady=0,
                                      sticky=tkinter.W)
        self.checkbox_HotSpot.deselect()

        # Checkbox variables for the Kernel Density option.
        self.statusAnalysis_KernelDensity = tkinter.IntVar()
        self.checkbox_KernelDensity = \
            tkinter.Checkbutton(self.analysisOptionsLabelFrame,
                                text="Kernel Dens.",
                                variable=self.statusAnalysis_KernelDensity)
        # command=self.func_Controls_For_Analysis_Options)
        self.checkbox_KernelDensity.grid(column=1, row=0, padx=0, pady=0,
                                         sticky=tkinter.W)
        self.checkbox_KernelDensity.deselect()

        # Checkbox variables for the Line Density option.
        self.statusAnalysis_LineDensity = tkinter.IntVar()
        self.checkbox_LineDensity = \
            tkinter.Checkbutton(self.analysisOptionsLabelFrame,
                                text="Line Dens.",
                                variable=self.statusAnalysis_LineDensity)
        # , command=self.func_Window_Parameters_LineDensity)
        self.checkbox_LineDensity.grid(column=2, row=0, padx=0, pady=0,
                                        sticky=tkinter.W)
        self.checkbox_LineDensity.deselect()

        # Checkbox variables for the Output Count Details to CSV File option.
        self.statusAnalysis_OutputToCSVFile = tkinter.IntVar()
        self.checkbox_OutputToCSVFile = \
            tkinter.Checkbutton(self.analysisOptionsLabelFrame,
                                text="Output Count Details to CSV File",
                                variable=self.statusAnalysis_OutputToCSVFile)
        # command=self.func_Controls_For_Analysis_Options)
        self.checkbox_OutputToCSVFile.grid(column=0, row=1, padx=0, pady=0,
                                           columnspan=3, sticky=tkinter.W)
        self.checkbox_OutputToCSVFile.deselect()

    def func_RadioButton_State_Frame_Options(self):

        # This function controls what occurs when the user selects STATE as the
        # clipping option. If the user selects STATE, a combobox appears with
        # all states (and DC) populated.

        # Frame for State combobox.
        self.comboFrame_State = ttk.Frame(self.clippingOptionsLabelFrame)
        self.comboFrame_State.grid(column=1, row=1, padx=1, pady=1,
                                   sticky=tkinter.W)

        # Combobox variables to display combobox with appropriate values.
        self.stringState_Name = tkinter.StringVar()
        self.combo_State_Name = ttk.Combobox(self.comboFrame_State, width=4,
                                             textvariable=self.stringState_Name,
                                             state="readonly")  # font =
        self.combo_State_Name["values"] = (dictKeys_StateNames)
        self.combo_State_Name.grid(column=0, row=0, padx=5,
                                   sticky=tkinter.W)

        # Display the state at the first index based on state abbreviation (AK).
        self.combo_State_Name.current(0)

        # Bind the user's selection to a function that checks for GUI re-sizing.
        self.combo_State_Name.bind("<<ComboboxSelected>>",
                                   self.func_Check_If_Combobox_Text_Changes)

    def func_RadioButton_County_Frame_Options(self):

        # This function controls what occurs when the user selects COUNTY as the
        # clipping option. If the user selects COUNTY, a combobox appars with
        # all county names affiliated with whatever state is displayed within
        # the STATE combobox.

        # Import all county names associated with each state from a separate
        # dictionary module.
        from GUI_CountiesPerState import dict_state_counties

        # Frame for the county combobox.
        self.comboFrame_Counties = ttk.Frame(self.clippingOptionsLabelFrame)
        self.comboFrame_Counties.grid(column=1, row=2, padx=1, pady=1,
                                      sticky=tkinter.W)

        # Combobox variables for displaying the counties.
        self.stringCounty_Name = tkinter.StringVar()
        self.combo_County_Name = ttk.Combobox(self.comboFrame_Counties,
                                            width=28,
                                            textvariable=self.stringCounty_Name,
                                            state="readonly")  # font =
        self.combo_County_Name["values"] = \
            (dict_state_counties[self.stringState_Name.get()])
        self.combo_County_Name.grid(column=0, row=0, padx=5, sticky=tkinter.W)

        # Display the first county name for the selected state (alphabetical).
        self.combo_County_Name.current(0)

        # Bind the user's selection to a function that checks for GUI re-sizing.
        self.combo_County_Name.bind("<<ComboboxSelected>>",
                                    self.func_Check_If_Combobox_Text_Changes)

        # Bind the user's input to a function that determines which counties to
        # display, depending on which state the user selects.
        self.combo_State_Name.bind("<<ComboboxSelected>>",
                                self.func_Autopopulate_County_Combobox_Choices)

    def func_Check_If_Combobox_Text_Changes(self, event):

        # This function exists to check if the State or County Combobox text
        # field changes after the OK function has iterated. If something does
        # change after an iteration, the Window Resize function will check and
        # see if the scroll box and progress bar should be removed.

        self.func_windowResize()

    def func_Autopopulate_County_Combobox_Choices(self, event):

        # This function exists to auto-populate the County Combobox depending on
        # state choice. If the user changes the state, the counties will update.

        try:

            # Import all county names associated with each state from a separate
            # dictionary module.
            from GUI_CountiesPerState import dict_state_counties

            # Check to see if the GUI window should be re-sized.
            self.func_windowResize()

            # If the user selects the COUNTY radiobutton...
            if self.radioButton_Selection == 3:

                # If the STATE combobox has a value...
                if self.stringState_Name.get():
                    # Populate the counties from the dictionary affiliated with
                    # that state selection.
                    self.combo_County_Name["values"] = (
                        dict_state_counties[self.stringState_Name.get()])

                    # Display county at first index (alphabetical).
                    self.combo_County_Name.current(0)

        except Exception as e:

            # Display error message.
            self.func_Scroll_setOutputText("Error Message: " + str(e) + "\n" +
                                           "Traceback: " +
                                           traceback.format_exc(), color_Red)

    def func_CreateFolder(self):

        # This function controls the creation of the folder where all future
        # processing will be accomplished. This will be saved in the
        # user-specified output folder.
        # PLEASE NOTE:
        # Many sub-functions are attached to this function.

        try:

            # If the "More Options" checkbox is selected...
            if self.statusVar_Checkbutton_Options.get() == 1:

                # If the USA clipping option is selected...
                if self.radioButton_Selection == 1:

                    # Create variable for adding USA and DC Only to folder
                    # naming convention.
                    self.folderNamingAddition = \
                        "_" + featureClass_50States_and_DC_only

                # If the STATE clipping option is selected...
                if self.radioButton_Selection == 2:

                    # Create variable for adding State to folder
                    # naming convention.
                    self.featureClass_State_Selection_Only = \
                        "state_only_" + self.stringState_Name.get()
                    self.folderNamingAddition = \
                        "_" + self.featureClass_State_Selection_Only

                # If the COUNTY clipping option is selected...
                if self.radioButton_Selection == 3:

                    # Create variable for adding State to folder
                    # naming convention.
                    self.featureClass_State_Selection_Only = \
                        "state_only_" + self.stringState_Name.get()

                    # Create modified variable for County name, removing all
                    # instances of special characters or spacing.
                    self.modified_stringCountyName = \
                        self.stringCounty_Name.get(). \
                            replace("'", "").replace("-", ""). \
                            replace(".", "").replace(" ", "")

                    # Full string used for feature class naming purposes.
                    self.featureClass_County_State_Naming = "county_only_" + \
                                        self.modified_stringCountyName + "_" + \
                                        self.stringState_Name.get()

                    # Full string used for folder naming purposes.
                    self.folderNamingAddition = \
                        "_" + self.featureClass_County_State_Naming

                # If both timespan/intensity comboboxes are not "Custom..."...
                if self.stringHurricaneTimespan.get() != "Custom..." and \
                        self.stringHurricaneIntensity.get() != "Custom...":
                    # Assign naming conventions.
                    # (Mag/Timespan/Current Date broken out separately to be
                    # used later on for CSV files, XY Event Layers, and
                    # Feature Class).
                    self.only_Mag_Timespan_CurDate = self.mag_naming + "_" + \
                        str(self.timespan_url).replace("-", "_to_").lower() + \
                        curDate

                    # Full Path Name to be used for output files
                    self.fullPathName = self.folderDialogPath + "/" + noaa + \
                                        "_" + hurr + "_" + \
                                        self.only_Mag_Timespan_CurDate + \
                                        self.folderNamingAddition

                # If timespan combobox is "Custom..." and intensity combobox is
                # not "Custom..."...
                if self.stringHurricaneTimespan.get() == "Custom..." and \
                        self.stringHurricaneIntensity.get() != "Custom...":
                    # Assign naming conventions.
                    # (Mag/Timespan/Current Date broken out separately to be
                    # used later on for CSV files, XY Event Layers, and
                    # Feature Class).
                    self.only_Mag_Timespan_CurDate = self.mag_naming + \
                                    self.timespan_file_folder_naming + curDate

                    # Full Path Name to be used for output files
                    self.fullPathName = self.folderDialogPath + "/" + noaa + \
                                            "_" + hurr + "_" + \
                                            self.only_Mag_Timespan_CurDate + \
                                            self.folderNamingAddition

                # If timespan is "Custom..." and intensity is "Custom..."...
                if self.stringHurricaneTimespan.get() == "Custom..." and \
                        self.stringHurricaneIntensity.get() == "Custom...":

                    # Assign naming conventions.
                    # (Mag/Timespan/Current Date broken out separately to be
                    # used later on for CSV files, XY Event Layers, and
                    # Feature Class).
                    self.only_Mag_Timespan_CurDate = \
                        self.custom_Intensity_Naming + \
                        self.timespan_file_folder_naming + curDate

                    # Full Path Name to be used for output files
                    self.fullPathName = self.folderDialogPath + "/" + noaa + \
                                        "_" + hurr + "_" + \
                                        self.only_Mag_Timespan_CurDate + \
                                        self.folderNamingAddition

                # If timespan is not "Custom..." and intensity is "Custom..."...
                if self.stringHurricaneTimespan.get() != "Custom..." and \
                        self.stringHurricaneIntensity.get() == "Custom...":

                    # Assign naming conventions.
                    # (Mag/Timespan/Current Date broken out separately to be
                    # used later on for CSV files, XY Event Layers, and
                    # Feature Class).
                    self.only_Mag_Timespan_CurDate = \
                        self.custom_Intensity_Naming + "_" + \
                        str(self.timespan_url).replace("-", "_to_").lower() + \
                        curDate

                    # Full Path Name to be used for output files
                    self.fullPathName = self.folderDialogPath + "/" + noaa + \
                                        "_" + hurr + "_" + \
                                        self.only_Mag_Timespan_CurDate + \
                                        self.folderNamingAddition

            # If "More Options" checkbox is unchecked...
            if self.statusVar_Checkbutton_Options.get() == 0:

                # If both timespan/intensity comboboxes are not "Custom"...
                if self.stringHurricaneTimespan.get() != "Custom..." and \
                        self.stringHurricaneIntensity.get() != "Custom...":

                    # Assign naming conventions for output data and folders.
                    # (Mag/Timespan/Current Date broken out separately to be
                    # used later on for CSV files, XY Event Layers, and
                    # Feature Class).
                    self.only_Mag_Timespan_CurDate = self.mag_naming + "_" + \
                        str(self.timespan_url).replace("-", "_to_").lower() + \
                        curDate

                    # Full Path Name to be used for output files
                    self.fullPathName = self.folderDialogPath + "/" + noaa + \
                                        "_" + hurr + "_" + \
                                        self.only_Mag_Timespan_CurDate

                # If timespan combobox is "Custom..." and intensity combobox is
                # not "Custom..."...
                if self.stringHurricaneTimespan.get() == "Custom..." and \
                        self.stringHurricaneIntensity.get() != "Custom...":

                    # Assign naming conventions for output data and folders.
                    # (Mag/Timespan/Current Date broken out separately to be
                    # used later on for CSV files, XY Event Layers, and
                    # Feature Class).
                    self.only_Mag_Timespan_CurDate = self.mag_naming + \
                                    self.timespan_file_folder_naming + curDate

                    # Full Path Name to be used for output files
                    self.fullPathName = self.folderDialogPath + "/" + noaa + \
                                        "_" + hurr + "_" + \
                                        self.only_Mag_Timespan_CurDate

                # If timespan combobox is "Custom..." and intensity combobox is
                # "Custom..."...
                if self.stringHurricaneTimespan.get() == "Custom..." and \
                        self.stringHurricaneIntensity.get() == "Custom...":

                    # Assign naming conventions for output data and folders.
                    # (Mag/Timespan/Current Date broken out separately to be
                    # used later on for CSV files, XY Event Layers, and
                    # Feature Class).
                    self.only_Mag_Timespan_CurDate = \
                        self.custom_Intensity_Naming + \
                        self.timespan_file_folder_naming + curDate

                    # Full Path Name to be used for output files
                    self.fullPathName = self.folderDialogPath + "/" + noaa + \
                                        "_" + hurr + "_" + \
                                        self.only_Mag_Timespan_CurDate

                # If timespan combobox is not "Custom..." and intensity combobox
                # is "Custom..."...
                if self.stringHurricaneTimespan.get() != "Custom..." and \
                        self.stringHurricaneIntensity.get() == "Custom...":

                    # Assign naming conventions for output data and folders.
                    # (Mag/Timespan/Current Date broken out separately to be
                    # used later on for CSV files, XY Event Layers, and
                    # Feature Class).
                    self.only_Mag_Timespan_CurDate = \
                        self.custom_Intensity_Naming + "_" + \
                        str(self.timespan_url).replace("-", "_to_").lower() + \
                        curDate

                    # Full Path Name to be used for output files
                    self.fullPathName = self.folderDialogPath + "/" + noaa + \
                                        "_" + hurr + "_" + \
                                        self.only_Mag_Timespan_CurDate

            # If the folder path already exists...
            if os.path.isdir(self.fullPathName) == True:

                try:

                    self.func_Scroll_setOutputText(
                        "Folder path already exists.", None)

                    self.func_Scroll_setOutputText(
                        "Deleting pre-existing folder.", None)

                    # Pause script for 0.5 seconds.
                    sleep(0.5)

                    # Delete the folder.
                    shutil.rmtree(self.fullPathName)

                    self.func_Scroll_setOutputText(
                        "Pre-existing folder deleted.", None)

                    # Increment progress bar.
                    self.func_ProgressBar_setProgress(3)

                except Exception as e:

                    # Show error message.
                    self.func_Scroll_setOutputText(str(e) + "\n" +
                                                   traceback.format_exc(),
                                                   color_Red)

                    # Re-enable all user-selectable options.
                    self.func_Enable_Buttons()

                    # Stop the status bar.
                    self.func_StopStatusBar()

                    # Increment progress bar to 100 percent.
                    self.func_ProgressBar_setProgress(100)

                    # Calculate total script processing time.
                    self.func_Calculate_Script_Time()

                    # Output scroll text to file.
                    self.func_Scroll_saveOutputText()

                    # Exit the application's task.
                    exit()

            # Pause script for 2.0 seconds.
            sleep(2.0)

            self.func_Scroll_setOutputText("Creating folder path:\n" +
                                           self.fullPathName, None)

            # If the folder doesn't already exist, create it.
            if not os.path.exists(self.fullPathName):

                os.makedirs(self.fullPathName)

                self.func_Scroll_setOutputText("Folder path created.", None)

                # Increment progress bar.
                self.func_ProgressBar_setProgress(6)

            # Once the folder has been created, the function to download the
            # CSV files will start.
            self.func_Download_Zipped_Hurr_Shapefile()

        except Exception as e:

            # Show error message.
            self.func_Scroll_setOutputText("Error Message: " + str(e) + "\n" +
                                           "Traceback: " +
                                           traceback.format_exc(), color_Red)

            # Re-enable all user-selectable options.
            self.func_Enable_Buttons()

            # Stop the status bar.
            self.func_StopStatusBar()

            # Increment progress bar to 100 percent.
            self.func_ProgressBar_setProgress(100)

            # Calculate total script processing time.
            self.func_Calculate_Script_Time()

            # Output scroll text to file.
            self.func_Scroll_saveOutputText()

            # Exit the application's task.
            exit()

    def func_Create_CSV_subFolder(self):

        # This function controls the creation of a CSV subfolder where all
        # downloaded/created CSVs will be stored.

        try:

            # Name and location for the CSV subfolder.
            self.csvDirectory = self.fullPathName + "/CSV_Folder/"

            self.func_Scroll_setOutputText("Creating CSV subfolder.", None)

            # Pause script for 0.5 seconds.
            sleep(0.5)

            # If subfolder doesn't exist, create it.
            if not os.path.exists(self.csvDirectory):

                os.makedirs(self.csvDirectory)

                self.func_Scroll_setOutputText("CSV subfolder created.", None)

        except Exception as e:

            # Show error message.
            self.func_Scroll_setOutputText("Error Message: " + str(e) + "\n" +
                                           "Traceback: " +
                                           traceback.format_exc(), color_Red)

    def func_Create_GIS_subFolder(self):

        # This function controls the creation of a GIS subfolder where all
        # downloaded/created GIS data will be stored.

        try:

            # Name and location for the GIS subfolder.
            self.subFolder_GIS = self.fullPathName + "/GIS_Folder/"

            self.func_Scroll_setOutputText("Creating GIS subfolder.", None)

            # Pause script for 0.5 seconds.
            sleep(0.5)

            # If subfolder doesn't exist, create it.
            if not os.path.exists(self.subFolder_GIS):

                os.makedirs(self.subFolder_GIS)

                self.func_Scroll_setOutputText("GIS subfolder created.", None)

            # Increment progress bar.
            self.func_ProgressBar_setProgress(9)

        except Exception as e:

            # Show error message.
            self.func_Scroll_setOutputText("Error Message: " + str(e) + "\n" +
                                           "Traceback: " +
                                           traceback.format_exc(), color_Red)

    def func_Download_Zipped_Hurr_Shapefile(self):

        # This function controls the downloading of the hurricane Shapefile
        # from the web.

        try:

            # If timespan is not "Custom..."...
            if self.stringHurricaneTimespan.get() != "Custom...":

                # If timespan equals All...
                if self.stringHurricaneTimespan.get() == \
                        "All | 1842-" + str(int_OneYearAgo):

                    # Run function to create GIS subfolder.
                    self.func_Create_GIS_subFolder()

                    try:

                        self.func_Scroll_setOutputText("Downloading:\n" + noaa +
                            "_" + hurr + "_" +
                            str(self.timespan_url).replace("-", "_to_").lower()+
                            curDate + fileExtZip, None)

                        # Retrieve CSV from URL.
                        request.urlretrieve(self.textURLTextbox.get(),
                            self.subFolder_GIS + "/" + noaa + "_" + hurr + "_" +
                            str(self.timespan_url).replace("-", "_to_").lower()+
                            curDate + fileExtZip)

                        self.func_Scroll_setOutputText("Download Complete.",
                                                       None)

                    # If download fails, try one more time (it could have been
                    # a small, temporary network glitch).
                    except:

                        self.func_Scroll_setOutputText(
                            "Download failed, trying again:\n" + noaa +
                            "_" + hurr + "_" +
                            str(self.timespan_url).replace("-", "_to_").lower()+
                            curDate + fileExtZip, color_Orange)

                        sleep(5)

                        # Retrieve CSV from URL.
                        request.urlretrieve(self.textURLTextbox.get(),
                            self.subFolder_GIS + "/" + noaa + "_" + hurr + "_" +
                            str(self.timespan_url).replace("-", "_to_").lower()+
                            curDate + fileExtZip)

                        self.func_Scroll_setOutputText("Download Complete.",
                                                       None)

                    self.func_Scroll_setOutputText("Unzipping " + noaa + "_" +
                        hurr + "_" +
                        str(self.timespan_url).replace("-", "_to_").lower() +
                        curDate + fileExtZip, None)

                    # Unzip the CSV file within the same folder location.
                    unZipThisFile = zipfile.ZipFile(self.subFolder_GIS + "/" +
                        noaa + "_" + hurr + "_" +
                        str(self.timespan_url).replace("-", "_to_").lower() +
                        curDate + fileExtZip, 'r')

                    unZipThisFile.extractall(self.subFolder_GIS)

                    # Close file to prevent locks.
                    unZipThisFile.close()

                    self.func_Scroll_setOutputText("Shapefile unzipped.", None)

                else:

                    # Run function to create GIS subfolder.
                    self.func_Create_GIS_subFolder()

                    try:

                        self.func_Scroll_setOutputText("Downloading:\n" + noaa +
                            "_" + hurr + "_" +
                            str(self.timespan_url).replace("-", "_to_").lower()+
                            curDate, None)

                        # Retrieve CSV from URL.
                        request.urlretrieve(self.textURLTextbox.get(),
                            self.subFolder_GIS + "/" + noaa + "_" + hurr + "_" +
                            str(self.timespan_url).replace("-","_to_").lower() +
                            curDate + fileExtZip)

                        self.func_Scroll_setOutputText("Download Complete.",
                                                       None)

                    # If download fails, try one more time (it could have been
                    # a small, temporary network glitch).
                    except:

                        self.func_Scroll_setOutputText(
                            "Download failed, trying again:\n" + noaa +
                            "_" + hurr + "_" +
                            str(self.timespan_url).replace("-", "_to_").lower()+
                            curDate, color_Orange)

                        sleep(5)

                        # Retrieve CSV from URL.
                        request.urlretrieve(self.textURLTextbox.get(),
                            self.subFolder_GIS + "/" + noaa + "_" + hurr + "_" +
                            str(self.timespan_url).replace("-","_to_").lower() +
                            curDate + fileExtZip)

                        self.func_Scroll_setOutputText("Download Complete.",
                                                       None)

                    self.func_Scroll_setOutputText("Unzipping " + noaa + "_" +
                                            hurr + "_" +
                                            str(self.timespan_url).replace(
                                            "-", "_to_").lower() +
                                            curDate + fileExtZip, None)

                    # Unzip the CSV file within the same folder location.
                    unZipThisFile = zipfile.ZipFile(self.subFolder_GIS + "/" +
                                            noaa + "_" + hurr + "_" +
                                            str(self.timespan_url).replace(
                                            "-", "_to_").lower() +
                                            curDate + fileExtZip, 'r')

                    unZipThisFile.extractall(self.subFolder_GIS)

                    # Close file to prevent locks.
                    unZipThisFile.close()

                    self.func_Scroll_setOutputText("Shapefile unzipped.", None)

                # Pause script for half a second.
                sleep(0.5)

                # Execute function to rename the unzipped Shapefile.
                self.func_Rename_Unzipped_Hurr_Shapefile()

                # Increment progress bar.
                self.func_ProgressBar_setProgress(20)

                # Run function to assign naming convention to feature class
                # created from Shapefile.
                self.func_NonCustomTimespan_AssignFeatureClassName()

                # Run function to create feature class from hurricane
                # Shapefile.
                self.func_Create_FeatureClass_from_Shapefile()

                # Run function to check attribute values within feature class.
                self.func_NonCustomTimespan_FeatureClass_ValueChecks()

            # If timespan is "Custom..."...
            if self.stringHurricaneTimespan.get() == "Custom...":

                # Run function to create GIS subfolder.
                self.func_Create_GIS_subFolder()

                try:

                    self.func_Scroll_setOutputText("Downloading:\n" + noaa +
                            "_" + hurr + "_" +
                            str(self.timespan_url).replace("-", "_").lower() +
                            curDate + fileExtZip, None)

                    # Retrieve CSV from URL.
                    request.urlretrieve(self.textURLTextbox.get(),
                            self.subFolder_GIS + "/" + noaa + "_" + hurr + "_" +
                            str(self.timespan_url).replace("-","_to_").lower() +
                            curDate + fileExtZip)

                    self.func_Scroll_setOutputText("Download Complete.", None)

                # If download fails, try one more time (it could have been
                # a small, temporary network glitch).
                except:

                    self.func_Scroll_setOutputText(
                            "Download failed, trying again:\n" + noaa +
                            "_" + hurr + "_" +
                            str(self.timespan_url).replace("-", "_").lower() +
                            curDate + fileExtZip, color_Orange)

                    sleep(5)

                    # Retrieve CSV from URL.
                    request.urlretrieve(self.textURLTextbox.get(),
                            self.subFolder_GIS + "/" + noaa + "_" + hurr + "_" +
                            str(self.timespan_url).replace("-","_to_").lower() +
                            curDate + fileExtZip)

                    self.func_Scroll_setOutputText("Download Complete.", None)

                self.func_Scroll_setOutputText("Unzipping " + noaa + "_" +
                        hurr + "_" +
                        str(self.timespan_url).replace("-", "_to_").lower() +
                        curDate + fileExtZip, None)

                # Unzip the CSV file within the same folder location.
                unZipThisFile = zipfile.ZipFile(self.subFolder_GIS + "/" +
                        noaa + "_" + hurr + "_" +
                        str(self.timespan_url).replace("-", "_to_").lower() +
                        curDate + fileExtZip, 'r')

                unZipThisFile.extractall(self.subFolder_GIS)

                # Close file to prevent locks.
                unZipThisFile.close()

                self.func_Scroll_setOutputText("Shapefile unzipped.", None)

                # Pause script for half a second.
                sleep(0.5)

                # Execute function to rename the unzipped Shapefile.
                self.func_Rename_Unzipped_Hurr_Shapefile()

                # Increment progress bar.
                self.func_ProgressBar_setProgress(20)

                # Run function to assign naming convention to feature class
                # created from Shapefile.
                self.func_CustomTimespan_AssignFeatureClassName()

                # Run function to create feature class from hurricane
                # Shapefile.
                self.func_Create_FeatureClass_from_Shapefile()

                # Run function to add/populate a full_date field to the
                # attribute fields.
                self.func_Add_Populate_Date_Field_ForCustomTimespan()

                # Run function to check attribute values within feature class.
                self.func_CustomTimespan_FeatureClass_ValueChecks()

            # Pause script for 0.5 seconds.
            sleep(0.5)

        except HTTPError as httpError:

            # Display error message for URL-specific problems.
            self.func_Scroll_setOutputText(str(httpError), color_Red)

            messagebox.showerror(errorMessage_Header,
                                 "Unable to access web URL.\n"
                                 "Perhaps the website's URL is missing, "
                                 "offline, or down for maintenance?\n"
                                 "Please check URL connection and try again.")

        except URLError as urlError:

            # Display error message for internet connectivity-specific problems.
            self.func_Scroll_setOutputText(str(urlError), color_Red)

            messagebox.showerror(errorMessage_Header,
                                 "Unable to access internet connectivity.\n"
                                 "Possibly temporary internet problems or\n"
                                 "URL formatting issues?\n"
                                 "Please check connection and try again.")

        except Exception as e:

            # Display error message for all other errors.
            self.func_Scroll_setOutputText("Error Message: " + str(e) + "\n" +
                                           "Traceback: " +
                                           traceback.format_exc(), color_Red)

    def func_Rename_Unzipped_Hurr_Shapefile(self):

        # This function renames the previously unzipped hurricane Shapefile. The
        # raw Shapefile naming convention contains periods, which will cause a
        # geoprocessing script to fail when attempting to copy the Shapefile
        # into a file GDB. This function will convert those periods to
        # underscores.

        try:

            self.func_Scroll_setOutputText(
                "Renaming the unzipped Shapefile to:\n" +
                self.unzipped_Hurr_RawShapefileName.replace(
                    ".", "_").lower() + fileExtShp, None)

            for file in os.listdir(self.subFolder_GIS):

                if file.__contains__(self.unzipped_Hurr_RawShapefileName):

                    if file.endswith(fileExtShp):

                        os.rename(os.path.join(self.subFolder_GIS, file),
                        os.path.join(self.subFolder_GIS,
                        self.unzipped_Hurr_RawShapefileName.replace(
                        ".","_").lower() + fileExtShp))

                    elif file.endswith(fileExtShx):

                        os.rename(os.path.join(self.subFolder_GIS, file),
                        os.path.join(self.subFolder_GIS,
                        self.unzipped_Hurr_RawShapefileName.replace(
                        ".","_").lower() + fileExtShx))

                    elif file.endswith(fileExtPrj):

                        os.rename(os.path.join(self.subFolder_GIS, file),
                        os.path.join(self.subFolder_GIS,
                        self.unzipped_Hurr_RawShapefileName.replace(
                            ".","_").lower() + fileExtPrj))

                    elif file.endswith(fileExtDbf):

                        os.rename(os.path.join(self.subFolder_GIS, file),
                        os.path.join(self.subFolder_GIS,
                        self.unzipped_Hurr_RawShapefileName.replace(
                            ".","_").lower() + fileExtDbf))

            self.func_Scroll_setOutputText("Shapefile renamed.", None)

        except Exception as e:

            # Display error message for all other errors.
            self.func_Scroll_setOutputText("Error Message: " + str(e) + "\n" +
                                           "Traceback: " +
                                           traceback.format_exc(), color_Red)

    def func_NonCustomTimespan_AssignFeatureClassName(self):

        # This function controls the naming convention of the
        # self.name_Hurr_FeatureClass variable if a non-custom timespan is
        # chosen.

        # If the speed combobox displays "Custom..."...
        if self.stringHurricaneIntensity.get() == "Custom...":

                # This will be the naming convention of the output feature class
                # once converted from Shapefile.
                self.name_Hurr_FeatureClass = noaa + "_" + hurr + "_" + \
                        self.custom_Intensity_Naming + "_" + \
                        str(self.timespan_url).replace("-", "_to_").lower() + \
                        curDate

        # If the speed combobox does not display "Custom..."...
        elif self.stringHurricaneIntensity.get() != "Custom...":

            # This will be the naming convention of the output feature class
            # once converted from Shapefile.
            self.name_Hurr_FeatureClass = noaa + "_" + hurr + "_" + \
                        self.mag_naming + "_" + \
                        str(self.timespan_url).replace("-","_to_").lower() + \
                        curDate

    def func_CustomTimespan_AssignFeatureClassName(self):

        # This function controls the naming convention of the
        # self.name_Hurr_FeatureClass variable if a custom timespan is chosen.

        # If the speed combobox displays "Custom..."...
        if self.stringHurricaneIntensity.get() == "Custom...":

            # This will be the naming convention of the output feature class
            # once converted from Shapefile.
            self.name_Hurr_FeatureClass = \
                noaa + "_" + hurr + "_" + self.custom_Intensity_Naming + \
                self.timespan_file_folder_naming + curDate

        # If the speed combobox does not display "Custom..."...
        elif self.stringHurricaneIntensity.get() != "Custom...":

            # This will be the naming convention of the output feature class
            # once converted from Shapefile.
            self.name_Hurr_FeatureClass = noaa + "_" + hurr + "_" + \
                                            self.mag_naming + \
                                            self.timespan_file_folder_naming + \
                                            curDate

    def func_Create_FeatureClass_from_Shapefile(self):

        # This function controls the process of creating an output File GDB that
        # will be stored with a feature class created from the raw hurricane
        # Shapefile. This feature class is used to create a new,
        # re-projected feature class of the same data. The original feature
        # class is deleted, and the re-projected feature class naming convention
        # is changed to match the original feature class that was deleted.

        try:

            self.func_Scroll_setOutputText("Creating File GDB...", None)

            # Create File GDB within the GIS subfolder.
            arcpy.CreateFileGDB_management(self.subFolder_GIS, nameFileGDB)

            # Display ArcPy geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            self.func_Scroll_setOutputText("File GDB created.", None)

            # Increment progress bar.
            self.func_ProgressBar_setProgress(34)

            self.func_Scroll_setOutputText(
                "Creating Feature Class from downloaded hurricane Shapefile...",
                None)

            # Set workspace to the GIS subfolder for following task.
            arcpy.env.workspace = self.subFolder_GIS

            # Conversion parameters, with optional parameters set to
            # None for Esri defaults.
            required_InputFile = \
                self.unzipped_Hurr_RawShapefileName.replace(".","_").lower() + \
                fileExtShp
            required_OutputWorkspace = nameFileGDB
            required_OutputFile = self.name_Hurr_FeatureClass
            optional_WhereClause = None
            optional_FieldMapping = None
            optional_ConfigKeyword = None

            # Convert Shapefile into a feature class stored within the File GDB.
            arcpy.FeatureClassToFeatureClass_conversion(required_InputFile,
                                                    required_OutputWorkspace,
                                                    required_OutputFile,
                                                    optional_WhereClause,
                                                    optional_FieldMapping,
                                                    optional_ConfigKeyword)

            # Display ArcPy geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            self.func_Scroll_setOutputText(
                "Feature Class from Shapefile created.", None)

            # Set workspace to the File GDB for following tasks.
            arcpy.env.workspace = self.subFolder_GIS + nameFileGDB

            # Create variable to represent unclipped, unprojected
            # feature class name. This will be a temporary naming convention.
            self.featureClass_Hurricane_Unclipped_Unprojected = \
                self.name_Hurr_FeatureClass

            # Create variable to represent unclipped, projected feature class
            # name. This will be a temporary naming convention.
            self.featureClass_Hurricane_Unclipped_Projected = \
                self.name_Hurr_FeatureClass + "_Projected"

            self.func_Scroll_setOutputText("Projecting feature class to PCS " +
                            pcsReferenceString +
                            " with Central Meridian Offset (-30.0 degrees)...",
                            None)

            # Set projected coordinate system of feature class to the designated
            # PCS reference with -30.0 Central Meridian offset.
            arcpy.Project_management(
                self.featureClass_Hurricane_Unclipped_Unprojected,
                self.featureClass_Hurricane_Unclipped_Projected, pcsReference)

            # Display ArcPy geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            self.func_Scroll_setOutputText("PCS Projection to " +
                    pcsReferenceString +
                    " with Central Meridian Offset (-30.0 degrees) completed.",
                    None)

            self.func_Scroll_setOutputText(
                "Recalculating extent for feature class...",
                None)

            # Recalculate extent of newly projected feature class.
            arcpy.RecalculateFeatureClassExtent_management(
                self.featureClass_Hurricane_Unclipped_Projected)

            # Display ArcPy geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            self.func_Scroll_setOutputText("Feature class extent recalculated.",
                                           None)

            self.func_Scroll_setOutputText("Deleting feature class " +
                            self.featureClass_Hurricane_Unclipped_Unprojected +
                            " from File GDB...", None)

            # Delete original feature class conversion from CSV.
            arcpy.Delete_management(
                self.featureClass_Hurricane_Unclipped_Unprojected)

            # Display ArcPy geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            self.func_Scroll_setOutputText(
                "Feature class deleted from File GDB.", None)

            self.func_Scroll_setOutputText("Renaming feature class " +
                    self.featureClass_Hurricane_Unclipped_Projected + " to " +
                    self.featureClass_Hurricane_Unclipped_Unprojected + "...",
                    None)

            # Rename the projected feature class to the unprojected feature
            # class name that was just deleted.
            arcpy.Rename_management(
                self.featureClass_Hurricane_Unclipped_Projected,
                self.featureClass_Hurricane_Unclipped_Unprojected)

            # Display ArcPy geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            self.func_Scroll_setOutputText(
                "Feature class has been renamed.", None)

            # Increment progress bar.
            self.func_ProgressBar_setProgress(40)

            # Execute function that clears any "in_memory" storage used during
            # ArcPy geoprocessing tasks.
            self.func_Clear_InMemory()

            # Execute function to evaluate which clipping option is selected.
            #self.func_RadioButton_Clipping_Rules()

        except arcpy.ExecuteError:

            # Display ArcPy-specific error messages. If any geoprocessing tasks
            # fails, no further functions are attempted.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Red)

            # Re-enable all selectable buttons and drop-down lists.
            self.func_Enable_Buttons()

            # Stop the status bar.
            self.func_StopStatusBar()

            # Increment progress bar to 100 percent.
            self.func_ProgressBar_setProgress(100)

            # Calculate total script processing time.
            self.func_Calculate_Script_Time()

            # Save all scroll box text to file.
            self.func_Scroll_saveOutputText()

            # Exit the process.
            exit()

        except Exception as e:

            # Display all other error messages.
            self.func_Scroll_setOutputText("Error Message: " + str(e) + "\n" +
                                           "Traceback: " +
                                           traceback.format_exc(), color_Red)

            # Re-enable all selectable buttons and drop-down lists.
            self.func_Enable_Buttons()

            # Stop the status bar.
            self.func_StopStatusBar()

            # Increment progress bar to 100 percent.
            self.func_ProgressBar_setProgress(100)

            # Calculate total script processing time.
            self.func_Calculate_Script_Time()

            # Save all scroll box text to file.
            self.func_Scroll_saveOutputText()

            # Exit the process.
            exit()

    def func_NonCustomTimespan_FeatureClass_ValueChecks(self):

        # This function will analyzing data within the hurricane feature class
        # for unneeded values or discrepancies.

        try:

            # Set workspace to the File GDB for following tasks.
            arcpy.env.workspace = self.subFolder_GIS + nameFileGDB

            self.func_Scroll_setOutputText("Checking hurricane feature class "
                                           "for erroneous wind speed values "
                                           "equal to or less than zero knots.",
                                           None)

            # Open the hurricane feature class with an Update Cursor.
            # Attribute fields are set to the wind speed column and feature
            # class line length (in meters).
            with arcpy.da.UpdateCursor(self.name_Hurr_FeatureClass,
                                field_names=[analysis_Mag_Field,
                                analysis_Line_Length_Field_InMeters]) as cursor:

                # For each feature in the hurricane feature class.
                for row in cursor:

                    # This If statement removes all wind values less than or
                    # equal to zero, as well as wind speeds above 200 knots.
                    # Additionally, any feature class hurricane polylines less
                    # than 1600 meters in length (approximately 1 mile) will be
                    # removed as well.
                    if int(float(row[0])) <= 0 or int(float(row[0])) > 200 or \
                            int(float(row[1])) < 1600:

                        cursor.deleteRow()

            with arcpy.da.UpdateCursor(self.name_Hurr_FeatureClass,
                                field_names=[analysis_Mag_Field,
                                analysis_Line_Length_Field_InMeters]) as cursor:

                for row in cursor:

                    # If the wind intensity is set to All...
                    if self.stringHurricaneIntensity.get() == "All":

                        # Delete nothing.
                        pass

                    # If the wind intensity is set to Tropical Depression...
                    elif self.stringHurricaneIntensity.get() == \
                            "Trop. Depression":

                        # If the wind intensity is greater than or equal to
                        # 34 knots...
                        if int(float(row[0])) >= 34:
                            # Delete the row from the feature class.
                            cursor.deleteRow()

                    # If the wind intensity is set to Tropical Storm...
                    elif self.stringHurricaneIntensity.get() == \
                            "Trop. Storm":

                        # If the wind intensity is less than 34 knots and
                        # greater than or equal to 64 knots...
                        if int(float(row[0])) < 34 or \
                                int(float(row[0])) >= 64:
                            # Delete the row from the feature class.
                            cursor.deleteRow()

                    # If the wind intensity is set to Category 1...
                    elif self.stringHurricaneIntensity.get() == "Cat. 1":

                        # If the wind intensity is less than 64 knots and
                        # greater than or equal to 83 knots...
                        if int(float(row[0])) < 64 or \
                                int(float(row[0])) >= 83:
                            # Delete the row from the feature class.
                            cursor.deleteRow()

                    # If the wind intensity is set to Category 2...
                    elif self.stringHurricaneIntensity.get() == "Cat. 2":

                        # If the wind intensity is less than 83 knots and
                        # greater than or equal to 96 knots...
                        if int(float(row[0])) < 83 or \
                                int(float(row[0])) >= 96:
                            # Delete the row from the feature class.
                            cursor.deleteRow()

                    # If the wind intensity is set to Category 3...
                    elif self.stringHurricaneIntensity.get() == "Cat. 3":

                        # If the wind intensity is less than 96 knots and
                        # greater than or equal to 113 knots...
                        if int(float(row[0])) < 96 or \
                                int(float(row[0])) >= 113:
                            # Delete the row from the feature class.
                            cursor.deleteRow()

                    # If the wind intensity is Category 4...
                    elif self.stringHurricaneIntensity.get() == "Cat. 4":

                        # If the wind intensity is less than 113 knots and
                        # greater than or equal to 137 knots...
                        if int(float(row[0])) < 113 or \
                                int(float(row[0])) >= 137:
                            # Delete the row from the feature class.
                            cursor.deleteRow()

                    # If the wind intensity is Category 5...
                    elif self.stringHurricaneIntensity.get() == "Cat. 5":

                        # If the wind intensity is less than 137 knots...
                        if int(float(row[0])) < 137:
                            # Delete the row from the feature class.
                            cursor.deleteRow()

                    # If the wind intensity is set to Custom...
                    elif self.stringHurricaneIntensity.get() == "Custom...":

                        # If the wind intensity is not within the
                        # From/To selections...
                        if int(float(row[0])) < \
                                int(self.textCustomIntensityFrom) or \
                                int(float(row[0])) > \
                                int(self.textCustomIntensityTo):
                            # Delete the row from the feature class.
                            cursor.deleteRow()

            # Display ArcPy geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            self.func_Scroll_setOutputText("Hurricane feature class has been "
                                           "checked for wind speed and polyline"
                                           " length errors.", None)

            self.func_Scroll_setOutputText(
                "Recalculating extent for feature class...",
                None)

            # Recalculate extent of newly projected feature class.
            arcpy.RecalculateFeatureClassExtent_management(
                self.name_Hurr_FeatureClass)

            # Display ArcPy geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            self.func_Scroll_setOutputText("Feature class extent recalculated.",
                                           None)

            self.checked_name_Hurr_FeatureClass = \
                self.name_Hurr_FeatureClass + "_checked"

            self.func_Scroll_setOutputText("Renaming feature class " +
                        self.name_Hurr_FeatureClass + " to " +
                        self.checked_name_Hurr_FeatureClass + "...",
                        None)

            # Rename the hurricane feature class to include "_checked" at the
            # end of the naming convention.
            arcpy.Rename_management(self.name_Hurr_FeatureClass,
                                    self.checked_name_Hurr_FeatureClass)

            # Display ArcPy geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            self.func_Scroll_setOutputText("Feature class has been renamed.",
                                           None)

            # Get the feature count of the input argument and assign to count
            # variable.
            self.raw_hurricaneCountResult = \
                arcpy.GetCount_management(self.checked_name_Hurr_FeatureClass)

            # Store the integer version of the hurricane count to variable.
            self.global_hurricaneCount = \
                int(self.raw_hurricaneCountResult.getOutput(0))

            # If zero hurricane features present within the feature class...
            if self.global_hurricaneCount < 1:

                # Display this message and error message to the user, since the
                # script can't proceed any farther.
                self.func_Scroll_setOutputText("No hurricane features "
                        "present within the timespan/intensity/location.\n" +
                        "Unable to continue.", color_Red)

                messagebox.showerror(errorMessage_Header,
                                     "No hurricane features present within the "
                                     "timespan/intensity/location.\n" +
                                     "Unable to continue.")

                # Re-enable all selectable buttons and drop-down lists.
                self.func_Enable_Buttons()

                # Stop the status bar.
                self.func_StopStatusBar()

                # Increment progress bar to 100 percent.
                self.func_ProgressBar_setProgress(100)

                # Calculate total script processing time.
                self.func_Calculate_Script_Time()

                # Save all scroll box text to file.
                self.func_Scroll_saveOutputText()

                # Exit the process.
                exit()

            else:

                # Display this message and error message to the user, since the
                # script can't proceed any farther.
                self.func_Scroll_setOutputText(str(self.global_hurricaneCount) +
                                " global hurricane features present within the "
                                "timespan/intensity/location.", None)

                # Execute function to evaluate which clipping option is
                # selected.
                self.func_RadioButton_Clipping_Rules()

        except arcpy.ExecuteError:

            # Display ArcPy-specific error messages. If any geoprocessing tasks
            # fails, no further functions are attempted.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Red)

            # Re-enable all selectable buttons and drop-down lists.
            self.func_Enable_Buttons()

            # Stop the status bar.
            self.func_StopStatusBar()

            # Increment progress bar to 100 percent.
            self.func_ProgressBar_setProgress(100)

            # Calculate total script processing time.
            self.func_Calculate_Script_Time()

            # Save all scroll box text to file.
            self.func_Scroll_saveOutputText()

            # Exit the process.
            exit()

        except Exception as e:

            # Display all other error messages.
            self.func_Scroll_setOutputText("Error Message: " + str(e) + "\n" +
                                           "Traceback: " +
                                           traceback.format_exc(), color_Red)

            # Re-enable all selectable buttons and drop-down lists.
            self.func_Enable_Buttons()

            # Stop the status bar.
            self.func_StopStatusBar()

            # Increment progress bar to 100 percent.
            self.func_ProgressBar_setProgress(100)

            # Calculate total script processing time.
            self.func_Calculate_Script_Time()

            # Save all scroll box text to file.
            self.func_Scroll_saveOutputText()

            # Exit the process.
            exit()

    def func_Add_Populate_Date_Field_ForCustomTimespan(self):

        # This function will create a new date field within the feature class
        # attribute table. This will combine the month, day, and year
        # information from the separated fields and combine them into one field.
        # This will allow later portions of the script to extract date-specific
        # hurricane information.

        try:

            # Set workspace to the File GDB for following tasks.
            arcpy.env.workspace = self.subFolder_GIS + nameFileGDB

            self.func_Scroll_setOutputText("Adding a FULL_DATE field within the"
                                           " feature class...", None)

            # Add Field parameters
            required_InputFC = self.name_Hurr_FeatureClass
            required_FieldName = "full_date"
            required_FieldType = "TEXT"
            optional_FieldPrecision = None
            optional_FieldScale = None
            optional_FieldLength = None
            optional_FieldAlias = None
            optional_FieldIsNullable = None
            optional_FieldIsRequired = None
            optional_FieldDomain = None

            # Add the attribute field.
            arcpy.AddField_management(required_InputFC, required_FieldName,
                                required_FieldType, optional_FieldPrecision,
                                optional_FieldScale, optional_FieldLength,
                                optional_FieldAlias, optional_FieldIsNullable,
                                optional_FieldIsRequired, optional_FieldDomain)

            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            self.func_Scroll_setOutputText("FULL_DATE field added.", None)

            sleep(1)

            self.func_Scroll_setOutputText("Populating FULL_DATE field...",
                                           None)

            # Populate the newly created attribute field via UpdateCursor.
            with arcpy.da.UpdateCursor(self.name_Hurr_FeatureClass,
                                       date_fields) as cursor:

                for row in cursor:

                    row[3] = str(row[0]) + "-" + str(row[1]) + "-" + str(row[2])

                    cursor.updateRow(row)

            self.func_Scroll_setOutputText("FULL_DATE field populated.", None)


        except arcpy.ExecuteError:

            # Display ArcPy-specific error messages. If any geoprocessing tasks
            # fails, no further functions are attempted.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Red)

            # Re-enable all selectable buttons and drop-down lists.
            self.func_Enable_Buttons()

            # Stop the status bar.
            self.func_StopStatusBar()

            # Increment progress bar to 100 percent.
            self.func_ProgressBar_setProgress(100)

            # Calculate total script processing time.
            self.func_Calculate_Script_Time()

            # Save all scroll box text to file.
            self.func_Scroll_saveOutputText()

            # Exit the process.
            exit()

        except Exception as e:

            # Display all other error messages.
            self.func_Scroll_setOutputText("Error Message: " + str(e) + "\n" +
                                           "Traceback: " +
                                           traceback.format_exc(), color_Red)

            # Re-enable all selectable buttons and drop-down lists.
            self.func_Enable_Buttons()

            # Stop the status bar.
            self.func_StopStatusBar()

            # Increment progress bar to 100 percent.
            self.func_ProgressBar_setProgress(100)

            # Calculate total script processing time.
            self.func_Calculate_Script_Time()

            # Save all scroll box text to file.
            self.func_Scroll_saveOutputText()

            # Exit the process.
            exit()

    def func_CustomTimespan_FeatureClass_ValueChecks(self):

        # This function will analyze data within the hurricane feature class
        # for unneeded values or discrepancies.

        try:

            # Set workspace to the File GDB for following tasks.
            arcpy.env.workspace = self.subFolder_GIS + nameFileGDB

            self.func_Scroll_setOutputText("Removing hurricane features not "
                                           "within the selected custom "
                                           "timespan...", None)

            # Open the hurricane feature class with an Update Cursor.
            # Attribute field is set to the full_date field. Any values not
            # within the custom timespan selected will be deleted from the
            # feature class.
            with arcpy.da.UpdateCursor(self.name_Hurr_FeatureClass,
                                       dateField_FullDate) as cursor:

                # For each feature in the hurricane feature class...
                for row in cursor:

                    # Assign the YYYYMM's monthly range in days.
                    monthRange = \
                        calendar.monthrange(int(self.textCustomYearFrom),
                                            int(self.textCustomMonthFrom))[1]

                    # Create FROM date by combining YYYY, MM, and DD
                    # parameters. DD = 1 for beginning of month.
                    fromDate = \
                        datetime.datetime.strptime(self.textCustomYearFrom +
                                                "-" + self.textCustomMonthFrom +
                                                "-1", "%Y-%m-%d")

                    # Create TO date by combining YYYY, MM, and DD
                    # parameters. DD = Monthly range for the given month/year.
                    toDate = \
                        datetime.datetime.strptime(self.textCustomYearTo +
                                                "-" + self.textCustomMonthTo +
                                                "-" + str(monthRange),
                                                "%Y-%m-%d")

                    # Format the "full_date" column into the
                    # following date format so that it can be used to
                    # compare itself to the fromDate and toDate variables.
                    date_in_row = datetime.datetime.strptime(str(row[0]),
                                                             "%Y-%m-%d")

                    # If the feature class date is not between the from date or
                    # the to date...
                    if date_in_row < fromDate or date_in_row > toDate:

                        # Delete the hurricane feature.
                        cursor.deleteRow()

            self.func_Scroll_setOutputText("Hurricane features not within the "
                                           "selected custom timespan have been "
                                           "removed.", None)

            # Pause script for one second.
            sleep(1)

            self.func_Scroll_setOutputText("Checking hurricane feature class "
                                           "for erroneous wind speed values "
                                           "equal to or less than zero knots. "
                                           "Polyline features less than ~1 mile"
                                           " will be removed as well.", None)

            # Open the hurricane feature class with an Update Cursor.
            # Attribute fields are set to the wind speed column and feature
            # class line length (in meters).
            with arcpy.da.UpdateCursor(self.name_Hurr_FeatureClass,
                                field_names=[analysis_Mag_Field,
                                analysis_Line_Length_Field_InMeters]) as cursor:

                # For each feature in the hurricane feature class.
                for row in cursor:

                    # This If statement removes all wind values less than or
                    # equal to zero, as well as wind speeds above 200 knots.
                    # Additionally, any feature class hurricane polylines less
                    # than 1600 meters in length (approximately 1 mile) will be
                    # removed as well.
                    if int(float(row[0])) <= 0 or int(float(row[0])) > 200 or \
                            int(float(row[1])) < 1600:

                        cursor.deleteRow()

            # Open the hurricane feature class with an Update Cursor.
            # Attribute fields are set to the wind speed column and feature
            # class line length (in meters).
            with arcpy.da.UpdateCursor(self.name_Hurr_FeatureClass,
                                field_names=[analysis_Mag_Field,
                                analysis_Line_Length_Field_InMeters]) as cursor:

                for row in cursor:

                    # If the wind intensity is set to All...
                    if self.stringHurricaneIntensity.get() == "All":

                        # Delete nothing.
                        pass

                    # If the wind intensity is set to Tropical Depression...
                    elif self.stringHurricaneIntensity.get() == \
                            "Trop. Depression":

                        # If the wind intensity is greater than or equal to
                        # 34 knots...
                        if int(float(row[0])) >= 34:
                            # Delete the row from the feature class.
                            cursor.deleteRow()

                    # If the wind intensity is set to Tropical Storm...
                    elif self.stringHurricaneIntensity.get() == \
                            "Trop. Storm":

                        # If the wind intensity is less than 34 knots and
                        # greater than or equal to 64 knots...
                        if int(float(row[0])) < 34 or \
                                int(float(row[0])) >= 64:
                            # Delete the row from the feature class.
                            cursor.deleteRow()

                    # If the wind intensity is set to Category 1...
                    elif self.stringHurricaneIntensity.get() == "Cat. 1":

                        # If the wind intensity is less than 64 knots and
                        # greater than or equal to 83 knots...
                        if int(float(row[0])) < 64 or \
                                int(float(row[0])) >= 83:
                            # Delete the row from the feature class.
                            cursor.deleteRow()

                    # If the wind intensity is set to Category 2...
                    elif self.stringHurricaneIntensity.get() == "Cat. 2":

                        # If the wind intensity is less than 83 knots and
                        # greater than or equal to 96 knots...
                        if int(float(row[0])) < 83 or \
                                int(float(row[0])) >= 96:
                            # Delete the row from the feature class.
                            cursor.deleteRow()

                    # If the wind intensity is set to Category 3...
                    elif self.stringHurricaneIntensity.get() == "Cat. 3":

                        # If the wind intensity is less than 96 knots and
                        # greater than or equal to 113 knots...
                        if int(float(row[0])) < 96 or \
                                int(float(row[0])) >= 113:
                            # Delete the row from the feature class.
                            cursor.deleteRow()

                    # If the wind intensity is Category 4...
                    elif self.stringHurricaneIntensity.get() == "Cat. 4":

                        # If the wind intensity is less than 113 knots and
                        # greater than or equal to 137 knots...
                        if int(float(row[0])) < 113 or \
                                int(float(row[0])) >= 137:
                            # Delete the row from the feature class.
                            cursor.deleteRow()

                    # If the wind intensity is Category 5...
                    elif self.stringHurricaneIntensity.get() == "Cat. 5":

                        # If the wind intensity is less than 137 knots...
                        if int(float(row[0])) < 137:
                            # Delete the row from the feature class.
                            cursor.deleteRow()

                    # If the wind intensity is set to Custom...
                    elif self.stringHurricaneIntensity.get() == "Custom...":

                        # If the wind intensity is not within the
                        # From/To selections...
                        if int(float(row[0])) < \
                                int(self.textCustomIntensityFrom) or \
                                int(float(row[0])) > \
                                int(self.textCustomIntensityTo):
                            # Delete the row from the feature class.
                            cursor.deleteRow()

            # Display ArcPy geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            self.func_Scroll_setOutputText("Hurricane feature class has been "
                                           "checked for wind speed and polyline"
                                           " length errors.", None)

            self.func_Scroll_setOutputText(
                "Recalculating extent for feature class...",
                None)

            # Recalculate extent of newly projected feature class.
            arcpy.RecalculateFeatureClassExtent_management(
                self.name_Hurr_FeatureClass)

            # Display ArcPy geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            self.func_Scroll_setOutputText("Feature class extent recalculated.",
                                           None)

            self.checked_name_Hurr_FeatureClass = \
                self.name_Hurr_FeatureClass + "_checked"

            self.func_Scroll_setOutputText("Renaming feature class " +
                                self.name_Hurr_FeatureClass + " to " +
                                self.checked_name_Hurr_FeatureClass + "...",
                                None)

            # Rename the hurricane feature class to include "_checked" at the
            # end of the naming convention.
            arcpy.Rename_management(self.name_Hurr_FeatureClass,
                                    self.checked_name_Hurr_FeatureClass)

            # Display ArcPy geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            self.func_Scroll_setOutputText("Feature class has been renamed.",
                                           None)

            # Get the feature count of the input argument and assign to count
            # variable.
            self.raw_hurricaneCountResult = \
                arcpy.GetCount_management(self.checked_name_Hurr_FeatureClass)

            # Get the feature count of the input argument and assign to count
            # variable.
            self.raw_hurricaneCountResult = \
                arcpy.GetCount_management(self.checked_name_Hurr_FeatureClass)

            # Store the integer version of the hurricane count to variable.
            self.global_hurricaneCount = \
                int(self.raw_hurricaneCountResult.getOutput(0))

            # If zero hurricane features present within the feature class...
            if self.global_hurricaneCount < 1:

                # Display this message and error message to the user, since the
                # script can't proceed any farther.
                self.func_Scroll_setOutputText("No hurricane features "
                        "present within the timespan/intensity/location.\n" +
                        "Unable to continue.", color_Red)

                messagebox.showerror(errorMessage_Header,
                                     "No hurricane features present within the "
                                     "timespan/intensity/location.\n" +
                                     "Unable to continue.")

                # Re-enable all selectable buttons and drop-down lists.
                self.func_Enable_Buttons()

                # Stop the status bar.
                self.func_StopStatusBar()

                # Increment progress bar to 100 percent.
                self.func_ProgressBar_setProgress(100)

                # Calculate total script processing time.
                self.func_Calculate_Script_Time()

                # Save all scroll box text to file.
                self.func_Scroll_saveOutputText()

                # Exit the process.
                exit()

            else:

                # Display this message and error message to the user, since the
                # script can't proceed any farther.
                self.func_Scroll_setOutputText(str(self.global_hurricaneCount) +
                                " global hurricane features present within the "
                                "timespan/intensity/location.", None)

                # Execute function to evaluate which clipping option is
                # selected.
                self.func_RadioButton_Clipping_Rules()

        except arcpy.ExecuteError:

            # Display ArcPy-specific error messages. If any geoprocessing tasks
            # fails, no further functions are attempted.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Red)

            # Re-enable all selectable buttons and drop-down lists.
            self.func_Enable_Buttons()

            # Stop the status bar.
            self.func_StopStatusBar()

            # Increment progress bar to 100 percent.
            self.func_ProgressBar_setProgress(100)

            # Calculate total script processing time.
            self.func_Calculate_Script_Time()

            # Save all scroll box text to file.
            self.func_Scroll_saveOutputText()

            # Exit the process.
            exit()

        except Exception as e:

            # Display all other error messages.
            self.func_Scroll_setOutputText("Error Message: " + str(e) + "\n" +
                                           "Traceback: " +
                                           traceback.format_exc(), color_Red)

            # Re-enable all selectable buttons and drop-down lists.
            self.func_Enable_Buttons()

            # Stop the status bar.
            self.func_StopStatusBar()

            # Increment progress bar to 100 percent.
            self.func_ProgressBar_setProgress(100)

            # Calculate total script processing time.
            self.func_Calculate_Script_Time()

            # Save all scroll box text to file.
            self.func_Scroll_saveOutputText()

            # Exit the process.
            exit()

    def func_RadioButton_Clipping_Command(self):

        # This function controls how the clipping options should operate with
        # regard to the radio buttons. Depending on the clipping selection,
        # the appearance of state or county drop-down lists will change.

        try:

            # Get the value of the clipping option selected by the user.
            self.radioButton_Selection = self.statusClippingOption.get()

            # If the clipping option represents "USA"...
            if self.radioButton_Selection == 1:

                # If the user selects USA after already selecting State, remove
                # the state drop-down list and set state variables to None.
                if self.comboFrame_State is not None:

                    self.comboFrame_State.grid_remove()

                    self.comboFrame_State = None

                    self.stringState_Name = None

                # If the user selects USA after already selecting county option,
                #  remove the county/state drop-down lists and set county
                # variables to None.
                if self.comboFrame_Counties is not None:

                    self.comboFrame_Counties.grid_remove()

                    self.comboFrame_Counties = None

                    self.stringCounty_Name = None

                # Execute function to resize window accordingly.
                self.func_windowResize()

            # If the clipping option represents "State"...
            if self.radioButton_Selection == 2:

                # If the user selects State after already selecting State,
                # remove the previously created state drop-down list and reset
                # state variables to None. This prevents duplicate drop-down
                # lists from stacking on top of each other with each radio
                # button click.
                if self.comboFrame_State is not None:

                    self.comboFrame_State.grid_remove()

                    self.comboFrame_State = None

                # If the user selects State after already selecting County,
                # remove the previously created county/state drop-down lists and
                # reset county variables to None. This prevents duplicate
                # drop-down lists from stacking on top of each other with
                # each radio button click.
                if self.comboFrame_Counties is not None:

                    self.comboFrame_Counties.grid_remove()

                    self.comboFrame_Counties = None

                    self.stringCounty_Name = None

                # Execute function that handles the functionality of the state
                # drop-down list.
                self.func_RadioButton_State_Frame_Options()

                # Excecute function to resize window accordingly.
                self.func_windowResize()

            # If the clipping option represents "County" while the state
            # drop-down list is already visible (User selects state option
            # immediately before switching to county option)...
            if self.radioButton_Selection == 3 and \
                    self.comboFrame_State is not None:

                # Do nothing, leave the state drop-down list visible.
                pass

                # If the user selects County after already selecting County,
                # remove the previously created county drop-down list and
                # reset county variables to None. This prevents duplicate
                # drop-down lists from stacking on top of each other with
                # each radio button click.
                if self.comboFrame_Counties is not None:

                    self.comboFrame_Counties.grid_remove()

                    self.comboFrame_Counties = None

                    self.stringCounty_Name = None

                # Execute function that handles the functionality of the county
                # drop-down list.
                self.func_RadioButton_County_Frame_Options()

                # Execute function to resize window accordingly.
                self.func_windowResize()

            # If the clipping option represents "County" while the state
            # drop-down list isn't already visible (User does not select state
            # option immediately before switching to county option)...
            if self.radioButton_Selection == 3 and \
                    self.comboFrame_State is None:

                # If County options already exists, remove the drop-down list
                # and clear county variablesto prevent duplicate drop-down lists
                # from stacking on top of each other.
                if self.comboFrame_Counties is not None:

                    self.comboFrame_Counties.grid_remove()

                    self.comboFrame_Counties = None

                    self.stringCounty_Name = None

                # Execute function that handles the functionality of the state
                # drop-down list.
                self.func_RadioButton_State_Frame_Options()

                # Execute function that handles the functionality of the county
                # drop-down list.
                self.func_RadioButton_County_Frame_Options()

                # Execute function to resize window accordingly.
                self.func_windowResize()

        except Exception as e:

            # Display error message.
            self.func_Scroll_setOutputText("Error Message: " + str(e) + "\n" +
                                           "Traceback: " +
                                           traceback.format_exc(), color_Red)

    def func_RadioButton_Clipping_Rules(self):

        # This function controls how the Census Bureau's Shapefile is clipped,
        # depending on user preference assigned within the clipping options
        # radio button/drop-down list selection.
        try:
            # If the radio button is USA...
            if self.radioButton_Selection == 1:

                # Execute function that downloads/unzips the Census Bureau's
                # Shapefile.
                self.func_Download_Unzip_Census_Shapefile()

                # Once Census Shapefile has been downloaded, execute function
                # to extract the 50 states and Washington DC only.
                self.func_Extract_50_States_and_DC_Only(
                    self.subFolder_CensusShapefile + "/" +
                    census_URL_CountyShapefile_FileName + fileExtShp,
                    self.subFolder_GIS + "/" + nameFileGDB)

                # Increment progress bar.
                self.func_ProgressBar_setProgress(60)

                # Then execute function to clip hurricane features to the
                # polygon boundary for US states and DC.
                self.func_FeatureClass_Clip(
                                    self.checked_name_Hurr_FeatureClass,
                                    featureClass_50States_and_DC_only,
                                    "clipped_" +
                                    self.checked_name_Hurr_FeatureClass)

                # Execute function to verify if clipped hurricane feature class
                # still contains any features.
                self.func_Check_If_Empty_Output_FeatureClass()

                # Execute function to buffer the clipped hurricane feature.
                self.func_FeatureClass_Buffer(self.clipped_Output_FeatureClass,
                                "buffered_" + self.clipped_Output_FeatureClass)

                # Execute function that controls analysis options.
                self.func_Controls_For_Analysis_Options(
                    featureClass_50States_and_DC_only)

            # If the radio button is State...
            elif self.radioButton_Selection == 2:

                # Execute function that downloads/unzips the Census Bureau's
                # Shapefile.
                self.func_Download_Unzip_Census_Shapefile()

                # Once Census Shapefile has been downloaded, execute function
                # to extract the 50 states and Washington DC only.
                self.func_Extract_50_States_and_DC_Only(
                    self.subFolder_CensusShapefile + "/" +
                    census_URL_CountyShapefile_FileName + fileExtShp,
                    self.subFolder_GIS + "/" + nameFileGDB)

                # Increment progress bar.
                self.func_ProgressBar_setProgress(55)

                # Once Census Shapefile has been downloaded, execute function
                # to extract state selection only.
                self.func_Extract_State_Selection_Only(
                    self.subFolder_CensusShapefile + "/" +
                    census_URL_CountyShapefile_FileName + fileExtShp,
                    self.subFolder_GIS + "/" + nameFileGDB)

                # Increment progress bar.
                self.func_ProgressBar_setProgress(60)

                # Then execute function to clip hurricane features to the
                # polygon state boundary.
                self.func_FeatureClass_Clip(
                                    self.checked_name_Hurr_FeatureClass,
                                    self.featureClass_State_Selection_Only,
                                    "clipped_" +
                                    self.checked_name_Hurr_FeatureClass)

                # Execute function to verify if clipped hurricane feature class
                # still contains any features.
                self.func_Check_If_Empty_Output_FeatureClass()

                # Execute function to buffer the clipped hurricane feature.
                self.func_FeatureClass_Buffer(self.clipped_Output_FeatureClass,
                                "buffered_" + self.clipped_Output_FeatureClass)

                # Execute function that controls analysis options.
                self.func_Controls_For_Analysis_Options(
                    self.featureClass_State_Selection_Only)

            # If the radio button is County...
            elif self.radioButton_Selection == 3:

                # Execute function that downloads/unzips the Census Bureau's
                # Shapefile.
                self.func_Download_Unzip_Census_Shapefile()

                # Once Census Shapefile has been downloaded, execute function
                # to extract the 50 states and Washington DC only.
                self.func_Extract_50_States_and_DC_Only(
                    self.subFolder_CensusShapefile + "/" +
                    census_URL_CountyShapefile_FileName + fileExtShp,
                    self.subFolder_GIS + "/" + nameFileGDB)

                # Increment progress bar.
                self.func_ProgressBar_setProgress(55)

                # Once Census Shapefile has been downloaded, execute function
                # to extract state selection only.
                self.func_Extract_State_Selection_Only(
                    self.subFolder_CensusShapefile + "/" +
                    census_URL_CountyShapefile_FileName + fileExtShp,
                    self.subFolder_GIS + "/" + nameFileGDB)

                # Increment progress bar.
                self.func_ProgressBar_setProgress(58)

                # Once Census Shapefile has been downloaded, execute function
                # to extract the county selection only.
                self.func_Extract_County_Selection_Only(
                    self.subFolder_CensusShapefile + "/" +
                    census_URL_CountyShapefile_FileName + fileExtShp,
                    self.subFolder_GIS + "/" + nameFileGDB)

                # Increment progress bar.
                self.func_ProgressBar_setProgress(60)

                # Then execute function to clip hurricane features to the
                # polygon county boundary.
                self.func_FeatureClass_Clip(
                                    self.checked_name_Hurr_FeatureClass,
                                    self.featureClass_County_State_Naming,
                                    "clipped_" +
                                    self.checked_name_Hurr_FeatureClass)

                # Execute function to verify if clipped hurricane feature class
                # still contains any features.
                self.func_Check_If_Empty_Output_FeatureClass()

                # Execute function to buffer the clipped hurricane feature.
                self.func_FeatureClass_Buffer(self.clipped_Output_FeatureClass,
                                "buffered_" + self.clipped_Output_FeatureClass)

                # Execute function that controls analysis options.
                self.func_Controls_For_Analysis_Options(
                    self.featureClass_County_State_Naming)

        except Exception as e:

            # Display error message.
            self.func_Scroll_setOutputText("Error Message: " + str(e) + "\n" +
                                           "Traceback: " +
                                           traceback.format_exc(), color_Red)

    def func_Download_Unzip_Census_Shapefile(self):

        # This function controls the download and and unzipping of the Shapefile
        # obtained from the US Census Bureau.

        try:

            # Create subfolder naming variable for location to save Shapefile.
            self.subFolder_CensusShapefile = self.subFolder_GIS + \
                                             "/Census_Shapefile/"

            self.func_Scroll_setOutputText(
                "Creating Census Shapefile subfolder...", None)

            # If subfolder does not already exist, create it.
            if not os.path.exists(self.subFolder_CensusShapefile):
                os.makedirs(self.subFolder_CensusShapefile)

                self.func_Scroll_setOutputText(
                    "Census Shapefile subfolder created.", None)

            # Increment progress bar.
            self.func_ProgressBar_setProgress(43)

            # Pause script for half a second.
            sleep(0.5)

            try:

                self.func_Scroll_setOutputText(
                    "Downloading US Census Shapefile...", None)

                # Attempt to download the Shapefile.
                request.urlretrieve(census_URL_CountyShapefile,
                                    self.subFolder_CensusShapefile + "/" +
                                    census_URL_CountyShapefile_FileName +
                                    fileExtZip)

                self.func_Scroll_setOutputText(
                    "US Census Shapefile Downloaded.", None)

            # If download fails, try one more time (it could have been
            # a small, temporary network glitch).
            except:

                self.func_Scroll_setOutputText(
                    "Download failed, trying again...", color_Orange)

                sleep(5)

                # Attempt to download the Shapefile.
                request.urlretrieve(census_URL_CountyShapefile,
                                    self.subFolder_CensusShapefile + "/" +
                                    census_URL_CountyShapefile_FileName +
                                    fileExtZip)

                self.func_Scroll_setOutputText(
                    "US Census Shapefile Downloaded.", None)

            # Increment progress bar.
            self.func_ProgressBar_setProgress(49)

            # Pause script for half a second.
            sleep(0.5)

            self.func_Scroll_setOutputText(
                "Unzipping US Census Shapefile...", None)

            # Unzip the Shapefile within the same Shapefile subfolder.
            unZipThisFile = zipfile.ZipFile(self.subFolder_CensusShapefile +
                                    "/" + census_URL_CountyShapefile_FileName +
                                    fileExtZip, 'r')
            unZipThisFile.extractall(self.subFolder_CensusShapefile)

            # Close file to prevent locks.
            unZipThisFile.close()

            self.func_Scroll_setOutputText(
                "US Census Shapefile unzipped.", None)

            # Increment progress bar.
            self.func_ProgressBar_setProgress(52)

        except HTTPError as httpError:

            # Display error message for URL-specific problems.
            self.func_Scroll_setOutputText(str(httpError), color_Red)

            messagebox.showerror(errorMessage_Header,
                                 "Unable to access web URL.\n"
                                 "Perhaps the website's URL is missing, "
                                 "offline, or down for maintenance?\n"
                                 "Please check URL connection and try again.")


        except URLError as urlError:

            # Display error message for internet connectivity-specific problems.
            self.func_Scroll_setOutputText(str(urlError), color_Red)

            messagebox.showerror(errorMessage_Header,
                                 "Unable to access internet connectivity.\n"
                                 "Possibly temporary internet issues?\n"
                                 "Please check connection and try again.")

        except Exception as e:

            # Display error messages for all other errors.
            self.func_Scroll_setOutputText("Error Message: " + str(e) + "\n" +
                                           "Traceback: " +
                                           traceback.format_exc(), color_Red)

    def func_Extract_50_States_and_DC_Only(self, censusShapefile, fileGDB_Path):

        # This function controls the process of extracting the 50 states and
        # Washington DC from the Census Bureau's Shapefile and performing
        # various modifications to that data.

        try:

            self.func_Scroll_setOutputText(
                "Copying Census Shapefile to File GDB...", None)

            # Copy the Census Shapefile to a feature class within the File GDB.
            arcpy.CopyFeatures_management(censusShapefile,
                                          fileGDB_Path + "/" +
                                          featureClass_50States_and_DC_only)

            # Display geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            self.func_Scroll_setOutputText(
                "Census Shapefile copied to File GDB.", None)

            # Pause script for one second.
            sleep(1)

            self.func_Scroll_setOutputText(
                "Extracting 50 States and DC from Feature Class...", None)

            # Open the Census feature class with an Update Cursor.
            # Attribute field set to the state's FIPS code.
            with arcpy.da.UpdateCursor(fileGDB_Path + "/" +
                                    featureClass_50States_and_DC_only,
                                    census_Shapefile_Field_StateFIPS) as cursor:

                # For each feature in the Census feature class.
                for row in cursor:

                    # This If statement removes non-50 state (and DC) FIPS codes
                    # from the Census feature class. The original data includes
                    # all US territories, and those FIPS codes must be removed.
                    if row[0] == "60" or row[0] == "66" or row[0] == "69" or \
                            row[0] == "72" or row[0] == "78":

                        # Delete polygon feature.
                        cursor.deleteRow()

            # Display geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            self.func_Scroll_setOutputText(
                "50 States and DC extracted from Feature Class.", None)

            # Set the workspace within the File GDB for the following tasks.
            arcpy.env.workspace = fileGDB_Path

            # Set naming convention variable for projecting Census feature
            # class.
            self.featureClass_Polygons_Projected = \
                featureClass_50States_and_DC_only + "_Projected"

            self.func_Scroll_setOutputText("Projecting feature class to PCS " +
                            pcsReferenceString +
                            " with Central Meridian Offset (-30.0 degrees)...",
                            None)

            # Project the Census feature class to the designated PCS as a new
            # feature class within the File GDB.
            arcpy.Project_management(featureClass_50States_and_DC_only,
                                     self.featureClass_Polygons_Projected,
                                     pcsReference)

            # Display geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            self.func_Scroll_setOutputText("PCS Projection to " +
                                           pcsReferenceString + " completed.",
                                           None)

            self.func_Scroll_setOutputText(
                "Recalculating extent for feature class...", None)

            # Recalculate extent of the projected Census feature class.
            arcpy.RecalculateFeatureClassExtent_management(
                self.featureClass_Polygons_Projected)

            # Display geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            self.func_Scroll_setOutputText("Feature class extent recalculated.",
                                           None)

            self.func_Scroll_setOutputText("Deleting feature class " +
                                           featureClass_50States_and_DC_only +
                                           " from File GDB...", None)

            # Delete the original, pre-projected Census feature class from the
            # File GDB. It is no longer needed.
            arcpy.Delete_management(featureClass_50States_and_DC_only)

            # Get geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            self.func_Scroll_setOutputText(
                "Feature class deleted from File GDB.", None)

            self.func_Scroll_setOutputText("Renaming feature class " +
                                    self.featureClass_Polygons_Projected +
                                    " back to " +
                                    featureClass_50States_and_DC_only + "...",
                                    None)

            # Rename the projected Census feature class to the original naming
            # convention of the feature class that was just deleted.
            arcpy.Rename_management(self.featureClass_Polygons_Projected,
                                    featureClass_50States_and_DC_only)

            # Get geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            self.func_Scroll_setOutputText("Feature class has been renamed.",
                                           None)

        except arcpy.ExecuteError:

            # Display geoprocessing error messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Red)

        except Exception as e:

            # Display error messages for all other errors.
            self.func_Scroll_setOutputText("Error Message: " + str(e) + "\n" +
                                           "Traceback: " +
                                           traceback.format_exc(), color_Red)

    def func_Extract_State_Selection_Only(self, censusShapefile, fileGDB_Path):

        # This function controls the process of extracting the user-selected
        # state from the Census Bureau's Shapefile and performing various
        # modifications to that data.

        try:

            self.func_Scroll_setOutputText(
                "Copying Census Shapefile to File GDB...", None)

            # Copy the Census Shapefile to a feature class within the File GDB.
            arcpy.CopyFeatures_management(censusShapefile, fileGDB_Path + "/" +
                                        self.featureClass_State_Selection_Only)

            # Get geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            self.func_Scroll_setOutputText(
                "Census Shapefile copied to File GDB.", None)

            # Pause script for one second.
            sleep(1)

            self.func_Scroll_setOutputText("Extracting state selection(" +
                                           self.stringState_Name.get() +
                                           ") from Feature Class...", None)

            # Open the Census feature class with an Update Cursor.
            # Attribute field set to the state's FIPS code.
            with arcpy.da.UpdateCursor(fileGDB_Path + "/" +
                                    self.featureClass_State_Selection_Only,
                                    census_Shapefile_Field_StateFIPS) as cursor:

                # For each feature in the Census feature class...
                for row in cursor:

                    # This If statement removes all polygons not affiliated with
                    # the user-selected state's FIPS code. This is accessed
                    # from the state name/state FIPS dictionary.
                    if row[0] != \
                            dict_StateName_StateFIPs.get(
                                self.stringState_Name.get()):

                        # Delete polygon feature.
                        cursor.deleteRow()

            # Get geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            self.func_Scroll_setOutputText("State selection(" +
                                           self.stringState_Name.get() +
                                           ") extracted from Feature Class.",
                                           None)

            # Set workspace for the following tasks.
            arcpy.env.workspace = fileGDB_Path

            # Set naming convention variable for projecting Census feature
            # class.
            self.featureClass_Polygons_Projected = \
                self.featureClass_State_Selection_Only + "_Projected"

            self.func_Scroll_setOutputText("Projecting feature class to PCS " +
                            pcsReferenceString +
                            " with Central Meridian Offset (-30.0 degrees)...",
                            None)

            # Project the Census feature class to the designated PCS as a new
            # feature class within the File GDB.
            arcpy.Project_management(self.featureClass_State_Selection_Only,
                                     self.featureClass_Polygons_Projected,
                                     pcsReference)

            # Get geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            self.func_Scroll_setOutputText("PCS Projection to " +
                                           pcsReferenceString + " completed.",
                                           None)

            self.func_Scroll_setOutputText(
                "Recalculating extent for feature class...",
                None)

            # Recalculate extent of the projected Census feature class.
            arcpy.RecalculateFeatureClassExtent_management(
                self.featureClass_Polygons_Projected)

            # Get geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            self.func_Scroll_setOutputText("Feature class extent recalculated.",
                                           None)

            self.func_Scroll_setOutputText("Deleting feature class " +
                                        self.featureClass_State_Selection_Only +
                                        " from File GDB...", None)

            # Delete the original, pre-projected Census feature class from the
            # File GDB. It is no longer needed.
            arcpy.Delete_management(self.featureClass_State_Selection_Only)

            # Get geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            self.func_Scroll_setOutputText(
                "Feature class deleted from File GDB.", None)

            self.func_Scroll_setOutputText("Renaming feature class " +
                                self.featureClass_Polygons_Projected +
                                " back to " +
                                self.featureClass_State_Selection_Only + "...",
                                None)

            # Rename the projected Census feature class to the original naming
            # convention of the feature class that was just deleted.
            arcpy.Rename_management(self.featureClass_Polygons_Projected,
                                    self.featureClass_State_Selection_Only)

            # Get geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            self.func_Scroll_setOutputText("Feature class has been renamed.",
                                           None)

        except arcpy.ExecuteError:

            # Display geoprocessing error messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Red)

        except Exception as e:

            # Display error messages for all other errors.
            self.func_Scroll_setOutputText("Error Message: " + str(e) + "\n" +
                                           "Traceback: " +
                                           traceback.format_exc(), color_Red)

    def func_Extract_County_Selection_Only(self, censusShapefile, fileGDB_Path):

        # This function controls the process of extracting the user-selected
        # county from the Census Bureau's Shapefile and performing various
        # modifications to that data.

        try:

            self.func_Scroll_setOutputText(
                "Copying Census Shapefile to File GDB...", None)

            # Copy the Census Shapefile to a feature class within the File GDB.
            arcpy.CopyFeatures_management(censusShapefile, fileGDB_Path + "/" +
                                          self.featureClass_County_State_Naming)

            # Get geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            self.func_Scroll_setOutputText(
                "Census Shapefile copied to File GDB.", None)

            # Pause script for one second.
            sleep(1)

            self.func_Scroll_setOutputText("Extracting (" +
                                           self.stringCounty_Name.get() +
                                           ", " + self.stringState_Name.get() +
                                           ") from Feature Class...", None)

            # Open the Census feature class with an Update Cursor.
            # Field names set to the state's FIPS code and county names.
            with arcpy.da.UpdateCursor(fileGDB_Path + "/" +
                                self.featureClass_County_State_Naming,
                                field_names=[census_Shapefile_Field_StateFIPS,
                                census_Shapefile_Field_CountyName]) as cursor:

                # For each feature in the Census feature class...
                for row in cursor:

                    # If the feature's state FIPS code matches the user-selected
                    # state's FIPS code...
                    if row[0] == dict_StateName_StateFIPs.get(
                            self.stringState_Name.get()):

                        # If the feature's county name matches the user-selected
                        # county name within the matching state FIPS code...
                        if row[1] == self.stringCounty_Name.get():

                            # Do nothing, leave that record within the feature
                            # class.
                            pass

                        else:

                            # Delete the feature from the feature class, as it
                            # is not a match.
                            cursor.deleteRow()

                    else:

                        # Else, delete the feature as the state FIPS code does
                        # not match the user-selected state.
                        cursor.deleteRow()

            # Get geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            self.func_Scroll_setOutputText(self.stringCounty_Name.get() + ", " +
                                           self.stringState_Name.get() +
                                           " extracted from Feature Class.",
                                           None)

            # Set workspace for the following tasks.
            arcpy.env.workspace = fileGDB_Path

            # Set naming convention variable for projecting Census feature
            # class.
            self.featureClass_Polygons_Projected = \
                self.featureClass_County_State_Naming + "_Projected"

            self.func_Scroll_setOutputText("Projecting feature class to PCS " +
                            pcsReferenceString +
                            " with Central Meridian Offset (-30.0 degrees)...",
                            None)

            # Project the Census feature class to the designated PCS as a new
            # feature class within the File GDB.
            arcpy.Project_management(self.featureClass_County_State_Naming,
                                     self.featureClass_Polygons_Projected,
                                     pcsReference)

            # Get geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            self.func_Scroll_setOutputText("PCS Projection to " +
                                           pcsReferenceString + " completed.",
                                           None)

            self.func_Scroll_setOutputText(
                "Recalculating extent for feature class...", None)

            # Recalculate extent of the projected Census feature class.
            arcpy.RecalculateFeatureClassExtent_management(
                self.featureClass_Polygons_Projected)

            # Get geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            self.func_Scroll_setOutputText("Feature class extent recalculated.",
                                           None)

            self.func_Scroll_setOutputText("Deleting feature class " +
                                        self.featureClass_County_State_Naming +
                                        " from File GDB...", None)

            # Delete the original, pre-projected Census feature class from the
            # File GDB. It is no longer needed.
            arcpy.Delete_management(self.featureClass_County_State_Naming)

            # Get geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            self.func_Scroll_setOutputText(
                "Feature class deleted from File GDB.", None)

            self.func_Scroll_setOutputText("Renaming feature class " +
                                self.featureClass_Polygons_Projected +
                                " back to " +
                                self.featureClass_County_State_Naming + "...",
                                None)

            # Rename the projected Census feature class to the original naming
            # convention of the feature class that was just deleted.
            arcpy.Rename_management(self.featureClass_Polygons_Projected,
                                    self.featureClass_County_State_Naming)

            # Get geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            self.func_Scroll_setOutputText("Feature class has been renamed.",
                                           None)

        except arcpy.ExecuteError:

            # Display geoprocessing error messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Red)

        except Exception as e:

            # Display error messages for all other errors.
            self.func_Scroll_setOutputText("Error Message: " + str(e) + "\n" +
                                           "Traceback: " +
                                           traceback.format_exc(), color_Red)

    def func_FeatureClass_Clip(self, inputFC, clipFC, outputFC_Name):

        # This function controls the processes involved with clipping the
        # hurricane line feature class to the user-selected Census polygon
        # boundary feature class.

        try:

            # Set the workspace to the File GDB for the following tasks.
            arcpy.env.workspace = self.subFolder_GIS + "/" + nameFileGDB

            # Buffer parameters.
            required_InputFile = clipFC
            required_OutputFile = "in_memory/bufferedStates"
            required_BufferDistance = "49.9 Miles"
            optional_LineSide = None
            optional_LineEndType = None
            optional_DissolveOption = None
            optional_DissolveField = None
            optional_Method = None

            arcpy.Buffer_analysis(required_InputFile, required_OutputFile,
                            required_BufferDistance, optional_LineSide,
                            optional_LineEndType, optional_DissolveOption,
                            optional_DissolveField, optional_Method)

            # Set a new variable name for clipping based on this argument.
            self.clipped_Output_FeatureClass = outputFC_Name

            # If the user selects USA...
            if self.radioButton_Selection == 1:

                # Display this particular message before executing the clip.
                self.func_Scroll_setOutputText(
                    "Clipping hurricane features to 50 states and DC "
                    "(with ~50 mile buffer)...", None)

            # If the user selects State...
            elif self.radioButton_Selection == 2:

                # Display this particular message before executing the clip.
                self.func_Scroll_setOutputText(
                    "Clipping hurricane features to state selection(" +
                    self.stringState_Name.get() + ") with ~50 mile buffer...",
                    None)

            # If the user selects County...
            elif self.radioButton_Selection == 3:

                # Display this particular message before executing the clip.
                self.func_Scroll_setOutputText(
                    "Clipping hurricane features to " +
                    self.stringCounty_Name.get() + ", " +
                    self.stringState_Name.get() + " with ~50 mile buffer...",
                    None)

            # Perform a clip of the hurricane line features to the specified
            # polygon boundary.
            arcpy.Clip_analysis(inputFC, "in_memory/bufferedStates",
                                self.clipped_Output_FeatureClass)

            # Display geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            #Create empty list for storing storm feature information.
            stormList = []

            # Search the clipped hurricane feature class via SearchCursor.
            with arcpy.da.SearchCursor(self.clipped_Output_FeatureClass,
                                       [analysis_HurrCode_Field,
                                        analysis_HurrName_Field]) as cursor:

                # For each feature in the cursor...
                for row in cursor:

                    # Add the storm names to the stormList.
                    stormList.append(row[0] + ": " + row[1] + ",")

            # Gets the unique storm names and counts how many exist.
            text_UniqueNames = numpy.unique((stormList))
            int_StormCount = len(numpy.unique((stormList)))

            # If the user selects USA...
            if self.radioButton_Selection == 1:

                # Store the integer hurricane count as a variable for use within
                # other functions.
                self.nationwide_storm_count = int_StormCount

                # Store the nationwide list of unique hurricane storm names for
                # use within other functions.
                self.nationwide_storm_names = text_UniqueNames

                # Display this particular message after executing the clip.
                self.func_Scroll_setOutputText(
                    str(self.nationwide_storm_count) + " storms have been "
                    "clipped to 50 states and DC.", None)

            # If the user selects State...
            if self.radioButton_Selection == 2:

                # Store the integer hurricane count as a variable for use within
                # other functions.
                self.state_storm_count = int_StormCount

                # Store the statewide list of unique hurricane storm names for
                # use within other functions.
                self.state_storm_names = text_UniqueNames

                # Display this particular message after executing the clip.
                self.func_Scroll_setOutputText(
                    str(self.state_storm_count) + " storms have been "
                    "clipped to state selection(" +
                    self.stringState_Name.get() + ").", None)

            # If the user selects County...
            if self.radioButton_Selection == 3:

                # Store the integer hurricane count as a variable for use within
                # other functions.
                self.county_storm_count = int_StormCount

                # Store the countywide list of unique hurricane storm names for
                # use within other functions.
                self.county_storm_names = text_UniqueNames

                # Display this particular message after executing the clip.
                self.func_Scroll_setOutputText(
                    str(self.county_storm_count) + " storms have been clipped "
                    "to " + self.stringCounty_Name.get() + ", " +
                    self.stringState_Name.get() + ".", None)

            # Clear any in memory storage.
            self.func_Clear_InMemory()

            # Increment progress bar.
            self.func_ProgressBar_setProgress(64)

        except arcpy.ExecuteError:

            # Display geoprocessing-specific errors.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Red)

        except Exception as e:

            # Display all other types of errors.
            self.func_Scroll_setOutputText("Error Message: " + str(e) + "\n" +
                                           "Traceback: " +
                                           traceback.format_exc(), color_Red)

    def func_Check_If_Empty_Output_FeatureClass(self):

        # This function controls the processes that check to ensure the clipped
        # hurricane line feature class still have features once clipped.

        # If user selects USA...
        if self.radioButton_Selection == 1:

            test_StormCount = self.nationwide_storm_count

        # If user selects State...
        if self.radioButton_Selection == 2:

            test_StormCount = self.state_storm_count

        # If user selects County...
        if self.radioButton_Selection == 3:

            test_StormCount = self.county_storm_count

        # If zero storm systems present within the feature class...
        if test_StormCount < 1:

            # Display this message and error message to the user, since the
            # script can't proceed any farther.
            self.func_Scroll_setOutputText("No hurricane polyline features "
                        "present within the timespan/intensity/location.\n" +
                        "Unable to continue with analysis.", color_Red)

            messagebox.showerror(errorMessage_Header,
                                 "No hurricane polyline features present within"
                                 " the timespan/intensity/location.\n" +
                                 "Unable to continue with analysis.")

            # Re-enable all selectable buttons and drop-down lists.
            self.func_Enable_Buttons()

            # Stop the status bar.
            self.func_StopStatusBar()

            # Increment progress bar to 100 percent.
            self.func_ProgressBar_setProgress(100)

            # Calculate total script processing time.
            self.func_Calculate_Script_Time()

            # Save all scroll box text to file.
            self.func_Scroll_saveOutputText()

            # Exit the process.
            exit()

    def func_FeatureClass_Buffer(self, inputClippedFC, outputBufferedFC):

        # This function controls the processes involved with buffering the
        # clipped hurricane line feature class.

        try:

            # Set the workspace to the File GDB for the following tasks.
            arcpy.env.workspace = self.subFolder_GIS + "/" + nameFileGDB

            # Set a new variable name for buffered output naming convention.
            # This will be used in later processes.
            self.buffered_Output_FeatureClass = outputBufferedFC

            # Display this particular message before executing the clip.
            self.func_Scroll_setOutputText("Creating 50 mile buffer to the "
                            "left/right of clipped hurricane paths", None)

            # Buffer parameters
            required_InputFeatureClass = inputClippedFC
            required_OutputFeatureClass = outputBufferedFC
            required_BufferDistanceMiles = "50 Miles"
            optional_LineSide = "FULL" # This is default for left/right sides.
            optional_LineEndType = "ROUND" # "ROUND"  # Flat or Round
            optional_DissolveOption = "NONE"
            optional_DissolveField = None
            optional_Method = None

            # Perform a buffer of the hurricane line features.
            arcpy.Buffer_analysis(required_InputFeatureClass,
                            required_OutputFeatureClass,
                            required_BufferDistanceMiles, optional_LineSide,
                            optional_LineEndType, optional_DissolveOption,
                            optional_DissolveField, optional_Method)

            # Display geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            # Display this particular message after executing the clip.
            self.func_Scroll_setOutputText(
                "Clipped hurricane features have been buffered.", None)

            # Increment progress bar.
            self.func_ProgressBar_setProgress(67)

        except arcpy.ExecuteError:

            # Display geoprocessing-specific errors.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Red)

        except Exception as e:

            # Display all other types of errors.
            self.func_Scroll_setOutputText("Error Message: " + str(e) + "\n" +
                                           "Traceback: " +
                                           traceback.format_exc(), color_Red)

    def func_Controls_For_Analysis_Options(self, featureClass_Mask):

        # This function controls the analysis geoprocessing options, if selected
        # by the user.

        # Set the initial progress bar value for all analyses to the following
        # value. As each analysis completes, the value will be incremented by
        # three percent.
        self.analysis_Percentage_Counter = 67

        try:

            # If the user chooses to output the count results to CSV file...
            if self.statusAnalysis_OutputToCSVFile.get() == 1:

                # Execute function to create CSV folder for output data counts
                # file to be stored.
                self.func_Create_CSV_subFolder()

                self.func_Scroll_setOutputText(
                    "Compiling count results to CSV file...", None)

                # Set the workspace for the following analysis.
                arcpy.env.workspace = self.subFolder_GIS + "/" + nameFileGDB

                # If the user selects USA clipping option...
                if self.radioButton_Selection == 1:

                    # Execute function to retrieve global storm count.
                    self.func_CSV_DataCount_Global_Count()

                    required_InputFile = [self.buffered_Output_FeatureClass,
                                            featureClass_50States_and_DC_only]
                    required_OutputFile = "temp_union"
                    optional_JoinAttributes = None
                    optional_ClusterTolerance = None
                    optional_Gaps = None

                    # Perform union of buffered hurricane feature class
                    # and the USA polygon feature class. Store output in_memory.
                    arcpy.Union_analysis(required_InputFile,
                                         required_OutputFile,
                                         optional_JoinAttributes,
                                         optional_ClusterTolerance,
                                         optional_Gaps)

                    # Create/Open a new CSV file within the CSV subfolder for
                    # data counts to be written into.
                    csvFile = open(self.csvDirectory + "DataCounts_" +
                                   self.name_Hurr_FeatureClass +
                                   self.folderNamingAddition + fileExtCSV, "w")

                    # If timespan and intensity drop-downs don't show Custom...
                    if self.stringHurricaneTimespan.get() != "Custom..." and \
                            self.stringHurricaneIntensity.get() != "Custom...":

                        # Write the following lines into the data counts CSV.
                        csvFile.write("Timespan:," +
                                    self.stringHurricaneTimespan.get() + ",\n")
                        csvFile.write("Intensity Range (Knots):," +
                                    self.stringHurricaneIntensity.get() + ",\n")

                    # If timespan drop-down shows Custom and intensity doesn't..
                    if self.stringHurricaneTimespan.get() == "Custom..." and \
                            self.stringHurricaneIntensity.get() != "Custom...":

                        # WRite the following lines into the data counts CSV.
                        csvFile.write("Timespan:," + self.textCustomYearFrom +
                                      self.textCustomMonthFrom.zfill(2) +
                                      "-" + self.textCustomYearTo +
                                      self.textCustomMonthTo.zfill(2) + ",\n")
                        csvFile.write("Intensity Range (Knots):," +
                                    self.stringHurricaneIntensity.get() + ",\n")

                    # If timespan and intensity drop-downs both show Custom...
                    if self.stringHurricaneTimespan.get() == "Custom..." and \
                            self.stringHurricaneIntensity.get() == "Custom...":

                        # Write the following lines into the data counts CSV.
                        csvFile.write("Timespan:," + self.textCustomYearFrom +
                                      self.textCustomMonthFrom.zfill(2) +
                                      "-" + self.textCustomYearTo +
                                      self.textCustomMonthTo.zfill(2) + ",\n")
                        csvFile.write("Intensity Range (Knots):," +
                                      self.textCustomIntensityFrom + "-" +
                                      self.textCustomIntensityTo + ",\n")

                    # If timespan drop-down doesn't show Custom and Intensity
                    # does...
                    if self.stringHurricaneTimespan.get() != "Custom..." and \
                            self.stringHurricaneIntensity.get() == "Custom...":

                        # Write the following lines into the data counts CSV.
                        csvFile.write("Timespan:," +
                                    self.stringHurricaneTimespan.get() + ",\n")
                        csvFile.write("Intensity Range (Knots):," +
                                      self.textCustomIntensityFrom + "-" +
                                      self.textCustomIntensityTo + ",\n")

                    # Now write the following lines, regardless of
                    # timespan/intensity selection.
                    csvFile.write("\n")
                    csvFile.write(
                        "Note: All US locations include 50 mile buffer.,\n")
                    csvFile.write("\n")
                    csvFile.write("Worldwide Storm Count:," +
                                  str(self.worldwide_storm_count) + ",\n")
                    csvFile.write("USA (and DC) Storms:," +
                                  str(self.nationwide_storm_count) + ",\n")
                    csvFile.write("\n")
                    csvFile.write("Nationwide Hurricane Data,\n")
                    csvFile.write("V,V,V,V,V,\n")
                    csvFile.write("Minimum Intensity,Maximum Intensity,"
                                  "Mean Intensity,Median Intensity,"
                                  "Mode Intensity,\n")

                    # Create empty list to store all US intensity values.
                    magList_US = []

                    # Open the temp_union feature class as a Search Cursor,
                    # with analysis fields set to FIPS code and intensity.
                    with arcpy.da.SearchCursor("temp_union",
                                            [census_Shapefile_Field_StateFIPS,
                                            analysis_Mag_Field]) as cursor:

                        # For each feature within the spatial join...
                        for row in cursor:

                            if row[1] > 0:

                                # Append hurricane intensities to magList_US.
                                magList_US.append(row[1])

                    try:

                        # Calculate mode of all intensities within list.
                        modeValue_US = mode(magList_US)

                        # Convert mode information to float and then to
                        # string with two decimal places.
                        modeString_US = \
                                    str("{0:.2f}".format(float(modeValue_US)))

                    except StatisticsError:

                            # This catches any lists containing no mode.
                            # This will occur if all values within list are
                            # unique values.

                            # Assign modeString to the following phrase.
                        modeString_US = "No Unique Mode"

                        pass

                        # Write the following data to the data counts CSV.
                        # Min intensity, max intensity, mean intensity, median
                        # intensity, and mode intensity.
                    csvFile.write(str(min(magList_US)) + "," +
                                str(max(magList_US)) + "," +
                                str("{0:.2f}".format(numpy.mean(magList_US)) +
                                "," +
                                str("{0:.2f}".format(
                                    numpy.median(magList_US))) + "," +
                                modeString_US + "," + ",\n"))

                    csvFile.write("\n")
                    csvFile.write("Nationwide Storm Name(s):,")

                    for eachStorm in self.nationwide_storm_names:

                        csvFile.write(eachStorm)

                    csvFile.write("\n\n")
                    csvFile.write("Storm Data per State,\n")
                    csvFile.write("V,V,V,V,V,V,V,V,\n")
                    csvFile.write("States with Storms,Storm Count,"
                                  "Minimum Intensity,Maximum Intensity,"
                                  "Mean Intensity,Median Intensity,"
                                  "Mode Intensity,State FIPS Code,\n")

                    # Create empty list for storing hurricane values per state.
                    hurrList = []

                    # Create empty list for storing hurricane intensity values
                    # per state.
                    magList = []

                    # For each state value in the ordered dictionary...
                    for key in dictKeys_OrderedDict_StateNames:

                        # Set counter to zero, for counting hurricane within
                        # each state during loop.
                        counter = 0

                        # Clears hurrList after each state count has concluded.
                        hurrList.clear()

                        # Clears magList after each state count has concluded.
                        magList.clear()

                        # Open the in_memory spatial join as a Search Cursor,
                        # with analysis fields set to FIPS code and intensity.
                        with arcpy.da.SearchCursor("temp_union",
                                            [census_Shapefile_Field_StateFIPS,
                                            analysis_HurrCode_Field,
                                            analysis_Mag_Field]) as cursor:

                            # For each feature within the spatial join...
                            for row in cursor:

                                # If FIPS code matches a state in the ordered
                                # dictionary and the wind speed is above 0...
                                if row[0] == \
                                    dictKeys_OrderedDict_StateNames[key] and \
                                    row[2] > 0:

                                    # Append hurricane names to hurrList.
                                    hurrList.append(row[1])

                                    # Append hurricane intensities to magList.
                                    magList.append(row[2])

                                    # Increment counter by one.
                                    counter = counter + 1

                        # If counter is greater than zero...
                        if counter > 0:

                            try:

                                # Calculate mode of all intensities within list.
                                modeValue = mode(magList)

                                # Convert mode information to float and then to
                                # string with two decimal places.
                                modeString = \
                                    str("{0:.2f}".format(float(modeValue)))

                            except StatisticsError:

                                # This catches any lists containing no mode.
                                # This will occur if all values within list are
                                # unique values.

                                # Assign modeString to the following phrase.
                                modeString = "No Unique Mode"

                                pass

                            # Identify and count the unique storm names within
                            # hurrList. The length (count) of the uniqueNames
                            # variable will reveal how many hurricanes occurred.
                            uniqueNameCount = len(numpy.unique((hurrList)))

                            # Write the following data to the data counts CSV.
                            # State name, how many hurricanes, min mag, max
                            # mag, mean mag, median mag, mode mag, and FIPs.
                            csvFile.write(str(key) + "," +
                                str(uniqueNameCount) + "," +
                                str(min(magList)) + "," + str(max(magList)) +
                                "," +
                                str("{0:.2f}".format(numpy.mean(magList)) +
                                "," +
                                str("{0:.2f}".format(numpy.median(magList))) +
                                "," + modeString + "," +
                                str(dictKeys_OrderedDict_StateNames[key]) +
                                ",\n"))

                    # Close the data counts CSV file.
                    csvFile.close()

                # If the user selects State clipping option...
                if self.radioButton_Selection == 2:

                    # Import the tuples and dictionaries affiliated with states
                    # and counties.
                    import GUI_CountiesPerState

                    # Execute function to retrieve global storm count.
                    self.func_CSV_DataCount_Global_Count()

                    # Execute function to retrieve nationwide storm count.
                    self.func_CSV_DataCount_Nationwide_Count()

                    required_InputFile = [self.buffered_Output_FeatureClass,
                                        self.featureClass_State_Selection_Only]
                    required_OutputFile = "temp_union"
                    optional_JoinAttributes = None
                    optional_ClusterTolerance = None
                    optional_Gaps = None

                    # Perform union of buffered hurricane feature class
                    # and the USA polygon feature class. Store output in_memory.
                    arcpy.Union_analysis(required_InputFile,
                                         required_OutputFile,
                                         optional_JoinAttributes,
                                         optional_ClusterTolerance,
                                         optional_Gaps)

                    # Create/Open a new CSV file within the CSV subfolder for
                    # data counts to be written into.
                    csvFile = open(self.csvDirectory + "DataCounts_" +
                                   self.name_Hurr_FeatureClass +
                                   self.folderNamingAddition + fileExtCSV, "w")

                    # If timespan and intensity drop-downs don't show Custom...
                    if self.stringHurricaneTimespan.get() != "Custom..." and \
                            self.stringHurricaneIntensity.get() != "Custom...":

                        # Write the following lines into the data counts CSV.
                        csvFile.write("Timespan:," +
                                      self.stringHurricaneTimespan.get() +
                                      ",\n")
                        csvFile.write("Intensity Range (Knots):," +
                                      self.stringHurricaneIntensity.get() +
                                      ",\n")

                    # If timespan drop-down shows Custom and intensity drop-down
                    # doesn't show Custom...
                    if self.stringHurricaneTimespan.get() == "Custom..." and \
                            self.stringHurricaneIntensity.get() != "Custom...":

                        # Write the following lines into the data counts CSV.
                        csvFile.write("Timespan:," + self.textCustomYearFrom +
                                      self.textCustomMonthFrom.zfill(2) +
                                      "-" + self.textCustomYearTo +
                                      self.textCustomMonthTo.zfill(2) + ",\n")
                        csvFile.write("Intensity Range (Knots):," +
                                    self.stringHurricaneIntensity.get() + ",\n")

                    # If timespan drop-down shows Custom and intensity drop-down
                    # shows Custom...
                    if self.stringHurricaneTimespan.get() == "Custom..." and \
                            self.stringHurricaneIntensity.get() == "Custom...":

                        # Write the following lines into the data counts CSV.
                        csvFile.write("Timespan:," + self.textCustomYearFrom +
                                      self.textCustomMonthFrom.zfill(2) +
                                      "-" + self.textCustomYearTo +
                                      self.textCustomMonthTo.zfill(2) + ",\n")
                        csvFile.write("Intensity Range (Knots):," +
                                      self.textCustomIntensityFrom + "-" +
                                      self.textCustomIntensityTo + ",\n")

                    # If timespan drop-down doesn't show Custom and intensity
                    # drop-down shows Custom...
                    if self.stringHurricaneTimespan.get() != "Custom..." and \
                            self.stringHurricaneIntensity.get() == "Custom...":

                        # Write the following lines into the data counts CSV.
                        csvFile.write("Timespan:," +
                                      self.stringHurricaneTimespan.get() + ",\n")
                        csvFile.write("Intensity Range (Knots):," +
                                      self.textCustomIntensityFrom + "-" +
                                      self.textCustomIntensityTo + ",\n")

                    # Now write the following lines, regardless of
                    # timespan/intensity selection.
                    csvFile.write("\n")
                    csvFile.write(
                        "Note: All US locations include 50 mile buffer.,\n")
                    csvFile.write("\n")
                    csvFile.write("Worldwide Storm Count:," +
                                  str(self.worldwide_storm_count) + ",\n")
                    csvFile.write("USA (and DC) Storms:," +
                                  str(self.nationwide_storm_count) + ",\n")
                    csvFile.write("\n")
                    csvFile.write("State Storms - " +
                                  str(self.stringState_Name.get()) +
                                  " (FIPS: " +
                                  str(dictKeys_OrderedDict_StateNames[
                                          self.stringState_Name.get()]) +
                                  "):," + str(self.state_storm_count) + ",\n")
                    csvFile.write("\n")
                    csvFile.write("Statewide Hurricane Data,\n")
                    csvFile.write("V,V,V,V,V,\n")
                    csvFile.write("Minimum Intensity,Maximum Intensity,"
                                  "Mean Intensity,Median Intensity,"
                                  "Mode Intensity,\n")

                    # Create empty list to store all state intensity values.
                    magList_State = []

                    # Open the in_memory spatial join as a Search Cursor,
                    # with analysis fields set to FIPS code and intensity.
                    with arcpy.da.SearchCursor("temp_union",
                                            [census_Shapefile_Field_StateFIPS,
                                            analysis_Mag_Field]) as cursor:

                        # For each feature within the spatial join...
                        for row in cursor:

                            # If the intensity field is greater than zero...
                            if row[1] > 0:

                                # Append hurricane intensities to magList_State.
                                magList_State.append(row[1])

                    try:

                        # Calculate mode of all intensities within list.
                        modeValue_State = mode(magList_State)

                        # Convert mode information to float and then to
                        # string with two decimal places.
                        modeString_State = \
                                    str("{0:.2f}".format(
                                        float(modeValue_State)))

                    except StatisticsError:

                            # This catches any lists containing no mode.
                            # This will occur if all values within list are
                            # unique values.

                            # Assign modeString to the following phrase.
                        modeString_State = "No Unique Mode"

                        pass

                        # Write the following data to the data counts CSV.
                        # Min intensity, max intensity, mean intensity, median
                        # intensity, and mode intensity.
                    csvFile.write(str(min(magList_State)) + "," +
                                str(max(magList_State)) + "," +
                                str("{0:.2f}".format(
                                    numpy.mean(magList_State)) + "," +
                                str("{0:.2f}".format(
                                    numpy.median(magList_State))) + "," +
                                modeString_State + "," + ",\n"))

                    csvFile.write("\n")
                    csvFile.write("State Storm Name(s):,")

                    for eachStorm in self.state_storm_names:

                        csvFile.write(eachStorm)

                    csvFile.write("\n\n")
                    csvFile.write("Storm Data per County\n")
                    csvFile.write("V,V,V,V,V,V,V,\n")
                    csvFile.write("Counties with Storms,Storm Count,"
                                  "Minimum Intensity,Maximum Intensity,"
                                  "Mean Intensity,Median Intensity,"
                                  "Mode Intensity,\n")

                    # Create empty list for storing hurricane values per county.
                    hurrList = []

                    # Create empty list for storing hurricane intensity values
                    # per county.
                    magList = []

                    # For each county list within state/county dictionary
                    # matching the state drop-down selection...
                    for key in GUI_CountiesPerState.dict_state_counties[
                        self.stringState_Name.get()]:

                        # Set counter to zero, for counting hurricane within
                        # each county during loop.
                        counter = 0

                        # Clears hurrList after each county count has concluded.
                        hurrList.clear()

                        # Clears magList after each county count has concluded.
                        magList.clear()

                        # Open the in_memory spatial join as a Search Cursor,
                        # with analysis fields set to FIPS code and intensity.
                        with arcpy.da.SearchCursor("temp_union",
                                        [census_Shapefile_Field_CountyName_1,
                                            analysis_HurrCode_Field,
                                            analysis_Mag_Field]) as cursor:

                            # For each feature within the spatial join...
                            for row in cursor:

                                # If FIPS code matches a state in the ordered
                                # dictionary and the wind speed is above 0...
                                if row[0] == key and row[2] > 0:

                                    # Append hurricane names to hurrList.
                                    hurrList.append(row[1])

                                    # Append hurricane intensities to magList.
                                    magList.append(row[2])

                                    # Increment counter by one.
                                    counter = counter + 1

                        # If counter is greater than zero...
                        if counter > 0:

                            try:

                                # Calculate mode of all intensities within list.
                                modeValue = mode(magList)

                                # Convert mode information to float and then to
                                # string with two decimal places.
                                modeString = \
                                    str("{0:.2f}".format(float(modeValue)))

                            except StatisticsError:

                                # This catches any lists containing no mode.
                                # This will occur if all values within list are
                                # unique values.

                                # Assign modeString to the following phrase.
                                modeString = "No Unique Mode"

                                pass

                            # Identify and count the unique storm names within
                            # hurrList. The length (count) of the uniqueNames
                            # variable will reveal how many hurricanes occurred.
                            uniqueNameCount = len(numpy.unique((hurrList)))

                            # Write the following data to the data counts CSV.
                            # State name, how many hurricanes, min mag, max
                            # mag, mean mag, median mag, mode mag, and FIPs.
                            csvFile.write(str(key) + "," +
                                str(uniqueNameCount) + "," +
                                str(min(magList)) + "," + str(max(magList)) +
                                "," +
                                str("{0:.2f}".format(numpy.mean(magList)) +
                                "," +
                                str("{0:.2f}".format(numpy.median(magList))) +
                                "," + modeString + ",\n"))

                    # Close the data counts CSV file.
                    csvFile.close()

                # If the user selects County clipping option...
                if self.radioButton_Selection == 3:

                    # Import the tuples and dictionaries affiliated with states
                    # and counties.
                    import GUI_CountiesPerState

                    # Execute function to retrieve global storm count.
                    self.func_CSV_DataCount_Global_Count()

                    # Execute function to retrieve nationwide storm count.
                    self.func_CSV_DataCount_Nationwide_Count()

                    # Execute function to retrieve statewide storm count.
                    self.func_CSV_DataCount_Statewide_Count()

                    # Create/Open a new CSV file within the CSV subfolder for
                    # data counts to be written into.
                    csvFile = open(self.csvDirectory + "DataCounts_" +
                                   self.name_Hurr_FeatureClass +
                                   self.folderNamingAddition + fileExtCSV, "w")

                    # If timespan and intensity drop-downs don't show Custom...
                    if self.stringHurricaneTimespan.get() != "Custom..." and \
                            self.stringHurricaneIntensity.get() != "Custom...":

                        # Write the following lines into the data counts CSV.
                        csvFile.write("Timespan:," +
                                      self.stringHurricaneTimespan.get() +
                                      ",\n")
                        csvFile.write("Intensity Range (Knots):," +
                                      self.stringHurricaneIntensity.get() +
                                      ",\n")

                    # If timespan drop-down shows Custom and intensity drop-down
                    # doesn't show Custom...
                    if self.stringHurricaneTimespan.get() == "Custom..." and \
                            self.stringHurricaneIntensity.get() != "Custom...":

                        # Write the following lines into the data counts CSV.
                        csvFile.write("Timespan:," + self.textCustomYearFrom +
                                      self.textCustomMonthFrom.zfill(2) +
                                      "-" + self.textCustomYearTo +
                                      self.textCustomMonthTo.zfill(2) + ",\n")
                        csvFile.write("Intensity Range (Knots):," +
                                      self.stringHurricaneIntensity.get() +
                                      ",\n")

                    # timespan drop-down shows Custom and intensity drop-down
                    # shows Custom...
                    if self.stringHurricaneTimespan.get() == "Custom..." and \
                            self.stringHurricaneIntensity.get() == "Custom...":

                        # Write the following lines into the data counts CSV.
                        csvFile.write("Timespan:," + self.textCustomYearFrom +
                                      self.textCustomMonthFrom.zfill(2) +
                                      "-" + self.textCustomYearTo +
                                      self.textCustomMonthTo.zfill(2) + ",\n")
                        csvFile.write("Intensity Range (Knots):," +
                                      self.textCustomIntensityFrom + "-" +
                                      self.textCustomIntensityTo + ",\n")

                    # If timespan drop-down doesn't show Custom and intensity
                    # drop-down shows Custom...
                    if self.stringHurricaneTimespan.get() != "Custom..." and \
                            self.stringHurricaneIntensity.get() == "Custom...":

                        # Write the following lines into the data counts CSV.
                        csvFile.write("Timespan:," +
                                    self.stringHurricaneTimespan.get() + ",\n")
                        csvFile.write("Intensity Range (Knots):," +
                                      self.textCustomIntensityFrom + "-" +
                                      self.textCustomIntensityTo + ",\n")

                    # Now write the following lines, regardless of
                    # timespan/intensity selection.
                    csvFile.write("\n")
                    csvFile.write(
                        "Note: All US locations include 50 mile buffer.,\n")
                    csvFile.write("\n")
                    csvFile.write("Worldwide Storm Count:," +
                                  str(self.worldwide_storm_count) + ",\n")
                    csvFile.write("USA (and DC) Storms:," +
                                  str(self.nationwide_storm_count) + ",\n")
                    csvFile.write("State Storms - " +
                                str(self.stringState_Name.get()) + " (FIPS: " +
                                str(dictKeys_OrderedDict_StateNames[
                                self.stringState_Name.get()]) + "):," +
                                str(self.state_storm_count) + ",\n")
                    csvFile.write("\n")
                    csvFile.write("County Storms - " +
                                  self.stringCounty_Name.get() + ":," +
                                  str(self.county_storm_count) + ",\n")
                    csvFile.write("County Storm Name(s):,")

                    for eachStorm in self.county_storm_names:

                        csvFile.write(eachStorm)

                    csvFile.write("\n\n")
                    csvFile.write("County Storm Data\n")
                    csvFile.write("V,V,V,V,V,\n")
                    csvFile.write("Minimum Intensity,Maximum Intensity,"
                                  "Mean Intensity,Median Intensity,"
                                  "Mode Intensity,\n")

                    # Create empty list for storing hurricane values per county.
                    hurrList = []

                    # Create empty list for storing hurricane intensity values
                    # per county.
                    magList = []

                    required_InputFile = [self.buffered_Output_FeatureClass,
                                          self.featureClass_County_State_Naming]
                    required_OutputFile = "temp_union"
                    optional_JoinAttributes = None
                    optional_ClusterTolerance = None
                    optional_Gaps = None

                    # Perform union of buffered hurricane feature class
                    # and the USA polygon feature class. Store output in_memory.
                    arcpy.Union_analysis(required_InputFile,
                                         required_OutputFile,
                                         optional_JoinAttributes,
                                         optional_ClusterTolerance,
                                         optional_Gaps)

                    # For each county list within state/county dictionary
                    # matching the state drop-down selection...
                    for key in GUI_CountiesPerState.dict_state_counties[
                        self.stringState_Name.get()]:

                        # Set counter to zero, for counting hurricane within
                        # each county during loop.
                        counter = 0

                        # Clears hurrList after each county count has concluded.
                        hurrList.clear()

                        # Clears magList after each county count has concluded.
                        magList.clear()

                        # Open the in_memory spatial join as a Search Cursor,
                        # with analysis fields set to FIPS code and intensity.
                        with arcpy.da.SearchCursor("temp_union",
                                        [census_Shapefile_Field_CountyName_1,
                                        analysis_HurrCode_Field,
                                        analysis_Mag_Field]) as cursor:

                            # For each feature within the spatial join...
                            for row in cursor:

                                # If FIPS code matches a state in the ordered
                                # dictionary and the wind speed is above 0...
                                if row[0] == key and row[2] > 0:
                                    # Append hurricane names to hurrList.
                                    hurrList.append(row[1])

                                    # Append hurricane intensities to magList.
                                    magList.append(row[2])

                                    # Increment counter by one.
                                    counter = counter + 1

                        # If counter is greater than zero...
                        if counter > 0:

                            try:

                                # Calculate mode of all intensities within list.
                                modeValue = mode(magList)

                                # Convert mode information to float and then to
                                # string with two decimal places.
                                modeString = \
                                    str("{0:.2f}".format(float(modeValue)))

                            except StatisticsError:

                                # This catches any lists containing no mode.
                                # This will occur if all values within list are
                                # unique values.

                                # Assign modeString to the following phrase.
                                modeString = "No Unique Mode"

                                pass

                            # Identify and count the unique storm names within
                            # hurrList. The length (count) of the uniqueNames
                            # variable will reveal how many hurricanes occurred.
                            uniqueNameCount = len(numpy.unique((hurrList)))

                            # Write the following data to the data counts CSV.
                            # Min mag, max mag, mean mag, median mag, and
                            # mode mag.
                            csvFile.write(str("{0:.2f}".format(min(magList))) +
                                          "," +
                                          str("{0:.2f}".format(max(magList))) +
                                          "," +
                                          str("{0:.2f}".format(
                                            numpy.mean(magList))) +
                                          "," +
                                          str("{0:.2f}".format(
                                              numpy.median(magList))) +
                                          "," + modeString + ",\n")

                    # Close the data counts CSV file.
                    csvFile.close()

                self.func_Scroll_setOutputText("Count results successfully "
                                               "written to CSV file.", None)

                # Increase current progress bar percentage by six percent.
                self.analysis_Percentage_Counter = \
                    self.analysis_Percentage_Counter + 6

                # Increment progress bar by adjusted value.
                self.func_ProgressBar_setProgress(
                    self.analysis_Percentage_Counter)

                # Clear any intermediate output from memory.
                self.func_Clear_InMemory()

                # Pause script for one second.
                sleep(1)

        except arcpy.ExecuteError:

            # Display geoprocessing errors and skip the failed analysis.
            self.func_Scroll_setOutputText(
                "Output CSV was not written successfully.", color_Red)

            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Red)

            pass

        except Exception as e:

            # Display error messages for all other errors and skip failed
            # analysis.
            self.func_Scroll_setOutputText("Error Message: " + str(e) + "\n" +
                                           "Traceback: " +
                                           traceback.format_exc(), color_Red)

        try:

            # If the user selects the Kernel Density analysis...
            if self.statusAnalysis_KernelDensity.get() == 1:
                # Set the workspace for the following analysis.
                arcpy.env.workspace = self.subFolder_GIS + "/" + nameFileGDB

                # Set the extent to the input argument feature class mask.
                arcpy.env.extent = featureClass_Mask

                self.func_Scroll_setOutputText("Performing Kernel Density "
                    "Analysis on all lines, then clipping/masking output to " +
                    featureClass_Mask + " extent...", None)

                # Kernel Density parameters, with optional parameters set to
                # None for Esri defaults.
                required_InputFile = self.clipped_Output_FeatureClass
                optional_PopField = None
                optional_CellSize = None
                optional_SearchRadius = None
                optional_AreaUnitScaleFactor = None
                optional_OutputCellValues = None
                optional_Method = None

                # Perform the Kernel Density analysis.
                output_KernelDensity = arcpy.sa.KernelDensity(
                    required_InputFile, optional_PopField, optional_CellSize,
                    optional_SearchRadius, optional_AreaUnitScaleFactor,
                    optional_OutputCellValues, optional_Method)

                # Get geoprocessing messages.
                self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

                # Pause script for one second.
                sleep(1)

                # Mask the Kernel Density results.
                output_KernelDensity_with_Mask = arcpy.sa.ExtractByMask(
                    output_KernelDensity, featureClass_Mask)

                self.func_Scroll_setOutputText(
                    "Masking Kernel Density results...", None)

                # Save the masked Kernel Density feature class results to
                # File GDB.
                output_KernelDensity_with_Mask.save("kerneldensity_" +
                                            self.clipped_Output_FeatureClass)

                # Get geoprocessing messages.
                self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

                self.func_Scroll_setOutputText(
                    "Kernel Density Analysis completed.", None)

                # Increase current progress bar percentage by six percent.
                self.analysis_Percentage_Counter = \
                    self.analysis_Percentage_Counter + 6

                # Increment progress bar by adjusted value.
                self.func_ProgressBar_setProgress(
                    self.analysis_Percentage_Counter)

                # Pause script for one second.
                sleep(1)

        except arcpy.ExecuteError:

            # Display geoprocessing errors and skip the failed analysis.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Red)

            pass

        except Exception as e:

            # Display error messages for all other errors and skip failed
            # analysis.
            self.func_Scroll_setOutputText("Error Message: " + str(e) + "\n" +
                                           "Traceback: " +
                                           traceback.format_exc(), color_Red)

            pass

        try:

            # If the user selects the Hot Spot analysis...
            if self.statusAnalysis_HotSpot.get() == 1:

                # Set the workspace for the following analysis.
                arcpy.env.workspace = self.subFolder_GIS + "/" + nameFileGDB

                # Set the extent to the input argument feature class mask.
                arcpy.env.extent = featureClass_Mask

                # Get the feature count of the input argument and assign to count
                # variable.
                hurricaneCountResult = \
                    arcpy.GetCount_management(self.clipped_Output_FeatureClass)

                # Store the integer version of the wind count to variable.
                clipped_HurricaneCount = int(hurricaneCountResult.getOutput(0))

                # If the clipped hurricane count is less than 30 features...
                if clipped_HurricaneCount < 30:

                    # Display the following message and skip, as a minimum of
                    # 30 samples is required (per Esri) when the analysis field
                    # option is set with a value.
                    self.func_Scroll_setOutputText(
                        "UNABLE TO EXECUTE HOT SPOT ANALYSIS (WITH ANALYSIS "
                        "FIELD OPTION):\n" +
                        "According to Esri, this analysis requires a minimum of"
                        " 30 hurricane features within the sampling area.\n" +
                        "Skipping this analysis...", color_Red)

                    pass

                else:

                    # Else, perform the analysis.
                    self.func_Scroll_setOutputText(
                        "Performing Hot Spot Analysis on all lines "
                        "(analysis field = '" + analysis_Mag_Field +
                        "', relationship = 'INVERSE_DISTANCE'), "
                        "with output clipped to " +
                        featureClass_Mask + " extent...", None)

                    # Static Hot Spot Analysis parameters, with optional
                    # parameters set to None for Esri defaults.
                    required_InputFile = self.clipped_Output_FeatureClass
                    required_InputField = analysis_Mag_Field
                    required_OutputFile_WithMagField = "temp_hotspot"
                    required_SpatialRelationship = "INVERSE_DISTANCE"
                    required_DistanceMethod = "EUCLIDEAN_DISTANCE"
                    required_Standardization = None
                    optional_DistanceBand = None
                    optional_PotentialField = None
                    optional_MatrixFile = None
                    optional_FalseDiscoveryRate = None

                    arcpy.HotSpots_stats(required_InputFile,
                                         required_InputField,
                                         required_OutputFile_WithMagField,
                                         required_SpatialRelationship,
                                         required_DistanceMethod,
                                         required_Standardization,
                                         optional_DistanceBand,
                                         optional_PotentialField,
                                         optional_MatrixFile,
                                         optional_FalseDiscoveryRate)

                    # Display geoprocessing output messages.
                    self.func_Scroll_setOutputText(arcpy.GetMessages(0),
                                                   color_Blue)

                    self.func_Scroll_setOutputText("Hot Spot Analysis on all "
                            "lines (analysis field = '" +
                            analysis_Mag_Field + "', "
                            "relationship = 'INVERSE_DISTANCE'),) completed.",
                            None)

                    self.func_Scroll_setOutputText("Clipping Hot Spot Analysis "
                            "(analysis field = '" +
                            analysis_Mag_Field + "', "
                            "relationship = 'INVERSE_DISTANCE') results...",
                            None)

                    # The intermediate output feature class is clipped to the
                    # predetermined feature class mask and saved as a new
                    # feature class.
                    arcpy.Clip_analysis(required_OutputFile_WithMagField,
                                        featureClass_Mask,
                                        "hotspot_" + analysis_Mag_Field +
                                        "AnalysisField_" + \
                                        self.clipped_Output_FeatureClass)

                    # Get geoprocessing messages.
                    self.func_Scroll_setOutputText(arcpy.GetMessages(0),
                                                   color_Blue)

                    self.func_Scroll_setOutputText("Clipping for Hot Spot "
                                        "Analysis (analysis field = '" +
                                        analysis_Mag_Field + "') completed.",
                                        None)

                # Clear any intermediate output from memory.
                self.func_Clear_InMemory()

                # Increase current progress bar percentage by six percent.
                self.analysis_Percentage_Counter = \
                    self.analysis_Percentage_Counter + 6

                # Increment progress bar by adjusted value.
                self.func_ProgressBar_setProgress(
                    self.analysis_Percentage_Counter)

                # Pause script for one second.
                sleep(1)

        except arcpy.ExecuteError:

            # Display geoprocessing errors and skip the failed analysis.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Red)

            # Clear any intermediate output from memory.
            self.func_Clear_InMemory()

            pass

        except Exception as e:

            # Display error messages for all other errors and skip failed
            # analysis.
            self.func_Scroll_setOutputText("Error Message: " + str(e) + "\n" +
                                           "Traceback: " +
                                           traceback.format_exc(), color_Red)

            # Clear any intermediate output from memory.
            self.func_Clear_InMemory()

            pass

        try:

            # If the user selects the Line Density analysis...
            if self.statusAnalysis_LineDensity.get() == 1:
                # Set the workspace for the following analysis.
                arcpy.env.workspace = self.subFolder_GIS + "/" + nameFileGDB

                # Set the extent to the input argument feature class mask.
                arcpy.env.extent = featureClass_Mask

                self.func_Scroll_setOutputText("Performing Line Density "
                                "Analysis on all lines, then clipping/masking "
                                "output to " + featureClass_Mask + " extent...",
                                None)

                # Line Density parameters, with optional parameters set to None
                # for Esri defaults.
                required_InputFile = self.clipped_Output_FeatureClass
                required_PopField = analysis_Mag_Field
                optional_CellSize = None
                optional_SearchRadius = None
                optional_AreaUnitScalFactor = None

                # Execute Line Density analysis with default Esri values.
                output_LineDensity = arcpy.sa.LineDensity(required_InputFile,
                                                    required_PopField,
                                                    optional_CellSize,
                                                    optional_SearchRadius,
                                                    optional_AreaUnitScalFactor)

                # Get geoprocessing messages.
                self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

                # Pause script for one second.
                sleep(1)

                # Mask the Line Density results.
                output_LineDensity_with_Mask = \
                    arcpy.sa.ExtractByMask(output_LineDensity,
                                           featureClass_Mask)

                self.func_Scroll_setOutputText(
                    "Masking Line Density results...", None)

                # Save the masked results to the File GDB.
                output_LineDensity_with_Mask.save("linedensity_" +
                                            self.clipped_Output_FeatureClass)

                # Get geoprocessing messages.
                self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

                self.func_Scroll_setOutputText(
                    "Line Density Analysis completed.", None)

                # Increase current progress bar percentage by six percent.
                self.analysis_Percentage_Counter = \
                    self.analysis_Percentage_Counter + 6

                # Increment progress bar by adjusted value.
                self.func_ProgressBar_setProgress(
                    self.analysis_Percentage_Counter)

                # Pause script for one second.
                sleep(1)

        except arcpy.ExecuteError:

            # Display geoprocessing errors and skip the failed analysis.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Red)

            pass

        except Exception as e:

            # Display error messages for all other errors and skip failed
            # analysis.
            self.func_Scroll_setOutputText("Error Message: " + str(e) + "\n" +
                                           "Traceback: " +
                                           traceback.format_exc(), color_Red)

            pass

        try:

            self.func_Scroll_setOutputText("Deleting any temporary feature "
                                               "classes from the File GDB...",
                                               None)

            # Use the ListFeatureClasses function to return a list of
            # feature classes.
            featureClasses = arcpy.ListFeatureClasses()

            # Delete feature classes from the File GDB starting with "temp_"
            for fc in featureClasses:

                if fc.startswith("temp_"):

                    arcpy.Delete_management(fc)

            self.func_Scroll_setOutputText("Temporary feature classes "
                                            "deleted from the File GDB.", None)

            # Increase current progress bar percentage by three percent.
            self.analysis_Percentage_Counter = \
                self.analysis_Percentage_Counter + 3

            # Increment progress bar by adjusted value.
            self.func_ProgressBar_setProgress(self.analysis_Percentage_Counter)

        except arcpy.ExecuteError:

            # Display geoprocessing errors and skip the failed analysis.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Red)

            pass

        except Exception as e:

            # Display error messages for all other errors and skip failed
            # analysis.
            self.func_Scroll_setOutputText("Error Message: " + str(e) + "\n" +
                                           "Traceback: " +
                                           traceback.format_exc(), color_Red)

            pass

    def func_CSV_DataCount_Global_Count(self):

        # This function controls the counting of all hurricane storm systems
        # around the world.

        try:

            stormList = []

            # Set workspace to File GDB for the following analysis.
            arcpy.env.workspace = self.subFolder_GIS + "/" + nameFileGDB

            # Search the checked hurricane feature class via SearchCursor.
            with arcpy.da.SearchCursor(self.checked_name_Hurr_FeatureClass,
                                    analysis_HurrCode_Field) as cursor:

                # For each feature in the cursor...
                for row in cursor:

                    # Add the storm names to the stormList.
                    stormList.append(row[0])

            # Gets the global unique storm names and counts how many exist.
            int_StormCount = len(numpy.unique((stormList)))

            # Store the integer hurricane count as a variable for use within
            # other functions.
            self.worldwide_storm_count = int_StormCount

        except arcpy.ExecuteError:

            # Display geoprocessing errors and skip the failed analysis.
            self.func_Scroll_setOutputText(
                "Failure to count for output US CSV values.", color_Red)

            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Red)

            pass

        except Exception as e:

            # Display error message for all other errors.
            self.func_Scroll_setOutputText("Error Message: " + str(e) + "\n" +
                                           "Traceback: " +
                                           traceback.format_exc(), color_Red)

    def func_CSV_DataCount_Nationwide_Count(self):

        # This function controls the counting of all hurricanes within the US.
        # Used only if state or county clipping option is selected. It will be
        # used within the output data counts CSV file.

        try:

            # Set the workspace to the File GDB for the following tasks.
            arcpy.env.workspace = self.subFolder_GIS + "/" + nameFileGDB

            # Create Census polygon feature class variable stored within memory.
            memoryFeatureClass_US = "temp_censusdata"

            # Copy Census Shapefile to feature class stored in memory.
            arcpy.CopyFeatures_management(featureClass_50States_and_DC_only,
                                          memoryFeatureClass_US)

            # Pause script for one second.
            sleep(1)

            # Dissolve parameters.
            required_InputFile = memoryFeatureClass_US
            required_OutputFileDiss = "temp_DissolvedStates"
            optional_DissolveField = None
            optional_StatisticsField = None
            optional_MultiPart = None
            optional_UnsplitLines = None

            arcpy.Dissolve_management(required_InputFile,
                                      required_OutputFileDiss,
                                      optional_DissolveField,
                                      optional_StatisticsField,
                                      optional_MultiPart,
                                      optional_UnsplitLines)

            # Buffer parameters.
            required_InputFile = required_OutputFileDiss
            required_OutputFileBuff = "temp_BufferStates"
            required_BufferDistance = "49.9 Miles"
            optional_LineSide = None
            optional_LineEndType = None
            optional_DissolveOption = None
            optional_DissolveField = None
            optional_Method = None

            arcpy.Buffer_analysis(required_InputFile, required_OutputFileBuff,
                                  required_BufferDistance, optional_LineSide,
                                  optional_LineEndType, optional_DissolveOption,
                                  optional_DissolveField, optional_Method)

            # Recalculate the extent of the in_memory feature class.
            arcpy.RecalculateFeatureClassExtent_management(
                required_OutputFileBuff)

            # Create new feature class for clipped hurricane
            # lines.
            clipped_Output_FeatureClass = "temp_outputFeatureClass_US"

            # Perform a clip of raw hurricane lines to the 50 US states and DC
            # polygons and store within the clipped feature class.
            arcpy.Clip_analysis(self.checked_name_Hurr_FeatureClass,
                                required_OutputFileBuff,
                                clipped_Output_FeatureClass)

            stormList = []

            # Search the checked hurricane feature class via SearchCursor.
            with arcpy.da.SearchCursor(clipped_Output_FeatureClass,
                                       [analysis_HurrCode_Field,
                                        analysis_HurrName_Field]) as cursor:

                # For each feature in the cursor...
                for row in cursor:

                    # Add the storm names to the stormList.
                    stormList.append(row[0] + ": " + row[1] + ",")

            # Gets the nationwide unique storm names and counts how many exist.
            text_UniqueNames = numpy.unique((stormList))
            int_StormCount = len(numpy.unique((stormList)))

            # Store the integer hurricane count as a variable for use within
            # other functions.
            self.nationwide_storm_count = int_StormCount

            # Store the list of unique hurricane storm names for use within
            # other functions.
            self.nationwide_storm_names = text_UniqueNames

        except arcpy.ExecuteError:

            # Display geoprocessing errors and skip the failed analysis.
            self.func_Scroll_setOutputText(
                "Failure to count for output US CSV values.", color_Red)

            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Red)

            pass

        except Exception as e:

            # Display error message for all other errors.
            self.func_Scroll_setOutputText("Error Message: " + str(e) + "\n" +
                                           "Traceback: " +
                                           traceback.format_exc(), color_Red)

    def func_CSV_DataCount_Statewide_Count(self):

        # This function controls the counting of all hurricane within the
        # user-selected state.
        # Used only if county clipping option is selected. It will be
        # used within the output data counts CSV file.

        try:

            # Set workspace to File GDB for the following analysis.
            arcpy.env.workspace = self.subFolder_GIS + "/" + nameFileGDB

            # Create Census polygon feature class variable stored in memory.
            memoryFeatureClass_State = "in_memory/" + \
                                       self.stringState_Name.get()

            # Copy Census Shapefile to feature class stored in memory.
            arcpy.CopyFeatures_management(self.featureClass_State_Selection_Only,
                                          memoryFeatureClass_State)

            # Pause script for one second.
            sleep(1)

            # Dissolve parameters.
            required_InputFile = memoryFeatureClass_State
            required_OutputFileDiss = "in_memory/temp_DissolvedState"
            optional_DissolveField = None
            optional_StatisticsField = None
            optional_MultiPart = None
            optional_UnsplitLines = None

            arcpy.Dissolve_management(required_InputFile,
                                      required_OutputFileDiss,
                                      optional_DissolveField,
                                      optional_StatisticsField,
                                      optional_MultiPart,
                                      optional_UnsplitLines)

            # Buffer parameters.
            required_InputFile = required_OutputFileDiss
            required_OutputFileBuff = "in_memory/temp_BufferState"
            required_BufferDistance = "49.9 Miles"
            optional_LineSide = None
            optional_LineEndType = None
            optional_DissolveOption = None
            optional_DissolveField = None
            optional_Method = None

            arcpy.Buffer_analysis(required_InputFile, required_OutputFileBuff,
                                  required_BufferDistance, optional_LineSide,
                                  optional_LineEndType, optional_DissolveOption,
                                  optional_DissolveField, optional_Method)

            # Recalculate the extent of the in_memory feature class.
            arcpy.RecalculateFeatureClassExtent_management(
                required_OutputFileBuff)

            # Create new feature class variable in_memory for clipped hurricane
            # lines.
            clipped_Output_FeatureClass = "in_memory/ClippedOutputFC_State"

            # Perform a clip of raw hurricane lines to the user-selected state
            # and store output as the clipped in_memory feature class.
            arcpy.Clip_analysis(self.checked_name_Hurr_FeatureClass,
                                required_OutputFileBuff,
                                clipped_Output_FeatureClass)

            stormList = []

            # Search the checked hurricane feature class via SearchCursor.
            with arcpy.da.SearchCursor(clipped_Output_FeatureClass,
                                       [analysis_HurrCode_Field,
                                        analysis_HurrName_Field]) as cursor:

                # For each feature in the cursor...
                for row in cursor:
                    # Add the storm names to the stormList.
                    stormList.append(row[0] + ": " + row[1] + ", ")

            # Gets the statewide unique storm names and counts how many exist.
            text_UniqueNames = numpy.unique((stormList))
            int_StormCount = len(numpy.unique((stormList)))

            # Store the integer hurricane count as a variable for use within
            # other functions.
            self.state_storm_count = int_StormCount

            # Store the list of unique hurricane storm names for use within
            # other functions.
            self.state_storm_names = text_UniqueNames

        except arcpy.ExecuteError:

            # Display geoprocessing errors and skip the failed analysis.
            self.func_Scroll_setOutputText(
                "Failure to count for output state CSV values.", color_Red)

            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Red)

            pass

        except Exception as e:

            # Display error message for all other errors.
            self.func_Scroll_setOutputText("Error Message: " + str(e) + "\n" +
                                           "Traceback: " +
                                           traceback.format_exc(), color_Red)

    def func_CSV_DataCount_Countywide_Count(self):

        # This function controls the counting of all hurricane within the
        # user-selected county.
        # Used only if county clipping option is selected. It will be
        # used within the output data counts CSV file.

        try:

            # Set workspace to File GDB for the following analysis.
            arcpy.env.workspace = self.subFolder_GIS + "/" + nameFileGDB

            # Create Census polygon feature class variable stored in memory.
            memoryFeatureClass_County = "in_memory/" + \
                                       self.stringCounty_Name.get()

            # Copy Census Shapefile to feature class stored in memory.
            arcpy.CopyFeatures_management(self.featureClass_County_State_Naming,
                                          memoryFeatureClass_County)

            # Pause script for one second.
            sleep(1)

            # Buffer parameters.
            required_InputFile = memoryFeatureClass_County
            required_OutputFileBuff = "in_memory/temp_BufferCounty"
            required_BufferDistance = "49.9 Miles"
            optional_LineSide = None
            optional_LineEndType = None
            optional_DissolveOption = None
            optional_DissolveField = None
            optional_Method = None

            arcpy.Buffer_analysis(required_InputFile, required_OutputFileBuff,
                                  required_BufferDistance, optional_LineSide,
                                  optional_LineEndType, optional_DissolveOption,
                                  optional_DissolveField, optional_Method)

            # Recalculate the extent of the in_memory feature class.
            arcpy.RecalculateFeatureClassExtent_management(
                required_OutputFileBuff)

            # Create new feature class variable in_memory for clipped hurricane
            # lines.
            clipped_Output_FeatureClass = "in_memory/ClippedOutputFC_County"

            # Perform a clip of raw hurricane lines to the user-selected state
            # and store output as the clipped in_memory feature class.
            arcpy.Clip_analysis(self.checked_name_Hurr_FeatureClass,
                                required_OutputFileBuff,
                                clipped_Output_FeatureClass)

            stormList = []

            # Search the checked hurricane feature class via SearchCursor.
            with arcpy.da.SearchCursor(clipped_Output_FeatureClass,
                                       [analysis_HurrCode_Field,
                                       analysis_HurrName_Field]) as cursor:

                # For each feature in the cursor...
                for row in cursor:

                    # Add the storm names to the stormList.
                    stormList.append(row[0] + ": " + row[1] + ", ")

            # Gets the countywide unique storm names and counts how many exist.
            text_UniqueNames = numpy.unique((stormList))
            int_StormCount = len(numpy.unique((stormList)))

            # Store the integer hurricane count as a variable for use within
            # other functions.
            self.county_storm_count = int_StormCount

            # Store the list of unique hurricane storm names for use within
            # other functions.
            self.county_storm_names = text_UniqueNames

        except arcpy.ExecuteError:

            # Display geoprocessing errors and skip the failed analysis.
            self.func_Scroll_setOutputText(
                "Failure to count for output state CSV values.", color_Red)

            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Red)

            pass

        except Exception as e:

            # Display error message for all other errors.
            self.func_Scroll_setOutputText("Error Message: " + str(e) + "\n" +
                                           "Traceback: " +
                                           traceback.format_exc(), color_Red)

    def func_Clear_InMemory(self):

        # This function is responsible for clearing any intermediate data output
        # that has been stored in memory as "in_memory".

        try:

            self.func_Scroll_setOutputText(
                "Deleting any intermediary data (in memory)...", None)

            # Delete the in_memory data.
            arcpy.Delete_management("in_memory")

            # Get geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            self.func_Scroll_setOutputText(
                "Intermediary data (in memory) deleted.", None)

        except arcpy.ExecuteError:

            # Display geoprocessing errors and skip the failed analysis.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Red)

            pass

        except Exception as e:

            # Display error message for all other errors.
            self.func_Scroll_setOutputText("Error Message: " + str(e) + "\n" +
                                           "Traceback: " +
                                           traceback.format_exc(), color_Red)

    def func_Scroll_saveOutputText(self):

        # This function writes all of the output text found within the
        # ScrolledText widget to a text file located within the user-defined
        # workspace. This is done at the conclusion of every application
        # iteration.

        try:

            # If the output text file's naming convention has been set...
            if self.name_Hurr_FeatureClass is not None:

                # Create/Open a new text file for all output messages to be
                # written to.
                textFile_ProcessingHistory = open(self.fullPathName + "/" +
                        "ProcessingHistory_" + self.name_Hurr_FeatureClass +
                        fileExtText, "w")

            else:

                # If the application throws errors and fails within the early
                # stages, the naming convention for the output text file will
                # not be established. If that is the case, the naming convention
                # will be saved with FAILED in the name.
                textFile_ProcessingHistory = open(self.fullPathName + "/" +
                                    "ProcessingHistory_FAILED" + fileExtText,
                                    "w")

            # Once the application processes have finished, take all output
            # messages within the scroll box and write to the output text file.
            textFile_ProcessingHistory.write(
                self.scrollBox.get(1.0, tkinter.END))

            # Close the text file.
            textFile_ProcessingHistory.close()

            self.func_Scroll_setOutputText(
                "The processing history (what you see here) "
                "has been logged to a text file "
                "within the user-defined workspace.", None)

            # Stop the status bar.
            self.func_StopStatusBar()

            # Increment progress bar to 100 percent.
            self.func_ProgressBar_setProgress(100)

        except Exception as e:

            # Display error message and skip the failed analysis.
            self.func_Scroll_setOutputText("Error Message: " + str(e) + "\n" +
                                           "Traceback: " +
                                           traceback.format_exc(), color_Red)

            pass

    def func_windowResize(self):

        # This function controls the actions that occur when determining if
        # the GUI window needs to be resized.

        # If the scroll box already exists...
        if self.scrollBoxFrame is not None:
            # Remove the scroll box.
            self.scrollBoxFrame.grid_remove()

        # If the progress bar already exists...
        if self.progressBarFrame is not None:
            # Remove the progress bar.
            self.progressBarFrame.grid_remove()

        # Set the GUI expansion width if the More Options checkbox is selected.
        self.checkboxExpansionWidth = guiWindow_HurricaneOptions_Width + 300

        # Set the GUI expansion height if timespan/intensity drop-downs show
        # "Custom...".
        self.customSelection_Height = guiWindow_HurricaneOptions_Height + 75

        # If the More Options checkbox is not selected and "Custom..." is not
        # selected for both timespan and intensity...
        if self.statusVar_Checkbutton_Options.get() == 0 and \
                self.stringHurricaneTimespan.get() != "Custom..." and \
                self.stringHurricaneIntensity.get() != "Custom...":

            # Set the GUI window dimensions accordingly.
            self.winfo_toplevel().geometry("%dx%d" % (
                guiWindow_HurricaneOptions_Width,
                guiWindow_HurricaneOptions_Height))

            # If the Custom Intensity Min/Max drop-down lists are visible...
            if self.comboFrame_Custom_Intensity is not None:
                # Remove the Custom Intensity Min/Max drop-down lists.
                self.comboFrame_Custom_Intensity.grid_remove()

            # If the Custom Timespan From/To drop-down lists are visible...
            if self.comboFrame_Custom_Timespan is not None:
                # Remove the Custom Timespan From/To drop-down lists.
                self.comboFrame_Custom_Timespan.grid_remove()

            # Clear the variable assignment for the State combobox drop-down.
            if self.comboFrame_State is not None:

                self.comboFrame_State = None

            # Clear the variable assignment for the County combobox drop-down.
            if self.comboFrame_Counties is not None:

                self.comboFrame_Counties = None

        # Else if the More Options checkbox is not selected and custom timespan
        # or custom intensity are selected...
        elif self.statusVar_Checkbutton_Options.get() == 0 and \
                (self.stringHurricaneTimespan.get() == "Custom..." or
                 self.stringHurricaneIntensity.get() == "Custom..."):

            # Set the GUI window dimensions accordingly.
            self.winfo_toplevel().geometry("%dx%d" % (
                guiWindow_HurricaneOptions_Width,
                self.customSelection_Height))

            # Clear the variable assignment for the State combobox drop-down.
            if self.comboFrame_State is not None:
                self.comboFrame_State = None

            # Clear the variable assignment for the County combobox drop-down.
            if self.comboFrame_Counties is not None:
                self.comboFrame_Counties = None

        # Else if the More Options checkbox is selected and both the custom
        # timespan and custom intensity are not selected...
        elif self.statusVar_Checkbutton_Options.get() == 1 and \
                self.stringHurricaneTimespan.get() != "Custom..." and \
                self.stringHurricaneIntensity.get() != "Custom...":

            # Set the GUI window dimensions accordingly.
            self.winfo_toplevel().geometry("%dx%d" % (
                self.checkboxExpansionWidth,
                guiWindow_HurricaneOptions_Height))

            # If the Custom Intensity Min/Max drop-down lists are visible...
            if self.comboFrame_Custom_Intensity is not None:
                # Remove the Custom Intensity Min/Max drop-down lists.
                self.comboFrame_Custom_Intensity.grid_remove()

            # If the Custom Timespan From/To drop-down lists are visible...
            if self.comboFrame_Custom_Timespan is not None:
                # Remove the Custom Timespan From/To drop-down lists.
                self.comboFrame_Custom_Timespan.grid_remove()

        # Else if the More Options checkbox is checked and the custom timespan
        # or custom intensity are selected...
        elif self.statusVar_Checkbutton_Options.get() == 1 and \
                (self.stringHurricaneTimespan.get() == "Custom..." or
                 self.stringHurricaneIntensity.get() == "Custom..."):

            # Set the GUI window dimensions accordingly.
            self.winfo_toplevel().geometry("%dx%d" % (
                self.checkboxExpansionWidth,
                self.customSelection_Height))

    def func_Enable_Buttons(self):

        # This function controls the enabling of all user-selectable buttons,
        # checkboxes, radio buttons, and drop-down lists. This is used when the
        # application has finished performing all tasks.

        # Enable Intensity drop-down list.
        self.combo_HurricaneIntensity.config(state="readonly")
        self.combo_HurricaneIntensity.update()

        # Enable Timespan drop-down list.
        self.combo_HurricaneTimespan.config(state="readonly")
        self.combo_HurricaneTimespan.update()

        # Enable the "Browse" button for setting the output workspace.
        self.workspaceFolderButton_FolderDialog.config(state=tkinter.NORMAL)
        self.workspaceFolderButton_FolderDialog.update()

        # Enable the Back button.
        self.buttonBack.config(state=tkinter.NORMAL)
        self.buttonBack.update()

        # Enable the OK button.
        self.buttonOK.config(state=tkinter.NORMAL)
        self.buttonOK.update()

        # Enable the More Options checkbox.
        self.checkboxOptions.config(state=tkinter.NORMAL)
        self.checkboxOptions.update()

        # Rename the Cancel button text back to Exit, leave enabled.
        self.buttonExitCancel.config(text="Exit")
        self.buttonExitCancel.update()

        # If the Custom Intensity Min/Max drop-down lists are visible...
        if self.comboFrame_Custom_Intensity is not None:
            # Enable the Custom Intensity Min drop-down list.
            self.combo_Custom_Intensity_Min.config(state="readonly")
            self.combo_Custom_Intensity_Min.update()

            # Enable the Custom Intensity Max drop-down list.
            self.combo_Custom_Intensity_Max.config(state="readonly")
            self.combo_Custom_Intensity_Max.update()

        # If the Custom Timespan From/To drop-down lists are visible...
        if self.comboFrame_Custom_Timespan is not None:
            # Enable the Custom Timespan From Year drop-down list.
            self.combo_CustomTimespan_Year_From.config(state="readonly")
            self.combo_CustomTimespan_Year_From.update()

            # Enable the Custom Timespan To Year drop-down list.
            self.combo_CustomTimespan_Year_To.config(state="readonly")
            self.combo_CustomTimespan_Year_To.update()

            # Enable the Custom Timespan From Month drop-down list.
            self.combo_CustomTimespan_Month_From.config(state="readonly")
            self.combo_CustomTimespan_Month_From.update()

            # Enable the Custom Timespan To Month drop-down list.
            self.combo_CustomTimespan_Month_To.config(state="readonly")
            self.combo_CustomTimespan_Month_To.update()

        # If the Analysis Options and Clipping Options are visible...
        if self.analysisOptionsFrame is not None:
            # Enable the US Clipping Option.
            self.radiobuttonClippingOption_US.config(state=tkinter.NORMAL)
            self.radiobuttonClippingOption_US.update()

            # Enable the State Clipping Option.
            self.radiobuttonClippingOption_State.config(state=tkinter.NORMAL)
            self.radiobuttonClippingOption_State.update()

            # Enable the County Clipping Option.
            self.radiobuttonClippingOption_County.config(state=tkinter.NORMAL)
            self.radiobuttonClippingOption_County.update()

            # Enable the Kernel Density checkbox.
            self.checkbox_KernelDensity.config(state=tkinter.NORMAL)
            self.checkbox_KernelDensity.update()

            # Enable the Hot Spot checkbox.
            self.checkbox_HotSpot.config(state=tkinter.NORMAL)
            self.checkbox_HotSpot.update()

            # Enable the Line Density checkbox.
            self.checkbox_LineDensity.config(state=tkinter.NORMAL)
            self.checkbox_LineDensity.update()

            # Enable the Output Data Counts to CSV checkbox.
            self.checkbox_OutputToCSVFile.config(state=tkinter.NORMAL)
            self.checkbox_OutputToCSVFile.update()

        # If the State drop-down list in the State Clipping Options is visible..
        if self.combo_State_Name is not None:
            # Enable the drop-down list for the State Clipping Option.
            self.combo_State_Name.config(state="readonly")
            self.combo_State_Name.update()

        # If the County drop-down list in the County Clipping Options is
        # visible...
        if self.combo_County_Name is not None:
            # Enable the drop-down list for the County Clipping Option.
            self.combo_County_Name.config(state="readonly")
            self.combo_County_Name.update()

    def func_Disable_Buttons(self):

        # This function controls the disabling of all user-selectable buttons,
        # checkboxes, radio buttons, and drop-down lists. This is used when the
        # application begins performing all tasks after the user clicks the OK
        # button.

        # Disable the Intensity drop-down list.
        self.combo_HurricaneIntensity.config(state=tkinter.DISABLED)
        self.combo_HurricaneIntensity.update()

        # Disable the Timespan drop-down list.
        self.combo_HurricaneTimespan.config(state=tkinter.DISABLED)
        self.combo_HurricaneTimespan.update()

        # Disable the "Browse" button for the output workspace.
        self.workspaceFolderButton_FolderDialog.config(state=tkinter.DISABLED)
        self.workspaceFolderButton_FolderDialog.update()

        # Disable the Back button.
        self.buttonBack.config(state=tkinter.DISABLED)
        self.buttonBack.update()

        # Disable the OK button.
        self.buttonOK.config(state=tkinter.DISABLED)
        self.buttonOK.update()

        # Disable the More Options checkbox.
        self.checkboxOptions.config(state=tkinter.DISABLED)
        self.checkboxOptions.update()

        # Change the text on the Exit button to "Cancel", leave enabled.
        self.buttonExitCancel.config(text="Cancel")
        self.buttonExitCancel.update()

        # If the Custom Timespan From/To drop-down boxes are visible...
        if self.comboFrame_Custom_Timespan is not None:
            # Disable the Year From drop-down list.
            self.combo_CustomTimespan_Year_From.config(state=tkinter.DISABLED)
            self.combo_CustomTimespan_Year_From.update()

            # Disable the Year To drop-down list.
            self.combo_CustomTimespan_Year_To.config(state=tkinter.DISABLED)
            self.combo_CustomTimespan_Year_To.update()

            # Disable the Month From drop-down list.
            self.combo_CustomTimespan_Month_From.config(state=tkinter.DISABLED)
            self.combo_CustomTimespan_Month_From.update()

            # Disable the Month To drop-down list.
            self.combo_CustomTimespan_Month_To.config(state=tkinter.DISABLED)
            self.combo_CustomTimespan_Month_To.update()

        # If the Custom Intensity Min/Max drop-down lists are visible...
        if self.comboFrame_Custom_Intensity is not None:
            # Disable the Min Intensity drop-down list.
            self.combo_Custom_Intensity_Min.config(state=tkinter.DISABLED)
            self.combo_Custom_Intensity_Min.update()

            # Disable the Max Intensity drop-down list.
            self.combo_Custom_Intensity_Max.config(state=tkinter.DISABLED)
            self.combo_Custom_Intensity_Max.update()

        # If the Analysis Options and Clipping Options are visible...
        if self.analysisOptionsFrame is not None:

            # Disable the US Clipping Option checkbox.
            self.radiobuttonClippingOption_US.config(state=tkinter.DISABLED)
            self.radiobuttonClippingOption_US.update()

            # Disable the State Clipping Option checkbox.
            self.radiobuttonClippingOption_State.config(state=tkinter.DISABLED)
            self.radiobuttonClippingOption_State.update()

            # Disable the County Clipping Option checkbox.
            self.radiobuttonClippingOption_County.config(state=tkinter.DISABLED)
            self.radiobuttonClippingOption_County.update()

            # Disable the Kernel Density checkbox.
            self.checkbox_KernelDensity.config(state=tkinter.DISABLED)
            self.checkbox_KernelDensity.update()

            # Disable the Hot Spot checkbox.
            self.checkbox_HotSpot.config(state=tkinter.DISABLED)
            self.checkbox_HotSpot.update()

            # Disable the Line Density checkbox.
            self.checkbox_LineDensity.config(state=tkinter.DISABLED)
            self.checkbox_LineDensity.update()

            # Disable the Output Data Counts to CSV File checkbox.
            self.checkbox_OutputToCSVFile.config(state=tkinter.DISABLED)
            self.checkbox_OutputToCSVFile.update()

        # If the State drop-down list in the State Clipping Option is visible..
        if self.combo_State_Name is not None:

            # Disable the drop-down list for the State Clipping Option.
            self.combo_State_Name.config(state=tkinter.DISABLED)
            self.combo_State_Name.update()

        # If the County drop-down list in the County Clipping Option is
        # visible...
        if self.combo_County_Name is not None:

            # Disable the drop-down list for the County Clipping Option.
            self.combo_County_Name.config(state=tkinter.DISABLED)
            self.combo_County_Name.update()

    def func_Calculate_Script_Time(self):

        # This function determines the total time of script processing and
        # formats that time to display within the scroll box.

        # Current time minus start time.
        self.elapsed_time = time.time() - self.start_time

        # If total time is greater than or equal to 3600 seconds, execute
        # conversion formula for hour, minute, second.
        if self.elapsed_time >= 3600:

            self.hours = int(self.elapsed_time / 3600)
            self.remainingSeconds = self.elapsed_time % 3600

            if self.remainingSeconds >= 60:

                self.minutes = int(self.remainingSeconds / 60)
                self.remainingSeconds = self.remainingSeconds % 60

            elif self.remainingSeconds < 60:

                self.minutes = 0

            self.func_Scroll_setOutputText(
                "This Python script completed in:\n" +
                "{0:.0f}".format(self.hours) + " h, " +
                "{0:.0f}".format(self.minutes) + " m", None)

        # Else if total time is greater than or equal to 60 seconds, execute
        # conversion formula for minutes and seconds.
        elif self.elapsed_time >= 60:

            self.minutes = int(self.elapsed_time / 60)
            self.remainingSeconds = self.elapsed_time % 60

            self.func_Scroll_setOutputText(
                "This Python script completed in:\n" +
                "{0:.0f}".format(self.minutes) + " m, " +
                "{0:.0f}".format(self.remainingSeconds) + " s", None)

        # Else if total time is greater than or equal to zero seconds, display
        # the seconds.
        elif self.elapsed_time >= 0:

            self.remainingSeconds = self.elapsed_time

            self.func_Scroll_setOutputText(
                "This Python script completed in:\n" +
                "{0:.0f}".format(self.remainingSeconds) + " s", None)

    def func_Scroll_setOutputText(self, word, tag):

        # This function controls what and how the output texts are displayed
        # within the scroll box for users to read. It takes an input argument
        # from the user as well as a text color tag.

        # These tags set the color used for specific text.
        self.scrollBox.tag_config(color_Red, foreground=color_Red)
        self.scrollBox.tag_config(color_Orange, foreground=color_Orange)
        self.scrollBox.tag_config(color_Blue, foreground=color_Blue)

        # This section inputs the user-defined wording and displays the message
        # within the scroll box. The focus of the scroll box shifts to the
        # last (bottom) entered text message.
        self.scrollBox.config(state=tkinter.NORMAL)
        self.scrollBox.insert(tkinter.END, word, (tag))
        self.scrollBox.insert(tkinter.END, "\n--------------------\n")
        self.scrollBox.see(tkinter.END)
        self.scrollBox.config(state=tkinter.DISABLED)

    def func_ProgressBar_setProgress(self, value):

        # This function controls the progress bar increment by taking a
        # user-defined input argument (integer).

        self.progressBar["value"] = value
        self.progressBar.update()