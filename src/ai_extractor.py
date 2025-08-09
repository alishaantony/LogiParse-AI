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
    From the following logistics document text, please extract the following:
    - Invoice Number
    - Due Date
    - Total Amount
    
    You MUST return the output as a valid JSON object. Do not include any explanatory text, 
    markdown formatting, or any characters before or after the JSON object. Your entire response
    should start with a '{{' and end with a '}}'.
    
    If a piece of information is not found, use "N/A"
    
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