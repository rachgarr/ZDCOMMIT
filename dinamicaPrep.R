# This file is meant to have all the code used to prepare the raster files used for the initial test of a land use model in dinamica
# It uses the same functions and idea outlined in the rasterManipulation.R file, which outlines more of what each step is doing.
# This file simply just uses those ideas and works with the many files we need

# Libraries used
library(raster) 
library(rasterVis)
library(rgdal) 

# Extent wanted for all from the bigger files
extentWanted <- extent(-65, -58, -25, -10)

# Changing the working directory to dropbox. This command works differently for mac and windows so use the correct one
# Windows 
# setwd("C:/Users/rodri/Dropbox/SESYNC GIS Database/")
# Mac
setwd("~/Dropbox/SESYNC GIS Database/") 
# The layers needed are: admin level 2, TNC ecoregions, Brazil Biomes, temperature, precipitation, elevation, population, protected areas, distance to towns, distance to ports, distance to roads, distance to rivers

# We will need to load all of these 
initialAdmin2 <- raster("Admin/final_level2.tif")
initialEcoregions <- raster("Biomes/final_tnc_terr_ecoregions.tif")
initialBrazilBiomes <- raster("Biomes/final_Brazil_Biomes.tif")
initialTemperature <- raster("BiophysicalData/Temp_Precipitation/final_air.mon.ltm.v401.tif")
initialPrecipitation <- raster("BiophysicalData/Temp_Precipitation/final_precip.mon.ltm.v401.tif")
initialSlope <- raster("BiophysicalData/SRTMv4.1/final_Slope.tif")
initialElevation <- raster("BiophysicalData/SRTMv4.1/final_Elevation.tif")
initialPopulation <- raster("Population/final-v4-population-density_2010.tif")
initialProtectedAreas <- raster("Protected_Area/WDPA_Protected/final_WDPA_Sept2016-shapefile-polygons.tif")
initialTowns <- raster("Towns_Population/towns/final_POP_MAX__Towns_over50k.tif")
initialPorts <- raster("transport data/Ports/final_Ports.tif")
initialRoads <- raster("transport data/Roads_DigitalCharts/final_Merged_Roads_major.tif")
initialRivers <- raster("transport data/sa_riv_30s/final_sa_riv_30.tif")

# Then a new image is created with the extent, as well as the projection(the projection can be found in the properties of the initial images)
mapWanted<- raster(crs = "+proj=longlat +datum=WGS84 +no_defs +ellps=WGS84 +towgs84=0", ext = extentWanted)

# We then crop the initial maps with the map we generated
finalAdmin2 <- crop(initialAdmin2, mapWanted) 
finalEcoregions <- crop(initialEcoregions, mapWanted)
finalBrazilBiomes <- crop(initialBrazilBiomes, mapWanted)
finalTemperature <- crop(initialTemperature, mapWanted)
finalPrecipitation <- crop(initialPrecipitation, mapWanted)
finalSlope <- crop(initialSlope, mapWanted)
finalElevation <- crop(initialElevation, mapWanted)
finalPopulation <- crop(initialPopulation, mapWanted)
finalProtectedAreas <- crop(initialProtectedAreas, mapWanted)
finalTowns <- crop(initialTowns, mapWanted)
finalPorts <- crop(initialPorts, mapWanted)
finalRoads <- crop(initialRoads, mapWanted)
finalRivers <- crop(initialRivers, mapWanted)

# Finally they get written out - using INT2S for categorical and integer continuous variables, and FLT4S for non-integer continuous variables
writeRaster(finalAdmin2, filename = "dinamicaMaps/finalAdmin2.tif", datatype = "INT2S", format = "GTiff",overwrite=TRUE)
writeRaster(finalEcoregions, filename = "dinamicaMaps/finalEcoregions.tif", datatype = "INT2S", format = "GTiff",overwrite=TRUE)
writeRaster(finalBrazilBiomes, filename = "dinamicaMaps/finalBrazilBiomes.tif", datatype = "INT2S", format = "GTiff",overwrite=TRUE)
writeRaster(finalTemperature, filename = "dinamicaMaps/finalTemperature.tif", datatype = "FLT4S", format = "GTiff",overwrite=TRUE)
writeRaster(finalPrecipitation, filename = "dinamicaMaps/finalPrecipitation.tif", datatype = "FLT4S", format = "GTiff",overwrite=TRUE)
writeRaster(finalSlope, filename = "dinamicaMaps/finalSlope.tif", datatype = "FLT4S", format = "GTiff",overwrite=TRUE)
writeRaster(finalElevation, filename = "dinamicaMaps/finalElevation.tif", datatype = "FLT4S", format = "GTiff",overwrite=TRUE)
writeRaster(finalPopulation, filename = "dinamicaMaps/finalPopulation.tif", datatype = "INT2S", format = "GTiff",overwrite=TRUE)
writeRaster(finalProtectedAreas, filename = "dinamicaMaps/finalProtectedAreas.tif", datatype = "INT2S", format = "GTiff",overwrite=TRUE)
writeRaster(finalTowns, filename = "dinamicaMaps/finalTowns.tif", datatype = "INT2S", format = "GTiff",overwrite=TRUE)
writeRaster(finalPorts, filename = "dinamicaMaps/finalPorts.tif", datatype = "INT2S", format = "GTiff",overwrite=TRUE)
writeRaster(finalRoads, filename = "dinamicaMaps/finalRoads.tif", datatype = "INT2S", format = "GTiff",overwrite=TRUE)
writeRaster(finalRivers, filename = "dinamicaMaps/finalRivers.tif", datatype = "INT2S", format = "GTiff",overwrite=TRUE)
