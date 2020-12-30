import time
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q, A
from elasticsearch.helpers import bulk
import requests
import json

es = Elasticsearch(["10.0.169.115:9200"], http_auth=('elastic', 'Powercdn123'))
D = time.strftime('%Y.%m.%d')
cdnindex = "logstash-cdnerrorlog-"+D


def agg_es():
    s = Search(using=es, index=cdnindex)
    s.aggs.bucket('test', 'terms', field='dm.keyword', size=0).metric("st", 'terms', field='st.keyword')
    # metric("max_age", "sum", script="doc['downFlux'].value+doc['upFlux'].value")
    print( s.to_dict(), '\n' )
    res = s.execute()
    print( res )
    print( res.aggregations )
    print( res.to_dict() )
