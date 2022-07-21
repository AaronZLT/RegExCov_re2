'''
Created on Jan 14, 2018

@author: peipei
'''
import subprocess
import traceback
import sys
import re
from DFA import StaticDFA,DynamicDFA,Coverage
import pickle
import csv

dfa_obj="/home/peipei/re2/getDFA"
dfa_str1='^pattern: "(.*)"$'
dfa_str2=r'^pattern: "(.*)" forward_size: (\d+)$'
dfa_str3=r'^byte range size: (\d+) byte ranges are: $'
dfa_str4=r'^is match: (0|1) \[(.+),\]$'
dfa_str5=r'^range: (\d+) bytes: (.+),$'

dfa_str6=r'^pattern: "(.*)" input: "(.*)"$'
dfa_str7=r'pattern: "(.*)" input: "(.*)" ismatch: (0|1)$'
dfa_str8=r'^initial: (.+) isMatch: (0|1)$'
dfa_str9=r'^(.+) byte: (\d+) next: (.+) isMatch: (0|1)$'
dfa_str10=r'^(.+) lastbyte: (\d+) next: (.+) isMatch: (0|1)$'
dfa_re1=re.compile(dfa_str1,re.DOTALL)
dfa_re2=re.compile(dfa_str2,re.DOTALL)
dfa_re3=re.compile(dfa_str3)
dfa_re4=re.compile(dfa_str4)
dfa_re5=re.compile(dfa_str5)
dfa_re6=re.compile(dfa_str6,re.DOTALL)
dfa_re7=re.compile(dfa_str7,re.DOTALL)
dfa_re8=re.compile(dfa_str8)
dfa_re9=re.compile(dfa_str9)
dfa_re10=re.compile(dfa_str10)

output_static_dir="/home/peipei/ISSTA2018/data/dfa/static/"
output_dynamic_dir="/home/peipei/ISSTA2018/data/dfa/dynamic/"
# output_dynamic_dir="/home/peipei/ISSTA2018/data/dfa/rex/"
# output_dynamic_dir="/home/peipei/ISSTA2018/data/dfa/rex/ascii/"
# output_dynamic_dir="/home/peipei/ISSTA2018/data/dfa/rex/unicode/"
output_coverage_dir="/home/peipei/ISSTA2018/data/cov/"
def execute(cmd):
    """
        Purpose  : To execute a command and return exit status
        Argument : cmd - command to execute
        Return   : exit_code
    """
    print("command:", cmd)
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #Drop shell=True. The arguments to Popen() are treated differently on Unix if shell=True:
        (result, error) = process.communicate()
        if result:
            return (process.returncode,result)       
        if error:
            print("Error: failed to execute command")
            return (process.returncode,error)
    except OSError as e:
        print("OSError > ",e.errno)
        print("OSError > ",e.strerror)
        print("OSError > ",e.filename)
    except ValueError as ve:
        print("ValueError > ",ve)
        return (10,"has nullbyte errors")
    except:
        print("Error > ",sys.exc_info()[0])
        traceback.print_exc(file=sys.stdout)
        raise

def splitlines(res):
#     return re.findall('(?:"[^"]*"|.)+', res) 
    return re.findall('(?:"[.\n]*"|.)+', res)

def getStaticForwardDFA(output):
#     lines=splitlines(output)    
#     res=dfa_re1.match(lines[0])
    res=re.match('^pattern: "(.*)"\nis match:',output,re.DOTALL|re.MULTILINE)
    if not res:
        print("not correct Static DFA format")
        raise Exception("not correct Static DFA format")
    pattern=res.group(1)
    pos1=res.end(1)
    
    
    res=re.search(r',]\npattern: "(.*)" forward_size: (\d+)\n',output,re.DOTALL|re.MULTILINE)
    if not res:
        print("not correct Static DFA format")
        raise Exception("not correct Static DFA format")
    pattern2=res.group(1)
    size=int(res.group(2))    
    if pattern2!=pattern:
        print("pattern not equal not correct Static DFA format")
        raise Exception("not correct Static DFA format")
    pos2=res.start(1)
    
    
    res=re.search(r'forward_size: \d+\nbyte range size: (\d+) byte ranges are: \n',output,re.MULTILINE)
    if not res:
        print("not correct Static DFA format")
        raise Exception("not correct Static DFA format")
    byte_range=int(res.group(1))
    pos3=res.end(1)
    
    
    dfa=StaticDFA(pattern,size,byte_range)
    
#     lines=dfa_re4.findall(output)
#     for line in lines:
    dfa_re=re.compile(r'\nis match: (0|1) \[(.+),\]\n',re.MULTILINE)
    res=dfa_re.search(output,pos1,pos2)
    count=0
    while res is not None:
        count+=1
        isMatch=bool(int(res.group(1)))
        sfrom=dfa.appendState(isMatch)
        
        nexts=res.group(2).split(",")
        if len(nexts)>byte_range:
            print("not correct dfa format")
            raise Exception("not correct Static DFA format")
        for next in nexts:
            t_edges=dfa.appendEdge(sfrom, int(next))
        
        pos1=res.end(2)
        res=dfa_re.search(output,pos1,pos2)
    if count<size:
        print("DFA size not equal")
        raise Exception("DFA size not equal")
    
    dfa_re=re.compile(r'\nrange: (\d+) bytes: (.+),\n',re.MULTILINE)
    res=dfa_re.search(output,pos3)
    count=0
    while res is not None:
        count+=1        
        index=int(res.group(1))
        passbytes=res.group(2).split(",")
        passbytes=[int(passbyte) for passbyte in passbytes]
        
        s_range=dfa.appendByteRange(index, passbytes)
        if s_range>byte_range:
            print("not correct dfa format")
            raise Exception("not correct Static DFA format") 
        
        pos3=res.end(2)
        res=dfa_re.search(output,pos3)
    if count<byte_range:
        print("DFA byte range not equal")
        raise Exception("DFA byte range not equal") 
    return dfa

mode_modifiers=["(?i)","(?m)","(?s)","(?U)"]
#mode_re=re.compile("(\(\?[imsU]{1,4}\))\^(.*)") ##regexStr=res.group(1)+res.group(2)
mode_re=re.compile("(\(\?(?!.{0,2}(.).{0,2}\\2)[imsU]{1,4}\))\^(.*)",re.DOTALL)
def removeAnchorFlag(regexStr):
#         regexStr=regexStr.encode('utf-8')
        if len(regexStr)>1 and regexStr[0]=="^": ##except ^ should at least another char
                regexStr=regexStr[1:]
                
         
        if len(regexStr)>5 and regexStr[0]=="(":
            res=mode_re.match(regexStr)
            if res:
                regexStr=res.group(1)+res.group(3)
        return regexStr
    
def getStaticDFA(regexStr,index,outputDir=output_static_dir):
    try:
        regexStr=removeAnchorFlag(regexStr)
            
        status,res=execute([dfa_obj,regexStr])
            
        if status>0: ###error not valid regex
            print("could not compile pattern: ",regexStr)
            print(res)
            return None
        else:            
            print("process forward static DFA")
            res=res.decode('utf-8')
            dfa=getStaticForwardDFA(res)
            
            print("picking regex index: ",index)
            output=open(outputDir+str(index)+".regex",'wb')
            pickle.dump(dfa, output, pickle.HIGHEST_PROTOCOL)
            output.close() 
            print("dumped regex") 
                
            print("saving results output regex index: ",index)
            file_name=outputDir+str(index)+"_regex.txt"
            with open(file_name,'w') as resultFile:
                for line in splitlines(res):
                    resultFile.write(line)
                    resultFile.write("\n")
            
            
            return dfa
    except UnicodeEncodeError:
            print("Regex String Unicode error:", sys.exc_info()[0])
            traceback.print_exc()
#             pass
    except:
        print("Error in execute getStaticDFA")
        traceback.print_exc()
#         pass
            
def getStaticDFAByIndex(index,outputDir=output_static_dir):    
    input_dfa=open(outputDir+str(index)+".regex",'rb')
    dfa= pickle.load(input_dfa)
    return dfa

def getDynamicForwardDFA(sdfa,output):
#     lines=splitlines(res)
    pattern=None
    input=None
    isMatch=None
#     res=dfa_re6.match(lines[0])
    res=re.match(r'^pattern: "(.*)" input: "(.*)"\ninitial:',output,re.DOTALL|re.MULTILINE)
    if not res:
        print("not correct match format")
        return None
    pattern=res.group(1)
    input=res.group(2)
    
#     res=dfa_re7.match(lines[-1])
    res=re.search(r'\npattern: "(.*)" input: "(.*)" ismatch: (0|1)\n',output,re.DOTALL|re.MULTILINE)
    if not res or pattern!=res.group(1) or input!=res.group(2):
        print("not correct match format")
        return None
    isMatch=bool(int(res.group(3)))    
    ddfa=DynamicDFA(pattern,input,isMatch)    
        
#     res=dfa_re8.match(lines[1])
    res=re.search(r'"\ninitial: (.+) isMatch: (0|1)\n',output,re.MULTILINE)
    if not res:
        print("not correct match format")
        return None    
    states=dict()
    start=res.group(1)
    start_isMatchState=bool(int(res.group(2)))
    if not sdfa.isStart(start_isMatchState):
        print("not correct mapping to static dfa format")
        return None
    
    states[start]=[0,start_isMatchState]
    states['DeadState']=[-1,False]
#     for line in lines[2:-2]:
#         res=dfa_re9.match(line)
#         if not res:
#             print("not correct match format")
#             return None  
    dfa_re=re.compile(r'\n(.+) byte: (\d+) next: (.+) isMatch: (0|1)\n', re.MULTILINE)
    pos=res.end(2)
    res=dfa_re.search(output,pos)
    while res is not None:      
        sfrom=res.group(1)
        byte=int(res.group(2))
        sto=res.group(3)
        isMatch=bool(int(res.group(4)))
        if sfrom not in states:
            print("not correct match format")
            return None         
        mfrom=states[sfrom][0]
        if sto not in states:
            mto=sdfa.map(mfrom,byte,isMatch)
            if mto is None:
                print("not correct match format")
                return None
            states[sto]=[mto,isMatch]
        else:
            mto=states[sto][0]
        ddfa.appendEdge(mfrom,mto,byte)
        pos=res.end(4)
        res=dfa_re.search(output,pos)
    
    
#     res=dfa_re10.match(lines[-2])
    if ddfa.isMatch:
        res=re.search(r'\n(.+) lastbyte: (\d+) next: (.+) isMatch: (0|1)\n',output,re.MULTILINE)
        if res:
            sfrom=res.group(1)
            lastbyte=int(res.group(2))
            if lastbyte!=256:
                print("not correct match format")
                return None 
            sto=res.group(3)
            isMatch=bool(int(res.group(4)))
            mfrom=states[sfrom][0]   
            if ddfa.isMatch and sto!="DeadState" and isMatch:
                if sto not in states:
                    mto=sdfa.map(mfrom,lastbyte,isMatch)
                    if mto is None:
                        print("not correct match format")
                        return None
                    states[sto]=[mto,isMatch]
                else:
                    mto=states[sto][0]
                ddfa.appendEdge(mfrom,mto,lastbyte)
            elif not ddfa.isMatch and sto=="DeadState" and not isMatch:
                mto=-1
                states[sto]=[-1,False]
                ddfa.appendEdge(mfrom,mto,byte)
            else:
                print("not correct match format")
                return None
        else:
            print("not correct match format")
            return None                
    return ddfa

def getDynamicDFA(sdfa,regexStr,input):
    try:
        if type(regexStr)==str:
            regexStr=regexStr.encode('utf-8')
        if type(input)==str:
            input=input.encode('utf-8')
        if len(regexStr)>0 and regexStr[0]=="^":
            regexStr=regexStr[1:]
        if len(regexStr)>0 and regexStr[-1]=="$":
            regexStr=regexStr[:-1]
        status,res=execute([dfa_obj,regexStr,input])                    
        if status>0: ###error not valid regex
            print("could not build Dynamic DFA pattern: ",regexStr," input:",input)
            print(res)
            if status==10:
                return (10,None)
            else:  
                raise Exception(res)
        else:            
            print("process forward dynamic DFA")
            res=res.decode('utf-8')
            ddfa=getDynamicForwardDFA(sdfa,res)
            return (0,ddfa)
    except UnicodeEncodeError:
            print("Regex String Unicode error:", sys.exc_info()[0])
            traceback.print_exc()
#             pass
    except:
        print("Error in execute staticDFAs")
        traceback.print_exc()
#         pass

def getDynamicDFAs(index,inputs,outputDir=output_dynamic_dir, sdfaDir=output_static_dir):  
    dfa=getStaticDFAByIndex(index,sdfaDir)
    pattern=dfa.getPattern()
    
    ddfa_dict=dict()
    for input in inputs:
        if len(input)>131071:
            print("failed to build dynamic dfa due to input string is too long for bash : ",input[:100],"...")
            continue
        
        ret,ddfa=getDynamicDFA(dfa,pattern, input)
        if ret==10 and ddfa is None:
            print("failed to build dynamic dfa due to invalid input: ",input)
        elif ddfa is None:
            raise Exception("Dynamic DFA is None")
        else:
            ddfa_dict[input]=ddfa
        
    print("picking regex dynamic inputs index: ",index)
    output=open(outputDir+str(index)+".regex",'wb')
    pickle.dump(ddfa_dict, output, pickle.HIGHEST_PROTOCOL)
    output.close() 
    print("dumped regex") 
        
    print("saving results output regex index: ",index)
    file_name=outputDir+str(index)+"_dfas.txt"
    with open(file_name,'w') as resultFile:
        for input, ddfa in ddfa_dict.items():
            resultFile.write("pattern:"+pattern+" input:"+input)
            resultFile.write("\n")
            edges=ddfa.getEdges()
            isMatch=ddfa.isMatch
            for mfrom,byte,mto in edges:
                resultFile.write(str(mfrom)+":"+str(byte)+":"+str(mto)+":"+str(isMatch))
                resultFile.write("\n")
    return ddfa_dict

def getDynamicDFAs2(index,inputs,succ,outputDir=output_dynamic_dir, sdfaDir=output_static_dir):  
    dfa=getStaticDFAByIndex(index,sdfaDir)
    pattern=dfa.getPattern()
    
    count_succ=0
    ddfa_dict=dict()
    for input in inputs:
        if len(input)>131071:
            print("failed to build dynamic dfa due to input string is too long for bash : ",input[:100],"...")
            continue
        
        ret,ddfa=getDynamicDFA(dfa,pattern, input)
        if ret==10 and ddfa is None:
            print("failed to build dynamic dfa due to invalid input: ",input)
        elif ddfa is None:
            raise Exception("Dynamic DFA is None")
        else:
            if ddfa.isMatch:
                ddfa_dict[input]=ddfa
                count_succ+=1
                if count_succ>=succ:
                    break
        
    print("picking regex dynamic inputs index: ",index)
    output=open(outputDir+str(index)+".regex",'wb')
    pickle.dump(ddfa_dict, output, pickle.HIGHEST_PROTOCOL)
    output.close() 
    print("dumped regex") 
        
    print("saving results output regex index: ",index)
    file_name=outputDir+str(index)+"_dfas.txt"
    with open(file_name,'w') as resultFile:
        for input, ddfa in ddfa_dict.items():
            resultFile.write("pattern:"+pattern+" input:"+input)
            resultFile.write("\n")
            edges=ddfa.getEdges()
            isMatch=ddfa.isMatch
            for mfrom,byte,mto in edges:
                resultFile.write(str(mfrom)+":"+str(byte)+":"+str(mto)+":"+str(isMatch))
                resultFile.write("\n")
    return ddfa_dict
                
def getDynamicDFAsByIndex(index):
    input_dfa=open(output_dynamic_dir+index+".regex",'r')
    ddfa= pickle.load(input_dfa)
    return ddfa

def getDynamicDFAsByInput(index,input):
    ddfa=getDynamicDFAsByIndex(index)
    if input in ddfa:
        return ddfa[input]
    else:
        return None             
            

def getCoverages(sdfa,ddfas):
    cov_total=Coverage(sdfa)
    cov_match=Coverage(sdfa)
    cov_mismatch=Coverage(sdfa)
    
    for input,ddfa in ddfas.items():
        if ddfa.isMatch:
            cov_match.update(ddfa)
        else:
            cov_mismatch.update(ddfa)
        cov_total.update(ddfa)
    
    coverages=[cov_total.calculate(),cov_match.calculate(),cov_mismatch.calculate()]
    return coverages
def getSuccessCoverage(sdfa,ddfas):
    cov_match=Coverage(sdfa)
    for input,ddfa in ddfas.items():
        if ddfa.isMatch:
            cov_match.update(ddfa)
        else:
            raise Exception("Dynamic DFA is not matched!!!")
    return cov_match.calculate()

def CalculateCov(index,regexStr,inputs):
    if len(regexStr)>131071: ##The maximum size for a single string argument is limited to 131072
        return 2
    
    
    sdfa=getStaticDFA(regexStr, index)
    if sdfa is None: ##compilation error
        return 1
    
    ddfas=getDynamicDFAs(index,inputs)
    coverages=getCoverages(sdfa,ddfas)
               
    print("saving results output regex index: ",index)
    file_name=output_coverage_dir+"regex_cov.csv"
    with open(file_name,'a+') as resultFile:
        wr = csv.writer(resultFile, dialect='excel')        
        for i in range(0,3):
            t=[index]
            t.extend(coverages[i])
            t.append(i)
            wr.writerow(t)
    return 0
if __name__== '__main__':
    dfa=getStaticDFA(1,b"\n")