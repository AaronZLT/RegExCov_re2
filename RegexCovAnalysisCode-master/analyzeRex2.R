library(ggplot2)
library(reshape2)
library(dplyr)
library(effsize)
setwd("/home/peipei/ISSTA/paper/figures")

# cov_rexASCII="/home/peipei/ISSTA2018/data/cov/1_ASCII_avgCov.csv"
# cov_rexUnicode="/home/peipei/ISSTA2018/data/cov/1_Unicode_avgCov.csv"
# cov_rex5ASCII="/home/peipei/ISSTA2018/data/cov/5_ASCII_avgCov.csv"
# cov_rex10ASCII="/home/peipei/ISSTA2018/data/cov/10_ASCII_avgCov.csv"

cov_rexASCII="/home/peipei/ISSTA2018/data/cov/1_ASCII_avgCov2.csv"
cov_rex5ASCII="/home/peipei/ISSTA2018/data/cov/5_ASCII_avgCov2.csv"
cov_rex10ASCII="/home/peipei/ISSTA2018/data/cov/10_ASCII_avgCov2.csv"


stackCov2=stackCov[stackCov$type==1,]
stackCov2=stackCov2[stackCov2$count>0,]
cov_node=stackCov2$c_node*100/stackCov2$t_node
cov_edge=stackCov2$c_edge*100/stackCov2$t_edge
cov_epair=stackCov2$c_epair*100/stackCov2$t_epair
getSummary(cov_node)
getSummary(cov_edge)
getSummary(cov_epair)

stackCov3=stackCov[stackCov$type==0,]
stackCov3=stackCov3[stackCov3$stack_index %in% stackCov2$stack_index,]
cov_node1=stackCov3$c_node*100/stackCov3$t_node
cov_edge1=stackCov3$c_edge*100/stackCov3$t_edge
cov_epair1=stackCov3$c_epair*100/stackCov3$t_epair
getSummary(cov_node1)
getSummary(cov_edge1)
getSummary(cov_epair1[!is.na(cov_epair1)])

asciiCov=read.csv(file=cov_rexASCII,head=FALSE, colClasses=c("integer","integer","integer","integer","integer","integer","integer"),sep=",")
colnames(asciiCov)=c("index","c_node","t_node","c_edge","t_edge","c_epair","t_epair")
asciiCov=as.data.frame(asciiCov)

ascii_node=asciiCov$c_node*100/asciiCov$t_node
ascii_edge=asciiCov$c_edge*100/asciiCov$t_edge
ascii_epair=asciiCov$c_epair*100/asciiCov$t_epair
getSummary(ascii_node)
getSummary(ascii_edge)
getSummary(ascii_epair)

ascii5Cov=read.csv(file=cov_rex5ASCII,head=FALSE, colClasses=c("integer","integer","integer","integer","integer","integer","integer"),sep=",")
colnames(ascii5Cov)=c("index","c_node","t_node","c_edge","t_edge","c_epair","t_epair")
ascii5Cov=as.data.frame(ascii5Cov)

ascii5_node=ascii5Cov$c_node*100/ascii5Cov$t_node
ascii5_edge=ascii5Cov$c_edge*100/ascii5Cov$t_edge
ascii5_epair=ascii5Cov$c_epair*100/ascii5Cov$t_epair
getSummary(ascii5_node)
getSummary(ascii5_edge)
getSummary(ascii5_epair)

ascii10Cov=read.csv(file=cov_rex10ASCII,head=FALSE, colClasses=c("integer","integer","integer","integer","integer","integer","integer"),sep=",")
colnames(ascii10Cov)=c("index","c_node","t_node","c_edge","t_edge","c_epair","t_epair")
ascii10Cov=as.data.frame(ascii10Cov)

ascii10_node=ascii10Cov$c_node*100/ascii10Cov$t_node
ascii10_edge=ascii10Cov$c_edge*100/ascii10Cov$t_edge
ascii10_epair=ascii10Cov$c_epair*100/ascii10Cov$t_epair
getSummary(ascii10_node)
getSummary(ascii10_edge)
getSummary(ascii10_epair)

asciiCov2=stackCov2[stackCov2$stack_index %in% asciiCov$index,]
ascii_node2=asciiCov2$c_node*100/asciiCov2$t_node
ascii_edge2=asciiCov2$c_edge*100/asciiCov2$t_edge
ascii_epair2=asciiCov2$c_epair*100/asciiCov2$t_epair
getSummary(ascii_node2)
getSummary(ascii_edge2)
getSummary(ascii_epair2)

asciiCov3=stackCov3[stackCov3$stack_index %in% asciiCov$index,]
ascii_node3=asciiCov3$c_node*100/asciiCov3$t_node
ascii_edge3=asciiCov3$c_edge*100/asciiCov3$t_edge
ascii_epair3=asciiCov3$c_epair*100/asciiCov3$t_epair
getSummary(ascii_node3)
getSummary(ascii_edge3)
getSummary(ascii_epair3)
getSummary(asciiCov3$count)

timed_regex=c(723,983,984,5326,12960)

unicodeCov=read.csv(file=cov_rexUnicode,head=FALSE, colClasses=c("integer","integer","integer","integer","integer","integer","integer"),sep=",")
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

##wilcoxon test
# H_0: \mu_{Repo2S} = \mu_{RexS1} // do this for NC, EC, EPC
wilcox.test(ascii_node2, ascii_node, paired=TRUE, exact=FALSE, correct=FALSE)
wilcox.test(ascii_edge2, ascii_edge, paired=TRUE, exact=FALSE, correct=FALSE)
wilcox.test(ascii_epair2, ascii_epair, paired=TRUE, exact=FALSE, correct=FALSE)

cliff.delta(ascii_node2,ascii_node) ##negligible
cliff.delta(ascii_edge2,ascii_edge) ##negligible
cliff.delta(ascii_epair2,ascii_epair) ## negligible

# H_0: \mu_{Repo2S} = \mu_{RexS5} // do this for NC, EC, EPC
wilcox.test(ascii_node2, ascii5_node, paired=TRUE, exact=FALSE, correct=FALSE)
wilcox.test(ascii_edge2, ascii5_edge, paired=TRUE, exact=FALSE, correct=FALSE)
wilcox.test(ascii_epair2, ascii5_epair, paired=TRUE, exact=FALSE, correct=FALSE)

cliff.delta(ascii_node2,ascii5_node) ##negligible
cliff.delta(ascii_edge2,ascii5_edge) ##negligible
cliff.delta(ascii_epair2,ascii5_epair) ## negligible

# H_0: \mu_{Repo2S} = \mu_{RexS10} // do this for NC, EC, EPC
wilcox.test(ascii_node2, ascii10_node, paired=TRUE, exact=FALSE, correct=FALSE)
wilcox.test(ascii_edge2, ascii10_edge, paired=TRUE, exact=FALSE, correct=FALSE)
wilcox.test(ascii_epair2, ascii10_epair, paired=TRUE, exact=FALSE, correct=FALSE)

cliff.delta(ascii_node2,ascii10_node) ##negligible
cliff.delta(ascii_edge2,ascii10_edge) ##negligible
cliff.delta(ascii_epair2,ascii10_epair) ## negligible


# H_0: \mu_{Repo2T} = \mu_{RexS5} // do this for NC, EC, EPC
wilcox.test(ascii_node3, ascii5_node, paired=TRUE, exact=FALSE, correct=FALSE)
wilcox.test(ascii_edge3, ascii5_edge, paired=TRUE, exact=FALSE, correct=FALSE)
wilcox.test(ascii_epair3, ascii5_epair, paired=TRUE, exact=FALSE, correct=FALSE)

cliff.delta(ascii_node3,ascii5_node) ##negligible
cliff.delta(ascii_edge3,ascii5_edge) ##negligible
cliff.delta(ascii_epair3,ascii5_epair) ## negligible


# H_0: \mu_{Repo2T} = \mu_{RexS1} // do this for NC, EC, EPC
wilcox.test(ascii_node3, ascii_node, paired=TRUE, exact=FALSE, correct=FALSE)
wilcox.test(ascii_edge3, ascii_edge, paired=TRUE, exact=FALSE, correct=FALSE)
wilcox.test(ascii_epair3, ascii_epair, paired=TRUE, exact=FALSE, correct=FALSE)

cliff.delta(ascii_node3,ascii_node) ##negligible
cliff.delta(ascii_edge3,ascii_edge) ##negligible
cliff.delta(ascii_epair3,ascii_epair) ## negligible

# H_0: \mu_{Repo2T} = \mu_{RexS10} // do this for NC, EC, EPC
wilcox.test(ascii_node3, ascii10_node, paired=TRUE, exact=FALSE, correct=FALSE)
wilcox.test(ascii_edge3, ascii10_edge, paired=TRUE, exact=FALSE, correct=FALSE)
wilcox.test(ascii_epair3, ascii10_epair, paired=TRUE, exact=FALSE, correct=FALSE)

cliff.delta(ascii_node3,ascii10_node) ##negligible
cliff.delta(ascii_edge3,ascii10_edge) ##negligible
cliff.delta(ascii_epair3,ascii10_epair) ## negligible


# H_0: \mu_{Repo2T} = \mu_{Repo1T} // do this for NC, EC, EPC
wilcox.test(ascii_node3, cov_node1, paired=FALSE, exact=FALSE, correct=FALSE, conf.level=0.95)
wilcox.test(ascii_edge3, cov_edge1, paired=FALSE, exact=FALSE, correct=FALSE, conf.level=0.95)
wilcox.test(ascii_epair3, cov_epair1, paired=FALSE, exact=FALSE, correct=FALSE, conf.level=0.95)

cliff.delta(ascii_node3,cov_node1) ##negligible
cliff.delta(ascii_edge3,cov_edge1) ##negligible
cliff.delta(ascii_epair3,cov_epair1) ## negligible

# H_0: \mu_{Repo2S} = \mu_{Repo1S} // do this for NC, EC, EPC
wilcox.test(ascii_node2, cov_node, paired=FALSE, exact=FALSE, correct=FALSE, conf.level=0.95)
wilcox.test(ascii_edge2, cov_edge, paired=FALSE, exact=FALSE, correct=FALSE, conf.level=0.95)
wilcox.test(ascii_epair2, cov_epair, paired=FALSE, exact=FALSE, correct=FALSE, conf.level=0.95)

cliff.delta(ascii_node2,cov_node) ##negligible
cliff.delta(ascii_edge2,cov_edge) ##negligible
cliff.delta(ascii_epair2,cov_epair) ## negligible


# H_0: \mu_{Repo2S} = \mu_{Repo2T} // do this for NC, EC, EPC
wilcox.test(ascii_node2, ascii_node3, paired=TRUE, exact=FALSE, correct=FALSE)
wilcox.test(ascii_edge2, ascii_edge3, paired=TRUE, exact=FALSE, correct=FALSE)
wilcox.test(ascii_epair2, ascii_epair3, paired=TRUE, exact=FALSE, correct=FALSE)

cliff.delta(ascii_node2,ascii_node3) ##negligible
cliff.delta(ascii_edge2,ascii_edge3) ##negligible
cliff.delta(ascii_epair2,ascii_epair3) ## negligible


names_f=c("Repo1T","Repo2T","Repo2S","RexS1","RexS5","RexS10")
names_r=c(expression(Repo[A]~"S"), expression(Repo[B]~"S"), expression(Repo[B]~"M"),"Rex1M","Rex5M","Rex10M")

names_f2=c("Repo2T","Repo2S","RexS1","RexS5","RexS10")
names_r2=c(expression(Repo[B]~"S"), expression(Repo[B]~"M"),"Rex1M","Rex5M","Rex10M")

nc1=data.frame(value=cov_node1)
nc1$type="Repo1T"
nc2=data.frame(value=ascii_node3)
nc2$type="Repo2T"
nc3=data.frame(value=ascii_node2)
nc3$type="Repo2S"
nc4=data.frame(value=ascii_node)
nc4$type="RexS1"
nc5=data.frame(value=ascii5_node)
nc5$type="RexS5"
nc6=data.frame(value=ascii10_node)
nc6$type="RexS10"
nc_ascii=rbind(nc1,nc2,nc3,nc4,nc5,nc6)
nc_ascii$factor<-factor(nc_ascii$type, levels=names_f)
nc_ascii2=rbind(nc2,nc3,nc4,nc5,nc6)
nc_ascii2$factor<-factor(nc_ascii2$type, levels=names_f2)

ec1=data.frame(value=cov_edge1)
ec1$type="Repo1T"
ec2=data.frame(value=ascii_edge3)
ec2$type="Repo2T"
ec3=data.frame(value=ascii_edge2)
ec3$type="Repo2S"
ec4=data.frame(value=ascii_edge)
ec4$type="RexS1"
ec5=data.frame(value=ascii5_edge)
ec5$type="RexS5"
ec6=data.frame(value=ascii10_edge)
ec6$type="RexS10"
ec_ascii=rbind(ec1,ec2,ec3,ec4,ec5,ec6)
ec_ascii$factor<-factor(ec_ascii$type, levels=names_f)
ec_ascii2=rbind(ec2,ec3,ec4,ec5,ec6)
ec_ascii2$factor<-factor(ec_ascii2$type, levels=names_f2)

epc1=data.frame(value=cov_epair1)
epc1$type="Repo1T"
epc2=data.frame(value=ascii_epair3)
epc2$type="Repo2T"
epc3=data.frame(value=ascii_epair2)
epc3$type="Repo2S"
epc4=data.frame(value=ascii_epair)
epc4$type="RexS1"
epc5=data.frame(value=ascii5_epair)
epc5$type="RexS5"
epc6=data.frame(value=ascii10_epair)
epc6$type="RexS10"
epc_ascii=rbind(epc1,epc2,epc3,epc4,epc5,epc6)
epc_ascii$factor<-factor(epc_ascii$type, levels=names_f)
epc_ascii2=rbind(epc2,epc3,epc4,epc5,epc6)
epc_ascii2$factor<-factor(epc_ascii2$type, levels=names_f2)


pdf(file='rexCovASCII.pdf', onefile=T, width=7,height=3) 
par(mfrow = c(1, 3),oma=c(0,0,0,0),mar=c(4.5, 5, 2, 0.5),las=1)
boxplot(nc_ascii$value~nc_ascii$factor, names=names_r, col=(c("palegreen1","palegreen2","palegreen3","lightskyblue1","lightskyblue2","lightskyblue3")), main="Node", boxwex=wid, ylab="", xlab="Node Coverage(%)", horizontal=TRUE) #names=c("total","success","failure")
axis(1, at=seq(0,100,10))
boxplot(ec_ascii$value~ec_ascii$factor, names=names_r, col=(c("palegreen1","palegreen2","palegreen3","lightskyblue1","lightskyblue2","lightskyblue3")), main="Edge", boxwex=wid,  ylab="", xlab="Edge Coverage(%)", horizontal=TRUE)
axis(1, at=seq(0,100,10))
boxplot(epc_ascii$value~epc_ascii$factor, names=names_r, col=(c("palegreen1","palegreen2","palegreen3","lightskyblue1","lightskyblue2","lightskyblue3")),  main="Edge-Pair", boxwex=wid, ylab="", xlab="Edge-Pair Coverage(%)", horizontal=TRUE)
axis(1, at=seq(0,100,10))
dev.off()

#pdf(file='rexCovASCII2.pdf', onefile=T, width=7,height=2) 
cairo_pdf(file='rexCovASCII2.pdf', onefile=T, width=7,height=2) 
par(mfrow = c(1, 3),oma=c(0,0,0,0),mar=c(4.5, 5, 2, 0.5),las=1)
boxplot(nc_ascii2$value~nc_ascii2$factor, names=names_r2, col=(c("palegreen1","palegreen2","lightskyblue1","lightskyblue2","lightskyblue3")), main="Node", boxwex=wid, ylab="", xlab="Node Coverage(%)", horizontal=TRUE) #names=c("total","success","failure")
axis(1, at=seq(0,100,10))
boxplot(ec_ascii2$value~ec_ascii2$factor, names=names_r2, col=(c("palegreen1","palegreen2","lightskyblue1","lightskyblue2","lightskyblue3")), main="Edge", boxwex=wid,  ylab="", xlab="Edge Coverage(%)", horizontal=TRUE)
axis(1, at=seq(0,100,10))
boxplot(epc_ascii2$value~epc_ascii2$factor, names=names_r2, col=(c("palegreen1","palegreen2","lightskyblue1","lightskyblue2","lightskyblue3")),  main="Edge-Pair", boxwex=wid, ylab="", xlab="Edge-Pair Coverage(%)", horizontal=TRUE)
axis(1, at=seq(0,100,10))
dev.off()

covs_ascii=data.frame(Node=ascii_node,Edge=ascii_edge,Epair=ascii_epair)
covs_ascii2=data.frame(Node=ascii_node2,Edge=ascii_edge2,Epair=ascii_epair2)
covs_ascii=melt(covs_ascii)
covs_ascii2=melt(covs_ascii2)

wid=0.3
#boxwex=wid
x11(width=7,height=7)
# postscript(paste(paste("rex","covASCII_s1",sep="_"),"eps",sep="."),width=7,height=7)
pdf(file='rexCovASCIIS1.pdf', onefile=T, width=7,height=7) 
par(mfrow = c(1, 2),oma=c(0,0,2,0))
boxplot(covs_ascii2$value~covs_ascii2$variable, main="Repo", ylim=c(0,100), xlab="", ylab="Coverage(%)", horizontal=FALSE) #names=c("total","success","failure")
axis(2, at=seq(0,100,10)) 
boxplot(covs_ascii$value~covs_ascii$variable, main="Rex in ASCII",ylim=c(0,100), xlab="", ylab="Coverage(%)", horizontal=FALSE)
axis(2, at=seq(0,100,10)) 
# boxplot(nc_ascii$value~nc_ascii$variable, main="Node", boxwex=wid, ylim=c(0,100), xlab="", ylab="Node Coverage(%)", horizontal=FALSE) #names=c("total","success","failure")
# axis(2, at=seq(0,100,10)) 
# boxplot(ec_ascii$value~ec_ascii$variable, main="Edge", boxwex=wid, ylim=c(0,100), xlab="", ylab="Edge Coverage(%)", horizontal=FALSE)
# axis(2, at=seq(0,100,10)) 
# boxplot(epc_ascii$value~epc_ascii$variable, main="Edge pair", boxwex=wid, ylim=c(0,100), xlab="", ylab="Edge pair Coverage(%)", horizontal=FALSE)
# axis(2, at=seq(0,100,10)) 
dev.off()



nc_unicode=data.frame(repo=unicode_node2,rex=unicode_node)
nc_unicode=melt(nc_unicode)
ec_unicode=data.frame(repo=unicode_edge2,rex=unicode_edge)
ec_unicode=melt(ec_unicode)
epc_unicode=data.frame(repo=unicode_epair2,rex=unicode_epair)
epc_unicode=melt(epc_unicode)

covs_unicode=data.frame(Node=unicode_node,Edge=unicode_edge,Epair=unicode_epair)
covs_unicode2=data.frame(Node=unicode_node2,Edge=unicode_edge2,Epair=unicode_epair2)
covs_unicode=melt(covs_unicode)
covs_unicode2=melt(covs_unicode2)

# postscript(paste(paste("rex","covUnicode_s1",sep="_"),"eps",sep="."))
pdf(file='rexCovUnicodeS1.pdf', onefile=T, width=7,height=7) 
par(mfrow = c(1, 2),oma=c(0,0,2,0))
boxplot(covs_unicode2$value~covs_unicode2$variable, main="Repo", ylim=c(0,100), xlab="", ylab="Coverage(%)", horizontal=FALSE) #names=c("total","success","failure")
axis(2, at=seq(0,100,10)) 
boxplot(covs_unicode$value~covs_unicode$variable, main="Rex in Unicode",ylim=c(0,100), xlab="", ylab="Coverage(%)", horizontal=FALSE)
axis(2, at=seq(0,100,10)) 
# boxplot(nc_unicode$value~nc_unicode$variable, main="Node", ylim=c(0,100), xlab="", ylab="Node Coverage(%)", horizontal=FALSE) #names=c("total","success","failure")
# axis(2, at=seq(0,100,10)) 
# boxplot(ec_unicode$value~ec_unicode$variable, main="Edge", ylim=c(0,100), xlab="", ylab="Edge Coverage(%)", horizontal=FALSE)
# axis(2, at=seq(0,100,10)) 
# boxplot(epc_unicode$value~epc_unicode$variable, main="Edge pair", ylim=c(0,100), xlab="", ylab="Edge pair Coverage(%)", horizontal=FALSE)
# axis(2, at=seq(0,100,10)) 
dev.off()