#!/usr/bin/env python3
"""
Script to add skills assessment questions for Furniture Making and Interior Design trades
"""

import sys
import os
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def connect_to_mongodb():
    """Connect to MongoDB database using the working approach"""
    mongo_url = os.getenv('MONGO_URL')
    if not mongo_url:
        raise ValueError("MONGO_URL environment variable not set")
    
    # Use the same approach that worked in the previous script
    client = MongoClient(mongo_url)
    db = client['ServiceHub']
    return client, db

def create_furniture_making_questions():
    """Create 7 skills assessment questions for Furniture Making"""
    return [
        {
            "trade_category": "Furniture Making",
            "question": "What type of wood joint is strongest for connecting two pieces of wood at a right angle?",
            "options": [
                "Butt joint",
                "Mortise and tenon joint",
                "Lap joint",
                "Biscuit joint"
            ],
            "correct_answer": "Mortise and tenon joint",
            "difficulty": "Medium",
            "explanation": "Mortise and tenon joints provide the strongest connection for right-angle joints due to their interlocking design and large glue surface area."
        },
        {
            "trade_category": "Furniture Making",
            "question": "Which wood species is most commonly used for furniture making in Nigeria due to its availability and workability?",
            "options": [
                "Mahogany",
                "Iroko",
                "Obeche",
                "Ebony"
            ],
            "correct_answer": "Iroko",
            "difficulty": "Easy",
            "explanation": "Iroko is widely available in Nigeria, durable, and has excellent workability, making it a popular choice for furniture making."
        },
        {
            "trade_category": "Furniture Making",
            "question": "What is the recommended moisture content for wood used in furniture making?",
            "options": [
                "15-20%",
                "8-12%",
                "20-25%",
                "5-8%"
            ],
            "correct_answer": "8-12%",
            "difficulty": "Medium",
            "explanation": "Wood with 8-12% moisture content is properly seasoned and stable, reducing the risk of warping, cracking, or shrinking after furniture construction."
        },
        {
            "trade_category": "Furniture Making",
            "question": "Which finishing technique provides the best protection for outdoor wooden furniture?",
            "options": [
                "Shellac",
                "Polyurethane varnish",
                "Wax finish",
                "Oil finish"
            ],
            "correct_answer": "Polyurethane varnish",
            "difficulty": "Hard",
            "explanation": "Polyurethane varnish creates a durable, waterproof barrier that protects wood from UV rays, moisture, and weather damage, making it ideal for outdoor furniture."
        },
        {
            "trade_category": "Furniture Making",
            "question": "What is the primary purpose of using wood glue in furniture construction?",
            "options": [
                "To fill gaps between wood pieces",
                "To create strong, permanent bonds between wood surfaces",
                "To prevent wood from splitting",
                "To add color to the wood"
            ],
            "correct_answer": "To create strong, permanent bonds between wood surfaces",
            "difficulty": "Easy",
            "explanation": "Wood glue chemically bonds with wood fibers to create joints that are often stronger than the wood itself when properly applied."
        },
        {
            "trade_category": "Furniture Making",
            "question": "Which tool is essential for creating precise, smooth curves in furniture making?",
            "options": [
                "Circular saw",
                "Band saw",
                "Table saw",
                "Miter saw"
            ],
            "correct_answer": "Band saw",
            "difficulty": "Medium",
            "explanation": "Band saws have a thin, flexible blade that can follow curved cutting lines precisely, making them ideal for creating smooth curves in furniture components."
        },
        {
            "trade_category": "Furniture Making",
            "question": "What is the correct sequence for sanding furniture before finishing?",
            "options": [
                "Start with fine grit, progress to coarse grit",
                "Use only medium grit throughout",
                "Start with coarse grit, progress to fine grit",
                "Sand only with steel wool"
            ],
            "correct_answer": "Start with coarse grit, progress to fine grit",
            "difficulty": "Hard",
            "explanation": "Progressive sanding from coarse to fine grit (e.g., 80→120→180→220) removes scratches from previous grits and creates an increasingly smooth surface for finishing."
        }
    ]

def create_interior_design_questions():
    """Create 7 skills assessment questions for Interior Design"""
    return [
        {
            "trade_category": "Interior Design",
            "question": "What is the 60-30-10 rule in interior design?",
            "options": [
                "Room dimensions ratio",
                "Color distribution formula",
                "Furniture spacing guideline",
                "Lighting intensity ratio"
            ],
            "correct_answer": "Color distribution formula",
            "difficulty": "Medium",
            "explanation": "The 60-30-10 rule suggests using 60% dominant color, 30% secondary color, and 10% accent color to create balanced and harmonious color schemes."
        },
        {
            "trade_category": "Interior Design",
            "question": "Which color combination creates a warm and inviting atmosphere in Nigerian homes?",
            "options": [
                "Blue and white",
                "Earth tones with warm accents",
                "Black and gray",
                "Purple and silver"
            ],
            "correct_answer": "Earth tones with warm accents",
            "difficulty": "Easy",
            "explanation": "Earth tones like browns, beiges, and terracotta with warm accents like orange or gold create cozy, welcoming spaces that complement Nigerian climate and culture."
        },
        {
            "trade_category": "Interior Design",
            "question": "What is the ideal ceiling height for residential spaces in Nigeria to ensure comfort and energy efficiency?",
            "options": [
                "2.4 - 2.7 meters",
                "3.0 - 3.6 meters",
                "2.0 - 2.3 meters",
                "4.0 - 4.5 meters"
            ],
            "correct_answer": "3.0 - 3.6 meters",
            "difficulty": "Medium",
            "explanation": "Higher ceilings (3.0-3.6m) promote better air circulation and heat dissipation, which is crucial for comfort in Nigeria's warm climate while maintaining proportional aesthetics."
        },
        {
            "trade_category": "Interior Design",
            "question": "Which lighting principle is most important for creating functional task areas in Nigerian homes?",
            "options": [
                "Use only natural light",
                "Layer ambient, task, and accent lighting",
                "Install only overhead fixtures",
                "Use colored lighting throughout"
            ],
            "correct_answer": "Layer ambient, task, and accent lighting",
            "difficulty": "Hard",
            "explanation": "Layered lighting combines general illumination (ambient), focused work lighting (task), and decorative lighting (accent) to create versatile, functional spaces."
        },
        {
            "trade_category": "Interior Design",
            "question": "What is the recommended walking space around furniture in a living room?",
            "options": [
                "30-45 cm",
                "60-90 cm",
                "15-30 cm",
                "120-150 cm"
            ],
            "correct_answer": "60-90 cm",
            "difficulty": "Easy",
            "explanation": "60-90 cm provides comfortable passage around furniture, allowing easy movement without feeling cramped or wasting space."
        },
        {
            "trade_category": "Interior Design",
            "question": "Which material is best for flooring in Nigerian kitchens considering climate and maintenance?",
            "options": [
                "Carpet",
                "Hardwood",
                "Ceramic tiles",
                "Laminate"
            ],
            "correct_answer": "Ceramic tiles",
            "difficulty": "Medium",
            "explanation": "Ceramic tiles are water-resistant, easy to clean, cool underfoot in hot weather, and durable against humidity and spills common in Nigerian kitchens."
        },
        {
            "trade_category": "Interior Design",
            "question": "What is the most effective way to maximize natural light in Nigerian homes while controlling heat gain?",
            "options": [
                "Remove all window treatments",
                "Use dark, heavy curtains",
                "Install light-colored blinds or sheer curtains",
                "Paint walls in dark colors"
            ],
            "correct_answer": "Install light-colored blinds or sheer curtains",
            "difficulty": "Hard",
            "explanation": "Light-colored blinds or sheer curtains allow natural light to enter while diffusing harsh sunlight and reducing heat gain, perfect for Nigeria's bright climate."
        }
    ]

def main():
    """Main function to add questions for both trades"""
    try:
        # Connect to database
        client, db = connect_to_mongodb()
        collection = db.skills_assessment_questions
        
        print("Adding Furniture Making and Interior Design questions...")
        
        # Create questions for both trades
        furniture_questions = create_furniture_making_questions()
        interior_questions = create_interior_design_questions()
        
        all_new_questions = furniture_questions + interior_questions
        
        # Insert questions
        inserted_count = 0
        for question in all_new_questions:
            try:
                result = collection.insert_one(question)
                if result.inserted_id:
                    inserted_count += 1
                    print(f"✓ Added question for {question['trade_category']}: {question['question'][:50]}...")
            except DuplicateKeyError:
                print(f"⚠ Question already exists for {question['trade_category']}")
            except Exception as e:
                print(f"✗ Error adding question for {question['trade_category']}: {e}")
        
        print(f"\n📊 Summary:")
        print(f"Total questions added: {inserted_count}")
        
        # Verify final counts
        print(f"\n🔍 Verification:")
        for trade in ["Furniture Making", "Interior Design"]:
            count = collection.count_documents({"trade_category": trade})
            print(f"{trade}: {count} questions")
        
        # Get total count across all trades
        total_questions = collection.count_documents({})
        total_trades = len(collection.distinct("trade_category"))
        print(f"\n📈 System totals:")
        print(f"Total trades: {total_trades}")
        print(f"Total questions: {total_questions}")
        
        print(f"\n✅ Successfully added questions for Furniture Making and Interior Design!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)