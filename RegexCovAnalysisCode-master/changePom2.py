import os
import sys
from LogUtils import closeLog, createLog
from PomUtils import agent_pom,mvn_pom
from MavenUtils import sortPom
import csv
import shutil

ws="/home/peipei/RepoReaper/" ##workspace
file_dir="/home/peipei/ISSTA2018/data/valid_pom_mvn/"
log_dir="/home/peipei/RepoReaper/loggings/"
output_dir="/home/peipei/ISSTA2018/data/valid_pom_jar/"
# ws="/home/pwang7/RepoReaper/" ##workspace
# file_dir="/home/pwang7/results/"
# log_dir="/home/pwang7/log/"
# output_dir="/home/pwang7/results/"
file_suffix="_mvn.csv"

def changePom(i):
    filename=file_dir+str(i)+file_suffix ##/home/peipei/RepoReaper/RegexCollection/1_bref.csv
    log,fh = createLog(log_dir+str(i)+".log")
    results=list()
    with open(filename, 'r') as csvfile:
        spamreader = csv.reader(csvfile, dialect='excel')
        for row in spamreader:            
            r,pom_need,compiled,tested,count_xml=row[:5]
            repo_dir=str(i)+"_"+str(row[0])            
            pom_need,compiled,tested=int(pom_need),int(compiled),int(tested)
            count_xml=int(count_xml)
#             if pom_need>compiled or pom_need>tested:
#                 log.info("The repo %s has compilation or test error before changing pom"%repo_dir)
#                  
#                 continue
            os.chdir(ws+repo_dir)
            log.info("Changing Pom.xml files in directory %s" %repo_dir)
            
            output_sorts,err_sort=sortPom(log)
            print("output_sorts len: ",len(output_sorts))
            print("output_sorts: ",output_sorts)
            ##modify and change every found pom.xml
            d=0
            jdk=None
            while d<count_xml:
                cur_dir=output_sorts[2*d+1].decode('utf-8')
                print("count: ",count_xml,"d: ",d," cur_dir: ",cur_dir)
                
                pom_file=cur_dir+"/pom.xml"
                if os.stat(pom_file).st_size==0 or "archetype-resources" in cur_dir: ##ignore archetype
                    d+=1
                    continue
                
                jdk_temp=mvn_pom(pom_file,repo_dir,log)
                agent_pom(pom_file,repo_dir,d,log)
                print(jdk_temp)
                if jdk is None and jdk_temp is not None:
                    jdk=jdk_temp
                elif jdk is not None and jdk_temp is not None:
                    if jdk<jdk_temp:
                        jdk=jdk_temp
                d+=1
            
            if jdk is None:
                jdk='NA' 
            log.info("Changed all pom.xml directory %s" %repo_dir)
            print("Changed all pom.xml directory %s" %repo_dir)
            t=[r,pom_need,compiled,tested,jdk,count_xml]
            t.extend(row[5:])      
            results.append(tuple(t))
#             log.info("Changed pom in directory %s" %repo_dir)

    closeLog(log,fh)
    file_name=output_dir+str(i)+"_jar.csv"
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
        changePom(page)
