
"""
官方文档：https://www.elastic.co/guide/cn/elasticsearch/guide/current/aggregations.html
官方文档：https://elasticsearch-dsl.readthedocs.io/en/latest/search_dsl.html
参考：https://blog.csdn.net/hanyuyang19940104/article/details/81668880中的bug解决方案

可参考：https://blog.csdn.net/junfeng666/article/details/78251788
可参考： https://linux.ctolib.com/elasticsearch-dsl-py.html
"""
# metric的方法有sum、avg、max、min, value_count等等
import time
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q, A
from elasticsearch.helpers import bulk
import requests
import json

es = Elasticsearch( ['localhost'], port=9200 )
dict_1 = {"name": "test", "ac": "bob", "address": {"city": "shanghai"}}
dict_2 = [
    {"name": 'bob', "age" : 100, "ac": "sssssss"},
    {"name": 'marry', "age": 110, "ac": "i am marry"},
    {"name": 'lili', "age": 155, "ac": "helloworld"},
]


def get_data_by_id() :
    return es.get(index="bank", doc_type="account", id='qwe')


def query_data() :
    res = es.search(index="bank", doc_type="account")
    return res


def index_data() :
    return es.index( index="bank", doc_type="account", body=dict_1 )


def bulk_data(data=None):
    if not data:
        data = dict_2
    actions = []
    # '_op_type':'index',#操作 index update create delete
    for i in data :
        action = {
            '_op_type' : 'index',  # 操作 index update create delete
            # '_index': "bank",
            '_index' : "cars",
            "_type" : "transactions",
            # "_type": "account",
            "_source" : i

        }
        actions.append( action )
    success, _ = bulk( es, actions=actions, raise_on_error=True )
    return success


def Q_func() :
    # 官方文档：https://elasticsearch-dsl.readthedocs.io/en/latest/search_dsl.html
    # q = Q("multi_match", query="bob", fields=["name", 'ac'])
    s = Search( using=es, index="bank" )
    # Q("match", title='python') & Q("match", title='django')
    s.query = Q( 'bool', must=[Q( 'match', name='bob' ), Q( 'match', ac='bob' )] )  # name=bob且ac=bob
    # s.query = Q('bool', must=[Q('match', name='bob')])
    res_3 = s.query().execute()
    print( res_3 )
    print( len( res_3 ) )
    # <Response: [<Hit(bank/account/a_AJWGYB6B4UEZt2YIRu): {'name': 'marry', 'age': 10, 'ac': 'i am marry'}>


def q_search() :
    # .source(["address"])可以指定返回字段
    s = Search( using=es, index="bank" )
    # s = s.filter('term', category__keyword='Python')
    s = s.query( 'match', address__city='shanghai' )  # 查二级数据
    # data为dict_1 = {"name": "test", "ac": "bob", "address": {"city":"shanghai"}}
    res = s.execute()
    print( res )


# 聚合：

def A_func() :
    s = Search( using=es, index="bank" )
    # a = A('terms', field='name')
    # s.aggs.bucket("term_name", "terms", field='name')
    # res =a.metric('clicks_per_category', 'sum', field='clicks') \
    #     .bucket('tags_per_category', 'terms', field='tags')

    s.aggs.bucket( 'sum_age', 'match', field='name' ) \
        .metric( "max_age", "sum", script="doc['downFlux'].value+doc['upFlux'].value" )
    # .metric("max_age", "sum", field='age')
    # s.aggs.bucket('sum_age', 'terms', field='name')  # 参数为group_name, 方法, 栏
    # s.aggs.metric('max_age', 'max', field='age')

    # s.aggs.bucket('per_name', 'terms', field='name') \
    #     .metric('max_age', 'max', field='age')

    res = s.execute()
    for i in res :
        print( i )
    print( len( res ) )
    # a = {'terms': {'field': 'name'}}
    # {
    #   'terms': {'field': 'category'},
    #   'aggs': {
    #     'clicks_per_category': {'sum': {'field': 'clicks'}},
    #     'tags_per_category': {'terms': {'field': 'tags'}}
    #   }
    # }


# index_data()
# q_search()
# A_func()
# print(bulk_data())

def curl_es() :
    data = [
        {"price" : 10000, "color" : "red", "make" : "honda", "sold" : "2014-10-28"},
        {"price" : 20000, "color" : "red", "make" : "honda", "sold" : "2014-11-05"},
        {"price" : 30000, "color" : "green", "make" : "ford", "sold" : "2014-05-18"},
        {"price" : 15000, "color" : "blue", "make" : "toyota", "sold" : "2014-07-02"},
        {"price" : 12000, "color" : "green", "make" : "toyota", "sold" : "2014-08-19"},
        {"price" : 20000, "color" : "red", "make" : "honda", "sold" : "2014-11-05"},
        {"price" : 80000, "color" : "red", "make" : "bmw", "sold" : "2014-01-01"},
        {"price" : 25000, "color" : "blue", "make" : "ford", "sold" : "2014-02-12"},
    ]
    body = {
        "size" : 0,
        "aggs" : {
            "popular_colors" : {
                "terms" : {
                    "field" : "color.keyword"
                }
            }
        }
    }
    res = es.search( index="cars", doc_type="transactions", body=body )
    print( res )
    # for key, i in res:
    #     print(key, i)


def agg_es() :
    #
    # s = Search(using=es, index="cars", doc_type='transactions').extra(size=0)  ### 注意这里size=0可加快查询速度
    s = Search( using=es, index="cars", doc_type='transactions' )
    # metric的方法有sum、avg、max、min, value_count等等
    # bucket的size参数只返回1个bucket桶
    # 加上size=1000返回的数据不会只有10条
    s.aggs.bucket( 'test', 'terms', field='color.keyword', size=1000 ).metric( "sum_test", 'count',
                                                                               field='make.keyword' )
    # metric("max_age", "sum", script="doc['downFlux'].value+doc['upFlux'].value")
    print( s.to_dict(), '\n' )
    res = s.execute()
    print( res )
    print( res.aggregations )
    print( res.to_dict() )
    '''
    {'_index': 'cars', '_type': 'transactions', '_id': 'fPDTW2YB6B4UEZt2CYQ_', '_score': 1.0,
          '_source': {'price': 20000, 'color': 'red', 'make': 'honda', 'sold': '2014-11-05'}}]}, 'aggregations': {
        'test': {'doc_count_error_upper_bound': 0, 'sum_other_doc_count': 0,
                 'buckets': [{'key': 'red', 'doc_count': 4, 'sum_test': {'value': 130000.0}},
                             {'key': 'blue', 'doc_count': 2, 'sum_test': {'value': 40000.0}},
                             {'key': 'green', 'doc_count': 2, 'sum_test': {'value': 42000.0}}]}}}
    '''


if __name__ == "__main__" :
    agg_es()

# doc_count:查询出的记录条数,与聚合后的buckets的list 长度不同
