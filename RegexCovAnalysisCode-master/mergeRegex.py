import os
import sys
import glob
import csv
import pickle

ws="/home/peipei/ISSTA2018/data/regex/1.7/" ##workspace
output_dir="/home/peipei/ISSTA2018/data/regex/"

def mergePage(files):
    regList=list()
    for regexFile in files:
        ##extract page and row
        nums=regexFile.split("_")
        page,row=int(nums[0]),int(nums[1])    
        regexReader = open(regexFile, 'rb')
        regexes= pickle.load(regexReader)
        for key,value in regexes.items():
            temp=[page,row]
            
            keys=list(key)
            temp.extend(keys)
            
            count=len(value)            
            temp.append(count)
            
            regList.append(temp)
    regList.sort(key=lambda k:(k[0],k[1]))
    return regList

def merge(pfrom=1,pend=4496):
    os.chdir(ws)
    regList=list()
    i=pfrom
    while i<pend:
        files=glob.glob(str(i)+"_*.regex")
        if len(files)>0:
            regList.extend(mergePage(files))
        i+=1
    
    filename=output_dir+str(pfrom)+"_"+str(pend)
    save(filename,regList)
    
def save(filename,regList):
    print("len lists of regex: ",len(regList))
    if len(regList)>0:
        print("picking regex list: ")
        output=open(filename+".regex",'wb')
        pickle.dump(regList, output)
        output.close() 
        print("dumped regex") 
        
        print("saving csv regex: ")
        with open(filename+"_regex.csv",'w') as resultFile:
            wr = csv.writer(resultFile, dialect='excel')
            wr.writerow(["page","row","file","class","method","regex","input","count"])
            wr.writerows(regList)
            
if __name__== '__main__':
    if sys.argv is None or len(sys.argv)<2: #(begin,end]
        sys.exit('Error! You need to specify one project ID or begin and end project ID!!')
        
    begin=int(sys.argv[1])
    end=begin
    if len(sys.argv)==3:
        end=int(sys.argv[2])
    elif len(sys.argv)==2:
        end=end+1
        
    merge(begin,end) 
