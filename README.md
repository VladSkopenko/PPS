# PDF OCR with Google Cloud Vision API

Extract text from PDF files using Google Cloud Vision API.

## Features

- 1000 requests/month free
- Excellent OCR quality for Cyrillic text
- Simple API

## Quick Start

### 1. Install

```bash
pip install -r requirements.txt
```

### 2. Get API Key

1. Go to https://console.cloud.google.com/
2. Create new project
3. Enable "Cloud Vision API"
4. Credentials → Create → API Key
5. Copy the key

### 3. Use

```python
from pdf_parser import extract_text_from_pdf

text = extract_text_from_pdf("document.pdf", api_key="YOUR_API_KEY")
print(text)
```

## Pricing

| Requests | Cost |
|----------|------|
| 0 - 1,000/month | Free |
| 1,001+ | $1.50 per 1,000 |

## Files

- `pdf_parser.py` - Main parser
- `example.py` - Usage examples
- `test_google_vision.py` - Setup verification

## License

MIT
