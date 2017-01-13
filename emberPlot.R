# at first use, you'll need to install these packages:
#install.packages("ggplot2")
#install.packages("data.table")

library("ggplot2")
library("data.table")
# read data
parent.folder <- "E:/Eigene Dateien/results/runx/"
#print (parent.folder)
sub.folders <- list.dirs(parent.folder, recursive=TRUE)[-1]
#print (sub.folders)

for(i in sub.folders){
  setwd(i)
  # check whether txt exists and is empty or not, continue when existing and not empty
  if((file.exists("emberList.txt")) && ((file.size("emberList.txt")) > 0)) {
    x <- 4
    data <- data.table(read.table("emberList.txt"))
    setnames(data,old="V1",new="number")
    setnames(data,old="V2",new="found")
    
    # show data as table
    print(data)
    
    # calc. average number of websites that use jQuery
    data[,nrow(data)/max(number)]
    
    # add a cumulative sum of how many websites were found
    data[,count:=1]
    data[,count:=cumsum(count)]
    
    # plot this data
    ggplot(data,aes(number,count)) + geom_line()
    
  }
  setwd(parent.folder)
}


# interpret this data -> your job

