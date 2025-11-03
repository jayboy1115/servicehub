#!/usr/bin/env python3
"""
Reduce Skills Assessment Questions to 7 per Trade

This script reduces the number of skills assessment questions from 20+ to 7 
for each trade category to prevent user boredom during registration.

Current situation:
- Building: 20 questions → reduce to 7
- Electrical Repairs: 20 questions → reduce to 7  
- Painting: 20 questions → reduce to 7
- Plumbing: 28 questions → reduce to 7
- Tiling: 15 questions → reduce to 7
"""

import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import random

async def reduce_questions_to_7():
    """Reduce questions to 7 per trade category"""
    load_dotenv()
    
    client = AsyncIOMotorClient(os.getenv('MONGO_URL'))
    db = client[os.getenv('DB_NAME')]
    
    print("🔧 Reducing Skills Assessment Questions to 7 per Trade")
    print("=" * 60)
    
    # Get all skills questions
    questions = await db.skills_questions.find({}).to_list(None)
    
    # Group by trade_category
    trade_questions = {}
    for q in questions:
        trade = q.get('trade_category', 'Unknown')
        if trade not in trade_questions:
            trade_questions[trade] = []
        trade_questions[trade].append(q)
    
    total_removed = 0
    
    for trade, questions_list in trade_questions.items():
        current_count = len(questions_list)
        
        if current_count <= 7:
            print(f"✅ {trade}: {current_count} questions (no reduction needed)")
            continue
            
        print(f"🔄 {trade}: {current_count} questions → reducing to 7")
        
        # Sort questions by difficulty and category for better selection
        # Keep a mix of Easy, Medium, Hard questions
        easy_questions = [q for q in questions_list if q.get('difficulty') == 'Easy']
        medium_questions = [q for q in questions_list if q.get('difficulty') == 'Medium']
        hard_questions = [q for q in questions_list if q.get('difficulty') == 'Hard']
        
        # Select 7 questions with good distribution
        selected_questions = []
        
        # Try to get 2 easy, 3 medium, 2 hard
        selected_questions.extend(random.sample(easy_questions, min(2, len(easy_questions))))
        selected_questions.extend(random.sample(medium_questions, min(3, len(medium_questions))))
        selected_questions.extend(random.sample(hard_questions, min(2, len(hard_questions))))
        
        # If we don't have enough, fill from remaining questions
        if len(selected_questions) < 7:
            remaining_questions = [q for q in questions_list if q not in selected_questions]
            needed = 7 - len(selected_questions)
            selected_questions.extend(random.sample(remaining_questions, min(needed, len(remaining_questions))))
        
        # If we have more than 7, trim to exactly 7
        selected_questions = selected_questions[:7]
        
        # Get IDs of questions to keep
        keep_ids = [q['id'] for q in selected_questions]
        
        # Delete questions not in the keep list
        delete_result = await db.skills_questions.delete_many({
            'trade_category': trade,
            'id': {'$nin': keep_ids}
        })
        
        removed_count = delete_result.deleted_count
        total_removed += removed_count
        
        print(f"   ✅ Kept 7 questions, removed {removed_count} questions")
        
        # Show difficulty distribution of kept questions
        kept_difficulties = [q.get('difficulty', 'Unknown') for q in selected_questions]
        difficulty_counts = {}
        for diff in kept_difficulties:
            difficulty_counts[diff] = difficulty_counts.get(diff, 0) + 1
        
        difficulty_str = ", ".join([f"{diff}: {count}" for diff, count in difficulty_counts.items()])
        print(f"   📊 Difficulty distribution: {difficulty_str}")
    
    print(f"\n🎯 Summary:")
    print(f"   • Total questions removed: {total_removed}")
    print(f"   • All trades now have ≤ 7 questions")
    
    # Verify final counts
    print(f"\n📋 Final Question Counts:")
    final_questions = await db.skills_questions.find({}).to_list(None)
    final_trade_counts = {}
    for q in final_questions:
        trade = q.get('trade_category', 'Unknown')
        final_trade_counts[trade] = final_trade_counts.get(trade, 0) + 1
    
    for trade, count in sorted(final_trade_counts.items()):
        print(f"   • {trade}: {count} questions")
    
    print(f"\n✅ Question reduction completed successfully!")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(reduce_questions_to_7())