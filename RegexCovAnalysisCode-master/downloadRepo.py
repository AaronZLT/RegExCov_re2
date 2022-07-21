import os
import sys
from LogUtils import closeLog
from LogUtils import createLog
import csv

ws="/home/peipei/RepoReaper/" ##workspace
file_dir="/home/peipei/ISSTA2018/data/valid_repo_pom/"
log_dir="/home/peipei/RepoReaper/loggings/"
# ws="/home/pwang7/RepoReaper/" ##workspace
# file_dir="/home/pwang7/results/"
# log_dir="/home/pwang7/log/"
#file_suffix="_bref.csv"
file_suffix="_pom.csv"


def download_repo(i,r,string_url,log):
    if os.path.exists(str(i)+"_"+str(r)):
        return
    ##add username:password for https://github.com
#     string_url="https://wangpeipei90:jiangzhen123456@"+string_url[8:]
    cmd_git="git clone "+string_url+".git "+str(i)+"_"+str(r)    
    log.info(cmd_git)

    status_git=os.system(cmd_git)
    log.info("git status: "+str(status_git))
    print("git status: "+str(status_git))

def download_page(i):
    filename=file_dir+str(i)+file_suffix ##/home/peipei/RepoReaper/RegexCollection/1_bref.csv
    log,fh = createLog(log_dir+str(i)+".log")
    with open(filename, 'r') as csvfile:
        spamreader = csv.reader(csvfile, dialect='excel')
        for row in spamreader:
            print(row)
            r,repo,valid_url,string_url,valid_api,string_api,=row[0:6]
            r=int(r)
            valid_url= valid_url=='True'
            valid_api= valid_api=='True'
            
            if valid_url and valid_api:
                download_repo(i,r,string_url,log)
            elif not valid_url:  ## if the url is not valid we could not download
                log.error("Repo URL is not valid for download")
            elif not valid_api:
                log.error("API URL is not valid for download")
                
    closeLog(log,fh)


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
        download_page(page)
