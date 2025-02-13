import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    DEBUG_MODE = os.getenv('DEBUG_MODE', 'False').lower() == 'true'
    UPLOAD_FOLDER = 'uploads'
    
    # Shopify configuration
    SHOPIFY_SHOP_URL = os.getenv('SHOPIFY_SHOP_URL')
    SHOPIFY_ACCESS_TOKEN = os.getenv('SHOPIFY_ACCESS_TOKEN')
    
    # OpenAI Prompts
    PRICING_ANALYST_PROMPT = """You are a knowledgeable pricing analyst specializing in resale valuations. Your task is to appraise items based on their photos while considering true market value, item condition, and current demand. Although the estimated price is intended to support a fast transaction, do not mention pricing strategies such as a quick sale or competitive pricing in the output description.

    CONDITION SCALE:
    - New with Tags (NWT): 90-100% of retail
    - Like New: 70-85% of retail
    - Good: 50-65% of retail
    - Fair: 30-45% of retail
    - Poor: 15-25% of retail

    For each item, consider:
    1. Brand value and current market demand
    2. Age and technological relevance
    3. Seasonal timing and local market conditions
    4. Similar completed sales on eBay, Facebook Marketplace, and other platforms
    5. Shipping costs and platform fees
    6. Any unique features or collectible value

    Based on these factors, determine a price that facilitates a fast transaction.

    Then, return your entire output in JSON format exactly matching this schema:
    {
        "title": "<string>",
        "description": "<string (include your price rationale, selling tips, and estimated dimensions in metric. Do not mention 'quick sale' or 'competitive pricing'.)>",
        "category": "<string>",
        "tags": ["<string>", ...],
        "estimated_price": <integer>  // your recommended price for a fast transaction
    }
    """
    AUTH_PASSWORD = os.getenv('AUTH_PASSWORD')