# This is a file with code that manipulates raster data. Originally intended to manipulate images to be used with dinamica later on. 

# Libraries used
library(raster)
library(rasterVis)
library(rgdal) 

# These 3 libraries seem to be the best ones for dealing with raster files. I used their manuals as references for this entire script but specifically used that of the raster library

# Goal 1: Separating a piece of the map. Specifically a rectangle with all 4 countries for early testing of a model. 

# Science this file is on a repository, the working files will be on the dropbox but their file paths can be changed. 
setwd("~/Dropbox/SESYNC GIS Database") 
initialImage <- raster("Admin/final_level1.tif") # Loading a tif file 
plot(initialImage) # Plotting the file
initialImage # Seeing the image properties

# So now that the initial image is loaded, we have to extract the part we want. For this section I will cut a small rectangle
# First we need to select the extent of the section wanted
extentWanted <- extent(-61.7844, -56.35492, -27.12773, -11.59093)
# Then a new image is created with the extent, as well as the projection(we know it because of the properties of the initial image)
newMap<- raster(crs = "+proj=longlat +datum=WGS84 +no_defs +ellps=WGS84 +towgs84=0", ext = extentWanted)
#Finally, we crop the section we want from the initial map
finalMap <- crop(initialImage,newMap)

# For the first step of the model, a cut is need from both a 2012 and a 2013 land use map, similar to what we did above. 
# I will first figure out a standard cut that will be taken out from all the images. In this case I will manially use the select function to see what it is best through trial and error
initialAdmin <- raster("Admin/final_level0.tif") 
plot(initialAdmin)
select(initialAdmin)
initialAdmin
# After seeing the many extents I selected, I have decided to go for (-65, -58, -25, -10), so I'll create the extent
extentForCrop <- extent(-65, -58, -25, -10)
# I will then crop this out of the 2 maps I am going to use
initial2012Image <- raster("Land_Use_Class/Jordan/final_2012.tif") # Loading a tif file 
initial2013Image <- raster("Land_Use_Class/Jordan/final_2013.tif") # Loading a tif file 

new2012Image <- crop(initial2012Image, extentForCrop)
new2013Image <- crop(initial2013Image, extentForCrop)

# Finally I will write them out to files in the correct format. Take not that R will default to a data type that is not what dinamica accepts, so you have to indicate what type you want.
writeRaster(new2012Image, filename = "cropped2012.tif", datatype = "INT2S", format = "GTiff",overwrite=TRUE)
writeRaster(new2013Image, filename = "cropped2013.tif", datatype = "INT2S", format = "GTiff",overwrite=TRUE)

# Just in case to check if they were written out correctly I will plot them, as well as seeing their properties and comparing them to the cropped ones
check2012 <- raster("dinamicaMaps/cropped2012.tif")
plot(check2012)
check2013 <- raster("dinamicaMaps/cropped2013.tif")
plot(check2013)
check2012
new2012Image
check2012
