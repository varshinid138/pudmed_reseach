import xml.etree.ElementTree as ET
import re
from typing import List, Tuple, Optional

PHARMA_KEYWORDS = ["pharmaceutical", "biotech", "biotechnology", "drug company", "pharma"]

def extract_email_from_text(text: str) -> Optional[str]:
    """Extracts email addresses from text using regex."""
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group(0) if match else None

def get_email_from_pubmed(xml_data: str) -> str:
    """Extracts the corresponding author's email from PubMed XML data."""
    corresponding_author_email = "N/A"
    root = ET.fromstring(xml_data)

    # ✅ 1. Check <Author><Email> tags
    email_nodes = root.findall(".//Author/Email")
    for email_node in email_nodes:
        if email_node is not None and email_node.text:
            return email_node.text  # Return the first found email

    # ✅ 2. Check affiliations for emails
    for aff in root.findall(".//AffiliationInfo/Affiliation"):
        extracted_email = extract_email_from_text(aff.text or "")
        if extracted_email:
            return extracted_email  # Return the first found email

    # ✅ 3. Check other locations like <CommentsCorrections>
    comments_corrections = root.findall(".//CommentsCorrections")
    for comment in comments_corrections:
        extracted_email = extract_email_from_text(comment.text or "")
        if extracted_email:
            return extracted_email  # Return the first found email

    return corresponding_author_email  # If no email is found, return "N/A"

def extract_affiliations(xml_data: str) -> Tuple[List[str], List[str], List[str], str]:
    """Extracts authors, affiliations, and corresponding author email."""
    affiliations, non_academic_authors, company_affiliations = [], [], []
    
    root = ET.fromstring(xml_data)

    for author in root.findall(".//Author"):
        aff = author.find("AffiliationInfo/Affiliation")
        if aff is not None and aff.text:
            aff_text = aff.text.lower()
            affiliations.append(aff_text)
            if any(keyword in aff_text for keyword in PHARMA_KEYWORDS):
                company_affiliations.append(aff_text)
            else:
                non_academic_authors.append(author.find("LastName").text or "Unknown")

    # ✅ Get email using the new function
    corresponding_author_email = get_email_from_pubmed(xml_data)

    print(f"DEBUG: Found Email - {corresponding_author_email}")
    return affiliations, non_academic_authors, company_affiliations, corresponding_author_email
