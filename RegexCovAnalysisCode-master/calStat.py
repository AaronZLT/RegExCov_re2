'''
Created on Jan 18, 2018

@author: peipei
'''
import os
from analyzeDFA import getStackRegexInfo,getDFAIndex, getRegexInfo, getAllStaticDFAs, getAllDynamicDFAs, getSuccessFailedInfo
from analyzeCov import getDataFrameFromDF, getCovByRepo, getRepoInfo,\
    getCovByStack,getStringInfoByStack,getNumInputsByStack
from DFA import Coverage
import csv
import pickle
from functools import reduce
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
from itertools import chain
ws = "/home/peipei/ISSTA2018/data/regex/"

def reindexDataFrame(filePath1,filePath2):
    df=getDataFrameFromDF(filePath1)
    df=df.reset_index(drop=True)
    df=df.loc[:,['page','row','file', 'class', 'method', 'regex','input']]
    pickle.dump(df,open(filePath2,'wb'))
    
def reshapeDataFrame():
    df = getDataFrameFromDF("all.df")
    df=df.reset_index(drop=True)
    
    regex_dict=dict()
    regexes = df.groupby('regex')
    count=0
    for regex, group in regexes:
        regex_dict[count]=regex
        group['regex'].replace(regex,count)
        count+=1
    regex_map={v:k for k,v in regex_dict.items()}
#     df['regex'].replace(regex_map,inplace=True)  
#     df2=['regex'].replace(regex_map,inplace=True)
    df['regex']=df['regex'].map(regex_map)
    
    repo_dict=dict()
    repos = df.groupby(['page','row'])
    count=0
    for repo, group in repos:
        repo_dict[count]=repo
        group[['page','row']].replace(repo,count)
        count+=1
    repo_map={v:k for k,v in repo_dict.items()}   
    df['repo']=list(zip(df['page','row'])) 
    df['repo']=df['repo'].map(repo_map)
    
    
    frames_dict=dict()
    frames = df.groupby(['file','class','method'])
    count=0
    for frame, group in frames:
        frames_dict[count]=frame
#         group['file','class','method'].replace(frame,count)
        count+=1
    frames_map={v:k for k,v in frames_dict.items()}
    
    output = open("index_regex", 'wb')
    pickle.dump(regex_dict, output, pickle.HIGHEST_PROTOCOL)
    output.close()
    output = open("index_repo", 'wb')
    pickle.dump(repo_dict, output, pickle.HIGHEST_PROTOCOL)
    output.close()     
    output = open("index_frame", 'wb')
    pickle.dump(frames_dict, output, pickle.HIGHEST_PROTOCOL)
    output.close()
    
    output = open("shaped.df", 'wb')
    pickle.dump(df, output, pickle.HIGHEST_PROTOCOL)
    output.close()
        
def getRegexDFA():
    sdfas = getAllStaticDFAs()
    res = []
    for index, sdfa in sdfas.items():
        cov = Coverage(sdfa)
        nodes, edges, epairs = cov.getStat()
        res.append([index, nodes, edges, epairs])
    filename = "/home/peipei/ISSTA2018/data/regex/regex_dfa.csv"
    with open(filename, 'w') as resultFile:
        wr2 = csv.writer(resultFile, dialect='excel')
        for result in res:
            wr2.writerow(result)


def getFailedRegex(df, regex_all, regex_failed, regex_long):   
    res = list()
    regexes = df.groupby('regex')
    for regex, group in regexes:
        index = regex_all[regex]
        if index in regex_failed or index in regex_long:
            res.append(regex)
    
    valid_df = df[~df['regex'].isin(res)]
    print("#regex: ",len(regexes))
    print("#failed: ",len(res))
    print("#valid regex: ",len(valid_df.groupby("regex")))
    print("#valid regex+repo+stack: ",len(valid_df.groupby(['page','row','file','class','method','regex'])))
    output = open("valid.df", 'wb')
    pickle.dump(valid_df, output, pickle.HIGHEST_PROTOCOL)
    output.close()
    
    return valid_df, len(res)


def dropByStackCount(df):
    df.reset_index(drop=True)
#     df=df.iloc[:100000,:]
    stacks = df.groupby(['file', 'class', 'method', 'regex'])
    print("len df: ", len(df))
    print("len stack: ", len(stacks))
    ss = stacks['count'].sum()
    q1, q2, q3 = ss.quantile([.25, .5, .75])
    iqr = q3 - q1
    threshold = q3 + 1.5 * iqr
    routliers = ss[ss > threshold]
    print("num of outliers: ", len(routliers))
    
    res = [stacks.get_group(group_name).index for group_name in routliers.index]
    from itertools import chain
    res2 = list(chain(*res))
    
#     res2 = reduce(lambda x, y: x.union(y), res)  # #Int64Index Union
    print(len(res2))
    df2 = df.loc[res2]
    output = open("outliers.df", 'wb')
    pickle.dump(df2, output, pickle.HIGHEST_PROTOCOL)
    output.close()
    print("len dropped df: ", len(df2))
    print("len regex unique: ", len(df2['regex'].unique()))
    print("len2 regex unique: ", len(df2.groupby('regex')))
    print("len dropped stack: ", len(df2.groupby(['page', 'row', 'file', 'class', 'method', 'regex'])))
    
    res3 = [i for i in df.index if i not in res2]
    
#     res3 = pd.Int64Index(np.arange(len(df))).difference(res2)
    df3 = df.loc[res3]
    output = open("clean.df", 'wb')
    pickle.dump(df3, output, pickle.HIGHEST_PROTOCOL)
    output.close()
    print("len clean df: ", len(df3))
    print("len regex unique: ", len(df3['regex'].unique()))
    print("len2 regex unique: ", len(df3.groupby('regex')))
    print("len clean stack: ", len(df3.groupby(['page', 'row', 'file', 'class', 'method', 'regex'])))
    return df3, df2

def outliersByIQR(stacks):
    s=[]
    for stack,group in stacks:
        n_repo=len(group.groupby(['page','row']))
        s.append(n_repo)
    s.sort()
    
    ss=pd.Series(s)
    sdf=ss.to_frame()
    sdf.reset_index(inplace=True)
    sdf.columns=['id','repos']
    sdf.plot(kind='scatter',x='id',y='repos')
    plt.show()
    plt.savefig("scatter.pdf")
    
    ss.hist(bins=1)
    plt.savefig("hist.pdf")
    
    print("percentiles: ",ss.quantile([0.1,0.25,0.5,0.75,0.9,0.95,0.99]))
    q1, q2, q3 = ss.quantile([.25, .5, .75])
    iqr = q3 - q1
    threshold = q3 + 1.5 * iqr
    print("q1:",q1,"q3:",q3,"IQR:",iqr,"threshold:",threshold)
    routliers = ss[ss > threshold]
    print("num of outliers: ", len(routliers))
    
def dropByStackRepoCount(df):
    stacks = df.groupby(['file', 'class', 'method', 'regex'])
    print("len df: ", len(df))
    print("len stack+regex: ", len(stacks))
    print("len rep+stack+regex: ",len(df.groupby(['page','row','file', 'class', 'method', 'regex'])))
    
    s=dict()
    for stack,group in stacks:
        n_repo=len(group.groupby(['page','row']))
        s[stack]=n_repo

    res = [stacks.get_group(group_name).index for group_name in s if s[group_name]>1]
    res2 = list(chain(*res))
#     res2 = reduce(lambda x, y: x.union(y), res)  # #Int64Index Union
    print(len(res2))
    df2 = df.loc[res2]
    output = open("outliers.df", 'wb')
    pickle.dump(df2, output, pickle.HIGHEST_PROTOCOL)
    output.close()
    print("len dropped df: ", len(df2))
    print("len regex unique: ", len(df2['regex'].unique()))
    print("len2 regex unique: ", len(df2.groupby('regex')))
    print("len dropped stack+regex: ", len(df2.groupby(['file', 'class', 'method', 'regex'])))
    print("len clean repo+stack+regex: ", len(df2.groupby(['page','row','file', 'class', 'method', 'regex'])))
    res = [stacks.get_group(group_name).index for group_name in s if s[group_name]==1]
    res3 = list(chain(*res))
#     res3 = [i for i in df.index if i not in res2]
    print(len(res3))
#     res3 = pd.Int64Index(np.arange(len(df))).difference(res2)
    df3 = df.loc[res3]
    output = open("clean.df", 'wb')
    pickle.dump(df3, output, pickle.HIGHEST_PROTOCOL)
    output.close()
    print("len clean df: ", len(df3))
    print("len regex unique: ", len(df3['regex'].unique()))
    print("len2 regex unique: ", len(df3.groupby('regex')))
    print("len2 repo unique: ", len(df3.groupby(['page','row'])))
    print("len clean stack+regex: ", len(df3.groupby(['file', 'class', 'method', 'regex'])))
    print("len clean repo+stack+regex: ", len(df3.groupby(['page','row','file', 'class', 'method', 'regex'])))
    return df3, df2


# def getRegexRepo  
# ## drop based on IQR rule
# ##For a given continuous variable, 
# ##outliers are those observations that lie outside 1.5 * IQR, 
# # where IQR, the ‘Inter Quartile Range’ is the difference between 75th and 25th quartiles


def testIRQ():
    df = pd.DataFrame(columns=['index', 'regex', 'input', 'count'])
    df['index'] = [1, 1, 2, 3, 1, 2, 4, 5, 2, 4]
    df['regex'] = ['A', 'A', 'A', 'A', 'C', 'B', 'C', 'A', 'D', 'D']
    df['input'] = ['a', 'b', 'a', 'a', 'c', 'b', 'b', 'b', 'd', 'd']
    df['count'] = [random.randint(50, 100) if n < 3 else random.randint(1, 40) for n in range(10)]
    # #[73,73,82,6,16,18,9,34,12,40]
    print(df)  
    
    groups = df.groupby(['index', 'regex'])
    ss = groups['count'].sum()
    print(ss)
    
    q1, q2, q3 = ss.quantile([.25, .5, .75])
    iqr = q3 - q1
    threshold = q3 + 1.5 * iqr
    print(threshold)
    routliers = ss[ss > threshold]
    print("num of outliers: ", len(routliers))
    print(routliers) 
    print("outlier index: ", routliers.index)
    
    res = [groups.get_group(group_name).index for group_name in routliers.index]
    res2 = reduce(lambda x, y: x.union(y), res)  # #Int64Index Union
    print(len(res2))
    df2 = df.loc[res2]
    print(df2)


if __name__ == '__main__':
    os.chdir(ws)
#     reindexDataFrame("all.df", "reindex.df")
#     df = getDataFrameFromDF("reindex.df")
#     clean_df, dropped_df = dropByStackRepoCount(df)
#     exit(0)
#     getRegexDFA()
#     clean_df = getDataFrameFromDF("clean.df")
#     regex_all, regex_failed, regex_long = getDFAIndex()
#     valid_df, dropped_failedRE2 = getFailedRegex(clean_df, regex_all, regex_failed, regex_long)

#     ddfass=getAllDynamicDFAs()
#     getSuccessFailedInfo(ddfass)

#     valid_df = getDataFrameFromDF("valid.df")
#     regex_all, regex_failed, regex_long = getDFAIndex()
#     getStackRegexInfo(valid_df,regex_all)
    valid_df = getDataFrameFromDF("valid.df")
    ddfass=getAllDynamicDFAs()
    sdfas=getAllStaticDFAs()
    regex_all, regex_failed, regex_long = getDFAIndex()
#     getStringInfoByStack(valid_df,sdfas,ddfass,regex_all)
    getNumInputsByStack(valid_df,sdfas,ddfass,regex_all)
#     getCovByStack(valid_df,sdfas,ddfass,regex_all)
#     getRepoInfo(df,regex_all,regex_failed,regex_long)
#     sdfas=getAllStaticDFAs()
#     ddfass=getAllDynamicDFAs()
#     getCovByRepo(df,sdfas,ddfass,regex_all,regex_failed,regex_long)
