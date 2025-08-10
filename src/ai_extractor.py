import os
import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path
from pdf_extractor import extract_text_from_pdf

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def extract_data_with_ai(text_content):
    
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    prompt_text =f"""
    Analyze the following logistics text. Your task is to extract these specific fields:
    - "document_id": The main identifier, like an Invoice Number or Shipment ID.
    - "contact_person": The name of any person mentioned as a contact or recipient.
    - "special_requirements": Any special notes like "Forklift required" or temperature constraints.
    - "due_date_or_deadline": Any mention of a due date or a delivery deadline.

    You MUST return the output as a valid JSON object. Do not include any explanatory text, 
    markdown formatting, or any characters before or after the JSON object. Your entire response
    should start with a '{{' and end with a '}}'.

    If a field is not found, use the value "N/A".
    
    Here is the text:
    ---
    {text_content}
    ---
    """
    response = model.generate_content(prompt_text)
    return response.text

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent
    pdf_path = project_root/"data"/"sample.pdf"
    raw_text = extract_text_from_pdf(pdf_path)
    
    
    ai_extracted_data = extract_data_with_ai(raw_text)
    
    print("AI Extracted data")
    print (ai_extracted_data)