import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "echo_ai.db")

def get_db_connection():
    """Returns a connection to the SQLite database, with dictionary row factory enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database schema if tables do not exist."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create sessions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            timestamp TEXT NOT NULL,
            transcript TEXT NOT NULL,
            word_count INTEGER NOT NULL,
            wpm REAL NOT NULL,
            speed_category TEXT NOT NULL,
            confidence_score INTEGER NOT NULL,
            communication_score INTEGER NOT NULL,
            duration REAL NOT NULL,
            audio_filename TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()

def save_session(session_data: dict):
    """Saves a new session recording analysis to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO sessions (
            session_id, timestamp, transcript, word_count, wpm, 
            speed_category, confidence_score, communication_score, duration, audio_filename
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        session_data["session_id"],
        session_data["timestamp"],
        session_data["transcript"],
        session_data["word_count"],
        session_data["wpm"],
        session_data["speed_category"],
        session_data["confidence_score"],
        session_data["communication_score"],
        session_data["duration"],
        session_data["audio_filename"]
    ))
    conn.commit()
    conn.close()

def get_all_sessions():
    """Retrieves all sessions ordered by timestamp descending."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sessions ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_session(session_id: str):
    """Retrieves a single session by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sessions WHERE session_id = ?", (session_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def delete_session(session_id: str):
    """Deletes a session from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT audio_filename FROM sessions WHERE session_id = ?", (session_id,))
    row = cursor.fetchone()
    filename = row["audio_filename"] if row else None
    
    cursor.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))
    conn.commit()
    conn.close()
    return filename

def get_dashboard_stats():
    """Aggregates sessions data for dashboard statistics and trends."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Simple aggregates
    cursor.execute("""
        SELECT 
            COUNT(*) as total,
            COALESCE(AVG(wpm), 0) as avg_wpm,
            COALESCE(AVG(confidence_score), 0) as avg_conf,
            COALESCE(AVG(communication_score), 0) as avg_comm
        FROM sessions
    """)
    agg = cursor.fetchone()
    
    # Trend over time (last 15 sessions in chronological order for charting)
    cursor.execute("""
        SELECT timestamp, wpm, confidence_score, communication_score 
        FROM sessions 
        ORDER BY timestamp ASC 
        LIMIT 15
    """)
    trend_rows = cursor.fetchall()
    conn.close()
    
    # Format trends
    trends = []
    for row in trend_rows:
        # Format date as MM/DD
        ts = row["timestamp"]
        date_str = ts.split("T")[0] if "T" in ts else ts
        if len(date_str) > 5:
            date_str = date_str[-5:] # Show MM-DD
        trends.append({
            "label": date_str,
            "wpm": round(row["wpm"], 1),
            "confidence_score": round(row["confidence_score"], 1),
            "communication_score": round(row["communication_score"], 1)
        })
        
    return {
        "total_recordings": agg["total"],
        "average_wpm": round(agg["avg_wpm"], 1),
        "average_confidence": round(agg["avg_conf"], 1),
        "average_communication": round(agg["avg_comm"], 1),
        "trends": trends
    }

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully at:", DB_PATH)

