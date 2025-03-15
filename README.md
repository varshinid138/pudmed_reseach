"# Pudmed Research" 
# PudMed Research - Fetch & Summarize Research Papers

## 📌 Overview
**PudMed Research** is a Python project that fetches research papers from **PubMed**, extracts author affiliations, identifies pharmaceutical/biotech companies, and summarizes paper abstracts using **LLM (Hugging Face Transformers - `facebook/bart-large-cnn`)**. The extracted details are saved in a structured CSV format.

## 📂 Project Structure
```
├── pudmed_research/        # Main package
│   ├── cli.py              # Command-line interface (CLI) script
│   ├── pudmed_client.py    # Fetches data from PubMed API
│   ├── filter_utils.py     # Extracts authors, affiliations, and emails
│   ├── filter_writer.py    # Saves data to CSV
│   ├── llm_summarizer.py   # Summarizes text using LLM (Transformers)
├── tests/                  # Unit tests
├── output/                 # Folder to store output CSV
├── pyproject.toml          # Poetry configuration file
├── .gitignore              # Ignores unnecessary files
├── README.md               # Project documentation
```

## 🚀 Features
✅ Fetches research papers from **PubMed API** using search queries.  
✅ Extracts **authors**, **company affiliations**, and **corresponding author emails**.  
✅ Uses **Hugging Face Transformers** (`facebook/bart-large-cnn`) for **summarizing** research abstracts.  
✅ Saves extracted data into **CSV** format.  
✅ Provides a **CLI tool** (`get-papers-list`) for easy access.  
✅ Available on **TestPyPI** for installation & testing.  

---

## 🛠️ Installation & Setup
### **1️⃣ Install Poetry (Dependency Manager)**
```sh
pip install poetry
```

### **2️⃣ Clone the Repository (For Development Mode)**
```sh
git clone https://github.com/your-username/pudmed-research.git
cd pudmed-research
```

### **3️⃣ Install Dependencies Using Poetry**
```sh
poetry install
```

### **4️⃣ Activate Virtual Environment**
```sh
poetry shell
```

### **5️⃣ Run the CLI Tool**
```sh
poetry run get-papers-list "cancer research" 5 --debug -f output/research_papers.csv
```

---

## 🔥 Installing & Running from **TestPyPI**
This package is available on **TestPyPI** for testing purposes.

### **1️⃣ Create a New Virtual Environment (Recommended)**
```sh
python -m venv test_env
cd test_env
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On macOS/Linux
```

### **2️⃣ Install from TestPyPI**
```sh
pip install -i https://test.pypi.org/simple/ pudmed-research==0.1.3
```

### **3️⃣ Run the Installed CLI Tool**
```sh
python -m pudmed_research.cli "cancer" 5 --debug -f output/research_papers.csv
```

---

## ⚡ Key Components & Code Explanation
### 📜 `cli.py` (Command-Line Interface)
Handles user inputs, calls the **PubMed API**, extracts necessary data, and stores it in a CSV file.
```python
parser = argparse.ArgumentParser(description="Fetch and summarize research papers from PubMed.")
parser.add_argument("query", type=str, help="Search query")
parser.add_argument("max_results", type=int, help="Number of papers to fetch")
parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
parser.add_argument("-f", "--file", type=str, default="output/research_papers.csv", help="Output filename")
```

### 📜 `pudmed_client.py` (PubMed API Fetching)
Fetches **paper details, summaries, and affiliations** from **PubMed**.
```python
response = requests.get(PUBMED_API_URL, params=params)
data = response.json()
paper_ids = data.get("esearchresult", {}).get("idlist", [])
```

### 📜 `filter_utils.py` (Extracting Affiliations & Emails)
Extracts **emails and company affiliations** from research papers.
```python
def get_email_from_pubmed(xml_data: str) -> str:
    email_nodes = root.findall(".//Author/Email")
    for email_node in email_nodes:
        if email_node is not None and email_node.text:
            return email_node.text
    return "N/A"  # Return default if no email found
```

### 📜 `llm_summarizer.py` (Summarization using LLMs)
Uses **Hugging Face Transformers** (`facebook/bart-large-cnn`) to summarize **research abstracts**.
```python
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
def summarize_text(text: str, max_length: int = 1000):
    summary = summarizer(text, max_length=max_length, min_length=100, do_sample=False)
    return summary[0]["summary_text"]
```

### 📜 `filter_writer.py` (Saving Data to CSV)
Saves extracted information in a structured **CSV file**.
```python
def save_to_csv(data: List[Dict], filename: str):
    df = pd.DataFrame(data, columns=["PubMedID", "Title", "Publication Date", "Company Affiliations", "Email ID", "Summary"])
    df.to_csv(filename, index=False, mode='a', header=not os.path.exists(filename), encoding='utf-8')
```

---

## 🌍 Publishing to TestPyPI
Want to publish a new version? Follow these steps:
### **1️⃣ Remove Old Builds**
```sh
rm -rf dist/
```

### **2️⃣ Update `pyproject.toml` with a New Version**
```toml
version = "0.1.4"  # Increment version before publishing
```

### **3️⃣ Build the Package**
```sh
poetry build
```

### **4️⃣ Publish to TestPyPI**
```sh
poetry publish -r testpypi --username __token__ --password <YOUR_TEST_PYPI_API_TOKEN>
```

---

## 🔧 Troubleshooting
If you face any issues:
✔ **Check installed version:**
```sh
pip show pudmed-research
```
✔ **Reinstall dependencies:**
```sh
poetry install
```
✔ **Run the CLI manually:**
```sh
python -m pudmed_research.cli "Novartis" 5 --debug -f output/research_papers.csv
```

---

## 📜 License
This project is licensed under the **MIT License**.


