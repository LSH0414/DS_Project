import requests
import json

# headers = {'Content-Type': 'application/json; chearset=utf-8'}

# ## 예시 http://tools.kinds.or.kr:8888/topn_keyword
# url = 'http://tools.kinds.or.kr:8888/word_cloud'
# data = {
# 	'access_key': '3a593bd3-85e5-428e-b942-d7f5cd91b5ca',
# 	'argument': {
#     'published_at': {
#         'from': '2022-01-01',
#         'until': '2022-01-03'
#     },
#     'provider': [
#         '경향신문'
#     ],
#     'category': [
#         'IT_과학'
#     ]
# 	}
# }
# res = requests.post(url, data=json.dumps(data), headers=headers)
# print(str(res.status_code) + " | " + res.text)


# headers = {'Content-Type': 'application/json; chearset=utf-8'}

# ## 예시 http://tools.kinds.or.kr:8888/topn_keyword
# url = 'https://www.newstore.or.kr/api/search.json'
# data = {
# 	'apiKey': '3a593bd3-85e5-428e-b942-d7f5cd91b5ca',
# 	'argument': {
#     'from': '2022-01-01',
#     'until': '2022-01-03',
#     'provider': '경향신문',
#     'category': 'IT_과학'
# 	}
# }
# res = requests.post(url, data=json.dumps(data), headers=headers)
# print(str(res.status_code) + " | " + res.text)


# headers = {'Content-Type': 'application/json; chearset=utf-8'}

# ## 예시 http://tools.kinds.or.kr:8888/topn_keyword
# url = 'http://tools.kinds.or.kr:8888/topn_keyword'
# data = {
# 	'access_key': '3a593bd3-85e5-428e-b942-d7f5cd91b5ca',
# 	'argument': {
#         'date_hour': '2019080100'
# 	}
# }
# res = requests.post(url, data=json.dumps(data), headers=headers)
# print(str(res.status_code) + " | " + res.text)


headers = {'Content-Type': 'application/json; chearset=utf-8'}

## 예시 http://tools.kinds.or.kr:8888/topn_keyword
url = 'http://tools.kinds.or.kr:8888/search/news'
data = {
	'access_key': '3a593bd3-85e5-428e-b942-d7f5cd91b5ca',
	'argument': {
        'query': '서비스 AND 출시',
        'published_at': {
            'from': '2019-01-01',
            'until': '2019-03-31'
        },
        'provider': [
            '경향신문',
        ],
        'category': [
            '정치>정치일반',
            'IT_과학'
        ],
        'byline': '',
        'provider_subject': [
            '경제', '부동산'
        ],
        'subject_info': [
            ''
        ],
        'subject_info1': [
            ''
        ],
        'subject_info2': [
            ''
        ],
        'sort': {'date': 'desc'},
        'hilight': 200,
        'return_from': 0,
        'return_size': 5,
        'fields': [
            'byline',
            'category',
            'category_incident',
            'provider_new_id'
        ]
	}
}
res = requests.post(url, data=json.dumps(data), headers=headers)
print(str(res.status_code) + " | " + res.text)