#!/usr/bin/env python3
"""
Test Nigerian Trades Skills Assessment System

This script tests the updated skills assessment system to ensure:
1. All 15 trades have exactly 7 questions each
2. Trade categories are properly configured
3. Questions have proper difficulty distribution
4. System can retrieve questions for assessment
"""

import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import sys
sys.path.append('.')
from models.trade_categories import NIGERIAN_TRADE_CATEGORIES, get_all_categories

async def test_nigerian_trades_system():
    """Test the complete Nigerian trades skills assessment system"""
    load_dotenv()
    
    client = AsyncIOMotorClient(os.getenv('MONGO_URL'))
    db = client[os.getenv('DB_NAME')]
    
    print("🧪 Testing Nigerian Trades Skills Assessment System")
    print("=" * 60)
    
    # Test 1: Verify trade categories configuration
    print("\n1️⃣ Testing Trade Categories Configuration")
    print("-" * 40)
    
    configured_trades = get_all_categories()
    print(f"   📋 Configured trades: {len(configured_trades)}")
    for i, trade in enumerate(configured_trades, 1):
        print(f"   {i:2d}. {trade}")
    
    # Test 2: Verify database questions
    print(f"\n2️⃣ Testing Database Questions")
    print("-" * 40)
    
    all_questions = await db.skills_questions.find({}).to_list(None)
    trade_counts = {}
    difficulty_distribution = {}
    
    for question in all_questions:
        trade = question.get('trade_category', 'Unknown')
        difficulty = question.get('difficulty', 'Unknown')
        
        # Count by trade
        trade_counts[trade] = trade_counts.get(trade, 0) + 1
        
        # Count by difficulty per trade
        if trade not in difficulty_distribution:
            difficulty_distribution[trade] = {'Easy': 0, 'Medium': 0, 'Hard': 0}
        difficulty_distribution[trade][difficulty] = difficulty_distribution[trade].get(difficulty, 0) + 1
    
    print(f"   📊 Total questions in database: {len(all_questions)}")
    print(f"   📈 Trades with questions: {len(trade_counts)}")
    
    # Test 3: Verify each trade has exactly 7 questions
    print(f"\n3️⃣ Testing Question Counts (Target: 7 per trade)")
    print("-" * 40)
    
    all_good = True
    for trade in sorted(trade_counts.keys()):
        count = trade_counts[trade]
        status = "✅" if count == 7 else "❌"
        print(f"   {status} {trade}: {count} questions")
        if count != 7:
            all_good = False
    
    if all_good:
        print(f"   🎯 SUCCESS: All trades have exactly 7 questions!")
    else:
        print(f"   ⚠️  WARNING: Some trades don't have 7 questions")
    
    # Test 4: Check difficulty distribution
    print(f"\n4️⃣ Testing Difficulty Distribution")
    print("-" * 40)
    
    for trade in sorted(difficulty_distribution.keys()):
        dist = difficulty_distribution[trade]
        total = sum(dist.values())
        print(f"   📚 {trade} ({total} total):")
        print(f"      Easy: {dist['Easy']}, Medium: {dist['Medium']}, Hard: {dist['Hard']}")
    
    # Test 5: Verify trade categories match database
    print(f"\n5️⃣ Testing Trade Categories Alignment")
    print("-" * 40)
    
    db_trades = set(trade_counts.keys())
    config_trades = set(configured_trades)
    
    missing_in_db = config_trades - db_trades
    extra_in_db = db_trades - config_trades
    
    if missing_in_db:
        print(f"   ⚠️  Trades in config but missing questions:")
        for trade in sorted(missing_in_db):
            print(f"      • {trade}")
    
    if extra_in_db:
        print(f"   ⚠️  Trades with questions but not in config:")
        for trade in sorted(extra_in_db):
            print(f"      • {trade}")
    
    if not missing_in_db and not extra_in_db:
        print(f"   ✅ Perfect alignment between config and database!")
    
    # Test 6: Sample question retrieval
    print(f"\n6️⃣ Testing Question Retrieval")
    print("-" * 40)
    
    # Test retrieving questions for a few trades
    test_trades = ["Generator Services", "Welding", "Carpentry"]
    
    for trade in test_trades:
        questions = await db.skills_questions.find({"trade_category": trade}).to_list(None)
        if questions:
            sample_q = questions[0]
            print(f"   ✅ {trade}: Retrieved {len(questions)} questions")
            print(f"      Sample: {sample_q['question'][:50]}...")
        else:
            print(f"   ❌ {trade}: No questions found")
    
    # Test 7: System summary
    print(f"\n7️⃣ System Summary")
    print("-" * 40)
    
    total_questions = sum(trade_counts.values())
    total_trades = len(trade_counts)
    avg_questions = total_questions / total_trades if total_trades > 0 else 0
    
    print(f"   📊 Total Questions: {total_questions}")
    print(f"   🏪 Total Trades: {total_trades}")
    print(f"   📈 Average Questions per Trade: {avg_questions:.1f}")
    print(f"   🎯 Target Questions per Trade: 7")
    
    # Overall status
    print(f"\n🏆 Overall System Status")
    print("=" * 60)
    
    if all_good and not missing_in_db and not extra_in_db and total_trades == 15:
        print("   ✅ SYSTEM READY: Nigerian trades skills assessment is fully configured!")
        print("   🇳🇬 All 15 Nigerian basic trades have 7 questions each")
        print("   📚 Total of 105 questions available for assessments")
    else:
        print("   ⚠️  SYSTEM NEEDS ATTENTION: Some issues detected above")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(test_nigerian_trades_system())