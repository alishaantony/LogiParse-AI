import fitz
from pathlib import Path 

def extract_text_from_pdf(pdf_path):
    doc= fitz.open(pdf_path)
    full_text=" "


    for page in doc:
        full_text+= page.get_text()
    

    doc.close()
    return full_text


if __name__ =="__main__":
    
    project_root = Path(__file__).parent.parent
    pdf_path = project_root/"data"/"sample.pdf"
    
    extracted_text = extract_text_from_pdf(pdf_path)
    print("Extracted Text:")    
    print(extracted_text)