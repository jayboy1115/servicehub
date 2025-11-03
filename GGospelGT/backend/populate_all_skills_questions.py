#!/usr/bin/env python3
"""
Script to populate the database with skills test questions for ALL trade categories.
This script reads the complete skillsTestQuestions.js file and adds all questions to the MongoDB database.
"""

import asyncio
import os
import sys
import json
import re
from datetime import datetime
import uuid
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import Database

def parse_js_questions_file(file_path):
    """Parse the JavaScript skillsTestQuestions.js file and extract all questions"""
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Extract the skillsTestQuestions object
    # Find the start of the object
    start_pattern = r'export const skillsTestQuestions\s*=\s*{'
    start_match = re.search(start_pattern, content)
    
    if not start_match:
        raise ValueError("Could not find skillsTestQuestions object in file")
    
    start_pos = start_match.end() - 1  # Include the opening brace
    
    # Find the matching closing brace
    brace_count = 0
    end_pos = start_pos
    
    for i, char in enumerate(content[start_pos:], start_pos):
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0:
                end_pos = i + 1
                break
    
    # Extract the object content
    obj_content = content[start_pos:end_pos]
    
    # Parse trade categories and their questions
    trades_data = {}
    
    # Find all trade categories
    trade_pattern = r"'([^']+)'\s*:\s*\["
    trade_matches = re.finditer(trade_pattern, obj_content)
    
    for match in trade_matches:
        trade_name = match.group(1)
        trade_start = match.end() - 1  # Include the opening bracket
        
        # Find the matching closing bracket for this trade
        bracket_count = 0
        trade_end = trade_start
        
        for i, char in enumerate(obj_content[trade_start:], trade_start):
            if char == '[':
                bracket_count += 1
            elif char == ']':
                bracket_count -= 1
                if bracket_count == 0:
                    trade_end = i + 1
                    break
        
        # Extract questions for this trade
        trade_content = obj_content[trade_start:trade_end]
        questions = parse_questions_from_trade_content(trade_content)
        trades_data[trade_name] = questions
    
    return trades_data

def parse_questions_from_trade_content(trade_content):
    """Parse individual questions from a trade's content"""
    questions = []
    
    # Find all question objects
    question_pattern = r'\{\s*question:\s*"([^"]+)"'
    question_matches = re.finditer(question_pattern, trade_content)
    
    for match in question_matches:
        question_start = match.start()
        
        # Find the matching closing brace for this question
        brace_count = 0
        question_end = question_start
        
        for i, char in enumerate(trade_content[question_start:], question_start):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    question_end = i + 1
                    break
        
        # Extract and parse the question object
        question_content = trade_content[question_start:question_end]
        question_data = parse_single_question(question_content)
        if question_data:
            questions.append(question_data)
    
    return questions

def parse_single_question(question_content):
    """Parse a single question object from JavaScript format"""
    try:
        # Extract question text
        question_match = re.search(r'question:\s*"([^"]+)"', question_content)
        if not question_match:
            return None
        question_text = question_match.group(1)
        
        # Extract options array
        options_match = re.search(r'options:\s*\[([^\]]+)\]', question_content)
        if not options_match:
            return None
        options_str = options_match.group(1)
        options = [opt.strip().strip('"') for opt in options_str.split(',')]
        
        # Extract correct answer
        correct_match = re.search(r'correct:\s*(\d+)', question_content)
        if not correct_match:
            return None
        correct_answer = int(correct_match.group(1))
        
        # Extract category
        category_match = re.search(r'category:\s*"([^"]+)"', question_content)
        category = category_match.group(1) if category_match else "General"
        
        # Extract explanation
        explanation_match = re.search(r'explanation:\s*"([^"]+)"', question_content)
        explanation = explanation_match.group(1) if explanation_match else ""
        
        return {
            "question": question_text,
            "options": options,
            "correct_answer": correct_answer,
            "category": category,
            "explanation": explanation,
            "difficulty": "Medium"  # Default difficulty
        }
    
    except Exception as e:
        print(f"Error parsing question: {str(e)}")
        return None

async def populate_all_trades_questions():
    """Populate the database with all trades' skills questions"""
    
    # Path to the frontend skillsTestQuestions.js file
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'src', 'data', 'skillsTestQuestions.js')
    
    if not os.path.exists(frontend_path):
        print(f"Error: Could not find skillsTestQuestions.js at {frontend_path}")
        return
    
    print(f"Reading questions from: {frontend_path}")
    
    try:
        # Parse the JavaScript file
        trades_data = parse_js_questions_file(frontend_path)
        print(f"Found {len(trades_data)} trade categories:")
        for trade, questions in trades_data.items():
            print(f"  - {trade}: {len(questions)} questions")
        
    except Exception as e:
        print(f"Error parsing JavaScript file: {str(e)}")
        return
    
    # Initialize database connection
    database = Database()
    
    try:
        # Connect to MongoDB
        await database.connect_to_mongo()
        print("\nConnected to MongoDB successfully")
        
        # Set the correct database name
        database.database = database.client['ServiceHub']
        
        total_added = 0
        
        # Process each trade category
        for trade_name, questions in trades_data.items():
            print(f"\nProcessing {trade_name}...")
            
            # Check if questions already exist
            existing_questions = await database.get_questions_for_trade(trade_name)
            if existing_questions:
                print(f"  Found {len(existing_questions)} existing questions. Skipping {trade_name}.")
                continue
            
            print(f"  No existing questions found. Adding {len(questions)} questions...")
            
            # Add each question to the database
            added_count = 0
            for question_data in questions:
                try:
                    question_id = await database.add_skills_question(trade_name, question_data)
                    if question_id:
                        added_count += 1
                    else:
                        print(f"    Failed to add question: {question_data['question'][:50]}...")
                except Exception as e:
                    print(f"    Error adding question: {str(e)}")
            
            print(f"  Successfully added {added_count} questions for {trade_name}")
            total_added += added_count
        
        print(f"\n=== SUMMARY ===")
        print(f"Total questions added across all trades: {total_added}")
        
        # Verify all trades have questions
        print(f"\nVerification:")
        for trade_name in trades_data.keys():
            verification_questions = await database.get_questions_for_trade(trade_name)
            print(f"  {trade_name}: {len(verification_questions)} questions in database")
        
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        # Close database connection
        await database.close_mongo_connection()
        print("\nDatabase connection closed")

if __name__ == "__main__":
    print("Starting comprehensive skills questions population for all trades...")
    asyncio.run(populate_all_trades_questions())
    print("Population script completed!")