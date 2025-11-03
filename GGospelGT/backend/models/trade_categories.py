# Nigerian Market Trade Categories
# Comprehensive list of trades and services for the Nigerian marketplace

NIGERIAN_TRADE_CATEGORIES = [
    # Existing trades with questions (DO NOT REMOVE)
    "Building",
    "Electrical Repairs",
    "Painting", 
    "Plumbing",
    "Tiling",
    
    # Essential Nigerian basic trades
    "Generator Services",
    "Air Conditioning & Refrigeration",
    "Welding",
    "Carpentry",
    "General Handyman Work",
    "Roofing",
    "Cleaning",
    "Solar & Inverter Installation",
    "Bathroom Fitting",
    "Flooring",
    
    # New trades
    "Furniture Making",
    "Interior Design"
]

# For validation purposes
def validate_trade_category(category: str) -> bool:
    """Validate if a trade category is in the approved list"""
    return category in NIGERIAN_TRADE_CATEGORIES

def get_all_categories() -> list:
    """Get all available trade categories"""
    return NIGERIAN_TRADE_CATEGORIES.copy()

# Category groupings for better UX
TRADE_CATEGORY_GROUPS = {
    "Construction & Building": [
        "Building",
        "Tiling",
        "Flooring"
    ],
    "Interior & Finishing": [
        "Painting",
        "Bathroom Fitting",
        "Carpentry",
        "Furniture Making",
        "Interior Design"
    ],
    "Installation & Repair": [
        "Air Conditioning & Refrigeration",
        "Solar & Inverter Installation",
        "Generator Services"
    ],
    "Utilities & Systems": [
        "Electrical Repairs",
        "Plumbing",
        "Welding"
    ],
    "General Services": [
        "General Handyman Work",
        "Roofing",
        "Cleaning"
    ]
}