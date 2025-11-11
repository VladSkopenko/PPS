"""
Usage examples for PDF parser
"""

from pdf_parser import extract_text_from_pdf
import os
import dotenv
dotenv.load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")



def example_with_api_key():
    """Simple API key usage"""
    
    api_key = os.getenv("GOOGLE_API_KEY", "YOUR_API_KEY_HERE")
    text = extract_text_from_pdf("структури власності_1.pdf", api_key=api_key)
    print(text)


def example_with_json():
    """Service Account JSON file"""
    
    text = extract_text_from_pdf("власності_1.pdf")
    print(text)


def example_batch():
    """Process multiple PDFs"""
    
    import glob
    
    api_key = os.getenv("GOOGLE_API_KEY")
    
    for pdf_file in glob.glob("*.pdf"):
        print(f"Processing: {pdf_file}")
        text = extract_text_from_pdf(pdf_file, api_key=api_key)
        
        output = pdf_file.replace(".pdf", "_extracted.txt")
        with open(output, "w", encoding="utf-8") as f:
            f.write(text)
        
        print(f"Saved: {output}\n")


if __name__ == "__main__":
    print("Uncomment example you want to run:\n")
    
    example_with_api_key()
    example_with_json()
    #example_batch()
