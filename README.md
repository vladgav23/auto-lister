# Camera Upload Application

A web application that captures photos and uses GPT-4 to analyze them, then creates Shopify listings.

## Quick Start

1. Set up environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install flask openai python-dotenv
```


2. Create `.env`:
```
OPENAI_API_KEY=your_api_key_here
DEBUG_MODE=False

# Shopify API Credentials
SHOPIFY_STORE_URL=your-store.myshopify.com
SHOPIFY_ACCESS_TOKEN=your_access_token
```


3. Run:
```bash
python app.py
```


## Project Structure

```
├── app/
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css      # Main styling
│   │   └── js/
│   │       ├── components/     # React components
│   │       │   ├── ListingPopup.jsx
│   │       │   └── CameraApp.jsx
│   │       └── main.js         # Core camera functionality
│   ├── templates/
│   │   └── index.html         # Main page template
│   └── list.py               # Listing class & OpenAI/Shopify integration
└── app.py                    # Flask application
```


## Key Components

### Camera Interface
- Uses `getUserMedia` API with environment-facing camera preference
- Captures photos and displays thumbnails
- Allows photo deletion before upload

### AI Analysis
- Integrates with GPT-4 for image analysis
- Provides detailed pricing analysis based on:
  - Condition scale (NWT to Poor)
  - Market factors
  - Comparable sales
  - Platform considerations

### Shopify Integration
- Automatically creates draft listings in Shopify
- Uses AI-generated metadata for product details
- Uploads photos to Shopify's CDN
- Creates variants based on analysis