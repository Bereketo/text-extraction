# Information Extractor (LLM-Powered)

This project extracts structured JSON data from PDF invoices using GPT-4 and a JSON schema-aware prompt. It handles messy text, missing fields, and returns clean outputs ready for integration.

---

## 🚀 Features

✅ PDF-to-text extraction  
✅ Structured JSON extraction with GPT-4  
✅ Handles missing fields  
✅ Auto-formats invoice line items  
✅ Easily extendable to OCR or Donut-based parsing

---

## 🧱 Project Structure


---

## ⚙️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/bereketo/text-extraction.git
cd text-extraction
```

### 2. Create virtual environment
```
python -m venv venv
source venv/bin/activate     # Linux/macOS
venv\Scripts\activate        # Windows
```
### 3. Install dependencies 
```
pip install -r requirements.txt
```

### 4. Set your api key
```
client = openai.OpenAI(api_key="your-api-key")
```
Or load from **.env** environment
```
export OPENAI_API_KEY="your-key"
```

### 5. Run the script
```
python llm_parser.py
```
