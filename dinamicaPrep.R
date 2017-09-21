# This file is meant to have all the code used to prepare the raster files used for the initial test of a land use model in dinamica
# It uses the same functions and idea outlined in the rasterManipulation.R file, which outlines more of what each step is doing.
# This file simply just uses those ideas and works with the many files we need

# Libraries used
library(raster)
library(rasterVis)
library(rgdal) 

# Extent wanted for all from the bigger files
extentWanted <- extent(-61.7844, -56.35492, -27.12773, -11.59093)

# Changing the working directory to dropbox
setwd("~/Dropbox/SESYNC GIS Database") 
initialImage <- raster("Admin/final_level1.tif") # Loading a tif file 
plot(initialImage) # Plotting the file
initialImage # Seeing the image properties








extentForCrop <- extent(-65, -58, -25, -10)
# I will then crop this out of the 2 maps I am going to use
initial2012Image <- raster("Land_Use_Class/final_2012.tif") # Loading a tif file 
initial2013Image <- raster("Land_Use_Class/final_2013.tif") # Loading a tif file 

# Then a new image is created with the extent, as well as the projection(we know it because of the properties of the initial image)
newMap<- raster(crs = "+proj=longlat +datum=WGS84 +no_defs +ellps=WGS84 +towgs84=0", ext = extentWanted)
#Finally, we crop the section we want from the initial map
finalMap <- crop(initialImage,newMap)
