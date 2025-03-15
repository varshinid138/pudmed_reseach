from transformers import pipeline
from typing import List
import re

# Load Hugging Face Summarization Pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def clean_text(text: str) -> str:
    """Removes XML tags and unnecessary metadata."""
    text = re.sub(r"<.*?>", " ", text)  # Remove XML tags
    text = re.sub(r"\s+", " ", text).strip()  # Remove extra spaces
    return text

def summarize_text(text: str, max_length: int = 400) -> str:
    """Summarizes a given research paper text using a transformer model."""
    
    # ✅ Clean input text (remove XML tags)
    text = clean_text(text)
    
    print(f"DEBUG: Summarizing text of length {len(text.split())} words")

    # ✅ If text is 500 words or less, return it as is
    if len(text.split()) <= 500:
        print("DEBUG: Text is short, returning full text instead of summarization.")
        return text

    # ✅ Trim text if it's too long for the model
    if len(text.split()) > 1000:
        print("DEBUG: Text too long, truncating to 1000 words.")
        text = " ".join(text.split()[:1000])

    # ✅ Print cleaned text being sent for summarization
    print(f"DEBUG: Input Text for Summarization:\n{text[:500]}...\n")

    try:
        summary = summarizer(text, max_length=max_length, min_length=100, do_sample=False)
        return summary[0]["summary_text"]
    except Exception as e:
        print(f"❌ ERROR: Summarization failed - {e}")
        return "Summarization Error"
