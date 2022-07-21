import csv
import pickle
import pandas as pd
import numpy as np
import re
import os
import glob
from DFA import Coverage, StaticDFA, DynamicDFA
ws="/home/peipei/ISSTA2018/data/dfa/static/" ##workspace
d_ws="/home/peipei/ISSTA2018/data/dfa/dynamic/"
output_dir="/home/peipei/ISSTA2018/data/dfa/"
regex_dir="/home/peipei/ISSTA2018/data/regex/"
def getAllStaticDFAs():
    file_pattern="/home/peipei/ISSTA2018/data/dfa/static/*.regex"
    files=glob.glob(file_pattern)
    sdfa_dict=dict()
    for file_dfa in files:
        print("static:",file_dfa[39:-6])
        index=int(file_dfa[39:-6])
        
        dfaReader= open(file_dfa, 'rb')
        sdfa= pickle.load(dfaReader)
        sdfa_dict[index]=sdfa
    
    return sdfa_dict

def getAllDFASizes():
    file_pattern="/home/peipei/ISSTA2018/data/dfa/static/*.regex"
    files=glob.glob(file_pattern)
    sdfa_size=dict()
    for file_dfa in files:
        index=int(file_dfa[40:-6])
        dfaReader = open(file_dfa, 'rb')
        sdfa= pickle.load(dfaReader)
        sdfa_size[index]=sdfa.size    
    return sdfa_size

def getAllDynamicDFAs():
    file_pattern="/home/peipei/ISSTA2018/data/dfa/dynamic/*.regex"
    files=glob.glob(file_pattern)
    ddfa_dict=dict()
    for file_ddfa in files:
        print("dynamic:",file_ddfa[40:-6])
        index=int(file_ddfa[40:-6])
        ddfaReader = open(file_ddfa, 'rb')
        ddfa= pickle.load(ddfaReader)
        ddfa_dict[index]=ddfa
    return ddfa_dict

def getDynamicDFAs(index):
    file_ddfa=d_ws+str(index)+".regex"
    ddfaReader = open(file_ddfa, 'rb')
    ddfas= pickle.load(ddfaReader)
    return ddfas

def getUniInputsSize(index):
    file_ddfa=d_ws+str(index)+".regex"
    ddfaReader = open(file_ddfa, 'rb')
    ddfas= pickle.load(ddfaReader)
    return len(ddfas)

def getSizeInputs(index):
    size=getStaticDFA(index).size
    len_totalInputs=getUniInputsSize(index)   
    return size,len_totalInputs

def getRegexInfo(df,regex_all,regex_failed,regex_long):
    regexes=df.groupby('regex')
    info_list=list()
    for regex,group in regexes:
        index=regex_all[regex]
        n_repos=len(group.groupby(['page','row']))
        len_inputs=group['count'].sum()##every input may be practiced several times for the same project
        len_unInputs=len(group['input'].unique())
        isFailed= index in regex_failed or index in regex_long
        if isFailed:
            size=-1
            len_validInputs=-1
        else:
            size,len_validInputs=getSizeInputs(index)
        info_list.append([index,size,len_inputs,len_unInputs,len_validInputs,isFailed,n_repos])
    
    filename=regex_dir+"regex_info.csv"
    with open(filename,'w') as resultFile:
        wr = csv.writer(resultFile, dialect='excel')
        for info in info_list:
            wr.writerow(info)

def getStackRegexInfo(valid_df,regex_all):
    stacks=valid_df.groupby(['page','row','file','class','method','regex'])
    count=0
    info_list=list()
    for stack,group in stacks:
        page,row,rfile,rclass,rmethod,regex=stack
        
        index=regex_all[regex]
        
        #len_inputs=group['count'].sum()##every input may be practiced several times for the same project
        uniInputs=group['input'].unique()
        len_uniInputs=len(uniInputs)
        succ=failed=dropped=0
        
        sdfa=getStaticDFA(index)
        
        dfa_size=sdfa.size
        nodes,edges,epairs=Coverage(sdfa).getStat()
        
        ddfas=getDynamicDFAs(index)
        len_totalInputs=len(ddfas)
        for input in uniInputs:
            try:
                ddfa=ddfas[input]
            
                if ddfa.isMatch:
                    succ+=1
                else:
                    failed+=1
            except KeyError as e:
                print(e)
                dropped+=1
                    
        info_list.append([count,index,page,row,nodes,edges,epairs,len_totalInputs,len_uniInputs,succ,failed,dropped])
        count+=1
    print("num of stack regex: ",count)
    filename=regex_dir+"stack_info.csv"
    with open(filename,'w') as resultFile:
        wr = csv.writer(resultFile, dialect='excel')
        for info in info_list:
            wr.writerow(info)
def getSuccessFailedInfo(ddfass):
    regex_result=[]
    for index, ddfas in ddfass.items():
        size=len(ddfas)
        succ,failed=(0,0)
        for input,ddfa in ddfas.items():
            if ddfa.isMatch:
                succ+=1
            else:
                failed+=1
        regex_result.append([index,size,succ,failed])
    filename=regex_dir+"regex_result.csv"    
    with open(filename,'w') as resultFile:
        wr2 = csv.writer(resultFile, dialect='excel')
        for result in regex_result:
            wr2.writerow(result)
                     
def getStaticDFA(index):
    file_dfa=ws+str(index)+".regex"
    dfaReader = open(file_dfa, 'rb')
    dfa= pickle.load(dfaReader)
    return dfa

def getDFASize(sdfa_dict):
    sdfa_size=dict()
    for index, sdfa in sdfa_dict.items():
        sdfa_size[index]=sdfa.size
    return sdfa_size

def getDFAIndex():
    all=open(regex_dir+"unique.regex",'rb')
    regex_all=pickle.load(all)
    
    failed=open(regex_dir+"failed.regex",'rb')
    regex_failed=pickle.load(failed)

#     strlong=open(regex_dir+"strlen.regex",'rb')
#     regex_long=pickle.load(strlong)
    regex_long=dict()
    for regex,index in regex_all.items():
        if index not in regex_failed:
            f_path=ws+str(index)+".regex"
            if not os.path.exists(f_path):
                regex_long[index]=regex
            
    
    return regex_all,regex_failed,regex_long                    
if __name__== '__main__':
    os.chdir(ws)
    getAllStaticDFAs()
