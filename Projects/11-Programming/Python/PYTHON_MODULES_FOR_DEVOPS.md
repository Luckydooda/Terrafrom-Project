# Python Modules for DevOps/SRE (1 Hour)
## Understanding Imports and Essential Modules

---

## 🎯 Goals for This Hour:
- Understand what modules and imports are
- Learn essential built-in modules for DevOps
- Explore external modules (requests, boto3)
- Practice real SRE use cases

---

## 📚 Part 1: What Are Modules? (10 min)

### Think of modules as toolboxes

```python
# Without modules - manual work
def read_file(filename):
    # Write all file reading code yourself
    pass

# With modules - use pre-built tools
import os
os.path.exists('file.txt')  # Already written for you!
```

### Types of Modules

1. **Built-in** - Come with Python (os, sys, json)
2. **External** - Install with pip (requests, boto3)
3. **Your own** - Custom modules you create

---

## 📦 Part 2: Essential Built-in Modules (30 min)

### 1. `os` - Operating System Interface

**Use for:** File operations, paths, environment variables

```python
import os

# Check if file exists
if os.path.exists('/var/log/app.log'):
    print("Log file found!")

# Get current directory
current_dir = os.getcwd()
print(f"Working in: {current_dir}")

# List files in directory
files = os.listdir('/var/log')
print(f"Found {len(files)} files")

# Get environment variables
db_host = os.getenv('DATABASE_HOST', 'localhost')  # Default if not set
api_key = os.environ.get('API_KEY')

# Create directory
os.makedirs('/tmp/backups', exist_ok=True)  # exist_ok prevents error if exists

# Path operations
log_path = os.path.join('/var', 'log', 'app.log')  # /var/log/app.log
filename = os.path.basename('/var/log/app.log')     # app.log
directory = os.path.dirname('/var/log/app.log')     # /var/log
```

**SRE Use Case:**
```python
import os

def check_disk_space():
    """Check if log directory has space"""
    log_dir = '/var/log'
    
    # Get disk usage
    stat = os.statvfs(log_dir)
    free_space = stat.f_bavail * stat.f_frsize / (1024**3)  # GB
    
    if free_space < 10:
        print(f"⚠️ WARNING: Only {free_space:.2f} GB left!")
        return False
    return True
```

---

### 2. `sys` - System Parameters

**Use for:** Command-line arguments, exit codes, Python info

```python
import sys

# Get command-line arguments
# python script.py arg1 arg2
script_name = sys.argv[0]  # script.py
first_arg = sys.argv[1]    # arg1

# Exit with status code
if error:
    sys.exit(1)  # Exit with error (non-zero)
else:
    sys.exit(0)  # Exit successfully

# Python version
print(f"Python version: {sys.version}")

# Module search paths
print(sys.path)

# Platform info
print(f"Running on: {sys.platform}")  # linux, win32, darwin
```

**SRE Use Case:**
```python
import sys

def backup_logs(log_file):
    """Backup log file with error handling"""
    if len(sys.argv) < 2:
        print("Usage: python backup.py <log_file>")
        sys.exit(1)
    
    log_file = sys.argv[1]
    
    try:
        # Backup logic here
        print(f"✓ Backed up {log_file}")
        sys.exit(0)
    except Exception as e:
        print(f"✗ Backup failed: {e}")
        sys.exit(1)
```

---

### 3. `subprocess` - Run Shell Commands

**Use for:** Execute Linux commands from Python

```python
import subprocess

# Simple command
result = subprocess.run(['ls', '-la'], capture_output=True, text=True)
print(result.stdout)

# Check if command succeeded
if result.returncode == 0:
    print("Command succeeded!")

# Run with shell (use carefully!)
subprocess.run('echo "Hello" | grep ll', shell=True)

# Get output
output = subprocess.check_output(['df', '-h']).decode()
print(output)

# Run command with timeout
try:
    subprocess.run(['sleep', '10'], timeout=5)
except subprocess.TimeoutExpired:
    print("Command timed out!")
```

**SRE Use Case:**
```python
import subprocess

def restart_nginx():
    """Restart nginx with validation"""
    
    # Test config first
    test = subprocess.run(['nginx', '-t'], capture_output=True, text=True)
    
    if test.returncode != 0:
        print("✗ Nginx config invalid!")
        print(test.stderr)
        return False
    
    # Restart
    restart = subprocess.run(['systemctl', 'restart', 'nginx'])
    
    if restart.returncode == 0:
        print("✓ Nginx restarted successfully")
        return True
    return False
```

---

### 4. `datetime` - Date and Time

**Use for:** Timestamps, log parsing, scheduling

```python
from datetime import datetime, timedelta

# Current time
now = datetime.now()
print(f"Current time: {now}")

# Format timestamp
timestamp = now.strftime('%Y-%m-%d %H:%M:%S')  # 2026-01-07 14:30:00

# Parse timestamp from logs
log_time = datetime.strptime('2026-01-07 10:30:00', '%Y-%m-%d %H:%M:%S')

# Time calculations
one_hour_ago = now - timedelta(hours=1)
tomorrow = now + timedelta(days=1)

# Compare times
if log_time > one_hour_ago:
    print("Recent log entry")
```

**SRE Use Case:**
```python
from datetime import datetime, timedelta

def find_recent_errors(log_file, hours=1):
    """Find errors from last N hours"""
    
    cutoff_time = datetime.now() - timedelta(hours=hours)
    
    with open(log_file) as f:
        for line in f:
            # Parse: "2026-01-07 10:30:00 ERROR ..."
            timestamp_str = ' '.join(line.split()[:2])
            log_time = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
            
            if log_time > cutoff_time and 'ERROR' in line:
                print(line.strip())
```

---

### 5. `json` - JSON Parsing

**Use for:** Config files, API responses, logs

```python
import json

# Parse JSON string
json_str = '{"name": "app1", "port": 8080}'
config = json.loads(json_str)
print(config['name'])  # app1

# Parse JSON file
with open('config.json') as f:
    config = json.load(f)

# Convert to JSON
data = {'status': 'running', 'uptime': 3600}
json_str = json.dumps(data)
json_pretty = json.dumps(data, indent=2)

# Write JSON file
with open('output.json', 'w') as f:
    json.dump(data, f, indent=2)
```

**SRE Use Case:**
```python
import json

def parse_docker_inspect(container_id):
    """Get container info from docker inspect"""
    import subprocess
    
    output = subprocess.check_output(['docker', 'inspect', container_id])
    data = json.loads(output)
    
    container = data[0]
    return {
        'name': container['Name'],
        'status': container['State']['Status'],
        'ip': container['NetworkSettings']['IPAddress']
    }
```

---

### 6. `pathlib` - Modern Path Handling

**Use for:** Better path operations (alternative to os.path)

```python
from pathlib import Path

# Create path object
log_dir = Path('/var/log')
app_log = log_dir / 'app.log'  # Nicer than os.path.join!

# Check if exists
if app_log.exists():
    print("Log file found")

# Read file
content = app_log.read_text()

# Write file
app_log.write_text("New log entry\n")

# Get parent directory
parent = app_log.parent  # /var/log

# Get filename
name = app_log.name  # app.log

# Find all log files
for log in log_dir.glob('*.log'):
    print(log)
```

---

### 7. `collections` - Specialized Data Structures

**Use for:** Counting, grouping, default dictionaries

#### `Counter` - Count Occurrences

```python
from collections import Counter

# Count items in a list
log_levels = ['INFO', 'ERROR', 'INFO', 'WARNING', 'ERROR', 'ERROR', 'INFO']
counts = Counter(log_levels)
print(counts)  # Counter({'INFO': 3, 'ERROR': 3, 'WARNING': 1})

# Access counts
print(counts['ERROR'])  # 3

# Most common items
print(counts.most_common(2))  # [('INFO', 3), ('ERROR', 3)]

# Count words in text
text = "error error warning info error"
word_counts = Counter(text.split())
print(word_counts)  # Counter({'error': 3, 'warning': 1, 'info': 1})

# Update counter
counts.update(['INFO', 'ERROR'])
print(counts)  # Added more counts

# Combine counters
c1 = Counter(['a', 'b', 'c'])
c2 = Counter(['b', 'c', 'd'])
combined = c1 + c2  # Counter({'b': 2, 'c': 2, 'a': 1, 'd': 1})
```

**SRE Use Case - Count Errors by Type:**
```python
from collections import Counter

def analyze_error_types(log_file):
    """Count different error types in logs"""
    
    error_types = Counter()
    
    with open(log_file) as f:
        for line in f:
            if 'ERROR' in line:
                # Extract error type (e.g., "OutOfMemory", "ConnectionTimeout")
                parts = line.split()
                if len(parts) > 3:
                    error_type = parts[3]
                    error_types[error_type] += 1
    
    # Show top 5 errors
    print("Top 5 Error Types:")
    for error, count in error_types.most_common(5):
        print(f"  {error}: {count} occurrences")
    
    return error_types
```

---

#### `defaultdict` - Dictionary with Default Values

```python
from collections import defaultdict

# Normal dict - KeyError if key doesn't exist
normal = {}
# normal['new_key'] += 1  # ERROR!

# defaultdict - auto-creates keys with default value
counts = defaultdict(int)  # Default value is 0
counts['errors'] += 1  # No error! Auto-creates with 0, then adds 1
print(counts['errors'])  # 1

# Default list
grouped = defaultdict(list)
grouped['errors'].append('OutOfMemory')
grouped['errors'].append('Timeout')
grouped['warnings'].append('High CPU')
print(grouped)  
# defaultdict(<class 'list'>, {
#     'errors': ['OutOfMemory', 'Timeout'],
#     'warnings': ['High CPU']
# })

# Default dict
nested = defaultdict(dict)
nested['server1']['cpu'] = 45
nested['server1']['memory'] = 78
print(nested)
# defaultdict(<class 'dict'>, {
#     'server1': {'cpu': 45, 'memory': 78}
# })
```

**SRE Use Case - Group Logs by Hour:**
```python
from collections import defaultdict
from datetime import datetime

def group_errors_by_hour(log_file):
    """Group errors by hour of day"""
    
    errors_by_hour = defaultdict(list)
    
    with open(log_file) as f:
        for line in f:
            if 'ERROR' in line:
                # Parse: "2026-01-07 10:30:00 ERROR ..."
                timestamp_str = ' '.join(line.split()[:2])
                log_time = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                hour = log_time.hour
                
                # Group by hour (auto-creates list if not exists!)
                errors_by_hour[hour].append(line.strip())
    
    # Show errors per hour
    for hour in sorted(errors_by_hour.keys()):
        count = len(errors_by_hour[hour])
        print(f"Hour {hour:02d}:00 - {count} errors")
    
    return errors_by_hour

# Usage
errors = group_errors_by_hour('app.log')
# Output:
# Hour 10:00 - 3 errors
# Hour 14:00 - 2 errors
```

**SRE Use Case - Track Metrics by Server:**
```python
from collections import defaultdict

def track_server_metrics():
    """Track CPU/Memory by server using defaultdict"""
    
    metrics = defaultdict(lambda: {'cpu': [], 'memory': []})
    
    # Simulate collecting metrics
    metrics['server1']['cpu'].append(45)
    metrics['server1']['memory'].append(78)
    metrics['server2']['cpu'].append(32)
    metrics['server2']['memory'].append(65)
    
    # No KeyError even for new servers!
    metrics['server3']['cpu'].append(12)  # Auto-creates everything
    
    # Calculate averages
    for server, data in metrics.items():
        avg_cpu = sum(data['cpu']) / len(data['cpu'])
        avg_mem = sum(data['memory']) / len(data['memory'])
        print(f"{server}: CPU {avg_cpu:.1f}%, Memory {avg_mem:.1f}%")

track_server_metrics()
```

---

#### Quick Comparison: dict vs defaultdict vs Counter

```python
from collections import defaultdict, Counter

# Problem: Count word frequency

words = ['error', 'info', 'error', 'warning', 'error', 'info']

# Method 1: Regular dict (manual)
counts1 = {}
for word in words:
    if word in counts1:
        counts1[word] += 1
    else:
        counts1[word] = 1

# Method 2: defaultdict (cleaner)
counts2 = defaultdict(int)
for word in words:
    counts2[word] += 1  # No if check needed!

# Method 3: Counter (easiest!)
counts3 = Counter(words)

# All give same result:
print(counts1)  # {'error': 3, 'info': 2, 'warning': 1}
print(counts2)  # defaultdict(<class 'int'>, {'error': 3, 'info': 2, 'warning': 1})
print(counts3)  # Counter({'error': 3, 'info': 2, 'warning': 1})

# But Counter has extra methods
print(counts3.most_common(1))  # [('error', 3)]
```

**When to use which:**
- **Regular dict**: When you don't need defaults
- **defaultdict**: When you want automatic key creation with defaults
- **Counter**: When specifically counting occurrences

---

## 🌐 Part 3: Essential External Modules (15 min)

### 1. `requests` - HTTP Requests

**Install:** `pip install requests`

**Use for:** API calls, health checks, webhooks

```python
import requests

# GET request
response = requests.get('https://api.github.com')
print(response.status_code)  # 200
data = response.json()

# POST request
data = {'key': 'value'}
response = requests.post('https://api.example.com', json=data)

# With headers
headers = {'Authorization': 'Bearer token123'}
response = requests.get('https://api.example.com', headers=headers)

# With timeout
try:
    response = requests.get('https://slow-api.com', timeout=5)
except requests.Timeout:
    print("Request timed out!")
```

**SRE Use Case:**
```python
import requests

def health_check(url):
    """Check if service is healthy"""
    try:
        response = requests.get(f"{url}/health", timeout=3)
        
        if response.status_code == 200:
            print(f"✓ {url} is healthy")
            return True
        else:
            print(f"✗ {url} returned {response.status_code}")
            return False
    except requests.Timeout:
        print(f"✗ {url} timed out")
        return False
    except requests.ConnectionError:
        print(f"✗ Cannot connect to {url}")
        return False

# Check multiple services
services = [
    'http://app1.example.com',
    'http://app2.example.com',
    'http://app3.example.com'
]

for service in services:
    health_check(service)
```

---

### 2. `boto3` - AWS SDK

**Install:** `pip install boto3`

**Use for:** Managing AWS resources

```python
import boto3

# S3 operations
s3 = boto3.client('s3')

# List buckets
response = s3.list_buckets()
for bucket in response['Buckets']:
    print(bucket['Name'])

# Upload file
s3.upload_file('local.txt', 'my-bucket', 'remote.txt')

# Download file
s3.download_file('my-bucket', 'remote.txt', 'local.txt')

# EC2 operations
ec2 = boto3.client('ec2')

# List instances
instances = ec2.describe_instances()

# Start instance
ec2.start_instances(InstanceIds=['i-1234567890'])
```

**SRE Use Case:**
```python
import boto3
from datetime import datetime, timedelta

def backup_to_s3(local_file, bucket_name):
    """Backup file to S3 with timestamp"""
    s3 = boto3.client('s3')
    
    # Add timestamp to filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    s3_key = f"backups/{timestamp}_{local_file}"
    
    try:
        s3.upload_file(local_file, bucket_name, s3_key)
        print(f"✓ Uploaded {local_file} to s3://{bucket_name}/{s3_key}")
        return True
    except Exception as e:
        print(f"✗ Upload failed: {e}")
        return False
```

---

### 3. `paramiko` - SSH Client

**Install:** `pip install paramiko`

**Use for:** Remote server operations

```python
import paramiko

# Create SSH client
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect
ssh.connect('server.example.com', username='admin', password='pass')

# Run command
stdin, stdout, stderr = ssh.exec_command('df -h')
print(stdout.read().decode())

# Close connection
ssh.close()
```

---

## 🏋️ Part 4: Practical Examples (20 min)

### Example 1: Log Analyzer Script

```python
#!/usr/bin/env python3
"""
Analyze application logs
Usage: python log_analyzer.py app.log
"""

import sys
import json
from datetime import datetime
from collections import Counter

def analyze_log(log_file):
    """Analyze log file and generate report"""
    
    # Counters
    log_levels = Counter()
    errors_by_type = Counter()
    
    # Read file
    with open(log_file) as f:
        for line in f:
            parts = line.split()
            if len(parts) < 3:
                continue
            
            # Extract log level
            log_level = parts[2]
            log_levels[log_level] += 1
            
            # Track error types
            if log_level == 'ERROR':
                error_msg = ' '.join(parts[3:])
                errors_by_type[error_msg] += 1
    
    # Generate report
    report = {
        'total_lines': sum(log_levels.values()),
        'by_level': dict(log_levels),
        'top_errors': dict(errors_by_type.most_common(5))
    }
    
    return report

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python log_analyzer.py <log_file>")
        sys.exit(1)
    
    log_file = sys.argv[1]
    
    try:
        report = analyze_log(log_file)
        print(json.dumps(report, indent=2))
    except FileNotFoundError:
        print(f"Error: {log_file} not found")
        sys.exit(1)
```

---

### Example 2: Health Check Monitor

```python
#!/usr/bin/env python3
"""
Monitor multiple services and send alerts
"""

import requests
import smtplib
from datetime import datetime

SERVICES = [
    'http://app1.example.com/health',
    'http://app2.example.com/health',
    'http://db.example.com/ping'
]

def check_service(url):
    """Check if service is up"""
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except:
        return False

def send_alert(failed_services):
    """Send email alert for failed services"""
    message = f"""
    ALERT: Services Down
    
    The following services are not responding:
    {', '.join(failed_services)}
    
    Time: {datetime.now()}
    """
    print(message)  # In real scenario, send email

def monitor():
    """Run health checks"""
    failed = []
    
    for service in SERVICES:
        if not check_service(service):
            failed.append(service)
            print(f"✗ {service} is DOWN")
        else:
            print(f"✓ {service} is UP")
    
    if failed:
        send_alert(failed)
    
    return len(failed) == 0

if __name__ == '__main__':
    success = monitor()
    sys.exit(0 if success else 1)
```

---

### Example 3: Backup Script

```python
#!/usr/bin/env python3
"""
Backup important files to S3
"""

import os
import boto3
from datetime import datetime
from pathlib import Path

def backup_to_s3(local_dir, bucket_name):
    """Backup directory to S3"""
    s3 = boto3.client('s3')
    timestamp = datetime.now().strftime('%Y%m%d')
    
    # Find all files
    local_path = Path(local_dir)
    files = list(local_path.rglob('*'))
    
    uploaded = 0
    for file in files:
        if file.is_file():
            # Create S3 key
            relative = file.relative_to(local_path)
            s3_key = f"backups/{timestamp}/{relative}"
            
            try:
                s3.upload_file(str(file), bucket_name, s3_key)
                uploaded += 1
                print(f"✓ Uploaded {file}")
            except Exception as e:
                print(f"✗ Failed to upload {file}: {e}")
    
    print(f"\nBackup complete: {uploaded} files uploaded")
    return uploaded

if __name__ == '__main__':
    backup_to_s3('/var/log', 'my-backup-bucket')
```

---

## 📝 Quick Module Reference

| Module | Use Case | Key Functions |
|--------|----------|---------------|
| `os` | File/path operations | `os.path.exists()`, `os.listdir()`, `os.getenv()` |
| `sys` | CLI args, exit codes | `sys.argv`, `sys.exit()` |
| `subprocess` | Run shell commands | `subprocess.run()`, `subprocess.check_output()` |
| `datetime` | Timestamps, time math | `datetime.now()`, `strptime()`, `timedelta()` |
| `json` | Parse/create JSON | `json.loads()`, `json.dumps()` |
| `pathlib` | Modern paths | `Path()`, `.exists()`, `.glob()` |
| `collections` | Counting, grouping | `Counter()`, `defaultdict()` |
| `requests` | HTTP/API calls | `requests.get()`, `requests.post()` |
| `boto3` | AWS operations | `boto3.client('s3')`, `.upload_file()` |

---

## 🎯 What You'll Know After This:

✅ What modules and imports are  
✅ Essential built-in modules for DevOps  
✅ How to use external modules (pip install)  
✅ Real SRE automation examples  
✅ How to write Python scripts for ops work  

---

**Practice these on your machine and EC2!**

*Time: 60 minutes*
