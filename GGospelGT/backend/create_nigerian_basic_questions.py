#!/usr/bin/env python3
"""
Create Skills Assessment Questions for Nigerian Basic Trades

This script creates 7 questions each for the 10 essential Nigerian basic trades:
1. Generator Services
2. Air Conditioning & Refrigeration  
3. Welding
4. Carpentry
5. General Handyman Work
6. Roofing
7. Cleaning
8. Solar & Inverter Installation
9. Bathroom Fitting
10. Flooring

Each trade will get exactly 7 questions with a mix of Easy, Medium, and Hard difficulty levels.
"""

import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import uuid
from datetime import datetime

# Questions data for each trade
NIGERIAN_BASIC_TRADE_QUESTIONS = {
    "Generator Services": [
        {
            "question": "What is the recommended oil change interval for a petrol generator?",
            "options": ["Every 50 hours", "Every 100 hours", "Every 200 hours", "Every 500 hours"],
            "correct_answer": 1,
            "category": "Maintenance",
            "explanation": "Most petrol generators require oil changes every 100 hours of operation.",
            "difficulty": "Medium"
        },
        {
            "question": "Which fuel type is most commonly used for residential generators in Nigeria?",
            "options": ["Diesel", "Petrol", "Gas", "Kerosene"],
            "correct_answer": 1,
            "category": "Fuel Systems",
            "explanation": "Petrol is the most commonly used fuel for residential generators in Nigeria.",
            "difficulty": "Easy"
        },
        {
            "question": "What should you check first when a generator won't start?",
            "options": ["Spark plug", "Fuel level", "Air filter", "Oil level"],
            "correct_answer": 1,
            "category": "Troubleshooting",
            "explanation": "Always check fuel level first as it's the most common cause of starting problems.",
            "difficulty": "Easy"
        },
        {
            "question": "What is the purpose of an AVR in a generator?",
            "options": ["Control fuel flow", "Regulate voltage output", "Start the engine", "Cool the system"],
            "correct_answer": 1,
            "category": "Electrical Systems",
            "explanation": "AVR (Automatic Voltage Regulator) maintains stable voltage output.",
            "difficulty": "Hard"
        },
        {
            "question": "How often should you run a standby generator for maintenance?",
            "options": ["Daily", "Weekly", "Monthly", "Yearly"],
            "correct_answer": 2,
            "category": "Maintenance",
            "explanation": "Standby generators should be run monthly for 15-20 minutes to maintain proper operation.",
            "difficulty": "Medium"
        },
        {
            "question": "What size generator is typically needed for a 3-bedroom house in Nigeria?",
            "options": ["2.5KVA", "5KVA", "7.5KVA", "10KVA"],
            "correct_answer": 2,
            "category": "Sizing",
            "explanation": "A 7.5KVA generator typically handles the load of a 3-bedroom house with basic appliances.",
            "difficulty": "Medium"
        },
        {
            "question": "Which component converts mechanical energy to electrical energy in a generator?",
            "options": ["Engine", "Alternator", "Fuel tank", "Control panel"],
            "correct_answer": 1,
            "category": "Components",
            "explanation": "The alternator converts the mechanical energy from the engine into electrical energy.",
            "difficulty": "Hard"
        }
    ],
    
    "Air Conditioning & Refrigeration": [
        {
            "question": "What refrigerant is commonly used in modern split AC units?",
            "options": ["R-22", "R-410A", "R-134a", "R-12"],
            "correct_answer": 1,
            "category": "Refrigerants",
            "explanation": "R-410A is the standard refrigerant for modern split AC systems.",
            "difficulty": "Medium"
        },
        {
            "question": "How often should AC filters be cleaned in dusty Nigerian conditions?",
            "options": ["Weekly", "Monthly", "Every 3 months", "Every 6 months"],
            "correct_answer": 1,
            "category": "Maintenance",
            "explanation": "In dusty conditions, AC filters should be cleaned monthly for optimal performance.",
            "difficulty": "Easy"
        },
        {
            "question": "What is the ideal temperature setting for energy efficiency in Nigerian climate?",
            "options": ["18°C", "20°C", "24°C", "26°C"],
            "correct_answer": 2,
            "category": "Energy Efficiency",
            "explanation": "24°C provides good comfort while maintaining energy efficiency in tropical climates.",
            "difficulty": "Easy"
        },
        {
            "question": "What causes ice formation on AC evaporator coils?",
            "options": ["High refrigerant", "Dirty filters", "Low voltage", "High temperature"],
            "correct_answer": 1,
            "category": "Troubleshooting",
            "explanation": "Dirty filters restrict airflow, causing the evaporator coils to freeze.",
            "difficulty": "Medium"
        },
        {
            "question": "Which tool is essential for checking refrigerant pressure?",
            "options": ["Multimeter", "Manifold gauge", "Thermometer", "Vacuum pump"],
            "correct_answer": 1,
            "category": "Tools",
            "explanation": "Manifold gauges are used to measure refrigerant pressures in AC systems.",
            "difficulty": "Hard"
        },
        {
            "question": "What is the main function of the condenser in an AC system?",
            "options": ["Cool the air", "Remove heat", "Filter air", "Control humidity"],
            "correct_answer": 1,
            "category": "Components",
            "explanation": "The condenser removes heat from the refrigerant, releasing it outside.",
            "difficulty": "Medium"
        },
        {
            "question": "What voltage is standard for residential AC units in Nigeria?",
            "options": ["110V", "220V", "240V", "415V"],
            "correct_answer": 1,
            "category": "Electrical",
            "explanation": "220V is the standard voltage for residential AC units in Nigeria.",
            "difficulty": "Hard"
        }
    ],
    
    "Welding": [
        {
            "question": "Which welding process is most common for general steel work?",
            "options": ["TIG", "MIG", "Arc welding", "Gas welding"],
            "correct_answer": 2,
            "category": "Processes",
            "explanation": "Arc welding (SMAW) is the most common process for general steel fabrication.",
            "difficulty": "Easy"
        },
        {
            "question": "What electrode size is typically used for 6mm steel plate?",
            "options": ["2.5mm", "3.2mm", "4.0mm", "5.0mm"],
            "correct_answer": 1,
            "category": "Electrodes",
            "explanation": "3.2mm electrodes are commonly used for welding 6mm steel plates.",
            "difficulty": "Medium"
        },
        {
            "question": "What safety equipment is most critical when welding?",
            "options": ["Gloves", "Welding helmet", "Apron", "Safety boots"],
            "correct_answer": 1,
            "category": "Safety",
            "explanation": "Welding helmet protects eyes and face from harmful UV radiation and sparks.",
            "difficulty": "Easy"
        },
        {
            "question": "What causes porosity in welded joints?",
            "options": ["High current", "Moisture", "Fast travel", "Thick material"],
            "correct_answer": 1,
            "category": "Defects",
            "explanation": "Moisture in electrodes or base metal causes gas bubbles (porosity) in welds.",
            "difficulty": "Hard"
        },
        {
            "question": "Which position is easiest for beginners to learn welding?",
            "options": ["Flat", "Horizontal", "Vertical", "Overhead"],
            "correct_answer": 0,
            "category": "Positions",
            "explanation": "Flat position welding is easiest as gravity helps with puddle control.",
            "difficulty": "Easy"
        },
        {
            "question": "What is the purpose of flux in welding electrodes?",
            "options": ["Increase heat", "Protect weld pool", "Add strength", "Speed up welding"],
            "correct_answer": 1,
            "category": "Materials",
            "explanation": "Flux protects the weld pool from atmospheric contamination.",
            "difficulty": "Medium"
        },
        {
            "question": "What amperage range is suitable for 3.2mm electrodes?",
            "options": ["60-80A", "90-120A", "130-160A", "170-200A"],
            "correct_answer": 1,
            "category": "Settings",
            "explanation": "3.2mm electrodes typically require 90-120 amperes for proper penetration.",
            "difficulty": "Hard"
        }
    ],
    
    "Carpentry": [
        {
            "question": "Which wood is commonly used for furniture making in Nigeria?",
            "options": ["Pine", "Mahogany", "Oak", "Teak"],
            "correct_answer": 1,
            "category": "Materials",
            "explanation": "Mahogany is widely available and commonly used for furniture in Nigeria.",
            "difficulty": "Easy"
        },
        {
            "question": "What is the standard thickness for plywood used in cabinet making?",
            "options": ["12mm", "15mm", "18mm", "25mm"],
            "correct_answer": 2,
            "category": "Materials",
            "explanation": "18mm plywood provides good strength and is standard for cabinet construction.",
            "difficulty": "Medium"
        },
        {
            "question": "Which joint is strongest for corner connections?",
            "options": ["Butt joint", "Mortise and tenon", "Lap joint", "Dado joint"],
            "correct_answer": 1,
            "category": "Joinery",
            "explanation": "Mortise and tenon joints provide the strongest corner connections.",
            "difficulty": "Hard"
        },
        {
            "question": "What tool is essential for checking if surfaces are level?",
            "options": ["Ruler", "Spirit level", "Square", "Compass"],
            "correct_answer": 1,
            "category": "Tools",
            "explanation": "Spirit level is essential for checking if surfaces are perfectly horizontal or vertical.",
            "difficulty": "Easy"
        },
        {
            "question": "What grit sandpaper should be used for final finishing?",
            "options": ["80 grit", "120 grit", "220 grit", "320 grit"],
            "correct_answer": 2,
            "category": "Finishing",
            "explanation": "220 grit sandpaper provides a smooth finish suitable for final sanding before staining.",
            "difficulty": "Medium"
        },
        {
            "question": "Which saw is best for making curved cuts?",
            "options": ["Circular saw", "Jigsaw", "Hand saw", "Miter saw"],
            "correct_answer": 1,
            "category": "Tools",
            "explanation": "Jigsaw is specifically designed for making curved and intricate cuts.",
            "difficulty": "Easy"
        },
        {
            "question": "What is the purpose of wood glue in joinery?",
            "options": ["Fill gaps", "Bond joints", "Seal wood", "Add color"],
            "correct_answer": 1,
            "category": "Adhesives",
            "explanation": "Wood glue creates strong bonds between wood pieces in joints.",
            "difficulty": "Medium"
        }
    ],
    
    "General Handyman Work": [
        {
            "question": "Which tool is most versatile for a handyman?",
            "options": ["Hammer", "Screwdriver set", "Drill", "Pliers"],
            "correct_answer": 2,
            "category": "Tools",
            "explanation": "A drill can be used for drilling, driving screws, and with attachments for many tasks.",
            "difficulty": "Easy"
        },
        {
            "question": "What should you check first when a door won't close properly?",
            "options": ["Hinges", "Door frame", "Lock", "Door handle"],
            "correct_answer": 0,
            "category": "Troubleshooting",
            "explanation": "Loose or misaligned hinges are the most common cause of door closing problems.",
            "difficulty": "Easy"
        },
        {
            "question": "Which adhesive is best for fixing loose tiles?",
            "options": ["Super glue", "Tile adhesive", "Wood glue", "Silicone"],
            "correct_answer": 1,
            "category": "Materials",
            "explanation": "Tile adhesive is specifically formulated for bonding tiles to surfaces.",
            "difficulty": "Medium"
        },
        {
            "question": "What causes paint to peel off walls?",
            "options": ["Poor quality paint", "Moisture", "Wrong color", "Thick application"],
            "correct_answer": 1,
            "category": "Troubleshooting",
            "explanation": "Moisture is the primary cause of paint peeling from walls.",
            "difficulty": "Medium"
        },
        {
            "question": "Which screw type is best for drywall installation?",
            "options": ["Wood screws", "Drywall screws", "Machine screws", "Self-tapping screws"],
            "correct_answer": 1,
            "category": "Fasteners",
            "explanation": "Drywall screws are specifically designed for attaching drywall to studs.",
            "difficulty": "Hard"
        },
        {
            "question": "What is the standard height for electrical switches in Nigeria?",
            "options": ["1.0m", "1.2m", "1.4m", "1.6m"],
            "correct_answer": 1,
            "category": "Standards",
            "explanation": "1.2m is the standard height for electrical switches in Nigerian buildings.",
            "difficulty": "Hard"
        },
        {
            "question": "Which sealant is best for bathroom applications?",
            "options": ["Acrylic", "Silicone", "Polyurethane", "Latex"],
            "correct_answer": 1,
            "category": "Materials",
            "explanation": "Silicone sealant is waterproof and flexible, ideal for bathroom use.",
            "difficulty": "Easy"
        }
    ],
    
    "Roofing": [
        {
            "question": "Which roofing material is most popular in Nigeria?",
            "options": ["Clay tiles", "Aluminum sheets", "Concrete tiles", "Thatch"],
            "correct_answer": 1,
            "category": "Materials",
            "explanation": "Aluminum roofing sheets are widely used due to durability and cost-effectiveness.",
            "difficulty": "Easy"
        },
        {
            "question": "What is the minimum roof slope for aluminum sheets?",
            "options": ["5 degrees", "10 degrees", "15 degrees", "20 degrees"],
            "correct_answer": 1,
            "category": "Installation",
            "explanation": "10 degrees minimum slope ensures proper water drainage for aluminum sheets.",
            "difficulty": "Medium"
        },
        {
            "question": "Which gauge aluminum sheet is standard for residential roofing?",
            "options": ["0.4mm", "0.5mm", "0.6mm", "0.8mm"],
            "correct_answer": 1,
            "category": "Materials",
            "explanation": "0.5mm gauge aluminum sheets provide good balance of strength and cost for residential use.",
            "difficulty": "Hard"
        },
        {
            "question": "What causes roof leaks most commonly?",
            "options": ["Poor materials", "Damaged flashing", "Wrong slope", "Heavy rain"],
            "correct_answer": 1,
            "category": "Troubleshooting",
            "explanation": "Damaged or improperly installed flashing around roof penetrations causes most leaks.",
            "difficulty": "Medium"
        },
        {
            "question": "How should roof sheets be overlapped?",
            "options": ["End to end", "One corrugation", "Two corrugations", "Three corrugations"],
            "correct_answer": 1,
            "category": "Installation",
            "explanation": "One corrugation overlap provides adequate weather protection for roof sheets.",
            "difficulty": "Easy"
        },
        {
            "question": "What is the purpose of roof battens?",
            "options": ["Support sheets", "Insulation", "Ventilation", "Decoration"],
            "correct_answer": 0,
            "category": "Components",
            "explanation": "Roof battens provide structural support for roofing sheets.",
            "difficulty": "Easy"
        },
        {
            "question": "Which fastener is best for aluminum roofing sheets?",
            "options": ["Nails", "Screws with washers", "Bolts", "Clips"],
            "correct_answer": 1,
            "category": "Fasteners",
            "explanation": "Self-drilling screws with rubber washers provide secure, weatherproof attachment.",
            "difficulty": "Hard"
        }
    ],
    
    "Cleaning": [
        {
            "question": "Which cleaning agent is best for removing grease?",
            "options": ["Bleach", "Ammonia", "Degreaser", "Vinegar"],
            "correct_answer": 2,
            "category": "Chemicals",
            "explanation": "Degreasers are specifically formulated to break down and remove grease.",
            "difficulty": "Easy"
        },
        {
            "question": "What is the proper dilution ratio for most household bleach?",
            "options": ["1:5", "1:10", "1:20", "1:50"],
            "correct_answer": 1,
            "category": "Chemicals",
            "explanation": "1:10 dilution (1 part bleach to 10 parts water) is standard for disinfection.",
            "difficulty": "Medium"
        },
        {
            "question": "Which material should never be mixed with bleach?",
            "options": ["Water", "Soap", "Ammonia", "Detergent"],
            "correct_answer": 2,
            "category": "Safety",
            "explanation": "Mixing bleach with ammonia creates toxic chloramine gas.",
            "difficulty": "Hard"
        },
        {
            "question": "What is the best way to clean glass surfaces?",
            "options": ["Circular motions", "Horizontal then vertical", "Vertical only", "Random pattern"],
            "correct_answer": 1,
            "category": "Techniques",
            "explanation": "Horizontal then vertical strokes prevent streaking on glass surfaces.",
            "difficulty": "Easy"
        },
        {
            "question": "Which tool is most effective for removing dust from high places?",
            "options": ["Cloth", "Vacuum", "Feather duster", "Microfiber duster"],
            "correct_answer": 3,
            "category": "Tools",
            "explanation": "Microfiber dusters trap dust effectively and are safe for delicate surfaces.",
            "difficulty": "Medium"
        },
        {
            "question": "How often should cleaning cloths be replaced?",
            "options": ["Daily", "Weekly", "Monthly", "When visibly dirty"],
            "correct_answer": 3,
            "category": "Hygiene",
            "explanation": "Cleaning cloths should be replaced when visibly dirty or smelly to maintain hygiene.",
            "difficulty": "Easy"
        },
        {
            "question": "What is the correct order for cleaning a room?",
            "options": ["Floor first", "Top to bottom", "Bottom to top", "Random order"],
            "correct_answer": 1,
            "category": "Procedures",
            "explanation": "Top to bottom cleaning prevents dust and debris from falling on already cleaned surfaces.",
            "difficulty": "Medium"
        }
    ],
    
    "Solar & Inverter Installation": [
        {
            "question": "What is the typical voltage output of a solar panel?",
            "options": ["12V", "24V", "36V", "48V"],
            "correct_answer": 2,
            "category": "Components",
            "explanation": "Most residential solar panels output around 36V under standard conditions.",
            "difficulty": "Medium"
        },
        {
            "question": "Which battery type is best for solar systems?",
            "options": ["Car battery", "Deep cycle", "Motorcycle battery", "UPS battery"],
            "correct_answer": 1,
            "category": "Batteries",
            "explanation": "Deep cycle batteries are designed for repeated discharge/charge cycles in solar systems.",
            "difficulty": "Easy"
        },
        {
            "question": "What is the purpose of a charge controller?",
            "options": ["Convert DC to AC", "Regulate charging", "Store energy", "Monitor usage"],
            "correct_answer": 1,
            "category": "Components",
            "explanation": "Charge controllers regulate the voltage and current from solar panels to batteries.",
            "difficulty": "Hard"
        },
        {
            "question": "Which direction should solar panels face in Nigeria?",
            "options": ["North", "South", "East", "West"],
            "correct_answer": 1,
            "category": "Installation",
            "explanation": "Solar panels should face south for maximum sun exposure in Nigeria.",
            "difficulty": "Easy"
        },
        {
            "question": "What is the ideal tilt angle for solar panels in Nigeria?",
            "options": ["0 degrees", "10 degrees", "15 degrees", "30 degrees"],
            "correct_answer": 2,
            "category": "Installation",
            "explanation": "15 degrees tilt angle is optimal for Nigeria's latitude for year-round performance.",
            "difficulty": "Hard"
        },
        {
            "question": "Which inverter type is most efficient?",
            "options": ["Modified sine wave", "Pure sine wave", "Square wave", "Stepped wave"],
            "correct_answer": 1,
            "category": "Inverters",
            "explanation": "Pure sine wave inverters are most efficient and compatible with all appliances.",
            "difficulty": "Medium"
        },
        {
            "question": "What safety equipment is essential during solar installation?",
            "options": ["Gloves", "Safety harness", "Hard hat", "All of the above"],
            "correct_answer": 3,
            "category": "Safety",
            "explanation": "All safety equipment is essential when working at height during solar installation.",
            "difficulty": "Easy"
        }
    ],
    
    "Bathroom Fitting": [
        {
            "question": "What is the standard height for a bathroom sink?",
            "options": ["750mm", "850mm", "950mm", "1050mm"],
            "correct_answer": 1,
            "category": "Standards",
            "explanation": "850mm is the standard height for bathroom sinks for comfortable use.",
            "difficulty": "Medium"
        },
        {
            "question": "Which sealant is best for around bathtubs?",
            "options": ["Acrylic", "Silicone", "Polyurethane", "Latex"],
            "correct_answer": 1,
            "category": "Materials",
            "explanation": "Silicone sealant is waterproof and flexible, ideal for bathtub sealing.",
            "difficulty": "Easy"
        },
        {
            "question": "What causes low water pressure in showers?",
            "options": ["Blocked showerhead", "Faulty pump", "Pipe blockage", "All of the above"],
            "correct_answer": 3,
            "category": "Troubleshooting",
            "explanation": "All these factors can cause low water pressure in showers.",
            "difficulty": "Medium"
        },
        {
            "question": "Which pipe material is best for bathroom plumbing?",
            "options": ["PVC", "Copper", "Steel", "Aluminum"],
            "correct_answer": 0,
            "category": "Materials",
            "explanation": "PVC pipes are corrosion-resistant and ideal for bathroom plumbing.",
            "difficulty": "Easy"
        },
        {
            "question": "What is the minimum slope for bathroom floor drainage?",
            "options": ["1%", "2%", "3%", "5%"],
            "correct_answer": 1,
            "category": "Installation",
            "explanation": "2% slope ensures proper drainage while maintaining comfortable walking surface.",
            "difficulty": "Hard"
        },
        {
            "question": "Which tool is essential for cutting ceramic tiles?",
            "options": ["Hacksaw", "Tile cutter", "Chisel", "Grinder"],
            "correct_answer": 1,
            "category": "Tools",
            "explanation": "Tile cutters provide clean, precise cuts for ceramic tiles.",
            "difficulty": "Easy"
        },
        {
            "question": "What causes toilet to keep running?",
            "options": ["Faulty flapper", "Broken chain", "Warped flapper seat", "All of the above"],
            "correct_answer": 3,
            "category": "Troubleshooting",
            "explanation": "All these issues can cause a toilet to keep running continuously.",
            "difficulty": "Hard"
        }
    ],
    
    "Flooring": [
        {
            "question": "Which flooring is most suitable for Nigerian climate?",
            "options": ["Carpet", "Ceramic tiles", "Hardwood", "Vinyl"],
            "correct_answer": 1,
            "category": "Materials",
            "explanation": "Ceramic tiles are durable, easy to clean, and suitable for tropical climate.",
            "difficulty": "Easy"
        },
        {
            "question": "What is the standard thickness for floor tiles?",
            "options": ["8mm", "10mm", "12mm", "15mm"],
            "correct_answer": 1,
            "category": "Materials",
            "explanation": "10mm thickness provides good durability for residential floor tiles.",
            "difficulty": "Medium"
        },
        {
            "question": "Which adhesive is best for ceramic floor tiles?",
            "options": ["Cement-based", "Epoxy", "Acrylic", "Silicone"],
            "correct_answer": 0,
            "category": "Installation",
            "explanation": "Cement-based adhesives provide strong, durable bonds for ceramic tiles.",
            "difficulty": "Easy"
        },
        {
            "question": "What tool is used to ensure tiles are level?",
            "options": ["Ruler", "Spirit level", "Square", "Trowel"],
            "correct_answer": 1,
            "category": "Tools",
            "explanation": "Spirit level ensures tiles are installed perfectly level.",
            "difficulty": "Easy"
        },
        {
            "question": "What is the purpose of tile spacers?",
            "options": ["Support tiles", "Create uniform gaps", "Level tiles", "Cut tiles"],
            "correct_answer": 1,
            "category": "Installation",
            "explanation": "Tile spacers ensure uniform gaps between tiles for grouting.",
            "difficulty": "Medium"
        },
        {
            "question": "How long should tile adhesive cure before grouting?",
            "options": ["2 hours", "12 hours", "24 hours", "48 hours"],
            "correct_answer": 2,
            "category": "Installation",
            "explanation": "24 hours allows tile adhesive to fully cure before applying grout.",
            "difficulty": "Hard"
        },
        {
            "question": "Which grout type is best for floor tiles?",
            "options": ["Sanded", "Unsanded", "Epoxy", "Acrylic"],
            "correct_answer": 0,
            "category": "Materials",
            "explanation": "Sanded grout is stronger and better for floor tile joints wider than 3mm.",
            "difficulty": "Hard"
        }
    ]
}

async def create_nigerian_basic_questions():
    """Create 7 questions for each Nigerian basic trade"""
    load_dotenv()
    
    client = AsyncIOMotorClient(os.getenv('MONGO_URL'))
    db = client[os.getenv('DB_NAME')]
    
    print("🇳🇬 Creating Skills Assessment Questions for Nigerian Basic Trades")
    print("=" * 70)
    
    total_created = 0
    
    for trade_category, questions_data in NIGERIAN_BASIC_TRADE_QUESTIONS.items():
        print(f"\n📝 Creating questions for: {trade_category}")
        
        # Check if questions already exist
        existing_count = await db.skills_questions.count_documents({"trade_category": trade_category})
        if existing_count > 0:
            print(f"   ⚠️  {existing_count} questions already exist - skipping")
            continue
        
        created_count = 0
        for question_data in questions_data:
            # Create question document
            question_doc = {
                "id": str(uuid.uuid4()),
                "trade_category": trade_category,
                "question": question_data["question"],
                "options": question_data["options"],
                "correct_answer": question_data["correct_answer"],
                "category": question_data["category"],
                "explanation": question_data["explanation"],
                "difficulty": question_data["difficulty"],
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
                "created_by": "admin",
                "is_active": True
            }
            
            # Insert question
            await db.skills_questions.insert_one(question_doc)
            created_count += 1
        
        print(f"   ✅ Created {created_count} questions")
        total_created += created_count
    
    print(f"\n🎯 Summary:")
    print(f"   • Total questions created: {total_created}")
    print(f"   • Trades covered: {len(NIGERIAN_BASIC_TRADE_QUESTIONS)}")
    
    # Verify final state
    print(f"\n📊 Final Question Counts:")
    all_questions = await db.skills_questions.find({}).to_list(None)
    trade_counts = {}
    for q in all_questions:
        trade = q.get('trade_category', 'Unknown')
        trade_counts[trade] = trade_counts.get(trade, 0) + 1
    
    for trade, count in sorted(trade_counts.items()):
        print(f"   • {trade}: {count} questions")
    
    print(f"\n✅ Nigerian basic trade questions created successfully!")
    print(f"   Total trades with questions: {len(trade_counts)}")
    print(f"   Total questions in system: {sum(trade_counts.values())}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(create_nigerian_basic_questions())