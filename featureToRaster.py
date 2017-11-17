# By: Rodrigo River
# This file is meant to be used with ArcMap in order to extract information from a shapefile and export it into a raster

# The main file we have is 2012PanelData.shp and what we want to get out is the following
# soy_area
# corn_area
# soy_yield
# cattle_heads

# Import system modules
import arcpy
from arcpy import env
from arcpy.sa import *

# Set environment settings
# Workspace(this might change depending on your folder structure)
env.workspace = "C:/Users/rodri/Desktop/Sandbox"

arcpy.ClearEnvironment("snapRaster")
arcpy.ClearEnvironment("cellSize")
arcpy.ClearEnvironment("extent")

arcpy.env.snapRaster = Raster("cropped2012.tif")
arcpy.env.cellSize = Raster("cropped2012.tif")
arcpy.env.extent = Raster("cropped2012.tif")

# Set main feature
inFeature = "2012PanelData.shp"

# Soy Area
outRaster = "soyArea2012.tif"
field = "soy_area"
## Execute FeatureToRaster
arcpy.FeatureToRaster_conversion(inFeature, field, outRaster)

# Corn Area
outRaster = "cornArea2012.tif"
field = "corn_area"
arcpy.FeatureToRaster_conversion(inFeature, field, outRaster)

# Soy Yield
outRaster = "soyYield2012.tif"
field = "soy_yield"
arcpy.FeatureToRaster_conversion(inFeature, field, outRaster)

# Cattle Heads
outRaster = "cattleHeads2012.tif"
field = "cattle_hea"
arcpy.FeatureToRaster_conversion(inFeature, field, outRaster)