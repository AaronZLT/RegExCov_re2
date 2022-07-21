'''
Created on Dec 7, 2017

@author: peipei
'''

class RegexTrace(object):
    '''
    classdocs
    '''        
    def __init__(self, regex, file=None, fullclass=None, method=None):
        '''
        Constructor
        '''
        self.regex=regex
        self.file=file
        self.fullclass=fullclass
        self.method=method
#         self.lines=None
        self.str=(self.regex+":("+self.file+","+self.fullclass+","+self.method+")").encode('utf-8')

    def __cmp__(self,other):
        if self.regex==other.regex and self.file==other.file and self.fullclass==other.fullclass and self.method==other.method:
            return 0
        elif self.regex>other.regex or self.fullclass>other.fullclass or self.method>other.method or self.file>other.file:
            return 1
        else:
            return -1
    
    def __eq__(self, other): ## for comparison in list
        return self.str==other.str
    
    def __hash__(self): ## for comparison in list or dict=====hashing for dictionary
        return hash(self.str)
    
    def __str__(self):        
        return self.str
 
    def toString(self):
        return self.__str__()