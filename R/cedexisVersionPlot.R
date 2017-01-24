# at first use, you'll need to install these packages:
#install.packages("ggplot2")
#install.packages("data.table")

library("ggplot2")
library("data.table")

# set parent folder
parent.folder <- "E:/Eigene Dateien/results/runx"

# get all sub folder of parent folder
sub.folders <- list.dirs(parent.folder, recursive=TRUE)

for(i in sub.folders){
  setwd(i)
  # check whether txt data exists and is empty or not, continue when existing and not empty
  if((file.exists("cedexisList.txt")) && ((file.size("cedexisList.txt")) > 0)) {
    if(!exists("dataset")){
      dataset <- data.table(read.table("cedexisList.txt"))
      print(dataset)
    }else{
      data <-data.table(read.table("cedexisList.txt"))
      print(data)
      #dataset <- merge(dataset, data)
      dataset <- rbind(dataset, data)
      print(dataset)
    }
    
  }
  setwd(parent.folder)
}


colnames(dt)

# führe das auf Spalte V9 deines datasets aus, nachdem die For Schleife durchgelaufen ist
dataset[,V9:=gsub("'>", "", gsub("match='", "", V9))]

# erstes element pro website
dt2 <- dataset[,list(version=V9[1]),by=V10]

# zähle anzahl websiten pro versions nummer
dt3 <- dt2[,list(count=length(V10)),by=version]

setkey(dt3,version)
#42% wären älter als März 2012
8/nrow(dt2)

# wähle nur die aus mit count=1, und ersetze das Versions feld mit "so"
dt3[count==1,version:="so"]

# summiere counts auf, für jede version
dt4 <- dt3[,list(count=sum(count)),by=version] 

#
ggplot(dt4,aes(x=version,y=count)) +
  geom_bar(stat = "identity") + theme(axis.text.x
                                      = element_text(angle = 90, vjust = 0.5, hjust=1))

