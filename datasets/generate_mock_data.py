import sqlite3
import os
import uuid
import random
from datetime import datetime, timedelta

# Path to database
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend", "echo_ai.db")

MOCK_TRANSCRIPTS = [
    "So, basically, today I wanted to, uh, talk about our project timeline. We are, like, slightly behind on the frontend, but I think, you know, we can catch up if we work hard.",
    "Hello team, um, er, this is a quick status update. The database is initialized and, uh, I have set up the tables. However, like, the API calls are having issues.",
    "Um, so today's meeting is about communication skills. I think we, uh, need to pay attention to, like, how fast we speak because sometimes we speak, you know, too fast.",
    "Good morning. I'm pleased to report that the testing phase is complete. We, uh, found three minor bugs but, like, they have been resolved. The performance is solid.",
    "Let's discuss the deployment strategy. We will deploy the FastAPI backend to Render. The Flutter Web client, uh, will be hosted on Vercel for high speed access.",
    "I've been practicing my speaking speed. Today, I'm trying to, uh, maintain a steady pace of around one hundred and thirty words per minute, avoiding filler words.",
    "This is a demonstration of the Echo AI communication intelligence platform. Speech rate is normal, pauses are consistent, and confidence is rising.",
    "Effective communication requires clear articulation, proper pacing, and minimal filler words. I am speaking clearly and confidently to ensure maximum impact."
]

def populate_mock_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Ensure tables exist
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
    
    # Clear old data to prevent duplication
    cursor.execute("DELETE FROM sessions")
    
    start_date = datetime.utcnow() - timedelta(days=30)
    
    print("Generating 30 days of mock speech sessions...")
    
    for i in range(30):
        # Progress simulation: as days progress, the metrics improve!
        progress_factor = i / 30.0 # From 0.0 to 1.0
        
        # Select transcript based on progress
        if progress_factor < 0.3:
            transcript = random.choice(MOCK_TRANSCRIPTS[:3])
            filler_penalty = random.randint(15, 25)
        elif progress_factor < 0.7:
            transcript = random.choice(MOCK_TRANSCRIPTS[3:6])
            filler_penalty = random.randint(5, 15)
        else:
            transcript = random.choice(MOCK_TRANSCRIPTS[5:])
            filler_penalty = random.randint(0, 5)
            
        words = transcript.split()
        word_count = len(words)
        
        # Normal speaking duration for this word count (110 - 160 WPM)
        # As progress improves, the WPM centers towards the ideal 130 WPM
        target_wpm = 130 + random.randint(-25, 25) * (1.0 - progress_factor)
        duration = (word_count / target_wpm) * 60.0
        
        # Recalculate WPM
        wpm = (word_count / duration) * 60.0
        
        if wpm < 110:
            speed_category = "Slow"
        elif wpm <= 150:
            speed_category = "Normal"
        else:
            speed_category = "Fast"
            
        # Scores increase as progress factor increases
        base_confidence = 65 + int(progress_factor * 25)
        confidence_score = base_confidence + random.randint(-5, 5) - filler_penalty // 2
        confidence_score = max(50, min(100, confidence_score))
        
        base_comm = 68 + int(progress_factor * 23)
        communication_score = base_comm + random.randint(-4, 4) - filler_penalty // 3
        # Penalize WPM dev
        wpm_dev = abs(wpm - 130)
        communication_score -= int(wpm_dev * 0.3)
        communication_score = max(50, min(100, communication_score))
        
        session_id = str(uuid.uuid4())
        session_date = start_date + timedelta(days=i) + timedelta(hours=random.randint(0, 8))
        timestamp = session_date.isoformat() + "Z"
        
        # Fake audio filename
        audio_filename = f"{session_id}_original.wav"
        
        cursor.execute("""
            INSERT INTO sessions (
                session_id, timestamp, transcript, word_count, wpm, 
                speed_category, confidence_score, communication_score, duration, audio_filename
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session_id, timestamp, transcript, word_count, round(wpm, 1),
            speed_category, confidence_score, communication_score, round(duration, 1), audio_filename
        ))
        
    conn.commit()
    conn.close()
    print("Database seeding completed successfully.")

if __name__ == "__main__":
    populate_mock_data()
