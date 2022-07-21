'''
Created on Mar 4, 2018

@author: peipei
'''
import os
import glob
import csv
import pickle
ws1="/home/peipei/ISSTA2018/data/valid_repo_pom/"
ws2="/home/peipei/ISSTA2018/data/regex/"
file_suffix="_pom.csv"

def untestedProjects(ws=ws1):
    os.chdir(ws)
    files=glob.glob("*_pom.csv")
    count=0
    count2=0
    for filename in files:
        index=int(filename[:-8])
        
        with open(filename, 'r') as csvfile:
            spamreader = csv.reader(csvfile, dialect='excel')
            for row in spamreader:
                isvalidUrl, isvalidApi=row[2], row[4]
                n_regex, n_match, n_xml=int(row[8]), int(row[9]), int(row[10])
                
                if isvalidApi and isvalidUrl:
                    if n_regex>0 and n_match>0 and n_xml>0:
                        count+=1
                        if index<1950:
                            count2+=1
    print("count:",count)
    print("count2:",count2)

def getTestedRepos(ws=ws2):
    os.chdir(ws)
    filename="stack_info.csv"
    page_rows=dict()
    with open(filename, 'r') as csvfile:
            spamreader = csv.reader(csvfile, dialect='excel')
            for row in spamreader:
                repo_page, repo_row=int(row[2]), int(row[3])
                if repo_page not in page_rows:
                    page_rows[repo_page]=set([repo_row])
                else:
                    page_rows[repo_page].add(repo_row)
    return page_rows

def getCleanedRepos(ws=ws2):
    os.chdir(ws)
    clean_df=pickle.load(open("clean.df",'rb'))
    repos=clean_df.groupby(['page','row'])
    
    page_rows=dict()
    for repo in repos.groups.keys():
        repo_page, repo_row=repo
        if repo_page not in page_rows:
            page_rows[repo_page]=set([repo_row])
        else:
            page_rows[repo_page].add(repo_row)
    return page_rows
   
def untestedRegex(page_rows,ws=ws1):
    os.chdir(ws)
    count,size=0,0
    match_count=dict()
    for page,rows in page_rows.items():
        size+=len(rows)
        
        filename=str(page)+"_pom.csv"        
        with open(filename, 'r') as csvfile:
            spamreader = csv.reader(csvfile, dialect='excel')
            for row in spamreader:
                row_number, n_match=int(row[0]), int(row[9])
                if row_number in rows:
                    count+=n_match
                    match_count[(page,row_number)]=n_match
    
    print("total projects: ",size)
    print("total regex matches: ",count)
    
    with open(ws2+"callsite_valid", 'w') as myfile:
        wr2 = csv.writer(myfile, dialect='excel')
        for repo,n_match in match_count.items():
            page,row=repo
            wr2.writerow([page,row,n_match])    

def untestedCallSite(ws=ws2):
    os.chdir(ws)
    filename="valid.df"
    valid_df=pickle.load(open(filename,"rb"))
    stacks=valid_df.groupby(['page','row','file','class','method','regex'])
    print("number of unique regex stacks: ",len(stacks))


    callSites=valid_df.groupby(['file','class','method'])
    print("number of callSites: ", len(callSites.groups))
    
    res=[]
    for callSite, group in callSites:
        repos=group.groupby(['page','row'])
        if len(repos.groups)>1:
            print("alarm one call site, multiple repos: ", callSite,repos.groups.keys())
        uniRegex=group['regex'].unique()
        res.append(len(uniRegex))
    
    with open("callsite_regex", 'w') as myfile:
        wr2 = csv.writer(myfile, dialect='excel')
        for num_regex in res:
            wr2.writerow([num_regex])    
 
def testedCallSites(ws=ws2):
    os.chdir(ws)
    filename="valid.df"
    valid_df=pickle.load(open(filename,"rb"))
    
    res=[]
    repos=valid_df.groupby(['page','row'])
    for repo,group in repos:
        callSites=group.groupby(['file','class','method'])
        res.append(len(callSites))
    
    with open("callsite_tested", 'w') as myfile:
        wr2 = csv.writer(myfile, dialect='excel')
        for num_regex in res:
            wr2.writerow([num_regex])    
                 
if __name__ == '__main__':
#     untestedProjects(ws1)
    testedCallSites(ws2)
    
#     page_rows=getTestedRepos(ws2)
# #     page_rows=getCleanedRepos(ws2)
#     untestedRegex(page_rows,ws1)    
#     untestedCallSite(ws2)
                        