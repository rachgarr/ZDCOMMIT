# Put SESYNC.py in Lib under the ArcGIS10.4\Lib folder 

# import arcpy
# from arcpy import env  
# from arcpy.sa import *
# import os 
# import sys 
# from os import rename, listdir 
# arcpy.env.overwriteOutput=True

# arcpy.CheckOutExtension("Spatial")
# arcpy.CheckOutExtension("3D")
# arcpy.CheckOutExtension("Network")
# arcpy.CheckOutExtension("Tracking")

# userAccount = str('C:\\Users\\standard\\Dropbox\\')
# defaultFolder = str('SESYNC_ToyModel_BBAP')

# defaultPath = userAccount + defaultFolder
# jordanFolder = defaultPath+ str("\\Jordon\\")
# sr1 = arcpy.Describe(Raster(jordanFolder + "2001.tif")).spatialReference
# snap_file = jordonFolder + "2001.tif"
# mask = defaultPath + "\\master_mask.tif"

from SESYNC import *  


#check your environment settings 
environments = arcpy.ListEnvironments()
environments.sort
for environment in environments:
    print("{0:<30}: {1}".format(environment, arcpy.env[environment]))


##################################################################
####################### POINT VECTORS WITH FID############################
##################################################################

####
#Ports
####
env.workspace =  defaultPath + "\\Ports"
arcpy.ClearEnvironment("snapRaster")
arcpy.ClearEnvironment("cellSize")
arcpy.ClearEnvironment("extent")

#Merge points from individual countries 
port_list = arcpy.ListFiles("*.shp")
arcpy.Merge_management(port_list, "Merged_Ports.shp")

#Reproject to WGS84 
for shpFile in arcpy.ListFiles("Merged*.shp"):
    shpFileName = os.path.splitext(shpFile)[0]
    outputFile = "reprojected_" + shpFileName.replace('Merged_', '', 1) + ".shp"
    arcpy.Project_management(shpFile,outputFile,sr1)

field_name = str("FID2")
#Add 1 to all FID (if there is a 0 FID and conversion to raster creates a "0" block around the port-pixel, causing information to be lost)
for k in arcpy.ListFiles("reprojected_*.shp"):
    arcpy.AddField_management(k, "FID2", "DOUBLE")
    fields = ['FID', 'FID2']
    count = 0 
    with arcpy.da.UpdateCursor(k, fields) as cursor: 
        for row in cursor: 
            row[1] = row[0] + 1
            cursor.updateRow(row)
#Convert to raster 
arcpy.env.snapRaster = Raster(jordanFolder + "2001.tif")
arcpy.env.cellSize = Raster(jordanFolder + "2001.tif")
arcpy.env.extent = Raster(jordanFolder + "2001.tif")
for shpFile in arcpy.ListFiles("reprojected_*.shp"):
    shpFileName = os.path.splitext(shpFile)[0] #can be used interchangeably with the 
    print(shpFileName)
    print(shpFile)
    outputFile = shpFileName.replace('reprojected_', 'interm_', 1) + ".tif" 
    print(outputFile)
    arcpy.FeatureToRaster_conversion(shpFile, field_name, outputFile)



####
#Slaughter House (the folder is erratically named Fridges): similar to Ports
####
arcpy.ClearEnvironment("snapRaster")
arcpy.ClearEnvironment("cellSize")
arcpy.ClearEnvironment("extent")
env.workspace =  defaultPath + "\\Fridges" 
fridge_list = arcpy.ListFiles("*.shp")
arcpy.Merge_management(fridge_list, "Merged_Fridges.shp")


for shpFile in arcpy.ListFiles("Merged*.shp"):
    shpFileName = os.path.splitext(shpFile)[0]
    outputFile = "reprojected_" + shpFileName.replace('Merged_', '', 1) + ".shp"
    print(shpFileName)
    print(shpFile)
    print(outputFile)
    arcpy.Project_management(shpFile,outputFile,sr1)
field_name = str("FID2")
arcpy.env.snapRaster = Raster(jordanFolder + "2001.tif")
arcpy.env.cellSize = Raster(jordanFolder + "2001.tif")
arcpy.env.extent = Raster(jordanFolder + "2001.tif")
#
for shpFile in arcpy.ListFiles("reprojected_*.shp"):
    arcpy.AddField_management(shpFile, "FID2", "DOUBLE")
    fields = ['FID', 'FID2']
    count = 0 
    with arcpy.da.UpdateCursor(shpFile, fields) as cursor: 
        for row in cursor: 
            row[1] = row[0] + 1
            cursor.updateRow(row)
    shpFileName = os.path.splitext(shpFile)[0]
    print(shpFileName, shpFile)
    outputFile = shpFileName.replace('reprojected_', 'interm_', 1) + ".tif" 
    print(outputFile)
    arcpy.FeatureToRaster_conversion(shpFile, field_name, outputFile)



####
#Processing Facilities: similar to Ports
####
arcpy.ClearEnvironment("snapRaster")
arcpy.ClearEnvironment("cellSize")
arcpy.ClearEnvironment("extent")
env.workspace =  defaultPath + "\\Processing Facilities" 

fridge_list = arcpy.ListFiles("*.shp")
arcpy.Merge_management(fridge_list, "Merged_Processing.shp")


for shpFile in arcpy.ListFiles("*Merged*.shp"):
    shpFileName = os.path.splitext(shpFile)[0]
    outputFile = "reprojected_" + shpFileName.replace('Merged_', '', 1) + ".shp"
    print(shpFileName)
    print(shpFile)
    print(outputFile)
    arcpy.Project_management(shpFile,outputFile,sr1)
field_name = str("FID2")
arcpy.env.snapRaster = Raster(jordanFolder + "2001.tif")
arcpy.env.cellSize = Raster(jordanFolder + "2001.tif")
arcpy.env.extent = Raster(jordanFolder + "2001.tif")
for shpFile in arcpy.ListFiles("reprojected_*.shp"):
    arcpy.AddField_management(shpFile, "FID2", "DOUBLE")
    fields = ['FID', 'FID2']
    count = 0 
    with arcpy.da.UpdateCursor(shpFile, fields) as cursor: 
        for row in cursor: 
            row[1] = row[0] + 1
            cursor.updateRow(row)
    shpFileName = os.path.splitext(shpFile)[0]
    print(shpFileName, shpFile)
    outputFile = shpFileName.replace('reprojected_', 'interm_', 1) + ".tif" 
    print(outputFile)
    arcpy.FeatureToRaster_conversion(shpFile, field_name, outputFile)

##################################################################
####################### POINT VECTORS WITHOUT FID############################
##################################################################

####
# Towns: similar to Ports
####
env.workspace =  defaultPath + "\\Towns" 
arcpy.ClearEnvironment("snapRaster")
arcpy.ClearEnvironment("cellSize")
arcpy.ClearEnvironment("extent")

town_50k_list = arcpy.ListFiles("*over50k*.shp")
town_10k_list= arcpy.ListFiles("*over10k*.shp")
arcpy.CopyFeatures_management("Towns.shp", "Merged_Towns_over0k.shp")
arcpy.Merge_management(town_50k_list, "Merged_Towns_over50k.shp")
arcpy.Merge_management(town_10k_list, "Merged_Towns_over10k.shp")


for shpFile in arcpy.ListFiles("Merged*.shp"):
    shpFileName = os.path.splitext(shpFile)[0]
    outputFile = shpFileName.replace("Merged", "reprojected_", 1) + ".shp"
    print(shpFileName)
    print(shpFile)
    print(outputFile)
    arcpy.Project_management(shpFile,outputFile,sr1)
arcpy.env.snapRaster = Raster(jordanFolder + "2001.tif")
arcpy.env.cellSize = Raster(jordanFolder + "2001.tif")
arcpy.env.extent = Raster(jordanFolder + "2001.tif")

#Since we don't have mean population for major towns, 
#convert to raster with field name: max population, min population

field_name = str("POP_MAX")
for shpFile in arcpy.ListFiles("reprojected_*.shp"):
    shpFileName = os.path.splitext(shpFile)[0]
    print(shpFileName, shpFile)
    outputFile = shpFileName.replace('reprojected_', 'interm_' + field_name  +"_", 1) + ".tif" 
    print(outputFile)
    arcpy.FeatureToRaster_conversion(shpFile, field_name, outputFile)
field_name = str("POP_MIN")
for shpFile in arcpy.ListFiles("reprojected_*.shp"):
    shpFileName = os.path.splitext(shpFile)[0]
    print(shpFileName, shpFile)
    outputFile = shpFileName.replace('reprojected_', 'interm_' + field_name  +"_", 1) + ".tif" 
    print(outputFile)
    arcpy.FeatureToRaster_conversion(shpFile, field_name, outputFile)


############
#Set noData to 9999 
#For point vector, arcGIS creates a block of 0 around the targeted tile
#So we need to change Null Value to 0, and the change all 0 value to -9999 as the NoData Value 
############
# env.workspace =  defaultPath  
# rasters_list =[]
# for dirpath, dirnames, filenames in arcpy.da.Walk(defaultPath, topdown = True, datatype = "RasterDataset"):
#     for filename in filenames:
#         if ("interm_" in filename) :
#             rasters_list.append(os.path.join(dirpath, filename))
#             print(os.path.join(dirpath, filename))

# for k in rasters_list:
#     OutRaster = Con(IsNull(k), 0, k) #Change all NoData values to 0
#     Final = Con(EqualTo(OutRaster, 0), -9999, OutRaster) #Change all 0 values to 9999
#     output_file = k.replace("interm_", "raster_", 1) 
#     Final.save(FinalRaster_Name)



for k in arcpy.ListRasters("interm_*", "TIF"):
    OutRaster = Con(IsNull(k), 0, k) #Change all NoData values to 0
    Final = Con(EqualTo(OutRaster, 0), -9999, OutRaster) #Change all 0 values to 9999
    FinalRaster_Name = "raster_" + k.replace('interm_', '', 1)
    Final.save(FinalRaster_Name)


env.workspace =  defaultPath + "\\Ports" 
for k in arcpy.ListRasters("interm_*", "TIF"):
    OutRaster = Con(IsNull(k), 0, k) #Change all NoData values to 0
    Final = Con(EqualTo(OutRaster, 0), -9999, OutRaster) #Change all 0 values to 9999
    FinalRaster_Name = "raster_" + k.replace('interm_', '', 1)
    Final.save(FinalRaster_Name)

env.workspace =  defaultPath + "\\Fridges" 
for k in arcpy.ListRasters("interm_*", "TIF"):
    OutRaster = Con(IsNull(k), 0, k) #Change all NoData values to 0
    Final = Con(EqualTo(OutRaster, 0), -9999, OutRaster) #Change all 0 values to 9999
    FinalRaster_Name = "raster_" + k.replace('interm_', '', 1)
    Final.save(FinalRaster_Name)

env.workspace =  defaultPath + "\\Towns" 
for k in arcpy.ListRasters("interm_*", "TIF"):
    OutRaster = Con(IsNull(k), 0, k) #Change all NoData values to 0
    Final = Con(EqualTo(OutRaster, 0), -9999, OutRaster) #Change all 0 values to 9999
    FinalRaster_Name = "raster_" + k.replace('interm_', '', 1)
    Final.save(FinalRaster_Name)

env.workspace =  defaultPath + "\\Processing Facilities" 
for k in arcpy.ListRasters("interm_*", "TIF"):
    OutRaster = Con(IsNull(k), 0, k) #Change all NoData values to 0
    Final = Con(EqualTo(OutRaster, 0), -9999, OutRaster) #Change all 0 values to 9999
    FinalRaster_Name = "raster_" + k.replace('interm_', '', 1)
    Final.save(FinalRaster_Name)



##################################################################
################LINES AND POLYGONS ###############################
##################################################################
#####
# WDPA Protected 
#####
arcpy.ClearEnvironment("snapRaster")
arcpy.ClearEnvironment("cellSize")
arcpy.ClearEnvironment("extent")
env.workspace =  defaultPath + "\\WDPA_Protected" 
field_name= str('WDPAID')
#WDPA shape files do not have projection defined, but it is WGS85
for k in arcpy.ListFiles("*.shp"):
    arcpy.DefineProjection_management(k,sr1)

arcpy.env.snapRaster = Raster(jordanFolder + "2001.tif")
arcpy.env.cellSize = Raster(jordanFolder + "2001.tif")
arcpy.env.extent = Raster(jordanFolder + "2001.tif")

#Convert to raster 
for shpFile in arcpy.ListFiles("*.shp"):
    shpFileName = os.path.splitext(shpFile)[0]
    outputFile = 'raster_' + shpFileName + ".tif" 
    print(shpFileName, shpFile, outputFile)
    arcpy.FeatureToRaster_conversion(shpFile, field_name, outputFile)

#####
#Biomes:  
#####
arcpy.ClearEnvironment("snapRaster")
arcpy.ClearEnvironment("cellSize")
arcpy.ClearEnvironment("extent")
env.workspace =  defaultPath + "\\Biomes"  
# Reproject to WGS84
for shpFile in arcpy.ListFiles("*.shp"):
    shpFileName = os.path.splitext(shpFile)[0]
    outputFile = "reprojected_" + shpFileName + ".shp"
    print(shpFileName, shpFile, outputFile)
    arcpy.Project_management(shpFile,outputFile,sr1)
arcpy.env.snapRaster = Raster(jordanFolder + "2001.tif")
arcpy.env.cellSize = Raster(jordanFolder + "2001.tif")
arcpy.env.extent = Raster(jordanFolder + "2001.tif")
#Similar to point vector, I add 1 to all FID, so there is no 0 
field_name = str("FID2")
for shpFile in arcpy.ListFiles("reprojected_*.shp"):
    arcpy.AddField_management(shpFile, "FID2", "DOUBLE")
    fields = ['FID', 'FID2']
    count = 0 
    with arcpy.da.UpdateCursor(shpFile, fields) as cursor: 
        for row in cursor: 
            row[1] = row[0] + 1
            cursor.updateRow(row)
    shpFileName = os.path.splitext(shpFile)[0]
    print(shpFileName, shpFile)
    if "tnc" in str(shpFileName):
        #Name it raster_mask since the master mask would be based only on tnc layer
        #as Brazilian biome does not cover BBAP
        outputFile = shpFileName.replace('reprojected_', 'raster_mask_', 1) + ".tif" 
    else:
        outputFile = shpFileName.replace('reprojected_', 'raster_', 1) + ".tif" 
    print(outputFile)
    arcpy.FeatureToRaster_conversion(shpFile, field_name, outputFile)



#####
# River 
#####
arcpy.ClearEnvironment("snapRaster")
arcpy.ClearEnvironment("cellSize")
arcpy.ClearEnvironment("extent")
env.workspace =  defaultPath + "\\sa_riv_30s" ### REDO 
field_name = str("UP_CELLS")
#Reproject to WGS84
for shpFile in arcpy.ListFiles("*.shp"):
    shpFileName = os.path.splitext(shpFile)[0]
    outputFile = "reprojected_" + shpFileName + ".shp"
    print(shpFile, outputFile)
    arcpy.Project_management(shpFile,outputFile,sr1)
arcpy.env.snapRaster = Raster(jordanFolder + "2001.tif")
arcpy.env.cellSize = Raster(jordanFolder + "2001.tif")
arcpy.env.extent = Raster(jordanFolder + "2001.tif")
#Retain all of the UP_CELLS value 
for shpFile in arcpy.ListFiles("reprojected_*.shp"):
    shpFileName = os.path.splitext(shpFile)[0]
    outputFile = shpFileName.replace('reprojected_', 'raster_', 1) + ".tif" 
    print(shpFileName, shpFile, outputFile)
    arcpy.FeatureToRaster_conversion(shpFile, field_name, outputFile)




####
# Roads (OpenStreetMap) 
####
arcpy.ClearEnvironment("snapRaster")
arcpy.ClearEnvironment("cellSize")
arcpy.ClearEnvironment("extent")
env.workspace =  defaultPath + "\\Roads" 
OpenStreet_list = arcpy.ListFiles("*exp*.shp")
#For uniformity, I name all shape files as Merge_*, so in the next step I can 
#use wild card search Merge*
arcpy.CopyFeatures_management("Roads.shp", "Merged_Roads_minor.shp")
arcpy.CopyFeatures_management("Roads_GRI.shp", "Merged_Roads_major.shp")
arcpy.Merge_management(OpenStreet_list, "Merged_Roads_pave.shp")
#Reproject to WGS84
for shpFile in arcpy.ListFiles("Merged*.shp"):
    shpFileName = os.path.splitext(shpFile)[0]
    outputFile =  shpFileName.replace("Merged", "reprojected_", 1) + ".shp"
    print(shpFileName, shpFile, outputFile)
    arcpy.Project_management(shpFile,outputFile,sr1)

arcpy.env.snapRaster = Raster(jordanFolder + "2001.tif")
arcpy.env.cellSize = Raster(jordanFolder + "2001.tif")
arcpy.env.extent = Raster(jordanFolder + "2001.tif")

for shpFile in arcpy.ListFiles("reprojected_*.shp"):
    shpFileName = os.path.splitext(shpFile)[0]
    outputFile = shpFileName.replace('reprojected_', 'raster_', 1) + ".tif" 
    print(shpFileName, shpFile, outputFile)
    arcpy.AddField_management(shpFile, "FID2", "DOUBLE")
    fields = ['FID', 'FID2']
    count = 0 
    with arcpy.da.UpdateCursor(shpFile, fields) as cursor: 
        for row in cursor: 
            row[1] = row[0] + 1
            cursor.updateRow(row)
    # Field name used for FeatureToRaster conversion changes depending on the layer
    if 'pave' in shpFileName:
        field_name = 'paved'
    elif ('major' in shpFileName) or ('minor' in shpFileName):
        field_name = 'FID'
    arcpy.FeatureToRaster_conversion(shpFile, field_name, outputFile)

####
# Admin 
####
arcpy.ClearEnvironment("snapRaster")
arcpy.ClearEnvironment("cellSize")
arcpy.ClearEnvironment("extent")

env.workspace =  defaultPath + "\\Admin" 
# Merge country admin shape files by level0, level1, level2, level3
for i in range(0, 4):
    holder = "*adm" + str(i) + "*.shp" 
    outputname = "level" + str(i) + ".shp"
    print(holder)
    listfile= arcpy.ListFiles(holder)
    print(listfile)
    arcpy.Merge_management(listfile, outputname)
#Reproject the merged layers into WGS84
for shpFile in arcpy.ListFiles("level*.shp"):
    shpFileName = os.path.splitext(shpFile)[0]
    outputFile = "reprojected_" + shpFileName + ".shp"
    arcpy.Project_management(shpFile,outputFile,sr1)
arcpy.env.snapRaster = Raster(jordanFolder + "2001.tif")
arcpy.env.cellSize = Raster(jordanFolder + "2001.tif")
arcpy.env.extent = Raster(jordanFolder + "2001.tif")
#Convert to raster, name level0 as raster_mask_* instead of raster_* 
#since we use level0 to compute master_mask 
field_name= str('FID')
for shpFile in arcpy.ListFiles("reprojected_*.shp"):
    shpFileName = os.path.splitext(shpFile)[0]
    print(shpFileName)
    print(shpFile)
    if "level0" in shpFileName:
        outputFile = shpFileName.replace('reprojected_', 'raster_mask_', 1) + ".tif" 
    else:
        outputFile = shpFileName.replace('reprojected_', 'raster_', 1) + ".tif" 
    print(outputFile)
    arcpy.FeatureToRaster_conversion(shpFile, field_name, outputFile)


##################################################################
########################### RASTER ###############################
##################################################################

####
# Mosaic SRTM, Project onto 2-D, calculate slope, convert back to WGS84 
####
env.workspace =  defaultPath + "\\SRTMv4.1"
arcpy.ClearEnvironment("snapRaster")
arcpy.ClearEnvironment("cellSize")
arcpy.ClearEnvironment("extent")
#Mosaic all SRTM tiles in the folder 
raster_list = arcpy.ListRasters("srtm_*", "TIF")
arcpy.MosaicToNewRaster_management(raster_list, defaultPath + "\\SRTMv4.1\\" , "Mosaic_Elevation.tif", number_of_bands = 1 )
#Clip it to the extent of Jordan's map 
arcpy.Clip_management(Raster("Mosaic_Elevation.tif"),"#","interm_Elevation.tif", Raster( jordanFolder + "2001.tif") ,-9999,"NONE","MAINTAIN_EXTENT")
#nNeed to remind arcGIS that 255 is NOT the nodata value by setting -9999 as the nodata value
#In fact, the SRTM layers have NO nodata cells, all cells have values between 0 to 255 
arcpy.SetRasterProperties_management("interm_Elevation.tif", "", "", "", "1 -9999", "")
arcpy.BuildPyramids_management("interm_Elevation.tif")

#Reproject the elevation layer into projected coordinate system (2D)
sr_robinson = arcpy.SpatialReference(54030)
#This is oftentime problematic, thus we need to execute it twice, or weird things happen 
arcpy.ProjectRaster_management("interm_Elevation.tif", "Robinson_Elevation.tif", sr_robinson, in_coor_system = sr1)
arcpy.ProjectRaster_management("interm_Elevation.tif", "Robinson_Elevation.tif", sr_robinson, in_coor_system = sr1)

#Calculate Slope 
arcpy.ClearEnvironment("snapRaster") # Clear the environment just to be safe 
arcpy.ClearEnvironment("cellSize")
arcpy.ClearEnvironment("extent")
arcpy.Slope_3d("Robinson_Elevation.tif" , "Slope_Robinson.tif", "DEGREE", "1")
arcpy.ProjectRaster_management("Slope_Robinson.tif", "interm_Slope.tif", sr1) # Project from Robinson back to WGS84

# Finally, snap to the grid to Jordan's data  
# WARNING: CANNOT USE CLIP_MANAGEMENT OR PROJECTRASTER MANAGEMENT! DOESN'T WORK
#          ONLY THE FOLLOWING WORKS 
arcpy.env.snapRaster = Raster(jordanFolder + "2001.tif")
arcpy.env.cellSize = Raster(jordanFolder + "2001.tif")
arcpy.env.extent = Raster(jordanFolder + "2001.tif")
for tiffFile in arcpy.ListRasters("*interm_*", "TIF"):   
    outputFile = tiffFile.replace("interm_", "raster_", 1)
    temp = Con(IsNull(Raster(snap_file)), tiffFile, tiffFile)
    print(outputFile)
    temp.save(outputFile)
    arcpy.SetRasterProperties_management(outputFile, "", "", "", "1 -9999", "")


# Mask 
# This doesn't work, as the mask I downloaded from CGIAR website 
# does not give me a clearly defined coastline 

# env.workspace =  defaultPath + "\\SRTMv4.1\\srtm_mk"
# arcpy.ClearEnvironment("snapRaster")
# arcpy.ClearEnvironment("cellSize")
# arcpy.ClearEnvironment("extent")

# for k in arcpy.ListRasters("Z_*", "TIF"):
#     arcpy.DefineProjection_management(k,sr1)

# raster_list = arcpy.ListRasters("Z_*", "TIF")
# arcpy.MosaicToNewRaster_management(raster_list, defaultPath + "\\SRTMv4.1\\srtm_mk\\" , "Mosaic_Mask.tif", number_of_bands = 1 )
# arcpy.Clip_management(Raster("Mosaic_Mask.tif"),"#","raster_mask.tif", Raster( jordanFolder + "2001.tif") ,-9999,"NONE","MAINTAIN_EXTENT")

# temp = arcpy.MosaicToNewRaster_management(raster_list, defaultPath + "\\SRTMv4.1\\srtm_mk\\" , "Mosaic_Mask.tif", number_of_bands = 1 )
# arcpy.Clip_management(temp,"#","raster_mask.tif", Raster( jordanFolder + "2001.tif") ,-9999,"NONE","MAINTAIN_EXTENT")

# for tiffFile in arcpy.ListRasters("*raster_mask*", "TIF"):   
#     outputFile = tiffFile.replace("interm_", "raster_", 1)
#     print(outputFile)
#     temp = Con(IsNull(Raster(snap_file)), tiffFile, tiffFile)
#     temp.save(outputFile)


####
# Make NetCDF RasterLayer for precipitation and temperature 
####
arcpy.ClearEnvironment("snapRaster")
arcpy.ClearEnvironment("cellSize")
arcpy.ClearEnvironment("extent")
env.workspace =  defaultPath + "\\temp_pre"

#Convert from NetCDFRaster to Raster, and Reproject to WGS84
for shpFile in arcpy.ListFiles("*.nc"):
    shpFileName = os.path.splitext(shpFile)[0]
    outputFile = "Reprojected_" + shpFileName.replace('.nc', '', 1) + '.tif' 
    print(shpFileName)
    print(shpFile)
    print(outputFile)
    if "air" in str(shpFileName):
        arcpy.MakeNetCDFRasterLayer_md(shpFile, "air", "lon", "lat", "output")
        arcpy.ProjectRaster_management("output", outputFile,sr1)
    elif "precip" in str(shpFileName): 
        arcpy.MakeNetCDFRasterLayer_md(shpFile, "precip", "lon", "lat", "output")
        arcpy.ProjectRaster_management("output", outputFile,sr1)



###################### THE ERRATIC WAY ###############
# arcpy.env.snapRaster = Raster(jordanFolder + "2001.tif")
# arcpy.env.cellSize = Raster(jordanFolder + "2001.tif")
# arcpy.env.extent = Raster(jordanFolder + "2001.tif")
#####Clip to the extent to Jordan's layer >> CHANGES DATA ACCURACY. DONT DO IT >> THIS CAUSES PROBLEMS 
#####Since temperature and precipitation data is the most coarse, we exclude these two in mask calculation, 
#####and attempt to fill them in  
# for tiffFile in arcpy.ListRasters("Reprojected*", "TIF"):
#     outputFile = tiffFile.replace("Reprojected", "Clipped_noEnv", 1)
#     print(outputFile)
#     arcpy.Clip_management(tiffFile, "#",outputFile, Raster( jordanFolder + "2001.tif"), -9999,"NONE", "MAINTAIN_EXTENT")
# for tiffFile in arcpy.ListRasters("Clipped*", "TIF"):   
#     outputFile = tiffFile.replace("Clipped_", "raster_", 1)
#     print(outputFile)
#     # arcpy.CopyRaster_management(tiffFile, outputFile) #CopyRaster_management respectd the grid cell size
#     temp = Con(IsNull(Raster(snap_file)), tiffFile, tiffFile)
#     temp.save(outputFile)


############### THE CORRECT WAY ###############
#####Since temperature and precipitation data is the most coarse, we exclude these two in mask calculation, 
#####and attempt to fill them in  

arcpy.ClearEnvironment("snapRaster")
arcpy.ClearEnvironment("cellSize")
arcpy.ClearEnvironment("extent")

#Create focal layers (average of 3 by 3 grid)
#Make sure Environment is TURNED OFF
for k in arcpy.ListRasters("Reprojected*", "TIF"):
    print(k)
    outputname_focal = k.replace("Reprojected", "Focal1", 1)
    temp_focal = arcpy.sa.FocalStatistics(k, NbrRectangle(3,3), "MEAN", "")
    temp_focal.save(outputname_focal)
    arcpy.BuildPyramids_management(outputname_focal)

#Create focal layers (average of 7 by 7 grid)
#Make sure Environment is TURNED OFF
for k in arcpy.ListRasters("Reprojected*", "TIF"):
    print(k)
    outputname_focal = k.replace("Reprojected", "Focal2", 1)
    temp_focal = arcpy.sa.FocalStatistics(k, NbrRectangle(7,7), "MEAN", "")
    temp_focal.save(outputname_focal)
    arcpy.BuildPyramids_management(outputname_focal)

#Snap these focal layers, as well as the temp precipitation layers to 
#Jordan's grid 
#ATTENTION: Focal layers would be later AFTER the master mask is computed 
arcpy.env.snapRaster = Raster(jordanFolder + "2001.tif")
arcpy.env.cellSize = Raster(jordanFolder + "2001.tif")
arcpy.env.extent = Raster(jordanFolder + "2001.tif")

for tiffFile in arcpy.ListRasters("Reprojected*", "TIF"):   
    outputFile = tiffFile.replace("Reprojected", "raster", 1)
    print(outputFile)
    temp = Con(IsNull(Raster(snap_file)), tiffFile, tiffFile)
    temp.save(outputFile)

for k in arcpy.ListRasters("Focal", "TIF"):
    outputname_focal = k.replace("Focal", "SnapFocal", 1)
    temp = Con(IsNull(Raster(snap_file)), k, k)
    temp.save(outputname_focal)
    arcpy.BuildPyramids_management(outputname_focal)



####
# Population Density 
####
arcpy.ClearEnvironment("snapRaster")
arcpy.ClearEnvironment("cellSize")
arcpy.ClearEnvironment("extent")
env.workspace =  defaultPath + "\\gpw_v4_population_density"  
#Reproject to WGS84 
for tiffFile in arcpy.ListFiles("*gpw-v4-population-density*.tif"):
    tiffFileName = os.path.splitext(tiffFile)[0]
    outputFile = "Reprojected_" + tiffFileName + ".tif"
    arcpy.ProjectRaster_management(tiffFile, outputFile,sr1)


############### Find the actual NoData layer ################
# If no data from any of the original raster, is met with an explanation from 
# the data quality layer, then we assume there is data >> derive the footprint of BBAP
count = 0 
for k in arcpy.ListFiles("*data-quality-indicators*.tif"):
    layer_temp = Con(IsNull(k), -9999, 2) #-9999 if null, 2 if not null
    if count == 0: 
        mask1 = Con(EqualTo(layer_temp, 2), 2, -9999) # 1 is null, 2 is not null
    else:
        mask1 = Con(EqualTo(layer_temp, 2), 2, mask1) # 2 propagates, 1 can be replaced by 2
    count = count + 1
# mask1.save("correctors.tif") # 2 value pixels mean that there are explanations 
# data_quality = "correctors.tif"

# Eliminate noData space with the data quality indicators 
data_quality = mask1 
data = "gpw-v4-population-density_2015.tif"
data_null = Con(IsNull(data), -9999, 2)  #-9999 is no data 2 is data 
mask2 = Con( EqualTo(data_quality, 2) & IsNull(data), 2, data_null ) #-9999 is no data 2 is data 
mask2.save("noData.tif") 

arcpy.ClearEnvironment("snapRaster")
arcpy.ClearEnvironment("cellSize")
arcpy.ClearEnvironment("extent")

for tiffFile in arcpy.ListFiles("noData*.tif"):
    tiffFileName = os.path.splitext(tiffFile)[0]
    outputFile = "Reprojected_" + tiffFileName + ".tif"
    arcpy.ProjectRaster_management(tiffFile, outputFile,sr1)

############### Find the actual NoData layer ################
corrector = Raster("rReprojected_noData.tif")

for tiffFile in arcpy.ListRasters("Reprojected*", "TIF"):   
    arcpy.ClearEnvironment("snapRaster")
    arcpy.ClearEnvironment("cellSize")
    arcpy.ClearEnvironment("extent")
    outputFile = tiffFile.replace("Reprojected", "raster", 1)
    print(outputFile)
    # If data quality layer says its water body, then we don't consider it a noData cell
    # Change population density to 0 
    # Remember to remain the original extent of the noData layer  
    temp2 = Con(IsNull(tiffFile) & EqualTo(corrector, 2), 0, tiffFile)
    #Snap the corrected population density raster to Jordan's grid 
    arcpy.env.snapRaster = Raster(jordanFolder + "2001.tif")
    arcpy.env.cellSize = Raster(jordanFolder + "2001.tif")
    arcpy.env.extent = Raster(jordanFolder + "2001.tif")
    temp = Con(IsNull(Raster(snap_file)), temp2, temp2)
    temp.save(outputFile)

######2001.tif#
# Jordan Dataraster(snap_file) Mask 
#######
env.workspace =  jordanFolder
for k in arcpy.ListFiles("2001.tif"):
    outputName = "raster_mask_" + k
    arcpy.CopyRaster_management(k, outputName)

##################################################################
########################### Create Mask ###############################
##################################################################

#Anything that is named raster_mask instead of raster, 
#gets to be used to compute the Master Mask 
env.workspace = defaultPath
arcpy.env.snapRaster = Raster(jordanFolder + "2001.tif")
arcpy.env.cellSize = Raster(jordanFolder + "2001.tif")
arcpy.env.extent = Raster(jordanFolder + "2001.tif")

masks_list =[]
for dirpath, dirnames, filenames in arcpy.da.Walk(defaultPath, topdown = True, datatype = "RasterDataset"):
    for filename in filenames:
        if (("raster_mask" in filename) or ("mask_raster" in filename)) :
            masks_list.append(os.path.join(dirpath, filename))

#Perform overlap analysis to examine the extent 
count = 0 
for k in masks_list:
    print(k, count)
    if count == 0: 
        k_int = Con(IsNull(k), -9999, k)
        mask1 = Con(EqualTo(k_int, -9999) , 0, 9999)
        print("count == 0")
    else:
        try:
            k_int = Con(IsNull(k), -9999, k)
            mask1 = Con(EqualTo(k_int, -9999), count, mask1)
            # mask1.save(str(count)+ "_t3.tif") 
            # arcpy.BuildPyramids_management(str(count)+ ".tif")
        except Exception, e:
            pass
            print(e)
        print("count != 0", count)
    count = count + 1
mask1.save("master_mask.tif")


#Apply mask 
arcpy.env.snapRaster = Raster(jordanFolder + "2001.tif")
arcpy.env.cellSize = Raster(jordanFolder + "2001.tif")
arcpy.env.extent = Raster(jordanFolder + "2001.tif")

mask = defaultPath + "\\master_mask.tif"
# List all the data rasters to be applied with the master mask 
rasters_list =[]
for dirpath, dirnames, filenames in arcpy.da.Walk(defaultPath, topdown = True, datatype = "RasterDataset"):
    for filename in filenames:
        # Anything that says raster_* or mask_raster_* or raster_mask*
        if ("raster_" in filename) and (".tif" in filename) and ("interm" not in filename) and ("noData" not in filename):
            print(dirpath,filename)
            rasters_list.append(os.path.join(dirpath, filename))

#Since Jordan's data is the template for our snapping grid, there is no
#Processing being done to Jordan, and all Jordan's data starts with 20**
#Need to separately add Jordan's data 
for dirpath, dirnames, filenames in arcpy.da.Walk(defaultPath, topdown = True, datatype = "RasterDataset"):
    # print(dirpath, dirnames, filenames)
    for filename in filenames:
        if ("Jordan" in dirpath) and (".tif" in filename) and ("mask" not in filename) :
            print(dirpath, filename)
            rasters_list.append(os.path.join(dirpath, filename))

#Apply the mask, and save with the "final_" prefix 
for k in rasters_list:
    print(k)
    try:
        outputname =　k.replace("raster_mask", "final", 1).replace("mask_raster", "final", 1).replace("raster", "final", 1).replace("Jordan\\","Jordan\\final_" , 1).replace("final_final", "final", 1)
        temp = Con(EqualTo(mask, 9999), Con(IsNull(k), -9999, k) , -9999)
        temp.save(outputname)
        arcpy.SetRasterProperties_management(outputname, "", "", "", "1 -9999", "")
        arcpy.BuildPyramids_management(outputname)
        print(outputname)
    except Exception, e:
        pass
        print(e)

##################################################################
########################### FILL IN DATA #########################
###########  DEAL WITH TEMPERATURE AND PRECIPITATION LAYER #######################
##################################################################
env.workspace =  defaultPath + "\\temp_pre"
mask = defaultPath + "\\master_mask.tif"

arcpy.env.snapRaster = Raster(jordanFolder + "2001.tif")
arcpy.env.cellSize = Raster(jordanFolder + "2001.tif")
arcpy.env.extent = Raster(jordanFolder + "2001.tif")


#Rename "final_" to "noFill_" since we need to fill in some boundary 
#temperature and precipitation data 
for k in arcpy.ListRasters("final*", "TIF"):   
    arcpy.Rename_management(k, k.replace("final", "noFill", 1))

#If master_mask says a cell has data, but temp/precipitation says no Data
#we deem the value to be FocalLayer1 (3 x 3 rectangle average)
#If FocalLayer1 is also null value, we use FocalLayer2 (7x7 rectangle average)
for k in arcpy.ListRasters("noFill*", "TIF"):
    print(k)
    outputname = k.replace("noFill", "final", 1)
    FocalName = k.replace("noFill", "SnapFocal1", 1)
    Focal2Name = k.replace("noFill", "SnapFocal2", 1)
    print(FocalName, Focal2Name, k, outputname)
    temp = Con( IsNull(k) & EqualTo(mask, 9999), Con(IsNull(FocalName), Focal2Name, FocalName) , k )    # temp = Con( IsNull(k) & EqualTo(mask, 9999), 0, 1) 
    temp.save(outputname)
    arcpy.BuildPyramids_management(outputname)
    print(outputname)
