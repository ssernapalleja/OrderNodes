import graphviz
from graphviz import Digraph

g = Digraph('G', engine="neato", filename='test.gv',format='pdf')
g.attr(size='7')
g.node('10',pos='-1,0!')
g.node('11',pos='1,1!')
g.node('12',pos='1,2!')
g.node('00',pos='0,0!')
g.node('01',pos='0,1!')
g.node('02',pos='0,2!')
g.node('20',pos='2,0!')
g.node('21',pos='2,1!')
g.node('22',pos='15,1!', color="green",shape="box",width="2")
g.node('23',pos='15,2!', color="red",shape="box",width="10")
g.edge('10','20')
g.edge('10','30')
g.render()
g.view()