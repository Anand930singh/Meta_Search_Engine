# from flask import Flask, request, jsonify
# import http.client
# import json
# import urllib.parse
# from serpapi import GoogleSearch
# from flask_cors import CORS
# import ranking_final as rf

# app = Flask(__name__)
# CORS(app)

# # Google Search API headers
# headers_google = {
#     'x-rapidapi-key': "0370908d5bmsh9d424bf29cdd7e9p1f8768jsnd1271994c07b",
#     'x-rapidapi-host': "google-search72.p.rapidapi.com"
# }
# # global index
# # index = 0

# @app.route('/submit', methods=['POST'])
# def submit():
#     # global index
    
#     data = request.get_json()
#     if not data or 'query' not in data:
#         return jsonify({"error": "JSON body with 'query' field is required"}), 400

    
#     query = data['query']
   
#     encoded_query = urllib.parse.quote(query)
    
#     # Google Search
#     conn = http.client.HTTPSConnection("google-search72.p.rapidapi.com")
#     conn.request("GET", f"/search?q={encoded_query}&lr=en-IN&num=10", headers=headers_google)
#     res_google = conn.getresponse()
    
#     raw_data_google = res_google.read()
    
#     # DuckDuckGo Search
#     ddg_params = {
#         "api_key": "09ea60bb38a064c32931c85dec18237f9e6188a3c5fd7c13ca4955b6f869d75b",
#         "engine": "duckduckgo",
#         "q": query,
#         "kl": "in-en"
#     }
#     ddg_search = GoogleSearch(ddg_params)
#     results_duckduckgo = ddg_search.get_dict()

#     # Bing Search
#     bing_params = {
#         "engine": "bing",
#         "q": query,
#         "kl": "in-en",
#         "api_key": "09ea60bb38a064c32931c85dec18237f9e6188a3c5fd7c13ca4955b6f869d75b"
#     }
#     bing_search = GoogleSearch(bing_params)
#     results_bing = bing_search.get_dict()

#     # Decode and parse the Google search results
#     try:
#         results_google = json.loads(raw_data_google.decode("utf-8"))
#     except json.JSONDecodeError:
#         return jsonify({"error": "Failed to decode Google JSON response"}), 500

#     # Filter Google results to get only link and snippet
#     google_results_filtered = [
#         {"link": item["link"], "snippet": item["snippet"], "title": item["htmlTitle"], "source":"google","index":index}
#         for index,item in enumerate(results_google.get("items", []))
#     ]


#     # DuckDuckGo filter
#     if 'organic_results' in results_duckduckgo:
#         for index,item in enumerate(results_duckduckgo['organic_results']):
#             if isinstance(item, dict):
#                 link = item.get('link')
#                 snippet = item.get('snippet')
#                 title = item.get('title')
#                 if link and snippet:  # Check if both link and snippet are present
#                     google_results_filtered.append({"link": link, "snippet": snippet, "title": title, "source":"duckduckgo","index":index})


#     # Bing results
#     if 'organic_results' in results_bing:
#         for index,item in enumerate(results_bing['organic_results']):
#             if isinstance(item, dict):
#                 link = item.get('link')
#                 snippet = item.get('snippet')
#                 title = item.get('title')
#                 if link and snippet:  # Check if both link and snippet are present
#                     google_results_filtered.append({"link": link, "snippet": snippet, "title": title, "source":"duckduckgo","index":index})


#     # Combine results into a single response
#     combined_results = {
#         "results":google_results_filtered
#     }

#     output_results = rf.return_results(query, combined_results)
    
#     return jsonify(output_results)

# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask, request, jsonify
import http.client
import json
import urllib.parse
from serpapi import GoogleSearch
from flask_cors import CORS
import ranking_final as rf
import query_preprocessing as qp

app = Flask(__name__)
CORS(app)

# Google Search API headers
headers_google = {
    'x-rapidapi-key': "f8a00b7e06msh61438fbfb5ca279p1466ebjsn99aec5fe206d",
    'x-rapidapi-host': "google-search74.p.rapidapi.com"
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
    preprocessed_query = qp.preprocess_query(query)
    encoded_query = urllib.parse.quote(query)
    
    # Google Search
    conn = http.client.HTTPSConnection("google-search72.p.rapidapi.com")
    conn.request("GET", f"/search?q={encoded_query}&lr=en-IN&num=10", headers=headers_google)
    res_google = conn.getresponse()
    
    raw_data_google = res_google.read()
    
    # DuckDuckGo Search
    ddg_params = {
        "api_key": "b0485e76110947cf20812c947bb677257c0499eb0a04dbbfc27d49f3580c5b62",
        "engine": "duckduckgo",
        "q": query,
        "kl": "in-en"
    }
    ddg_search = GoogleSearch(ddg_params)
    results_duckduckgo = ddg_search.get_dict()

    # Bing Search
    bing_params = {
        "engine": "bing",
        "q": query,
        "kl": "in-en",
        "api_key": "09ea60bb38a064c32931c85dec18237f9e6188a3c5fd7c13ca4955b6f869d75b"
    }
    bing_search = GoogleSearch(bing_params)
    results_bing = bing_search.get_dict()

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
    if 'organic_results' in results_duckduckgo:
        for index,item in enumerate(results_duckduckgo['organic_results']):
            if isinstance(item, dict):
                link = item.get('link')
                snippet = item.get('snippet')
                title = item.get('title')
                if link and snippet:  # Check if both link and snippet are present
                    google_results_filtered.append({"link": link, "snippet": snippet, "title": title, "source":"duckduckgo","index":index})


    # Bing results
    if 'organic_results' in results_bing:
        for index,item in enumerate(results_bing['organic_results']):
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

    output_results = rf.return_results(query, combined_results)
    
    return jsonify(output_results)

if __name__ == '__main__':
    app.run(debug=True)