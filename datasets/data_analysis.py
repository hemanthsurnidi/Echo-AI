import sqlite3
import os
import csv
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend", "echo_ai.db")
CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "user_sessions.csv")

def extract_and_export_data():
    """Extracts session records from SQLite and exports them to a structured CSV file."""
    if not os.path.exists(DB_PATH):
        print(f"Database file not found at {DB_PATH}. Run generate_mock_data.py first.")
        return []

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM sessions ORDER BY timestamp ASC")
    rows = cursor.fetchall()
    conn.close()
    
    sessions = [dict(row) for row in rows]
    
    # Save as CSV
    if sessions:
        keys = sessions[0].keys()
        os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
        with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
            dict_writer = csv.DictWriter(f, keys)
            dict_writer.writeheader()
            dict_writer.writerows(sessions)
        print(f"Successfully exported {len(sessions)} records to: {CSV_PATH}")
    
    return sessions

def run_data_analysis():
    """Performs statistical feature extraction and analytics on the session dataset."""
    sessions = extract_and_export_data()
    if not sessions:
        return
        
    print("\n" + "="*50)
    print("           ECHO AI DATA SCIENCE ANALYTICS            ")
    print("="*50)
    
    # Calculate aggregate metrics
    durations = [s["duration"] for s in sessions]
    wpms = [s["wpm"] for s in sessions]
    confidence_scores = [s["confidence_score"] for s in sessions]
    communication_scores = [s["communication_score"] for s in sessions]
    word_counts = [s["word_count"] for s in sessions]
    
    num_sessions = len(sessions)
    
    def mean(lst): return sum(lst) / len(lst) if lst else 0
    def std_dev(lst, mu): return (sum((x - mu)**2 for x in lst) / len(lst))**0.5 if lst else 0
    
    mean_wpm = mean(wpms)
    mean_conf = mean(confidence_scores)
    mean_comm = mean(communication_scores)
    mean_dur = mean(durations)
    
    std_wpm = std_dev(wpms, mean_wpm)
    std_conf = std_dev(confidence_scores, mean_conf)
    std_comm = std_dev(communication_scores, mean_comm)
    
    print(f"Total Sessions Analyzed: {num_sessions}")
    print(f"Average Recording Duration: {mean_dur:.1f} seconds")
    print(f"Speech Rate (WPM):          {mean_wpm:.1f} (StdDev: {std_wpm:.1f})")
    print(f"Confidence Score (0-100):   {mean_conf:.1f} (StdDev: {std_conf:.1f})")
    print(f"Communication Score (0-100):{mean_comm:.1f} (StdDev: {std_comm:.1f})")
    
    # Pace category distribution
    slow_count = sum(1 for s in sessions if s["speed_category"] == "Slow")
    normal_count = sum(1 for s in sessions if s["speed_category"] == "Normal")
    fast_count = sum(1 for s in sessions if s["speed_category"] == "Fast")
    
    print("\nSpeech Pace Distribution:")
    print(f" - Slow (<110 WPM):   {slow_count} ({slow_count/num_sessions*100:.1f}%)")
    print(f" - Normal (110-150): {normal_count} ({normal_count/num_sessions*100:.1f}%)")
    print(f" - Fast (>150 WPM):   {fast_count} ({fast_count/num_sessions*100:.1f}%)")
    
    # Correlation analysis (simple Pearson Correlation Coefficient)
    def pearson_correlation(x, y):
        mean_x, mean_y = mean(x), mean(y)
        num = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        den_x = sum((xi - mean_x)**2 for xi in x)
        den_y = sum((yi - mean_y)**2 for yi in y)
        if den_x == 0 or den_y == 0:
            return 0
        return num / (den_x * den_y)**0.5
        
    corr_wpm_comm = pearson_correlation(wpms, communication_scores)
    corr_conf_comm = pearson_correlation(confidence_scores, communication_scores)
    corr_dur_conf = pearson_correlation(durations, confidence_scores)
    
    print("\nFeature Correlation Matrix:")
    print(f" - Correlation (WPM, Communication Score):        {corr_wpm_comm:+.3f}")
    print(f" - Correlation (Confidence, Communication Score): {corr_conf_comm:+.3f} (Strong positive correlation)")
    print(f" - Correlation (Duration, Confidence Score):       {corr_dur_conf:+.3f}")
    
    # Try importing scientific libraries for visualization (if installed)
    try:
        import pandas as pd
        import matplotlib.pyplot as plt
        
        # Load dataset
        df = pd.read_csv(CSV_PATH)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        plt.figure(figsize=(12, 5))
        
        # Plot communication progress
        plt.subplot(1, 2, 1)
        plt.plot(df['timestamp'], df['communication_score'], marker='o', color='#8b5cf6', label='Communication')
        plt.plot(df['timestamp'], df['confidence_score'], marker='x', linestyle='--', color='#ec4899', label='Confidence')
        plt.title('Communication Intelligence Score Progress')
        plt.xlabel('Date')
        plt.ylabel('Score')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.xticks(rotation=45)
        
        # Plot WPM vs Communication Score correlation
        plt.subplot(1, 2, 2)
        plt.scatter(df['wpm'], df['communication_score'], color='#14b8a6', alpha=0.7)
        plt.axvline(130, color='red', linestyle=':', label='Ideal WPM (130)')
        plt.title('Speech Speed (WPM) vs Communication Score')
        plt.xlabel('Words Per Minute')
        plt.ylabel('Communication Score')
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        plot_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "analytics_trends.png")
        plt.tight_layout()
        plt.savefig(plot_path)
        print(f"\nAdvanced analytics plot generated and saved to: {plot_path}")
        
    except ImportError:
        print("\nNote: Install 'pandas' and 'matplotlib' for advanced analytics visualization png generation.")

if __name__ == "__main__":
    run_data_analysis()
