import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer, util
from collections import defaultdict

model = SentenceTransformer('all-MiniLM-L6-v2')

def remove_duplicates(results):
    unique_results = []
    seen_urls = set()  

    for result in results['results']:
        if result['link'] not in seen_urls:
            unique_results.append(result)
            seen_urls.add(result['link'])

    return unique_results

def compute_relevance(query, result):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([query, result['title'] + " " + result['snippet']])
    tfidf_score = (tfidf_matrix[0] * tfidf_matrix[1].T).toarray()[0][0]

    query_embedding = model.encode(query)
    result_embedding = model.encode(result['title'] + " " + result['snippet'])
    semantic_score = util.cos_sim(query_embedding, result_embedding).item()

    return 0.5 * tfidf_score + 0.5 * semantic_score

def compute_authority(result):
    source_weight = {
        "google": 1.2,
        # "Bing": 1.1,
        "duckduckgo": 1.1
    }
    position_score = max(1, 10 - result['index']) / 10
    return source_weight.get(result['index'], 1) * position_score


def rerank_results(query, results):
    results = remove_duplicates(results)
    ranked_results = []

    for result in results:
        relevance = compute_relevance(query, result)
        authority = compute_authority(result)

        final_score = 0.7 * relevance + 0.3 * authority
        result['score'] = final_score
        ranked_results.append(result)

    ranked_results.sort(key=lambda x: x['score'], reverse=True)
    return ranked_results


def return_results(query, results):
    ranked_results = rerank_results(query, results)

    output_data = {
        "query": query,
        "results": [
            {
                "link": result['link'],
                "title": result['title'],
                "snippet": result['snippet']
            }
            for result in ranked_results[:10]
        ]
    }

    return output_data

    
