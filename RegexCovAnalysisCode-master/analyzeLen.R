library(ggplot2)
library(reshape2)
library(dplyr)
setwd("/home/peipei/ISSTA/paper/figures")
regexLen_path="/home/peipei/ISSTA2018/data/regex/stack_strLen.csv"

lenInfo=read.csv(file=regexLen_path,na.strings="na",head=FALSE,colClasses=c("integer","integer","integer","integer","integer","integer","integer","numeric","numeric","numeric","numeric","numeric","numeric","integer"),sep=",")
colnames(lenInfo)=c("stack_index","regex_index","page","row","regex_size","regex_size_dfa","total_inputs","mean_inputs","dev_inputs","mean_succ","dev_succ","mean_fail","dev_fail","valid_inputs")
lenInfo=as.data.frame(lenInfo)

dfa_m=stackCov[stackCov$type==0,c("stack_index","t_node","t_edge","t_epair")]
# dfa_m=b[b$type==0,c("stack_index","t_node","t_edge","t_epair")]
len_m=lenInfo[c("stack_index","regex_size")]
c=merge(dfa_m,len_m,by="stack_index")
cor.test(c$t_node,c$regex_size,method=m)
cor.test(c$t_edge,c$regex_size,method=m)
cor.test(c$t_epair,c$regex_size,method=m)

validLenInfo=merge(dfa_m,lenInfo,by="stack_index")
merge(dfa_m,len_m,by="stack_index")
getSummary(validLenInfo$regex_size)
getSummary(validLenInfo$mean_inputs)
