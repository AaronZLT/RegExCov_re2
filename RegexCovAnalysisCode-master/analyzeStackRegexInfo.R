library(ggplot2)
library(reshape2)
library(dplyr)
setwd("/home/peipei/ISSTA/paper/figures")

regexStack_path="/home/peipei/ISSTA2018/data/regex/stack_info.csv"
regexStackInfo=read.csv(file=regexStack_path,head=FALSE,colClasses=c("integer","integer","integer","integer","integer","integer","integer","integer","integer","integer","integer","integer"),sep=",")
colnames(regexStackInfo)=c("stackindex","regexindex","page","row","nodes","edges","epairs","totalInputs","uniInputs","succ","failed","dropped")
regexStackInfo=as.data.frame(regexStackInfo)

getSummary=function(data){
  print(mean(data))
  print(min(data))
  print(max(data))
  quantile(data, c(0.1,0.25,0.5,0.75,0.9,0.95,0.98,0.99))
}

callSite_path="/home/peipei/ISSTA2018/data/regex/callsite_regex"
callSitekInfo=read.csv(file=callSite_path,head=FALSE,colClasses="integer",sep=",")
getSummary(callSitekInfo$V1)

repoTestCallSite_path="/home/peipei/ISSTA2018/data/regex/callsite_tested"
repoTestCallSite=read.csv(file=repoTestCallSite_path,head=FALSE,colClasses="integer",sep=",")
getSummary(repoTestCallSite$V1)

repocallSite_path="/home/peipei/ISSTA2018/data/regex/callsite_valid"
repocallSite=read.csv(file=repocallSite_path,head=FALSE,colClasses=c("integer","integer","integer"),sep=",")
colnames(repocallSite)=c("page","row","callSites")
getSummary(repocallSite$callSites)

total=sum(repocallSite$callSites) ##18426
tested=nrow(callSitekInfo)
untested=total-tested
t=rep(0,each=untested)
cc=c(callSitekInfo$V1,t)
getSummary(cc)

callsites=data.frame(all=repocallSite$callSites, tested=repoTestCallSite$V1)
callsites=melt(callsites)

x=data.frame(value=cc, type="all")
y=data.frame(value=callSitekInfo$V1, type="tested")
regexCallSite=rbind(x,y)

postscript("callsite.eps",sep=".")
pdf("callsite1.pdf")

par(mfrow = c(2, 1),oma=c(0,0,0,0),mar=c(4, 4, 2, 1) )
pdf("callsite1.pdf")
wid=0.3


pdf(file='callsite1.pdf', onefile=T, width=7,height=3)
# postscript("callsite1.eps", onefile=T, width=7,height=3)
par(mfrow = c(1, 1),oma=c(0,0,0,0),mar=c(5, 3, 1, 1) )
boxplot(callsites$value~callsites$variable, boxwex=wid, ylim=c(0,50), xlab="# call sites", ylab="", horizontal=TRUE)
axis(1, at=seq(0,50,5)) 
dev.off()
# pdf("callsite2.pdf")
pdf(file='callsite2.pdf', onefile=T, width=7,height=2)
# postscript("callsite2.eps",onefile=T, width=7,height=3)
par(mfrow = c(1, 1),oma=c(0,0,0,0),mar=c(5, 3, 1, 1) )
boxplot(callSitekInfo$V1, boxwex=wid, ylim=c(0,10),xlab="# regular expressions per call site", ylab="", horizontal=TRUE)
axis(1, at=seq(0,10,1)) 
dev.off()

boxplot(cc, boxwex=wid, ylim=c(0,10), xlab="Regular expressions per call site over 18,426 call sites", ylab="", horizontal=TRUE)
axis(1, at=seq(0,10,1)) 
boxplot(callSitekInfo$V1, boxwex=wid, ylim=c(0,10), xlab="Regular expressions per call site over 3093 tested call sites", ylab="", horizontal=TRUE)
axis(1, at=seq(0,10,1)) 
dev.off()