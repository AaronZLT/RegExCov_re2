import os
import sys
from LogUtils import closeLog, createLog
from PomUtils import agent_pom
import csv
import shutil

# ws="/home/peipei/RepoReaper/" ##workspace
# file_dir="/home/peipei/ISSTA2018/data/valid_pom_mvn/"
# log_dir="/home/peipei/RepoReaper/loggings/"
ws="/home/pwang7/RepoReaper/" ##workspace
file_dir="/home/pwang7/results/"
log_dir="/home/pwang7/log/"
file_suffix="_mvn.csv"

def changePom(i):
    filename=file_dir+str(i)+file_suffix ##/home/peipei/RepoReaper/RegexCollection/1_bref.csv
    log,fh = createLog(log_dir+str(i)+".log")
    results=list()
    with open(filename, 'r') as csvfile:
        spamreader = csv.reader(csvfile, dialect='excel')
        for row in spamreader:            
            r,pom_need,compiled,tested,jdkversion, count_xml=row[:6]
            repo_dir=str(i)+"_"+str(row[0])
            

            pom_need,compiled,tested=int(pom_need),int(compiled),int(tested)

#             if pom_need>compiled or pom_need>tested:
#                 log.info("The repo %s has compilation or test error before changing pom"%repo_dir)
#                  
#                 continue
            
            log.info("Changing Pom.xml in directory %s" %repo_dir)
                      
            pom_dirs=row[6:]
            d=0
            while d<pom_need: ##even is depth and odd is dirpath     
                print("i: ",d," pom_need: ",pom_need)           
                cur_dir=pom_dirs[d]
                pom_file=ws+repo_dir+"/"+cur_dir+"/pom.xml"                
                agent_pom(pom_file,repo_dir,log)
                
                d+=1       
            results.append(row)
            log.info("Changed pom in directory %s" %repo_dir)

    closeLog(log,fh)
#     file_name=file_dir+str(i)+"_jar.csv"
#     with open(file_name,'w') as resultFile:
#         wr = csv.writer(resultFile, dialect='excel')
#         wr.writerows(results)
        
if __name__== '__main__':
    if sys.argv is None or len(sys.argv)<2: #(begin,end]
        sys.exit('Error! You need to specify one project ID or begin and end project ID!!')
    begin=int(sys.argv[1])
    end=begin
    
    if len(sys.argv)==3:
        end=int(sys.argv[2])
    elif len(sys.argv)==2:
        end=end+1
    print(begin, end)
    
    os.chdir(ws)
    for page in range(begin,end):
        changePom(page)
