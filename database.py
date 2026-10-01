import sqlite3
import os
from datetime import datetime
from config import Config

def get_db_connection():
    """Returns an active SQLite database connection with Row factory."""
    os.makedirs(os.path.dirname(Config.DATABASE_PATH), exist_ok=True)
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    """Initializes all required database tables and indexes."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            phone TEXT,
            role TEXT NOT NULL DEFAULT 'citizen', -- 'citizen', 'admin', 'staff'
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Staff Profiles Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS staff_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            specialty TEXT DEFAULT 'General Plumbing & Mainlines',
            zone TEXT DEFAULT 'Zone A - Metro Central',
            status TEXT DEFAULT 'Available',
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')

    # Complaints Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            complaint_id TEXT UNIQUE NOT NULL,
            user_id INTEGER,
            title TEXT NOT NULL,
            street_name TEXT NOT NULL,
            landmark TEXT,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            category TEXT NOT NULL,
            ai_predicted_category TEXT,
            ai_confidence REAL DEFAULT 0.0,
            priority TEXT NOT NULL DEFAULT 'Medium',
            ai_priority_score INTEGER DEFAULT 50,
            user_severity INTEGER DEFAULT 3,
            description TEXT NOT NULL,
            ai_field_summary TEXT,
            photo_path TEXT,
            status TEXT NOT NULL DEFAULT 'Pending', -- 'Pending', 'Assigned', 'In Progress', 'Resolved', 'Rejected'
            is_duplicate_of TEXT,
            duplicate_score REAL DEFAULT 0.0,
            estimated_loss_lph INTEGER DEFAULT 200,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL
        )
    ''')

    # Staff Assignments Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            complaint_id TEXT NOT NULL,
            staff_id INTEGER NOT NULL,
            assigned_by INTEGER,
            assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            notes TEXT,
            status TEXT DEFAULT 'Assigned', -- 'Assigned', 'In Progress', 'Completed'
            completed_at TIMESTAMP,
            FOREIGN KEY (complaint_id) REFERENCES complaints (complaint_id) ON DELETE CASCADE,
            FOREIGN KEY (staff_id) REFERENCES users (id) ON DELETE CASCADE,
            FOREIGN KEY (assigned_by) REFERENCES users (id) ON DELETE SET NULL
        )
    ''')

    # Status Timeline History Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS status_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            complaint_id TEXT NOT NULL,
            changed_by INTEGER,
            old_status TEXT,
            new_status TEXT NOT NULL,
            comment TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (complaint_id) REFERENCES complaints (complaint_id) ON DELETE CASCADE,
            FOREIGN KEY (changed_by) REFERENCES users (id) ON DELETE SET NULL
        )
    ''')

    # AI Corrections / Feedback Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ai_corrections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            complaint_id TEXT NOT NULL,
            original_category TEXT,
            corrected_category TEXT,
            original_priority TEXT,
            corrected_priority TEXT,
            corrected_by INTEGER,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (complaint_id) REFERENCES complaints (complaint_id) ON DELETE CASCADE,
            FOREIGN KEY (corrected_by) REFERENCES users (id) ON DELETE SET NULL
        )
    ''')

    # Create Indexes for fast querying
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_complaint_id ON complaints(complaint_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_complaint_status ON complaints(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_complaint_category ON complaints(category)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_complaint_user ON complaints(user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_assignments_complaint ON assignments(complaint_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_status_history_complaint ON status_history(complaint_id)')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully.")
