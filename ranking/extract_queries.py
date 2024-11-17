import http.client
import json
import urllib.parse
from serpapi import GoogleSearch
import server.ranking_final as rf

# Google Search API headers
headers_google = {
    'x-rapidapi-key': "24ee15174cmsh4bb6311b46d43abp1ff5afjsn9025854e548e",
    'x-rapidapi-host': "google-search72.p.rapidapi.com"
}

# Predefined queries
PREDEFINED_QUERIES = [
    "top travel destinations", "popular books to read", "best restaurants",
    "latest technology news", "most beautiful beaches", "healthy dinner recipes",
    "top consumer electronics", "world news headlines", "tips for job interviews",
    "best online courses", "most popular movies", "luxury hotels",
    "trendy fashion accessories", "emerging technologies", "famous landmarks around the world",
    "tips for saving money", "new smartphone releases", "popular music artists",
    "best exercise equipment for home", "most energy efficient appliances",
    "top tourist attractions", "best-selling books", "global business news",
    "luxury vacation destinations", "highly rated electronics", "tips for home improvement",
    "popular video games", "world's best restaurants", "emerging fashion trends",
    "highly anticipated movies"
]

def fetch_and_save_results(output_file):
    results_data = []

    for query in PREDEFINED_QUERIES:
        print(f"Fetching results for query: {query}")
        encoded_query = urllib.parse.quote(query)

        # Google Search
        conn = http.client.HTTPSConnection("google-search72.p.rapidapi.com")
        conn.request("GET", f"/search?q={encoded_query}&lr=en-IN&num=10", headers=headers_google)
        res_google = conn.getresponse()
        raw_data_google = res_google.read()

        # DuckDuckGo Search
        ddg_params = {
            "api_key": "a28c998ec76fe2f7cf91c3076047ef22f7eee67f4133bde18f52b79b88febdbc",
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
            "api_key": "a28c998ec76fe2f7cf91c3076047ef22f7eee67f4133bde18f52b79b88febdbc"
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
                        google_results_filtered.append({"link": link, "snippet": snippet, "title": title, "source":"bing","index":index})


        # Combine results into a single response
        combined_results = {
            "results":google_results_filtered
        }

        output_results = rf.return_results(query, combined_results)

        # Format results in the desired structure
        formatted_results = {
            "query": query,
            "results": [
                {
                    "link": item["link"],
                    "title": item["title"],
                    "snippet": item["snippet"]
                }
                for item in google_results_filtered[:10]
            ]
        }

        # Append to results data
        results_data.append(formatted_results)

    # Save all results to a JSON file
    with open(output_file, "w") as file:
        json.dump(results_data, file, indent=2)

# Example usage
if __name__ == "__main__":
    fetch_and_save_results("query_results.json")
