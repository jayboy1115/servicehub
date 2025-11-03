#!/usr/bin/env python3
"""
Test script to verify the updated Nigerian trades system with new trades
"""

import sys
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def connect_to_mongodb():
    """Connect to MongoDB database"""
    mongo_url = os.getenv('MONGO_URL')
    if not mongo_url:
        raise ValueError("MONGO_URL environment variable not set")
    
    client = MongoClient(mongo_url)
    db = client['ServiceHub']
    return client, db

def test_trade_categories():
    """Test that trade categories include the new trades"""
    try:
        # Import the updated trade categories
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from models.trade_categories import NIGERIAN_TRADE_CATEGORIES, TRADE_CATEGORY_GROUPS
        
        print("🔍 Testing Trade Categories Configuration...")
        
        # Check if new trades are in the list
        new_trades = ["Furniture Making", "Interior Design"]
        for trade in new_trades:
            if trade in NIGERIAN_TRADE_CATEGORIES:
                print(f"✅ {trade} found in NIGERIAN_TRADE_CATEGORIES")
            else:
                print(f"❌ {trade} NOT found in NIGERIAN_TRADE_CATEGORIES")
                return False
        
        # Check if new trades are in the Interior & Finishing group
        interior_finishing = TRADE_CATEGORY_GROUPS.get("Interior & Finishing", [])
        for trade in new_trades:
            if trade in interior_finishing:
                print(f"✅ {trade} found in Interior & Finishing group")
            else:
                print(f"❌ {trade} NOT found in Interior & Finishing group")
                return False
        
        print(f"📊 Total trades configured: {len(NIGERIAN_TRADE_CATEGORIES)}")
        print(f"📊 Interior & Finishing trades: {len(interior_finishing)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing trade categories: {e}")
        return False

def test_database_questions():
    """Test that database has questions for the new trades"""
    try:
        client, db = connect_to_mongodb()
        collection = db.skills_assessment_questions
        
        print("\n🔍 Testing Database Questions...")
        
        # Test new trades
        new_trades = ["Furniture Making", "Interior Design"]
        total_new_questions = 0
        
        for trade in new_trades:
            count = collection.count_documents({"trade_category": trade})
            print(f"📋 {trade}: {count} questions")
            
            if count == 7:
                print(f"✅ {trade} has correct number of questions (7)")
                total_new_questions += count
            else:
                print(f"❌ {trade} has incorrect number of questions (expected 7, got {count})")
                return False
        
        # Get all trades and their question counts
        all_trades = collection.distinct("trade_category")
        total_questions = collection.count_documents({})
        
        print(f"\n📈 System Summary:")
        print(f"Total trades with questions: {len(all_trades)}")
        print(f"Total questions in system: {total_questions}")
        print(f"New questions added: {total_new_questions}")
        
        # List all trades with their question counts
        print(f"\n📋 All Trades and Question Counts:")
        for trade in sorted(all_trades):
            count = collection.count_documents({"trade_category": trade})
            print(f"  {trade}: {count} questions")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing database questions: {e}")
        return False

def test_question_quality():
    """Test the quality and structure of new questions"""
    try:
        client, db = connect_to_mongodb()
        collection = db.skills_assessment_questions
        
        print("\n🔍 Testing Question Quality...")
        
        new_trades = ["Furniture Making", "Interior Design"]
        
        for trade in new_trades:
            questions = list(collection.find({"trade_category": trade}))
            
            print(f"\n📋 {trade} Questions Analysis:")
            
            # Check difficulty distribution
            difficulty_counts = {}
            for question in questions:
                difficulty = question.get('difficulty', 'Unknown')
                difficulty_counts[difficulty] = difficulty_counts.get(difficulty, 0) + 1
            
            print(f"  Difficulty distribution: {difficulty_counts}")
            
            # Check question structure
            valid_questions = 0
            for i, question in enumerate(questions, 1):
                has_question = bool(question.get('question'))
                has_options = len(question.get('options', [])) == 4
                has_correct_answer = bool(question.get('correct_answer'))
                has_explanation = bool(question.get('explanation'))
                
                if has_question and has_options and has_correct_answer and has_explanation:
                    valid_questions += 1
                else:
                    print(f"    ⚠ Question {i} missing required fields")
            
            print(f"  Valid questions: {valid_questions}/{len(questions)}")
            
            if valid_questions == len(questions):
                print(f"✅ All {trade} questions are properly structured")
            else:
                print(f"❌ Some {trade} questions have structural issues")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing question quality: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Testing Updated Nigerian Trades System with New Trades")
    print("=" * 60)
    
    all_tests_passed = True
    
    # Test 1: Trade Categories Configuration
    if not test_trade_categories():
        all_tests_passed = False
    
    # Test 2: Database Questions
    if not test_database_questions():
        all_tests_passed = False
    
    # Test 3: Question Quality
    if not test_question_quality():
        all_tests_passed = False
    
    print("\n" + "=" * 60)
    if all_tests_passed:
        print("🎉 ALL TESTS PASSED! The system is ready with the new trades.")
        print("✅ Furniture Making and Interior Design have been successfully added!")
    else:
        print("❌ SOME TESTS FAILED! Please check the issues above.")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)