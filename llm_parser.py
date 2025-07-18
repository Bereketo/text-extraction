import openai
import fitz  # PyMuPDF
import json
import os
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY is not set in the .env file!")

client = openai.OpenAI(api_key=api_key)


def extract_pdf_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = "\n".join(page.get_text() for page in doc)
    doc.close()
    return text


def build_prompt(pdf_text):
    schema = {
        "doc_dtls": {
            "document_type": "",
            "irn_no": "",
            "invoice_no": "",
            "invoice_date": "",
            "seller_name": "",
            "seller_gstin": "",
            "seller_location": "",
            "buyer_name": "",
            "buyer_gstin": "",
            "buyer_location": ""
        },
        "item_list": [
            {
                "sr_no": 1,
                "product_name": "",
                "item_description": "",
                "hsn_sac_no": "",
                "qty": "",
                "unit": "",
                "unit_price": "",
                "total_value": "",
                "disc_rate": "",
                "disc_amount": "",
                "taxable_value": "",
                "other_charges": "",
                "cgst_rate": "",
                "sgst_rate": "",
                "igst_rate": "",
                "cess_value": "",
                "total_amount": ""
            }
        ],
        "val_dtls": {
            "total_value_sum": "",
            "total_discount": "0",
            "total_other_charges": "",
            "total_taxable_value": "",
            "total_cgst_value": "",
            "total_sgst_value": "",
            "total_igst_value": "",
            "total_gst_value": "1",
            "total_invoice_value": ""
        },
        "extraction_costs": {
            "doc_dtls_cost": 0,
            "items_cost": 0.0038532,
            "val_dtls_cost": 0.0018368,
            "gst_extractor_cost": 0.0011756,
            "ocr_cost": 0.0,
            "total_cost": 0.0094048,
            "token_usage": 27034
        },
        "request_id": "mock-request-id",
        "file_type": "INVOICE"
    }

    return f"""You are a document intelligent agent.
Given the invoice text below, extract the structured data in JSON format exactly like the template shown below.
Extract all line items from the invoice without skipping any. Do not summarize.

 "".

JSON:
{json.dumps(schema, indent=2)}

---INVOICE TEXT---
{pdf_text}
"""


def extract_structured_json(prompt):
    chat_response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "You are a document parsing AI that extracts invoice data into structured JSON."},
                  {"role": "user", "content": prompt}
                  ],
        temperature=0,
    )
    return chat_response.choices[0].message.content.strip()


text = extract_pdf_text("data/Invoice Sample.pdf")
prompt = build_prompt(text)
response = extract_structured_json(prompt)


try:
    parsed = json.loads(response)
except json.JSONDecodeError:
    parsed = {"raw_output": response}

output_path = "output/llm_extracted_invoice.json"
os.makedirs("output", exist_ok=True)

with open("output/llm_extracted_invoice.json", "w") as f:
    json.dump(parsed, f, indent=2)

print(" Saved to output/llm_extracted_invoice.json")

