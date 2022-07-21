'''
Created on Jan 14, 2018

@author: peipei
'''
from pandas.util._decorators import indent
class StaticDFA(object):
    '''
    classdocs
    '''


    def __init__(self, pattern, size, byte_range):
        '''
        Constructor
        '''
        self.pattern=pattern
        self.size=size+1
        self.byte_range=byte_range
        
        self.states=dict()
        self.states[-1]=[]            
        self.matchStates=[]
        self.byteranges=dict()
    
    def appendState(self,isMatch):
        index=len(self.states)-1
        if isMatch:
            self.matchStates.append(index)
        self.states[index]=[]
        return index
    
    def appendEdge(self,sfrom,sto):
        self.states[sfrom].append(sto)
        return len(self.states[sfrom])
    
    def isSinglePath(self):
        res=True
        for sfrom in self.states:
            if sfrom==-1:
                continue            
            sl=len(self.states[sfrom])
            hasError=-1 in self.states[sfrom]
            
            if hasError and sl==2:
                continue
            elif not hasError and sl==1:
                continue
            else:
                res=False
                break
        return res
    
    def appendByteRange(self,index,bytes):
        self.byteranges[index]=bytes
        return len(self.byteranges)
    
    def getPattern(self):
        return self.pattern
    
    def getStates(self):
        return self.states
    
    def isStart(self,isMatch):
        if isMatch and 0 in self.matchStates:
            return True        
        if not isMatch and 0 not in self.matchStates:
            return True        
        return False
    
    def getRange(self,byte):
        for ind,bytes in self.byteranges.items():
            if byte in bytes:
                return ind
        return None
    
    def map(self,mfrom,byte,isMatch):
        ind=self.getRange(byte)
        mto=self.states[mfrom][ind]
        if isMatch and mto in self.matchStates:
            return mto
        if not isMatch and mto not in self.matchStates:
            return mto
        return None
    
class DynamicDFA(object):
    def __init__(self, pattern, input, isMatch):
        '''
        Constructor
        '''
        self.pattern=pattern
        self.input=input
        self.isMatch=isMatch
        self.edge=list()
    def isMatch(self):
        return self.isMatch
    def getEdges(self):
        return self.edge
    
    def appendEdge(self,mfrom,mto,byte):
        self.edge.append((mfrom,byte,mto))
    
class Coverage(object):
    def __init__(self, sdfa):
        '''
        Constructor
        '''
        states=sdfa.getStates()
        self.nodes=dict()
        for node in states.keys():
            self.nodes[node]=0
        
        self.edges=dict()
        for node,edges in states.items():
            for nto in edges:
                self.edges[(node,nto)]=0
        
        self.edgePairs=dict()
        for node,nto in self.edges.keys():
            if nto==-1:
                continue
            for edge in states[nto]:
                self.edgePairs[(node,nto,edge)]=0
    
    def getStat(self):
        return len(self.nodes),len(self.edges),len(self.edgePairs)
    
    def update(self,ddfa):
        nodes=set()
        for mfrom,byte,mto in ddfa.getEdges():
            nodes.add(mfrom)
            nodes.add(mto)   
            try:             
                self.edges[(mfrom,mto)]+=1
            except KeyError as e:
                print("from: ",mfrom,"to:",mto,"byte:",byte)
                
        
        for node in nodes:
            self.nodes[node]+=1
                
        edges=ddfa.getEdges()
        size_edges=len(edges)
        if size_edges>1:
            t=size_edges-1
            while t>0:
                mfrom2,byte2,mto2=edges[t]
                mfrom1,byte1,mto1=edges[t-1]
                if mto1==mfrom2:
                    try:
                        self.edgePairs[(mfrom1,mto1,mto2)]+=1
                    except KeyError as e:
                        print("from: ",mfrom,"via: ",mto1," to:",mto2,"byte:",byte)
                t-=1               
    
    def calculate(self):
        total_node=len(self.nodes)
        total_edges=len(self.edges)
        total_edgePairs=len(self.edgePairs)
        
        count_node=0
        for node,times in self.nodes.items():
            if times>0:
                count_node+=1
        
        count_edge=0
        for edge,times in self.edges.items():
            if times>0:
                count_edge+=1
        
        count_edgePair=0
        for edgePair,times in self.edgePairs.items():
            if times>0:
                count_edgePair+=1
        
        return [count_node,total_node,count_edge,total_edges,count_edgePair,total_edgePairs]