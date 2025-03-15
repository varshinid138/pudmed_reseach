import requests
from typing import List, Dict

PUBMED_API_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_SUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
PUBMED_DETAILS_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

API_KEY = "50dda823d4fff6db481f5128fb14535eaa09" # Replace with actual API key

def fetch_pubmed_papers(query: str, max_results: int = 10) -> List[str]:
    """Fetches paper IDs from PubMed."""
    params = {"db": "pubmed", "term": query, "retmax": max_results, "retmode": "json", "api_key": API_KEY}
    response = requests.get(PUBMED_API_BASE, params=params)
    data = response.json()
    return data.get("esearchresult", {}).get("idlist", [])

def fetch_paper_summary(paper_id: str) -> Dict[str, str]:
    """Fetches paper title and publication date using PubMed summary API."""
    params = {"db": "pubmed", "id": paper_id, "retmode": "json", "api_key": API_KEY}
    response = requests.get(PUBMED_SUMMARY_URL, params=params)
    if response.status_code != 200:
        return {"title": "N/A", "pubdate": "N/A"}

    summary_data = response.json()
    result = summary_data.get("result", {}).get(paper_id, {})
    return {"title": result.get("title", "N/A"), "pubdate": result.get("pubdate", "N/A")}

def fetch_paper_details(paper_id: str) -> str:
    """Fetches detailed paper information."""
    params = {"db": "pubmed", "id": paper_id, "retmode": "xml", "api_key": API_KEY}
    response = requests.get(PUBMED_DETAILS_URL, params=params)
    return response.text
