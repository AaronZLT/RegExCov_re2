import os
import shutil
import sys
from LogUtils import closeLog
from LogUtils import createLog
from MavenUtils import isMaven,calRegex
import csv
from multiprocessing import Pool

ws="/home/peipei/RepoReaper/" ##workspace
file_dir="/home/peipei/RepoReaper/RegexCollection/"
log_dir="/home/peipei/RepoReaper/loggings/"
# ws="/home/pwang7/RepoReaper/" ##workspace
# file_dir="/home/pwang7/results/"
# log_dir="/home/pwang7/log/"
file_suffix="_bref.csv"

def filterPom(i):
    filename=file_dir+str(i)+file_suffix ##/home/peipei/RepoReaper/RegexCollection/1_bref.csv
    log,fh = createLog(log_dir+str(i)+".log")
    hasPoms=list()
    with open(filename, 'r') as csvfile:
        spamreader = csv.reader(csvfile, dialect='excel')
        for row in spamreader:
            repo_dir=str(i)+"_"+str(row[0])
            if os.path.exists(repo_dir):
                count_xml,errxml=isMaven(repo_dir, log)
                count_regex,err_regex=calRegex(repo_dir,r'java.util.regex.*',log)
                count_matches,err_matches=calRegex(repo_dir,r'.matches(',log)
                if count_xml==0:
                    log.info("delete the directory %s because no pom.xml in its repo" %repo_dir)
                    shutil.rmtree(repo_dir,ignore_errors=False,onerror=None) ## since no pom.xml we do not spend time on it
                elif count_regex==0:
                    log.info("delete the directory %s because no regex is used in its repo" %repo_dir)
                    shutil.rmtree(repo_dir,ignore_errors=False,onerror=None) ## since no pom.xml we do not spend time on it
                elif count_matches==0:
                    log.info("delete the directory %s because no regex full matches is used in its repo" %repo_dir)
                    shutil.rmtree(repo_dir,ignore_errors=False,onerror=None) ## since no pom.xml we do not spend time on it
                else:
                    log.info("There are %d pom.xml in the directory %s"%(count_xml,repo_dir))
                    row.append(count_regex)
                    row.append(count_matches)
                    row.append(count_xml)
                    hasPoms.append(row)
    closeLog(log,fh)

    file_name=file_dir+str(i)+"_pom.csv"
    with open(file_name,'w') as resultFile:
        wr = csv.writer(resultFile, dialect='excel')
        wr.writerows(hasPoms)
        
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
    pool = Pool(processes=2)            # start 4 worker processes ##intotal it has 4 cores
    print(pool.map(filterPom, range(int(begin),int(end))))       # prints "[0, 1, 4,..., 81]"
    pool.terminate()
#     for page in range(begin,end):
#         filterPom(page)
