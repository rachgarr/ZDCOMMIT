library(sf)
library(sp)
library(tidyr)
library(raster)
library(RPostgreSQL)

#add ADD

#Read data
setwd('/nfs/supplychaincommitments-data')

#Import South America Boundary
#SA_sf <- st_read(dsn='SouthAmerica','SouthAmerica')

#Import State Boundary Files
BRstate_sf <- st_read(dsn='Admin','BRA_adm1')
#ARstate_sf <- st_read(dsn='Admin','ARG_adm1')
#PRstate_sf <- st_read(dsn='Admin','PRY_adm1')
#BOstate_sf <- st_read(dsn='Admin','BOL_adm1')

st_bbox(BRstate_sf) #get extent/boundaries of BRstate boundaries
plot(BRstate_sf$geometry) #plot BRstate boundaries

#BRARstate_sf=aggregate(BRstate_sf,ARstate_sf)
#plot(BRARstate_sf$geometry) #plotting spatial data

#Import Biomes Boundaries
BRbiome_sf <- st_read(dsn="Biomes","Brazil_Biomes")
plot(BRbiome_sf$geometry) #plotting spatial data
#SAbiome_sf <- st_read(dsn="Biomes","tnc_terr_ecoregions")


#Joined biomes to administrative units
BRadmin_intersects_list <- st_intersects(x=BRadmin_sf,y=biome_sf) #getting identifier of overlapping biomes
BRadmin_biomes_combined <-do.call("rbind",BRadmin_intersects_list)
#Lost 5 munis, why????? there should have been perfect overlap between biome map and admin map

names(biome_sf)
biome_sf
plot(biome_sf,add=T,col="red")
BRadmin_sf <- st_read(dsn='Admin','BRA_adm2')


Trade<-read.csv("big5trade-1_updated.csv")
Trade_df=data.frame(Trade)

ADMTrade=Trade_df[which(Trade_df$EXPORTER=="ADM"),]
CargillTrade=Trade_df[which(Trade_df$EXPORTER=="CARGILL"),]

gather(ADMTrade,)

Production<-read.csv("/Non-GIS.Data/stateproduction.csv")
Regulations<-read.csv("/Non-GIS.Data/regulations.csv")

BRstate_trade_sf=merge(x=BRstate_sf,y=Trade_df,by="HASC_1")


BR_Production_State

#Check projections
st_crs(biome_sf)
st_crs(BRadmin_sf)
summary(BRadmin_sf)
BRadmin_sf


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


#Load data into PostgreSQL from ESRI shape file 
##Connect
con <- dbConnect(PostgreSQL(), dbname = 'supplychaincommitments',user='supplychaincommitments',password='34gj36fd', host = 'sesync-postgis01.research.sesync.org')

#
psql -h sesync-postgis01.research.sesync.org -d supplychaincommitments -U supplychaincommitments

##Here we are reading in the shapefile data into the database 
#sqlcommand=c("shp2pgsql -s 4326 -c -I /nfs/supplychaincommitments-data/GIS.Data/Admin/BRA_adm1.shp AdminUnits | psql -U supplychaincommitments -d supplychaincommitments")

sqlcommand=c("shp2pgsql -s 4326 /nfs/supplychaincommitments-data/GIS.Data/Admin/BRA_adm1.shp AdminUnits")

##Access the database
dbSendQuery(con,sqlcommand)


Do above in one step
shp2pgsql -s 4326 neighborhoods public.neighborhoods | psql -h myserver -d mydb -U myuser

Load data into PostgreSQL from ESRI shape file MA stateplane feet to geography
shp2pgsql -G -s 2249:4326 neighborhoods public.neighborhoods > neighborhoods_geog.sql
psql -h myserver -d mydb -U myuser -f neighborhoods_geog.sql

Sample linux sh script to load tiger 2007 massachusetts edges and landmark points
TMPDIR="/gis_data/staging"
STATEDIR="/gis_data/25_MASSACHUSETTS"
STATESCHEMA="ma"
DB="tiger"
USER_NAME="tigeruser"
cd $STATEDIR
#unzip files into temp directory
for z in */*.zip; do unzip -o -d $TMPDIR $z; done 
for z in *.zip; do unzip -o -d $TMPDIR $z; done


#loop thru pointlm and edges county tables and append to respective ma.pointlm ma.edges tables
for t in pointlm edges;
do
for z in *${t}.dbf;
do 
shp2pgsql  -s 4269 -g the_geom_4269 -S -W "latin1" -a $z ${STATE_SCHEMA}.${t} | psql -d $DB -U $USER_NAME;  
done
done

# disconnect from the PostgreSQL server
#dbDisconnect(con)

