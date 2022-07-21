regexInfo_path="/home/peipei/ISSTA2018/data/regex/regex_info.csv"
regexDFA_path="/home/peipei/ISSTA2018/data/regex/regex_dfa.csv"
regexResults_path="/home/peipei/ISSTA2018/data/regex/regex_result.csv"

library(ggplot2)
library(reshape2)
library(dplyr)
setwd("/home/peipei/ISSTA/paper/figures")
regexInfo=read.csv(file=regexInfo_path,head=FALSE,colClasses=c("integer","integer","integer","integer","integer","logical","integer"),sep=",")
colnames(regexInfo)=c("index","dfa","total","unique","valid","failed","repo")
regexInfo=as.data.frame(regexInfo)

regexResults=read.csv(file=regexResults_path,head=FALSE,colClasses=c("integer","integer","integer","integer"),sep=",")
colnames(regexResults)=c("index","total","success","failed")
regexResults=as.data.frame(regexResults)

regexDFA=read.csv(file=regexDFA_path,head=FALSE,colClasses=c("integer","integer","integer","integer"),sep=",")
colnames(regexDFA)=c("index","nodes","edges","epairs")
regexDFA=as.data.frame(regexDFA)

rsize=nrow(regexInfo)
failed=regexInfo[regexInfo[,"failed"]==TRUE,]
failed_size=nrow(failed)

valid=regexInfo[regexInfo$failed==FALSE,]
nrow(valid)
getSummary(valid$dfa)
getSummary(valid$total)
getSummary(valid$unique)
getSummary(valid$repo)
getSummary(regexDFA$nodes)
getSummary(regexDFA$edges)
getSummary(regexDFA$epairs)
valid2=valid[valid$repo<=166,]

getSummary=function(data){
  print(mean(data))
  print(min(data))
  print(max(data))
  quantile(data, c(0.1,0.25,0.5,0.75,0.9,0.95,0.98,0.99))
}

valid2=valid[valid$repo<=166,]
getSummary(valid2$unique)  ##90 percentile 34

valid3=valid2[valid2$unique<=34,]
valid3=valid3[valid3$valid>0,]
dropped=setdiff(valid[,'index'],valid3[,'index']) ##13203 + 1434

for (row in 1:nrow(valid3)) {
  index=valid3[row,"index"]
  valid3[row,'t_inputs']=regexResults[regexResults$index==index,"total"]
  valid3[row,'t_success']=regexResults[regexResults$index==index,"success"]
  valid3[row,'t_failed']=regexResults[regexResults$index==index,"failed"]
}
getSummary(valid3$t_failed) 
getSummary(valid3$t_success)
getSummary(valid3$t_inputs)

length(which(valid3$t_failed==0)) ##5470
length(which(valid3$t_success==0)) ##4686
length(which(valid3$t_success!=0 & valid3$t_failed!=0)) ###3060
length(which(valid3$t_success==0 & valid3$t_failed==0)) ### 6 
valid3[which(valid3$t_success==0 & valid3$t_failed==0),"index"]  ##5299 8866 8892 8893 8894 8895







#covs=cbind(cbind(nodes=cov_node,type=regeCov$type),cbind(edges=cov_edge,type=regexCov$type),cbindedge_pairs=cov_epair,type=repoCov$type)
covs=cbind(nodes=cov_node,edges=cov_edge,edge_pairs=cov_epair)
covs=as.data.frame(covs)
covs=cbind(covs,type=regexCov$type)
t_covs=covs[covs$type=="total",c("nodes","edges","edge_pairs")]
# covs=melt(covs,id=c("type"))
#setEPS()
#postscript(paste(paste("regex","cov",sep="_"),"eps",sep="."))
p=ggplot(covs, aes(type,value))+ theme_bw()+
  theme(axis.line = element_line(colour = "black"),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.border = element_rect(colour = "black", fill=NA, size=0.2),
        panel.background = element_blank()) ++ theme(plot.title = element_text(size=15))
p=p+geom_boxplot(aes(fill=variable),outlier.colour = NULL,outlier.shape=1, outlier.size=0.3)
p=p+scale_y_continuous(breaks = pretty(covs$value, n = 10))
p=p+xlab("Type of Matching") + ylab("Coverages(%)") + ggtitle("Coverages across all regular expressions")
p=p+guides(fill=guide_legend(title="Coverage Types"))
p=p+scale_fill_grey(start=0.5,end=0.8)
# ggsave(filename="regex_cov.pdf", plot=p)
#dev.off()

# mean(cov_node)
# median(cov_node)
# quantile(cov_node, c(0.25,0.5,0.75,0.9,0.99))
# mean(cov_edge)
# median(cov_edge)
# quantile(cov_edge, c(0.25,0.5,0.75,0.9,0.99))
# mean(cov_epair,na.rm=TRUE)
# median(cov_epair,na.rm=TRUE)
# quantile(cov_epair, c(0.25,0.5,0.75,0.9,0.99),na.rm=TRUE)

setEPS()
postscript(paste(paste("regex","cov",sep="_"),"eps",sep="."))
par(mfrow = c(1, 3),oma=c(0,0,2,0))
# postscript(paste(paste("node","cov",sep="_"),"eps",sep="."))
boxplot(cov_node~regexCov$type, main="Node", names=c("total","success","failure"),
        xlab="", ylab="Node Coverage(%)")
axis(2, at=seq(0,100,10)) 
# dev.off()
# 
# setEPS()

#postscript(paste(paste("edge","cov",sep="_"),"eps",sep="."))
boxplot(cov_edge~regexCov$type, main="Edge", names=c("total","success","failure"),
        xlab="", ylab="Edge Coverage(%)")
axis(2, at=seq(0,100,10)) 
# dev.off()
# 
# setEPS()
# postscript(paste(paste("epair","cov",sep="_"),"eps",sep="."))
boxplot(cov_epair~regexCov$type, main="Edge pair", names=c("total","success","failure"),
        xlab="", ylab="Edge pair Coverage(%)")
axis(2, at=seq(0,100,10)) 
# title("Node, Edge, and Edge-Pair Coverages", line = -2,outer=TRUE) 
dev.off()

data=cbind('dfa size'=valid3$dfa,'total inputs'=valid3$total,'unique inputs'=valid3$unique,
           'nodes'=regexCov$t_node,'edges'=regexCov$t_edge,'edge pairs'=regexCov$t_epair)
data=as.data.frame(data)
#data=melt(data)

# max(valid3$dfa)
# max(regexCov$t_node)
# max(regexCov$t_edge)
# max(regexCov$t_epair)
# max(valid3$total)
# max(valid3$unique)
# min(valid3$dfa)
# min(regexCov$t_node)
# min(regexCov$t_edge)
# min(regexCov$t_epair)
# min(valid3$total)
# min(valid3$unique)
# mean(valid3$dfa)
# mean(regexCov$t_node)
# mean(regexCov$t_edge)
# mean(regexCov$t_epair)
# mean(valid3$total)
# mean(valid3$unique)
# quantile(regexCov$t_node, c(0.1,0.25,0.5,0.75,0.9,0.95,0.98,0.99))
# quantile(regexCov$t_edge, c(0.1,0.25,0.5,0.75,0.9,0.95,0.98,0.99))
# quantile(regexCov$t_epair, c(0.1,0.25,0.5,0.75,0.9,0.95,0.98,0.99))
# quantile(valid3$valid, c(0.1,0.25,0.5,0.75,0.9,0.95,0.98,0.99))
# quantile(valid3$total, c(0.1,0.25,0.5,0.75,0.9,0.95,0.98,0.99))
# quantile(valid3$dfa, c(0.1,0.25,0.5,0.75,0.9,0.95,0.98,0.99))

mapply(mean,data)
mapply(min,data)
mapply(max,data)
# quantile(data, c(0.1,0.25,0.5,0.75,0.9,0.95,0.98,0.99))

repoCov$v_node=repoCov$c_node*100/repoCov$t_node
repoCov$v_edge=repoCov$c_edge*100/repoCov$t_edge
repoCov$v_epair=repoCov$c_epair*100/repoCov$t_epair
repoCov=repoCov[,c("page","row","index","v_node","v_edge","v_epair","type")]
repoCov$id <- paste(repoCov$page,repoCov$row,sep="_")
repoStars$id=paste(repoStars$page,repoStars$row,sep="_")
validStars=repoStars[repoStars$id %in% repoCov$id,]

repoSize$id=paste(repoSize$page,repoSize$row,sep="_")
repoSize=repoSize[repoSize$id %in% repoCov$id,]
# vstar=merge(repoCov,validStars,by="id")
# vstar=vstar[,c("id","stars","tests","v_node","v_edge","v_epair","type")]

t=split(repoCov,repoCov$type)

tts=split(t$total,t$total$id)
avgCov=function(ss){
  sapply(list(ss$v_node,ss$v_edge,ss$v_epair),mean)
}
cov_t=sapply(tts,avgCov)
cov_tm=melt(cov_t)
boxplot(cov_tm$value~cov_tm$Var1)

ttss=split(t$successful,t$successful$id)
cov_s=sapply(ttss,avgCov)
cov_sm=melt(cov_s)
boxplot(cov_sm$value~cov_sm$Var1)

ttsf=split(t$failed,t$failed$id)
cov_f=sapply(ttsf,avgCov)
cov_fm=melt(cov_f)
boxplot(cov_fm$value~cov_fm$Var1)

pnode=rbind(total=cov_t[1,],successful=cov_s[1,],failed=cov_f[1,])
reponode=melt(pnode)
pedge=rbind(total=cov_t[2,],successful=cov_s[2,],failed=cov_f[2,])
repoedge=melt(pedge)
pepair=rbind(total=cov_t[3,],successful=cov_s[3,],failed=cov_f[3,])
repoepair=melt(pepair)
setEPS()
postscript(paste(paste("repo","cov",sep="_"),"eps",sep="."))
par(mfrow = c(1, 3),oma=c(0,0,2,0))
boxplot(reponode$value~reponode$Var1, main="Node", names=c("total","success","failure"),
        xlab="", ylab="Node Coverage(%)")
axis(2, at=seq(0,100,10)) 
boxplot(repoedge$value~repoedge$Var1, main="Edge", names=c("total","success","failure"),
        xlab="", ylab="Edge Coverage(%)")
axis(2, at=seq(0,100,10)) 
boxplot(repoepair$value~repoepair$Var1, main="Edge pair", names=c("total","success","failure"),
        xlab="", ylab="Edge pair Coverage(%)")
axis(2, at=seq(0,100,10)) 
dev.off()

cnames=colnames(cov_t)
getStart=function(id){return(validStars[validStars$id==id,"stars"])}
stars=sapply(cnames,getStart)
cov_tstars=rbind(cov_t,stars)
cov_tstars=t(cov_tstars)
cov_tstars=as.data.frame(cov_tstars)
colnames(cov_tstars)=c("v_node","v_edge","v_epair","stars")
split_stars=split(cov_tstars,cov_tstars$stars)
cov_star_t=sapply(split_stars,avgCov)

# cov_s
cov_sstars=rbind(cov_s,stars)
cov_sstars=t(cov_sstars)
cov_sstars=as.data.frame(cov_sstars)
colnames(cov_sstars)=c("v_node","v_edge","v_epair","stars")
split_stars=split(cov_sstars,cov_sstars$stars)
cov_star_s=sapply(split_stars,avgCov)

# cov_f
cov_fstars=rbind(cov_f,stars)
cov_fstars=t(cov_fstars)
cov_fstars=as.data.frame(cov_fstars)
colnames(cov_fstars)=c("v_node","v_edge","v_epair","stars")
split_stars=split(cov_fstars,cov_fstars$stars)
cov_star_f=sapply(split_stars,avgCov)

m="spearman" ##"spearman", "kendall"pearson
cor.test(cov_tstars$stars,cov_tstars$v_node,method=m)
cor.test(cov_tstars$stars,cov_tstars$v_edge,method=m)
cor.test(cov_tstars$stars,cov_tstars$v_epair,method=m)
cor.test(cov_tstars$stars,cov_tstars$v_node-cov_tstars$v_edge,method=m)

cor.test(cov_sstars$stars,cov_sstars$v_node,method=m)
cor.test(cov_sstars$stars,cov_sstars$v_edge,method=m)
cor.test(cov_sstars$stars,cov_sstars$v_epair,method=m)

cor.test(cov_fstars$stars,cov_fstars$v_node,method=m)
cor.test(cov_fstars$stars,cov_fstars$v_edge,method=m)
cor.test(cov_fstars$stars,cov_fstars$v_epair,method=m)

setEPS()
postscript(paste(paste("star","cov",sep="_"),"eps",sep="."))
plot(cov_star_t[1,],type="n",xlab="Stars",ylab="Coverage(%)",yaxs="i",xaxs="i") 
lines(cov_star_t[1,],lty=1)##total node
lines(cov_star_s[1,],lty=2)##success node dashed
# lines(cov_star_f[1,],lty=3)##failure node dotted
lines(cov_star_t[2,],lty=1,col='red')##total edge
lines(cov_star_s[2,],lty=2,col='red')##success node dashed
lines(cov_star_t[3,],lty=1,col='blue')##total edge pair
lines(cov_star_s[3,],lty=2,col='blue')##success node dashed
legend(20,103, legend=c("Node total", "Node success", "Edge total", "Edge success", "Edge pair total","Edge pair success"),
       ncol=3,bty='n',cex=0.7,lty=c(1,2,1,2,1,2),col=c("black","black",'red','red','blue','blue'),title="Line types")
dev.off()