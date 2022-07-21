import csv
import pickle
import re
import os
import sys
import traceback
import subprocess
import time
import glob
from DFA import Coverage
from analyzeDFA import getDFAIndex
from DFAUtils import getStaticDFA,getDynamicDFAs,getCoverages,getDynamicDFAs2
from extractRegexTrace import stack_regex
from inspect import stack
import numpy as np
# ws="G:\\regex" ##workspace
ws="/home/peipei/ISSTA2018/data/regex/"
dfa_dir="/home/peipei/ISSTA2018/data/dfa/"
output_cov_dir="/home/peipei/ISSTA2018/data/cov/"
rex_path="E:\\Rex"
 
mode_modifiers=["(?i)","(?m)","(?s)"] 
def getRegexes():
    file_all=open("unique.regex",'rb')
    regex_all=pickle.load(file_all)    
    failed=open("failed.regex",'rb')
    regex_failed=pickle.load(failed)
    return regex_all, regex_failed

def getRexFailedTimed():
    rex_failed=pickle.load(open("failed_rex.regex",'rb'))
    rex_timed=pickle.load(open("timed_rex.regex",'rb'))
    return rex_failed,rex_timed

def getRegexInfo():
    #c("index","dfa","total","unique","valid","failed","repo")
    regexInfo=dict()
    with open('regex_info.csv', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            index,dfa,total,unique,valid,failed,repo=row
            regexInfo[int(index)]=int(unique)
        return regexInfo
def generateStrings(regex_all,regex_failed, seed=None):
    str_seed=None
    if seed is not None:
        str_seed="/seed:"+str(seed)
        
    failed=dict()
    timed=dict()
    for regex,index in regex_all.items():
        if index in regex_failed:
            continue
        regextemp=regex
        regexprefix=''
        while regextemp[0:4] in mode_modifiers:
            regexprefix=regexprefix+regextemp[0:4]
            regextemp=regextemp[4:]
            
        if len(regex)>0 and regex[0]!='^':
            regextemp='^'+regextemp
        if len(regex)>0 and regex[-1]!='$':
            regextemp=regextemp+'$'
        regextemp=regexprefix+regextemp
        regextemp1=regextemp.encode('utf-8')  ##print not utf8 cause unicode error
        regextemp=regextemp1.decode("utf-8")
        print("generating for strings of regex: ",regextemp1,"index: ",index)
        for type_encode in ['ASCII','Unicode']:                
            fileInputs="inputs/"+str(index)+"_"+type_encode        
            try:
#                 status,res=execute([rex_path,"/k:34","/file:"+fileInputs,"/encoding:"+type_encode,regextemp])
                if seed is None:
                    cmd=[rex_path,"/k:34","/file:"+fileInputs,"/encoding:"+type_encode,regextemp]
                else:
                    cmd=[rex_path,"/k:34","/file:"+fileInputs,"/encoding:"+type_encode,str_seed,regextemp]
#                 print(cmd)                        
                p=subprocess.Popen(cmd)
                stdoutdata, stderrdata=p.communicate(timeout=3600)
                if p.returncode>0: ###error not valid regex
                    print("could not generate for pattern: ",regextemp1," index: ",index)
                    failed[index]=type_encode
                    continue        
            except subprocess.TimeoutExpired:
                print("time out of generating strings for pattern: ",regextemp1," index: ",index)
                p.kill()
                timed[index]=type_encode
                pass
                continue
            except UnicodeEncodeError:
                print("unicode encode error of generating strings for pattern: ",regextemp1," index: ",index)
                print("Regex String Unicode error:", sys.exc_info()[0])
                traceback.print_exc()
                pass
                continue
            except:
                print("Error in generate for pattern: ",regextemp1," index: ",index)
                traceback.print_exc()
    output=open("failed_rex.regex",'wb')
    pickle.dump(failed, output, pickle.HIGHEST_PROTOCOL)
    output.close()
    output=open("timed_rex.regex",'wb')
    pickle.dump(timed, output, pickle.HIGHEST_PROTOCOL)
    output.close()
    
def getASCIIInputs(index):
    fileInputs=open("inputs/"+str(index)+"_"+"ASCII",'r')
    inputs=[]
    for line in fileInputs:
        inputs.append(line[1:-2])
    return inputs

def getUnicodeInputs(index):
    fileInputs=open("inputs/"+str(index)+"_"+"Unicode",'r')
    inputs=[]
    for line in fileInputs:
        inputs.append(line[1:-2])
    return inputs

def getInputs(input_dir,stack_index,encoding):    
    file_string=input_dir+str(stack_index)+"_"+encoding
    fileInputs=open(file_string,'r')
    inputs=[]
    for line in fileInputs:
        input=line[1:-2]
        try:
            input=input.encode("utf-8",'surrogateescape').decode("unicode_escape")
            input.encode('utf8')
        except UnicodeDecodeError:
            pass
        except UnicodeEncodeError:
            continue
        inputs.append(input)   
    return inputs

def saveCov(coverage_dict,file_cov):
    with open(file_cov,'w') as resultFile:
        wr = csv.writer(resultFile, dialect='excel')
        wr.writerow(["index","c_node","t_node","c_edge","t_edge","c_epair","t_epair","type"])               
        for index,cov in coverage_dict.items():
            for i in range(0,3):
                t=[index]
                t.extend(cov[i])
                t.append(i)
                wr.writerow(t)

def calRexCovAscii(regex_all,regex_failed,rex_failed,rex_timed,regexInfo):
    coverage_dict=dict()
    coverageTruncated_dict=dict()
    count_inputs=dict()
    for regex,index in regex_all.items():
        if index not in regex_failed and index not in rex_failed and index not in rex_timed:
            inputs=getASCIIInputs(index)
            count=regexInfo[index]
            count_inputs[index]=len(inputs)
             
            ddfas=getDynamicDFAs(index,inputs)
            sdfa=getStaticDFA(index)
            #coverage_dict[index]=getSuccessCoverage(sdfa,ddfas)
            coverage_dict[index]=getCoverages(sdfa,ddfas) 
            if len(inputs)>count:          
                inputs2=inputs[:count]
                ddfa2=dict()
                for input in inputs2:
                    ddfa2[input]=ddfas[input]
                coverageTruncated_dict[index]=getCoverages(sdfa,ddfa2)
            else:
                coverageTruncated_dict[index]=coverage_dict[index]
             
    saveCov(coverage_dict,output_cov_dir+"ascii_all.csv")
    saveCov(coverageTruncated_dict,output_cov_dir+"ascii_same.csv")
    return count_inputs       
def calRexCovUnicode(regex_all,regex_failed,rex_failed,rex_timed,regexInfo):
    coverage_dict=dict()
    coverageTruncated_dict=dict()
    count_inputs=dict()
    for index in regex_all.values():
        if index not in regex_failed and index not in rex_failed and index not in rex_timed:
            inputs=getASCIIInputs(index)
            count=regexInfo[index]
            count_inputs[index]=len(inputs)
             
            ddfas=getDynamicDFAs(index,inputs)
            sdfa=getStaticDFA(index)
#             coverage_dict[index]=getSuccessCoverage(sdfa,ddfas)
            coverage_dict[index]=getCoverages(sdfa,ddfas)
            saveCov(coverage_dict,output_cov_dir+"unicode_all.csv")
 
            if len(inputs)>count:
                inputs2=inputs[:count]
                ddfa2=dict()
                for input in inputs2:
                    ddfa2[input]=ddfas[input]
                coverageTruncated_dict[index]=getCoverages(sdfa,ddfa2)
            else:
                coverageTruncated_dict[index]=coverage_dict[index]
    saveCov(coverage_dict,output_cov_dir+"unicode_all.csv")
    saveCov(coverageTruncated_dict,output_cov_dir+"unicode_same.csv")
    return count_inputs

def exportCount2CSV(file1,file2):
    data=pickle.load(open(file1,'rb'))
    with open(file2,'w') as resultFile:
        wr = csv.writer(resultFile, dialect='excel')
        for index,count in data.items():
            wr.writerow([index,count])

def addAnchors(regexStr,flags_re):
    flags=None
    ##remove start ^
    if len(regexStr)>0 and regexStr[0]=='^':
        regexStr=regexStr[1:]
    ###start with flags:
    if len(regexStr)>4 and regexStr[0]=="(":
        res=flags_re.match(regexStr)
        if res:
            flags,regexStr=res.group(1),res.group(3)
    ###add ^
    if len(regexStr)>0 and regexStr[0]!='^':
        regexStr='^'+regexStr
    ## add $
    if len(regexStr)>0 and regexStr[-1]!='$':
        regexStr=regexStr+'$'
    ###add falgs
    if flags is not None:
        regexStr=flags+regexStr
    regexStr=regexStr.encode('utf-8')  ##print not utf8 cause unicode error
    regexStr=regexStr.decode("utf-8")    
    return regexStr
def genStringsPerStack(stack_index,regexStr,regex_index,validCount,input_dir,isSeed=True):
    print("generating for strings of stack regex index: ",stack_index,regex_index)
    res=[0,0]
    for type_encode in ['ASCII','Unicode']:                
        fileInputs=input_dir+str(stack_index)+"_"+type_encode        
        try:
            cmd=[rex_path]
            cmd.append("/k:"+str(validCount))
            cmd.append("/file:"+fileInputs)
            cmd.append("/encoding:"+type_encode)
            if isSeed:
                seed=int(time.time())
                cmd.append("/seed:"+str(seed))
            cmd.append(regexStr)
#             print(cmd)                        
            p=subprocess.Popen(cmd)
            stdoutdata, stderrdata=p.communicate(timeout=3600)
            if p.returncode>0: ###error not valid regex
                try:
                    print("encoding:",type_encode,"could not generate for pattern:",regexStr,"stack regex index: ",stack_index,regex_index)
                except UnicodeEncodeError:
                    print("encoding:",type_encode,"unicode encode error of generating strings for pattern stack regex index: ",stack_index,regex_index)
                    print("error printing Regex String Unicode error:", sys.exc_info()[0])    
                if stdoutdata is not None:
                    print(stdoutdata)
                if stderrdata is not None:
                    print(stderrdata)
                i=0
                if type_encode=="Unicode":
                    i=1
                res[i]=p.returncode
                continue        
        except subprocess.TimeoutExpired:
            try:
                print("encoding:",type_encode,"could not generate for pattern:",regexStr,"stack regex index: ",stack_index,regex_index)
            except UnicodeEncodeError:
                print("encoding:",type_encode,"unicode encode error of generating strings for pattern stack regex index: ",stack_index,regex_index)
                print("error printing Regex String Unicode error:", sys.exc_info()[0])    
            p.kill()
            i=0
            if type_encode=="Unicode":
                i=1
            res[i]=-100
            continue
        except UnicodeEncodeError:
            print("encoding:",type_encode,"unicode encode error of generating strings for pattern stack regex index: ",stack_index,regex_index)
            print("Regex String Unicode error:", sys.exc_info()[0])
            traceback.print_exc()
            p.kill()
            i=0
            if type_encode=="Unicode":
                i=1
            res[i]=-101
            pass
        except:
            print("encoding:",type_encode,"Error in generate for pattern stack regex index: ",stack_index,regex_index)
            traceback.print_exc()
            p.kill()
            i=0
            if type_encode=="Unicode":
                i=1
            res[i]=-102
            continue
    return res
def exp(scale=1,rep=10):
    print("scale: ",scale," rep:",rep)
    stack_dict=dict()
    with open('stack_regex2.csv', mode='r') as infile:
        reader = csv.reader(infile)
        for row in reader:
            stack_index,regex_index,validCount=row
            stack_dict[int(stack_index)]=[int(regex_index),int(validCount)]
    print("getting stack_regex2")
    regexfile_all=open("unique.regex",'rb')
    regex_all=pickle.load(regexfile_all)
    regex_dict=dict()
    flags_re=re.compile("(\(\?(?!.{0,2}(.).{0,2}\\2)[imsU]{1,4}\))(.*)",re.DOTALL)
    for regex,regex_index in regex_all.items():
        regexStr=regex
        regexStr=addAnchors(regexStr, flags_re)
        regex_dict[regex_index]=regexStr
        
    print("getting regex_dict")
    repetition=rep
    for count in range(repetition):
        input_dir="input_"+str(scale)+"_"+str(count)+"/"
        if not os.path.exists(input_dir):
            os.makedirs(input_dir)
        print("input_dir: ",input_dir)
        res_dict=dict()    
        for stack_index in stack_dict:
#             print(stack_index)
#             if stack_index<14009:
#                 continue
            regex_index,validCount=stack_dict[stack_index]
            if validCount==0:
                print("skip stack because of no valid input: ",regex_index)
                continue
            regexStr=regex_dict[regex_index]
            res=genStringsPerStack(stack_index,regexStr, regex_index, validCount*scale, input_dir, True)
            print("stack_index: ",stack_index,"regex_index",regex_index,"res: ",res)
            res_dict[stack_index]=res
        
        with open("genRes_"+str(count),'w') as resultFile:
            wr = csv.writer(resultFile, dialect='excel')
            wr.writerow(["stack_index","ASCII","Unicode"])               
            for stack_regex,res in res_dict.items():
                wr.writerow([stack_regex,res[0],res[1]])


def getSDFAInfo(sdfa_file_path, stack_index):
    sdfa=pickle.load(open(sdfa_file_path,'rb'))
    cov=Coverage(sdfa)
    return (stack_index, len(cov.nodes), len(cov.edges), len(cov.edgePairs))
def getStackIndex(static_dir, file_pattern="*.regex"):
    n=len(file_pattern)-1    
    files=glob.glob1(static_dir,file_pattern)
    if len(files)>0:
#         stacks=[int(file_name[:-n]) for file_name in files]
        stacks=[getSDFAInfo(static_dir+file_name,int(file_name[:-n])) for file_name in files]
        return stacks
    else:
        return []

def getInputDirs(scale,repetition):
    if scale==1:
        input_dirs=["input_"+str(count)+"/" for count in range(repetition)]
    else:
        input_dirs=["input_"+str(scale)+"_"+str(count)+"/" for count in range(repetition)]
    return input_dirs

def getOutputDirs(scale,repetition):  
    if scale==1:
        output_dirs=[dfa_dir+"input_"+str(count)+"/" for count in range(repetition)]
    else:
        output_dirs=[dfa_dir+"input_"+str(scale)+"_"+str(count)+"/" for count in range(repetition)]
    return output_dirs
  
def calRex(scale=1,rep=10):
    repetition=rep
    input_dirs=getInputDirs(scale, repetition)
        
    stack_dict=dict()
    with open('stack_regex2.csv', mode='r') as infile:
        reader = csv.reader(infile)
        for row in reader:
            stack_index,regex_index,validCount=row
            stack_dict[int(stack_index)]=[int(regex_index),int(validCount)]
    
    regexfile_all=open("unique.regex",'rb')
    regex_all=pickle.load(regexfile_all)
    regex_dict=dict()
    for regexStr,regex_index in regex_all.items():
        regex_dict[regex_index]=regexStr
        
        
    for i in range(repetition):
        input_dir=input_dirs[i]
        output_dir=dfa_dir+input_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        for encoding in ['ASCII','Unicode']:  
            encoding_dir=output_dir+encoding+"/"
            if not os.path.exists(encoding_dir):
                os.makedirs(encoding_dir)
            static_dir=encoding_dir+"static/"
            if not os.path.exists(static_dir):
                os.makedirs(static_dir)
            dynamic_dir=encoding_dir+"dynamic/"
            if not os.path.exists(dynamic_dir):
                os.makedirs(dynamic_dir)
                            
            for stack_index in [14]:
#             for stack_index in stack_dict:    
                file_string=input_dir+str(stack_index)+"_"+encoding
                if not os.path.exists(file_string):
                    print("skip stack because of no input string file: ",file_string, stack_index)
                    continue
                inputs=getInputs(input_dir,stack_index,encoding)
                if len(inputs)==0:
                    print("skip stack because regex failed in Rex and no generated string: ",file_string, stack_index)
                    continue
                
                regex_index,validCount=stack_dict[stack_index]
                if validCount==0:
                    print("skip stack because of no valid input: ",stack_index)
                    continue
                print("rep: ",i," encoding: ",encoding," stack_index: ", stack_index)
                regexStr=regex_dict[regex_index]
                sdfa=getStaticDFA(regexStr,stack_index,static_dir)
                if sdfa is None: ##compilation error
                    print("skip stack because regex failed in RE2: ",stack_index,regex_index)
                    continue
                ddfas=getDynamicDFAs(stack_index,inputs,dynamic_dir,static_dir)


def calRex2(scale=1,rep=10):
    repetition=rep
    input_dirs=getInputDirs(scale, repetition)
        
    rex_succASCII=pickle.load(open("ASCIISucc.regex",'rb'))
    rex_succUnicode=pickle.load(open("UnicodeSucc.regex",'rb'))
    rex_succ=dict()
    rex_succ["ASCII"]=rex_succASCII
    rex_succ["Unicode"]=rex_succUnicode
    
    succRex=dict()
    succRex["ASCII"]=dict()
    succRex["Unicode"]=dict()
    
    for i in range(repetition):
        input_dir=input_dirs[i]
        output_dir=dfa_dir+input_dir
        for encoding in ['ASCII','Unicode']:
            encoding_dir=output_dir+encoding+"/"
            static_dir=encoding_dir+"static/"
            dynamic_dir=encoding_dir+"dynamic/"                           
            for stack_index in rex_succ[encoding]:
#                 if stack_index!=60:
#                     continue
                print("rep: ",i, "encoding:", encoding, "stack_index: ",stack_index)
                if stack_index not in succRex[encoding]:
                    succRex[encoding][stack_index]=[rex_succ[encoding][stack_index][0]] ##add default succ
                    
                file_string=input_dir+str(stack_index)+"_"+encoding
                if not os.path.exists(file_string):
                    print("skip stack because of no input string file: ",file_string, stack_index)
                    continue
                inputs=getInputs(input_dir,stack_index,encoding)
                if len(inputs)==0:
                    print("skip stack because regex failed in Rex and no generated string: ",file_string, stack_index)
                    continue
                                
                ddfas=getDynamicDFAs(stack_index,inputs,dynamic_dir,static_dir)
                succ_ddfa=0
                for input, ddfa in ddfas.items():
                    if ddfa.isMatch:
                        succ_ddfa+=1
                succRex[encoding][stack_index].append(succ_ddfa)
    
    for encoding in ['ASCII','Unicode']:
        output=open(encoding+"Succ3.regex",'wb')
        pickle.dump(succRex[encoding], output, pickle.HIGHEST_PROTOCOL)
        output.close()
        
        file_name=encoding+"_succ3.csv"
        with open(file_name,'w') as resultFile:
            wr2 = csv.writer(resultFile, dialect='excel')
            for stack_index,info in succRex[encoding].items():
                wr2.writerow([stack_index]+info)


def calRex3(scale=1,rep=10,encoding="ASCII", reps=0):
    repetition=rep
    input_dirs=getInputDirs(scale, repetition)
    
    stack_dict=dict()
    with open('stack_regex2.csv', mode='r') as infile:
        reader = csv.reader(infile)
        for row in reader:
            stack_index,regex_index,validCount=row
            stack_dict[int(stack_index)]=[int(regex_index),int(validCount)]
    
    regexfile_all=open("unique.regex",'rb')
    regex_all=pickle.load(regexfile_all)
    regex_dict=dict()
    for regexStr,regex_index in regex_all.items():
        regex_dict[regex_index]=regexStr
            
    if encoding=="ASCII":
        rex_succASCII=pickle.load(open("ASCIISucc.regex",'rb'))
        rex_succ=rex_succASCII
    else:
        rex_succUnicode=pickle.load(open("UnicodeSucc.regex",'rb'))
        rex_succ=rex_succUnicode
    succRex=dict()
    
    for i in range(reps,reps+1):
        input_dir=input_dirs[i]
        output_dir=dfa_dir+input_dir    
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)    
        encoding_dir=output_dir+encoding+"/"
        if not os.path.exists(encoding_dir):
                os.makedirs(encoding_dir)
        static_dir=encoding_dir+"static/"
        if not os.path.exists(static_dir):
            os.makedirs(static_dir)
        dynamic_dir=encoding_dir+"dynamic/"
        if not os.path.exists(dynamic_dir):
            os.makedirs(dynamic_dir)
                          
        for stack_index in rex_succ:
            regex_index,validCount=stack_dict[stack_index]
            if validCount==0:
                print("skip stack because of no valid input: ",stack_index)
                continue
            print("rep: ",i," encoding: ",encoding," stack_index: ", stack_index)

            regexStr=regex_dict[regex_index]
            sdfa=getStaticDFA(regexStr,stack_index,static_dir)
            if sdfa is None: ##compilation error
                print("skip stack because regex failed in RE2: ",stack_index,regex_index)
                continue
                    
#             print("rep: ",i, "encoding:", encoding, "stack_index: ",stack_index)
            succ=rex_succ[stack_index][0]
            if stack_index not in succRex:
                succRex[stack_index]=[succ] ##add default succ
                
            file_string=input_dir+str(stack_index)+"_"+encoding
            if not os.path.exists(file_string):
                print("skip stack because of no input string file: ",file_string, stack_index)
                continue
            inputs=getInputs(input_dir,stack_index,encoding)
            if len(inputs)==0:
                print("skip stack because regex failed in Rex and no generated string: ",file_string, stack_index)
                continue
                            
            ddfas=getDynamicDFAs2(stack_index,inputs,succ*scale,dynamic_dir,static_dir)
            succ_ddfa=0
            for input, ddfa in ddfas.items():
                if ddfa.isMatch:
                    succ_ddfa+=1
            succRex[stack_index].append(succ_ddfa)
    
    file_output=str(scale)+"_"+encoding+"_"+str(reps)
    output=open(file_output+"Succ3.regex",'wb')
    pickle.dump(succRex, output, pickle.HIGHEST_PROTOCOL)
    output.close()
    
    with open(file_output+"_succ3.csv",'w') as resultFile:
        wr2 = csv.writer(resultFile, dialect='excel')
        for stack_index,info in succRex.items():
            wr2.writerow([stack_index]+info)
            
def ifSampling(rex_succ,stack_index,scale=1):
    values=rex_succ[stack_index]
    if sum(values[1:])<values[0]*scale:
        return (-1,values[0]*scale)
    for value in values[1:]:
        if value<values[0]*scale:
            return (1,values[0]*scale)
    return (0,values[0]*scale)

def getRexCov1(sdfa,ddfas,succ):
    cov_match=Coverage(sdfa)
    succ_dfa=0
    for ddfa in ddfas:
        if ddfa.isMatch:
            cov_match.update(ddfa)
            succ_dfa+=1
        if succ_dfa>=succ:
            break  
    coverages=cov_match.calculate()
    return succ_dfa,coverages

def getRexCov2(sdfa,ddfas,succ):
    cov_match=Coverage(sdfa)
    for ddfa in ddfas:
        cov_match.update(ddfa)
    coverages=cov_match.calculate()
    return coverages

def getAveragesCov(info,rep=10):
    t_nodes=set([cov[1] for cov in info])
    t_edges=set([cov[3] for cov in info])
    t_epairs=set([cov[5] for cov in info])
    
    if len(t_nodes)!=1 or len(t_edges)!=1 or len(t_epairs)!=1:
        raise ValueError('total number of nodes, edges, epairs should be same across the repetitions')

    sum_nodes=sum(cov[0] for cov in info)
    sum_edges=sum(cov[2] for cov in info)
    sum_epairs=sum(cov[4] for cov in info)    
    return [sum_nodes,t_nodes.pop()*rep,sum_edges,t_edges.pop()*rep,sum_epairs,t_epairs.pop()*rep]
        
def covRex(scale=1, rep=10): 
    repetition=rep
    input_dirs=getInputDirs(scale, repetition)
    
    for encoding in ['ASCII']:
#     for encoding in ['ASCII', "Unicode"]:
        if scale!=1:
            rex_succ2=pickle.load(open(str(scale)+encoding+"Succ2.regex",'rb'))
        else:
            rex_succ2=pickle.load(open(encoding+"Succ2.regex",'rb'))
        rex_cov=dict()
        for stack_index in rex_succ2:
            m_handle,succ=ifSampling(rex_succ2, stack_index, scale)
            if m_handle<0: ##drop
                continue
            
            rex_cov[stack_index]=[]
            if m_handle==0: ## calculate seperately
                for i in range(repetition):
                    encoding_dir=dfa_dir+input_dirs[i]+encoding+"/"
                    sdfa_file_path=encoding_dir+"static/"+str(stack_index)+".regex"
                    ddfas_file_path=encoding_dir+"dynamic/"+str(stack_index)+".regex"
                    sdfa=pickle.load(open(sdfa_file_path,'rb'))
                    ddfas=pickle.load(open(ddfas_file_path,'rb'))
                    succ_dfa,coverages=getRexCov1(sdfa,ddfas.values(),succ)
                    rex_cov[stack_index].append(coverages)
            else: ##use bootstrapping to sample 
                ##get all ddfas
                all_ddfa=[]
                for i in range(repetition):
                    encoding_dir=dfa_dir+input_dirs[i]+encoding+"/"
                    ddfas_file_path=encoding_dir+"dynamic/"+str(stack_index)+".regex"
                    ddfas=pickle.load(open(ddfas_file_path,'rb'))
                    succ_ddfas=[ddfa for ddfa in ddfas.values() if ddfa.isMatch ]
                    all_ddfa.extend(succ_ddfas)
                len_all=len(all_ddfa)
                
                for i in range(repetition):
                    encoding_dir=dfa_dir+input_dirs[i]+encoding+"/"
                    sdfa_file_path=encoding_dir+"static/"+str(stack_index)+".regex"                    
                    sdfa=pickle.load(open(sdfa_file_path,'rb'))
                    print("stack_index:",stack_index,"len_all:",len_all,"succ:",succ)
                    ddfa_index=np.random.choice(len_all,succ,replace=False)
                    ddfas=[all_ddfa[index] for index in ddfa_index]
                                        
                    coverages=getRexCov2(sdfa,ddfas,succ)
                    rex_cov[stack_index].append(coverages)
        
        file_output=output_cov_dir+str(scale)+"_"+encoding
        output=open(file_output+"_cov.regex",'wb')
        pickle.dump(rex_cov, output, pickle.HIGHEST_PROTOCOL)
        output.close()
        
        with open(file_output+"_cov.csv",'w') as resultFile:
            wr2 = csv.writer(resultFile, dialect='excel')
            for stack_index,info in rex_cov.items():
                wr2.writerow([stack_index]+info)   
        ##print avg
        with open(file_output+"_avgCov.csv",'w') as resultFile:
            wr2 = csv.writer(resultFile, dialect='excel')
            for stack_index,info in rex_cov.items():
                avgs=getAveragesCov(info,rep)
                wr2.writerow([stack_index]+avgs) 

def covRex2(scale=1, rep=10): 
    repetition=rep
    input_dirs=getInputDirs(scale, repetition)
    
    for encoding in ['ASCII']:
#     for encoding in ['ASCII', "Unicode"]:
        if scale!=1:
            rex_succ2=pickle.load(open(str(scale)+encoding+"Succ2.regex",'rb'))
        else:
            rex_succ2=pickle.load(open(encoding+"Succ2.regex",'rb'))
        rex_cov=dict()
        rex_dfa=dict()
        for stack_index in rex_succ2:
            succ=rex_succ2[stack_index][0]*scale
            
            rex_cov[stack_index]=[]
            rex_dfa[stack_index]=[]
            for i in range(repetition):
                encoding_dir=dfa_dir+input_dirs[i]+encoding+"/"
                sdfa_file_path=encoding_dir+"static/"+str(stack_index)+".regex"
                ddfas_file_path=encoding_dir+"dynamic/"+str(stack_index)+".regex"
                sdfa=pickle.load(open(sdfa_file_path,'rb'))
                ddfas=pickle.load(open(ddfas_file_path,'rb'))
                succ_dfa,coverages=getRexCov1(sdfa,ddfas.values(),succ)
                
                rex_cov[stack_index].append(coverages)
                rex_dfa[stack_index].append(succ_dfa)
                
        file_output=output_cov_dir+str(scale)+"_"+encoding
        output=open(file_output+"_cov2.regex",'wb')
        pickle.dump(rex_cov, output, pickle.HIGHEST_PROTOCOL)
        output.close()
        
        with open(file_output+"_cov2.csv",'w') as resultFile:
            wr2 = csv.writer(resultFile, dialect='excel')
            for stack_index,info in rex_cov.items():
                wr2.writerow([stack_index]+info)   
        ##print avg
        with open(file_output+"_avgCov2.csv",'w') as resultFile:
            wr2 = csv.writer(resultFile, dialect='excel')
            for stack_index,info in rex_cov.items():
                avgs=getAveragesCov(info,rep)
                wr2.writerow([stack_index]+avgs) 
                        
        output=open(file_output+"_dfa2.regex",'wb')
        pickle.dump(rex_dfa, output, pickle.HIGHEST_PROTOCOL)
        output.close()
        
        with open(file_output+"_dfa2.csv",'w') as resultFile:
            wr2 = csv.writer(resultFile, dialect='excel')
            for stack_index,info in rex_dfa.items():
                wr2.writerow([stack_index]+info)   
        ##print avg
        with open(file_output+"_avgdfa2.csv",'w') as resultFile:
            wr2 = csv.writer(resultFile, dialect='excel')
            for stack_index,info in rex_dfa.items():
                wr2.writerow([stack_index,sum(info),rep])
                                       
def validSuccRex(scale=1, rep=10): 
    repetition=rep
    input_dirs=getInputDirs(scale, repetition)
    
    for encoding in ['ASCII']:
#         for encoding in ['ASCII', "Unicode"]:
        rex_succ=pickle.load(open(encoding+"Succ.regex",'rb'))
        rex_succ2=dict()
        for stack_index, v in rex_succ.items():
            succ,nodes,edges,epairs=v
            rex_succ2[stack_index]=[succ]
            for i in range(repetition):
                encoding_dir=dfa_dir+input_dirs[i]+encoding+"/"
                sdfa_file_path=encoding_dir+"static/"+str(stack_index)+".regex"
                ddfas_file_path=encoding_dir+"dynamic/"+str(stack_index)+".regex"
                sdfa=pickle.load(open(sdfa_file_path,'rb'))
                cov=Coverage(sdfa)
                ddfas=pickle.load(open(ddfas_file_path,'rb'))
                succ_ddfa=0
                for input, ddfa in ddfas.items():
                    if ddfa.isMatch:
                        succ_ddfa+=1
                rex_succ2[stack_index].append(succ_ddfa)
        
        output=open(str(scale)+encoding+"Succ2.regex",'wb')
        pickle.dump(rex_succ2, output, pickle.HIGHEST_PROTOCOL)
        output.close()
        
        file_name=str(scale)+encoding+"_succ2.csv"
        with open(file_name,'w') as resultFile:
            wr2 = csv.writer(resultFile, dialect='excel')
            for stack_index,info in rex_succ2.items():
                wr2.writerow([stack_index]+info)   
            
def saveSuccRex(): 
    ## stack_count.csv import the count for successful matching from Github repos
    ###stack_count,len(uniInputs),len(valid_inputs),succ,fail
    stackSucc_dict=dict()
    dropped=0
    with open('stack_count.csv', 'r') as csvfile:
        csvReader = csv.reader(csvfile, dialect='excel')
        for row in csvReader:
            stack_index, uniInputs, validInputs, succ, fail=[int(x) for x in row]
            if succ>0:
                stackSucc_dict[stack_index]=succ
            else:
#                 print("drop stack because of no succ inputs: ", row)
                dropped+=1
    print("regex with succ: ",len(stackSucc_dict))
    print("regex without succ: ",dropped)
    
    output=open(ws+"repoSucc.regex",'wb')
    pickle.dump(stackSucc_dict, output, pickle.HIGHEST_PROTOCOL)
    output.close()

    file_name=ws+"repo_succ.csv"
    with open(file_name,'w') as resultFile:
        wr2 = csv.writer(resultFile, dialect='excel')
        for stack_index,succ in stackSucc_dict.items():
            wr2.writerow([stack_index,stack_index])      
    
    for encoding in ['ASCII', "Unicode"]:
        rex_succ=dict()
        dropped=0
        with open(encoding+'_sdfa_info.csv', 'r') as csvfile:
            csvReader = csv.reader(csvfile, dialect='excel')
            for row in csvReader:
                stack_index, nodes, edges, epairs=[int(x) for x in row]
                if stack_index in stackSucc_dict:
                    succ=stackSucc_dict[stack_index]
                    rex_succ[stack_index]=[succ,nodes,edges,epairs]
                else:
#                     print("drop succ stack because Rex invalid: ", row)
                    dropped+=1  
        print("rex regex with succ: ",len(rex_succ))
        print("rex regex without succ: ",dropped)
        output=open(encoding+"Succ.regex",'wb')
        pickle.dump(rex_succ, output, pickle.HIGHEST_PROTOCOL)
        output.close()
        
        file_name=encoding+"_succ.csv"
        with open(file_name,'w') as resultFile:
            wr2 = csv.writer(resultFile, dialect='excel')
            for stack_index,info in rex_succ.items():
                wr2.writerow([stack_index]+info)   
def getRexSDFA(scale=1, rep=10):   
    repetition=rep
    if scale==1:
        input_dirs=["input_"+str(count)+"/" for count in range(repetition)]
    else:
        input_dirs=["input_"+str(scale)+"_"+str(count)+"/" for count in range(repetition)]
    
    
    for encoding in ['ASCII','Unicode']:
        stacksRep=[]
        for i in range(repetition):
            output_dir=dfa_dir+input_dirs[i]
            encoding_dir=output_dir+encoding+"/"
            static_dir=encoding_dir+"static/"
            stacks=getStackIndex(static_dir)
            print("i: ",i, "encoding: ",encoding,"stack len: ",len(stacks))
            
#             with open(encoding_dir+"stack_index.csv", 'w') as myfile:
#                 wr = csv.writer(myfile, dialect='excel')
#                 for stack_index in stacks:
#                     wr.writerow([stack_index])
            with open(encoding_dir+"sdfa_info.csv", 'w') as myfile:
                wr = csv.writer(myfile, dialect='excel')
                for sdfa_info in stacks:
                    wr.writerow(list(sdfa_info))
            stacksRep.append(stacks)
    
        stack_0=set(stacksRep[0])
        for i in range(1,repetition):
            if set(stacksRep[i])!=stack_0:
                print("different stack index: ", 0, ": ",i)
                return
        
        with open(ws+encoding+"_sdfa_info.csv", 'w') as myfile:
                wr = csv.writer(myfile, dialect='excel')
                for sdfa_info in stacksRep[0]:
                    wr.writerow(list(sdfa_info))
#         with open(ws+encoding+"_stack_index.csv", 'w') as myfile:
#                 wr = csv.writer(myfile, dialect='excel')
#                 for stack_index_set in zip(*stacksRep):
#                     wr.writerow(list(stack_index_set))
def saveRegexDict():
    stack_dict=dict()
    with open('stack_regex2.csv', mode='r') as infile:
        reader = csv.reader(infile)
        for row in reader:
            stack_index,regex_index,validCount=row
            stack_dict[int(stack_index)]=[int(regex_index),int(validCount)]

    regexfile_all=open("unique.regex",'rb')
    regex_all=pickle.load(regexfile_all)
    regex_dict=dict()
    for regexStr,regex_index in regex_all.items():
        regex_dict[regex_index]=regexStr
    
    output=open(ws+"stackIndex.regex",'wb')
    pickle.dump(regex_dict, output, pickle.HIGHEST_PROTOCOL)
    output.close()
    
    file_name=ws+"index_regex.csv"
    with open(file_name,'w') as resultFile:
        wr2 = csv.writer(resultFile, dialect='excel')
        for index,stack in regex_dict.items():
            wr2.writerow([index,stack])          

def getSinglePaths(scale=1, rep=10,encoding="ASCII"):
    file_output=output_cov_dir+str(scale)+"_"+encoding    
    stack_indexs=[]
    with open(file_output+"_cov.csv",'r') as csvfile:
            csvReader = csv.reader(csvfile, dialect='excel')
            for row in csvReader:
                stack_indexs.append(row[0])
                
    input_dirs=getInputDirs(scale, rep)
    static_dir=dfa_dir+input_dirs[0]+encoding+"/static/"
    t=0
    for stack_index in stack_indexs:
        sdfa_file_path=static_dir+str(stack_index)+".regex"
        sdfa=pickle.load(open(sdfa_file_path,'rb')) 
        if sdfa.isSinglePath():
            t+=1
    print("total: ",len(stack_indexs)," singlePath: ",t)                                                      
if __name__== '__main__':
    os.chdir(ws)
#     getSinglePaths(1,10,"ASCII")
#     covRex2(1, 10)
    covRex2(5, 5)
    covRex2(10, 5)
#     validSuccRex(10,5)
#     calRex2(1, 10)
#     calRex(10, 5)
#     calRex3(5, 5,"ASCII")
#     calRex3(10, 5,"ASCII")
#     calRex3(10, 5,"ASCII",4)
#     calRex3(10, 5,"ASCII",3)
#     calRex(20, 5)
#     getRexSDFA(1,5)
    exit(0)
#     exp()
#     exp(10,5)  ##scale 10, rep 5
#     exp(5,5)
#     exp(20,5) 
#     calRex(1,10)
#     exportCount2CSV("count_unicode.regex", "count_unicode.csv")
#     exportCount2CSV("count_ascii.regex", "count_ascii.csv")
#     
#     regex_all,regex_failed=getRegexes()
#     regexInfo=getRegexInfo()
#     rex_failed,rex_timed=getRexFailedTimed()    
#     count_ascii=calRexCovAscii(regex_all,regex_failed,rex_failed,rex_timed,regexInfo)
#     pickle.dump(count_ascii,open("count_ascii.regex",'wb'))
#     count_unicode=calRexCovUnicode(regex_all,regex_failed,rex_failed,rex_timed,regexInfo)
#     pickle.dump(count_unicode,open("count_unicode.regex",'wb'))
      
#     regex_all,regex_failed=getRegexes()
#     generateStrings(regex_all,regex_failed)
