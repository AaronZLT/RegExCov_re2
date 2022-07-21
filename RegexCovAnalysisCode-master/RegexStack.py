'''
Created on Feb 13, 2018

@author: peipei
'''

class RegexStack(object):
    '''
    classdocs
    '''


    def __init__(self, rpage,rrow,rfile,rclass,rmethod,regex,count):
        '''
        Constructor
        '''
        self.page=rpage
        self.row=rrow
        self.file=rfile
        self.regex_class=rclass
        self.method=rmethod
        self.regex=regex
        self.count=count
        self.inputs=dict()
        self.failed=False
    
    def addInput(self,input_str,input_count):
        self.inputs[input_str]=input_count
    
    def getInputNums(self):
        return len(self.inputs)
    
    def isDFAFailed(self):
        return self.isFailed
    
    def setDFAFailed(self):
        self.failed=True
     
    def setIndex(self,index):
       self.index=index
    
    def setRegexIndex(self,index):
        self.rindex=index
          
    def toList(self):
        return [self.index,self.page,self.row,self.file,self.regex_class,self.method,self.regex,self.count,self.getInputNums()]