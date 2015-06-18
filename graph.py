#coding=UTF-8
__author__ = 'Administrator'
from collections import defaultdict
import codecs
import operator
class VideoGraph:
    def __init__(self):
        self.qv = defaultdict(dict)
        self.qq = defaultdict(dict)
        self.vv = defaultdict(dict)
        pass

    def load(self,filepath):
        file = codecs.open(filepath,mode='r',encoding='utf-8')
        while True:
            line = file.readline()
            if not line:
                break
            fields = line.split('\t')
            if len(fields)!=3:
                continue
            print fields[0]
            key = fields[1]
            rel_dict = self.parse_dict(fields[2])
            print 'result dict len: %d'%len(rel_dict)
            if fields[0]==u'QQ':
                self.qq[key] = rel_dict
            elif fields[0]==u'QV':
                self.qv[key] = rel_dict
            elif fields[0]==u'VV':
                self.vv[key] = rel_dict
        file.close()
        print 'graph file %s is loaded' %filepath
        print 'VV: %d QQ: %d, QV: %d' %(len(self.vv),len(self.qq),len(self.qv))

    def parse_dict(self,line):
        res_dict = dict()
        results = line.split('|')
        for item in results:
            info = item.split(',')
            if len(info)!=2:
                continue
            res_dict[info[0]] = float(info[1])
        return res_dict

    def get_video_connection(self, key1, key2):
        connection = self.intersect(self.qv[key1],self.qv[key2])
        res_list = sorted(connection.items(), key=operator.itemgetter(1), reverse=True)
        return res_list[:100]

    def get_query_connection(self, key1, key2):
        print 'Left Len: %d Right Len: %d'%(len(self.qq[key1]),len(self.qq[key2]))
        connection = self.intersect(self.qq[key1],self.qq[key2])
        res_list = sorted(connection.items(), key=operator.itemgetter(1), reverse=True)
        return res_list[:100]

    def intersect(self,leftdict, rightdict):
        result = dict()
        for key in leftdict:
            if key in rightdict:
                result[key] = leftdict[key]*rightdict[key] #(leftdict[key],rightdict[key], leftdict[key]*rightdict[key])
        return result
