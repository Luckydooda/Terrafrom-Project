# SRE/DevOps Python Practice Problems
# Using modules: os, subprocess, datetime, json

"""
PROBLEM 2: Health Check Monitor
===============================

You are an SRE and need to build a simple health checker.
Check if services are "healthy" based on simulated responses.

TASKS:
1. Check each service's status (simulated)
2. Return list of healthy and unhealthy services
3. Generate a JSON report with:
   - timestamp
   - total_services
   - healthy_count
   - unhealthy_count
   - services (list with name and status)

HINTS:
- Use datetime.now() for timestamp
- Use json.dumps() to create JSON
- Handle exceptions for failed services
"""

import json
from datetime import datetime

# Simulated service responses (in real life, you'd use requests.get())
SERVICES = {
    'api-server': {'status': 200, 'response_time': 0.5},
    'database': {'status': 200, 'response_time': 0.3},
    'cache-redis': {'status': 500, 'response_time': 5.0},  # UNHEALTHY!
    'auth-service': {'status': 200, 'response_time': 0.2},
    'notification': {'status': 503, 'response_time': 10.0},  # UNHEALTHY!
    'file-storage': {'status': 200, 'response_time': 0.8},
}


def is_healthy(service_name, service_data):
    """
    Check if a service is healthy.
    
    A service is healthy if:
    - status code is 200
    - response_time is less than 2 seconds
    
    TODO: Implement this function
    Return: True if healthy, False otherwise
    """
    if service_data['status'] == 200 and service_data['response_time'] < 2:
        return True
    return False


def run_health_check(services):
    """
    Run health check on all services.
    
    TODO: Implement this function
    Return: dict with structure:
    {
        'timestamp': '2026-01-07T22:00:00',
        'total_services': 6,
        'healthy_count': 4,
        'unhealthy_count': 2,
        'services': [
            {'name': 'api-server', 'status': 'healthy'},
            {'name': 'cache-redis', 'status': 'unhealthy'},
            ...
        ]
    }
    """
    time_stamp = datetime.now().isoformat()
    total_services = len(services)
    health_count=0
    unhealthy_count = 0
    services_list=[]
    for srvice_name in services:
        service_data=services[srvice_name]
        if is_healthy(srvice_name, service_data):
            health_count+=1
        else:
            unhealthy_count+=1
        services_list.append({'name': srvice_name, 'status': 'healthy' if is_healthy(srvice_name, service_data) else 'unhealthy'})
    return {'timestamp': time_stamp, 'total_services': total_services, 'healthy_count': health_count, 'unhealthy_count': unhealthy_count, 'services': services_list}


def generate_report(health_data):
    """
    Generate a JSON report from health check data.
    
    TODO: Implement this function
    Return: JSON string (pretty-printed)
    """
    return json.dumps(health_data, indent=4)


# ==================================================
# TEST
# ==================================================

if __name__ == "__main__":
    print("=" * 50)
    print("HEALTH CHECK MONITOR")
    print("=" * 50)
    
    # Run health check
    health_data = run_health_check(SERVICES)
    
    if health_data:
        # Generate report
        report = generate_report(health_data)
        
        print("\n📋 Health Check Report:")
        print(report)
        
        # Summary
        print("\n" + "=" * 50)
        print("SUMMARY:")
        print(f"✓ Healthy: {health_data['healthy_count']}")
        print(f"✗ Unhealthy: {health_data['unhealthy_count']}")
        
        # List unhealthy services
        unhealthy = [s['name'] for s in health_data['services'] if s['status'] == 'unhealthy']
        if unhealthy:
            print(f"\n⚠️ ALERT: These services are DOWN:")
            for service in unhealthy:
                print(f"  - {service}")
        
        print("\n" + "=" * 50)
        print("EXPECTED OUTPUT:")
        print("=" * 50)
        print("""
{
  "timestamp": "2026-01-07T22:51:52",
  "total_services": 6,
  "healthy_count": 4,
  "unhealthy_count": 2,
  "services": [
    {"name": "api-server", "status": "healthy"},
    {"name": "database", "status": "healthy"},
    {"name": "cache-redis", "status": "unhealthy"},
    {"name": "auth-service", "status": "healthy"},
    {"name": "notification", "status": "unhealthy"},
    {"name": "file-storage", "status": "healthy"}
  ]
}

SUMMARY:
✓ Healthy: 4
✗ Unhealthy: 2

⚠️ ALERT: These services are DOWN:
  - cache-redis
  - notification
""")
    else:
        print("\nImplement the functions to see results!")
