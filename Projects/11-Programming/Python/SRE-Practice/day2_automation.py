# SRE Automation Practice - Day 2
# Real-world DevOps scenarios

"""
PROBLEM 1: Disk Space Monitor
=============================

You are an SRE and need to monitor disk usage across multiple servers.
Given a list of servers with their disk usage, identify which need attention.

TASKS:
1. Find servers with disk usage > 80% (WARNING)
2. Find servers with disk usage > 90% (CRITICAL)
3. Return a report with counts and server names

Example:
    servers = {
        'web-01': 75,
        'web-02': 85,Z
        'db-01': 92,
        'cache-01': 45,
        'api-01': 88
    }
    
    Expected output:
    {
        'warning': ['web-02', 'api-01'],      # 80-90%
        'critical': ['db-01'],                 # >90%
        'healthy': ['web-01', 'cache-01'],     # <80%
        'warning_count': 2,
        'critical_count': 1
    }

HINTS:
- Loop through dict with .items()
- Categorize based on percentage thresholds
"""

def monitor_disk_usage(servers):
    """
    Monitor disk usage and categorize servers.
    
    Args:
        servers: dict of {server_name: disk_usage_percent}
    
    Returns:
        dict with 'warning', 'critical', 'healthy' lists and counts
    
    TODO: Implement this function
    """
    warning=[]
    critical=[]
    healthy=[]

    for server,usage in servers.items():
        if usage>90:
            critical.append(server)
        elif usage>80:
            warning.append(server)
        else:
            healthy.append(server)
    return {
        'warning': warning,
        'critical': critical,
        'healthy': healthy,
        'warning_count': len(warning),
        'critical_count': len(critical) 
    }

# ==================================================
# PROBLEM 2: Backup Scheduler
# ==================================================

"""
PROBLEM 2: Backup Time Calculator
=================================

You need to schedule backups for multiple databases.
Given backup sizes and network speed, calculate estimated time.

TASKS:
1. Calculate backup time for each database (size / speed)
2. Find total backup time
3. Estimate completion time (current time + total time)

Example:
    databases = {
        'users_db': 50,      # 50 GB
        'orders_db': 120,    # 120 GB
        'logs_db': 200       # 200 GB
    }
    network_speed = 10  # 10 GB per hour
    
    Expected:
    {
        'databases': {
            'users_db': 5.0,    # 50/10 = 5 hours
            'orders_db': 12.0,  # 120/10 = 12 hours
            'logs_db': 20.0     # 200/10 = 20 hours
        },
        'total_hours': 37.0,
        'estimated_completion': '2026-01-08 21:00:00'  # example
    }

HINTS:
- Use datetime for time calculations
- timedelta(hours=X) to add hours
"""

from datetime import datetime, timedelta

def calculate_backup_time(databases, network_speed_gbph):
    database_time={}
    total_time=0
    current_time=datetime.now()
    for db,size in databases.items():
        time=size/network_speed_gbph
        database_time[db]=time
        total_time+=time
    estimated_completion=current_time+timedelta(hours=total_time)
    return {
        'databases':database_time,
        'total_hours':total_time,
        'estimated_completion':estimated_completion.strftime('%Y-%m-%d %H:%M:%S')
    }
    """
    Calculate backup times for databases.
    
    Args:
        databases: dict of {db_name: size_in_gb}
        network_speed_gbph: network speed in GB per hour
    
    Returns:
        dict with individual times, total, and completion estimate
    """
    


# ==================================================
# TEST CASES
# ==================================================

if __name__ == "__main__":
    print("=" * 50)
    print("SRE Automation Practice - Day 2")
    print("=" * 50)
    
    # Test Problem 1: Disk Monitor
    print("\n📊 Problem 1: Disk Space Monitor")
    print("-" * 40)
    
    servers = {
        'web-01': 75,
        'web-02': 85,
        'db-01': 92,
        'cache-01': 45,
        'api-01': 88,
        'db-02': 95,
        'log-server': 78
    }
    
    result1 = monitor_disk_usage(servers)
    
    if result1:
        print(f"🟢 Healthy servers: {result1.get('healthy', [])}")
        print(f"🟡 Warning (>80%): {result1.get('warning', [])}")
        print(f"🔴 Critical (>90%): {result1.get('critical', [])}")
        print(f"\nWarning count: {result1.get('warning_count', 0)}")
        print(f"Critical count: {result1.get('critical_count', 0)}")
    else:
        print("Implement monitor_disk_usage function!")
    
    # Test Problem 2: Backup Calculator
    print("\n" + "=" * 50)
    print("📊 Problem 2: Backup Time Calculator")
    print("-" * 40)
    
    databases = {
        'users_db': 50,
        'orders_db': 120,
        'logs_db': 200
    }
    
    result2 = calculate_backup_time(databases, network_speed_gbph=10)
    
    if result2:
        print("Backup times per database:")
        for db, hours in result2.get('databases', {}).items():
            print(f"  {db}: {hours:.1f} hours")
        print(f"\nTotal backup time: {result2.get('total_hours', 0):.1f} hours")
        print(f"Estimated completion: {result2.get('estimated_completion', 'N/A')}")
    else:
        print("Implement calculate_backup_time function!")
    
    print("\n" + "=" * 50)
    print("EXPECTED OUTPUT:")
    print("=" * 50)
    print("""
📊 Problem 1: Disk Space Monitor
----------------------------------------
🟢 Healthy servers: ['web-01', 'cache-01', 'log-server']
🟡 Warning (>80%): ['web-02', 'api-01']
🔴 Critical (>90%): ['db-01', 'db-02']

Warning count: 2
Critical count: 2

📊 Problem 2: Backup Time Calculator
----------------------------------------
Backup times per database:
  users_db: 5.0 hours
  orders_db: 12.0 hours
  logs_db: 20.0 hours

Total backup time: 37.0 hours
Estimated completion: 2026-01-08 XX:XX:XX (current + 37h)
""")
