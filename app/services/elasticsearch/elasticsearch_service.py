import json
import requests
from config import get_config

class FilterElasticsearch:
    index: str = None
    type: str = None
    filter: object = {}
    is_search_all: bool = True
    
URL_ELASTICSEARCH = get_config("URL_ELASTICSEARCH")
HEADER = {
    'Content-Type': 'application/json'
}

# region API liệt kê, hiển thị các Index trong Elasticsearch
def get_indexs():
    url = URL_ELASTICSEARCH + '_cat/indices'
    payload={}

    response = requests.request("GET", url, headers=HEADER, data=payload)
    return response.text
# endregion

# region API tạo Index trong Elasticsearch
def create_index(name):
    url = URL_ELASTICSEARCH + name

    # Cài đặt các field, số replica set, số shard khi tạo Index
    # Mặc định number_of_shard = 5 và number_of_replicas = 1
    payload = json.dumps({
        "settings": {
            "index": {
            "number_of_shards": 3,
            "number_of_replicas": 2
            }
        }
    })

    response = requests.request("PUT", url, headers=HEADER, data=payload, verify=False, timeout=5)

    return response.json()
# endregion

# region API Insert, thêm dữ liệu vào Elasticsearch
def create_document(index: str, type: str, id: int, data: object = None):
    url = URL_ELASTICSEARCH + index+ '/' + type + '/' + 'id'

    payload = json.dumps({
        "name": "Int Map"
    })
    response = requests.request("POST", url, headers=HEADER, data=payload)

    return response.json()
# endregion

# region API get document Elasticsearch.
def get_document(index: str, type: str, id: int, data: object = None):
    url = URL_ELASTICSEARCH + index+ '/' + type + '/' + 'id'

    payload = {}

    response = requests.request("GET", url, headers=HEADER, data=payload)

    return response.json()
# endregion

# region API đọc dữ liệu – Tìm kiếm dữ liệu, document Elasticsearch
def search_documents(filter: FilterElasticsearch):
    url = URL_ELASTICSEARCH + 'test_log66/systen-log/_search'

    payload = json.dumps({
        "query": {
            "multi_match" : {
                "query" : filter.data.keyword,
                "fields" : ["_all"]
            }
        }
    })

    response = requests.request("GET", url, headers=HEADER, data=payload)

    return response.json()
# endregion

