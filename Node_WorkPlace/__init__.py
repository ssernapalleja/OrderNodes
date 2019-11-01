from Node.__init__ import Node
from NodeMap.__init__ import NodeMap
from graphviz import Digraph
from WorkPlace import possibleWork
from WorkPlace.__init__ import WorkPlace

import random
import math

#contains the date when is going to be produced.


class Node_WorkPlace:
    def __init__(self,_workPlace,_node,_startTime):
        self.endDate = self.startDate + _node.time/_workPlace.efficiency +_workPlace.initialTime
        self.available = _workPlace.isAvailable(_startTime,self.endDate) and _node.isAvailable() and _node.work in _workPlace.work 
        if self.available:
            self.workPlace = _workPlace
            _workPlace.nod_wp.append(self)
            self.startDate = _startTime
            self.node = _node
            self.node.isPlaced = True
            _node.nod_wp = self
        
        