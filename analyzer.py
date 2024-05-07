import os
from typing import List, Dict
from collections import Counter, defaultdict
import json
import requests
from bertopic import BERTopic
from pydantic import ValidationError

from data import Corporate
from gemini_api_reponse import GeminiResponse

try:
    from dotenv import load_dotenv

    load_dotenv()
except ModuleNotFoundError:
    print("Warning: 'python-dotenv' package is not installed. "
          "Environment variables won't be loaded from a .env file.")


def read_all_corporates() -> List[Corporate]:
    import json

    all_companies_json_path = "/home/gsoykan/Desktop/dev/entrapeer-agent/all_companies.json"
    with open(all_companies_json_path, 'r') as file:
        json_data = json.load(file)

    corporates = [Corporate(**item) for item in json_data]
    return corporates


def _get_top_k_themes(corporate: Corporate, k: int = 3) -> List[str]:
    all_themes = [item.strip() for partner in corporate.startup_partners for item in partner.theme_gd.split(',')]
    counter = Counter(all_themes)
    return list(map(lambda x: x[0], counter.most_common(k)))


def _corporate_to_str(corporate: Corporate) -> str:
    themes = _get_top_k_themes(corporate, 3)
    str_representation = f"""{corporate.name}: {corporate.description}, {', '.join(themes)}"""
    return str_representation


def _generate_cluster_summary_from_gemini(cluster_info: Dict) -> Dict | str:
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={gemini_api_key}"
    documents_formatted = "\n".join(cluster_info["docs"][:5])
    prompt = f"""\
Generate a concise  and sensible title and a brief description that captures the essence and main themes of the cluster. 
Output the title and description in JSON format.

---

Cluster Name: {cluster_info['name']}
Cluster Representation: {cluster_info['representation']}
Sample Documents in Cluster:
{documents_formatted}

---

Please generate a title and a description for the above cluster in JSON format.
"""
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url,
                             json=data,
                             headers=headers)

    if response.status_code == 200:
        try:
            api_response = GeminiResponse(**response.json())
            raw_result = api_response.candidates[0].content.parts[0].text
            try:
                parsed_result = json.loads(raw_result
                                           .replace('```json', '')
                                           .replace('```JSON', '')
                                           .replace('`', '')
                                           .strip())
                return parsed_result
            except Exception as e:
                print("Error decoding JSON:", str(e))
                return raw_result
        except ValidationError as e:
            print("Validation error:", e.json())
            raise e
    else:
        print("Failed to fetch data:", response.status_code)
        raise Exception("Failed to fetch data")


def analyse_corporates(corporates: List[Corporate]) -> List[Dict]:
    """
    - You can group companies and cluster them based on their closeness.
    - Calculation of the closeness metric is up to you.
    - You can utilize the vector embeddings or other nlp methods to group companies.
    - Then you can give the clusters to an LLM
        so that it writes a description and assigns a title for each cluster. (You can use free llms that can be used via api: Google Gemini is free up to 60 rpm) See: https://ai.google.dev/
    """
    topic_model = BERTopic()
    docs = list(map(_corporate_to_str, corporates))
    topics, probs = topic_model.fit_transform(docs)
    topic_info = topic_model.get_topic_info()
    document_info = topic_model.get_document_info(docs)

    clusters = {}
    for info in topic_info.itertuples(index=False):
        # ,Topic,Count,Name,Representation
        # TODO: @gsoykan - you can also store probabilities of docs
        #  then you can get top-k probable doc to use in the prompt
        clusters[info.Topic] = {
            'name': info.Name,
            'representation': info.Representation,
            'docs': []
        }

    for doc_info in document_info.itertuples(index=False):
        clusters[doc_info.Topic]['docs'].append(doc_info.Document)

    cluster_summaries = []
    for k, cluster_detail in clusters.items():
        summary = _generate_cluster_summary_from_gemini(cluster_detail)
        cluster_summaries.append(summary)

    return cluster_summaries


if __name__ == '__main__':
    all_corporates = read_all_corporates()
    result = analyse_corporates(all_corporates)
