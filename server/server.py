from flask import Flask, request, jsonify
import http.client
import json
import urllib.parse
from serpapi import GoogleSearch

app = Flask(__name__)

# Google Search API headers
headers_google = {
    'x-rapidapi-key': "0370908d5bmsh9d424bf29cdd7e9p1f8768jsnd1271994c07b",
    'x-rapidapi-host': "google-search72.p.rapidapi.com"
}
# global index
# index = 0

@app.route('/submit', methods=['POST'])
def submit():
    # global index
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({"error": "JSON body with 'query' field is required"}), 400

    query = data['query']
    encoded_query = urllib.parse.quote(query)

    # Google Search
    conn = http.client.HTTPSConnection("google-search72.p.rapidapi.com")
    conn.request("GET", f"/search?q={encoded_query}&lr=en-IN&num=10", headers=headers_google)
    res_google = conn.getresponse()
    raw_data_google = res_google.read()

    # DuckDuckGo Search
    params = {
        "api_key": "09ea60bb38a064c32931c85dec18237f9e6188a3c5fd7c13ca4955b6f869d75b",
        "engine": "duckduckgo",
        "q": query,
        "kl": "in-en"
    }
    search = GoogleSearch(params)
    results_duckduckgo = search.get_dict()

    # Decode and parse the Google search results
    try:
        results_google = json.loads(raw_data_google.decode("utf-8"))
    except json.JSONDecodeError:
        return jsonify({"error": "Failed to decode Google JSON response"}), 500

    # Filter Google results to get only link and snippet
    google_results_filtered = [
        {"link": item["link"], "snippet": item["snippet"], "title": item["htmlTitle"], "source":"google","index":index}
        for index,item in enumerate(results_google.get("items", []))
    ]


    # DuckDuckGo filter
    ddg_results_filtered = []
    if 'organic_results' in results_duckduckgo:
        for index,item in enumerate(results_duckduckgo['organic_results']):
            if isinstance(item, dict):
                link = item.get('link')
                snippet = item.get('snippet')
                title = item.get('title')
                if link and snippet:  # Check if both link and snippet are present
                    google_results_filtered.append({"link": link, "snippet": snippet, "title": title, "source":"duckduckgo","index":index})

    # Combine results into a single response
    combined_results = {
        "results":google_results_filtered
    }

    return jsonify(combined_results)

if __name__ == '__main__':
    app.run(debug=True)