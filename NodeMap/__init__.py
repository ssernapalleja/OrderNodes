#NodeMap 
#contains all the nodes of a single item
#also it schedule date 



from Node.__init__ import Node
class NodeMap:
    def __init__(self, name, importance, endDate, nodes):
        self.name=name
        self.importance = importance
        self.endDate=endDate
        self.nodes = nodes
        for k,n in nodes.items():
            n.mapper = self
    