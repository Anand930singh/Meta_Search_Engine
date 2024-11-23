import json

# Load the JSON data for results and ground truth
with open('ranking/query_results.json', 'r') as f:
    results_data = json.load(f)

with open('ranking/ground_truth.json', 'r') as f:
    ground_truth_data = json.load(f)


# Helper function to calculate precision and recall
def calculate_precision_recall(retrieved_docs, relevant_docs):
    # print(retrieved_docs)
    # print(relevant_docs)
    retrieved_set = set(retrieved_docs)
    relevant_set = set(relevant_docs)

    # Calculate Precision
    true_positives = len(retrieved_set & relevant_set)
    precision = true_positives / len(retrieved_set) if retrieved_set else 0.0

    # Calculate Recall
    recall = true_positives / len(relevant_set) if relevant_set else 0.0

    return precision, recall


# Helper function to calculate Average Precision (AP)
def calculate_average_precision(retrieved_docs, relevant_docs):
    relevant_set = set(relevant_docs)
    num_relevant = len(relevant_set)
    if num_relevant == 0:
        return 0.0  # Avoid division by zero if there are no relevant documents

    precision_sum = 0.0
    relevant_count = 0

    for i, doc in enumerate(retrieved_docs, start=1):
        if doc in relevant_set:
            relevant_count += 1
            precision_sum += relevant_count / i  # Precision at rank i

    return precision_sum / num_relevant


# Helper function to calculate Mean Average Precision (MAP)
def calculate_map(results_data, ground_truth_data):
    total_ap = 0.0
    num_queries = len(results_data)

    for query_result in results_data:
        query = query_result['query']
        retrieved_docs = [doc['link'] for doc in query_result['results']]

        # Find the relevant documents for this query in ground truth data
        relevant_docs = next((gt['results'] for gt in ground_truth_data if gt['query'] == query), [])

        # Calculate Average Precision for this query
        ap = calculate_average_precision(retrieved_docs, relevant_docs)
        total_ap += ap

    return total_ap / num_queries if num_queries > 0 else 0.0

def calculate_f1(precision, recall):
    if precision + recall == 0:
        return 0.0  # Avoid division by zero
    return 2 * (precision * recall) / (precision + recall)


# Evaluate Precision, Recall, F1, MAP
precision_list = []
recall_list = []
f1_list = []
ap_list = []

for query_result in results_data:
    query = query_result['query']
    retrieved_docs = [doc['link'] for doc in query_result['results']]

    # Find the relevant documents for this query in ground truth data
    relevant_docs = list(result['link'] for ground_truth in ground_truth_data if ground_truth['query'] == query for result in ground_truth['results'])

    # Calculate Precision and Recall for this query
    precision, recall = calculate_precision_recall(retrieved_docs, relevant_docs)
    precision_list.append(precision)
    recall_list.append(recall)

    # Calculate F1 score for this query
    f1 = calculate_f1(precision, recall)
    f1_list.append(f1)

    # Calculate Average Precision for this query
    ap = calculate_average_precision(retrieved_docs, relevant_docs)
    print(f"For query: '{query}'")
    print(f"Precision: {precision:.4f}, Recall: {recall:.4f}, F1: {f1:.4f}, AP: {ap:.4f}")
    ap_list.append(ap)

# Calculate MAP (Mean Average Precision)
map_score = sum(ap_list) / len(ap_list) if ap_list else 0.0

# Calculate Mean Precision, Mean Recall, and Mean F1 Score
mean_precision = sum(precision_list) / len(precision_list) if precision_list else 0.0
mean_recall = sum(recall_list) / len(recall_list) if recall_list else 0.0
mean_f1 = sum(f1_list) / len(f1_list) if f1_list else 0.0

# Print the results
print(f"Mean Precision: {mean_precision:.4f}")
print(f"Mean Recall: {mean_recall:.4f}")
print(f"Mean F1 Score: {mean_f1:.4f}")
print(f"Mean Average Precision (MAP): {map_score:.4f}")
