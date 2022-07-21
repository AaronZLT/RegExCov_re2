repoCov_path="/home/peipei/ISSTA2018/data/cov/repo_cov.csv"

library(ggplot2)
library(reshape2)
library(dplyr)
setwd("/home/peipei/ISSTA/paper/figures")

repoCov=read.csv(file=repoCov_path,head=TRUE, colClasses=c("integer","integer","integer","integer","integer","integer","integer","integer","integer","integer"),sep=",")
colnames(repoCov)=c("page","row","index","c_node","t_node","c_edge","t_edge","c_epair","t_epair","type")
repoCov=as.data.frame(repoCov)
repoCov$id=paste(repoCov$page,repoCov$row,sep="_")


repoCov=repoCov[!repoCov$index %in% dropped,]
repoCov$type <- factor(repoCov$type,levels = c(0,1,2),labels = c("total", "successful", "failed"))
nrow(unique(repoCov[,c("page","row")]))