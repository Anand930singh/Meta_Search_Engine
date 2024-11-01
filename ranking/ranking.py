import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer, util
from collections import defaultdict

# Load model for embedding-based semantic similarity
model = SentenceTransformer('all-MiniLM-L6-v2')


# 1. Remove Duplicates by URL
def remove_duplicates(results):
    unique_results = []
    seen_urls = set()  # Track unique URLs only


    for result in results['results']:
        # print(result)
        # print(result['link'])
        if result['link'] not in seen_urls:
            unique_results.append(result)
            seen_urls.add(result['link'])

    return unique_results

# 2. Compute Relevance Score (TF-IDF + Semantic Matching)
def compute_relevance(query, result):
    # TF-IDF relevance score
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([query, result['title'] + " " + result['snippet']])
    tfidf_score = (tfidf_matrix[0] * tfidf_matrix[1].T).toarray()[0][0]

    # Semantic similarity score
    query_embedding = model.encode(query)
    result_embedding = model.encode(result['title'] + " " + result['snippet'])
    semantic_score = util.cos_sim(query_embedding, result_embedding).item()

    # Final relevance score (weighted average)
    return 0.5 * tfidf_score + 0.5 * semantic_score


# 3. Compute Authority Score (Source + Position-Based)
def compute_authority(result):
    # Weights for sources to reflect authority
    source_weight = {
        "google": 1.2,
        # "Bing": 1.1,
        "duckduckgo": 1.1
    }
    # Position-based scoring: top positions get higher authority scores
    position_score = max(1, 10 - result['index']) / 10
    return source_weight.get(result['index'], 1) * position_score

# 4. Rerank Results
def rerank_results(query, results):
    # Step 1: Deduplicate by URL
    results = remove_duplicates(results)
    ranked_results = []

    for result in results:
        relevance = compute_relevance(query, result)
        authority = compute_authority(result)

        # Aggregate scores with weights for final ranking score
        final_score = 0.7 * relevance + 0.3 * authority  # Emphasizing relevance more heavily
        result['score'] = final_score
        ranked_results.append(result)

    # Sort by final score in descending order for ranking
    ranked_results.sort(key=lambda x: x['score'], reverse=True)
    return ranked_results


# 5. Run the Algorithm with Example Query and Results
query = "coffee"
with open('test.json', 'r') as file:
    results = json.load(file)

# Get the reranked results
ranked_results = rerank_results(query, results)

# Display top results
for result in ranked_results[:5]:  # Showing top 5
    print(f"Title: {result['title']}, URL: {result['link']}, Score: {result['score']}")