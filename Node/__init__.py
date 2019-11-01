#Nodos
#it contains all the production items and the 
#previous nodes needed to be available for the production


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
        self.isPlaced = False
        
    def setNext(self,_next):
        self.next[_next.name]=_next
        _next.prev[self.name]=self
        
    def setPrev(self,prev):
        prev.next[self.name]=self
        self.prev[prev.name]=prev
    
    #check if all the previous nodes are already placed, and if they're already finished
    def isAvailable(self,startDate):
        available = True
        for nd in self.prev:
            if not nd.isPlaced:
                available = False
                break
            if nd.nod_wp.endDate <= startDate:
                available = False
                break
        return available