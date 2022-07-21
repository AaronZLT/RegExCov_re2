library(ggplot2)
library(reshape2)
library(dplyr)
library(gridExtra)
setwd("/home/peipei/ISSTA/paper/figures")

stackCov_path="/home/peipei/ISSTA2018/data/cov/stack_cov.csv"
stackCov=read.csv(file=stackCov_path,head=TRUE, colClasses=c("integer","integer","integer","integer","integer","integer","integer","integer","integer","integer","integer","integer"),sep=",")
print(colnames(stackCov))
stackCov=as.data.frame(stackCov)

repos=unique(stackCov[,c("page","row")])
valid_repos=merge(repos, repoInfo, by=c("page","row"))
getSummary(valid_repos$stars)
# getSummary(valid_repos$stars2)
getSummary(valid_repos$size)
getSummary(valid_repos$tests)
getSummary(valid_repos$loc)

la=stackCov[stackCov$type==0, c("stack_index","page","row")]
res=rep.int(0,1225)
for (a in 1:1225){
  print(repos[a,c("page","row")])
  cc=0
  for (b in 1:15096){
    if (la[b,"page"]==repos[a,"page"] & la[b,"row"]==repos[a,"row"]){
      cc=cc+1
    }
  }
  res[a]=cc
}
getSummary(res)

stacks=split(stackCov,f = stackCov$stack_index)
res=sapply(stacks , function(x) x$count)
res=t(res)
colnames(res)=c("total","succ","failed")
res=as.data.frame(res)
res$succ_ratio=res$succ*100/res$total
res$fail_ratio=res$failed*100/res$total
getSummary(res$total)
getSummary(res$succ)
getSummary(res$failed)
getSummary(res$succ_ratio)
getSummary(res$fail_ratio)


length(which(res$failed==res$total))
length(which(res$succ==res$total))
length(which(res$total>res$succ+res$failed))

getSummary(stackCov3$count)
getSummary(stackCov3$t_node)
getSummary(stackCov3$t_edge)
getSummary(stackCov3$t_epair)

covs=stackCov[,c("c_node","t_node","c_edge","t_edge","c_epair","t_epair","type")]
# covs=b[,c("c_node","t_node","c_edge","t_edge","c_epair","t_epair","type")]
covs$type <- factor(covs$type, levels = c(0,1,2), labels = c("total", "successful", "failed"))
covs$v_node=covs$c_node*100/covs$t_node
covs$v_edge=covs$c_edge*100/covs$t_edge
covs$v_epair=covs$c_epair*100/covs$t_epair
covs=covs[,c("type","v_node","v_edge","v_epair")]
covs[is.na(covs$v_epair),"v_epair"]=0

n_untested=2863
a1=data.frame(type=rep("total",n_untested), v_node=rep(0,n_untested), v_edge=rep(0,n_untested), v_epair=rep(0,n_untested),stringsAsFactors = TRUE)
a2=data.frame(type=rep("successful",n_untested), v_node=rep(0,n_untested), v_edge=rep(0,n_untested), v_epair=rep(0,n_untested),stringsAsFactors = TRUE)
a3=data.frame(type=rep("failed",n_untested), v_node=rep(0,n_untested), v_edge=rep(0,n_untested), v_epair=rep(0,n_untested),stringsAsFactors = TRUE)
covs2=rbind(covs,a1,a2,a3)
covs=covs2
# types=split(covs,f = covs$type)
# total=types$`0`
# succ=types$`1`
# failure=types$`2`

ishorizontal=FALSE
setEPS()
if(ishorizontal){
  postscript(paste(paste("horz_stack","cov",sep="_"),"eps",sep="."))
  par(mfrow = c(3, 1),oma=c(0,0,0,0),mar=c(4, 3, 1, 2) )
  boxplot(covs$v_node~covs$type,names=c("total","success","failure"),
          xlab="Node Coverage(%)", ylab="", horizontal=TRUE)
  title("Node", line=0.5, outer=FALSE)
  axis(2, at=seq(0,100,10)) 
  boxplot(covs$v_edge~covs$type,names=c("total","success","failure"),
          xlab="Edge Coverage(%)", ylab="", horizontal=TRUE)
  title("Edge", line=0.5, outer=FALSE)
  axis(2, at=seq(0,100,10))
  boxplot(covs$v_epair~covs$type,names=c("total","success","failure"),
          xlab="Edge pair Coverage(%)", ylab="", horizontal=TRUE)
  title("Edge pair", line=0.5, outer=FALSE)
  axis(2, at=seq(0,100,10)) 
  dev.off()
}else{
  wid=0.5
  names_f=c("S",expression(S[succ]),expression(S[fail])) ##names_f=c("total","success","failure")
  postscript(paste(paste("stack","cov",sep="_"),"eps",sep="."))
  # postscript(paste(paste("stack","cov_not1",sep="_"),"eps",sep="."))
  # pdf(file='stackCov.pdf', onefile=T, width=7,height=7)
  par(mfrow = c(1, 3),mar=c(2,5,3,1),oma=c(0,0,0,0),las=1, cex.axis=2.0,cex.lab=2.0, cex.main=2.0)
  # postscript(paste(paste("node","cov",sep="_"),"eps",sep="."))
  boxplot(covs$v_node~covs$type, boxwex=wid, main="Node", names=names_f,
          xlab="", ylab="Node Coverage(%)", horizontal=FALSE)
  axis(2, at=seq(10,100,10)) 
  # dev.off()
  # 
  # setEPS()
  
  #postscript(paste(paste("edge","cov",sep="_"),"eps",sep="."))
  boxplot(covs$v_edge~covs$type, boxwex=wid, main="Edge", names=names_f,
          xlab="", ylab="Edge Coverage(%)", horizontal=FALSE)
  axis(2, at=seq(10,100,10)) 
  # dev.off()
  # 
  # setEPS()
  # postscript(paste(paste("epair","cov",sep="_"),"eps",sep="."))
  boxplot(covs$v_epair~covs$type, boxwex=wid, main="Edge-Pair", names=names_f,
          xlab="", ylab="Edge-Pair Coverage(%)", horizontal=FALSE)
  axis(2, at=seq(10,100,10)) 
  # title("Node, Edge, and Edge-Pair Coverages", line = -2,outer=TRUE) 
  dev.off()
}

types=split(covs,f = covs$type)
total=types$total
succ=types$successful
failed=types$failed
getSummary(total$v_node)
getSummary(succ$v_node)
getSummary(failed$v_node)
getSummary(total$v_edge)
getSummary(succ$v_edge)
getSummary(failed$v_edge)
getSummary(total$v_epair)
getSummary(succ$v_epair)
getSummary(failed$v_epair)
# getSummary(total$v_epair[!is.na(total$v_epair)])
# getSummary(succ$v_epair[!is.na(succ$v_epair)])
# getSummary(failed$v_epair[!is.na(failed$v_epair)])

a=stackCov[stackCov$type==0 & stackCov$count==1,"stack_index"] ### the stack_index which has valid input 1
b=stackCov[!stackCov$stack_index %in% a,]

# res_t=stackCov[stackCov$type==0,"count"]
# res_s=stackCov[stackCov$type==1,"count"]
# res_f=stackCov[stackCov$type==2,"count"]
# res=data.frame(res_t,res_s,res_f)
# getSummary(res$res_s*100/res$res_t)
# res$succ_ratio=res$res_s*100/res$res_t

res_t=b[b$type==0,"count"]
res_s=b[b$type==1,"count"]
res_f=b[b$type==2,"count"]

res=data.frame(res_t,res_s,res_f)
res$succ_ratio=res$res_s*100/res$res_t
res$fail_ratio=res$res_f*100/res$res_t
getSummary(res$res_f*100/res$res_t)
getSummary(res$res_s*100/res$res_t)
getSummary(res_t)
getSummary(res_s)
getSummary(res_f)


count_covs=stackCov[,c("stack_index","c_node","t_node","c_edge","t_edge","c_epair","t_epair","type","count")]
# count_covs=b[,c("stack_index","c_node","t_node","c_edge","t_edge","c_epair","t_epair","type","count")]
count_covs$type <- factor(count_covs$type, levels = c(0,1,2), labels = c("total", "successful", "failed"))
count_covs$v_node=count_covs$c_node*100/count_covs$t_node
count_covs$v_edge=count_covs$c_edge*100/count_covs$t_edge
count_covs$v_epair=count_covs$c_epair*100/count_covs$t_epair
count_types=split(count_covs,f = count_covs$type)
count_total=count_types$total
count_succ=count_types$successful
count_failed=count_types$failed

m="spearman" ##"spearman" distribution unknown, "kendall" rank, pair, pearson normal distribution
cor.test(count_total$count,count_total$v_node,method=m)
cor.test(count_total$count,count_total$v_edge,method=m)
cor.test(count_total$count,count_total$v_epair,method=m)

cor.test(res$succ_ratio,count_total$v_node,method=m)
cor.test(res$succ_ratio,count_total$v_edge,method=m)
cor.test(res$succ_ratio,count_total$v_epair,method=m)

cor.test(res$fail_ratio,count_total$v_node,method=m)
cor.test(res$fail_ratio,count_total$v_edge,method=m)
cor.test(res$fail_ratio,count_total$v_epair,method=m)

cor.test(count_succ$count,count_succ$v_node,method=m)
cor.test(count_succ$count,count_succ$v_edge,method=m)
cor.test(count_succ$count,count_succ$v_epair,method=m)

cor.test(count_failed$count,count_failed$v_node,method=m)
cor.test(count_failed$count,count_failed$v_edge,method=m)
cor.test(count_failed$count,count_failed$v_epair,method=m)

aov_m=data.frame(node=count_total$v_node,edge=count_total$v_edge,epair=count_total$v_epair,total=count_total$count,succ=count_succ$count,fail=count_failed$count)
aov_m$succ_ratio=res$succ_ratio
aov_m$fail_ratio=res$fail_ratio

aov_node=aov(node~total*succ*fail,data=aov_m)
aov_edge=aov(edge~total*succ*fail,data=aov_m)
aov_epair=aov(epair~total*succ*fail,data=aov_m)
summary(aov_node)
summary(aov_edge)
summary(aov_epair)

aov_node=aov(node~total*succ,data=aov_m)
aov_edge=aov(edge~total*succ,data=aov_m)
aov_epair=aov(epair~total*succ,data=aov_m)
summary(aov_node)
summary(aov_edge)
summary(aov_epair)

aov_node=aov(node~total*fail,data=aov_m)
aov_edge=aov(edge~total*fail,data=aov_m)
aov_epair=aov(epair~total*fail,data=aov_m)
summary(aov_node)
summary(aov_edge)
summary(aov_epair)


# types=split(stackCov,f=stackCov$type)
types=split(b,f=b$type)
uncovered=types$`0`
uncovered_index=uncovered$stack_index
uncovered_node==uncovered$t_node-uncovered$c_node
uncovered_edge=uncovered$t_edge-uncovered$c_edge
uncovered_epair=uncovered$t_epair-uncovered$c_epair
uncovs=data.frame(stack_index=uncovered_index,uncov_node=uncovered_node,uncov_edge=uncovered_edge,uncov_epair=uncovered_epair)
uncovs$node_r=uncovered_node*100/uncovered$t_node
uncovs$edge_r=uncovered_edge*100/uncovered$t_edge
uncovs$epair_r=uncovered_epair*100/uncovered$t_epair
getSummary(uncovs$uncov_node)
getSummary(uncovs$node_r)
getSummary(uncovs$uncov_edge)
getSummary(uncovs$edge_r)
getSummary(uncovs$uncov_epair)
getSummary(uncovs$epair_r[!is.na(uncovs$epair_r)])


startest_covs=merge(repoStarTests,stackCov,by=c("page","row"))
# startest_covs=merge(repoStarTests,b,by=c("page","row"))
startest_covs=startest_covs[,c("stack_index","stars2","tests","c_node","t_node","c_edge","t_edge","c_epair","t_epair","type")]
types=split(startest_covs,f=startest_covs$type)
cov_t=types$`0`
cov_t$v_node=cov_t$c_node*100/cov_t$t_node
cov_t$v_edge=cov_t$c_edge*100/cov_t$t_edge
cov_t$v_epair=cov_t$c_epair*100/cov_t$t_epair

cor.test(cov_t$stars2,cov_t$v_node,method=m)
cor.test(cov_t$stars2,cov_t$v_edge,method=m)
cor.test(cov_t$stars2,cov_t$v_epair,method=m)
cor.test(cov_t$tests,cov_t$v_node,method=m)
cor.test(cov_t$tests,cov_t$v_edge,method=m)
cor.test(cov_t$tests,cov_t$v_epair,method=m)

summary(aov(cov_t$v_node~cov_t$stars2*cov_t$tests))
summary(aov(cov_t$v_edge~cov_t$stars2*cov_t$tests))
summary(aov(cov_t$v_epair~cov_t$stars2*cov_t$tests))

postscript(paste(paste("tests","cov",sep="_"),"eps",sep="."))
# postscript(paste(paste("tests","cov2",sep="_"),"eps",sep="."))
p1=ggplot(cov_t, aes(x=tests, y=v_node,group=tests))+
  geom_boxplot(notch=FALSE, outlier.shape=NA, fill="red", alpha=0.2)
p2=ggplot(cov_t, aes(x=tests, y=v_edge,group=tests))+
  geom_boxplot(notch=FALSE, outlier.shape=NA, fill="red", alpha=0.2)
p3=ggplot(cov_t, aes(x=tests, y=v_epair,group=tests))+
  geom_boxplot(notch=FALSE, outlier.shape=NA, fill="red", alpha=0.2)
grid.arrange(p1, p2, p3, nrow = 3)
dev.off()

avg=function(x){
  v_node=x$c_node*100/x$t_node
  v_edge=x$c_edge*100/x$t_edge
  v_epair=x$c_epair*100/x$t_epair
  return(c(mean(x$tests),mean(v_node),mean(v_edge),mean(v_epair)))
}


data=data.frame(x1=cov_t$stars2,y1=cov_t$v_node,y2=cov_t$v_edge,y3=cov_t$v_epair)
avg_group=split(data,f=data$x1)
avg1=sapply(avg_group,function(x) mean(x$y1))
avg2=sapply(avg_group,function(x) mean(x$y2))
avg3=sapply(avg_group,function(x) mean(x$y3))
d2=data.frame(x1=as.numeric(names(avg1)),avg1,avg2,avg3)

#Graph
# postscript(paste(paste("stars","cov",sep="_"),"eps",sep="."))
postscript(paste(paste("stars","cov2",sep="_"),"eps",sep="."))
ax=seq(1, length(d2$x1), 5)
par(mfrow = c(3, 1),oma=c(0,0,0,0),mar=c(4, 4, 2, 1) )
boxplot(data$y1~factor(data$x1),pch=19,cex=0.4, xaxt="n", ylim=c(0,100), xlab="Project Star", ylab="Node Coverage(%)")
axis(2, at=seq(0,100,10)) 
axis(1, at=ax, labels=d2$x1[ax])
lines(x=factor(d2$x1),y=d2$avg1, lwd=2, col="blue")
boxplot(data$y2~factor(data$x1),pch=19,cex=0.4, xaxt="n", ylim=c(0,100), xlab="Project Star", ylab="Edge Coverage(%)")
axis(2, at=seq(0,100,10)) 
axis(1, at=ax, labels=d2$x1[ax])
lines(x=factor(d2$x1),y=d2$avg2, lwd=2, col="blue")
boxplot(data$y3~factor(data$x1),pch=19,cex=0.4, xaxt="n", ylim=c(0,100), xlab="Project Star", ylab="Edge-pair Coverage(%)")
axis(2, at=seq(0,100,10)) 
axis(1, at=ax, labels=d2$x1[ax])
lines(x=factor(d2$x1),y=d2$avg3, lwd=2, col="blue")
dev.off()


# muncovs=melt(uncovs,id="stack_index")
# muncovs$variable <- factor(muncovs$variable, levels = c("uncov_node","uncov_edge","uncov_epair"), labels = c("Node", "Edge", "Epair"))
# postscript(paste(paste("stack","uncovered",sep="_"),"eps",sep="."))
# boxplot(muncovs$value~muncovs$variable, main="", names=c("Node","Edge","Epair"),
#         xlab="", ylab="Node Coverage(%)", horizontal=FALSE)
# axis(2, at=seq(0,100,10)) 
# dev.off()
# 
# setEPS()

#postscript(paste(paste("edge","cov",sep="_"),"eps",sep="."))
boxplot(covs$v_edge~covs$type, main="Edge", names=c("total","success","failure"),
        xlab="", ylab="Edge Coverage(%)", horizontal=FALSE)
axis(2, at=seq(0,100,10)) 
# dev.off()
# 
# setEPS()
# postscript(paste(paste("epair","cov",sep="_"),"eps",sep="."))
boxplot(covs$v_epair~covs$type, main="Edge pair", names=c("total","success","failure"),
        xlab="", ylab="Edge pair Coverage(%)", horizontal=FALSE)
axis(2, at=seq(0,100,10)) 
# title("Node, Edge, and Edge-Pair Coverages", line = -2,outer=TRUE) 
dev.off()