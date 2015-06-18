#coding=UTF-8
__author__ = 'Administrator'
from graph import VideoGraph
from pprint import pprint
if __name__=='__main__':
    vg = VideoGraph()
    vg.load('tiny.txt')
    query_connection = vg.get_query_connection(u'美女',u'性感')
    for item in query_connection:
        print item[0].encode('utf-8')
    video_connection = vg.get_video_connection(u'美女',u'性感')
    for item in video_connection:
        print item[0].encode('utf-8')