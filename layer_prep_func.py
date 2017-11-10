
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

from SESYNC import * #That replaces everything above 


#check your environment settings 
environments = arcpy.ListEnvironments()
environments.sort
for environment in environments:
    print("{0:<30}: {1}".format(environment, arcpy.env[environment]))

def reproject(searchPhrase):
    try:
        for shpFile in arcpy.ListFiles(str(searchPhrase)):
            shpFileName = os.path.splitext(shpFile)[0]
            outputFile = "reprojected_" + shpFileName.replace('Merged_', '', 1) + ".shp"
            print(shpFileName)
            print(shpFile)
            print(outputFile)
            arcpy.Project_management(shpFile,outputFile,sr1)
    except Exception, e:
        pass
        print(e)
    return()

def addOne(field_name, searchPhrase):
    try:
        for k in arcpy.ListFiles("reprojected_*.shp"):
            arcpy.AddField_management(k, "FID2", "DOUBLE")
            fields = ['FID', 'FID2']
            count = 0 
            with arcpy.da.UpdateCursor(k, fields) as cursor: 
                for row in cursor: 
                    row[1] = row[0] + 1
                    cursor.updateRow(row)
    except Exception, e:
        pass
        print(e)    
    return()
    
def turnOnSettings():
    arcpy.env.snapRaster = Raster(jordanFolder + "2001.tif")
    arcpy.env.cellSize = Raster(jordanFolder + "2001.tif")
    arcpy.env.extent = Raster(jordanFolder + "2001.tif")
    print("turn on settings")
    return()

def turnOffSettings():
    arcpy.ClearEnvironment("snapRaster")
    arcpy.ClearEnvironment("cellSize")
    arcpy.ClearEnvironment("extent")
    print("turn off settings")
    return()

def convertPointToRaster(searchPhrase, outFIDtag, outname):
    try:
        for shpFile in arcpy.ListFiles(searchPhrase):
            shpFileName = os.path.splitext(shpFile)[0]
            print(shpFileName)
            print(shpFile)
            outputFile = shpFileName.replace('reprojected_', outname, 1) + ".tif" 
            if outFIDtag == 1: 
                outputFile = shpFileName.replace('reprojected_', outname + field_name  +"_", 1) + ".tif" 
            print(outputFile)
            arcpy.FeatureToRaster_conversion(shpFile, field_name, outputFile)
    except Exception, e:
        pass
        print(e)
    return()

def snapRaster(searchPhrase, replace, replaceby):
    try:
        for tiffFile in arcpy.ListRasters(searchPhrase, "TIF"):   
            outputFile = tiffFile.replace(replace, replaceby, 1)
            print(outputFile)
            temp = Con(IsNull(Raster(snap_file)), tiffFile, tiffFile)
            temp.save(outputFile)
    except Exception, e:
        pass
        print(e)    
    return()

##################################################################
####################### POINT VECTORS WITH FID############################
##################################################################

####
#Ports
####

env.workspace =  defaultPath + "\\Ports"
turnOffSettings()
#Merge points from individual countries 
port_list = arcpy.ListFiles("*.shp")
arcpy.Merge_management(port_list, "Merged_Ports.shp")
#Reproject to WGS84 
reproject("Merged*.shp")
field_name = str("FID2")
#Add 1 to all FID
addOne(field_name, "reprojected_*.shp")
#Convert to raster
turnOnSettings()
convertPointToRaster("reprojected_*.shp", 0, "interm_")


####
#Fridges
####
turnOffSettings()
env.workspace =  defaultPath + "\\Fridges" 
fridge_list = arcpy.ListFiles("*.shp")
arcpy.Merge_management(fridge_list, "Merged_Fridges.shp")
reproject("Merged*.shp")
field_name = str("FID2")
#Add 1 to all FID
addOne(field_name, "reprojected_*.shp")
#Convert to raster
turnOnSettings()
convertPointToRaster("reprojected_*.shp", 0, "interm_")



####
#Processing Facilities
####
turnOffSettings()
env.workspace =  defaultPath + "\\Processing Facilities" 

fridge_list = arcpy.ListFiles("*.shp")
arcpy.Merge_management(fridge_list, "Merged_Processing.shp")

reproject("Merged*.shp")
field_name = str("FID2")
#Add 1 to all FID
addOne(field_name, "reprojected_*.shp")
#Convert to raster
turnOnSettings()
convertPointToRaster("reprojected_*.shp", 0, "interm_")

##################################################################
####################### POINT VECTORS WITHOUT FID############################
##################################################################

####
# Towns 
####
env.workspace =  defaultPath + "\\Towns" 
turnOffSettings()
town_50k_list = arcpy.ListFiles("*over50k*.shp")
town_10k_list= arcpy.ListFiles("*over10k*.shp")
arcpy.CopyFeatures_management("Towns.shp", "Merged_Towns_over0k.shp")
arcpy.Merge_management(town_50k_list, "Merged_Towns_over50k.shp")
arcpy.Merge_management(town_10k_list, "Merged_Towns_over10k.shp")

reproject("Merged*.shp")

turnOnSettings()


field_name = str("POP_MAX")
convertPointToRaster("reprojected_*.shp", 1)

field_name = str("POP_MIN")
convertPointToRaster("reprojected_*.shp", 1)


############
#Set noData to 9999 
# Change Null Value to 0, Change all 0 value to -9999 as the NoData Value 
############
env.workspace =  defaultPath  
rasters_list =[]
for dirpath, dirnames, filenames in arcpy.da.Walk(defaultPath, topdown = True, datatype = "RasterDataset"):
    for filename in filenames:
        if ("interm_" in filename) :
            rasters_list.append(os.path.join(dirpath, filename))
            print(os.path.join(dirpath, filename))

for k in rasters_list:
    OutRaster = Con(IsNull(k), 0, k) #Change all NoData values to 0
    Final = Con(EqualTo(OutRaster, 0), -9999, OutRaster) #Change all 0 values to 9999
    output_file = k.replace("interm_", "raster_", 1) 
    Final.save(FinalRaster_Name)

##################################################################
################LINES AND POLYGONS ###############################
##################################################################
#####
# WDPA Protected 
#####
## Problem: reprojection to WGS84 gives us weird things 
## Solution: ignore the projection step and convert it right away 
turnOffSettings()
env.workspace =  defaultPath + "\\WDPA_Protected" 
field_name= str('WDPAID')
turnOnSettings()
for shpFile in arcpy.ListFiles("*.shp"):
    shpFileName = os.path.splitext(shpFile)[0]
    outputFile = 'raster_' + shpFileName + ".tif" 
    print(shpFileName, shpFile, outputFile)
    arcpy.FeatureToRaster_conversion(shpFile, field_name, outputFile)

#####
#Biomes 
#####
turnOffSettings()
env.workspace =  defaultPath + "\\Biomes"  
field_name = str("FID2")
reproject("*.shp")
turnOnSettings()

addOne(field_name, "reprojected_*.shp")
for shpFile in arcpy.ListFiles("reprojected_*.shp"):
    shpFileName = os.path.splitext(shpFile)[0]
    print(shpFileName, shpFile)
    if "tnc" in str(shpFileName):
        outputFile = shpFileName.replace('reprojected_', 'raster_mask_', 1) + ".tif" 
    else:
        outputFile = shpFileName.replace('reprojected_', 'raster_', 1) + ".tif" 
    print(outputFile)
    arcpy.FeatureToRaster_conversion(shpFile, field_name, outputFile)



#####
# River 
#####
turnOffSettings()
env.workspace =  defaultPath + "\\sa_riv_30s" ### REDO 
field_name = str("UP_CELLS")
reproject("*.shp")
turnOnSettings()

for shpFile in arcpy.ListFiles("reprojected_*.shp"):
    shpFileName = os.path.splitext(shpFile)[0]
    outputFile = shpFileName.replace('reprojected_', 'raster_', 1) + ".tif" 
    print(shpFileName, shpFile, outputFile)
    arcpy.FeatureToRaster_conversion(shpFile, field_name, outputFile)


####
# Roads (OpenStreetMap) 
####
turnOffSettings()
env.workspace =  defaultPath + "\\Roads" 
OpenStreet_list = arcpy.ListFiles("*exp*.shp")
arcpy.CopyFeatures_management("Roads.shp", "Merged_Roads_minor.shp")
arcpy.CopyFeatures_management("Roads_GRI.shp", "Merged_Roads_major.shp")
arcpy.Merge_management(OpenStreet_list, "Merged_Roads_pave.shp")
reproject("Merged*.shp")
turnOnSettings()
addOne(field_name, "reprojected_*.shp")

for shpFile in arcpy.ListFiles("reprojected_*.shp"):
    shpFileName = os.path.splitext(shpFile)[0]
    outputFile = shpFileName.replace('reprojected_', 'raster_', 1) + ".tif" 
    print(shpFileName, shpFile, outputFile)
    if 'pave' in shpFileName:
        field_name = 'paved'
    elif ('major' in shpFileName) or ('minor' in shpFileName):
        field_name = 'FID'
    arcpy.FeatureToRaster_conversion(shpFile, field_name, outputFile)

####
# Admin 
####
turnOffSettings()
env.workspace =  defaultPath + "\\Admin" 
for i in range(0, 4):
    holder = "*adm" + str(i) + "*.shp" 
    outputname = "level" + str(i) + ".shp"
    print(holder)
    listfile= arcpy.ListFiles(holder)
    print(listfile)
    arcpy.Merge_management(listfile, outputname)

field_name= str('FID')
reproject("level*.shp")
turnOnSettings()
for shpFile in arcpy.ListFiles("reprojected_*.shp"):
    shpFileName = os.path.splitext(shpFile)[0]
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
turnOffSettings()
raster_list = arcpy.ListRasters("srtm_*", "TIF")
arcpy.MosaicToNewRaster_management(raster_list, defaultPath + "\\SRTMv4.1\\" , "Mosaic_Elevation.tif", number_of_bands = 1 )

arcpy.Clip_management(Raster("Mosaic_Elevation.tif"),"#","interm_Elevation.tif", Raster( jordanFolder + "2001.tif") ,-9999,"NONE","MAINTAIN_EXTENT")
sr_robinson = arcpy.SpatialReference(54030)

#This is oftentime problematic, thus we run it twice 
arcpy.ProjectRaster_management("interm_Elevation.tif", "Robinson_Elevation.tif", sr_robinson, in_coor_system = sr1)
arcpy.ProjectRaster_management("interm_Elevation.tif", "Robinson_Elevation.tif", sr_robinson, in_coor_system = sr1)

#Calculate Slope in projected coordinate system 
turnOffSettings()
arcpy.Slope_3d("Robinson_Elevation.tif" , "Slope_Robinson.tif", "DEGREE", "1")
arcpy.ProjectRaster_management("Slope_Robinson.tif", "interm_Slope.tif", sr1)

# Finally, snap to the grid for Jordan's data 
turnOnSettings()

snapRaster("*interm_*","interm_", "raster_")


####
# Make NetCDF RasterLayer for precipitation and temperature 
####
turnOffSettings()
env.workspace =  defaultPath + "\\temp_pre"
for shpFile in arcpy.ListFiles("*.nc"):
    shpFileName = os.path.splitext(shpFile)[0]
    outputFile = "Reprojected_" + shpFileName.replace('.nc', '', 1) + '.tif' 
    print(shpFileName)
    print(shpFile)
    print(outputFile)
    if "air" in str(shpFileName):
        arcpy.MakeNetCDFRasterLayer_md(shpFile, "air", "lon", "lat", "output")
        arcpy.ProjectRaster_management(tiffFile, outputFile,sr1)
    elif "precip" in str(shpFileName): 
        arcpy.MakeNetCDFRasterLayer_md(shpFile, "precip", "lon", "lat", "output")
        arcpy.ProjectRaster_management("output", outputFile,sr1)

turnOnSettings()

for tiffFile in arcpy.ListRasters("Reprojected*", "TIF"):
    outputFile = tiffFile.replace("Reprojected", "Clipped", 1)
    print(outputFile)
    arcpy.Clip_management(tiffFile, "#",outputFile, Raster( jordanFolder + "2001.tif"), -9999,"NONE", "MAINTAIN_EXTENT")

snapRaster("Clipped*","Clipped_", "raster_mask_")



####
# Population Density 
####
turnOffSettings()
env.workspace =  defaultPath + "\\gpw_v4_population_density"  
for tiffFile in arcpy.ListFiles("*gpw-v4-population-density*.tif"):
    tiffFileName = os.path.splitext(tiffFile)[0]
    outputFile = "Reprojected_" + tiffFileName + ".tif"
    arcpy.ProjectRaster_management(tiffFile, outputFile,sr1)
turnOnSettings()
snapRaster("Reprojected*","Reprojected", "raster")

# Footprint analysis 
# If no data from any of the original raster, is met with a value from 
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

# Eliminate noData space with the data quality indicators 
# data_quality = "correctors.tif"
data_quality = mask1 
data = "gpw-v4-population-density_2015.tif"
data_null = Con(IsNull(data), -9999, 2)  #-9999 is no data 2 is data 
mask2 = Con( EqualTo(data_quality, 2) & IsNull(data), 2, data_null ) #-9999 is no data 2 is data 
mask2.save("noData.tif")
turnOffSettings()
for tiffFile in arcpy.ListFiles("noData*.tif"):
    tiffFileName = os.path.splitext(tiffFile)[0]
    outputFile = "Reprojected_" + tiffFileName + ".tif"
    arcpy.ProjectRaster_management(tiffFile, outputFile,sr1)
turnOnSettings()
snapRaster("Reprojected_noData*", "Reprojected", "raster_mask")

######2001.tif#
# Jordan Dataraster(snap_file) Mask 
#######
env.workspace =  jordanFolder
for k in arcpy.ListFiles("2001.tif"):
    outputName = "raster_mask_" + k
    arcpy.CopyRaster_management(k, outputName)

#######
# Inspect noData coverage places 
####### 
env.workspace = defaultPath

#Python folder walker ### what is dirnames??? 
masks_list =[]
for dirpath, dirnames, filenames in arcpy.da.Walk(defaultPath, topdown = True, datatype = "RasterDataset"):
    for filename in filenames:
        if ("raster_mask" in filename) :
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
rasters_list =[]
for dirpath, dirnames, filenames in arcpy.da.Walk(defaultPath, topdown = True, datatype = "RasterDataset"):
    for filename in filenames:
        if ("raster_" in filename) and (".tif" in filename) and ("interm" not in filename):
            print(dirpath,filename)
            rasters_list.append(os.path.join(dirpath, filename))

for dirpath, dirnames, filenames in arcpy.da.Walk(defaultPath, topdown = True, datatype = "RasterDataset"):
    # print(dirpath, dirnames, filenames)
    for filename in filenames:
        if ("Jordan" in dirpath) and (".tif" in filename) and ("mask" not in filename):
            print(dirpath, filename)
            rasters_list.append(os.path.join(dirpath, filename))

count = 0 
for k in rasters_list:
    print(k)
    outputname =k.replace(".tif", "_final.tif", 1)
    temp = Con(EqualTo("master_mask.tif", 9999), Con(IsNull(k), -9999, k) , -9999)
    temp.save(outputname)
    arcpy.BuildPyramids_management(outputname)
    print(outputname)
    else:
        pass
    count +=1

#Fill in the void for temperature and precipitation 