library(sf)
library(raster)
library(RPostgreSQL)

#add ADD

#Read data
setwd('/nfs/supplychaincommitments-data/GIS.Data/')

#Import South America Boundary
SA_sf <- st_read(dsn='SouthAmerica','SouthAmerica')

#Import State Boundary Files
BRstate_sf <- st_read(dsn='Admin','BRA_adm1')
ARstate_sf <- st_read(dsn='Admin','ARG_adm1')
PRstate_sf <- st_read(dsn='Admin','PRY_adm1')
BOstate_sf <- st_read(dsn='Admin','BOL_adm1')

st_bbox(BRstate_sf) #get extent/boundaries of BRstate boundaries
plot(BRstate_sf$geometry) #plot BRstate boundaries
plot(ARstate_sf$geometry) #plot BRstate boundaries


BRARstate_sf=aggregate(BRstate_sf,ARstate_sf)
plot(BRARstate_sf$geometry) #plotting spatial data
BRARstate_sf=st_union(BRstate_sf,ARstate_sf)
BRARstate_sf=st_union(BRstate_sf,ARstate_sf)

#Import Biomes Boundaries
BRbiome_sf <- st_read(dsn="Biomes","Brazil_Biomes")
SAbiome_sf <- st_read(dsn="Biomes","tnc_terr_ecoregions")

plot(BRbiome_sf$geometry) #plotting spatial data
plot(SAbiome_sf$geometry) #plotting spatial data

names(biome_sf)
biome_sf
plot(biome_sf,add=T,col="red")
BRadmin_sf <- st_read(dsn='Admin','BRA_adm2')


Trade<-read.csv("big5trade-1_updated.csv")

BRstate_trade_sf=merge(x=BRstate_sf,y=Trade)

Trade<-read.csv("big5trade-1.csv")

#Check projections
st_crs(biome_sf)
st_crs(BRadmin_sf)
summary(BRadmin_sf)
BRadmin_sf

#Joined biomes to administrative units
BRadmin_intersects_list <- st_intersects(x=BRadmin_sf,y=biome_sf) #getting identifier of overlapping biomes
BRadmin_biomes_combined <-do.call("rbind",BRadmin_intersects_list)
#Lost 5 munis, why????? there should have been perfect overlap between biome map and admin map

dim(BRadmin_biomes_combined)

#How to change projection for shapefile if necessary
st_transform(BRadmin_sf,crs="+proj=longlat +datum=WGS84 +no_defs")

#1) for each administrative unit, find out overlapping biomes
#2) select biomes and adminstrative unit st_intersects
#3) st_area

#Dataframe that has each row here (munis, sometimes duplicates), then 
#calculate area, then add column, then reshape long to wide

BRadmin_intersection_sf <- st_intersection(x=BRadmin_sf,y=biome_sf) #getting identifier of overlapping biomes
class(BRadmin_intersection_sf)
BRadmin_intersection_sf
st_area(BRadmin_intersection_sf[1,])

st_intersects()

