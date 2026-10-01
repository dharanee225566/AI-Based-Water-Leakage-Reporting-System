import sqlite3
import os
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from config import Config
from database import get_db_connection, init_db
from models.ai_engine import ai_engine

def seed_database():
    """Initializes tables and populates comprehensive realistic demonstration data."""
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()

    # Clear existing data for clean seed
    cursor.execute("DELETE FROM ai_corrections")
    cursor.execute("DELETE FROM status_history")
    cursor.execute("DELETE FROM assignments")
    cursor.execute("DELETE FROM complaints")
    cursor.execute("DELETE FROM staff_profiles")
    cursor.execute("DELETE FROM users")
    conn.commit()

    print("Seeding Users...")
    users_data = [
        # Admins
        ("Dr. Aris Thorne", "admin@aquawatch.org", generate_password_hash("admin123"), "+91 98450 11001", "admin"),
        # Staff
        ("David Miller", "david.crew@aquawatch.org", generate_password_hash("staff123"), "+91 98450 22001", "staff"),
        ("Elena Rostova", "elena.field@aquawatch.org", generate_password_hash("staff123"), "+91 98450 22002", "staff"),
        ("Marcus Chen", "marcus.tech@aquawatch.org", generate_password_hash("staff123"), "+91 98450 22003", "staff"),
        # Citizens
        ("Sophia Anderson", "sophia.citizen@gmail.com", generate_password_hash("user123"), "+91 98450 33001", "citizen"),
        ("Rahul Sharma", "rahul.citizen@gmail.com", generate_password_hash("user123"), "+91 98450 33002", "citizen"),
        ("Carlos Mendes", "carlos.citizen@gmail.com", generate_password_hash("user123"), "+91 98450 33003", "citizen"),
    ]

    cursor.executemany(
        "INSERT INTO users (full_name, email, password_hash, phone, role) VALUES (?, ?, ?, ?, ?)",
        users_data
    )
    conn.commit()

    # Retrieve User IDs
    cursor.execute("SELECT id, email FROM users")
    user_map = {row['email']: row['id'] for row in cursor.fetchall()}

    admin_id = user_map["admin@aquawatch.org"]
    david_id = user_map["david.crew@aquawatch.org"]
    elena_id = user_map["elena.field@aquawatch.org"]
    marcus_id = user_map["marcus.tech@aquawatch.org"]
    sophia_id = user_map["sophia.citizen@gmail.com"]
    rahul_id = user_map["rahul.citizen@gmail.com"]
    carlos_id = user_map["carlos.citizen@gmail.com"]

    print("Seeding Staff Profiles...")
    staff_profiles_data = [
        (david_id, "Emergency Main Pipeline & Heavy Pressure Conduits", "Zone A - Central Metro", "Available"),
        (elena_id, "Sewage Cross-Contamination & Water Quality Testing", "Zone B - North Sector", "On Field"),
        (marcus_id, "Smart Water Meters, Valves & Standposts", "Zone C - South Commercial", "Available"),
    ]
    cursor.executemany(
        "INSERT INTO staff_profiles (user_id, specialty, zone, status) VALUES (?, ?, ?, ?)",
        staff_profiles_data
    )
    conn.commit()

    now = datetime.now()

    # 15 Detailed Realistic Complaints
    raw_complaints = [
        {
            "cid": "AQUA-2026-1001",
            "uid": sophia_id,
            "title": "Catastrophic main transmission conduit burst flooding roadway",
            "street": "MG Road Underpass, Near Trinity Circle",
            "landmark": "Opposite Metro Pillar 142",
            "lat": 12.9738, "lng": 77.6190,
            "category": "Main Pipeline Burst",
            "severity": 5,
            "desc": "Massive high-pressure water geyser erupting 15 feet high through the asphalt on the underpass. Immense volume of water is flowing into the road and vehicles are stalling. Substantial erosion of pavement seen.",
            "photo": "main_burst.svg",
            "status": "In Progress",
            "staff": david_id,
            "days_ago": 1,
            "hours_ago": 6
        },
        {
            "cid": "AQUA-2026-1002",
            "uid": rahul_id,
            "title": "Subterranean supply pipe cracked under pedestrian sidewalk",
            "street": "100 Feet Road, Indiranagar",
            "landmark": "Near 12th Main Crossroad, Cafe Corner",
            "lat": 12.9712, "lng": 77.6415,
            "category": "Pipe Leakage",
            "severity": 3,
            "desc": "Water is leaking from an underground supply pipe under the sidewalk. Pavement stones are wet and clean potable drinking water is trickling steadily into the gutter non-stop.",
            "photo": "pipe_leak.svg",
            "status": "Assigned",
            "staff": david_id,
            "days_ago": 2,
            "hours_ago": 14
        },
        {
            "cid": "AQUA-2026-1003",
            "uid": carlos_id,
            "title": "Pungent black sewage overflow mixing with drinking line",
            "street": "CMH Road, Halasuru",
            "landmark": "Behind Municipal Market Complex",
            "lat": 12.9792, "lng": 77.6275,
            "category": "Sewage & Contamination",
            "severity": 5,
            "desc": "Foul-smelling black sewage water mixing with clean municipal tap water network. Terrible stench in the alleyway and residents are getting brownish contaminated water from their connections. Immediate health hazard.",
            "photo": "sewage_contamination.svg",
            "status": "Pending",
            "staff": None,
            "days_ago": 0,
            "hours_ago": 3
        },
        {
            "cid": "AQUA-2026-1004",
            "uid": sophia_id,
            "title": "Broken public drinking water tap dripping continuously",
            "street": "KBS Majestic Bus Stand",
            "landmark": "Platform 4 Passenger Waiting Shed",
            "lat": 12.9774, "lng": 77.5714,
            "category": "Tap Leakage",
            "severity": 2,
            "desc": "Community standpost tap washer is worn out and the tap knob cannot be turned off. Continuous heavy drip wasting clean treated drinking water day and night.",
            "photo": "tap_leak.svg",
            "status": "Resolved",
            "staff": marcus_id,
            "days_ago": 5,
            "hours_ago": 48
        },
        {
            "cid": "AQUA-2026-1005",
            "uid": rahul_id,
            "title": "Bulk commercial water meter housing cracked and spurting",
            "street": "Outer Ring Road, Bellandur Junction",
            "landmark": "EcoSpace Technology Park Entrance Gate 2",
            "lat": 12.9260, "lng": 77.6762,
            "category": "Other / Meter",
            "severity": 3,
            "desc": "Commercial water meter box is overflowing and filling with water. Meter dial spinning rapidly and the flange connector is spraying a steady stream across the utility trench.",
            "photo": "meter_leak.svg",
            "status": "In Progress",
            "staff": marcus_id,
            "days_ago": 2,
            "hours_ago": 20
        },
        {
            "cid": "AQUA-2026-1006",
            "uid": carlos_id,
            "title": "Severe road waterlogging and overflow submerging street lanes",
            "street": "Koramangala 80 Feet Road",
            "landmark": "Near 4th Block Signal Junction",
            "lat": 12.9352, "lng": 77.6245,
            "category": "Road Flooding",
            "severity": 4,
            "desc": "Severe water accumulation on the main road causing heavy traffic jam. Street submerged in knee-deep water due to massive pipeline overflow from storm drain culvert. Two-wheelers unable to pass.",
            "photo": "road_flood.svg",
            "status": "Assigned",
            "staff": elena_id,
            "days_ago": 1,
            "hours_ago": 18
        },
        {
            "cid": "AQUA-2026-1007",
            "uid": sophia_id,
            "title": "Park drinking fountain tap stuck open",
            "street": "Cubbon Park Avenue",
            "landmark": "Near Bandstand Garden Walking Track",
            "lat": 12.9763, "lng": 77.5929,
            "category": "Tap Leakage",
            "severity": 1,
            "desc": "Park drinking tap is stuck open and dripping heavily. Water spilling onto the grass lawn continuously.",
            "photo": "tap_leak.svg",
            "status": "Pending",
            "staff": None,
            "days_ago": 0,
            "hours_ago": 7
        },
        {
            "cid": "AQUA-2026-1008",
            "uid": rahul_id,
            "title": "Underground distribution pipe leak wetting pavement",
            "street": "Church Street",
            "landmark": "Near Museum Road Crossing",
            "lat": 12.9749, "lng": 77.6062,
            "category": "Pipe Leakage",
            "severity": 3,
            "desc": "Underground distribution pipe has a steady leak wetting the pavement. Water seeping through sidewalk tiles from broken municipal supply line.",
            "photo": "pipe_leak.svg",
            "status": "Resolved",
            "staff": david_id,
            "days_ago": 7,
            "hours_ago": 120
        },
        {
            "cid": "AQUA-2026-1009",
            "uid": carlos_id,
            "title": "Feeder line rupture spraying high pressure water jet",
            "street": "Brigade Road Commercial Hub",
            "landmark": "Near Opera House Junction",
            "lat": 12.9719, "lng": 77.6070,
            "category": "Main Pipeline Burst",
            "severity": 5,
            "desc": "Ruptured high pressure transmission line gushing thousands of liters per minute onto the road. Clean water geyser shooting upward, traffic diverted.",
            "photo": "main_burst.svg",
            "status": "Resolved",
            "staff": david_id,
            "days_ago": 9,
            "hours_ago": 180
        },
        {
            "cid": "AQUA-2026-1010",
            "uid": sophia_id,
            "title": "Drainage runoff infiltrating drinking water valve chamber",
            "street": "Malleshwaram 8th Cross",
            "landmark": "Near Canara Union Circle",
            "lat": 12.9984, "lng": 77.5711,
            "category": "Sewage & Contamination",
            "severity": 4,
            "desc": "Underground sewage line broken and leaking near clean water supply valve chamber. Odor of contaminated water detectable at nearby residential taps.",
            "photo": "sewage_contamination.svg",
            "status": "In Progress",
            "staff": elena_id,
            "days_ago": 3,
            "hours_ago": 30
        },
        {
            "cid": "AQUA-2026-1011",
            "uid": carlos_id,
            "title": "Water gushing on MG Road underpass near Trinity",
            "street": "MG Road Underpass",
            "landmark": "Trinity Circle Metro",
            "lat": 12.9739, "lng": 77.6192,
            "category": "Main Pipeline Burst",
            "severity": 5,
            "desc": "Huge water geyser erupting from underpass roadway, traffic completely blocked with heavy gushing torrent.",
            "photo": "main_burst.svg",
            "status": "Pending",
            "staff": None,
            "days_ago": 0,
            "hours_ago": 4,
            "is_duplicate_of": "AQUA-2026-1001",
            "duplicate_score": 92.4
        },
        {
            "cid": "AQUA-2026-1012",
            "uid": rahul_id,
            "title": "Utility water meter chamber flooded with clear water",
            "street": "Residency Road",
            "landmark": "Near Richmond Circle Flyover",
            "lat": 12.9663, "lng": 77.5997,
            "category": "Other / Meter",
            "severity": 2,
            "desc": "Water utility valve chamber flooded with clear water, cover displaced and water meter spinning slowly.",
            "photo": "meter_leak.svg",
            "status": "Pending",
            "staff": None,
            "days_ago": 1,
            "hours_ago": 12
        },
        {
            "cid": "AQUA-2026-1013",
            "uid": sophia_id,
            "title": "Water supply pipe hairline crack in front of house gate",
            "street": "Jayanagar 4th Block",
            "landmark": "Near BDA Shopping Complex",
            "lat": 12.9299, "lng": 77.5833,
            "category": "Pipe Leakage",
            "severity": 3,
            "desc": "Joint connecting the main line to home service connection is spraying water onto the pedestrian footpath. Clean water pooling continuously.",
            "photo": "pipe_leak.svg",
            "status": "In Progress",
            "staff": david_id,
            "days_ago": 2,
            "hours_ago": 28
        },
        {
            "cid": "AQUA-2026-1014",
            "uid": carlos_id,
            "title": "Excessive water overflow ponding across crossroad",
            "street": "Old Airport Road, Kodihalli",
            "landmark": "Near Leela Palace Signal",
            "lat": 12.9601, "lng": 77.6483,
            "category": "Road Flooding",
            "severity": 3,
            "desc": "Large pool of water covering both lanes of the highway intersection due to broken storm line culvert. Pedestrian crossing impassable.",
            "photo": "road_flood.svg",
            "status": "Pending",
            "staff": None,
            "days_ago": 0,
            "hours_ago": 9
        },
        {
            "cid": "AQUA-2026-1015",
            "uid": rahul_id,
            "title": "Damaged brass tap leaking at community water post",
            "street": "Shivajinagar Bus Depot",
            "landmark": "Near Russell Market Entrance",
            "lat": 12.9856, "lng": 77.6048,
            "category": "Tap Leakage",
            "severity": 2,
            "desc": "Public tap washer worn out, steady stream of water running down gutter at roadside public water post.",
            "photo": "tap_leak.svg",
            "status": "Resolved",
            "staff": marcus_id,
            "days_ago": 8,
            "hours_ago": 150
        }
    ]

    print("Seeding Complaints, AI Predictions, and Timeline History...")
    for item in raw_complaints:
        # Run through AI Engine for consistent ML inference
        ai_cls = ai_engine.classify_complaint(item["desc"])
        ai_prio = ai_engine.recommend_priority(item["category"], item["desc"], item["severity"])
        ai_summary = ai_engine.generate_field_summary(
            item["title"], item["category"], item["desc"], item["street"], ai_prio["priority"]
        )

        created_dt = now - timedelta(days=item.get("days_ago", 0), hours=item.get("hours_ago", 0))
        created_str = created_dt.strftime("%Y-%m-%d %H:%M:%S")
        updated_str = (created_dt + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute('''
            INSERT INTO complaints (
                complaint_id, user_id, title, street_name, landmark,
                latitude, longitude, category, ai_predicted_category, ai_confidence,
                priority, ai_priority_score, user_severity, description,
                ai_field_summary, photo_path, status, is_duplicate_of,
                duplicate_score, estimated_loss_lph, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            item["cid"],
            item["uid"],
            item["title"],
            item["street"],
            item["landmark"],
            item["lat"],
            item["lng"],
            item["category"],
            ai_cls["category"],
            ai_cls["confidence"],
            ai_prio["priority"],
            ai_prio["score"],
            item["severity"],
            item["desc"],
            ai_summary,
            item["photo"],
            item["status"],
            item.get("is_duplicate_of"),
            item.get("duplicate_score", 0.0),
            ai_prio["estimated_loss_lph"],
            created_str,
            updated_str
        ))

        # Status History Timeline
        # 1. Submission
        cursor.execute('''
            INSERT INTO status_history (complaint_id, changed_by, old_status, new_status, comment, timestamp)
            VALUES (?, ?, NULL, 'Pending', 'Citizen reported water leakage incident via AquaWatch Portal.', ?)
        ''', (item["cid"], item["uid"], created_str))

        # 2. AI Triage Event
        triage_time = (created_dt + timedelta(minutes=2)).strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO status_history (complaint_id, changed_by, old_status, new_status, comment, timestamp)
            VALUES (?, NULL, 'Pending', 'Pending', ?, ?)
        ''', (
            item["cid"],
            f"AI Pipeline classified as '{ai_cls['category']}' ({ai_cls['confidence']}% confidence) with {ai_prio['priority']} priority.",
            triage_time
        ))

        # 3. Assignment if applicable
        if item.get("staff"):
            assign_time = (created_dt + timedelta(minutes=45)).strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute('''
                INSERT INTO assignments (complaint_id, staff_id, assigned_by, assigned_at, notes, status)
                VALUES (?, ?, ?, ?, 'Dispatched maintenance technician with standard pipe repair kit.', ?)
            ''', (item["cid"], item["staff"], admin_id, assign_time, 'In Progress' if item["status"] != 'Assigned' else 'Assigned'))

            cursor.execute('''
                INSERT INTO status_history (complaint_id, changed_by, old_status, new_status, comment, timestamp)
                VALUES (?, ?, 'Pending', 'Assigned', 'Incident assigned to field maintenance engineer by Central Operations.', ?)
            ''', (item["cid"], admin_id, assign_time))

        # 4. In Progress event
        if item["status"] in ["In Progress", "Resolved"]:
            prog_time = (created_dt + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute('''
                INSERT INTO status_history (complaint_id, changed_by, old_status, new_status, comment, timestamp)
                VALUES (?, ?, 'Assigned', 'In Progress', 'Crew arrived on site, isolated water line, and initiated hydraulic repair.', ?)
            ''', (item["cid"], item["staff"], prog_time))

        # 5. Resolved event
        if item["status"] == "Resolved":
            resolv_time = (created_dt + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute('''
                INSERT INTO status_history (complaint_id, changed_by, old_status, new_status, comment, timestamp)
                VALUES (?, ?, 'In Progress', 'Resolved', 'Defective pipe segment replaced, pressure tested to 4.5 bar, roadway restored. Case closed.', ?)
            ''', (item["cid"], item["staff"], resolv_time))

            # Mark assignment completed
            cursor.execute('''
                UPDATE assignments SET status = 'Completed', completed_at = ? WHERE complaint_id = ?
            ''', (resolv_time, item["cid"]))

    conn.commit()
    conn.close()
    print("Database seeding completed successfully! All 15 sample complaints and demo accounts created.")

if __name__ == "__main__":
    seed_database()
