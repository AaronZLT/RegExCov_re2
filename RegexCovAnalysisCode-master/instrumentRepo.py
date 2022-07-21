import os
import sys
from LogUtils import closeLog,createLog
from MavenUtils import compileRepo,testRepo
import csv

ws="/home/peipei/RepoReaper/" ##workspace
file_dir="/home/peipei/ISSTA2018/data/valid_pom_jar/"
output_dir="/home/peipei/ISSTA2018/data/valid_pom_agent/"
log_dir="/home/peipei/RepoReaper/loggings/"
timeout_log="/home/peipei/RepoReaper/loggings/timeout.log"
#ws="/home/pwang7/RepoReaper/" ##workspace
#file_dir="/home/pwang7/results/"
#log_dir="/home/pwang7/log/"
#timeout_log="/home/pwang7/log/timeout.log"
file_suffix="_jar.csv"

def instrumentPom(i):
    filename=file_dir+str(i)+file_suffix ##/home/peipei/RepoReaper/RegexCollection/1_bref.csv
    log,fh = createLog(log_dir+str(i)+".log")
    results=list()
    timelog, timefh = createLog(timeout_log)
    
#     flag=False
    with open(filename, 'r') as csvfile:
        spamreader = csv.reader(csvfile, dialect='excel')
        for row in spamreader:
            r,pom_need,compiled,tested,jdkversion,count_xml=row[:6]
            repo_dir=str(i)+"_"+str(row[0])
#             if repo_dir!="20_7":
#                 break
            pom_need,compiled,tested=int(pom_need),int(compiled),int(tested)

            log.info("ReProcessing directory %s" %repo_dir)
            print("ReProcessing directory %s" %repo_dir)
            os.chdir(ws+repo_dir)
            cur_cwd=os.getcwd()
                      
            pom_dirs=row[6:]
            d=0
            dirs=list()
            compiled2=0
            tested2=0
            while d<pom_need: ##even is depth and odd is dirpath                
                cur_dir=pom_dirs[d]
                os.chdir(cur_dir)
                    
                if compileRepo(repo_dir,cur_dir,log,timelog):
                    compiled2+=1
                if testRepo(repo_dir,log,timelog):
                    tested2+=1
                    dirs.append(cur_dir)
                d+=1                      
                os.chdir(cur_cwd)
                                
            elem=[row[0],pom_need,compiled2,tested2]
            elem.extend(dirs)     
            results.append(tuple(elem))    
            log.info("ReProcessed directory %s" %repo_dir)
            
    closeLog(log,fh)
    closeLog(timelog,timefh)

    file_name=output_dir+str(i)+"_agent.csv"
    with open(file_name,'w') as resultFile:
        wr = csv.writer(resultFile, dialect='excel')
        wr.writerows(results)
        
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
        instrumentPom(page)
