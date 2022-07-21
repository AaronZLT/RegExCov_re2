library(ggplot2)
library(reshape2)
library(dplyr)
setwd("/home/peipei/ISSTA/paper/figures")

cov_rexASCII="/home/peipei/ISSTA2018/data/cov/1_ASCII_avgCov.csv"
cov_rexUnicode="/home/peipei/ISSTA2018/data/cov/1_Unicode_avgCov.csv"

stackCov2=stackCov[stackCov$type==1,]
stackCov2=stackCov2[stackCov2$count>0,]
cov_node=stackCov2$c_node*100/stackCov2$t_node
cov_edge=stackCov2$c_edge*100/stackCov2$t_edge
cov_epair=stackCov2$c_epair*100/stackCov2$t_epair
getSummary(cov_node)
getSummary(cov_edge)
getSummary(cov_epair)


asciiCov=read.csv(file=cov_rexASCII,head=TRUE, colClasses=c("integer","integer","integer","integer","integer","integer","integer"),sep=",")
colnames(asciiCov)=c("index","c_node","t_node","c_edge","t_edge","c_epair","t_epair")
asciiCov=as.data.frame(asciiCov)

ascii_node=asciiCov$c_node*100/asciiCov$t_node
ascii_edge=asciiCov$c_edge*100/asciiCov$t_edge
ascii_epair=asciiCov$c_epair*100/asciiCov$t_epair
getSummary(ascii_node)
getSummary(ascii_edge)
getSummary(ascii_epair)


asciiCov2=stackCov2[stackCov2$stack_index %in% asciiCov$index,]
ascii_node2=asciiCov2$c_node*100/asciiCov2$t_node
ascii_edge2=asciiCov2$c_edge*100/asciiCov2$t_edge
ascii_epair2=asciiCov2$c_epair*100/asciiCov2$t_epair
getSummary(ascii_node2)
getSummary(ascii_edge2)
getSummary(ascii_epair2)


unicodeCov=read.csv(file=cov_rexUnicode,head=TRUE, colClasses=c("integer","integer","integer","integer","integer","integer","integer"),sep=",")
colnames(unicodeCov)=c("index","c_node","t_node","c_edge","t_edge","c_epair","t_epair")
unicodeCov=as.data.frame(unicodeCov)

unicode_node=unicodeCov$c_node*100/unicodeCov$t_node
unicode_edge=unicodeCov$c_edge*100/unicodeCov$t_edge
unicode_epair=unicodeCov$c_epair*100/unicodeCov$t_epair
getSummary(unicode_node)
getSummary(unicode_edge)
getSummary(unicode_epair)

unicodeCov2=stackCov2[stackCov2$stack_index %in% unicodeCov$index,]
unicode_node2=unicodeCov2$c_node*100/unicodeCov2$t_node
unicode_edge2=unicodeCov2$c_edge*100/unicodeCov2$t_edge
unicode_epair2=unicodeCov2$c_epair*100/unicodeCov2$t_epair
getSummary(unicode_node2)
getSummary(unicode_edge2)
getSummary(unicode_epair2)


nc_ascii=data.frame(repo=ascii_node2,rex=ascii_node)
ec_ascii=data.frame(repo=ascii_edge2,rex=ascii_edge)
epc_ascii=data.frame(repo=ascii_epair2,rex=ascii_epair)