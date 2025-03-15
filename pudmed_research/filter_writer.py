import pandas as pd
import os
from typing import List, Dict

OUTPUT_DIR = "output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "research_papers.csv")

def ensure_output_directory():
    """Ensure the 'output' directory exists."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def save_to_csv(data: List[Dict], filename: str):
    """Saves extracted data to a CSV file, ensuring headers are written only once."""
    ensure_output_directory()

    # ✅ Define the correct column headers
    columns = ["PubMedID", "Title", "Publication Date", "Company Affiliations", "Email ID", "Summary"]

    # ✅ Convert list of dictionaries to a DataFrame
    df = pd.DataFrame(data, columns=columns)

    # ✅ Ensure headers exist if the file is empty
    file_exists = os.path.exists(filename) and os.path.getsize(filename) > 0

    # ✅ Write data to CSV
    df.to_csv(filename, index=False, mode='a', header=not file_exists, encoding='utf-8')

    print(f"✅ Results successfully saved to {filename}")
