library(readxl)
BR_crops <- read_excel("C:/Users/rodri/Dropbox/SESYNC GIS Database/Non-GIS Files/Dbl_crop/BR_crops.xlsx")
setwd("C:/Users/rodri/Dropbox/SESYNC GIS Database/dinamica/Model's Data/rentModel/rents")
yearWanted <- 2012

columns <- colnames(BR_crops)
mysubset <- BR_crops[BR_crops$Year == yearWanted, c("Identifier", "soy_a", "soy_y", "soy_p")]
colnames(mysubset) <- c("ID", "soy_area", "soy_yield", "soy_price")
mysubset$soy_area<-gsub("-","0",mysubset$soy_area)
mysubset$soy_yield<-gsub("-","0",mysubset$soy_yield)
mysubset$soy_price<-gsub("-","0",mysubset$soy_price)
#mysubset$soy_area<-gsub("...","0",mysubset$soy_area)
#mysubset$soy_yield<-gsub("...","0",mysubset$soy_yield)
#mysubset$soy_price<-gsub("...","0",mysubset$soy_price)

alreadyInThere <- vector()
newSubset <- data.frame()

for ( i in 1:nrow(mysubset)){
  thisLine <- mysubset[i,]
  if (thisLine$ID %in% alreadyInThere == FALSE){
      alreadyInThere <- c(alreadyInThere, thisLine$ID)
      newSubset <- rbind(newSubset,thisLine)
  }
}
str(mysubset)
str(newSubset)
mysubset <- newSubset

setwd("C:/Users/rodri/Dropbox/SESYNC GIS Database/dinamica/Model's Data/rentModel/rents")
key <- read.table(file = "statesKey.csv", sep = ",", header = T)

alreadyInThere <- vector()
newKey <- data.frame()
thisLine <- vector()

for ( i in 1:nrow(key)){
  thisLine <- key[i,]
  thisMuni <- as.character(key[i,2])
  if (thisMuni %in% alreadyInThere == FALSE){
    alreadyInThere <- c(alreadyInThere, thisMuni)
    newKey <- rbind(newKey,thisLine)
  }
}

key<- newKey

finalSubset <- data.frame()

for ( i in 1:nrow(mysubset)){
  thisMuni <- as.character(mysubset[i,1])
  numberKey <- key[key$stateString == thisMuni, 1]
  thisLine <- mysubset[i,]
  if (length(numberKey) != 0){
    thisLine[1,"ID"] <- numberKey
    finalSubset <- rbind(finalSubset,thisLine)
  }
}

for ( i in 1:nrow(mysubset)){
  i <-3
  thisMuni <- as.character(mysubset[i,1])
  numberKey <- key[key$stateString == thisMuni, 1]
  thisLine <- mysubset[i,]
  if (length(numberKey) != 0){
    thisLine[1,"ID"] <- numberKey
    finalSubset <- rbind(finalSubset,thisLine)
  }
}



mysubset <- finalSubset

write.table(mysubset, file = "2012soy.csv", sep = ",", quote = FALSE, row.names = FALSE)


as.vec



