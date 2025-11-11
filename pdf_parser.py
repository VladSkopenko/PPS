"""
PDF OCR Parser using Google Cloud Vision API
"""

import os
from pathlib import Path


def extract_text_from_pdf(pdf_path, api_key=None, credentials_path="google-cloud-key.json"):
    """
    Extract text from PDF using Google Cloud Vision API
    
    Args:
        pdf_path: Path to PDF file
        api_key: Google Cloud API key (simple string)
        credentials_path: Path to Service Account JSON key
        
    Returns:
        Extracted text from all pages
    """
    
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    client_options = None
    
    if api_key:
        from google.api_core.client_options import ClientOptions
        client_options = ClientOptions(api_key=api_key)
    elif os.environ.get('GOOGLE_API_KEY'):
        api_key = os.environ.get('GOOGLE_API_KEY')
        from google.api_core.client_options import ClientOptions
        client_options = ClientOptions(api_key=api_key)
    elif os.path.exists(credentials_path):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
    elif os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'):
        pass
    else:
        raise ValueError(
            "No credentials found. Provide either:\n"
            "1. api_key parameter\n"
            "2. GOOGLE_API_KEY environment variable\n"
            "3. google-cloud-key.json file\n"
            "4. GOOGLE_APPLICATION_CREDENTIALS environment variable"
        )
    
    try:
        from google.cloud import vision
        import fitz
        from PIL import Image
        import io
    except ImportError as e:
        raise ImportError(f"Missing dependencies: {e}\nRun: pip install -r requirements.txt")
    
    if client_options:
        client = vision.ImageAnnotatorClient(client_options=client_options)
    else:
        client = vision.ImageAnnotatorClient()
    
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    all_text = []
    
    print(f"Processing {total_pages} pages...")
    
    for page_num in range(total_pages):
        page = doc[page_num]
        zoom = 300 / 72
        matrix = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=matrix)
        
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_bytes = img_byte_arr.getvalue()
        
        image = vision.Image(content=img_bytes)
        response = client.document_text_detection(image=image)
        
        if response.error.message:
            print(f"Page {page_num + 1}: API error - {response.error.message}")
            continue
        
        if response.full_text_annotation:
            text = response.full_text_annotation.text
            all_text.append(text)
            print(f"Page {page_num + 1}/{total_pages}: {len(text)} chars")
        else:
            print(f"Page {page_num + 1}/{total_pages}: No text found")
    
    doc.close()
    
    full_text = "\n\n--- PAGE BREAK ---\n\n".join(all_text)
    print(f"\nDone. Total: {len(full_text)} characters")
    
    return full_text


if __name__ == "__main__":
    pdf_files = list(Path(".").glob("*.pdf"))
    
    if not pdf_files:
        print("No PDF files found in current directory")
        print("\nUsage:")
        print("  python pdf_parser.py")
        print("\nOr import:")
        print("  from pdf_parser import extract_text_from_pdf")
        print('  text = extract_text_from_pdf("file.pdf", api_key="YOUR_KEY")')
        exit(1)
    
    pdf_file = pdf_files[0]
    print(f"Processing: {pdf_file}\n")
    
    try:
        text = extract_text_from_pdf(str(pdf_file))
        
        with open("result.txt", "w", encoding="utf-8") as f:
            f.write(text)
        
        print(f"\nSaved to: result.txt")
        print(f"\nPreview (first 300 chars):")
        print("-" * 60)
        print(text[:300] + "...")
        
    except Exception as e:
        print(f"Error: {e}")

