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
  if((file.exists("javascript.txt")) && ((file.size("javascript.txt")) > 0)) {
    if(!exists("dataset")){
      dataset <- data.table(read.table("javascript.txt"))
      #print(dataset)
    }else{
      data <-data.table(read.table("javascript.txt"))
      #print(data)
      #dataset <- merge(dataset, data)
      dataset <- rbind(dataset, data)
      #print(dataset)
    }
    
  }
  setwd(parent.folder)
}

setnames(dataset,old="V1",new="number")
setnames(dataset,old="V4",new="scripttypejavascriptfound")

# show data as table
#print(dataset)

# calc. average number of websites that use ember
dataset[,nrow(dataset)/max(number)]

# add a cumulative sum of how many websites were found
dataset[,count:=1]
dataset[,count:=cumsum(scripttypejavascriptfound)]

# plot this data
ggplot(dataset,aes(number,count)) + geom_line()

# interpret this data -> your job

