class Node:
    def __init__(self, name, time, maxWorkers, work, fastStartDate,type_):
        self.time=time #time spent in hours
        self.name=name #identification
        self.maxWorkers=maxWorkers
        self.work=work #what they are going to do here
        self.next={}
        self.prev={}
        self.fastStartDate = fastStartDate
        self.type=type_ #if you have something that could by worked differently
        
    def setNext(self,_next):
        self.next[_next.name]=_next
        _next.prev[self.name]=self
        
    def setPrev(self,prev):
        prev.next[self.name]=self
        self.prev[prev.name]=prev
    
    

    