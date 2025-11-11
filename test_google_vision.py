"""
Verify Google Cloud Vision API setup
"""

import os
import dotenv
dotenv.load_dotenv()

def test_setup():
    """Check if Google Cloud Vision API is configured correctly"""
    
    print("=" * 60)
    print("Google Cloud Vision API - Setup Test")
    print("=" * 60)
    
    all_ok = True
    
    print("\n1. Checking google-cloud-vision library...")
    try:
        from google.cloud import vision
        print("   OK: Library installed")
    except ImportError:
        print("   ERROR: Library not installed")
        print("   Run: pip install google-cloud-vision")
        return False
    
    print("\n2. Checking credentials...")
    credentials_file = "google-cloud-key.json"
    env_cred = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    api_key = os.environ.get('GOOGLE_API_KEY')
    has_credentials = False
    client_options = None
    
    if api_key:
        print(f"   OK: API Key found in GOOGLE_API_KEY")
        from google.api_core.client_options import ClientOptions
        client_options = ClientOptions(api_key=api_key)
        has_credentials = True
    elif os.path.exists(credentials_file):
        print(f"   OK: JSON file found: {credentials_file}")
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_file
        has_credentials = True
    elif env_cred and os.path.exists(env_cred):
        print(f"   OK: JSON file found in env variable: {env_cred}")
        has_credentials = True
    
    if not has_credentials:
        print(f"   ERROR: No credentials found")
        print("\n   Options:")
        print("   1. Set GOOGLE_API_KEY environment variable")
        print("   2. Place google-cloud-key.json in project directory")
        return False
    
    print("\n3. Testing API connection...")
    try:
        if client_options:
            client = vision.ImageAnnotatorClient(client_options=client_options)
        else:
            client = vision.ImageAnnotatorClient()
        print("   OK: Client created successfully")
    except Exception as e:
        print(f"   ERROR: {e}")
        return False
    
    print("\n4. Testing OCR...")
    try:
        from PIL import Image, ImageDraw
        import io
        
        img = Image.new('RGB', (400, 100), color='white')
        draw = ImageDraw.Draw(img)
        draw.text((20, 30), "Test 123", fill='black')
        
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_bytes = img_byte_arr.getvalue()
        
        image = vision.Image(content=img_bytes)
        response = client.document_text_detection(image=image)
        
        if response.error.message:
            print(f"   ERROR: {response.error.message}")
            return False
        
        print("   OK: OCR works")
        
    except Exception as e:
        print(f"   ERROR: {e}")
        return False
    
    print("\n5. Checking other dependencies...")
    try:
        import fitz
        print("   OK: PyMuPDF installed")
    except ImportError:
        print("   ERROR: PyMuPDF not installed")
        print("   Run: pip install PyMuPDF")
        all_ok = False
    
    try:
        from PIL import Image
        print("   OK: Pillow installed")
    except ImportError:
        print("   ERROR: Pillow not installed")
        print("   Run: pip install Pillow")
        all_ok = False
    
    print("\n" + "=" * 60)
    if all_ok:
        print("SUCCESS: All checks passed")
        print("=" * 60)
        print("\nReady to use:")
        print("  python pdf_parser.py")
    else:
        print("FAILED: See errors above")
        print("=" * 60)
    
    return all_ok


if __name__ == "__main__":
    success = test_setup()
    exit(0 if success else 1)
