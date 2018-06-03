# David Lindsey - GISC 6389 - Master's Project
# Contact: dcl160230@utdallas.edu
# The following code represents the functionality for Hail Options.

# All import statements for utilized modules, excluding arcpy.
# Arcpy module will be imported at a later time.
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
from threading import Thread # this is used to unfreeze the GUI
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
guiWindow_HailOptions_Width = 470
guiWindow_HailOptions_Height = 225

# Formula to acquire date from one year ago in YYYY format. NOAA's portal for
# downloading hail data may take a year to have latest data available.
int_OneYearAgo = int(datetime.datetime.today().strftime("%Y")) - 1

# Integer iterator used for setting all years, starting with value from one
# year ago.
int_YearIterator = int_OneYearAgo

# Tuple for populating hail timespan text values within the combo box.
textCombo_HailTimespan = ()
textCombo_HailTimespan = textCombo_HailTimespan + \
                         ("Select...", "All | 1955-" + str(int_OneYearAgo))

# NOAA began keeping individual yearly CSV files beginning in 2008. These
# choices must be iterated and added to the tuple with this While loop.
while int_YearIterator >= 2008:
    textCombo_HailTimespan = textCombo_HailTimespan + (str(int_YearIterator),)
    int_YearIterator = int_YearIterator - 1

# Prior to 2008, NOAA kept specific timeframes for the CSV files. Those are
# added to the drop-down list with the following tuple addition.
textCombo_HailTimespan = textCombo_HailTimespan + ("2005-2007", "2000-2004",
                    "90-99", "80-89", "70-79", "60-69", "55-59", "Custom...")

# Reset int_YearIterator to original value from one year ago.
int_YearIterator = int_OneYearAgo

# The following code populates a list of years beginning with 1955 and ending
# with one year ago. This list will be used to populate the custom timespan
# combo box.
intList_Years = []
while int_YearIterator >= 1955:
    intList_Years.append(str(int_YearIterator))
    int_YearIterator = int_YearIterator - 1

# Tuple for populating hail diameter text values within the combo box.
textCombo_HailDiameter = ("Select...", "All", '0.5" - 0.99"', '1.0" - 1.99"',
                          '2.0" - 2.99"', '3.0"+', "Custom...")

# Tuple for populating the timespan combobox for monthly integer values when
# the custom timespan option is selected.
intCombo_Months = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)

# Tuple for populating the diameter combobox with integer values for the
# custom diameter option.
dbl_Combo_Diameters = (0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0,
                       5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0)

# Dictionary showing Census FIPs codes assigned to state abbreviation.
# This is used for the Census-derived polygon shapefile manipulations.
dict_StateName_StateFIPs = {"AL":"01", "AK":"02", "AZ":"04", "AR":"05",
                            "CA":"06", "CO":"08", "CT":"09", "DE":"10",
                            "DC":"11", "FL":"12", "GA":"13", "HI":"15",
                            "ID":"16", "IL":"17", "IN":"18", "IA":"19",
                            "KS":"20", "KY":"21", "LA":"22", "ME":"23",
                            "MD":"24", "MA":"25", "MI":"26", "MN":"27",
                            "MS":"28", "MO":"29", "MT":"30", "NE":"31",
                            "NV":"32", "NH":"33", "NJ":"34", "NM":"35",
                            "NY":"36", "NC":"37", "ND":"38", "OH":"39",
                            "OK":"40", "OR":"41", "PA":"42", "RI":"44",
                            "SC":"45", "SD":"46", "TN":"47", "TX":"48",
                            "UT":"49", "VT":"50", "VA":"51", "WA":"53",
                            "WV":"54", "WI":"55", "WY":"56"}

# Key/Values from Dictionary, sorted by Value (state abbreviation).
# To be used to populate the State combo box under Clipping Options (as string).
dictKeys_StateNames = sorted(dict_StateName_StateFIPs)

# Dictionary remains intact and unchanged (not string), only sorted.
# This is used for dictionary iterations with the UpdateCursor operations.
dictKeys_OrderedDict_StateNames = OrderedDict(dict_StateName_StateFIPs)

# Generic header for any error messages received.
errorMessage_Header = "Error Message"

# This string represents the static portion of the URL path for accessing the
# hail CSVs from NOAA website (used for non-custom parameter inputs only).
hail_siteURL = "http://www.spc.noaa.gov/wcm/data/"

# Comma-delimited header names for the NOAA hail CSVs.
hail_headers = "om" + "," + "yr" + "," + "mo" + "," + "dy" + "," + "date" + \
               "," + "time" + "," + "tz" + "," + "st" + "," + "stf" + "," + \
               "stn" + "," + "mag" + "," + "inj" + "," + "fat" + "," + \
               "loss" + "," + "closs" + "," + "slat" + "," + "slon" + "," + \
               "elat" + "," + "elon" + "," + "len" + "," + "wid" + "," + \
               "ns" + "," + "sn" + "," + "sg" + "," + "f1" + "," + "f2" + \
               "," + "f3" + "," + "f4"

# Text that will display within the URL textbox prior to a web URL link being
# created by the user.
urlDialog_Message = "URL will populate once Timespan and Diameter have been " \
                    "selected."

# Text that will display within the output folder textbox prior to an output
# workspace being selected by the user.
folderDialog_Message = "Output workspace folder path will display here..."

# Various components of output naming conventions to be used.
noaa = "noaa"
hail = "hail"
fileExtCSV = ".csv"
fileExtZip = ".zip"
fileExtShp = ".shp"
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

# Static output name for the extracted US-and-DC-only polygon feature class.
# This naming convention is used for the Shapefile-to-feature-class conversion.
featureClass_50States_and_DC_only = "USA_50_and_DC_only"

# Column header from CSV file for diameter, used as an input parameter for the
# various ArcPy analyses.
analysis_Mag_Field = "mag"

# ArcPy module is imported at this location so as to check for any runtime
# errors (due to internet connectivity issues and/or licensing issues).
# This issue is handled within the GUI_ApplicationDriver.py file.
# If the user chooses to proceed with the application after receiving a
# "Runtime Error", the same error will be ignored/passed within this .py file.
try:

    # If ArcPy available, import it.
    import arcpy

    # Universal parameters for assigning the Projected Coordinate System to the
    # hail and polygon feature classes.
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

# Class for the Hail Options GUI functionality.
class HailOptions(FrameLifts):

    def __init__(self, *args, **kwargs):
        FrameLifts.__init__(self, *args, **kwargs)

        # Universal parameters used throughout various functions of this class.
        # Setting values to None and later testing for None alleviates potential
        # "Attribute Errors" later on, as some variables will not be used if
        # certain tasks are not needed.

        self.timespan_url = None
        self.diameter_url = None
        self.comboFrame_Custom_Timespan = None
        self.comboFrame_Custom_Diameter = None
        self.custom_diameter_url = None
        self.intCustomTimespan_Year_From = None
        self.intCustomTimespan_Year_To = None
        self.intCustomTimespan_Month_From = None
        self.intCustomTimespan_Month_To = None
        self.doubleCustom_Diameter_Min = None
        self.doubleCustom_Diameter_Max = None
        self.textCustomDiameterFrom = None
        self.textCustomDiameterTo = None
        self.custom_Diameter_Naming = None
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

        # Settings and configuration for the Hail Options GUI window.
        self.winfo_toplevel().title("Hail Options")
        self.winfo_toplevel().geometry("%dx%d" %
                                        (guiWindow_HailOptions_Width,
                                         guiWindow_HailOptions_Height))

        # The GUI frame that all child frames will be placed.
        self.winFrame = tkinter.Frame(self.winfo_toplevel())
        self.winFrame.grid(
            column=0, row=0, padx=0, pady=0, columnspan=2, sticky=tkinter.NW)

        # Frame that displays the initial Hail dialog layout.
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

        # Executes the function controlling the Timespan/Diameter comboboxes
        self.func_ComboFrame()

        # Executes the function controlling the URL display text functionality.
        self.func_URLFrame()

        # Executes the function controlling the Workspace Folder dialog/text.
        self.func_WorkspaceFolderFrame()

        # Executes the function controlling the Exit/Back/OK buttons.
        self.func_ButtonFrame()

    def func_ComboFrame(self):

        # This function controls the display of the combobox frame.

        # Widget frame housing the combobox items for Timespan/Diameter.
        self.comboFrame = tkinter.Frame(self.initialFrame)
        self.comboFrame.grid(column=0, row=0, padx=40, pady=5, sticky=tkinter.W)

        # Label for Timespan combobox with Central Standard Time (CST).
        comboLabel_Timespan = ttk.Label(self.comboFrame, text="Timespan (CST):")
        comboLabel_Timespan.grid(column=0, row=0, sticky=tkinter.W)

        # Label for Diameter combobox.
        comboLabel_Diameter = ttk.Label(self.comboFrame,
                                        text="Diameter (Inch):")
        comboLabel_Diameter.grid(column=2, row=0, sticky=tkinter.W)

        # Combobox requirements for Timespan.
        self.stringHailTimespan = tkinter.StringVar()
        self.combo_HailTimespan = ttk.Combobox(self.comboFrame, width=13,
                                        textvariable=self.stringHailTimespan,
                                        state="readonly")
        self.combo_HailTimespan["values"] = (textCombo_HailTimespan)
        self.combo_HailTimespan.grid(column=0, row=1, sticky=tkinter.W)

        # GIF icon to symbolize Hail within the GUI.
        dirFolder = os.path.dirname(__file__)
        gifPath = os.path.join(dirFolder, "Icon_Hail.gif")
        self.photo_Hail_Icon = \
            tkinter.PhotoImage(file=gifPath)
        colorCode_Black = "black"
        self.subSampleImage = self.photo_Hail_Icon.subsample(4, 4)
        self.label_for_icon = ttk.Label(self.comboFrame, borderwidth=2,
                                        relief="solid",
                                        background=colorCode_Black,
                                        image=self.subSampleImage)
        self.label_for_icon.photo = self.photo_Hail_Icon
        self.label_for_icon.grid(column=1, row=0, padx=0,
                                 pady=5, sticky=tkinter.EW, rowspan=2)

        # Combobox requirements for Diameter.
        self.stringHailDiameter = tkinter.StringVar()
        self.combo_HailDiameter = ttk.Combobox(self.comboFrame, width=12,
                                    textvariable=self.stringHailDiameter,
                                    state="readonly")
        self.combo_HailDiameter["values"] = \
            (textCombo_HailDiameter)
        self.combo_HailDiameter.grid(column=2, row=1, sticky=tkinter.W)

        # Combobox selection binding that will be used to populate URL Field.
        self.combo_HailTimespan.bind("<<ComboboxSelected>>",
                                      self.func_PopulateURLField_Timespan)

        # Combobox selection binding that will be used to populate URL Field.
        self.combo_HailDiameter.bind("<<ComboboxSelected>>",
                                       self.func_PopulateURLField_Diameter)

        # For all items in the comboFrame, configure their grids the same way.
        for child in self.comboFrame.winfo_children():
            child.grid_configure(padx=25, pady=1)

        # Display first index for Timespan (Select...).
        self.combo_HailTimespan.current(0)

        # Display first index for Diameter (Select...).
        self.combo_HailDiameter.current(0)

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
                                                     pady = 5, sticky=tkinter.W)

        # Label for YEAR FROM combobox.
        comboLabel_CustomTimespan_Year_From = ttk.Label(
            self.comboLabelFrameCustomTimespan_From,
            text="Year:")
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
            self.comboLabelFrameCustomTimespan_From,
            width=4,
            textvariable=self.intCustomTimespan_Year_From,
            state="readonly")
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
        self.combo_CustomTimespan_Year_To["values"] = (intList_Years)
        self.combo_CustomTimespan_Year_To.grid(column=0, row=1,
                                               sticky=tkinter.W)

        # Combobox requirements for MONTH TO.
        self.intCustomTimespan_Month_To = tkinter.IntVar()
        self.combo_CustomTimespan_Month_To = ttk.Combobox(
            self.comboLabelFrameCustomTimespan_To, width=2,
            textvariable=self.intCustomTimespan_Month_To, state="readonly")
        self.combo_CustomTimespan_Month_To["values"] = (intCombo_Months)
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

    def func_ComboCustomDiameter(self):

        # This function controls the display of the custom combobox frame
        # controlling the custom Diameter.

        # If the custom diameter combobox frame already exists (is visible)...
        if self.comboFrame_Custom_Diameter is not None:

            # Remove the frame.
            self.comboFrame_Custom_Diameter.grid_remove()

        # Widget frame for custom diameter.
        self.comboFrame_Custom_Diameter = tkinter.Frame(self.initialFrame)
        self.comboFrame_Custom_Diameter.grid(column=0, row=1, padx=60, pady=5,
                                              sticky=tkinter.E)

        # Label frame for the diameter range comboboxes.
        self.comboLabelFrame_Custom_Diameter = ttk.LabelFrame(
            self.comboFrame_Custom_Diameter, text="Range:",
            labelanchor=tkinter.N)
        self.comboLabelFrame_Custom_Diameter.grid(column=0, row=0, padx=5,
                                                   pady=5, sticky=tkinter.E)

        # Label for MINIMUM diameter.
        comboLabel_Custom_Diameter_Min = ttk.Label(
            self.comboLabelFrame_Custom_Diameter, text="Min:        ")
        comboLabel_Custom_Diameter_Min.grid(column=0, row=0, sticky=tkinter.W)

        # Label for MAXIMUM diameter.
        comboLabel_Custom_Diameter_Max = ttk.Label(
            self.comboLabelFrame_Custom_Diameter, text="Max:")
        comboLabel_Custom_Diameter_Max.grid(column=3, row=0, sticky=tkinter.W)

        # Combobox requirements for MINIMUM diameter.
        self.doubleCustom_Diameter_Min = tkinter.DoubleVar()
        self.combo_Custom_Diameter_Min = ttk.Combobox(
            self.comboLabelFrame_Custom_Diameter, width=4,
            textvariable=self.doubleCustom_Diameter_Min, state="readonly")
        self.combo_Custom_Diameter_Min["values"] = (dbl_Combo_Diameters)
        self.combo_Custom_Diameter_Min.grid(column=0, row=1, sticky=tkinter.W)

        # Combobox requirements for MAXIMUM diameter.
        self.doubleCustom_Diameter_Max = tkinter.DoubleVar()
        self.combo_Custom_Diameter_Max = ttk.Combobox(
            self.comboLabelFrame_Custom_Diameter, width=4,
            textvariable=self.doubleCustom_Diameter_Max, state="readonly")
        self.combo_Custom_Diameter_Max["values"] = (dbl_Combo_Diameters)
        self.combo_Custom_Diameter_Max.grid(column=3, row=1, sticky=tkinter.E)

        # For all items in the custom diameter comboFrame, configure their
        # grids the same way.
        for child in self.comboFrame_Custom_Diameter.winfo_children():

            child.grid_configure(padx=10, pady=1)

        # Display first index for MINIMUM diameter (0.0).
        self.combo_Custom_Diameter_Min.current(0)

        # Display last index for MAXIMUM diameter (10.0).
        self.combo_Custom_Diameter_Max.current(20)

        # Combobox selection binding that will be used to populate URL field.
        self.combo_Custom_Diameter_Min.bind("<<ComboboxSelected>>",
                                             self.func_Set_Custom_Diameter)

        # Combobox selection binding that will be used to populate URL field.
        self.combo_Custom_Diameter_Max.bind("<<ComboboxSelected>>",
                                             self.func_Set_Custom_Diameter)

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
                self.timespan_file_folder_naming = "_" + \
                                    self.textCustomYearFrom + \
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

    def func_Set_Custom_Diameter(self, event):

        # This function handles events related to the custom Diameter options
        # that a user selects. Based on those selections, this function will
        # assign values and trigger other actions if necessary.

        try:

            # If the custom MINIMUM diameter has a value...
            if str(self.doubleCustom_Diameter_Min.get()):

                # Convert/assign the double value to string.
                # String conversion required for 0.0 to be accessible from
                # Combo list. "0.0" as double will not populate.
                self.textCustomDiameterFrom = str(
                    self.doubleCustom_Diameter_Min.get())

            # If the custom MAXIMUM diameter has a value...
            if self.doubleCustom_Diameter_Max.get():

                # Convert/assign the double value to string.
                self.textCustomDiameterTo = str(
                    self.doubleCustom_Diameter_Max.get())

            # If both combobox parameters for custom diameter exist...
            if self.textCustomDiameterFrom is not None and \
                self.textCustomDiameterTo is not None:

                pass

            # The combined string with adjustments used for file naming and
            # analyses later on in the script.
            self.custom_Diameter_Naming = \
                self.textCustomDiameterFrom.replace(".", "_") + "_to_" + \
                self.textCustomDiameterTo.replace(".", "_")

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
        urlLabel_HailURL = ttk.Label(self.urlFrame,
                            text="URL Download File Link:")
        urlLabel_HailURL.grid(column=0, row=0, padx=20, pady=1,
                                    sticky=tkinter.W)

        # Parameters for the URL textbox.
        self.textURLTextbox = tkinter.StringVar()
        self.textURLTextbox.set(urlDialog_Message)
        urlTextbox_HailURL = ttk.Entry(self.urlFrame,
                                             textvariable=self.textURLTextbox,
                                             width=70, state="readonly")
        urlTextbox_HailURL.grid(column=0, row=1, padx=20, pady=0)

    def func_PopulateURLField_Timespan(self, event):

        # This function handles the events where a user selects a timespan
        # option from the combobox. The selection will trigger various responses
        # as detailed below.

        try:

            # If the timespan combobox displays "Select..."...
            if self.stringHailTimespan.get() == "Select...":

                # Clear any variable assignments from the following items.
                self.timespan_url = None

                # Display this generic message within the URL textbox.
                self.textURLTextbox.set(urlDialog_Message)

                # Run function that checks if GUI window needs to be resized.
                self.func_windowResize()

                # If the custom timespan comboboxes exist, remove them from GUI.
                if self.comboFrame_Custom_Timespan is not None:

                    self.comboFrame_Custom_Timespan.grid_remove()

            # If the user selects all hail data from combobox...
            elif self.stringHailTimespan.get() == \
                    "All | 1955-" + str(int_OneYearAgo):

                # Assign/clear variables as needed.
                self.timespan_url = "1955-" + str(int_OneYearAgo) #+ "_hail"

                # Set the URL text of non custom timespan/diameter values.
                self.text_Hail_URL = hail_siteURL + self.timespan_url + "_" + \
                                     hail + fileExtCSV + fileExtZip
                
                if self.stringHailDiameter.get() != "Select...":
                    
                    self.textURLTextbox.set(self.text_Hail_URL)

                # Run function that checks if GUI window needs to be resized.
                self.func_windowResize()

                # If the custom timespan comboboxes exist, remove them from GUI.
                if self.comboFrame_Custom_Timespan is not None:

                    self.comboFrame_Custom_Timespan.grid_remove()

            # If the user selects "Custom..." from the combobox...
            elif self.stringHailTimespan.get() == "Custom...":

                # Assign/clear variables as needed.
                self.timespan_url = "1955-" + str(int_OneYearAgo) #+ "_hail"

                # Set the URL text of timespan values.
                self.text_Hail_URL = hail_siteURL + self.timespan_url + "_" + \
                                     hail + fileExtCSV + fileExtZip

                if self.stringHailDiameter.get() != "Select...":

                    self.textURLTextbox.set(self.text_Hail_URL)

                # Run function that checks if GUI window needs to be resized.
                self.func_windowResize()

                # Run the function that controls the custom timespan combobox.
                self.func_ComboCustomTimespan()

                # Run the function that sets the custom timespan variables.
                self.func_Set_Custom_Timespan(event)

            # If the user selects any option aside from Select, All, or Custom..
            elif self.stringHailTimespan.get():

                # Assign/clear variables as needed.
                self.timespan_url = self.stringHailTimespan.get() #+ "_hail"

                # Set the URL text of timespan values.
                self.text_Hail_URL = hail_siteURL + self.timespan_url + "_" + \
                                     hail + fileExtCSV

                if self.stringHailDiameter.get() != "Select...":
                    
                    self.textURLTextbox.set(self.text_Hail_URL)

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

    def func_PopulateURLField_Diameter(self, event):

        # This function handles the events where a user selects a diameter
        # option from the combobox. The selection will trigger various responses
        # as detailed below.

        # If the diameter combobox displays "Select..."...
        if self.stringHailDiameter.get() == "Select...":

            # Clear any variable assignments from the following items.
            self.diameter_url = None
            self.mag_naming = None

            # Display this generic message within the URL textbox.
            self.textURLTextbox.set(urlDialog_Message)

            # Run the function that checks if GUI window needs to be resized.
            self.func_windowResize()

            # If the custom diameter comboboxes exist, remove them from GUI.
            if self.comboFrame_Custom_Diameter is not None:

                self.comboFrame_Custom_Diameter.grid_remove()

        # If the user selects "All" from the combobox...
        elif self.stringHailDiameter.get() == "All":

            # Assign/clear variables as needed.
            self.mag_naming = "all"
            self.custom_diameter_url = None

            if self.stringHailTimespan.get() != "Select...":

                self.textURLTextbox.set(self.text_Hail_URL)

            # Run the function that checks if GUI window needs to be resized.
            self.func_windowResize()

            # If the custom diameter comboboxes exist, remove them from GUI.
            if self.comboFrame_Custom_Diameter is not None:

                self.comboFrame_Custom_Diameter.grid_remove()

        # If the user selects 0.5" - 0.99" from the combobox...
        elif self.stringHailDiameter.get() == '0.5" - 0.99"':

            # Assign/clear variables as needed.
            self.mag_naming = "0_5_to_0_99"
            self.custom_diameter_url = None

            if self.stringHailTimespan.get() != "Select...":

                self.textURLTextbox.set(self.text_Hail_URL)

            # Run the function that checks if GUI window needs to be resized.
            self.func_windowResize()

            # If the custom diameter comboboxes exist, remove them from GUI.
            if self.comboFrame_Custom_Diameter is not None:

                self.comboFrame_Custom_Diameter.grid_remove()

        # If the user selects 1.0" - 1.99" from the combobox...
        elif self.stringHailDiameter.get() == '1.0" - 1.99"':

            # Assign/clear variables as needed.
            self.mag_naming = "1_0_to_1_99"
            self.custom_diameter_url = None

            if self.stringHailTimespan.get() != "Select...":

                self.textURLTextbox.set(self.text_Hail_URL)

            # Run the function that checks if GUI window needs to be resized.
            self.func_windowResize()

            # If the custom diameter comboboxes exist, remove them from GUI.
            if self.comboFrame_Custom_Diameter is not None:

                self.comboFrame_Custom_Diameter.grid_remove()

        # If the user selects 2.0" - 2.99" from the combobox...
        elif self.stringHailDiameter.get() == '2.0" - 2.99"':

            # Assign/clear variables as needed.
            self.mag_naming = "2_0_to_2_99"
            self.custom_diameter_url = None

            if self.stringHailTimespan.get() != "Select...":

                self.textURLTextbox.set(self.text_Hail_URL)

            # Run the function that checks if GUI window needs to be resized.
            self.func_windowResize()

            # If the custom diameter comboboxes exist, remove them from GUI.
            if self.comboFrame_Custom_Diameter is not None:

                self.comboFrame_Custom_Diameter.grid_remove()

        # If the user selects 3.0"+ from the combobox...
        elif self.stringHailDiameter.get() == '3.0"+':

            # Assign/clear variables as needed.
            self.mag_naming = "3_0_and_Up"
            self.custom_diameter_url = None

            if self.stringHailTimespan.get() != "Select...":

                self.textURLTextbox.set(self.text_Hail_URL)

            # Run the function that checks if GUI window needs to be resized.
            self.func_windowResize()

            # If the custom diameter comboboxes exist, remove them from GUI.
            if self.comboFrame_Custom_Diameter is not None:

                self.comboFrame_Custom_Diameter.grid_remove()

        # If the user selects "Custom..." from the combobox...
        elif self.stringHailDiameter.get() == "Custom...":

            # Assign/clear variables as needed.
            # Custom hail diameter will default to All, as all data is initially
            # downloaded.
            self.mag_naming = "all"

            if self.stringHailTimespan.get() != "Select...":

                self.textURLTextbox.set(self.text_Hail_URL)

            # Run the function that checks if GUI window needs to be resized.
            self.func_windowResize()

            # Run the function that controls the display of the custom
            # diameter comboboxes.
            self.func_ComboCustomDiameter()

            # Run the function that sets the custom diameter variables.
            self.func_Set_Custom_Diameter(event)

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
        self.workspaceFolderTextbox_HailFolderDialog = \
            ttk.Entry(self.workspaceFolderFrame,
                      textvariable=self.textWorkspaceDialogPath, width=52,
                      state="readonly")
        self.workspaceFolderTextbox_HailFolderDialog.grid(column=1,
                                        row=1, padx=0, pady=0, sticky=tkinter.W)

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
        # widgetButtonCancel.config(height = 20, width = 20)
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
            text="More Options", variable = self.statusVar_Checkbutton_Options,
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
                guiWindow_HailOptions_Height + 200

            # If a custom timespan or custom diameter has been selected...
            if self.customSelection_Height is not None:

                # Expand the height of the GUI to accomodate the Custom
                # timespan/diameter height, plus the processing messages and
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

            # If the user has selected a valid timespan, diameter, and assigned
            # an output workspace folder...
            if self.stringHailTimespan.get() != "Select..." and \
                self.stringHailDiameter.get() != "Select..." and \
                self.workspaceFolderTextbox_HailFolderDialog.get() != \
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

                    # If the timespan or diameter combobox is "Custom..."...
                    if self.stringHailTimespan.get() == "Custom..." or \
                            self.stringHailDiameter.get() == "Custom...":

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

                        # If the custom minimum diameter and the custom
                        # maximum diameter comboboxes have values...
                        if self.doubleCustom_Diameter_Min is not None and\
                                self.doubleCustom_Diameter_Max is not None:

                            # If the minimum diameter exceeds the maximum
                            # diameter...
                            if self.doubleCustom_Diameter_Min.get() > \
                                    self.doubleCustom_Diameter_Max.get():

                                # Display error message.
                                messagebox.showerror(errorMessage_Header,
                                message="Invalid diameter entry.\n" +
                                "Minimum diameter exceeds Maximum diameter.")

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

                    # If the timespan or diameter "Custom..." comboboxes are
                    # selected...
                    if self.stringHailTimespan.get() == "Custom..." or \
                            self.stringHailDiameter.get() == "Custom...":

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

                        # If both the minimum and maximum diameter comboboxes
                        # have values...
                        if self.doubleCustom_Diameter_Min is not None and \
                            self.doubleCustom_Diameter_Max is not None:

                            # If the MINIMUM diameter exceeds the MAXIMUM
                            # diameter...
                            if self.doubleCustom_Diameter_Min.get() > \
                                    self.doubleCustom_Diameter_Max.get():

                                # Display error message.
                                messagebox.showerror(errorMessage_Header,
                                message="Invalid diameter entry.\n" +
                                "Minimum diameter exceeds Maximum diameter.")

                                # Re-enable all selectable items in the GUI.
                                self.func_Enable_Buttons()

                                # Exit the function.
                                return

                        # If no errors have occurred, adjust the GUI dimensions
                        # as assigned.
                        self.winfo_toplevel().geometry("%dx%d" % (
                                    guiWindow_HailOptions_Width,
                                    self.okClick_Custom_ExpansionHeight))

                    else:

                        # If no "Custom..." comboboxes have been selected, and
                        # no errors thrown, adjust the GUI dimensions as
                        # assigned.
                        self.winfo_toplevel().geometry("%dx%d" % (
                            guiWindow_HailOptions_Width,
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
                if self.stringHailTimespan.get() == "Select...":

                    # Display error message.
                    messagebox.showerror(errorMessage_Header,
                                        message="Invalid timespan entry.\n" +
                                        "Please select an option from the "
                                        "drop-down list and try again.")

                    # Re-enable all selectable intems in the GUI.
                    self.func_Enable_Buttons()

                # Else if the diameter combobox shows "Select..."...
                elif self.stringHailDiameter.get() == "Select...":

                    # Display error message.
                    messagebox.showerror(errorMessage_Header,
                                         message="Invalid diameter entry.\n" +
                                        "Please select an option from "
                                        "the drop-down list and try again.")

                    # Re-enable all selectable intems in the GUI.
                    self.func_Enable_Buttons()

                # Else if the output workspace text is the default message...
                elif \
                self.workspaceFolderTextbox_HailFolderDialog.get() == \
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

            # Re-enable all selectable intems in the GUI.
            self.func_Enable_Buttons()

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
                        width=self.scrollWidth, height=self.scrollHeight,
                        wrap=tkinter.WORD, state=tkinter.DISABLED)
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

            # If the "More Options" checkbox is unchecked, clear the radio button
            # selection, re-size the window, and remove the Analysis/Clipping
            # Options.
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
        self.analysisOptionsLabelFrame.grid(column=0, row=0, padx=0, pady = 2,
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
                    text="USA", value = 1, variable=self.statusClippingOption,
                    command = self.func_RadioButton_Clipping_Command)
        self.radiobuttonClippingOption_US.grid(column=0, row=0, padx=0, pady=0,
                                               sticky=tkinter.W)
        self.radiobuttonClippingOption_US.deselect()

        # Frame for the State clipping option.
        self.clippingOptions_radiobuttonFrame_State = \
            ttk.Frame(self.clippingOptionsLabelFrame)
        self.clippingOptions_radiobuttonFrame_State.grid(column=0, row=1,
                                                padx=0, pady=0,sticky=tkinter.W)

        # Radio button variables for the State clipping option.
        self.radiobuttonClippingOption_State = \
            tkinter.Radiobutton(self.clippingOptions_radiobuttonFrame_State,
                    text="State", value = 2, variable=self.statusClippingOption,
                    command = self.func_RadioButton_Clipping_Command)
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
                text="County", value = 3, variable=self.statusClippingOption,
                                command=self.func_RadioButton_Clipping_Command)
        self.radiobuttonClippingOption_County.grid(column=0, row=0, padx=0,
                                                pady=0, sticky=tkinter.W)
        self.radiobuttonClippingOption_County.deselect()

        # Checkbox variables for the IDW option.
        self.statusAnalysis_IDW = tkinter.IntVar()
        self.checkbox_IDW = tkinter.Checkbutton(self.analysisOptionsLabelFrame,
                                text="IDW", variable=self.statusAnalysis_IDW)
        #, command=self.test_IDW_parameters)
        self.checkbox_IDW.grid(column=0, row=0, padx=0, pady=0,sticky=tkinter.W)
        self.checkbox_IDW.deselect()

        # Checkbox variables for the Kernel Density option.
        self.statusAnalysis_KernelDensity = tkinter.IntVar()
        self.checkbox_KernelDensity = \
            tkinter.Checkbutton(self.analysisOptionsLabelFrame,
            text="Kernel Dens.", variable=self.statusAnalysis_KernelDensity)
        # command=self.func_Controls_For_Analysis_Options)
        self.checkbox_KernelDensity.grid(column=1, row=0, padx=0, pady=0,
                                         sticky=tkinter.W)
        self.checkbox_KernelDensity.deselect()

        # Checkbox variables for the Kriging option.
        self.statusAnalysis_Kriging = tkinter.IntVar()
        self.checkbox_Kriging = \
            tkinter.Checkbutton(self.analysisOptionsLabelFrame, text="Kriging",
                                variable=self.statusAnalysis_Kriging)
        # command=self.func_Controls_For_Analysis_Options)
        self.checkbox_Kriging.grid(column=2, row=0, padx=0, pady=0,
                                   sticky=tkinter.W)
        self.checkbox_Kriging.deselect()

        # Checkbox variables for the Natural Neighbor option.
        self.statusAnalysis_NaturalNeighbor = tkinter.IntVar()
        self.checkbox_NaturalNeighbor = \
            tkinter.Checkbutton(self.analysisOptionsLabelFrame,
            text="Nat. Neigh.", variable=self.statusAnalysis_NaturalNeighbor)
        # command=self.func_Controls_For_Analysis_Options)
        self.checkbox_NaturalNeighbor.grid(column=0, row=1, padx=0, pady=0,
                                           sticky=tkinter.W)
        self.checkbox_NaturalNeighbor.deselect()

        # Checkbox variables for the Optimized Hot Spot option.
        self.statusAnalysis_OptHotSpot = tkinter.IntVar()
        self.checkbox_OptHotSpot = \
            tkinter.Checkbutton(self.analysisOptionsLabelFrame,
                text="Opt. Hot Spot", variable=self.statusAnalysis_OptHotSpot)
        # command=self.func_Controls_For_Analysis_Options)
        self.checkbox_OptHotSpot.grid(column=1, row=1, padx=0, pady=0,
                                      sticky=tkinter.W)
        self.checkbox_OptHotSpot.deselect()

        # Checkbox variables for the Point Density option.
        self.statusAnalysis_PointDensity = tkinter.IntVar()
        self.checkbox_PointDensity = \
            tkinter.Checkbutton(self.analysisOptionsLabelFrame,
                text="Point Dens.", variable=self.statusAnalysis_PointDensity)
        #, command=self.func_Window_Parameters_PointDensity)
        self.checkbox_PointDensity.grid(column=2, row=1, padx=0, pady=0,
                                        sticky=tkinter.W)
        self.checkbox_PointDensity.deselect()

        # Checkbox variables for the Spline option.
        self.statusAnalysis_Spline = tkinter.IntVar()
        self.checkbox_Spline = \
            tkinter.Checkbutton(self.analysisOptionsLabelFrame, text="Spline",
            variable=self.statusAnalysis_Spline)
        # command=self.func_Controls_For_Analysis_Options)
        self.checkbox_Spline.grid(column=0, row=2, padx=0, pady=0,
                                  sticky=tkinter.W)
        self.checkbox_Spline.deselect()

        # Checkbox variables for the Thiessen option.
        self.statusAnalysis_Thiessen = tkinter.IntVar()
        self.checkbox_Thiessen = \
            tkinter.Checkbutton(self.analysisOptionsLabelFrame, text="Thiessen",
            variable=self.statusAnalysis_Thiessen)
        # command=self.func_Controls_For_Analysis_Options)
        self.checkbox_Thiessen.grid(column=1, row=2, padx=0, pady=0,
                                    sticky=tkinter.W)
        self.checkbox_Thiessen.deselect()

        # Checkbox variables for the Trend option.
        self.statusAnalysis_Trend = tkinter.IntVar()
        self.checkbox_Trend = \
            tkinter.Checkbutton(self.analysisOptionsLabelFrame, text="Trend",
            variable=self.statusAnalysis_Trend)
        # command=self.func_Controls_For_Analysis_Options)
        self.checkbox_Trend.grid(column=2, row=2, padx=0, pady=0,
                                   sticky=tkinter.W)
        self.checkbox_Trend.deselect()

        # Checkbox variables for the Output Count Details to CSV File option.
        self.statusAnalysis_OutputToCSVFile = tkinter.IntVar()
        self.checkbox_OutputToCSVFile = \
            tkinter.Checkbutton(self.analysisOptionsLabelFrame,
            text="Output Count Details to CSV File",
            variable=self.statusAnalysis_OutputToCSVFile)
        # command=self.func_Controls_For_Analysis_Options)
        self.checkbox_OutputToCSVFile.grid(column=0, row=3, padx=0, pady=0,
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
            textvariable=self.stringState_Name, state="readonly")  # font =
        self.combo_State_Name["values"] = (dictKeys_StateNames)
        self.combo_State_Name.grid(column=0, row=0, padx = 5,
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
        self.combo_County_Name = ttk.Combobox(self.comboFrame_Counties,width=28,
                                    textvariable=self.stringCounty_Name,
                                    state="readonly")  # font =
        self.combo_County_Name["values"] = \
            (dict_state_counties[self.stringState_Name.get()])
        self.combo_County_Name.grid(column=0, row=0, padx = 5, sticky=tkinter.W)

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

                    # Create modified variable for County name, removing all
                    # instances of special characters or spacing.
                    self.modified_stringCountyName = \
                        self.stringCounty_Name.get().\
                        replace("'", "").replace("-", "").\
                        replace(".", "").replace(" ", "")

                    # Full string used for feature class naming purposes.
                    self.featureClass_County_State_Naming = "county_only_" + \
                                        self.modified_stringCountyName + "_" + \
                                        self.stringState_Name.get()

                    # Full string used for folder naming purposes.
                    self.folderNamingAddition = \
                        "_" + self.featureClass_County_State_Naming

                # If both timespan/diameter comboboxes are not "Custom..."...
                if self.stringHailTimespan.get() != "Custom..." and \
                        self.stringHailDiameter.get() != "Custom...":

                    # Assign naming conventions.
                    # (Mag/Timespan/Current Date broken out separately to be
                    # used later on for CSV files, XY Event Layers, and
                    # Feature Class).
                    self.only_Mag_Timespan_CurDate = self.mag_naming + "_" + \
                                str(self.timespan_url).replace("-", "_to_") + \
                                curDate

                    # Full Path Name to be used for output files
                    self.fullPathName = self.folderDialogPath + "/" + noaa + \
                                        "_" + hail + "_" + \
                                        self.only_Mag_Timespan_CurDate + \
                                        self.folderNamingAddition

                # If timespan combobox is "Custom..." and diameter combobox is
                # not "Custom..."...
                if self.stringHailTimespan.get() == "Custom..." and \
                        self.stringHailDiameter.get() != "Custom...":

                    # Assign naming conventions.
                    # (Mag/Timespan/Current Date broken out separately to be
                    # used later on for CSV files, XY Event Layers, and
                    # Feature Class).
                    self.only_Mag_Timespan_CurDate = self.mag_naming + \
                                    self.timespan_file_folder_naming + curDate

                    # Full Path Name to be used for output files
                    self.fullPathName = self.folderDialogPath + "/" + noaa + \
                                        "_" + hail + "_" + \
                                        self.only_Mag_Timespan_CurDate + \
                                        self.folderNamingAddition

                # If timespan is "Custom..." and diameter is "Custom..."...
                if self.stringHailTimespan.get() == "Custom..." and \
                        self.stringHailDiameter.get() == "Custom...":

                    # Assign naming conventions.
                    # (Mag/Timespan/Current Date broken out separately to be
                    # used later on for CSV files, XY Event Layers, and
                    # Feature Class).
                    self.only_Mag_Timespan_CurDate = \
                        self.custom_Diameter_Naming + \
                        self.timespan_file_folder_naming + curDate

                    # Full Path Name to be used for output files
                    self.fullPathName = self.folderDialogPath + "/" + noaa + \
                                        "_" + hail + "_" + \
                                        self.only_Mag_Timespan_CurDate + \
                                        self.folderNamingAddition

                # If timespan is not "Custom..." and diameter is "Custom..."...
                if self.stringHailTimespan.get() != "Custom..." and \
                        self.stringHailDiameter.get() == "Custom...":

                    # Assign naming conventions.
                    # (Mag/Timespan/Current Date broken out separately to be
                    # used later on for CSV files, XY Event Layers, and
                    # Feature Class).
                    self.only_Mag_Timespan_CurDate = \
                        self.custom_Diameter_Naming + "_" + \
                        str(self.timespan_url).replace("-", "_to_") + curDate

                    # Full Path Name to be used for output files
                    self.fullPathName = self.folderDialogPath + "/" + noaa + \
                                        "_" + hail + "_" + \
                                        self.only_Mag_Timespan_CurDate + \
                                        self.folderNamingAddition

            # If "More Options" checkbox is unchecked...
            if self.statusVar_Checkbutton_Options.get() == 0:

                # If both timespan/diameter comboboxes are not "Custom"...
                if self.stringHailTimespan.get() != "Custom..." and \
                        self.stringHailDiameter.get() != "Custom...":

                    # Assign naming conventions for output data and folders.
                    # (Mag/Timespan/Current Date broken out separately to be
                    # used later on for CSV files, XY Event Layers, and
                    # Feature Class).
                    self.only_Mag_Timespan_CurDate = self.mag_naming + "_" + \
                                str(self.timespan_url).replace("-", "_to_") + \
                                curDate

                    # Full Path Name to be used for output files
                    self.fullPathName = self.folderDialogPath + "/" + noaa + \
                                        "_" + hail + "_" + \
                                        self.only_Mag_Timespan_CurDate

                # If timespan combobox is "Custom..." and diameter combobox is
                # not "Custom..."...
                if self.stringHailTimespan.get() == "Custom..." and \
                        self.stringHailDiameter.get() != "Custom...":

                    # Assign naming conventions for output data and folders.
                    # (Mag/Timespan/Current Date broken out separately to be
                    # used later on for CSV files, XY Event Layers, and
                    # Feature Class).
                    self.only_Mag_Timespan_CurDate = self.mag_naming + \
                                    self.timespan_file_folder_naming + curDate

                    # Full Path Name to be used for output files
                    self.fullPathName = self.folderDialogPath + "/" + noaa + \
                                        "_" + hail + "_" + \
                                        self.only_Mag_Timespan_CurDate

                # If timespan combobox is "Custom..." and diameter combobox is
                # "Custom..."...
                if self.stringHailTimespan.get() == "Custom..." and \
                        self.stringHailDiameter.get() == "Custom...":

                    # Assign naming conventions for output data and folders.
                    # (Mag/Timespan/Current Date broken out separately to be
                    # used later on for CSV files, XY Event Layers, and
                    # Feature Class).
                    self.only_Mag_Timespan_CurDate = \
                        self.custom_Diameter_Naming + \
                        self.timespan_file_folder_naming + curDate

                    # Full Path Name to be used for output files
                    self.fullPathName = self.folderDialogPath + "/" + noaa + \
                                        "_" + hail + "_" + \
                                        self.only_Mag_Timespan_CurDate

                # If timespan combobox is not "Custom..." and diameter combobox
                # is "Custom..."...
                if self.stringHailTimespan.get() != "Custom..." and \
                        self.stringHailDiameter.get() == "Custom...":

                    # Assign naming conventions for output data and folders.
                    # (Mag/Timespan/Current Date broken out separately to be
                    # used later on for CSV files, XY Event Layers, and
                    # Feature Class).
                    self.only_Mag_Timespan_CurDate = \
                        self.custom_Diameter_Naming + "_" + \
                        str(self.timespan_url).replace("-", "_to_") + curDate

                    # Full Path Name to be used for output files
                    self.fullPathName = self.folderDialogPath + "/" + noaa + \
                                        "_" + hail + "_" + \
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
            self.func_DownloadCSV()

        except Exception as e:

            # Show error message.
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

            # Increment progress bar.
            self.func_ProgressBar_setProgress(9)

        except Exception as e:

            # Show error message.
            self.func_Scroll_setOutputText("Error Message: " + str(e) + "\n" +
                                           "Traceback: " +
                                           traceback.format_exc(), color_Red)

    def func_DownloadCSV(self):

        # This function controls the downloading of the CSV files from the web.

        try:

            # If timespan is not "Custom..."...
            if self.stringHailTimespan.get() != "Custom...":

                # If timespan equals All...
                if self.stringHailTimespan.get() == \
                    "All | 1955-" + str(int_OneYearAgo):

                    # Run function to create CSV subfolder.
                    self.func_Create_CSV_subFolder()

                    try:

                        self.func_Scroll_setOutputText("Downloading:\n" + noaa +
                                "_" + hail + "_" +
                                str(self.timespan_url).replace("-", "_to_") +
                                curDate + fileExtCSV + fileExtZip, None)

                        # Retrieve CSV from URL.
                        request.urlretrieve(self.textURLTextbox.get(),
                                    self.csvDirectory + "/" + noaa + "_" +
                                    hail + "_" +
                                    str(self.timespan_url).replace("-",
                                    "_to_") + curDate + fileExtCSV + fileExtZip)

                        self.func_Scroll_setOutputText("Download Complete.",
                                                       None)

                    # If download fails, try one more time (it could have been
                    # a small, temporary network glitch).
                    except:

                        self.func_Scroll_setOutputText(
                            "Download failed, trying again:\n" + noaa +
                            "_" + hail + "_" +
                            str(self.timespan_url).replace("-", "_to_") +
                            curDate + fileExtCSV + fileExtZip, color_Orange)

                        sleep(5)

                        # Retrieve CSV from URL.
                        request.urlretrieve(self.textURLTextbox.get(),
                                    self.csvDirectory + "/" + noaa + "_" +
                                    hail + "_" +
                                    str(self.timespan_url).replace("-",
                                    "_to_") + curDate + fileExtCSV + fileExtZip)

                        self.func_Scroll_setOutputText("Download Complete.",
                                                       None)


                    self.func_Scroll_setOutputText("Unzipping " + noaa + "_" +
                                hail + "_" +
                                str(self.timespan_url).replace("-", "_to_") +
                                curDate + fileExtCSV + fileExtZip, None)

                    # Unzip the CSV file within the same folder location.
                    unZipThisFile = zipfile.ZipFile(self.csvDirectory + "/" +
                                    noaa + "_" + hail + "_" +
                                    str(self.timespan_url).replace("-","_to_") +
                                    curDate + fileExtCSV + fileExtZip, 'r')

                    unZipThisFile.extractall(self.csvDirectory)

                    # Close file to prevent locks.
                    unZipThisFile.close()

                    # Rename the unzipped file to better represent the input
                    # user-defined parameters.
                    os.rename(self.csvDirectory + self.timespan_url + "_" +
                              hail + fileExtCSV, self.csvDirectory + noaa +
                              "_" + hail + "_" +
                              str(self.timespan_url).replace("-","_to_") +
                              curDate + fileExtCSV)

                    self.func_Scroll_setOutputText("CSV file unzipped.", None)

                    # Increment progress bar.
                    self.func_ProgressBar_setProgress(20)

                    # Run function to do data checks on the CSV file.
                    self.func_NonCustomTimespan_CSV_HeaderCheck_ValueCheck()

                else:

                    # Run function to create CSV subfolder.
                    self.func_Create_CSV_subFolder()

                    try:

                        self.func_Scroll_setOutputText(
                            "Downloading:\n" + noaa + "_" + hail + "_" +
                            str(self.timespan_url).replace("-", "_to_") +
                            curDate + fileExtCSV, None)

                        # Retrieve CSV from URL.
                        request.urlretrieve(self.textURLTextbox.get(),
                                self.csvDirectory + "/" + noaa + "_" + hail +
                                "_" +
                                str(self.timespan_url).replace("-", "_to_") +
                                curDate + fileExtCSV)

                        self.func_Scroll_setOutputText("Download Complete.",
                                                       None)

                    # If download fails, try one more time (it could have been
                    # a small, temporary network glitch).
                    except:

                        self.func_Scroll_setOutputText(
                            "Download failed, trying again:\n" + noaa + "_" +
                            hail + "_" +
                            str(self.timespan_url).replace("-", "_to_") +
                            curDate + fileExtCSV, color_Orange)

                        sleep(5)

                        # Retrieve CSV from URL.
                        request.urlretrieve(self.textURLTextbox.get(),
                                self.csvDirectory + "/" + noaa + "_" + hail +
                                "_" +
                                str(self.timespan_url).replace("-", "_to_") +
                                curDate + fileExtCSV)

                        self.func_Scroll_setOutputText("Download Complete.",
                                                       None)

                    # Increment progress bar.
                    self.func_ProgressBar_setProgress(20)

                    # Run function to do data checks on the CSV file.
                    self.func_NonCustomTimespan_CSV_HeaderCheck_ValueCheck()

            # If timespan is "Custom..."...
            if self.stringHailTimespan.get() == "Custom...":

                # Run function to create CSV subfolder.
                self.func_Create_CSV_subFolder()

                try:

                    self.func_Scroll_setOutputText("Downloading:\n" + noaa +
                                    "_" + hail + "_" +
                                    str(self.timespan_url).replace("-", "_") +
                                    curDate + fileExtCSV + fileExtZip, None)

                    # Retrieve CSV from URL.
                    request.urlretrieve(self.textURLTextbox.get(),
                                self.csvDirectory + "/" + noaa + "_" + hail +
                                "_" +
                                str(self.timespan_url).replace("-", "_to_") +
                                curDate + fileExtCSV + fileExtZip)

                    self.func_Scroll_setOutputText("Download Complete.", None)

                # If download fails, try one more time (it could have been
                # a small, temporary network glitch).
                except:

                    self.func_Scroll_setOutputText(
                                "Download failed, trying again:\n" + noaa +
                                "_" + hail + "_" +
                                str(self.timespan_url).replace("-", "_") +
                                curDate + fileExtCSV + fileExtZip, color_Orange)

                    sleep(5)

                    # Retrieve CSV from URL.
                    request.urlretrieve(self.textURLTextbox.get(),
                                self.csvDirectory + "/" + noaa + "_" + hail +
                                "_" +
                                str(self.timespan_url).replace("-", "_to_") +
                                curDate + fileExtCSV + fileExtZip)

                    self.func_Scroll_setOutputText("Download Complete.", None)

                self.func_Scroll_setOutputText("Unzipping " + noaa + "_" +
                                hail + "_" +
                                str(self.timespan_url).replace("-", "_to_") +
                                curDate + fileExtCSV + fileExtZip, None)

                # Unzip the CSV file within the same folder location.
                unZipThisFile = zipfile.ZipFile(self.csvDirectory + "/" +
                                noaa + "_" + hail + "_" +
                                str(self.timespan_url).replace("-", "_to_") +
                                curDate + fileExtCSV + fileExtZip, 'r')

                unZipThisFile.extractall(self.csvDirectory)

                # Close file to prevent locks.
                unZipThisFile.close()

                # Rename the unzipped file to better represent the input
                # user-defined parameters.
                os.rename(self.csvDirectory + self.timespan_url + "_" + hail +
                          fileExtCSV, self.csvDirectory + noaa + "_" + hail +
                          "_" + str(self.timespan_url).replace("-", "_to_") +
                          curDate + fileExtCSV)

                self.func_Scroll_setOutputText("CSV file unzipped.", None)

                # Increment progress bar.
                self.func_ProgressBar_setProgress(20)

                # Run function to do data checks on the CSV file.
                self.func_CustomTimespan_CSV_HeaderCheck_ValueCheck()

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
                                 "Possibly temporary internet issues?\n"
                                 "Please check connection and try again.")

        except Exception as e:

            # Display error message for all other errors.
            self.func_Scroll_setOutputText("Error Message: " + str(e) + "\n" +
                                           "Traceback: " +
                                           traceback.format_exc(), color_Red)

    def func_NonCustomTimespan_CSV_HeaderCheck_ValueCheck(self):

        # This function will take the downloaded CSV and assigned differing
        # naming conventions, while also doing header checks and analyzing data
        # for unneeded values or discrepancies.

        try:

            # If the diameter combobox displays "Custom..."...
            if self.stringHailDiameter.get() == "Custom...":

                # Open the CSV file.
                self.csv_InputFile = open(self.csvDirectory + "/" + noaa +
                                "_" + hail + "_" +
                                str(self.timespan_url).replace("-", "_to_") +
                                curDate + fileExtCSV)

                # Read the CSV file.
                self.csv_Reader = csv.reader(self.csv_InputFile)

                # Create/open a new CSV file for output modifications to be
                # written to.
                self.csv_OutputFile = open(self.csvDirectory + "/" + noaa +
                                "_" + hail + "_" +
                                self.custom_Diameter_Naming + "_" +
                                str(self.timespan_url).replace("-", "_to_") +
                                curDate + "_checked" + fileExtCSV, "w")

                # Write to the output CSV file.
                self.csv_Writer = csv.writer(self.csv_OutputFile, quotechar='"',
                                    delimiter=',', quoting=csv.QUOTE_ALL,
                                    skipinitialspace=True, lineterminator='\n')

                # This will be the output naming convention of the CSV file once
                # it has gone through all of its checks.
                self.csv_Check_If_Empty_CSV_Input = self.csvDirectory + "/" + \
                                noaa + "_" + hail + "_" + \
                                self.custom_Diameter_Naming + "_" + \
                                str(self.timespan_url).replace("-", "_to_") + \
                                curDate + "_checked" + fileExtCSV

                # This will be the naming convention of the output feature class
                # once converted from CSV.
                self.nameFeatureClass_FromCSV = noaa + "_" + hail + "_" + \
                        self.custom_Diameter_Naming + "_" + \
                        str(self.timespan_url).replace("-", "_to_") + curDate

            # If the diameter combobox does not display "Custom..."...
            elif self.stringHailDiameter.get() != "Custom...":

                # Open the CSV file.
                self.csv_InputFile = open(self.csvDirectory + "/" + noaa +
                                "_" + hail + "_" +
                                str(self.timespan_url).replace("-", "_to_") +
                                curDate + fileExtCSV)

                # Read the CSV file.
                self.csv_Reader = csv.reader(self.csv_InputFile)

                # Create/open a new CSV file for output modifications to be
                # written to.
                self.csv_OutputFile = open(self.csvDirectory + "/" + noaa +
                                "_" + hail + "_" + self.mag_naming + "_" +
                                str(self.timespan_url).replace("-", "_to_") +
                                curDate + "_checked" + fileExtCSV, "w")

                # Write to the output CSV file.
                self.csv_Writer = csv.writer(self.csv_OutputFile, quotechar='"',
                                    delimiter=',', quoting=csv.QUOTE_ALL,
                                    skipinitialspace=True, lineterminator='\n')

                # This will be the output naming convention of the CSV file once
                # it has gone through all of its checks.
                self.csv_Check_If_Empty_CSV_Input = self.csvDirectory + "/" + \
                                noaa + "_" + hail + "_" + self.mag_naming + \
                                "_" + \
                                str(self.timespan_url).replace("-", "_to_") + \
                                curDate + "_checked" + fileExtCSV

                # This will be the naming convention of the output feature class
                # once converted from CSV.
                self.nameFeatureClass_FromCSV = noaa + "_" + hail + "_" + \
                                self.mag_naming + "_" + \
                                str(self.timespan_url).replace("-", "_to_") + \
                                curDate

            self.func_Scroll_setOutputText("Checking CSV file for missing "
                                    "headers, erroneous lat/long values, and "
                                    "removing invalid hail sizes.", None)

            # Remove single quotes and spaces from the CSV's first row.
            firstLine = \
                str(next(self.csv_Reader)).replace("'", "").replace(" ", "")

            # If the hail headers exist in that CSV's first row...
            if hail_headers in firstLine:

                # Write the hail headers to the output CSV file, splitting
                # at the comma. The firstLine row will be skipped for the next
                # step.
                self.csv_Writer.writerow(hail_headers.split(","))

            else:

                # Else, if the hail headers are not present in the CSV's
                # first row, add the hail headers.
                self.csv_Writer.writerow(hail_headers.split(","))

                # Return to first row of input CSV file, since this row does not
                # represent a header.
                self.csv_InputFile.seek(0)

            # For each row in the input CSV...
            for row in self.csv_Reader:

                # If entire row is not empty and diameter column and lat/long
                # columns are not blank...
                if row and row[10] != "" and row[15] != "" and row[16] != "":

                    # If lat/long columns are not showing 0,0 coordinates...
                    if (row[15] != "0" or row[15] != "0.0") and \
                            (row[16] != "0" or row[16] != "0.0"):

                        # If lat/long columns are within appropriate range...
                        if float(row[15]) >= -90.0 and float(row[15]) <= 90.0 \
                                and float(row[16]) >= -180.0 and \
                                float(row[16]) <= 180.0:

                            # If the diameter is greater than zero and less than
                            # 9.99 (negative values and 9.99 indicate errors)...
                            if float(row[10]) > 0.0 and float(row[10]) < 9.99:

                                # If the hail diameter is set to All...
                                if self.stringHailDiameter.get() == "All":

                                    # Write the row to the output CSV.
                                    self.csv_Writer.writerow(row)

                                # If the hail diameter is set to 0.5" - 0.99"...
                                elif self.stringHailDiameter.get() == \
                                        '0.5" - 0.99"':

                                    # If the CSV row diameter is 0.5" - 0.99"...
                                    if float(row[10]) >= 0.5 and \
                                            float(row[10]) < 1.0:

                                        # Write the row to the output CSV.
                                        self.csv_Writer.writerow(row)

                                # If the hail diameter is set to 1.0" - 1.99"...
                                elif self.stringHailDiameter.get() == \
                                        '1.0" - 1.99"':

                                    # If the CSV row diameter is 1.0" - 1.99"...
                                    if float(row[10]) >= 1.0 and \
                                            float(row[10]) < 2.0:

                                        # Write the row to the output CSV.
                                        self.csv_Writer.writerow(row)

                                # If the hail diameter is set to 2.0" - 2.99"...
                                elif self.stringHailDiameter.get() == \
                                        '2.0" - 2.99"':

                                    # If the CSV row diameter is 2.0" - 2.99"...
                                    if float(row[10]) >= 2.0 and \
                                            float(row[10]) < 3.0:

                                        # Write the row to the output CSV.
                                        self.csv_Writer.writerow(row)

                                # If the hail diameter is set to 3.0"+...
                                elif self.stringHailDiameter.get() == '3.0"+':

                                    # If the CSV row diameter is 3.0"+...
                                    if float(row[10]) >= 3.0:

                                        # Write the row to the output CSV.
                                        self.csv_Writer.writerow(row)

                                # If the hail diameter is set to Custom...
                                elif self.stringHailDiameter.get() == \
                                        "Custom...":

                                    # If the CSV row diameter is between the
                                    # Diameter From/To selections...
                                    if float(row[10]) >= \
                                        float(self.textCustomDiameterFrom) and \
                                        float(row[10]) <= \
                                        float(self.textCustomDiameterTo):

                                        # Write the row to the output CSV.
                                        self.csv_Writer.writerow(row)

            # Close the input CSV (otherwise there may be a file lock).
            self.csv_InputFile.close()

            # Close the output CSV (otherwise there may be a file lock).
            self.csv_OutputFile.close()

            self.func_Scroll_setOutputText("CSV file checked.", None)

            # Increment progress bar.
            self.func_ProgressBar_setProgress(25)

            # Run function to check if output CSV file contains 0 hail.
            self.func_Check_If_Empty_CSV(self.csv_Check_If_Empty_CSV_Input)

        except Exception as e:

            # Display error message.
            self.func_Scroll_setOutputText("Error Message: " + str(e) + "\n" +
                                           "Traceback: " +
                                           traceback.format_exc(), color_Red)

            # Close the input CSV (otherwise there may be a file lock).
            self.csv_InputFile.close()

            # Close the output CSV (otherwise there may be a file lock).
            self.csv_OutputFile.close()

    def func_CustomTimespan_CSV_HeaderCheck_ValueCheck(self):

        # This function will take the downloaded CSV and assigned differing
        # naming conventions, while also doing header checks and analyzing data
        # for unneeded values or discrepancies.

        try:

            # If the diameter combobox displays "Custom..."...
            if self.stringHailDiameter.get() == "Custom...":

                # Open the CSV file.
                self.csv_InputFile = open(self.csvDirectory + "/" + noaa +
                                "_" + hail + "_" +
                                str(self.timespan_url).replace("-", "_to_") +
                                curDate + fileExtCSV)

                # Read the CSV file.
                self.csv_Reader = csv.reader(self.csv_InputFile)

                # Create/open a new CSV file for output modifications to be
                # written to.
                self.csv_OutputFile = open(self.csvDirectory + "/" + noaa +
                                "_" + hail + "_" + self.custom_Diameter_Naming +
                                self.timespan_file_folder_naming +
                                curDate + "_checked" + fileExtCSV, "w")

                # Write to the output CSV file.
                self.csv_Writer = csv.writer(self.csv_OutputFile, quotechar='"',
                                    delimiter=',', quoting=csv.QUOTE_ALL,
                                    skipinitialspace=True, lineterminator='\n')

                # This will be the output naming convention of the CSV file once
                # it has gone through all of its checks.
                self.csv_Check_If_Empty_CSV_Input = self.csvDirectory + "/" + \
                                            noaa + "_" + hail + "_" + \
                                            self.custom_Diameter_Naming + \
                                            self.timespan_file_folder_naming + \
                                            curDate + "_checked" + fileExtCSV

                # This will be the naming convention of the output feature class
                # once converted from CSV.
                self.nameFeatureClass_FromCSV = noaa + "_" + hail + "_" + \
                                    self.custom_Diameter_Naming + \
                                    self.timespan_file_folder_naming + curDate

            # If the diameter combobox does not display "Custom..."...
            elif self.stringHailDiameter.get() != "Custom...":

                # Open the CSV file.
                self.csv_InputFile = open(self.csvDirectory + "/" + noaa +
                                "_" + hail + "_" +
                                str(self.timespan_url).replace("-", "_to_") +
                                curDate + fileExtCSV)

                # Read the CSV file.
                self.csv_Reader = csv.reader(self.csv_InputFile)

                # Create/open a new CSV file for output modifications to be
                # written to.
                self.csv_OutputFile = open(self.csvDirectory + "/" + noaa +
                                        "_" + hail + "_" + self.mag_naming +
                                        self.timespan_file_folder_naming +
                                        curDate + "_checked" + fileExtCSV, "w")

                # Write to the output CSV file.
                self.csv_Writer = csv.writer(self.csv_OutputFile, quotechar='"',
                                    delimiter=',', quoting=csv.QUOTE_ALL,
                                    skipinitialspace=True, lineterminator='\n')

                # This will be the output naming convention of the CSV file once
                # it has gone through all of its checks.
                self.csv_Check_If_Empty_CSV_Input = self.csvDirectory + "/" + \
                                            noaa + "_" + hail + "_" + \
                                            self.mag_naming + \
                                            self.timespan_file_folder_naming + \
                                            curDate + "_checked" + fileExtCSV

                # This will be the naming convention of the output feature class
                # once converted from CSV.
                self.nameFeatureClass_FromCSV = noaa + "_" + hail + "_" + \
                                            self.mag_naming + \
                                            self.timespan_file_folder_naming + \
                                            curDate

            self.func_Scroll_setOutputText("Checking CSV file for missing "
                                    "headers, erroneous lat/long values, and "
                                    "removing invalid hail sizes.", None)

            # Remove single quotes and spaces from the CSV's first row.
            firstLine = \
                str(next(self.csv_Reader)).replace("'", "").replace(" ", "")

            # If the hail headers exist in that CSV's first row...
            if hail_headers in firstLine:

                # Write the hail headers to the output CSV file, splitting
                # at the comma. The firstLine row will be skipped for the next
                # step.
                self.csv_Writer.writerow(hail_headers.split(","))

            else:

                # Else, if the hail headers are not present in the CSV's
                # first row, add the hail headers.
                self.csv_Writer.writerow(hail_headers.split(","))

                # Return to first row of input CSV file, since this row does not
                # represent a header.
                self.csv_InputFile.seek(0)

            # Variable declarations with no values assigned. These will be used
            # in the following for loop.
            fromDate = None
            toDate = None
            date_in_row = None

            # For each row in the input CSV...
            for row in self.csv_Reader:

                try:

                    # First, try to identify the CSV row's date (date_in_row)
                    # by combining the Year, Month, and Day fields. If the days
                    # of the month are out of range (e.g. June 31st), this will
                    # cause a ValueError to occur. If that happens, a different
                    # approach will be attempted within the except clause.

                    # User-defined variables combined to create the FROM date.
                    # YYYY, MM, DD. DD is set to 1.
                    fromDate = datetime.date(int(self.textCustomYearFrom),
                                             int(self.textCustomMonthFrom), 1)

                    # User-defined variables combined to create the TO date.
                    # YYYY, MM, DD. DD is set to the monthly range of the
                    # specific YYYYMM combination.
                    toDate = datetime.date(int(self.textCustomYearTo),
                                           int(self.textCustomMonthTo),
                                           calendar.monthrange(
                                               int(self.textCustomYearTo),
                                               int(self.textCustomMonthTo))[1])

                    # Year, Month, and Day column values from CSV combined to
                    # create a date field for each row.
                    date_in_row = \
                        datetime.date(int(row[1]), int(row[2]), int(row[3]))

                except ValueError:

                    # If the above Try block fails (likely due to a monthrange
                    # problem like June 31st being assigned within the CSV), the
                    # code will attempt to identify the CSV row's date by
                    # analyzing an additional column that has the YYYY/MM/DD
                    # fields combined into one. If this field does not have the
                    # same typos, it will proceed successfully with the
                    # following modification.

                    try:

                        # Assign the YYYYMM's monthly range in days.
                        monthRange = \
                            calendar.monthrange(int(self.textCustomYearFrom),
                                            int(self.textCustomMonthFrom))[1]

                        # Create FROM date by combining YYYY, MM, and DD
                        # parameters.
                        fromDate = \
                            datetime.datetime.strptime(self.textCustomYearFrom +
                                            "-" + self.textCustomMonthFrom +
                                            "-1","%Y-%m-%d")

                        # Create TO date by combining YYYY, MM, and DD
                        # parameters.
                        toDate = \
                            datetime.datetime.strptime(self.textCustomYearTo +
                                            "-" + self.textCustomMonthTo +
                                            "-" + str(monthRange), "%Y-%m-%d")

                        # Format the "date" column within the CSV into the
                        # following date format so that it can be used to
                        # compare itself to the fromDate and toDate variables.
                        date_in_row = datetime.datetime.strptime(row[4],
                                                    "%Y-%m-%d")  # '%m/%d/%Y')

                    except ValueError:

                        # If the "date" column within the CSV also shows invalid
                        # date values, then proceed to skip this row.
                        pass

                # If entire row is not empty and the date in CSV row is between
                # the from and to dates...
                if row and fromDate <= date_in_row <= toDate:

                    # If diameter column and lat/long columns are not blank...
                    if row[10] != "" and row[15] != "" and row[16] != "":

                        # If lat/long columns are not showing 0,0 coordinates...
                        if (row[15] != "0" or row[15] != "0.0") and \
                                (row[16] != "0" or row[16] != "0.0"):

                            # If lat/long columns are within appropriate range..
                            if float(row[15]) >= -90.0 and \
                                    float(row[15]) <= 90.0 and \
                                    float(row[16]) >= -180.0 and \
                                    float(row[16]) <= 180.0:

                                # If the diameter is greater than zero and less
                                # than 9.99 (negative values and 9.99 indicate
                                # errors)...
                                if float(row[10]) > 0.0 and \
                                        float(row[10]) < 9.99:

                                    # If hail diameter selection is All...
                                    if self.stringHailDiameter.get() == "All":

                                        # Write the row to the output CSV.
                                        self.csv_Writer.writerow(row)

                                    # If hail diameter selection is 0.5" - 0.99"
                                    elif self.stringHailDiameter.get() == \
                                            '0.5" - 0.99"':

                                        # If hail diameter in CSV is within this
                                        # range...
                                        if float(row[10]) >= 0.5 and \
                                                float(row[10]) < 1.0:

                                            # Write the row to the output CSV.
                                            self.csv_Writer.writerow(row)

                                    # If hail diameter selection is 1.0" - 1.99"
                                    elif self.stringHailDiameter.get() == \
                                            '1.0" - 1.99"':

                                        # If hail diameter in CSV is within this
                                        # range...
                                        if float(row[10]) >= 1.0 and \
                                                float(row[10]) < 2.0:

                                            # Write the row to the output CSV.
                                            self.csv_Writer.writerow(row)

                                    # If hail diameter selection is 2.0" - 2.99"
                                    elif self.stringHailDiameter.get() == \
                                        '2.0" - 2.99"':

                                        # If hail diameter in CSV is within this
                                        # range...
                                        if float(row[10]) >= 2.0 and \
                                                float(row[10]) < 3.0:

                                            # Write the row to the output CSV.
                                            self.csv_Writer.writerow(row)

                                    # If hail diameter selection is 3.0"+...
                                    elif self.stringHailDiameter.get() == \
                                            '3.0"+':

                                        # If hail diameter in CSV is within this
                                        # range...
                                        if float(row[10]) >= 3.0:

                                            # Write the row to the output CSV.
                                            self.csv_Writer.writerow(row)

                                    # If hail diameter selection is Custom...
                                    elif self.stringHailDiameter.get() == \
                                            "Custom...":

                                        # If CSV row's hail diameter is between
                                        # the Min and Max range...
                                        if float(row[10]) >= \
                                            float(self.textCustomDiameterFrom) \
                                                and float(row[10]) <= \
                                            float(self.textCustomDiameterTo):

                                            # Write the row to the output CSV.
                                            self.csv_Writer.writerow(row)

            # Close the input CSV (otherwise there may be a file lock).
            self.csv_InputFile.close()

            # Close the output CSV (otherwise there may be a file lock).
            self.csv_OutputFile.close()

            self.func_Scroll_setOutputText("CSV file checked.", None)

            # Increment progress bar.
            self.func_ProgressBar_setProgress(25)

            # Run function to check if output CSV file contains 0 hail.
            self.func_Check_If_Empty_CSV(self.csv_Check_If_Empty_CSV_Input)

        except Exception as e:

            # Display error message for all other errors.
            self.func_Scroll_setOutputText("Error Message: " + str(e) + "\n" +
                                           "Traceback: " +
                                           traceback.format_exc(), color_Red)

            # Close the input CSV (otherwise there may be a file lock).
            self.csv_InputFile.close()

            # Close the output CSV (otherwise there may be a file lock).
            self.csv_OutputFile.close()


    def func_Check_If_Empty_CSV(self, csvName):

        # This function checks to see the output, checked CSV file contains any
        # hail records.

        try:

            # Open the output, checked CSV file...
            with open(csvName) as csvFile:

                # Count all records within the CSV file. Assign the count total
                # to a raw hail count variable.
                self.raw_hail_count = sum(1 for row in csvFile)

                # If the hail count is less than 1...
                if self.raw_hail_count <= 1:

                    # Display error message explaining that no hail
                    # records exist within the CSV file. The function will exit
                    # from here.
                    messagebox.showerror(errorMessage_Header,
                                    message="CSV file contains no data!\n" + \
                                    "Unable to create GIS data.")

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

                    # Else if hail records exist, but are in excess of
                    # 500,000 records...
                    if self.raw_hail_count >= 500000:

                        # Inform the user that the next geoprocessing tasks may
                        # take considerable time to execute.
                        self.func_Scroll_setOutputText("BE ADVISED:\n" +
                            "The CSV contains " + '{:,}'.format(
                            self.raw_hail_count) + " features.\n" +
                            "All additional processes may take considerable "
                            "time to complete.", color_Orange)

                        # Pause the script for five seconds to allow the user
                        # ample time to read the message.
                        sleep(5)

                    # Increment progress bar.
                    self.func_ProgressBar_setProgress(28)

                    # Execute function to create feature class from CSV file.
                    self.func_CreateFeatureClass_from_CSV(
                        self.csv_Check_If_Empty_CSV_Input,
                        self.nameFeatureClass_FromCSV)

        except Exception as e:

            # Display error message for all other errors.
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

    def func_CreateFeatureClass_from_CSV(
            self, csvName, nameFeatureClass_FromCSV):

        # This function controls the process of creating a GIS subfolder where
        # an output File GDB will be stored with a feature class created from
        # the checked CSV file. During this process, the CSV file is converted
        # into a feature class. This feature class is used to create a new,
        # re-projected feature class of the same data. The original feature
        # class is deleted, and the re-projected feature class naming convention
        # is changed to match the original feature class that was deleted.

        try:

            # Set input CSV argument as name of unclipped, unprojected feature
            # class.
            self.featureClass_Hail_Unclipped_Unprojected = \
                nameFeatureClass_FromCSV

            # Set name for GIS Subfolder creation.
            self.subFolder_GIS = self.fullPathName + "/GIS_Folder/"

            self.func_Scroll_setOutputText("Creating GIS subfolder...", None)

            # If the GIS subfolder doesn't already exist, create it.
            if not os.path.exists(self.subFolder_GIS):
                os.makedirs(self.subFolder_GIS)

                self.func_Scroll_setOutputText("GIS subfolder created.", None)

            # Increment progress bar.
            self.func_ProgressBar_setProgress(31)

            # Pause script for half a second.
            sleep(0.5)

            self.func_Scroll_setOutputText("Creating File GDB...", None)

            # Create File GDB within the GIS subfolder.
            arcpy.CreateFileGDB_management(self.subFolder_GIS, nameFileGDB)

            # Display ArcPy geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            self.func_Scroll_setOutputText("File GDB created.", None)

            # Increment progress bar.
            self.func_ProgressBar_setProgress(34)

            self.func_Scroll_setOutputText(
                "Creating temporary XY Event Layer from CSV...", None)

            # XY Event Layer input parameters.
            inputFile = csvName
            input_X_Field = "slon"
            input_Y_Field = "slat"
            outputFile = "in_memory/csv_XY_EventLayer"
            spatialReferenceType = None
            input_Z_Field = None

            # Process: Make temporary XY Event Layer (Geographic Coordinate
            # system defaults to WGS84 when spatial reference set to None).
            arcpy.MakeXYEventLayer_management(inputFile, input_X_Field,
                                              input_Y_Field, outputFile,
                                              spatialReferenceType,
                                              input_Z_Field)

            # Display ArcPy geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            self.func_Scroll_setOutputText(
                "Temporary XY Event Layer from CSV created.", None)

            # Increment progress bar.
            self.func_ProgressBar_setProgress(37)

            self.func_Scroll_setOutputText(
                "Creating Feature Class from XY Event Layer...", None)

            # Convert temporary XY Event Layer into a feature class stored
            # within the File GDB.
            arcpy.FeatureClassToFeatureClass_conversion(outputFile,
                            self.subFolder_GIS + nameFileGDB,
                            self.featureClass_Hail_Unclipped_Unprojected)

            # Display ArcPy geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            self.func_Scroll_setOutputText(
                "Feature Class from XY Event Layer created.", None)

            # Set workspace to the File GDB for following tasks.
            arcpy.env.workspace = self.subFolder_GIS + nameFileGDB

            # Create new variable for unclipped, projected feature class name.
            # This will be a temporary naming convention.
            self.featureClass_Hail_Unclipped_Projected = \
                    self.featureClass_Hail_Unclipped_Unprojected + \
                    "_Projected"

            self.func_Scroll_setOutputText("Projecting feature class to PCS " +
                            pcsReferenceString +
                            " with Central Meridian Offset (-30.0 degrees)...",
                            None)

            # Set projected coordinate system of feature class to the designated
            # PCS reference with -30.0 Central Meridian offset.
            arcpy.Project_management(
                self.featureClass_Hail_Unclipped_Unprojected,
                self.featureClass_Hail_Unclipped_Projected, pcsReference)

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
                self.featureClass_Hail_Unclipped_Projected)

            # Display ArcPy geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            self.func_Scroll_setOutputText("Feature class extent recalculated.",
                                           None)

            self.func_Scroll_setOutputText("Deleting feature class " +
                        self.featureClass_Hail_Unclipped_Unprojected +
                        " from File GDB...", None)

            # Delete original feature class conversion from CSV.
            arcpy.Delete_management(
                self.featureClass_Hail_Unclipped_Unprojected)

            # Display ArcPy geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            self.func_Scroll_setOutputText(
                "Feature class deleted from File GDB.", None)

            self.func_Scroll_setOutputText("Renaming feature class " +
                self.featureClass_Hail_Unclipped_Projected + " to " +
                self.featureClass_Hail_Unclipped_Unprojected + "...",
                None)

            # Rename the projected feature class to the unprojected feature
            # class name that was just deleted.
            arcpy.Rename_management(
                self.featureClass_Hail_Unclipped_Projected,
                self.featureClass_Hail_Unclipped_Unprojected)

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

                # Then execute function to clip hail features to the
                # polygon boundary for US states and DC.
                self.func_FeatureClass_Clip(self.nameFeatureClass_FromCSV,
                                featureClass_50States_and_DC_only,
                                "clipped_" + self.nameFeatureClass_FromCSV)

                # Execute function to verify if clipped hail feature class
                # still contains any features.
                self.func_Check_If_Empty_Output_FeatureClass(
                    self.clipped_Output_FeatureClass)

                # Execute function that controls analysis options.
                self.func_Controls_For_Analysis_Options(
                    featureClass_50States_and_DC_only)

            # If the radio button is State...
            elif self.radioButton_Selection == 2:

                # Execute function that downloads/unzips the Census Bureau's
                # Shapefile.
                self.func_Download_Unzip_Census_Shapefile()

                # Once Census Shapefile has been downloaded, execute function
                # to extract state selection only.
                self.func_Extract_State_Selection_Only(
                    self.subFolder_CensusShapefile + "/" +
                    census_URL_CountyShapefile_FileName + fileExtShp,
                    self.subFolder_GIS + "/" + nameFileGDB)

                # Then execute function to clip hail features to the
                # polygon state boundary.
                self.func_FeatureClass_Clip(self.nameFeatureClass_FromCSV,
                                    self.featureClass_State_Selection_Only,
                                    "clipped_" + self.nameFeatureClass_FromCSV)

                # Execute function to verify if clipped hail feature class
                # still contains any features.
                self.func_Check_If_Empty_Output_FeatureClass(
                    self.clipped_Output_FeatureClass)

                # Execute function that controls analysis options.
                self.func_Controls_For_Analysis_Options(
                    self.featureClass_State_Selection_Only)

            # If the radio button is County...
            elif self.radioButton_Selection == 3:

                # Execute function that downloads/unzips the Census Bureau's
                # Shapefile.
                self.func_Download_Unzip_Census_Shapefile()

                # Once Census Shapefile has been downloaded, execute function
                # to extract the county selection only.
                self.func_Extract_County_Selection_Only(
                    self.subFolder_CensusShapefile + "/" +
                    census_URL_CountyShapefile_FileName + fileExtShp,
                    self.subFolder_GIS + "/" + nameFileGDB)

                # Then execute function to clip hail features to the
                # polygon county boundary.
                self.func_FeatureClass_Clip(self.nameFeatureClass_FromCSV,
                                    self.featureClass_County_State_Naming,
                                    "clipped_" + self.nameFeatureClass_FromCSV)

                # Execute function to verify if clipped hail feature class
                # still contains any features.
                self.func_Check_If_Empty_Output_FeatureClass(
                    self.clipped_Output_FeatureClass)

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
                        fileGDB_Path + "/" + featureClass_50States_and_DC_only)

            # Display geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            self.func_Scroll_setOutputText(
                "Census Shapefile copied to File GDB.", None)

            # Increment progress bar.
            self.func_ProgressBar_setProgress(55)

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

            # Increment progress bar.
            self.func_ProgressBar_setProgress(56)

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

            # Increment progress bar.
            self.func_ProgressBar_setProgress(57)

            self.func_Scroll_setOutputText(
                "Recalculating extent for feature class...", None)

            # Recalculate extent of the projected Census feature class.
            arcpy.RecalculateFeatureClassExtent_management(
                self.featureClass_Polygons_Projected)

            # Display geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            self.func_Scroll_setOutputText("Feature class extent recalculated.",
                                           None)

            # Increment progress bar.
            self.func_ProgressBar_setProgress(58)

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

            # Increment progress bar.
            self.func_ProgressBar_setProgress(59)

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

            # Increment progress bar.
            self.func_ProgressBar_setProgress(60)

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

            # Increment progress bar.
            self.func_ProgressBar_setProgress(55)

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
                    dict_StateName_StateFIPs.get(self.stringState_Name.get()):

                        # Delete polygon feature.
                        cursor.deleteRow()

            # Get geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            self.func_Scroll_setOutputText("State selection(" +
                                        self.stringState_Name.get() +
                                        ") extracted from Feature Class.", None)

            # Increment progress bar.
            self.func_ProgressBar_setProgress(56)

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

            # Increment progress bar.
            self.func_ProgressBar_setProgress(57)

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

            # Increment progress bar.
            self.func_ProgressBar_setProgress(58)

            self.func_Scroll_setOutputText("Deleting feature class " +
                                    self.featureClass_State_Selection_Only  +
                                    " from File GDB...", None)

            # Delete the original, pre-projected Census feature class from the
            # File GDB. It is no longer needed.
            arcpy.Delete_management(self.featureClass_State_Selection_Only )

            # Get geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            self.func_Scroll_setOutputText(
                "Feature class deleted from File GDB.", None)

            # Increment progress bar.
            self.func_ProgressBar_setProgress(59)

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

            # Increment progress bar.
            self.func_ProgressBar_setProgress(60)

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

            # Increment progress bar.
            self.func_ProgressBar_setProgress(55)

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
                                        " extracted from Feature Class.", None)

            # Increment progress bar.
            self.func_ProgressBar_setProgress(56)

            # Set workspace for the following tasks.
            arcpy.env.workspace = fileGDB_Path

            # Set naming convention variable for projecting Census feature
            # class.
            self.featureClass_Polygons_Projected = \
                self.featureClass_County_State_Naming + "_Projected"

            self.func_Scroll_setOutputText("Projecting feature class to PCS " +
                    pcsReferenceString +
                    " with Central Meridian Offset (-30.0 degrees)...", None)

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

            # Increment progress bar.
            self.func_ProgressBar_setProgress(57)

            self.func_Scroll_setOutputText(
                "Recalculating extent for feature class...", None)

            # Recalculate extent of the projected Census feature class.
            arcpy.RecalculateFeatureClassExtent_management(
                self.featureClass_Polygons_Projected)

            # Get geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            self.func_Scroll_setOutputText("Feature class extent recalculated.",
                                           None)

            # Increment progress bar.
            self.func_ProgressBar_setProgress(58)

            self.func_Scroll_setOutputText("Deleting feature class " +
                                        self.featureClass_County_State_Naming  +
                                        " from File GDB...", None)

            # Delete the original, pre-projected Census feature class from the
            # File GDB. It is no longer needed.
            arcpy.Delete_management(self.featureClass_County_State_Naming )

            # Get geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            self.func_Scroll_setOutputText(
                "Feature class deleted from File GDB.", None)

            # Increment progress bar.
            self.func_ProgressBar_setProgress(59)

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

            # Increment progress bar.
            self.func_ProgressBar_setProgress(60)

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
        # hail point feature class to the user-selected Census polygon
        # boundary feature class.

        try:

            # Set the workspace to the File GDB for the following tasks.
            arcpy.env.workspace = self.subFolder_GIS + "/" + nameFileGDB

            # Set a new variable name for clipping based on this argument.
            self.clipped_Output_FeatureClass = outputFC_Name

            # If the user selects USA...
            if self.radioButton_Selection == 1:

                # Display this particular message before executing the clip.
                self.func_Scroll_setOutputText(
                    "Clipping hail features to 50 states and DC...", None)

            # If the user selects State...
            elif self.radioButton_Selection == 2:

                # Display this particular message before executing the clip.
                self.func_Scroll_setOutputText(
                    "Clipping hail features to state selection(" +
                    self.stringState_Name.get() + ")...", None)

            # If the user selects County...
            elif self.radioButton_Selection == 3:

                # Display this particular message before executing the clip.
                self.func_Scroll_setOutputText(
                    "Clipping hail features to " +
                    self.stringCounty_Name.get() + ", " +
                    self.stringState_Name.get() + "...", None)

            # Perform a clip of the hail point features to the specified
            # polygon boundary.
            arcpy.Clip_analysis(inputFC, clipFC,
                                self.clipped_Output_FeatureClass)

            # Display geoprocessing messages.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

            # If the user selects USA...
            if self.radioButton_Selection == 1:

                # Display this particular message after executing the clip.
                self.func_Scroll_setOutputText("Hail features have been "
                                        "clipped to 50 states and DC.", None)

            # If the user selects State...
            if self.radioButton_Selection == 2:

                # Display this particular message after executing the clip.
                self.func_Scroll_setOutputText("Hail features have been "
                                               "clipped to state selection(" +
                                               self.stringState_Name.get() +
                                               ").", None)

            # If the user selects County...
            if self.radioButton_Selection == 3:

                # Display this particular message after executing the clip.
                self.func_Scroll_setOutputText("Hail features have been "
                                "clipped to " + self.stringCounty_Name.get() +
                                ", " + self.stringState_Name.get() + ".", None)

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

    def func_Check_If_Empty_Output_FeatureClass(self,
                                                clipped_FeatureClass_Points):

        # This function controls the processes that check to ensure the clipped
        # hail point feature class have features once clipped.

        # Set workspace to File GDB.
        arcpy.env.workspace = self.subFolder_GIS + "/" + nameFileGDB

        # Get the feature count of the input argument and assign to count
        # variable.
        self.hailCountResult = \
            arcpy.GetCount_management(clipped_FeatureClass_Points)

        # Store the integer version of the hail count to variable.
        self.clipped_hailCount = \
            int(self.hailCountResult.getOutput(0))

        # If user selects USA...
        if self.radioButton_Selection == 1:

            # Display this particular message with hail count value.
            self.func_Scroll_setOutputText(str(self.clipped_hailCount) +
            " hail features observed within the 50 states and DC.", None)

        # If user selects State...
        if self.radioButton_Selection == 2:

            # Display this particular message with hail count value.
            self.func_Scroll_setOutputText(str(self.clipped_hailCount) +
                                    " hail features observed within " +
                                    self.stringState_Name.get() + ".", None)

        # If user selects County...
        if self.radioButton_Selection == 3:

            # Display this particular message with hail count value.
            self.func_Scroll_setOutputText(str(self.clipped_hailCount) +
                                    " hail features observed within " +
                                    self.stringCounty_Name.get() + ", " +
                                    self.stringState_Name.get() + ".", None)

        # Increment progress bar.
        self.func_ProgressBar_setProgress(67)

        # Pause script for one second.
        sleep(1)

        # If zero hail features present within the feature class...
        if self.clipped_hailCount < 1:

            # Display this message and error message to the user, since the
            # script can't proceed any farther.
            self.func_Scroll_setOutputText("1 or fewer hail features "
                        "present within the timespan/diameter/location.\n" +
                        "Unable to continue with analysis.", color_Red)

            messagebox.showerror(errorMessage_Header,
                                 "No hail features present within the "
                                 "timespan/diameter/location.\n" +
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

                # Set the workspace for the following analysis.
                arcpy.env.workspace = self.subFolder_GIS + "/" + nameFileGDB

                self.func_Scroll_setOutputText(
                    "Compiling count results to CSV file...", None)

                # If the user selects USA clipping option...
                if self.radioButton_Selection == 1:

                    # Perform spatial join of clipped hail feature class
                    # and the USA polygon feature class. Store output in_memory.
                    arcpy.SpatialJoin_analysis(self.clipped_Output_FeatureClass,
                                            featureClass_50States_and_DC_only,
                                            "in_memory/SpatialJoin")

                    # Create/Open a new CSV file within the CSV subfolder for
                    # data counts to be written into.
                    csvFile = open(self.csvDirectory + "DataCounts_" +
                                   self.nameFeatureClass_FromCSV +
                                   self.folderNamingAddition + fileExtCSV, "w")

                    # If timespan and diameter drop-downs don't show Custom...
                    if self.stringHailTimespan.get() != "Custom..." and \
                            self.stringHailDiameter.get() != "Custom...":

                        # Write the following lines into the data counts CSV.
                        csvFile.write("Timespan:," +
                                self.stringHailTimespan.get() + ",\n")
                        csvFile.write("Diameter Range (Inches):," +
                                self.stringHailDiameter.get() + ",\n")

                    # If timespan drop-down shows Custom and diameter doesn't..
                    if self.stringHailTimespan.get() == "Custom..." and \
                            self.stringHailDiameter.get() != "Custom...":

                        # WRite the following lines into the data counts CSV.
                        csvFile.write("Timespan:," + self.textCustomYearFrom +
                                        self.textCustomMonthFrom.zfill(2) +
                                        "-" + self.textCustomYearTo +
                                        self.textCustomMonthTo.zfill(2) + ",\n")
                        csvFile.write("Diameter Range (Inches):," +
                                self.stringHailDiameter.get() + ",\n")

                    # If timespan and diameter drop-downs both show Custom...
                    if self.stringHailTimespan.get() == "Custom..." and \
                            self.stringHailDiameter.get() == "Custom...":

                        # Write the following lines into the data counts CSV.
                        csvFile.write("Timespan:," + self.textCustomYearFrom +
                                      self.textCustomMonthFrom.zfill(2) +
                                      "-" + self.textCustomYearTo +
                                      self.textCustomMonthTo.zfill(2) + ",\n")
                        csvFile.write("Diameter Range (Inches):," +
                                      self.textCustomDiameterFrom + "-" +
                                      self.textCustomDiameterTo + ",\n")

                    # If timespan drop-down doesn't show Custom and Diameter
                    # does...
                    if self.stringHailTimespan.get() != "Custom..." and \
                        self.stringHailDiameter.get() == "Custom...":

                        # Write the following lines into the data counts CSV.
                        csvFile.write("Timespan:," +
                                    self.stringHailTimespan.get() + ",\n")
                        csvFile.write("Diameter Range (Inches):," +
                                      self.textCustomDiameterFrom + "-" +
                                      self.textCustomDiameterTo + ",\n")

                    # Now write the following lines, regardless of
                    # timespan/diameter selection.
                    csvFile.write("\n")
                    csvFile.write("USA (and DC) Hail:," +
                                  str(self.clipped_hailCount) + ",\n")
                    csvFile.write("\n")
                    csvFile.write("Nationwide Hail Data,\n")
                    csvFile.write("V,V,V,V,V,\n")
                    csvFile.write("Minimum Diameter,Maximum Diameter,"
                                  "Mean Diameter,Median Diameter,"
                                  "Mode Diameter,\n")

                    # Create empty list to store all US diameter values.
                    magList_US = []

                    # Open the in_memory spatial join as a Search Cursor,
                    # with analysis fields set to FIPS code and diameter.
                    with arcpy.da.SearchCursor("in_memory/SpatialJoin",
                                            [census_Shapefile_Field_StateFIPS,
                                             analysis_Mag_Field]) as cursor:

                        # For each feature within the spatial join...
                        for row in cursor:

                            # Add the magnitude to the US list.
                            magList_US.append(row[1])

                    try:

                        # Calculate mode of all diameters within US list.
                        modeValue_US = mode(magList_US)

                        # Convert mode information to float and then to
                        # string with two decimal places.
                        modeString_US = \
                            str("{0:.2f}".format(float(modeValue_US)))

                    except StatisticsError:

                        # This catches any lists containing no mode.
                        # This will occur if all values within list are
                        # unique values.

                        # Assign mode to the following phrase.
                        modeString_US = "No Unique Mode"

                        pass

                    # Write the following data to the data counts CSV.
                    # Min diameter, max diameter, mean diameter, median
                    # diameter, and mode diameter.
                    csvFile.write(str(min(magList_US)) + "," +
                            str(max(magList_US)) + "," +
                            str("{0:.2f}".format(numpy.mean(magList_US)) + "," +
                            str("{0:.2f}".format(numpy.median(magList_US))) +
                            "," + modeString_US + "," + ",\n"))

                    csvFile.write("\n")
                    csvFile.write("Hail Data per State,\n")
                    csvFile.write("V,V,V,V,V,V,V,V,\n")
                    csvFile.write("States with Hail,Hail Count,"
                                  "Minimum Diameter,Maximum Diameter,"
                                  "Mean Diameter,Median Diameter,"
                                  "Mode Diameter,State FIPS Code,\n")

                    # Create empty list for storing hail/diameter values.
                    magList_State = []

                    # For each state value in the ordered dictionary...
                    for key in dictKeys_OrderedDict_StateNames:

                        # Set counter to zero, for counting hail within
                        # each state during loop.
                        counter = 0

                        # Clears magList after each state count has concluded.
                        magList_State.clear()

                        # Open the in_memory spatial join as a Search Cursor,
                        # with analysis fields set to FIPS code and diameter.
                        with arcpy.da.SearchCursor("in_memory/SpatialJoin",
                                            [census_Shapefile_Field_StateFIPS,
                                             analysis_Mag_Field]) as cursor:

                            # For each feature within the spatial join...
                            for row in cursor:

                                # If FIPS code matches a state in the ordered
                                # dictionary...
                                if row[0] == \
                                        dictKeys_OrderedDict_StateNames[key]:

                                    # Append row information to magList.
                                    magList_State.append(row[1])

                                    # Increment counter by one.
                                    counter = counter + 1

                        # If counter is greater than zero...
                        if counter > 0:

                            try:

                                # Calculate mode of all diameters within list.
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
                            # State name, how many hail, min mag, max
                            # mag, mean mag, median mag, mode mag, and FIPs.
                            csvFile.write(str(key) + "," + str(counter) +
                                "," + str(min(magList_State)) + "," +
                                str(max(magList_State)) + "," +
                                str("{0:.2f}".format(
                                numpy.mean(magList_State)) + "," +
                                str("{0:.2f}".format(
                                numpy.median(magList_State))) + "," +
                                modeString_State + "," +
                                str(dictKeys_OrderedDict_StateNames[key]) +
                                ",\n"))

                    # Close the data counts CSV file.
                    csvFile.close()

                # If the user selects State clipping option...
                if self.radioButton_Selection == 2:

                    # Import the tuples and dictionaries affiliated with states
                    # and counties.
                    import GUI_CountiesPerState

                    # Execute function to obtain total hail count within
                    # the US.
                    self.func_CSV_DataCount_Nationwide_Count()

                    # Perform spatial join of clipped hail feature class
                    # and State polygon feature class. Store output in_memory.
                    arcpy.SpatialJoin_analysis(self.clipped_Output_FeatureClass,
                                        self.featureClass_State_Selection_Only,
                                        "in_memory/SpatialJoin")

                    # Create/Open a new CSV file within the CSV subfolder for
                    # data counts to be written into.
                    csvFile = open(self.csvDirectory + "DataCounts_" +
                                   self.nameFeatureClass_FromCSV +
                                   self.folderNamingAddition + fileExtCSV, "w")

                    # If timespan and diameter drop-downs don't show Custom...
                    if self.stringHailTimespan.get() != "Custom..." and \
                            self.stringHailDiameter.get() != "Custom...":

                        # Write the following lines into the data counts CSV.
                        csvFile.write("Timespan:," +
                                self.stringHailTimespan.get() + ",\n")
                        csvFile.write("Diameter Range (Inches):," +
                                self.stringHailDiameter.get() + ",\n")

                    # If timespan drop-down shows Custom and diameter drop-down
                    # doesn't show Custom...
                    if self.stringHailTimespan.get() == "Custom..." and \
                            self.stringHailDiameter.get() != "Custom...":

                        # Write the following lines into the data counts CSV.
                        csvFile.write("Timespan:," + self.textCustomYearFrom +
                                      self.textCustomMonthFrom.zfill(2) +
                                      "-" + self.textCustomYearTo +
                                      self.textCustomMonthTo.zfill(2) + ",\n")
                        csvFile.write("Diameter Range (Inches):," +
                                self.stringHailDiameter.get() + ",\n")

                    # If timespan drop-down shows Custom and diameter drop-down
                    # shows Custom...
                    if self.stringHailTimespan.get() == "Custom..." and \
                            self.stringHailDiameter.get() == "Custom...":

                        # Write the following lines into the data counts CSV.
                        csvFile.write("Timespan:," + self.textCustomYearFrom +
                                      self.textCustomMonthFrom.zfill(2) +
                                      "-" + self.textCustomYearTo +
                                      self.textCustomMonthTo.zfill(2) + ",\n")
                        csvFile.write("Diameter Range (Inches):," +
                                      self.textCustomDiameterFrom + "-" +
                                      self.textCustomDiameterTo + ",\n")

                    # If timespan drop-down doesn't show Custom and diameter
                    # drop-down shows Custom...
                    if self.stringHailTimespan.get() != "Custom..." and \
                            self.stringHailDiameter.get() == "Custom...":

                        # Write the following lines into the data counts CSV.
                        csvFile.write("Timespan:," +
                                    self.stringHailTimespan.get() + ",\n")
                        csvFile.write("Diameter Range (Inches):," +
                                      self.textCustomDiameterFrom + "-" +
                                      self.textCustomDiameterTo + ",\n")

                    # Now write the following lines, regardless of
                    # timespan/diameter selection.
                    csvFile.write("\n")
                    csvFile.write("USA (and DC) Hail:," +
                                  str(self.usa_hail_count) + ",\n")
                    csvFile.write("\n")
                    csvFile.write("State Hail - " +
                                  str(self.stringState_Name.get()) +
                                  " (FIPS: " +
                                  str(dictKeys_OrderedDict_StateNames[
                                          self.stringState_Name.get()]) +
                                  "):," + str(self.clipped_hailCount) +
                                  ",\n")
                    csvFile.write("\n")
                    csvFile.write("Statewide Hail Data,\n")
                    csvFile.write("V,V,V,V,V,\n")
                    csvFile.write("Minimum Diameter,Maximum Diameter,"
                                  "Mean Diameter,Median Diameter,"
                                  "Mode Diameter,\n")

                    # Create empty list to store all state diameter values.
                    magList_State = []

                    # Open the in_memory spatial join as a Search Cursor,
                    # with analysis fields set to FIPS code and diameter.
                    with arcpy.da.SearchCursor("in_memory/SpatialJoin",
                                            [census_Shapefile_Field_CountyName,
                                                analysis_Mag_Field]) as cursor:

                        # For each feature within the spatial join...
                        for row in cursor:

                            # Add the diameter to the state list.
                            magList_State.append(row[1])

                    try:

                        # Calculate mode of all diameters within state list.
                        modeValue_State = mode(magList_State)

                        # Convert mode information to float and then to
                        # string with two decimal places.
                        modeString_State = \
                            str("{0:.2f}".format(float(modeValue_State)))

                    except StatisticsError:

                        # This catches any lists containing no mode.
                        # This will occur if all values within list are
                        # unique values.

                        # Assign mode to the following phrase.
                        modeString_State = "No Unique Mode"

                        pass

                    # Write the following data to the data counts CSV.
                    # Min diameter, max diameter, mean diameter,
                    # median diameter, and mode diameter.
                    csvFile.write(str(min(magList_State)) + "," +
                            str(max(magList_State)) + "," +
                            str("{0:.2f}".format(numpy.mean(magList_State)) +
                            "," +
                            str("{0:.2f}".format(numpy.median(magList_State))) +
                            "," + modeString_State + "," + ",\n"))

                    csvFile.write("\n")
                    csvFile.write("Hail Data per County\n")
                    csvFile.write("V,V,V,V,V,V,V,\n")
                    csvFile.write("Counties with Hail,Hail Count,"
                                  "Minimum Diameter,Maximum Diameter,"
                                  "Mean Diameter,Median Diameter,"
                                  "Mode Diameter,\n")

                    # Create empty list for storing hail/diameter values.
                    magList_County = []

                    # For each county list within state/county dictionary
                    # matching the state drop-down selection...
                    for key in GUI_CountiesPerState.dict_state_counties[
                        self.stringState_Name.get()]:

                        # Set counter to zero, for counting hail within
                        # each state during loop.
                        counter = 0

                        # Clears magList after each state count has concluded.
                        magList_County.clear()

                        # Open the in_memory spatial join as a Search Cursor,
                        # with analysis fields set to county name and diameter.
                        with arcpy.da.SearchCursor("in_memory/SpatialJoin",
                                            [census_Shapefile_Field_CountyName,
                                                analysis_Mag_Field]) as cursor:

                            # For each feature within the spatial join...
                            for row in cursor:

                                # If the county name matches a county name
                                # within the state/county dictionary....
                                if row[0] == key:

                                    # Append row information to magList_County.
                                    magList_County.append(row[1])

                                    # Increment counter by one.
                                    counter = counter + 1

                        # If row counter is greater than zero...
                        if counter > 0:

                            try:

                                # Calculate mode of all diameters within list.
                                modeValue_County = mode(magList_County)

                                # Convert mode information to float and then to
                                # string with two decimal places.
                                modeString_County = \
                                    str("{0:.2f}".format(
                                        float(modeValue_County)))

                            except StatisticsError:

                                # This catches any lists containing no mode.
                                # This will occur if all values within list are
                                # unique values.

                                # Assign modeString to the following phrase.
                                modeString_County = "No Unique Mode"

                                pass

                            # Write the following data to the data counts CSV.
                            # County name, how many hail, min diameter, max
                            # mag, mean diameter, median diameter, and mode
                            # diameter.
                            csvFile.write(str(key) + "," + str(counter) + "," +
                                          str("{0:.2f}".format(
                                              min(magList_County))) + "," +
                                          str("{0:.2f}".format(
                                            max(magList_County))) + "," +
                                          str("{0:.2f}".format(
                                            numpy.mean(magList_County))) + "," +
                                          str("{0:.2f}".format(
                                            numpy.median(magList_County))) +
                                          "," + modeString_County + ",\n")

                    # Close the data counts CSV file.
                    csvFile.close()

                # If the user selects County clipping option...
                if self.radioButton_Selection == 3:

                    # Import the tuples and dictionaries affiliated with states
                    # and counties.
                    import GUI_CountiesPerState

                    # Execute function to obtain total hail count within
                    # the US.
                    self.func_CSV_DataCount_Nationwide_Count()

                    # Execute function to obtain total hail count within
                    # the state.
                    self.func_CSV_DataCount_Statewide_Count()

                    # Create/Open a new CSV file within the CSV subfolder for
                    # data counts to be written into.
                    csvFile = open(self.csvDirectory + "DataCounts_" +
                                   self.nameFeatureClass_FromCSV +
                                   self.folderNamingAddition + fileExtCSV, "w")

                    # If timespan and diameter drop-downs don't show Custom...
                    if self.stringHailTimespan.get() != "Custom..." and \
                            self.stringHailDiameter.get() != "Custom...":

                        # Write the following lines into the data counts CSV.
                        csvFile.write("Timespan:," +
                                    self.stringHailTimespan.get() + ",\n")
                        csvFile.write("Diameter Range (Inches):," +
                                self.stringHailDiameter.get() + ",\n")

                    # If timespan drop-down shows Custom and diameter drop-down
                    # doesn't show Custom...
                    if self.stringHailTimespan.get() == "Custom..." and \
                            self.stringHailDiameter.get() != "Custom...":

                        # Write the following lines into the data counts CSV.
                        csvFile.write("Timespan," + self.textCustomYearFrom +
                                      self.textCustomMonthFrom.zfill(2) +
                                      "-" + self.textCustomYearTo +
                                      self.textCustomMonthTo.zfill(2) + ",\n")
                        csvFile.write("Diameter Range (Inches):," +
                                self.stringHailDiameter.get() + ",\n")

                    # timespan drop-down shows Custom and diameter drop-down
                    # shows Custom...
                    if self.stringHailTimespan.get() == "Custom..." and \
                            self.stringHailDiameter.get() == "Custom...":

                        # Write the following lines into the data counts CSV.
                        csvFile.write("Timespan:," + self.textCustomYearFrom +
                                      self.textCustomMonthFrom.zfill(2) +
                                      "-" + self.textCustomYearTo +
                                      self.textCustomMonthTo.zfill(2) + ",\n")
                        csvFile.write("Diameter Range (Inches):," +
                                      self.textCustomDiameterFrom + "-" +
                                      self.textCustomDiameterTo + ",\n")

                    # If timespan drop-down doesn't show Custom and diameter
                    # drop-down shows Custom...
                    if self.stringHailTimespan.get() != "Custom..." and \
                            self.stringHailDiameter.get() == "Custom...":

                        # Write the following lines into the data counts CSV.
                        csvFile.write("Timespan:," +
                                    self.stringHailTimespan.get() + ",\n")
                        csvFile.write("Diameter Range (Inches):," +
                                      self.textCustomDiameterFrom + "-" +
                                      self.textCustomDiameterTo + ",\n")

                    # Now write the following lines, regardless of
                    # timespan/diameter selection.
                    csvFile.write("\n")
                    csvFile.write("USA (and DC) Hail:," +
                                  str(self.usa_hail_count) + ",\n")
                    csvFile.write("State Hail - " +
                        str(self.stringState_Name.get()) + " (FIPS: " +
                        str(dictKeys_OrderedDict_StateNames[
                                self.stringState_Name.get()]) + "):," +
                                  str(self.state_hail_count) + ",\n")
                    csvFile.write("\n")
                    csvFile.write("County Hail - " +
                                  self.stringCounty_Name.get() + ":," +
                                  str(self.clipped_hailCount) + ",\n")
                    csvFile.write("\n")
                    csvFile.write("County Hail Data\n")
                    csvFile.write("V,V,V,V,V,\n")
                    csvFile.write("Minimum Diameter,Maximum Diameter,"
                                  "Mean Diameter,Median Diameter,"
                                  "Mode Diameter,\n")

                    # Create empty list for storing hail/diameter values.
                    magList = []

                    # Perform spatial join of clipped hail feature class
                    # and County polygon feature class. Store output in_memory.
                    arcpy.SpatialJoin_analysis(self.clipped_Output_FeatureClass,
                                        self.featureClass_County_State_Naming,
                                               "in_memory/SpatialJoin")

                    # For each county list within state/county dictionary
                    # matching the state drop-down selection...
                    for key in GUI_CountiesPerState.dict_state_counties[
                                                self.stringState_Name.get()]:

                        # Set counter to zero, for counting hail within
                        # each county during loop.
                        counter = 0

                        # Clears magList after each county count has concluded.
                        magList.clear()

                        # Open the in_memory spatial join as a Search Cursor,
                        # with analysis fields set to county name and diameter.
                        with arcpy.da.SearchCursor("in_memory/SpatialJoin",
                                        [census_Shapefile_Field_CountyName,
                                        analysis_Mag_Field]) as cursor:

                            # For each feature within the spatial join...
                            for row in cursor:

                                # If the county name matches a county name
                                # within the state/county dictionary...
                                if row[0] == key:

                                    # Append row information to magList.
                                    magList.append(row[1])

                                    # Increment counter by one.
                                    counter = counter + 1

                        # If row counter is greater than zero...
                        if counter > 0:

                            try:

                                # Calculate mode of all diameters within list.
                                modeValue = mode(magList)

                                # Convert mode information to float and then to
                                # string with two decimal places.
                                modeString = \
                                    str("{0:.2f}".format(float(modeValue)))

                            except StatisticsError:

                                # This catches any lists containing no mode.
                                # This will occur if all values within list are
                                # unique.

                                #Assign modeString to the following phrase.
                                modeString = "No Unique Mode"

                                pass

                            # Write the following data to the data counts CSV.
                            # Min mag, max mag, mean mag, median mag, and
                            # mode mag.
                            csvFile.write(str("{0:.2f}".format(min(magList))) +
                                "," + str("{0:.2f}".format(max(magList))) +
                                "," +
                                str("{0:.2f}".format(numpy.mean(magList))) +
                                "," +
                                str("{0:.2f}".format(numpy.median(magList))) +
                                "," + modeString + ",\n")

                    # Close the data counts CSV file.
                    csvFile.close()

                # Clear any intermediate output from memory.
                self.func_Clear_InMemory()

                self.func_Scroll_setOutputText("Count results successfully "
                                               "written to CSV file.", None)

                # Increase current progress bar percentage by three percent.
                self.analysis_Percentage_Counter = \
                    self.analysis_Percentage_Counter + 3

                # Increment progress bar by adjusted value.
                self.func_ProgressBar_setProgress(
                    self.analysis_Percentage_Counter)

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
            self.func_Scroll_setOutputText(str(e) + "\n" + 
                                           traceback.format_exc(), color_Red)

        try:

            # If the user selects the IDW analysis...
            if self.statusAnalysis_IDW.get() == 1:

                # Set the workspace for the following analysis.
                arcpy.env.workspace = self.subFolder_GIS + "/" + nameFileGDB

                # Set the extent to the input argument feature class mask.
                arcpy.env.extent = featureClass_Mask

                self.func_Scroll_setOutputText("Performing IDW Analysis on all "
                                    "points, then clipping/masking output to " +
                                    featureClass_Mask + " extent...", None)

                # Point Density parameters, with optional parameters set to None
                # for Esri defaults.
                required_InputFile = self.clipped_Output_FeatureClass
                required_ZField = analysis_Mag_Field
                optional_CellSize = None
                optional_Power = None
                optional_SearchRadius = None

                # Perform the IDW analysis.
                output_IDW = arcpy.sa.Idw(required_InputFile, required_ZField,
                                            optional_CellSize, optional_Power,
                                            optional_SearchRadius)

                # Get geoprocessing messages.
                self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

                # Pause script for one second.
                sleep(1)

                self.func_Scroll_setOutputText("Masking IDW results...", None)

                # Mask the IDW results.
                output_IDW_with_Mask = arcpy.sa.ExtractByMask(
                    output_IDW, featureClass_Mask)

                # Save the masked IDW feature class results to File GDB.
                output_IDW_with_Mask.save(
                    "idw_" + self.clipped_Output_FeatureClass)

                # Get geoprocessing messages.
                self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

                self.func_Scroll_setOutputText("IDW Analysis completed.", None)

                # Increase current progress bar percentage by three percent.
                self.analysis_Percentage_Counter = \
                    self. analysis_Percentage_Counter + 3

                # Increment progress bar by adjusted value.
                self.func_ProgressBar_setProgress(
                    self.analysis_Percentage_Counter)

                # Pause script by one second.
                sleep(1)

        except arcpy.ExecuteError:

            # Display geoprocessing errors and skip the failed analysis.
            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Red)

            pass

        except Exception as e:

            # Display error messages for all other errors and skip failed
            # analysis.
            self.func_Scroll_setOutputText(str(e) + "\n" + 
                                           traceback.format_exc(), color_Red)

            pass

        try:

            # If the user selects the Kernel Density analysis...
            if self.statusAnalysis_KernelDensity.get() == 1:

                # Set the workspace for the following analysis.
                arcpy.env.workspace = self.subFolder_GIS + "/" + nameFileGDB

                # Set the extent to the input argument feature class mask.
                arcpy.env.extent = featureClass_Mask

                self.func_Scroll_setOutputText("Performing Kernel Density "
                    "Analysis on all points, then clipping/masking output to " +
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

                # Increase current progress bar percentage by three percent.
                self.analysis_Percentage_Counter = \
                    self.analysis_Percentage_Counter + 3

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
            self.func_Scroll_setOutputText(str(e) + "\n" + 
                                           traceback.format_exc(), color_Red)

            pass

        try:

            # If the user selects the Kriging analysis...
            if self.statusAnalysis_Kriging.get() == 1:

                # Set the workspace for the following analysis.
                arcpy.env.workspace = self.subFolder_GIS + "/" + nameFileGDB

                # Set the extent to the input argument feature class mask.
                arcpy.env.extent = featureClass_Mask

                self.func_Scroll_setOutputText("Performing Kriging Analysis on "
                                "all points, then clipping/masking output to " +
                                featureClass_Mask + " extent...", None)

                # Kriging parameters, with optional parameters set to None
                # for Esri defaults.
                required_InputFile = self.clipped_Output_FeatureClass
                required_ZField = analysis_Mag_Field
                optional_KrigingModel = None
                optional_CellSize = None
                optional_SearchRadius = None
                optional_OutputVariancePredictionRaster = None

                # Perform the Kriging analysis.
                output_Kriging = arcpy.sa.Kriging(required_InputFile,
                                    required_ZField, optional_KrigingModel,
                                    optional_CellSize, optional_SearchRadius,
                                    optional_OutputVariancePredictionRaster)

                # Get geoprocessing messages.
                self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

                # Pause script for one second.
                sleep(1)

                # Mask the Kriging results.
                output_Kriging_with_Mask = arcpy.sa.ExtractByMask(
                    output_Kriging, featureClass_Mask)

                self.func_Scroll_setOutputText("Masking Kriging results...",
                                               None)

                # Save the masked Kriging results to File GDB.
                output_Kriging_with_Mask.save(
                    "kriging_" + self.clipped_Output_FeatureClass)

                # Get geoprocessing messages.
                self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

                self.func_Scroll_setOutputText("Kriging Analysis completed.",
                                               None)

                # Increase current progress bar percentage by three percent.
                self.analysis_Percentage_Counter = \
                    self.analysis_Percentage_Counter + 3

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
            self.func_Scroll_setOutputText(str(e) + "\n" + 
                                           traceback.format_exc(), color_Red)

            pass

        try:

            # If the user selects the Natural Neighbor analysis...
            if self.statusAnalysis_NaturalNeighbor.get() == 1:

                # Set the workspace for the following analysis.
                arcpy.env.workspace = self.subFolder_GIS + "/" + nameFileGDB

                # Set the extent to the input argument feature class mask.
                arcpy.env.extent = featureClass_Mask

                # If the total number of hail features reach 14,750,000...
                if self.raw_hail_count >= 14750000:

                    # Display this message, as the geoprocessing tool will fail
                    # if the total number approaches 15 million records (Esri).
                    self.func_Scroll_setOutputText(
                        "UNABLE TO EXECUTE NATURAL NEIGHBOR ANALYSIS:\n" +
                        "According to Esri, this analysis will fail if the "
                        "input hail count nears 15,000,000.\n" +
                        "Skipping this analysis...", color_Red)

                else:
                    # Else, perform the analysis.
                    self.func_Scroll_setOutputText("Performing Natural "
                                        "Neighbor Analysis on all points, "
                                        "then clipping/masking output to " +
                                        featureClass_Mask + " extent...", None)

                    # Natural Neighbor parameters, with optional parameters set
                    # to None for Esri defaults.
                    required_InputFile = self.clipped_Output_FeatureClass
                    required_ZField = analysis_Mag_Field
                    optional_CellSize = None

                    # Perform the Natural Neighbor analysis.
                    output_NaturalNeighbor = arcpy.sa.NaturalNeighbor(
                        required_InputFile, required_ZField, optional_CellSize)

                    # Get geoprocessing messages.
                    self.func_Scroll_setOutputText(arcpy.GetMessages(0),
                                                   color_Blue)

                    # Pause script for one second.
                    sleep(1)

                    # Mask the Natural Neighbor results.
                    output_NaturalNeighbor_with_Mask = arcpy.sa.ExtractByMask(
                        output_NaturalNeighbor, featureClass_Mask)

                    self.func_Scroll_setOutputText(
                        "Masking Natural Neighbor results...", None)

                    # Save masked results to the File GDB.
                    output_NaturalNeighbor_with_Mask.save(
                        "naturalneighbor_" + self.clipped_Output_FeatureClass)

                    # Get geoprocessing messages.
                    self.func_Scroll_setOutputText(arcpy.GetMessages(0),
                                                   color_Blue)

                    self.func_Scroll_setOutputText(
                        "Natural Neighbor Analysis completed.", None)

                # Increase current progress bar percentage by three percent.
                self.analysis_Percentage_Counter = \
                    self.analysis_Percentage_Counter + 3

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
            self.func_Scroll_setOutputText(str(e) + "\n" + 
                                           traceback.format_exc(), color_Red)

            pass

        try:

            # If the user selects the Optimized Hot Spot analysis...
            if self.statusAnalysis_OptHotSpot.get() == 1:

                # Set the workspace for the following analysis.
                arcpy.env.workspace = self.subFolder_GIS + "/" + nameFileGDB

                # Set the extent to the input argument feature class mask.
                arcpy.env.extent = featureClass_Mask

                # Static Optimized Hot Spot Analysis parameters, with optional
                # parameters set to None for Esri defaults.
                required_InputFile = self.clipped_Output_FeatureClass
                optional_IncidentDataAggregationMethod = None
                optional_BoundingPolygons = None
                optional_PolygonsForAggregatingIncidents = None
                optional_DensitySurface = None

                # If the clipped hail count is less than 30 features...
                if self.clipped_hailCount < 30:

                    # Display the following message and skip, as a minimum of
                    # 30 samples is required (per Esri) when the analysis field
                    # option is set with a value.
                    self.func_Scroll_setOutputText(
                        "UNABLE TO EXECUTE OPTIMIZED HOT SPOT ANALYSIS (WITH"
                        " ANALYSIS FIELD OPTION):\n" +
                        "According to Esri, this analysis requires a minimum of"
                        " 30 hail within the sampling area.\n" +
                        "Skipping this analysis...", color_Red)

                else:

                    # Else, perform the analysis.
                    self.func_Scroll_setOutputText(
                        "Performing Optimized Hot Spot Analysis on all points "
                        "(analysis field = 'mag'), with output clipped to " +
                        featureClass_Mask + " extent...", None)

                    # Output file name with Analysis Field option.
                    # A temporary workspace is assigned for intermediate output.
                    required_InputFile = self.clipped_Output_FeatureClass
                    required_OutputFile_WithMagField = "in_memory/tempInput_Mag"

                    # Analysis Field option reset to analysis_Mag_Field.
                    optional_AnalysisField = analysis_Mag_Field

                    # Please note: Some sort of "bug" occurs when the Optimized
                    # Hot Spot Analysis is conducted here with an Analysis Field
                    # utilized. A feature class lock will persist on the input
                    # file, even when the geoprocessing script has concluded.
                    # This will not occur when the Analysis Field option is left
                    # blank, however. The lock was causing issues with later
                    # tasks within the script. Numerous attempts were made to
                    # find the root cause of the issue, but the solution
                    # presented is discussed farther down within this function
                    # block.
                    arcpy.OptimizedHotSpotAnalysis_stats(required_InputFile,
                                required_OutputFile_WithMagField,
                                optional_AnalysisField,
                                optional_IncidentDataAggregationMethod,
                                optional_BoundingPolygons,
                                optional_PolygonsForAggregatingIncidents,
                                optional_DensitySurface)

                    # Display geoprocessing output messages.
                    self.func_Scroll_setOutputText(arcpy.GetMessages(0),
                                                   color_Blue)

                    self.func_Scroll_setOutputText("Optimized Hot Spot Analysis"
                                    " on all points (analysis field = '" +
                                    analysis_Mag_Field + "') completed.", None)

                    self.func_Scroll_setOutputText("Clipping Optimized Hot Spot"
                                    " Analysis (analysis field = '" +
                                    analysis_Mag_Field + "') results...", None)

                    # The intermediate output feature class is clipped to the
                    # predetermined feature class mask and saved as a new
                    # feature class.
                    arcpy.Clip_analysis(required_OutputFile_WithMagField,
                                        featureClass_Mask,
                                        "opthotspot_" + analysis_Mag_Field +
                                        "AnalysisField_" + \
                                        self.clipped_Output_FeatureClass)

                    # Get geoprocessing messages.
                    self.func_Scroll_setOutputText(arcpy.GetMessages(0),
                                                   color_Blue)

                    self.func_Scroll_setOutputText("Clipping for Optimized Hot "
                                "Spot Analysis (analysis field = '" +
                                analysis_Mag_Field + "') completed.", None)

                    # Pause script for one second.
                    sleep(1)

                # Begin the second iteration of the same analysis WITHOUT an
                # analysis field set as an input parameter.

                # If the clipped hail count is less than 60 features...
                if self.clipped_hailCount < 60:

                    # Display the following message and skip, as a minimum of
                    # 60 samples is required (per Esri) when the analysis field
                    # option is not used.
                    self.func_Scroll_setOutputText(
                        "UNABLE TO EXECUTE OPTIMIZED HOT SPOT ANALYSIS (WITHOUT"
                        " ANALYSIS FIELD OPTION):\n" +
                        "According to Esri, this analysis requires a minimum of"
                        " 60 hail within the sampling area.\n" +
                        "Skipping this analysis...", color_Red)

                else:

                    # As previously discussed, the Analysis Field option was
                    # causing a feature class lock on the input feature class.
                    # The most suitable way to fix this issue was to re-run
                    # the Optimized Hot Spot Analysis tool WITHOUT an Analysis
                    # Field option set. The following geoprocessing tool causes
                    # the lock to disappear from the feature class, which allows
                    # the rest of the script to function properly. As a result,
                    # the user will have two outputs for the Optimized Hot Spot
                    # Analysis.
                    self.func_Scroll_setOutputText("Performing Optimized Hot "
                            "Spot Analysis on all points (no analysis field), "
                            "with output clipped to " + featureClass_Mask +
                            " extent...", None)

                    # Changed output file name without Analysis Field option.
                    # A temporary workspace is assigned for intermediate output.
                    required_OutputFile_WithoutMagField = \
                        "in_memory/tempInput_noMag"

                    # Analysis Field option reset to None.
                    optional_AnalysisField = None

                    # ArcPy runs the amended Optimized Hot Spot Analysis
                    arcpy.OptimizedHotSpotAnalysis_stats(required_InputFile,
                                    required_OutputFile_WithoutMagField,
                                    optional_AnalysisField,
                                    optional_IncidentDataAggregationMethod,
                                    optional_BoundingPolygons,
                                    optional_PolygonsForAggregatingIncidents,
                                    optional_DensitySurface)

                    # Display geoprocessing output messages.
                    self.func_Scroll_setOutputText(
                        arcpy.GetMessages(0), color_Blue)

                    self.func_Scroll_setOutputText("Optimized Hot Spot Analysis"
                        " on all points (no analysis field) completed.", None)

                    self.func_Scroll_setOutputText("Clipping Optimized Hot Spot"
                            " Analysis (no analysis field) results...", None)

                    # The intermediate output feature class is clipped to the
                    # predetermined feature class mask and saved as a new
                    # feature class.
                    arcpy.Clip_analysis(required_OutputFile_WithoutMagField,
                                        featureClass_Mask,
                                            "opthotspot_noAnalysisField_" + \
                                            self.clipped_Output_FeatureClass)

                    # Get geoprocessing messages.
                    self.func_Scroll_setOutputText(
                        arcpy.GetMessages(0), color_Blue)

                    self.func_Scroll_setOutputText("Clipping for Optimized Hot "
                        "Spot Analysis (no analysis field) completed.", None)

                # Clear any intermediate output from memory.
                self.func_Clear_InMemory()

                # Increase current progress bar percentage by three percent.
                self.analysis_Percentage_Counter = \
                    self.analysis_Percentage_Counter + 3

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
            self.func_Scroll_setOutputText(str(e) + "\n" + 
                                           traceback.format_exc(), color_Red)

            # Clear any intermediate output from memory.
            self.func_Clear_InMemory()

            pass

        try:

            # If the user selects the Point Density analysis...
            if self.statusAnalysis_PointDensity.get() == 1:

                # Set the workspace for the following analysis.
                arcpy.env.workspace = self.subFolder_GIS + "/" + nameFileGDB

                # Set the extent to the input argument feature class mask.
                arcpy.env.extent = featureClass_Mask

                self.func_Scroll_setOutputText("Performing Point Density "
                                "Analysis on all points, then clipping/masking "
                                "output to " + featureClass_Mask + " extent...",
                                None)

                # Point Density parameters, with optional parameters set to None
                # for Esri defaults.
                required_InputFile = self.clipped_Output_FeatureClass
                optional_PopField = None
                optional_CellSize = None
                optional_NeighborhoodType = None
                optional_AreaUnitScalFactor = None

                # Execute Point Density analysis with default Esri values.
                output_PointDensity = arcpy.sa.PointDensity(required_InputFile,
                                        optional_PopField, optional_CellSize,
                                        optional_NeighborhoodType,
                                        optional_AreaUnitScalFactor)

                # Get geoprocessing messages.
                self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

                # Pause script for one second.
                sleep(1)

                # Mask the Point Density results.
                output_PointDensity_with_Mask = \
                    arcpy.sa.ExtractByMask(output_PointDensity,
                                           featureClass_Mask)

                self.func_Scroll_setOutputText(
                    "Masking Point Density results...", None)

                # Save the masked results to the File GDB.
                output_PointDensity_with_Mask.save("pointdensity_" +
                                            self.clipped_Output_FeatureClass)

                # Get geoprocessing messages.
                self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

                self.func_Scroll_setOutputText(
                    "Point Density Analysis completed.", None)

                # Increase current progress bar percentage by three percent.
                self.analysis_Percentage_Counter = \
                    self.analysis_Percentage_Counter + 3

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
            self.func_Scroll_setOutputText(str(e) + "\n" + 
                                           traceback.format_exc(), color_Red)

            pass

        try:

            # If the user selects the Spline analysis...
            if self.statusAnalysis_Spline.get() == 1:

                # Set the workspace for the following analysis.
                arcpy.env.workspace = self.subFolder_GIS + "/" + nameFileGDB

                # Set the extent to the input argument feature class mask.
                arcpy.env.extent = featureClass_Mask

                self.func_Scroll_setOutputText("Performing Spline Analysis on "
                                "all points, then clipping/masking output to " +
                                featureClass_Mask + " extent...", None)

                # Spline parameters, with optional parameters set to None
                # for Esri defaults.
                required_InputFile = self.clipped_Output_FeatureClass
                required_ZField = analysis_Mag_Field
                optional_CellSize = None
                optional_SplineType = None
                optional_Weight = None
                optional_PointNumber = None

                # Execute Spline Analysis with default Esri values.
                output_Spline = arcpy.sa.Spline(required_InputFile,
                                required_ZField, optional_CellSize,
                                optional_SplineType, optional_Weight,
                                optional_PointNumber)

                # Get geoprocessing messages.
                self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

                # Pause script for one second.
                sleep(1)

                # Mask the Spline results.
                output_Spline_with_Mask = arcpy.sa.ExtractByMask(output_Spline,
                                                          featureClass_Mask)

                self.func_Scroll_setOutputText("Masking Spline results...",
                                               None)

                # Save the masked results to File GDB.
                output_Spline_with_Mask.save("spline_" +
                                             self.clipped_Output_FeatureClass)

                # Get geoprocessing messages.
                self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

                self.func_Scroll_setOutputText("Spline Analysis completed.",
                                               None)

                # Increase current progress bar percentage by three percent.
                self.analysis_Percentage_Counter = \
                    self.analysis_Percentage_Counter + 3

                # Increment progress bar by adjusted value.
                self.func_ProgressBar_setProgress(
                    self.analysis_Percentage_Counter)

                # Clear any intermediate output from memory.
                self.func_Clear_InMemory()

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
            self.func_Scroll_setOutputText(str(e) + "\n" + 
                                           traceback.format_exc(), color_Red)

            # Clear any intermediate output from memory.
            self.func_Clear_InMemory()

            pass

        try:

            # If the user selects the Thiessen analysis...
            if self.statusAnalysis_Thiessen.get() == 1:

                # Set the workspace for the following analysis.
                arcpy.env.workspace = self.subFolder_GIS + "/" + nameFileGDB

                # Set the extent to the input argument feature class mask.
                arcpy.env.extent = featureClass_Mask

                self.func_Scroll_setOutputText("Performing Thiessen Polygon "
                            "Analysis on all points, with output clipped to " +
                            featureClass_Mask + " extent...", None)

                # Thiessen parameters, with optional parameters set to None
                # for Esri defaults.
                required_InputFile = self.clipped_Output_FeatureClass
                required_OutputFile = "in_memory/Thiessen"

                # This is not the Esri default. Parameter set to ALL so all
                # fields would be included with output (for visual reference).
                optional_OutputFields = "ALL"

                # Perform the Thiessen Polygon analysis.
                arcpy.CreateThiessenPolygons_analysis(required_InputFile,
                                    required_OutputFile, optional_OutputFields)

                # Get geoprocessing messages.
                self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

                # Pause script for one second.
                sleep(1)

                self.func_Scroll_setOutputText(
                    "Clipping Thiessen Polygon Analysis results...", None)

                # Perform a clip of the Thiessen polygon output and save to the
                # File GDB.
                arcpy.Clip_analysis(required_OutputFile, featureClass_Mask,
                                "thiessen_" + self.clipped_Output_FeatureClass)

                # Get geoprocessing messages.
                self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

                self.func_Scroll_setOutputText(
                    "Thiessen Polygon Analysis completed.", None)

                # Clear any intermediate output from memory.
                self.func_Clear_InMemory()

                # Increase current progress bar percentage by three percent.
                self.analysis_Percentage_Counter = \
                    self.analysis_Percentage_Counter + 3

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
            self.func_Scroll_setOutputText(str(e) + "\n" + 
                                           traceback.format_exc(), color_Red)

            # Clear any intermediate output from memory.
            self.func_Clear_InMemory()

            pass

        try:

            # If the user selects the Trend analysis...
            if self.statusAnalysis_Trend.get() ==1:

                # Set the workspace for the following analysis.
                arcpy.env.workspace = self.subFolder_GIS + "/" + nameFileGDB

                # Set the extent to the input argument feature class mask.
                arcpy.env.extent = featureClass_Mask

                self.func_Scroll_setOutputText("Performing Trend Analysis on "
                            "all points, then clipping/masking output to " +
                            featureClass_Mask + " extent...", None)

                # Trend parameters, with optional parameters set to None
                # for Esri defaults.
                required_InputFile = self.clipped_Output_FeatureClass
                required_ZField = analysis_Mag_Field
                optional_CellSize = None
                optional_Order = None
                optional_RegressionType = None
                optional_OutputRMSFile = None

                # Execute Trend Analysis with default Esri values
                output_Trend = arcpy.sa.Trend(required_InputFile,
                            required_ZField, optional_CellSize, optional_Order,
                            optional_RegressionType, optional_OutputRMSFile)

                # Get geoprocessing messages.
                self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

                # Pause script for one second.
                sleep(1)

                # Mask the Trend results.
                output_Trend_with_Mask = arcpy.sa.ExtractByMask(output_Trend,
                                                            featureClass_Mask)

                self.func_Scroll_setOutputText("Masking Trend results...", None)

                # Save the masked results to the File GDB.
                output_Trend_with_Mask.save("trend_" +
                                            self.clipped_Output_FeatureClass)

                # Get geoprocessing messages.
                self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Blue)

                self.func_Scroll_setOutputText("Trend Analysis completed.",
                                               None)

                # Increase current progress bar percentage by three percent.
                self.analysis_Percentage_Counter = \
                    self.analysis_Percentage_Counter + 3

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
            self.func_Scroll_setOutputText(str(e) + "\n" + 
                                           traceback.format_exc(), color_Red)

            pass

    def func_CSV_DataCount_Nationwide_Count(self):

        # This function controls the counting of all hail within the US.
        # Used only if state or county clipping option is selected. It will be
        # used within the output data counts CSV file.

        try:

            # Set workspace to File GDB for the following analysis.
            arcpy.env.workspace = self.subFolder_GIS + "/" + nameFileGDB

            # Assign Census Shapefile within Shapefile subfolder to variable.
            censusShapefile = self.subFolder_CensusShapefile + "/" + \
                              census_URL_CountyShapefile_FileName + fileExtShp

            # Create Census polygon feature class variable stored within memory.
            memoryFeatureClass_US = "in_memory/" + \
                                    featureClass_50States_and_DC_only

            # Copy Census Shapefile to feature class stored in memory.
            arcpy.CopyFeatures_management(censusShapefile,
                                          memoryFeatureClass_US)

            # Pause script for one second.
            sleep(1)

            # Open the Census in_memory feature class with an Update Cursor.
            with arcpy.da.UpdateCursor(memoryFeatureClass_US,
                                    census_Shapefile_Field_StateFIPS) as cursor:

                # For each feature in the Census in_memory feature class...
                for row in cursor:

                    # This If statement removes non-50 state (and DC) FIPS codes
                    # from the Census feature class. The original polygons
                    # include all US territories.
                    if row[0] == "60" or row[0] == "66" or row[0] == "69" or \
                                    row[0] == "72" or row[0] == "78":

                        # Delete feature from in_memory feature class.
                        cursor.deleteRow()

            # Recalculate the extent of the in_memory feature class.
            arcpy.RecalculateFeatureClassExtent_management(
                memoryFeatureClass_US)

            # Create new feature class variable in_memory for clipped hail
            # points.
            clipped_Output_FeatureClass = "in_memory/ClippedOutputFC_US"

            # Perform a clip of raw hail points to the 50 US states and DC
            # polygons and store within the clipped feature class in_memory.
            arcpy.Clip_analysis(self.nameFeatureClass_FromCSV,
                                memoryFeatureClass_US,
                                clipped_Output_FeatureClass)

            # Perform a count on the clipped hail features found within
            # the in_memory clipped feature class.
            hailCountResult_US = arcpy.GetCount_management(
                clipped_Output_FeatureClass)

            # Store the integer hail count as a variable for use within
            # other functions.
            self.usa_hail_count = \
                int(hailCountResult_US.getOutput(0))

        except arcpy.ExecuteError:

            # Display geoprocessing errors and skip the failed analysis.
            self.func_Scroll_setOutputText(
                "Failure to count for output US CSV values.", color_Red)

            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Red)

            pass

        except Exception as e:

            # Display error message for all other errors.
            self.func_Scroll_setOutputText(str(e) + "\n" + 
                                           traceback.format_exc(), color_Red)

    def func_CSV_DataCount_Statewide_Count(self):

        # This function controls the counting of all hail within the
        # user-selected state.
        # Used only if county clipping option is selected. It will be
        # used within the output data counts CSV file.

        try:

            # Set workspace to File GDB for the following analysis.
            arcpy.env.workspace = self.subFolder_GIS + "/" + nameFileGDB

            # Assign Census Shapefile within Shapefile subfolder to variable.
            censusShapefile = self.subFolder_CensusShapefile + "/" + \
                                census_URL_CountyShapefile_FileName + fileExtShp

            # Create Census polygon feature class variable stored in memory.
            memoryFeatureClass_State = "in_memory/" + \
                                       self.stringState_Name.get()

            # Copy Census Shapefile to feature class stored in memory.
            arcpy.CopyFeatures_management(censusShapefile,
                                          memoryFeatureClass_State)

            # Pause script for one second.
            sleep(1)

            # Open the Census in_memory feature class with an Update Cursor.
            with arcpy.da.UpdateCursor(memoryFeatureClass_State,
                                    census_Shapefile_Field_StateFIPS) as cursor:

                # For each feature in the Census in_memory feature class...
                for row in cursor:

                    # This If statement removes all state polygon features not
                    # matching the user-selected state FIPS code.
                    if row[0] != \
                    dict_StateName_StateFIPs.get(self.stringState_Name.get()):

                        # Delete feature from in_memory feature class.
                        cursor.deleteRow()

            # Recalculate the extent of the in_memory feature class.
            arcpy.RecalculateFeatureClassExtent_management(
                memoryFeatureClass_State)

            # Create new feature class variable in_memory for clipped hail
            # points.
            clipped_Output_FeatureClass = "in_memory/ClippedOutputFC_State"

            # Perform a clip of raw hail points to the user-selected state
            # and store output as the clipped in_memory feature class.
            arcpy.Clip_analysis(self.nameFeatureClass_FromCSV,
                                memoryFeatureClass_State,
                                clipped_Output_FeatureClass)

            # Perform a count on the clipped hail features found within
            # the in_memory clipped feature class.
            hailCountResult_State = arcpy.GetCount_management(
                clipped_Output_FeatureClass)

            # Store the integer hail count as a variable for use within
            # the in_memory clipped feature class.
            self.state_hail_count = \
                int(hailCountResult_State.getOutput(0))

        except arcpy.ExecuteError:

            # Display geoprocessing errors and skip the failed analysis.
            self.func_Scroll_setOutputText(
                "Failure to count for output state CSV values.", color_Red)

            self.func_Scroll_setOutputText(arcpy.GetMessages(0), color_Red)

            pass

        except Exception as e:

            # Display error message for all other errors.
            self.func_Scroll_setOutputText(str(e) + "\n" + 
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
            self.func_Scroll_setOutputText(str(e) + "\n" + 
                                           traceback.format_exc(), color_Red)

    def func_Scroll_saveOutputText(self):

        # This function writes all of the output text found within the
        # ScrolledText widget to a text file located within the user-defined
        # workspace. This is done at the conclusion of every application
        # iteration.

        try:

            # If the output text file's naming convention has been set...
            if self.nameFeatureClass_FromCSV is not None:

                # Create/Open a new text file for all output messages to be
                # written to.
                textFile_ProcessingHistory = open(self.fullPathName + "/" +
                        "ProcessingHistory_" + self.nameFeatureClass_FromCSV +
                                              fileExtText,"w")
            else:

                # If the application throws errors and fails within the early
                # stages, the naming convention for the output text file will
                # not be established. If that is the case, the naming convention
                # will be saved with FAILED in the name.
                textFile_ProcessingHistory = open(self.fullPathName + "/" +
                        "ProcessingHistory_FAILED" + fileExtText, "w")

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
        self.checkboxExpansionWidth = guiWindow_HailOptions_Width + 300

        # Set the GUI expansion height if timespan/diameter drop-downs show
        # "Custom...".
        self.customSelection_Height = guiWindow_HailOptions_Height + 75

        # If the More Options checkbox is not selected and "Custom..." is not
        # selected for both timespan and diameter...
        if self.statusVar_Checkbutton_Options.get() == 0 and \
                        self.stringHailTimespan.get() != "Custom..." and \
                        self.stringHailDiameter.get() != "Custom...":

            # Set the GUI window dimensions accordingly.
            self.winfo_toplevel().geometry("%dx%d" % (
                guiWindow_HailOptions_Width,
                guiWindow_HailOptions_Height))

            # If the Custom Diameter Min/Max drop-down lists are visible...
            if self.comboFrame_Custom_Diameter is not None:

                # Remove the Custom Diameter Min/Max drop-down lists.
                self.comboFrame_Custom_Diameter.grid_remove()

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
        # or custom diameter are selected...
        elif self.statusVar_Checkbutton_Options.get() == 0 and \
                (self.stringHailTimespan.get() == "Custom..." or
                        self.stringHailDiameter.get() == "Custom..."):

            # Set the GUI window dimensions accordingly.
            self.winfo_toplevel().geometry("%dx%d" % (
                guiWindow_HailOptions_Width,
                self.customSelection_Height))

            # Clear the variable assignment for the State combobox drop-down.
            if self.comboFrame_State is not None:

                self.comboFrame_State = None

            # Clear the variable assignment for the County combobox drop-down.
            if self.comboFrame_Counties is not None:

                self.comboFrame_Counties = None

        # Else if the More Options checkbox is selected and both the custom
        # timespan and custom diameter are not selected...
        elif self.statusVar_Checkbutton_Options.get() == 1 and \
                        self.stringHailTimespan.get() != "Custom..." and \
                        self.stringHailDiameter.get() != "Custom...":

            # Set the GUI window dimensions accordingly.
            self.winfo_toplevel().geometry("%dx%d" % (
                self.checkboxExpansionWidth,
                guiWindow_HailOptions_Height))

            # If the Custom Diameter Min/Max drop-down lists are visible...
            if self.comboFrame_Custom_Diameter is not None:

                # Remove the Custom Diameter Min/Max drop-down lists.
                self.comboFrame_Custom_Diameter.grid_remove()

            # If the Custom Timespan From/To drop-down lists are visible...
            if self.comboFrame_Custom_Timespan is not None:

                # Remove the Custom Timespan From/To drop-down lists.
                self.comboFrame_Custom_Timespan.grid_remove()

        # Else if the More Options checkbox is checked and the custom timespan
        # or custom diameter are selected...
        elif self.statusVar_Checkbutton_Options.get() == 1 and \
                (self.stringHailTimespan.get() == "Custom..." or
                         self.stringHailDiameter.get() == "Custom..."):

            # Set the GUI window dimensions accordingly.
            self.winfo_toplevel().geometry("%dx%d" % (
                self.checkboxExpansionWidth,
                self.customSelection_Height))

    def func_Enable_Buttons(self):

        # This function controls the enabling of all user-selectable buttons,
        # checkboxes, radio buttons, and drop-down lists. This is used when the
        # application has finished performing all tasks.

        # Enable Diameter drop-down list.
        self.combo_HailDiameter.config(state="readonly")
        self.combo_HailDiameter.update()

        # Enable Timespan drop-down list.
        self.combo_HailTimespan.config(state="readonly")
        self.combo_HailTimespan.update()

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

        # If the Custom Diameter Min/Max drop-down lists are visible...
        if self.comboFrame_Custom_Diameter is not None:

            # Enable the Custom Diameter Min drop-down list.
            self.combo_Custom_Diameter_Min.config(state="readonly")
            self.combo_Custom_Diameter_Min.update()

            # Enable the Custom Diameter Max drop-down list.
            self.combo_Custom_Diameter_Max.config(state="readonly")
            self.combo_Custom_Diameter_Max.update()

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

            # Enable the IDW checkbox.
            self.checkbox_IDW.config(state=tkinter.NORMAL)
            self.checkbox_IDW.update()

            # Enable the Kernel Density checkbox.
            self.checkbox_KernelDensity.config(state=tkinter.NORMAL)
            self.checkbox_KernelDensity.update()

            # Enable the Kriging checkbox.
            self.checkbox_Kriging.config(state=tkinter.NORMAL)
            self.checkbox_Kriging.update()

            # Enable the Natural Neighbor checkbox.
            self.checkbox_NaturalNeighbor.config(state=tkinter.NORMAL)
            self.checkbox_NaturalNeighbor.update()

            # Enable the Optimized Hot Spot checkbox.
            self.checkbox_OptHotSpot.config(state=tkinter.NORMAL)
            self.checkbox_OptHotSpot.update()

            # Enable the Point Density checkbox.
            self.checkbox_PointDensity.config(state=tkinter.NORMAL)
            self.checkbox_PointDensity.update()

            # Enable the Spline checkbox.
            self.checkbox_Spline.config(state=tkinter.NORMAL)
            self.checkbox_Spline.update()

            # Enable the Thiessen checkbox.
            self.checkbox_Thiessen.config(state=tkinter.NORMAL)
            self.checkbox_Thiessen.update()

            # Enable the Trend checkbox.
            self.checkbox_Trend.config(state=tkinter.NORMAL)
            self.checkbox_Trend.update()

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

        # Disable the Diameter drop-down list.
        self.combo_HailDiameter.config(state=tkinter.DISABLED)
        self.combo_HailDiameter.update()

        # Disable the Timespan drop-down list.
        self.combo_HailTimespan.config(state=tkinter.DISABLED)
        self.combo_HailTimespan.update()

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

        # If the Custom Diameter Min/Max drop-down lists are visible...
        if self.comboFrame_Custom_Diameter is not None:

            # Disable the Min Diameter drop-down list.
            self.combo_Custom_Diameter_Min.config(state=tkinter.DISABLED)
            self.combo_Custom_Diameter_Min.update()

            # Disable the Max Diameter drop-down list.
            self.combo_Custom_Diameter_Max.config(state=tkinter.DISABLED)
            self.combo_Custom_Diameter_Max.update()

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

            # Disable the IDW checkbox.
            self.checkbox_IDW.config(state=tkinter.DISABLED)
            self.checkbox_IDW.update()

            # Disable the Kernel Density checkbox.
            self.checkbox_KernelDensity.config(state=tkinter.DISABLED)
            self.checkbox_KernelDensity.update()

            # Disable the Kriging checkbox.
            self.checkbox_Kriging.config(state=tkinter.DISABLED)
            self.checkbox_Kriging.update()

            # Disable the Natural Neighbor checkbox.
            self.checkbox_NaturalNeighbor.config(state=tkinter.DISABLED)
            self.checkbox_NaturalNeighbor.update()

            # Disable the Optimized Hot Spot checkbox.
            self.checkbox_OptHotSpot.config(state=tkinter.DISABLED)
            self.checkbox_OptHotSpot.update()

            # Disable the Point Density checkbox.
            self.checkbox_PointDensity.config(state=tkinter.DISABLED)
            self.checkbox_PointDensity.update()

            # Disable the Spline checkbox.
            self.checkbox_Spline.config(state=tkinter.DISABLED)
            self.checkbox_Spline.update()

            # Disable the Thiessen checkbox.
            self.checkbox_Thiessen.config(state=tkinter.DISABLED)
            self.checkbox_Thiessen.update()

            # Disable the Trend checkbox.
            self.checkbox_Trend.config(state=tkinter.DISABLED)
            self.checkbox_Trend.update()

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
            self.remainingSeconds = self.elapsed_time%3600

            if self.remainingSeconds >= 60:

                self.minutes = int(self.remainingSeconds / 60)
                self.remainingSeconds = self.remainingSeconds%60

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
            self.remainingSeconds = self.elapsed_time%60

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
        self.scrollBox.tag_config(color_Red, foreground = color_Red)
        self.scrollBox.tag_config(color_Orange, foreground = color_Orange)
        self.scrollBox.tag_config(color_Blue, foreground = color_Blue)

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