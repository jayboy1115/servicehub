#!/usr/bin/env python3
"""
Script to reduce skills assessment questions from 20 to 7 per trade
and ensure all trades have questions available.
"""

import asyncio
import os
import sys
import json
import re
from typing import List, Dict, Any

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import Database

# Trade categories from the project
TRADE_CATEGORIES = [
    "Plumbing", "Electrical Repairs", "Building", "Tiling", "Painting",
    "Carpentry", "Cleaning", "Concrete Works", "Door & Window Installation",
    "Flooring", "Furniture Making", "General Handyman Work", "Generator Services",
    "Home Extensions", "Interior Design", "Locksmithing", "Plastering/POP",
    "Recycling", "Relocation/Moving", "Renovations", "Roofing", "Scaffolding",
    "Solar & Inverter Installation", "Waste Disposal", "Welding"
]

def connect_to_mongodb():
    """Connect to MongoDB database using the working approach"""
    mongo_url = os.getenv('MONGO_URL')
    if not mongo_url:
        raise ValueError("MONGO_URL environment variable not set")
    
    # Use the same approach that worked in the previous script
    client = MongoClient(mongo_url)
    db = client['ServiceHub']
    return client, db

def read_skills_questions():
    """Read questions from skillsTestQuestions.js file"""
    js_file_path = os.path.join('..', 'frontend', 'src', 'data', 'skillsTestQuestions.js')
    
    if not os.path.exists(js_file_path):
        print(f"❌ File not found: {js_file_path}")
        return {}
    
    with open(js_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Extract the questions object
    match = re.search(r'export const skillsTestQuestions = ({.*?});', content, re.DOTALL)
    if not match:
        print("❌ Could not find skillsTestQuestions in the file")
        return {}
    
    questions_str = match.group(1)
    
    # Convert JavaScript object to Python dict
    try:
        # Replace JavaScript syntax with Python syntax
        questions_str = re.sub(r'(\w+):', r'"\1":', questions_str)  # Add quotes to keys
        questions_str = questions_str.replace("'", '"')  # Convert single quotes to double
        questions_dict = json.loads(questions_str)
        return questions_dict
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing questions: {e}")
        return {}

def select_best_questions(questions: List[Dict], target_count: int = 7) -> List[Dict]:
    """Select the best questions based on category diversity and quality"""
    if len(questions) <= target_count:
        return questions
    
    # Priority categories for better coverage
    priority_categories = ['safety', 'problem_diagnosis', 'tools', 'materials', 'techniques']
    
    selected = []
    used_categories = set()
    
    # First, select questions from priority categories
    for question in questions:
        if len(selected) >= target_count:
            break
        
        category = question.get('category', '').lower()
        if any(priority in category for priority in priority_categories):
            if category not in used_categories:
                selected.append(question)
                used_categories.add(category)
    
    # Fill remaining slots with other questions
    for question in questions:
        if len(selected) >= target_count:
            break
        
        if question not in selected:
            selected.append(question)
    
    return selected[:target_count]

def create_basic_questions(trade: str) -> List[Dict]:
    """Create basic questions for trades that don't have existing questions"""
    basic_questions = [
        {
            "question": f"What is the most important safety consideration when working in {trade.lower()}?",
            "options": [
                "Working quickly to finish the job",
                "Using proper safety equipment and following safety protocols",
                "Using the cheapest materials available",
                "Working alone to avoid distractions"
            ],
            "correct": 1,
            "category": "safety",
            "explanation": f"Safety should always be the top priority in {trade.lower()} work to prevent accidents and injuries."
        },
        {
            "question": f"What should you do before starting any {trade.lower()} project?",
            "options": [
                "Start working immediately",
                "Assess the situation and plan the work",
                "Use whatever tools are available",
                "Skip the preparation phase"
            ],
            "correct": 1,
            "category": "planning",
            "explanation": f"Proper assessment and planning are essential for successful {trade.lower()} projects."
        },
        {
            "question": f"Which quality is most important for a professional in {trade.lower()}?",
            "options": [
                "Working as fast as possible",
                "Attention to detail and quality workmanship",
                "Using only expensive tools",
                "Avoiding customer communication"
            ],
            "correct": 1,
            "category": "professionalism",
            "explanation": f"Quality workmanship and attention to detail are hallmarks of professional {trade.lower()} services."
        },
        {
            "question": f"How should you handle a problem you haven't encountered before in {trade.lower()}?",
            "options": [
                "Guess and hope for the best",
                "Research the problem and seek expert advice if needed",
                "Ignore the problem",
                "Use trial and error without planning"
            ],
            "correct": 1,
            "category": "problem_solving",
            "explanation": f"Professional {trade.lower()} work requires proper research and consultation when facing new challenges."
        },
        {
            "question": f"What is the best approach to customer service in {trade.lower()}?",
            "options": [
                "Avoid talking to customers",
                "Communicate clearly and professionally",
                "Only focus on the technical work",
                "Make promises you can't keep"
            ],
            "correct": 1,
            "category": "customer_service",
            "explanation": f"Clear, professional communication builds trust and ensures customer satisfaction in {trade.lower()} services."
        },
        {
            "question": f"Why is it important to keep learning in the {trade.lower()} field?",
            "options": [
                "It's not important once you have basic skills",
                "Technology and techniques constantly evolve",
                "Only beginners need to learn",
                "Learning is only for academic purposes"
            ],
            "correct": 1,
            "category": "continuous_learning",
            "explanation": f"The {trade.lower()} field constantly evolves with new technologies, materials, and techniques."
        },
        {
            "question": f"What should you do if you make a mistake during a {trade.lower()} job?",
            "options": [
                "Hide the mistake and hope no one notices",
                "Acknowledge the mistake and fix it properly",
                "Blame someone else",
                "Leave the job unfinished"
            ],
            "correct": 1,
            "category": "integrity",
            "explanation": f"Professional integrity in {trade.lower()} means taking responsibility for mistakes and fixing them properly."
        }
    ]
    
    return basic_questions

async def main():
    try:
        print("🚀 Starting skills questions reduction process...")
        print(f"📋 Target: 7 questions per trade for {len(TRADE_CATEGORIES)} trades")
        
        # Connect to database
        database = Database()
        await database.connect_to_mongo()
        print("🔌 Connected to MongoDB successfully")
        
        # Check current state
        skills_collection = database.database['skills_questions']
        current_count = await skills_collection.count_documents({})
        print(f"📊 Current questions in database: {current_count}")
        
        # Read existing questions from JS file
        print("📖 Reading questions from skillsTestQuestions.js...")
        js_questions = read_skills_questions()
        
        if not js_questions:
            print("❌ No questions found in JS file")
            return
        
        print(f"✅ Found questions for {len(js_questions)} trades in JS file")
        
        # Clear existing questions
        print("🗑️ Clearing existing questions from database...")
        await skills_collection.delete_many({})
        
        # Process each trade
        total_added = 0
        
        for trade in TRADE_CATEGORIES:
            print(f"🔧 Processing {trade}...")
            
            if trade in js_questions:
                # Select best 7 questions from existing ones
                existing_questions = js_questions[trade]
                selected_questions = select_best_questions(existing_questions, 7)
                print(f"   ✅ Selected {len(selected_questions)} questions from existing {len(existing_questions)}")
            else:
                # Create basic questions for missing trades
                selected_questions = create_basic_questions(trade)
                print(f"   ✅ Created {len(selected_questions)} basic questions")
            
            # Add questions to database using the database class method
            for question_data in selected_questions:
                try:
                    question_id = await database.add_skills_question(trade, question_data)
                    if question_id:
                        total_added += 1
                except Exception as e:
                    print(f"    Error adding question: {str(e)}")
        
        print(f"\n💾 Successfully processed {total_added} questions")
        
        # Show summary by trade
        print("\n📊 Questions per trade:")
        for trade in TRADE_CATEGORIES:
            count = await skills_collection.count_documents({'trade_category': trade})
            print(f"   {trade}: {count} questions")
        
        await database.close_mongo_connection()
        print("\n🎉 Skills questions reduction completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())