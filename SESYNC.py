import arcpy
from arcpy import env  
from arcpy.sa import *
import os 
import sys 
from os import rename, listdir 
arcpy.env.overwriteOutput=True

arcpy.CheckOutExtension("Spatial")
arcpy.CheckOutExtension("3D")
arcpy.CheckOutExtension("Network")
arcpy.CheckOutExtension("Tracking")
arcpy.CheckOutExtension("Spatial")

userAccount = str('C:\\Users\\standard\\Dropbox\\')
#defaultFolder = str('SESYNC_ToyModel_BBAP')
defaultFolder = str('SESYNC_souce')


defaultPath = userAccount + defaultFolder
env.workspace =  defaultPath
jordanFolder = defaultPath+ str("\\Jordan\\")
snap_file = jordanFolder + "2001.tif"
mask = defaultPath + "\\master_mask.tif"


sr1 = arcpy.Describe(Raster(jordanFolder + "2001.tif")).spatialReference
defaultGeodatabase = str("C:\Users\standard\Documents\ArcGIS\Default.gdb")
