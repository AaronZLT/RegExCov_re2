import csv
import pickle
import pandas as pd
import numpy as np
import re
import os
import glob
ws="/home/peipei/ISSTA2018/data/regex/" ##workspace
output_dir="/home/peipei/ISSTA2018/data/regex/"
drop_dir="/home/peipei/workspace/RepoReaperGithub2/"
def getDataFrame(regexFile):
    regexReader = open(regexFile, 'rb')
    regexes= pickle.load(regexReader)
    
    df=pd.DataFrame(regexes,columns=['page','row','file','class','method','regex','input','count'])
    return df

def dropRecords(df):
    dropClassFileName=drop_dir+"droppedClasses"
    with open(dropClassFileName,'r') as dropClassFile:
        classes = [line.strip() for line in dropClassFile]
        for className in classes:
            df=dropRecordsByClass(className,df)
    return df

def dropRecordsByClass(className,df):
    re_class=re.compile(className)
    df=df[df['class'].apply(lambda x: re_class.match(x) == None)]
    return df

def saveDataFrames(file_path,df):
    filename=file_path+".df"
    #df.to_pickle(filename)
    pickle.dump(df,open(filename,'wb'))
    print("saved to pickle")
    
    filename2=file_path+"_df.csv"
    df.to_csv(filename2,index=False) 
    print("saved to csv")
    print("df length: ",len(df))
                  
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
def getUniqueRegex(df):
    regexes=df.groupby('regex')
    
    regex_dict=dict()
    for regex,group in regexes:
        uniInputs=group['input'].unique()
        regex_dict[regex]=len(uniInputs)
    st_regex=pd.Series(regex_dict)
    st_regex=st_regex.sort_values(ascending=False)
    print("number of unique regexes: ",len(st_regex))
    st_regex.to_csv(output_dir+"regex.csv")    ##ss_regex=pd.read_csv("regex.csv",header=None, squeeze=True, index_col=0)
    return st_regex

def concat(files):
#     files=[1,100,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600]
    pfrom=1
    filenames=[]
    for pto in files:
        filename=str(pfrom)+"_"+str(pto)+".regex"
        filenames.append(filename)
        pfrom=pto
    
    dfs=[]    
    for filename in filenames:
        print("file: ",filename)
        df=getDataFrame(filename)
        df=dropRecords(df)
        getUniqueProj(df)
        getUniqueStackTrace(df)
        getUniqueRegex(df)
        dfs.append(df)
    return pd.concat(dfs)

def mergeAllDataFrames():
    f_pattern="*_*.regex"
    filenames=glob.glob(f_pattern)
        
    dfs=[]    
    for filename in filenames:
        print("file: ",filename)
        df=getDataFrame(filename)
        df=dropRecords(df)
        dfs.append(df)
    return pd.concat(dfs)               
if __name__== '__main__':
    os.chdir(ws)
    df=mergeAllDataFrames()
    file_path=output_dir+"all"
    saveDataFrames(file_path,df)
#     files=[100,200,300,400,500]
#     df=concat(files)
#     saveDataFrames(output_dir+str(rfrom)+"_"+str(rto),df)
    
