import argparse
from pudmed_research.pudmed_client import fetch_pubmed_papers, fetch_paper_summary, fetch_paper_details
from pudmed_research.filter_utils import extract_affiliations
from pudmed_research.filter_writer import save_to_csv
from pudmed_research.llm_summarizer import summarize_text

def main():
    parser = argparse.ArgumentParser(description="Fetch and summarize research papers from PubMed.")
    parser.add_argument("query", type=str, help="Search query")
    parser.add_argument("max_results", type=int, help="Number of papers to fetch")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("-f", "--file", type=str, default="output/research_papers.csv", help="Output filename (default: output/research_papers.csv)")

    args = parser.parse_args()
    paper_ids = fetch_pubmed_papers(args.query, args.max_results)

    results = []
    for paper_id in paper_ids:
        xml_data = fetch_paper_details(paper_id)
        summary_data = fetch_paper_summary(paper_id)
        affiliations, non_academic_authors, company_affiliations, email = extract_affiliations(xml_data)
        summary = summarize_text(xml_data)  # Summarize the research paper

        # ✅ DEBUG: PRINT ALL FETCHED DATA
        print("\n📌 Fetched Data for Paper ID:", paper_id)
        print("🔹 Title:", summary_data["title"])
        print("📅 Publication Date:", summary_data["pubdate"])
        print("👨‍🔬 Non-Academic Authors:", non_academic_authors)
        print("🏢 Company Affiliations:", company_affiliations)
        print("📧 Email ID:", email)
        print("📝 Summary:", summary)
        print(f"DEBUG: Extracted Email for {paper_id}: {email}")
        # ✅ Store data in dictionary format
        paper_info = {
            "PubMedID": paper_id,
            "Title": summary_data["title"],
            "Publication Date": summary_data["pubdate"],
            "Company Affiliations": "; ".join(company_affiliations) if company_affiliations else "N/A",
            "Email ID": email,
            "Summary": summary
        }

        results.append(paper_info)


    save_to_csv(results, filename=args.file)

if __name__ == "__main__":
    main()
