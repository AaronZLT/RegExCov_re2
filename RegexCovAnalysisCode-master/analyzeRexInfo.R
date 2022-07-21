library(ggplot2)
library(reshape2)
library(dplyr)
setwd("/home/peipei/ISSTA/paper/figures")
rex_stackIndex="/home/peipei/ISSTA2018/data/dfa/input_0/ASCII/stack_index.csv"
rex_stackIndex2="/home/peipei/ISSTA2018/data/dfa/input_0/Unicode/stack_index.csv"
rex_sdfaInfoASCII="/home/peipei/ISSTA2018/data/regex/ASCII_sdfa_info.csv"
rex_sdfaInfoUnicode="/home/peipei/ISSTA2018/data/regex/Unicode_sdfa_info.csv"
succ_sdfaInfoASCII="/home/peipei/ISSTA2018/data/regex/ASCII_succ.csv"
succ_sdfaInfoUnicode="/home/peipei/ISSTA2018/data/regex/Unicode_succ.csv"
succ_rexASCII="/home/peipei/ISSTA2018/data/regex/ASCII_succ2.csv"
succ_rexUnicode="/home/peipei/ISSTA2018/data/regex/Unicode_succ2.csv"
succ_rex5ASCII="/home/peipei/ISSTA2018/data/regex/5ASCII_succ2.csv"
succ_rex10ASCII="/home/peipei/ISSTA2018/data/regex/10ASCII_succ2.csv"

stackInfo=read.csv(file=rex_stackIndex,na.strings="na",head=FALSE,colClasses="integer",sep=",")
colnames(stackInfo)="stack_index"
stackInfo=unlist(stackInfo)

stackInfo2=read.csv(file=rex_stackIndex2,na.strings="na",head=FALSE,colClasses="integer",sep=",")
colnames(stackInfo2)="stack_index2"
stackInfo2=unlist(stackInfo2)

rexInfo=stackCov[stackCov$stack_index %in% stackInfo, c("stack_index","regex_index","page","row","type","count")]
length(unique(rexInfo$stack_index))
length(unique(rexInfo$regex_index))
nrow(unique(rexInfo[c("page", "row")]))

t=merge(lenInfo[c("stack_index","regex_size","regex_size_dfa")], rexInfo, by="stack_index")
t=t[t$type==0,]
getSummary(t$regex_size)

sdfaInfoASCII=read.csv(file=rex_sdfaInfoASCII,na.strings="na",head=FALSE,colClasses=c("integer","integer","integer","integer"),sep=",")
colnames(sdfaInfoASCII)=c("stack_index","nodes","edges","epairs")
sdfaInfoASCII=as.data.frame(sdfaInfoASCII)

getSummary(sdfaInfoASCII$nodes)
getSummary(sdfaInfoASCII$edges)
getSummary(sdfaInfoASCII$epairs)

t2=merge(sdfaInfoASCII, sdfaInfo,by="stack_index")
which(t2$nodes!=t2$t_node)
which(t2$edges!=t2$t_edge)
which(t2$epairs!=t2$t_epair)
t2[which(t2$epairs!=t2$t_epair),]

sdfaInfoUnicode=read.csv(file=rex_sdfaInfoUnicode,na.strings="na",head=FALSE,colClasses=c("integer","integer","integer","integer"),sep=",")
colnames(sdfaInfoUnicode)=c("stack_index","nodes","edges","epairs")
sdfaInfoUnicode=as.data.frame(sdfaInfoUnicode)

getSummary(sdfaInfoUnicode$nodes)
getSummary(sdfaInfoUnicode$edges)
getSummary(sdfaInfoUnicode$epairs)

t3=merge(sdfaInfoUnicode, sdfaInfo,by="stack_index")
which(t3$nodes!=t3$t_node)
which(t3$edges!=t3$t_edge)
which(t3$epairs!=t3$t_epair)
t3[which(t3$epairs!=t3$t_epair),]  ### same as sdfaInfoASCII

sdfaSuccASCII=read.csv(file=succ_sdfaInfoASCII,na.strings="na",head=FALSE,colClasses=c("integer","integer","integer","integer","integer"),sep=",")
colnames(sdfaSuccASCII)=c("stack_index","succ","nodes","edges","epairs")
sdfaSuccASCII=as.data.frame(sdfaSuccASCII)
getSummary(sdfaSuccASCII$nodes)
getSummary(sdfaSuccASCII$edges)
getSummary(sdfaSuccASCII$epairs)
getSummary(sdfaSuccASCII$succ)

succASCIIInfo=stackCov[stackCov$stack_index %in% sdfaSuccASCII$stack_index, c("stack_index","regex_index","page","row","type","count")]
length(unique(succASCIIInfo$stack_index))
length(unique(succASCIIInfo$regex_index))
nrow(unique(succASCIIInfo[c("page", "row")]))

lenSuccASCII=lenInfo[lenInfo$stack_index %in% sdfaSuccASCII$stack_index, c("stack_index","regex_size","regex_size_dfa")]
getSummary(lenSuccASCII$regex_size)

sdfaSuccUnicode=read.csv(file=succ_sdfaInfoUnicode,na.strings="na",head=FALSE,colClasses=c("integer","integer","integer","integer","integer"),sep=",")
colnames(sdfaSuccUnicode)=c("stack_index","succ","nodes","edges","epairs")
sdfaSuccUnicode=as.data.frame(sdfaSuccUnicode)
getSummary(sdfaSuccUnicode$nodes)
getSummary(sdfaSuccUnicode$edges)
getSummary(sdfaSuccUnicode$epairs)
getSummary(sdfaSuccUnicode$succ)

succUnicodeInfo=stackCov[stackCov$stack_index %in% sdfaSuccUnicode$stack_index, c("stack_index","regex_index","page","row","type","count")]
length(unique(succUnicodeInfo$stack_index))
length(unique(succUnicodeInfo$regex_index))
nrow(unique(succUnicodeInfo[c("page", "row")]))

lenSuccUnicode=lenInfo[lenInfo$stack_index %in% sdfaSuccUnicode$stack_index, c("stack_index","regex_size","regex_size_dfa")]
getSummary(lenSuccUnicode$regex_size)


succRexASCII=read.csv(file=succ_rexASCII,na.strings="na",head=FALSE,sep=",")
colnames(succRexASCII)=c("stack_index","succ","r1","r2","r3","r4","r5","r6","r7","r8","r9","r10")
succRexASCII=as.data.frame(succRexASCII)

c1=which(succRexASCII$succ>succRexASCII$r1)
c2=which(succRexASCII$succ>succRexASCII$r2)
c3=which(succRexASCII$succ>succRexASCII$r3)
c4=which(succRexASCII$succ>succRexASCII$r4)
c5=which(succRexASCII$succ>succRexASCII$r5)
c6=which(succRexASCII$succ>succRexASCII$r6)
c7=which(succRexASCII$succ>succRexASCII$r7)
c8=which(succRexASCII$succ>succRexASCII$r8)
c9=which(succRexASCII$succ>succRexASCII$r9)
c10=which(succRexASCII$succ>succRexASCII$r10)
d=unique(c(c1,c2,c3,c4,c5,c6,c7,c8,c9,c10))
length(d)
View(succRexASCII[d,])
dd2=succRexASCII[d,"stack_index"]
dd3=stackCov[stackCov$stack_index %in% dd2,]
dd4=unique(dd3$regex_index)
length(dd4)

t=rowSums(succRexASCII[,c("r1","r2","r3","r4","r5","r6","r7","r8","r9","r10")])
tt=which(t<succRexASCII$succ)
length(tt)
View(succRexASCII[(which(t<succRexASCII$succ)),])
tt2=succRexASCII[(which(t<succRexASCII$succ)),"stack_index"]
tt3=stackCov[stackCov$stack_index %in% tt2,]
tt4=unique(tt3$regex_index)
length(tt4)

succRexASCII2=succRexASCII[!succRexASCII$stack_index %in% tt2,]
tt5=stackCov[stackCov$stack_index %in% succRexASCII$stack_index,]
tt6=unique(tt5$regex_index)
length(tt6)

succRexUnicode=read.csv(file=succ_rexUnicode,na.strings="na",head=FALSE,sep=",")
colnames(succRexUnicode)=c("stack_index","succ","r1","r2","r3","r4","r5","r6","r7","r8","r9","r10")
succRexUnicode=as.data.frame(succRexUnicode)

c1=which(succRexUnicode$succ>succRexUnicode$r1)
c2=which(succRexUnicode$succ>succRexUnicode$r2)
c3=which(succRexUnicode$succ>succRexUnicode$r3)
c4=which(succRexUnicode$succ>succRexUnicode$r4)
c5=which(succRexUnicode$succ>succRexUnicode$r5)
c6=which(succRexUnicode$succ>succRexUnicode$r6)
c7=which(succRexUnicode$succ>succRexUnicode$r7)
c8=which(succRexUnicode$succ>succRexUnicode$r8)
c9=which(succRexUnicode$succ>succRexUnicode$r9)
c10=which(succRexUnicode$succ>succRexUnicode$r10)
d=unique(c(c1,c2,c3,c4,c5,c6,c7,c8,c9,c10))
length(d)
View(succRexUnicode[d,])
dd2=succRexUnicode[d,"stack_index"]
dd3=stackCov[stackCov$stack_index %in% dd2,]
dd4=unique(dd3$regex_index)
length(dd4)

t=rowSums(succRexUnicode[,c("r1","r2","r3","r4","r5","r6","r7","r8","r9","r10")])
tt=which(t<succRexUnicode$succ)
length(tt)
View(succRexUnicode[(which(t<succRexUnicode$succ)),])
tt2=succRexUnicode[(which(t<succRexUnicode$succ)),"stack_index"]
tt3=stackCov[stackCov$stack_index %in% tt2,]
tt4=unique(tt3$regex_index)
length(tt4)

succRexUnicode2=succRexUnicode[!succRexUnicode$stack_index %in% tt2,]
tt5=stackCov[stackCov$stack_index %in% succRexUnicode2$stack_index,]
tt6=unique(tt5$regex_index)
length(tt6)


succRex5ASCII=read.csv(file=succ_rex5ASCII,na.strings="na",head=FALSE,sep=",")
colnames(succRex5ASCII)=c("stack_index","succ","r1","r2","r3","r4","r5")
succRex5ASCII=as.data.frame(succRex5ASCII)

c1=which(succRex5ASCII$succ*5>succRex5ASCII$r1)
c2=which(succRex5ASCII$succ*5>succRex5ASCII$r2)
c3=which(succRex5ASCII$succ*5>succRex5ASCII$r3)
c4=which(succRex5ASCII$succ*5>succRex5ASCII$r4)
c5=which(succRex5ASCII$succ*5>succRex5ASCII$r5)
d=unique(c(c1,c2,c3,c4,c5))
length(d)
View(succRex5ASCII[d,])
dd2=succRex5ASCII[d,"stack_index"]
dd3=stackCov[stackCov$stack_index %in% dd2,]
dd4=unique(dd3$regex_index)
length(dd4)

t=rowSums(succRex5ASCII[,c("r1","r2","r3","r4","r5")])
tt=which(t<succRex5ASCII$succ*5)
length(tt)
View(succRex5ASCII[(which(t<succRex5ASCII$succ*5)),])
tt2=succRex5ASCII[(which(t<succRex5ASCII$succ*5)),"stack_index"]
tt3=stackCov[stackCov$stack_index %in% tt2,]
tt4=unique(tt3$regex_index)
length(tt4)

succRex5ASCII2=succRex5ASCII[!succRex5ASCII$stack_index %in% tt2,]
tt5=stackCov[stackCov$stack_index %in% succRex5ASCII$stack_index,]
tt6=unique(tt5$regex_index)
length(tt6)

which(!succRex5ASCII2$stack_index %in% succRexASCII2$stack_index)
succRex5ASCII2[which(!succRex5ASCII2$stack_index %in% succRexASCII2$stack_index),]

succRex10ASCII=read.csv(file=succ_rex10ASCII,na.strings="na",head=FALSE,sep=",")
colnames(succRex10ASCII)=c("stack_index","succ","r1","r2","r3","r4","r5")
succRex10ASCII=as.data.frame(succRex10ASCII)

c1=which(succRex10ASCII$succ*10>succRex10ASCII$r1)
c2=which(succRex10ASCII$succ*10>succRex10ASCII$r2)
c3=which(succRex10ASCII$succ*10>succRex10ASCII$r3)
c4=which(succRex10ASCII$succ*10>succRex10ASCII$r4)
c5=which(succRex10ASCII$succ*10>succRex10ASCII$r5)
d=unique(c(c1,c2,c3,c4,c5))
length(d)
View(succRex10ASCII[d,])
dd2=succRex10ASCII[d,"stack_index"]
dd3=stackCov[stackCov$stack_index %in% dd2,]
dd4=unique(dd3$regex_index)
length(dd4)

t=rowSums(succRex10ASCII[,c("r1","r2","r3","r4","r5")])
tt=which(t<succRex10ASCII$succ*10)
length(tt)
View(succRex10ASCII[(which(t<succRex10ASCII$succ*10)),])
tt2=succRex10ASCII[(which(t<succRex10ASCII$succ*10)),"stack_index"]
tt3=stackCov[stackCov$stack_index %in% tt2,]
tt4=unique(tt3$regex_index)
length(tt4)

succRex10ASCII2=succRex10ASCII[!succRex10ASCII$stack_index %in% tt2,]
tt5=stackCov[stackCov$stack_index %in% succRex10ASCII$stack_index,]
tt6=unique(tt5$regex_index)
length(tt6)

which(!succRex10ASCII2$stack_index %in% succRexASCII2$stack_index)
succRex10ASCII2[which(!succRex10ASCII2$stack_index %in% succRexASCII2$stack_index),]

which(!succRex10ASCII2$stack_index %in% succRex5ASCII2$stack_index)
succRex10ASCII2[which(!succRex10ASCII2$stack_index %in% succRex5ASCII2$stack_index),]