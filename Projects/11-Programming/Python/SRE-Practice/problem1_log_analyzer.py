# SRE/DevOps Python Practice Problems
# Using modules: os, subprocess, datetime, collections, json

"""
PROBLEM 1: Log Analyzer
=======================

You are an SRE and need to analyze application logs.
The logs have this format:
    2026-01-07 10:00:01 INFO Starting application
    2026-01-07 10:00:05 ERROR Database connection failed
    2026-01-07 10:00:10 WARNING High memory usage: 85%

TASKS:
1. Count how many lines for each log level (INFO, ERROR, WARNING)
2. Find the top 3 most common error messages
3. Calculate error rate (ERROR count / total lines * 100)

HINTS:
- Use collections.Counter
- Use file.readlines() or iterate line by line
- Use split() to extract parts of each line
"""

from collections import Counter

# Sample log data (simulating a log file)
SAMPLE_LOGS = """2026-01-07 10:00:01 INFO Starting application server on port 8080
2026-01-07 10:00:02 INFO Database connection established
2026-01-07 10:00:05 ERROR Failed to connect to Redis cache
2026-01-07 10:00:10 WARNING High memory usage: 85%
2026-01-07 10:00:15 INFO Processing request from 192.168.1.45
2026-01-07 10:00:20 ERROR OutOfMemoryError: Java heap space
2026-01-07 10:00:25 INFO User login successful
2026-01-07 10:00:30 ERROR Failed to send email notification
2026-01-07 10:00:35 WARNING Slow query detected: 3.5 seconds
2026-01-07 10:00:40 ERROR OutOfMemoryError: Java heap space
2026-01-07 10:00:45 INFO Health check passed
2026-01-07 10:00:50 ERROR Database deadlock detected
2026-01-07 10:00:55 INFO Backup completed successfully
2026-01-07 10:01:00 ERROR OutOfMemoryError: Java heap space
2026-01-07 10:01:05 WARNING Rate limit exceeded"""


def analyze_logs(log_text):
    """
    Analyze log text and return:
    - counts: dict with count of each log level
    - top_errors: list of top 3 error messages with counts
    - error_rate: percentage of ERROR lines
    
    TODO: Implement this function
    """
    lines = log_text.strip().split('\n')
    log_levels =Counter()
    errors=[]
    for line in lines:
        parts = line.split()
        level = parts[2]
        log_levels[level]+=1
        if level == 'ERROR':
            error_msg = ' '.join(parts[3:])
            errors.append(error_msg)
    
    error_counter = Counter(errors)
    top_errors = error_counter.most_common(3)
    error_rate = log_levels['ERROR'] / len(lines) * 100
    return log_levels, top_errors, error_rate


    
    


# ==================================================
# TEST
# ==================================================

if __name__ == "__main__":
    result = analyze_logs(SAMPLE_LOGS)
    
    if result:
        counts, top_errors, error_rate = result
        
        print("=" * 50)
        print("LOG ANALYSIS REPORT")
        print("=" * 50)
        
        print("\n📊 Log Level Counts:")
        for level, count in counts.items():
            print(f"  {level}: {count}")
        
        print("\n🔥 Top 3 Error Messages:")
        for msg, count in top_errors:
            print(f"  [{count}x] {msg}")
        
        print(f"\n⚠️ Error Rate: {error_rate:.1f}%")
        
        print("\n" + "=" * 50)
        print("EXPECTED OUTPUT:")
        print("=" * 50)
        print("""
📊 Log Level Counts:
  INFO: 6
  ERROR: 6
  WARNING: 3

🔥 Top 3 Error Messages:
  [3x] OutOfMemoryError: Java heap space
  [1x] Failed to connect to Redis cache
  [1x] Failed to send email notification

⚠️ Error Rate: 40.0%
""")
    else:
        print("Implement the analyze_logs function!")
