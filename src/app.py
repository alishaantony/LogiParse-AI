import streamlit as st
import json
from pathlib import Path

# We need to make sure Python can find our 'src' folder
import sys
sys.path.append('src')

# Now we can import our functions
from pdf_extractor import extract_text_from_pdf
from ai_extractor import extract_data_with_ai

# --- Page Setup ---
st.set_page_config(page_title="LogiParse AI", page_icon="📄")
st.title("📄 LogiParse AI")
st.write("Upload a logistics document (PDF) and the AI will extract the key information.")

# --- File Uploader ---
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Save the uploaded file temporarily
    data_folder = Path("data")
    data_folder.mkdir(exist_ok=True)
    file_path = data_folder / uploaded_file.name

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"File '{uploaded_file.name}' uploaded successfully.")

    # --- Processing and Displaying ---
    with st.spinner("The AI is reading the document..."):
        # 1. Extract text from the PDF
        raw_text = extract_text_from_pdf(file_path)

        # 2. Extract structured data with AI
        ai_response_str = extract_data_with_ai(raw_text)

        st.subheader("Extracted Raw Text")
        st.text_area("Raw Text", raw_text, height=250)

        st.subheader("AI Extracted Structured Data")
        try:
            # The AI's response is a string, let's clean it and parse it as JSON
            # This removes potential markdown formatting like ```json ... ```
            json_str = ai_response_str.strip().replace("```json", "").replace("```", "")
            parsed_json = json.loads(json_str)
            st.json(parsed_json)
        except json.JSONDecodeError:
            st.error("The AI did not return valid JSON. Displaying the raw response:")
            st.text(ai_response_str)