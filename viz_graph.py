#coding=UTF-8
import json
__author__ = 'Administrator'
class VizGraph:
    def __init__(self):
        self.nodes = []
        self.edges = []

class VizNode:
    def __init__(self):
        self.query=u''
        self.pos_x=0
        self.pos_y=0
        self.weight=0

class VizEdge:
    def __init__(self):
        self.src_idx=0
        self.dst_idx=0
        self.weight=0

if __name__=='__main__':
    graph = VizGraph()
    node = VizNode()
    node.pos_x = 0.0
    node.pos_y = 0.0
    node.query='query0'
    node.weight = 0
    graph.nodes.append(node)

    node1 = VizNode()
    node1.pos_x = 0.1
    node1.pos_y = 0.1
    node1.query='query1'
    node1.weight = 0.1
    graph.nodes.append(node1)

    edge = VizEdge()
    edge.weight = 0
    edge.src_idx=0
    edge.dst_idx=1
    graph.edges.append(edge)
    str = json.dumps(graph,default=lambda o:o.__dict__,encoding='utf-8',ensure_ascii=False)
    #str = json.dumps(dict(graph),encoding='utf-8',ensure_ascii=False)
    print str