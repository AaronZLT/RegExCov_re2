import os
import sys
from LogUtils import closeLog, createLog
import csv
from lib2to3.fixes import fix_tuple_params
from readHTML_token import visitAPI
ws="/home/peipei/ISSTA2018/data/valid_repo_pom/"
output_dir="/home/peipei/ISSTA2018/data/"
file_suffix="_pom.csv"
detail_dir="/home/peipei/ISSTA2018/data/valid_repo_java/detail/"
detail_suffix="_detail.csv"

def readPoms(num=4495):
    pom_lists=[]
    for i in range(1,num+1):
        filename=ws+str(i)+file_suffix
        with open(filename, 'r') as csvfile:
            spamreader = csv.reader(csvfile, dialect='excel')
            for row in spamreader:            
                r=int(row[0])
                print("page: ",i," row: ",r)
                junitTest=float(row[6])
                stars=0 if row[7]=='NA' else int(row[7])
                count_regex=int(row[8])
                count_matches=int(row[9])
                count_xml=int(row[10])
                pom_lists.append((i,r,junitTest,stars,count_regex,count_matches,count_xml))
#     return pom_lists    
    file_name=output_dir+"pom_starTest.csv"
    with open(file_name,'w') as resultFile:
        wr = csv.writer(resultFile, dialect='excel')
        wr.writerow(["page","row","test_ratio","stars","#regex","#matches","#xml"])
        wr.writerows(pom_lists)

def apiPomStarSize(num=4495):
    pom_lists=[]
    for i in range(1,num+1):
        filename=ws+str(i)+file_suffix
        with open(filename, 'r') as csvfile:
            spamreader = csv.reader(csvfile, dialect='excel')
            for row in spamreader:            
                r=int(row[0])
                print("page: ",i," row: ",r)
                api_url=row[5]
                res=visitAPI(i,r,api_url)
                if res is not None:
                    star,watcher,size=res
                    print("page: ",i," row: ",r," star: ",star," watcher: ",watcher, "size: ",size)
                    pom_lists.append((i,r,star,watcher,size))
                else:
                    pom_lists.append((i,r,-1,-1,-1))
#     return pom_lists
    file_name=output_dir+"pom_byAPIVisit.csv"
    with open(file_name,'w') as resultFile:
        wr = csv.writer(resultFile, dialect='excel')
        wr.writerow(["page","row","stars","watcher","size"])
        wr.writerows(pom_lists)
def readRepoSize():
    pom_lists=readPoms()
    pom_size=[]
    for info in pom_lists:
        i,r=info[0:2]
        filename=detail_dir+str(i)+detail_suffix
        with open(filename, 'r') as csvfile:
            spamreader = csv.reader(csvfile, dialect='excel')
            for row in spamreader:
                if r==int(row[0]):
                    size=row[8]
                    if size !="NA":
                        size=int(size.replace(',',''))
                    pom_size.append((i,r,size))
#     return pom_size   
    
    file_name=output_dir+"pom_size.csv"
    with open(file_name,'w') as resultFile:
        wr = csv.writer(resultFile, dialect='excel')
        wr.writerow(["page","row","size"])
        wr.writerows(pom_size)               
    
def rankPom():
    pom_lists=readPoms()             
#     sorted_tests=sorted(pom_lists, cmp=byTest, reverse=True)
    sorted_tests=sorted(pom_lists, key=lambda x: (x[2],x[3]), reverse=True)
    file_name=output_dir+"pom_byTest.csv"
    with open(file_name,'w') as resultFile:
        wr = csv.writer(resultFile, dialect='excel')
        wr.writerow(["page","row","test_cov","stars","#regex","#matches","#xml"])
        wr.writerows(sorted_tests)  
    #     sorted_stars=sorted(pom_lists, cmp=byStar, reverse=True)
    sorted_stars=sorted(pom_lists, key=lambda x: (x[3],x[2]), reverse=True)
    def switch(x_tuple):
        x=list(x_tuple)
        x[2],x[3]=x[3],x[2] ##switch column
        return tuple(x)
    sorted_stars=[switch(x_tuple) for x_tuple in sorted_stars]    
    file_name=output_dir+"pom_byStar.csv"
    with open(file_name,'w') as resultFile:
        wr = csv.writer(resultFile, dialect='excel')
        wr.writerow(["page","row","stars","test_cov","#regex","#matches","#xml"])
        wr.writerows(sorted_stars)
            
if __name__== '__main__':
#     rankPom()
    readPoms()
#     readRepoSize()
#     visitAPI(2620, 120, "https://api.github.com/repos/veegit/VenmoPay")
#     apiPomStarSize()
