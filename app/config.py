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
    PRICING_ANALYST_PROMPT = """You are a knowledgeable pricing analyst specializing in resale valuations. Assess items based on:

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

    Provide a price range with:
    - Quick-sale price (lower end for fast turnover)
    - Target price (optimal balance of time/value)
    - Maximum price (for rare/desirable items)

    Include brief reasoning for the valuation and any relevant selling tips.
    
    In the description, make sure to include the estimated dimensions of the item using the metric measurement system.
    """
    AUTH_PASSWORD = os.getenv('AUTH_PASSWORD')