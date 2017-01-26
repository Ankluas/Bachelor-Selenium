# at first use, you'll need to install these packages:
# install.packages("ggplot2")
# install.packages("data.table")
# install.packages("foreach")

library("ggplot2")
library("data.table")
library("foreach")

# get all sub folder of parent folder
sub.folders <- list.dirs("E:/Eigene Dateien/results/runx", recursive=TRUE)

dt <- foreach(file=sub.folders, .combine=rbind, .errorhandling='remove') %do% {
  filename=paste(file,"javascript.txt",sep="/")
  if(file.exists(filename) && ((file.size(filename)) > 0) ) {
    print(filename)
    data.table(read.table(filename, fill=TRUE))
  }
}

dataset=dt

setnames(dataset,old="V1",new="number")
setnames(dataset,old="V2",new="jscountIGNORE")
setnames(dataset,old="V3",new="scriptcount")
setnames(dataset,old="V4",new="jstype")
setnames(dataset,old="V5",new="srcextern")
setnames(dataset,old="V6",new="async")
setnames(dataset,old="V7",new="httpEinbindung")
setnames(dataset,old="V8",new="httpsEinbindung")

dataset[,number:=as.numeric(as.character(number))]
dataset <- dataset[!is.na(number)]

# calc. average number of websites
# sum(?) - ? abändern zu dem gewollten Wert in "new"
dataset[,sum(httpsEinbindung)/max(number)]

# add a cumulative sum of how many websites were found
# cumsum(?) - ? zu dem oberen Wert in "new" abändern
dataset[,count:=1]
dataset[,count:=cumsum(httpsEinbindung)]

dataset[number < 25000, name:= "01.) top 25k"]
dataset[number >= 25000 & number < 50000, name:= "02.) 25k-50k"]
dataset[number >= 50000 & number < 75000, name:= "03.) 50k-75k"]
dataset[number >= 75000 & number < 100000, name:= "04.) 75k-100k"]
dataset[number >= 100000 & number < 125000, name:= "05.) 100k-125k"]
dataset[number >= 125000 & number < 150000, name:= "06.) 125k-150k"]
dataset[number >= 150000 & number < 175000, name:= "07.) 150k-175k"]
dataset[number >= 175000 & number < 200000, name:= "08.) 175k-200k"]
dataset[number >= 200000 & number < 225000, name:= "09.) 200k-225k"]
dataset[number >= 225000 & number < 250000, name:= "10.) 225k-250k"]
dataset[number >= 250000 & number < 275000, name:= "11.) 250k-275k"]
dataset[number >= 275000 & number < 300000, name:= "12.) 275k-300k"]
dataset[number >= 300000, name:= "13.) rest"]

# ??=mean(?) - ? zu dem oberen gewollten Wert ändern und ?? einen passenden Namen geben
dataset2 <- dataset[,list(https=mean(httpsEinbindung)),by=name]

# y=?? - ?? abändern zu dem passenden Namen
ggplot(dataset2,aes(x=name,y=https)) +
  geom_bar(stat = "identity") + theme(axis.text.x
                                      = element_text(angle = 90, vjust = 0.5, hjust=1))

