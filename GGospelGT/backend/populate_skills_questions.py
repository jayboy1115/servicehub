#!/usr/bin/env python3
"""
Script to populate the database with skills test questions for Tiling trade category.
This script adds the predefined Tiling questions to the MongoDB database.
"""

import asyncio
import os
import sys
from datetime import datetime
import uuid

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import Database

# Tiling questions from the frontend data
TILING_QUESTIONS = [
    {
        "question": "What is the standard thickness for floor tiles in high-traffic areas?",
        "options": ["8mm", "10mm", "12mm", "15mm"],
        "correct_answer": 2,
        "category": "Material Selection",
        "explanation": "12mm thickness provides adequate durability for high-traffic areas.",
        "difficulty": "Medium"
    },
    {
        "question": "Which adhesive type is best for bathroom wall tiling?",
        "options": ["Cement-based", "Epoxy-based", "Flexible adhesive", "Standard tile adhesive"],
        "correct_answer": 2,
        "category": "Adhesives",
        "explanation": "Flexible adhesive accommodates movement and moisture in bathrooms.",
        "difficulty": "Medium"
    },
    {
        "question": "What is the maximum tile size recommended without expansion joints?",
        "options": ["3m²", "6m²", "9m²", "12m²"],
        "correct_answer": 2,
        "category": "Installation Standards",
        "explanation": "Expansion joints are required for tiled areas exceeding 9m².",
        "difficulty": "Medium"
    },
    {
        "question": "Which grout is suitable for swimming pool tiling?",
        "options": ["Cement grout", "Epoxy grout", "Polymer-modified grout", "Sand-cement grout"],
        "correct_answer": 1,
        "category": "Waterproofing",
        "explanation": "Epoxy grout provides superior water and chemical resistance for pools.",
        "difficulty": "Hard"
    },
    {
        "question": "What is the standard joint width for wall tiles?",
        "options": ["1-2mm", "2-3mm", "3-5mm", "5-8mm"],
        "correct_answer": 1,
        "category": "Installation Details",
        "explanation": "1-2mm joint width is standard for wall tiles for aesthetic appeal.",
        "difficulty": "Easy"
    },
    {
        "question": "In Nigeria's humid climate, what preparation is essential before tiling bathrooms?",
        "options": ["Primer only", "Waterproof membrane", "Leveling compound", "Base coat"],
        "correct_answer": 1,
        "category": "Waterproofing",
        "explanation": "Waterproof membrane is essential to prevent moisture penetration in humid conditions.",
        "difficulty": "Medium"
    },
    {
        "question": "What causes tiles to 'drum' or sound hollow?",
        "options": ["Wrong adhesive", "Insufficient adhesive coverage", "Poor substrate preparation", "All of the above"],
        "correct_answer": 3,
        "category": "Installation Problems",
        "explanation": "All factors can cause inadequate bonding leading to hollow-sounding tiles.",
        "difficulty": "Medium"
    },
    {
        "question": "Which tool is essential for checking tile alignment?",
        "options": ["Spirit level", "Tile spacers", "Rubber mallet", "All of the above"],
        "correct_answer": 3,
        "category": "Tools & Equipment",
        "explanation": "All tools are essential for proper tile installation and alignment.",
        "difficulty": "Easy"
    },
    {
        "question": "What is the recommended curing time before grouting ceramic tiles?",
        "options": ["6 hours", "12 hours", "24 hours", "48 hours"],
        "correct_answer": 2,
        "category": "Installation Process",
        "explanation": "24 hours curing time ensures proper adhesive set before grouting.",
        "difficulty": "Medium"
    },
    {
        "question": "Which edge treatment is best for external tile corners?",
        "options": ["Metal trim", "Plastic trim", "Mitred cuts", "Rounded edge tiles"],
        "correct_answer": 0,
        "category": "Finishing Details",
        "explanation": "Metal trim provides the most durable protection for external corners.",
        "difficulty": "Medium"
    },
    {
        "question": "What substrate moisture content is acceptable before tiling?",
        "options": ["Less than 3%", "Less than 5%", "Less than 8%", "Less than 10%"],
        "correct_answer": 1,
        "category": "Substrate Preparation",
        "explanation": "Substrate moisture should be less than 5% for successful tile installation.",
        "difficulty": "Hard"
    },
    {
        "question": "Which pattern requires the most tile wastage?",
        "options": ["Straight lay", "Diagonal lay", "Herringbone", "Brick pattern"],
        "correct_answer": 2,
        "category": "Layout Patterns",
        "explanation": "Herringbone pattern typically requires 10-15% extra tiles due to cutting.",
        "difficulty": "Medium"
    },
    {
        "question": "What is the maximum variation allowed in tile lippage?",
        "options": ["1mm", "2mm", "3mm", "5mm"],
        "correct_answer": 1,
        "category": "Quality Standards",
        "explanation": "Maximum 2mm variation is acceptable for professional tile installation.",
        "difficulty": "Hard"
    },
    {
        "question": "Which cleaning method should be avoided on natural stone tiles?",
        "options": ["Water cleaning", "Neutral pH cleaners", "Acid-based cleaners", "Steam cleaning"],
        "correct_answer": 2,
        "category": "Maintenance",
        "explanation": "Acid-based cleaners can damage and etch natural stone surfaces.",
        "difficulty": "Medium"
    },
    {
        "question": "What is the proper sequence for tile installation?",
        "options": ["Adhesive, tiles, grout, sealant", "Tiles, adhesive, grout, sealant", "Sealant, adhesive, tiles, grout", "Grout, tiles, adhesive, sealant"],
        "correct_answer": 0,
        "category": "Installation Process",
        "explanation": "Proper sequence ensures optimal bonding and finishing.",
        "difficulty": "Easy"
    }
]

async def populate_tiling_questions():
    """Populate the database with Tiling skills questions"""
    
    # Initialize database connection
    database = Database()
    
    try:
        # Connect to MongoDB
        await database.connect_to_mongo()
        print("Connected to MongoDB successfully")
        
        # Set the correct database name
        database.database = database.client['ServiceHub']
        
        # Check if questions already exist
        existing_questions = await database.get_questions_for_trade("Tiling")
        if existing_questions:
            print(f"Found {len(existing_questions)} existing Tiling questions. Skipping population.")
            return
        
        print("No existing Tiling questions found. Adding questions...")
        
        # Add each question to the database
        added_count = 0
        for question_data in TILING_QUESTIONS:
            try:
                question_id = await database.add_skills_question("Tiling", question_data)
                if question_id:
                    added_count += 1
                    print(f"Added question {added_count}: {question_data['question'][:50]}...")
                else:
                    print(f"Failed to add question: {question_data['question'][:50]}...")
            except Exception as e:
                print(f"Error adding question: {str(e)}")
        
        print(f"\nSuccessfully added {added_count} Tiling questions to the database!")
        
        # Verify the questions were added
        verification_questions = await database.get_questions_for_trade("Tiling")
        print(f"Verification: Found {len(verification_questions)} Tiling questions in database")
        
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        # Close database connection
        await database.close_mongo_connection()
        print("Database connection closed")

if __name__ == "__main__":
    print("Starting Tiling skills questions population...")
    asyncio.run(populate_tiling_questions())
    print("Population script completed!")