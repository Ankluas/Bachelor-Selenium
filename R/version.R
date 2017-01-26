# at first use, you'll need to install these packages:
# install.packages("ggplot2")
# install.packages("data.table")
# install.packages("foreach")

library(ggplot2)
library(data.table)
library(foreach)

# get all sub folder of parent folder
sub.folders <- list.dirs("E:/Eigene Dateien/results/runx", recursive=TRUE)

# filename=paste(file,"??.txt",sep="/") - ersetze ?? mit name.txt
dt <- foreach(file=sub.folders, .combine=rbind, .errorhandling='remove') %do% {
  filename=paste(file,"jQueryList.txt",sep="/")
  if(file.exists(filename) && ((file.size(filename)) > 0) ) {
    print(filename)
    data.table(read.table(filename, fill=TRUE))
  }
}

dataset=dt

setnames(dataset,old="V1",new="number")
setnames(dataset,old="V2",new="found")

dataset[,number:=as.numeric(as.character(number))]
dataset <- dataset[!is.na(number)]

# führe das auf Spalte V9 deines datasets aus, nachdem die For Schleife
dataset[,V9:=gsub("'>", "", gsub("match='", "", V9))]

# erstes element pro website
dt2 <- dataset[,list(version=V9[1]),by=V10]

# zähle anzahl websiten pro versions nummer
dt3 <- dt2[,list(count=length(V10)),by=version]

# sortiert dt3 mit index version (kleinste Version oben, groesste unten)
setkey(dt3,version)

# jQuery: wähle nur die aus, welche count weniger als 200 haben, und ersetze das Versionsfeld mit "so"
# cedexis: count<1
dt3[count<200,version:="so"]

# summiere counts auf, für jede version
dt4 <- dt3[,list(count=sum(count)),by=version]

# Histogramm
ggplot(dt4,aes(x=version,y=count)) +
  geom_bar(stat = "identity") + theme(axis.text.x
                                      = element_text(angle = 90, vjust = 0.5, hjust=1))



