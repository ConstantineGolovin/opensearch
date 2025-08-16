from fastapi import FastAPI
from opensearchpy import OpenSearch
import random

app = FastAPI()


client = OpenSearch(
    hosts=[{'host': 'opensearch', 'port': 9200}],
    use_ssl=False,
    scheme="http"
)

INDEX_NAME = "documents"

mapping = {
    "mappings": {
        "properties": {
            "title": {"type": "text"},
            "content": {"type": "text"},
            "content_type": {"type": "keyword"}
        }
    }
}

if not client.indices.exists(index=INDEX_NAME):
    client.indices.create(index=INDEX_NAME, body=mapping)

types = ['news', 'blog', 'article', 'report']
docs = []
for i in range(5):
    docs.append({
        'title': 'Документ' + str(i),
        'content': f'Любая рандомная информация для документа {i}, ' * 4,
        'content_type': random.choice(types)
    })

for i, d in enumerate(docs):
    client.index(index=INDEX_NAME, id=i+1, body=d)

@app.get("/search")
def search(q: str, content_type: str):
    body = {
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": q,
                        "fields": ["title", "content"]
                    }
                },
                "filter": {
                    "term": {"content_type": content_type}
                }
            }
        }
    }
    res = client.search(index=INDEX_NAME, body=body)
    output = []
    for h in res['hits']['hits']:
        output.append({
            'title': h['_source']['title'],
            'snippet': h['_source']['content'][:50]
        })
    return output