library(ggplot2)
library(reshape2)
setwd("/home/peipei/ISSTA/paper/figures")
rex_ascii_path="/home/peipei/ISSTA2018/data/cov/ascii_all.csv"
rex_unicode_path="/home/peipei/ISSTA2018/data/cov/unicode_all.csv"
same_ascii_path="/home/peipei/ISSTA2018/data/cov/ascii_same.csv"
same_unicode_path="/home/peipei/ISSTA2018/data/cov/unicode_same.csv"
count_ascii_path="/home/peipei/ISSTA2018/data/regex/count_ascii.csv"
count_unicode_path="/home/peipei/ISSTA2018/data/regex/count_unicode.csv"

count_ascii=read.csv(file=count_ascii_path,head=FALSE, colClasses=c("integer","integer"),sep=",")
colnames(count_ascii)=c("index","count")
count_ascii=as.data.frame(count_ascii)
min(count_ascii$count)
max(count_ascii$count)
mean(count_ascii$count)
quantile(count_ascii$count,c(0.1,0.25,0.5,0.75,0.9,0.99))

count_unicode=read.csv(file=count_unicode_path,head=FALSE, colClasses=c("integer","integer"),sep=",")
colnames(count_unicode)=c("index","count")
count_unicode=as.data.frame(count_unicode)
min(count_unicode$count)
max(count_unicode$count)
mean(count_unicode$count)
quantile(count_unicode$count,c(0.1,0.25,0.5,0.75,0.9,0.99))


rexASCIICov=read.csv(file=rex_ascii_path,head=TRUE, colClasses=c("integer","integer","integer","integer","integer","integer","integer","integer"),sep=",")
colnames(rexASCIICov)=c("index","c_node","t_node","c_edge","t_edge","c_epair","t_epair","type")
rexASCIICov=as.data.frame(rexASCIICov)
rexASCIICov$type <- factor(rexASCIICov$type, levels = c(0,1,2), labels = c("total", "successful", "failed"))
rexASCIICovTotal=rexASCIICov[rexASCIICov$type=="total",]
rexASCIICovTotal$nodeCov=rexASCIICovTotal$c_node*100/rexASCIICovTotal$t_node
rexASCIICovTotal$edgeCov=rexASCIICovTotal$c_edge*100/rexASCIICovTotal$t_edge
rexASCIICovTotal$epairCov=rexASCIICovTotal$c_epair*100/rexASCIICovTotal$t_epair
rexASCIICovTotal=rexASCIICovTotal[,c('index',"nodeCov","edgeCov","epairCov")]
colnames(rexASCIICovTotal)=c("index","node","edge","edge pair")
rexASCIICovTotal=rexASCIICovTotal[!rexASCIICovTotal$index %in%  dropped,]
rexASCIICovTotal=melt(rexASCIICovTotal,id="index")
setEPS()
postscript(paste(paste("rex_ascii_total_all","cov",sep="_"),"eps",sep="."))
boxplot(rexASCIICovTotal$value~rexASCIICovTotal$variable, main="Coverages for all Matchings", names=c("Node","Edge","Edge-pair"),
        xlab="total", ylab="Coverage(%)")
axis(2, at=seq(0,100,10)) 
dev.off()


rexUnicodeCov=read.csv(file=rex_unicode_path,head=TRUE, colClasses=c("integer","integer","integer","integer","integer","integer","integer","integer"),sep=",")
colnames(rexUnicodeCov)=c("index","c_node","t_node","c_edge","t_edge","c_epair","t_epair","type")
rexUnicodeCov=as.data.frame(rexUnicodeCov)
rexUnicodeCov$type <- factor(rexUnicodeCov$type, levels = c(0,1,2), labels = c("total", "successful", "failed"))
rexUnicodeCovTotal=rexUnicodeCov[rexUnicodeCov$type=="total",]
rexUnicodeCovTotal$nodeCov=rexUnicodeCovTotal$c_node*100/rexUnicodeCovTotal$t_node
rexUnicodeCovTotal$edgeCov=rexUnicodeCovTotal$c_edge*100/rexUnicodeCovTotal$t_edge
rexUnicodeCovTotal$epairCov=rexUnicodeCovTotal$c_epair*100/rexUnicodeCovTotal$t_epair
rexUnicodeCovTotal=rexUnicodeCovTotal[,c('index',"nodeCov","edgeCov","epairCov")]
colnames(rexUnicodeCovTotal)=c("index","node","edge","edge pair")
rexUnicodeCovTotal=rexUnicodeCovTotal[!rexUnicodeCovTotal$index %in%  dropped,]
rexUnicodeCovTotal=melt(rexUnicodeCovTotal,id="index")
setEPS()
postscript(paste(paste("rex_unicode_total_all","cov",sep="_"),"eps",sep="."))
boxplot(rexUnicodeCovTotal$value~rexUnicodeCovTotal$variable, main="Coverages for all Matchings", names=c("Node","Edge","Edge-pair"),
        xlab="total", ylab="Coverage(%)")
axis(2, at=seq(0,100,10)) 
dev.off()


rexASCIICovSame=read.csv(file=same_ascii_path,head=TRUE, colClasses=c("integer","integer","integer","integer","integer","integer","integer","integer"),sep=",")
colnames(rexASCIICovSame)=c("index","c_node","t_node","c_edge","t_edge","c_epair","t_epair","type")
rexASCIICovSame=as.data.frame(rexASCIICovSame)
rexASCIICovSame$type <- factor(rexASCIICovSame$type, levels = c(0,1,2), labels = c("total", "successful", "failed"))
rexASCIICovSame=rexASCIICovSame[rexASCIICovSame$type=="total",]
rexASCIICovSame$nodeCov=rexASCIICovSame$c_node*100/rexASCIICovSame$t_node
rexASCIICovSame$edgeCov=rexASCIICovSame$c_edge*100/rexASCIICovSame$t_edge
rexASCIICovSame$epairCov=rexASCIICovSame$c_epair*100/rexASCIICovSame$t_epair
rexASCIICovSame=rexASCIICovSame[,c('index',"nodeCov","edgeCov","epairCov")]
colnames(rexASCIICovSame)=c("index","node","edge","edge pair")
rexASCIICovSame=rexASCIICovSame[!rexASCIICovSame$index %in%  dropped,]
rexASCIICovSame=melt(rexASCIICovSame,id="index")
setEPS()
postscript(paste(paste("rex_ascii_total_same","cov",sep="_"),"eps",sep="."))
boxplot(rexASCIICovSame$value~rexASCIICovSame$variable, main="Coverages for all Matchings", names=c("Node","Edge","Edge-pair"),
        xlab="total", ylab="Coverage(%)")
axis(2, at=seq(0,100,10)) 
dev.off()


rexUnicodeCovSame=read.csv(file=same_unicode_path,head=TRUE, colClasses=c("integer","integer","integer","integer","integer","integer","integer","integer"),sep=",")
colnames(rexUnicodeCovSame)=c("index","c_node","t_node","c_edge","t_edge","c_epair","t_epair","type")
rexUnicodeCovSame=as.data.frame(rexUnicodeCovSame)
rexUnicodeCovSame$type <- factor(rexUnicodeCovSame$type, levels = c(0,1,2), labels = c("total", "successful", "failed"))
rexUnicodeCovSame=rexUnicodeCovSame[rexUnicodeCovSame$type=="total",]
rexUnicodeCovSame$nodeCov=rexUnicodeCovSame$c_node*100/rexUnicodeCovSame$t_node
rexUnicodeCovSame$edgeCov=rexUnicodeCovSame$c_edge*100/rexUnicodeCovSame$t_edge
rexUnicodeCovSame$epairCov=rexUnicodeCovSame$c_epair*100/rexUnicodeCovSame$t_epair
rexUnicodeCovSame=rexUnicodeCovSame[,c('index',"nodeCov","edgeCov","epairCov")]
colnames(rexUnicodeCovSame)=c("index","node","edge","edge pair")
rexUnicodeCovSame=rexUnicodeCovSame[!rexUnicodeCovSame$index %in%  dropped,]
rexUnicodeCovSame=melt(rexUnicodeCovSame,id="index")
setEPS()
postscript(paste(paste("rex_unicode_total_same","cov",sep="_"),"eps",sep="."))
boxplot(rexUnicodeCovSame$value~rexUnicodeCovSame$variable, main="Coverages for all Matchings", names=c("Node","Edge","Edge-pair"),
        xlab="total", ylab="Coverage(%)")
axis(2, at=seq(0,100,10)) 
dev.off()

setEPS()
postscript(paste(paste("ascii","cov",sep="_"),"eps",sep="."))
par(mfrow = c(1, 2),oma=c(0,0,0,0)) #,mar=c(3,4,2,5)
boxplot(rexASCIICovTotal$value~rexASCIICovTotal$variable, boxwex=0.7, main="All Inputs", names=c("Node","Edge","E-Pair"),
        xlab="Total", ylab="Coverage(%)")
axis(2, at=seq(0,100,10))
boxplot(rexASCIICovSame$value~rexASCIICovSame$variable,  boxwex=0.7, main="Same number of Inputs", names=c("Node","Edge","E-Pair"),
        xlab="Total", ylab="Coverage(%)")
axis(2, at=seq(0,100,10)) 
dev.off()