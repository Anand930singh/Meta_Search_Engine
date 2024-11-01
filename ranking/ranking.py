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
query = "school"
with open('test.json', 'r') as file:
    results = json.load(file)

# Get the reranked results
ranked_results = rerank_results(query, results)

# Display top results
for result in ranked_results[:5]:  # Showing top 5
    print(f"Title: {result['title']}, URL: {result['link']}, Score: {result['score']}")