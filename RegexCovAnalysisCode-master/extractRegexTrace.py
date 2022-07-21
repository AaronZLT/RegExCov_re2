'''
Created on Dec 7, 2017
input:  id.log which has the regex matches() stacktrace
output: id.regex----key:(regex_str,file_str,class_str,method_str) value: [input_str]
@author: peipei
'''
import re
import sys
import os
import codecs
import pickle
import csv
import traceback
import glob

#stack_trace=r'^Stack Trace from: (?P<method>.*) in class: (?P<class>.*)\[on line number: (?P<line>-?[0-9]+) of file: (?P<file>.*\.java|null|\<generated\>)\]'
stack_trace=r'^Stack Trace from: (?P<method>.*) in class: (?P<class>.*)\[on line number: (?P<line>-?[0-9]+) of file: (?P<file>.*)\]'
pattern_full=r'^Pattern matches\(String regex, CharSequence input\)---regex: (?P<regex>.*)---input: (?P<input>.*)---#$'''
matcher_full=r'^Matcher matches\(\)---regex: (?P<regex>.*)---input: (?P<input>.*)---#$'''

pattern_first=r'Pattern matches(String regex, CharSequence input)---regex: '
matcher_first=r'Matcher matches()---regex: '

#ws="/home/peipei/ISSTA2018/data/regex_log/1.7/"
ws="/home/peipei/RepoReaper/loggings/"
output_dir="/home/peipei/ISSTA2018/data/regex/1.7/"
# ws="/home/pwang7/log/"
# output_dir="/home/pwang7/log/"
stack_regex=re.compile(stack_trace)
pattern_regex=re.compile(pattern_full,re.DOTALL|re.MULTILINE)
matcher_regex=re.compile(matcher_full,re.DOTALL|re.MULTILINE)

def getlogs(i):
    '''get all logs i_*.log'''
    log_pattern=str(i)+"_*_*.log"
    t=glob.glob(log_pattern)
    return t

def process(i):
    logs=getlogs(i)
    for log in logs:
        proj=log[:-4]
        print("process project: ",proj)
        f = codecs.open(log, 'r',encoding='utf-8')
        dict_regex=dict()
        trace=list()
        i=0
        prevline=''
        isLogBegin=False
        for line in f:
            i+=1
#             if line=='':
#                     print("!!!!!!!!Possible mutiple line matches regex!!!!!!!!")
#                     continue
            m1=stack_regex.match(line)
            if m1 is not None:
                method_str=m1.group('method')  ##matches
                class_str=m1.group('class')
                line_int=int(m1.group('line'))
                file_str=m1.group('file')  ##Matcher.java Pattern.java
                strace=(file_str,line_int,class_str,method_str)
                trace.append(strace)            
                continue
            #not stack trace, it is regex and string    
            m1=pattern_regex.match(line)
            isMatcherMatch=False
            if m1 is None and prevline!='':
                m1=pattern_regex.match(prevline+line)
                if m1 is not None:
                    prevline=''
                    isLogBegin=False
                        
            if m1 is None:
                m1=matcher_regex.match(line)
                isMatcherMatch=True 
            if m1 is None and prevline!='':
                m1=matcher_regex.match(prevline+line)
                if m1 is not None:
                    prevline=''
                    isLogBegin=False
                    
            if m1 is not None:
    #             print("Matcher match" if isMatcherMatch else "Pattern match")        
                regex_str=m1.group('regex')
                input_str=m1.group('input')                
                ### get the first trace after matches()
                for e in trace[1:]:
                    if e[3]!='matches' and e[2] not in ['java.lang.String', 'java.util.Pattern','java.util.Matcher']:                            
                        try:    
                            regexTrace=(e[0],e[2],e[3],regex_str,input_str) ##file,fullclass, method
                            if regexTrace not in dict_regex:
                                dict_regex[regexTrace]=[] ###set not duplicated input_str
                            dict_regex[regexTrace].append(i)
                        except:
                            print("Unexpected error:", sys.exc_info()[0])
                            traceback.print_exc()
                            raise
                        break                        
                trace=[]
            else:
                if line.startswith(pattern_first) or line.startswith(matcher_first):
                    isLogBegin=True
#                     print("start log matcher/pattern")
#                     print("line: ",i," content: ",line)
                
                if isLogBegin:
                    prevline=prevline+line
                else:
                    print("ERROR!!!!!!!!!!!!")
                    print("line: ",i," content: ",line)
                                
        f.close()
        print("len dict regex: ",len(dict_regex))
        if len(dict_regex)>0:
            print("picking regex project: ",proj)
            output=open(output_dir+proj+".regex",'wb')
            pickle.dump(dict_regex, output)
            output.close() 
            print("dumped regex") 
        
        if len(dict_regex)>0:
            print("saving csv regex project: ",proj)
            file_name=output_dir+proj+"_regex.csv"
            with open(file_name,'w') as resultFile:
                wr = csv.writer(resultFile, dialect='excel')
                for key, value in dict_regex.items():
                    wr.writerow([key, value])
#             with open('dict.csv', 'rb') as csv_file:
#                 reader = csv.reader(csv_file)
#                 mydict = dict(reader)


if __name__== '__main__':
    if sys.argv is None or len(sys.argv)<2: #[begin,end)
        sys.exit('Error! You need to specify one project ID or both begin and end project ID!!')
    begin=int(sys.argv[1])
    end=begin
    if len(sys.argv)==3:
        end=int(sys.argv[2])
    elif len(sys.argv)==2:
        end=begin+1
    print(begin, end)
    os.chdir(ws)
    for i in range(begin,end):
        try:
            process(i)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
