#!/usr/local/python2.7/bin/python
# -*- coding: utf-8 -*-
# Author: caoyun@powercdn.com
import requests
import json
import sys
import os
import time
from elasticsearch import Elasticsearch

headers = {'Content-Type' : 'application/json;charset=utf-8'}
# api_url = "https://oapi.dingtalk.com/robot/send?access_token=7f74d57d8f02f5e6b6735044d3a29ba9af07c0fbdb9bba2c8a40a8c6d6d18bba"
api_url = "https://oapi.dingtalk.com/robot/send?access_token=fc5fc2d3fd6fc283d30a0e92c683fa4cca4a35127b8fe9f00784bf11e6bdfd4d"
es = Elasticsearch( ["10.0.169.115:9200"], http_auth=('elastic', 'Powercdn123') )
D = time.strftime( '%Y.%m.%d' )
D1 = time.strftime( '%Y.%m.%d %H:%M:%S' )

body = {
    "size" : 0,
    "aggs" : {
        "dm" : {
            "terms" : {
                "script": "if(doc['dm.keyword'].size() > 0 && doc['sa.keyword'].size() >0 && doc['st.keyword'].size() >0) {return doc['dm.keyword'].value + '-'+ doc['sa.keyword'].value + '-' + doc['st.keyword'].value ;} else return 0;"

            }
        }
    },
    "query" : {
        "range" : {
            "@timestamp" : {
                "gt" : "now-2m",
                "lt" : "now"
            }
        }
    }
}


def msg(text) :
    json_text = {
        "msgtype" : "text",
        "at" : {
            "atMobiles" : [
                "13466473540"
            ],
            "isAtAll" : False
        },
        "text" : {
            "content" : text
        }
    }
    print
    requests.post( api_url, json.dumps( json_text ), headers=headers ).content


# def info(D,dm,host,code,count):
#    info1="""{}
#               Domain: {}
#               Httpcode:{}
#               Count:{} """.format(D,dm,host,code,dm_json["doc_count"])
#    print(info1)
if __name__ == '__main__' :
    response = es.search(
        index="logstash-cdnerrorlog-" + D,
        filter_path="aggregations.dm.buckets",
        body=body )
    # print(response)
    json_data = response['aggregations']['dm']['buckets']
    dm_count = len( json_data )
    for i in range( 0, dm_count - 1 ) :
        dm_json = json_data[i]
        dm_sa_st = dm_json["key"]
        dm_sa_st_list = dm_sa_st.split( "-" )
        if len( dm_sa_st_list ) > 2 :
            dm = "-".join( dm_sa_st_list[0 :-2] )
            host = dm_sa_st_list[-2]
            code = dm_sa_st_list[-1]
            if int( code ) >= 500 and int( dm_json["doc_count"] ) > 50 :
                info = """ CDN 错误代码统计
{}
Domain: {}
Host: {}
Httpcode: {}
Count: {} """.format( D1, dm, host, code, dm_json["doc_count"] )
                msg( "powercdnES:" + info )
                # print(dm,host,code,dm_json["doc_count"])
