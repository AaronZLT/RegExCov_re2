import csv
import pickle
import pandas as pd
import numpy as np
import re
import os
from analyzeRegex import getUniqueRegex
from itertools import count
from DFAUtils import CalculateCov
from analyzeDFA import getDFAIndex
from DFA import Coverage
from RegexStack import RegexStack
from math import sqrt

ws="/home/peipei/ISSTA2018/data/regex/" ##workspace
output_dir="/home/peipei/ISSTA2018/data/regex/"
drop_dir="/home/peipei/workspace/RepoReaperGithub2/"
output_coverage_dir="/home/peipei/ISSTA2018/data/cov/" 

def getDataFrameFromDF(regexFile):
    df=pd.read_pickle(regexFile)
    df=pickle.load(open(regexFile,'rb'))
#     df=pd.read_csv(regexFile)
#     df.input=df.input.fillna('')
    return df

def getCovByRegex(df):
    regexes=df.groupby('regex')
    regex_dict=dict()
    failed_regex=dict()
    str_length=dict()
    count=0
    
    file_name=output_coverage_dir+"regex_cov.csv"
    with open(file_name,'w') as resultFile:
        wr = csv.writer(resultFile, dialect='excel')
        wr.writerow(["index","c_node","t_node","c_edge","t_edge","c_epair","t_epair","type"])        
        
    for regex,group in regexes:
        if count<1003:
#             print("count: ",count," regex:",regex)
            count+=1
            continue
        print("count: ",count," regex:",regex)
        regex_dict[regex]=count
        uniInputs=group['input'].unique()   
        ret=CalculateCov(count,regex,uniInputs)
        if ret==1:
            failed_regex[count]=regex
        elif ret==2:
            str_length[count]=regex
        count+=1
    output=open(output_dir+"unique.regex",'wb')
    pickle.dump(regex_dict, output, pickle.HIGHEST_PROTOCOL)
    output.close()
    output=open(output_dir+"failed.regex",'wb')
    pickle.dump(failed_regex, output, pickle.HIGHEST_PROTOCOL)
    output.close()
    output=open(output_dir+"strlen.regex",'wb')
    pickle.dump(str_length, output, pickle.HIGHEST_PROTOCOL)
    output.close()
               
def getStatistics(df,column):
    colSeries=df[column].value_counts().sort_index()
    print("number of unique ",column," is: ",len(colSeries))
    colSeries.to_csv(output_dir+column+".csv")
    return colSeries
    
def getUniqueProj(df):
    projs=df.groupby(['page','row']).sum().sort_index()
    print("number of unique projects: ",len(projs))
    projs.to_csv(output_dir+"proj.csv")
    return projs

def getUniqueStackTrace(df):
    stacktraces=df.groupby(['file','class','method'])
    def getUniqueRegexPerStackTrace(group):
        return group['regex'].unique()
    
    stacktrace_dict=dict()
    for stacktrace,group in stacktraces:
        uniRegexes=getUniqueRegexPerStackTrace(group)
        stacktrace_dict[stacktrace]=len(uniRegexes)
    s_st=pd.Series(stacktrace_dict)
    s_st=s_st.sort_values(ascending=False)
    print("number of unique stacktrace: ",len(s_st))
    s_st.to_csv(output_dir+"stacktrace.csv")    
    return s_st                

def getCovByRepo(df,sdfas,ddfass,regex_all,regex_failed,regex_long):
    repos=df.groupby(['page','row'])
    projs=repos.sum().sort_index()
    print("number of unique projects: ",len(projs))
    projs.to_csv(output_dir+"proj.csv")
    
    regexPerRepo=[]
    file_name=output_coverage_dir+"repo_cov.csv"
    with open(file_name,'w') as resultFile:
        wr = csv.writer(resultFile, dialect='excel')
        wr.writerow(["page","row","index","c_node","t_node","c_edge","t_edge","c_epair","t_epair","type"])
               
    count=0
    for repo,group in repos:
        page,row=repo
        regex_groups=group.groupby("regex")
        regex_count=0
        failed=0
        for regex,regexgroup in regex_groups:
            regex_count+=1
            index=regex_all[regex]
            if index in regex_failed or index in regex_long:
                failed+=1
                continue
            
            uniInputs=regexgroup['input'].unique()
            sdfa=sdfas[index]
            ddfas=ddfass[index]
            coverages=getCovGivenInputs(uniInputs,sdfa,ddfas)
            saveCoverages(page,row,index,coverages)     
        count+=1
        regexPerRepo.append([page,row,regex_count,failed])
    
    file_name=output_dir+"repo_regex.csv"
    with open(file_name,'w') as resultFile:
        wr2 = csv.writer(resultFile, dialect='excel')
        for perRepo in regexPerRepo:
            wr2.writerow(perRepo)

def mean(s_list):
    return sum(s_list)/len(s_list)
def dev(s_list,mean):
    vars=[(s-mean)**2 for s in s_list]
    return sqrt(sum(vars))
    
def getStringInfoByStack(valid_df,sdfas,ddfass,regex_all):
    stacks=valid_df.groupby(['page','row','file','class','method','regex'])
    count=0
    print("number of unique regex stacks: ",len(stacks))
    repos=set()
    regexPerStack=dict()   
    stack_count=0
    dropped=0
    for stack,group in stacks:
        page,row,rfile,rclass,rmethod,regex=stack        
        repos.add((page,row))
        
        index=regex_all[regex]
        uniInputs=group['input'].unique()
        
        sdfa=sdfas[index]
        ddfas=ddfass[index]
        
        regex_size=len(regex)
        regex_size_dfa=len(sdfa.pattern)
        
        inputs_size=[len(input) for input in uniInputs]
        mean_inputs=mean(inputs_size)
        dev_inputs=dev(inputs_size,mean_inputs)

        valid_inputs=[input for input in uniInputs if input in ddfas]
        if len(valid_inputs)==0:
            print("drop stack index: ",stack_count)
            dropped+=1
            mean_succ=dev_succ="na"
            mean_fail=dev_fail="na"
        else:
            succ_size=[]
            fail_size=[]
            for input in valid_inputs:
                if ddfas[input].isMatch:
                    succ_size.append(len(input))
                else:
                    fail_size.append(len(input))
            if len(succ_size)==0:
                mean_succ=dev_succ="na"
            else:
                mean_succ=mean(succ_size)
                dev_succ=dev(succ_size,mean_succ)
            if len(fail_size)==0:
                mean_fail=dev_fail="na"
            else:
                mean_fail=mean(fail_size)
                dev_fail=dev(fail_size,mean_fail)
                  
        regexPerStack[stack_count]=[stack_count,index,page,row,regex_size,regex_size_dfa,len(inputs_size),mean_inputs,dev_inputs,mean_succ,dev_succ,mean_fail,dev_fail,len(valid_inputs)]
        stack_count+=1    
    
    print("total number of stack: ",stack_count)
    print("dropped stack because of dropped strings: ",dropped)
    file_name=output_dir+"stack_strLen.csv"
    with open(file_name,'w') as resultFile:
        wr2 = csv.writer(resultFile, dialect='excel')
        for index,stack in regexPerStack.items():
            wr2.writerow(stack)

def getNumInputsByStack(valid_df,sdfas,ddfass,regex_all):
    stacks=valid_df.groupby(['page','row','file','class','method','regex'])
    count=0
    print("number of unique regex stacks: ",len(stacks))
    repos=set()
    numInputsPerStack=dict()   
    stack_count=0
    dropped=0
    for stack,group in stacks:
        page,row,rfile,rclass,rmethod,regex=stack        
        repos.add((page,row))
        
        index=regex_all[regex]
        uniInputs=group['input'].unique()
        
        sdfa=sdfas[index]
        ddfas=ddfass[index]
        
        regex_size=len(regex)
        regex_size_dfa=len(sdfa.pattern)

        valid_inputs=[input for input in uniInputs if input in ddfas]
        if len(valid_inputs)==0:
            print("drop stack index: ",stack_count)
            dropped+=1
            numInputsPerStack[stack_count]=[stack_count,len(uniInputs),0,0,0]
        else:
            succ=0
            fail=0
            for input in valid_inputs:
                if ddfas[input].isMatch:
                    succ+=1
                else:
                    fail+=1                  
            numInputsPerStack[stack_count]=[stack_count,len(uniInputs),len(valid_inputs),succ,fail]
        stack_count+=1    
    
    print("total number of stack: ",stack_count)
    print("dropped stack because of dropped strings: ",dropped)
    
    output=open(output_dir+"stackCount.regex",'wb')
    pickle.dump(numInputsPerStack, output, pickle.HIGHEST_PROTOCOL)
    output.close()
    
    file_name=output_dir+"stack_count.csv"
    with open(file_name,'w') as resultFile:
        wr2 = csv.writer(resultFile, dialect='excel')
        for index,stack in numInputsPerStack.items():
            wr2.writerow(stack)            
def getCovByStack(valid_df,sdfas,ddfass,regex_all):
    stacks=valid_df.groupby(['page','row','file','class','method','regex'])
    count=0
    print("number of unique regex stacks: ",len(stacks))
#     stacks.to_csv(output_dir+"stacks.csv")
    repos=set()
    regexPerStack=dict()
    file_name=output_coverage_dir+"stack_cov.csv"
    with open(file_name,'w') as resultFile:
        wr = csv.writer(resultFile, dialect='excel')
        wr.writerow(["stack_index","regex_index","page","row","c_node","t_node","c_edge","t_edge","c_epair","t_epair","type","count"])
               
    stack_count=0
    dropped=0
    for stack,group in stacks:
        page,row,rfile,rclass,rmethod,regex=stack        
        repos.add((page,row))
        
        index=regex_all[regex]
        uniInputs=group['input'].unique()
        
        sdfa=sdfas[index]
        ddfas=ddfass[index]
        
        valid_ddfas=[ddfas[input] for input in uniInputs if input in ddfas]
        if len(valid_ddfas)==0:
            print("drop stack index: ",stack_count)
            dropped+=1
#         else:
#             coverages=getCovGivenValidDDFAs(sdfa,valid_ddfas)
#             saveStackCoverages(stack_count,index,page,row,coverages)     
        
#         regexPerStack[stack_count]=[stack_count,page,row,rfile,rclass,rmethod,index]
        regexPerStack[stack_count]=[stack_count,index,len(valid_ddfas)]
        stack_count+=1    
    
    print("total number of stack: ",stack_count)
    print("dropped stack because of dropped strings: ",dropped)
    file_name=output_dir+"stack_regex2.csv"
    with open(file_name,'w') as resultFile:
        wr2 = csv.writer(resultFile, dialect='excel')
        for index,stack in regexPerStack.items():
            wr2.writerow(stack)
    
            
            
def getRepoInfo(df,regex_all,regex_failed,regex_long):
    file_name=output_dir+"repo_regex.csv"
    regexPerRepo=[]
    repos=df.groupby(['page','row'])
    for repo,group in repos:
        page,row=repo
        count=group['count'].sum()
        regex_groups=group.groupby("regex")
        regex_count=0
        failed=0
        for regex,regexgroup in regex_groups:
            regex_count+=1
            index=regex_all[regex]
            if index in regex_failed or index in regex_long:
                failed+=1
                continue
        regexPerRepo.append([page,row,count,regex_count,failed])
    with open(file_name,'w') as resultFile:
        wr2 = csv.writer(resultFile, dialect='excel')
        for perRepo in regexPerRepo:
            wr2.writerow(perRepo)
def saveCoverages(page,row,index,coverages):
    file_name=output_coverage_dir+"repo_cov.csv"
    with open(file_name,'a+') as resultFile:
        wr = csv.writer(resultFile, dialect='excel')        
        for i in range(0,3):
            t=[page,row,index]
            t.extend(coverages[i])
            t.append(i)
            wr.writerow(t)
    return 0

def saveStackCoverages(stack_index,regex_index,page,row,coverages):
    file_name=output_coverage_dir+"stack_cov.csv"
    with open(file_name,'a+') as resultFile:
        wr = csv.writer(resultFile, dialect='excel')
        res=coverages[0] ##res=total,succ,failed
        coverages=coverages[1:]        
        for i in range(0,3):
            t=[stack_index,regex_index,page,row]
            t.extend(coverages[i])
            t.append(i) ##type
            t.append(res[i]) ##total, succ,failed
            wr.writerow(t)
    return 0

def getCovGivenInputs(inputs,sdfa,ddfas):
    valid_ddfas=[ddfas[input] for input in inputs if input in ddfas ]
    
    cov_total=Coverage(sdfa)
    cov_match=Coverage(sdfa)
    cov_mismatch=Coverage(sdfa)
    
    for ddfa in valid_ddfas:
        if ddfa.isMatch:
            cov_match.update(ddfa)
        else:
            cov_mismatch.update(ddfa)
        cov_total.update(ddfa)
    
    coverages=[cov_total.calculate(),cov_match.calculate(),cov_mismatch.calculate()]
    return coverages  
                  
def getCovGivenValidDDFAs(sdfa,valid_ddfas):
    cov_total=Coverage(sdfa)
    cov_match=Coverage(sdfa)
    cov_mismatch=Coverage(sdfa)
    
    total=matched=mismatched=0
    for ddfa in valid_ddfas:
        if ddfa.isMatch:
            cov_match.update(ddfa)
            matched+=1
        else:
            cov_mismatch.update(ddfa)
            mismatched+=1
        cov_total.update(ddfa)
        total+=1
    
    coverages=[[total,matched,mismatched],cov_total.calculate(),cov_match.calculate(),cov_mismatch.calculate()]
    return coverages                
if __name__== '__main__':
    os.chdir(ws)
    df=getDataFrameFromDF("all.df")
    getCovByRegex(df)
