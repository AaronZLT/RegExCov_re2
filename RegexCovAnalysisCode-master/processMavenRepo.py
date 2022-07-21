import os
import shutil
import sys
from LogUtils import closeLog
from LogUtils import createLog
from MavenUtils import isMaven,sortPom,compileRepo,testRepo
from PomUtils import mvn_pom
import csv

ws="/home/peipei/RepoReaper/" ##workspace
file_dir="/home/peipei/ISSTA2018/data/valid_repo_pom/"
log_dir="/home/peipei/RepoReaper/loggings/"
timeout_log="/home/peipei/RepoReaper/loggings/timeout.log"
output_dir="/home/peipei/ISSTA2018/data/valid_pom_mvn/"
# ws="/home/pwang7/RepoReaper/" ##workspace
# file_dir="/home/pwang7/results/"
# log_dir="/home/pwang7/log/"
# timeout_log="/home/pwang7/log/timeout.log"
# output_dir="/home/pwang7/results/"
file_suffix="_pom.csv"



def mavenPom(i):
    filename=file_dir+str(i)+file_suffix ##/home/peipei/RepoReaper/RegexCollection/1_bref.csv
    log,fh = createLog(log_dir+str(i)+".log")
    results=list()
    timelog, timefh = createLog(timeout_log)
    
#     flag=False
    with open(filename, 'r') as csvfile:
        spamreader = csv.reader(csvfile, dialect='excel')
        for row in spamreader:
            repo_dir=str(i)+"_"+str(row[0])
            
#             if not flag:
#                 flag= repo_dir == '1_122'
#             
#             if not flag:
#                 continue
            if i==79 and repo_dir!='79_176':
                continue  
            count_regex,count_matches,count_xml=int(row[-3]),int(row[-2]),int(row[-1])

            log.info("Processing directory %s" %repo_dir)
            print("Processing directory %s" %repo_dir)
            os.chdir(ws+repo_dir)

            output_sorts,err_sort=sortPom(log)            
                
            min_depth=int(output_sorts[0].decode('utf-8'))
            pom_dir=output_sorts[1].decode('utf-8')

            if pom_dir==".":
                pom_need=1                
                if not compileRepo(repo_dir,pom_dir,log,timelog):
                    elem=(row[0],pom_need,0,0,count_xml,pom_dir)
                    results.append(elem)
                    continue
                if not testRepo(repo_dir,log,timelog):
                    elem=(row[0],pom_need,1,0,count_xml,pom_dir)
                    results.append(elem)
                    continue
                else:
                    elem=(row[0],pom_need,1,1,count_xml,pom_dir)
                    results.append(elem)
                    continue
            else:
                pom_need=0
                compiled=0
                tested=0
                
                cur_cwd=os.getcwd()
                
                dirs=list()
                d=0
                while d<count_xml: ##even is depth and odd is dirpath
                    cur_depth=int(output_sorts[2*d].decode('utf-8'))  ##min_depth could be start to be 2 and have parallel sub projects
                    if cur_depth>min_depth:
                        break
                    
                    pom_need+=1
                    cur_dir=output_sorts[2*d+1].decode('utf-8')
                    print("d: ",d," cur_dir: ",cur_dir)
                    os.chdir(cur_dir)
                    dirs.append(cur_dir)
                       
                    if compileRepo(repo_dir,cur_dir,log,timelog):
                        compiled+=1
                        if testRepo(repo_dir,log,timelog):
                            tested+=1
                    d+=1
                    os.chdir(cur_cwd)  
                             
                elem=[row[0],pom_need,compiled,tested,count_xml]
                elem.extend(dirs)     
                results.append(tuple(elem))
            log.info("Processed directory %s" %repo_dir)
    closeLog(log,fh)
    closeLog(timelog,timefh)

    file_name=output_dir+str(i)+"_mvn.csv"
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
        mavenPom(page)
