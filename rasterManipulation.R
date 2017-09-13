# This is a file with code that manipulates raster data. Originally intended to manipulate images to be used with dinamica later on. 

# Libraries used
library(raster)
library(rasterVis)
library(rgdal) 

# These 3 libraries seem to be the best ones for dealing with raster files. I used their manuals as references for this entire script but specifically used that of the raster library

# Goal 1: Separating a piece of the map. Specifically a rectangle with all 4 countries for early testing of a model. 

# Science this file is on a repository, the working files will be on the desktop but their file paths can be changed. 
setwd("~/Desktop") 
initialImage <- raster("final_level1.tif") # Loading a tif file 
plot(initialImage) # Plotting the file
initialImage # Seeing the image properties

# So now that the initial image is loaded, we have to extract the part we want. For this section I will cut a small rectangle
# First we need to select the extent of the section wanted
extentWanted <- extent(-61.7844, -56.35492, -27.12773, -11.59093)
# Then a new image is created with the extent, as well as the projection(we know it because of the properties of the initial image)
newMap<- raster(crs = "+proj=longlat +datum=WGS84 +no_defs +ellps=WGS84 +towgs84=0", ext = extentWanted)
#Finally, we crop the section we want from the initial map
finalMap <- crop(initialImage,newMap)
