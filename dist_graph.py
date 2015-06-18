#coding=UTF-8
import codecs
from viz_graph import VizGraph
from viz_graph import VizEdge
from viz_graph import VizNode
import json
import operator
log = codecs.open('log.txt',mode='w',encoding='utf-8')
__author__ = 'Administrator'
class DistEdge:
    def __init__(self):
        self.dst_idx = 0
        self.weight = 0.0
        self.pos_x = 0
        self.pos_y = 0

    def parse(self,str):
        fields = str.split(':')
        if len(fields)!=3:
            return False
        self.dst_idx = int(fields[0])
        self.weight = float(fields[1])
        pos_str = fields[2].strip('()')
        pos_xy = pos_str.split(',')
        self.pos_x = float(pos_xy[0])
        self.pos_y = float(pos_xy[1])
        return True

class DistGraph:
    def __init__(self):
        self.query_table = [] #map id to query string
        self.query_dict = dict() #map query string to query id
        self.edges = []
        pass

    def load_graph(self,path):
        file = open(path)
        edge_list = dict()
        node_idx = 0

        while True:
            line = file.readline()
            if not line:
                break
            line = line.strip('\n\r')
            fields = line.split('\t')
            if len(fields)!=2:
                continue
            head = fields[0].split(':')
            node_idx = int(head[0])
            if node_idx!=len(self.edges):
                print 'ERR: unmatched node index. Exit.'
                break

            edges = fields[1].split('|')
            for edge in edges:
                e = DistEdge()
                if e.parse(edge):
                    #edge_list.append(e)
                    edge_list[e.dst_idx] = e
            self.edges.append(edge_list)
        file.close()

    def load_query(self,file):
        idx = 0
        query_file = codecs.open(file,'r','utf-8')
        while True:
            query = query_file.readline()
            if not query:
                break
            query = query.strip('\n\r')
            self.query_table.append(query)
            self.query_dict[query] = idx
            idx+=1
        query_file.close()

    def to_vizgraph(self,node_idx):
        viz_graph = VizGraph()
        id_map = dict() #map global
        id_table = []
        id_map[node_idx] = len(id_table)
        id_table.append(node_idx)
        edge_list = self.edges[node_idx]

        viz_node = VizNode()
        viz_node.weight = 1.0
        viz_node.pos_x = 0
        viz_node.pos_y = 0
        viz_node.query = self.query_table[node_idx]
        viz_graph.nodes.append(viz_node)
        for edge in edge_list:
            dst =edge_list[edge]
            if dst.dst_idx not in id_map:
                id_map[dst.dst_idx] = len(id_table)
                id_table.append(dst.dst_idx)
                viz_node_e = VizNode()
                viz_node_e.query = self.query_table[dst.dst_idx]
                #print viz_node_e.query.encode('utf-8')
                #log.writelines(viz_node_e.query.encode('utf-8'))
                #log.writelines(viz_node_e.query)
                log.write(viz_node_e.query+'\n')
                viz_node_e.pos_x = dst.pos_x
                viz_node_e.pos_y = dst.pos_y
                viz_node_e.weight = dst.weight
                viz_graph.nodes.append(viz_node_e)

        #sort id list based on global id
        id_table.sort()
        for i in xrange(len(id_table)):
            for j in range(i+1,len(id_table)):
                src_id = id_table[i]
                dst_id = id_table[j]
                if src_id==dst_id:
                    break
                if src_id < len(self.edges) and dst_id in self.edges[src_id] and self.edges[src_id][dst_id].weight<0.05:
                    viz_edge = VizEdge()
                    viz_edge.src_idx = id_map[src_id]
                    viz_edge.dst_idx = id_map[dst_id]
                    viz_edge.weight = self.edges[src_id][dst_id].weight
                    viz_graph.edges.append(viz_edge)
        return viz_graph

    def serialize(self,query):
        if query not in self.query_dict:
            return ''
        qid = self.query_dict[query]
        viz_graph = self.to_vizgraph(qid)
        str = json.dumps(viz_graph,default=lambda o:o.__dict__)
        return str

if __name__=='__main__':
    dist_graph = DistGraph()
    dist_graph.load_graph('position_graph.test.txt')
    dist_graph.load_query('queryfile.txt')
    str = dist_graph.serialize('09')
    log.flush()
    log.close()
    #str = str.encode()
    print str.encode('utf-8')
    '''
    str = dist_graph.serialize('09dota')
    print str
    str = dist_graph.serialize(u'09')
    print str
    str = dist_graph.serialize('09dota')
    print str
    '''



