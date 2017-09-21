# This file is meant to have all the code used to prepare the raster files used for the initial test of a land use model in dinamica
# It uses the same functions and idea outlined in the rasterManipulation.R file, which outlines more of what each step is doing.
# This file simply just uses those ideas and works with the many files we need

# Libraries used
library(raster)
library(rasterVis)
library(rgdal) 

# Extent wanted for all from the bigger files
extentWanted <- extent(-65, -58, -25, -10)

# Changing the working directory to dropbox
setwd("~/Dropbox/SESYNC GIS Database") 

# The layers needed are: admin level 2, TNC ecoregions, Brazil Biomes, temperature, precipitation, elevation, population, protected areas, distance to towns, distance to ports, distance to roads, distance to rivers
# We will need to load all of these 

initialAdmin2 <- raster(“filepath”) 
initialEcoregions <- raster(“filepath”) 
initialBrazilBiomes <- raster(“filepath”) 
initialTemperature <- raster(“filepath”) 
initialPrecipitation <- raster(“filepath”)
initialElevation <- raster(“filepath”) 
initialPopulation <- raster(“filepath”) 
initialProtectedAreas <- raster(“filepath”) 
initialTowns <- raster(“filepath”) 
initialPorts <- raster(“filepath”) 
initialRoads <- raster(“filepath”) 
initialRivers <- raster(“filepath”) 

# Then a new image is created with the extent, as well as the projection(the projection can be found in the properties of the initial images)
mapWanted<- raster(crs = "+proj=longlat +datum=WGS84 +no_defs +ellps=WGS84 +towgs84=0", ext = extentWanted)

# We then crop the initial maps with the map we generated
finalAdmin2 <- crop(initialAdmin2, mapWanted) 
finalEcoregions <- crop(initialEcoregions, mapWanted) 
finalBrazilBiomes <- crop(initialBrazilBiomes, mapWanted) 
finalTemperature <- crop(initialTemperature, mapWanted) 
finalPrecipitation <- crop(initialPrecipitation, mapWanted)
finalElevation <- crop(initialElevation, mapWanted) 
finalPopulation <- crop(initialPopulation, mapWanted) 
finalProtectedAreas <- crop(initialProtectedAreas, mapWanted) 
finalTowns <- crop(initialTowns, mapWanted) 
finalPorts <- crop(initialPorts, mapWanted) 
finalRoads <- crop(initialRoads, mapWanted) 
finalRivers <- crop(initialRivers, mapWanted) 
