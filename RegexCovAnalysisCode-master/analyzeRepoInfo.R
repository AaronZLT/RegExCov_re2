repoVisisted_path="/home/peipei/ISSTA2018/data/pom_byAPIVisit.csv"
repostarTest_path="/home/peipei/ISSTA2018/data/pom_starTest.csv"
repoSize_path="/home/peipei/ISSTA2018/data/pom_size.csv"
repoInfo_path="/home/peipei/ISSTA2018/data/regex/repo_regex.csv"

library(ggplot2)
library(reshape2)
library(dplyr)
setwd("/home/peipei/ISSTA/paper/figures")
repoPom=read.csv(file=repoVisisted_path,head=TRUE,colClasses=c("integer","integer","integer","integer","integer"),sep=",")
colnames(repoPom)=c("page","row","stars","watcher","size")
repoPom=as.data.frame(repoPom)
repoPom$id=paste(repoPom$page,repoPom$row,sep="_")

repoStarTests=read.csv(file=repostarTest_path,head=TRUE,colClasses=c("integer","integer","double","integer","integer","integer","integer"),sep=",")
colnames(repoStarTests)=c("page","row","tests","stars2","regexes","matches","xmls")
repoStarTests=as.data.frame(repoStarTests)
repoStarTests$id=paste(repoStarTests$page,repoStarTests$row,sep="_")

repoSize=read.csv(file=repoSize_path,head=TRUE,colClasses=c("integer","integer","integer"),sep=",")
colnames(repoSize)=c("page","row","loc")
repoSize=as.data.frame(repoSize)
repoSize$id=paste(repoSize$page,repoSize$row,sep="_")

repoInfo=repoPom[,c("page","row","stars","size")]
repoInfo$stars2=repoStarTests$stars2
repoInfo$tests=repoStarTests$tests
repoInfo$regexes=repoStarTests$regexes
repoInfo$loc=repoSize$loc


# repoInfo=read.csv(file=repoInfo_path,head=FALSE,colClasses=c("integer","integer","integer","integer"),sep=",")
# colnames(repoInfo)=c("page","row","total","count","failed") ##total inputs count of regex
# repoInfo=as.data.frame(repoInfo)
# repoInfo$id=paste(repoInfo$page,repoInfo$row,sep="_")

for (row in 1:nrow(repoPom)) {
  id=repoPom[row,"id"]
  repoPom[row,'loc']=repoSize[repoSize$id==id,"loc"]
  repoPom[row,'stars2']=repoStarTests[repoStarTests$id==id,"stars2"]
  repoPom[row,'tests']=repoStarTests[repoStarTests$id==id,"tests"]
}

repoPom=repoPom[,c("id","stars","tests","loc","size")]

for (row in 1:nrow(repoInfo)) {
  id=repoInfo[row,"id"]
  repoInfo[row,'stars']=repoPom[repoPom$id==id,"stars"]
  repoInfo[row,'tests']=repoPom[repoPom$id==id,"tests"]
  repoInfo[row,'loc']=repoPom[repoPom$id==id,"loc"]
  repoInfo[row,'size']=repoPom[repoPom$id==id,"size"]
}

# getSummary(repoInfo$total)
getSummary(repoInfo$stars)
getSummary(repoInfo$tests)
getSummary(repoInfo$loc)
getSummary(repoInfo$size)
getSummary(repoInfo$count)

repoInfo2=repoInfo[!repoInfo$id %in% dropped,]