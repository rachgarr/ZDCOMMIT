# By: Rodrigo Rivero
# This file is meant to be used with ArcMap in order to extract information from a shapefile and export it into a raster
# Import system modules needed
import arcpy
from arcpy import env
from arcpy.sa import *

# Workspace(this might change depending on your folder structure)
env.workspace = "C:/Users/rodri/Desktop/Sandbox"

# Clear environment
arcpy.ClearEnvironment("snapRaster")
arcpy.ClearEnvironment("cellSize")
arcpy.ClearEnvironment("extent")

# Environment settings
templateMap = ""
arcpy.env.snapRaster = Raster(templateMap)
arcpy.env.cellSize = Raster(templateMap)
arcpy.env.extent = Raster(templateMap)

# Set main feature(the shapefile you want to create the raster from)
inFeature = ""

# Name of the new raster
outRaster = ""

# Name of the field in the shapefile wanted
field = ""

## Execute FeatureToRaster
arcpy.FeatureToRaster_conversion(inFeature, field, outRaster)
