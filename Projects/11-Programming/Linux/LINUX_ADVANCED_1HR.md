# Linux Practice Session 2 - Advanced Commands (1 Hour)
## Building on Session 1

---

## 🎯 Goals for This Hour:
- Master text processing (sed, awk, cut)
- Learn process management
- Practice shell scripting basics
- Chain commands like a pro

---

## 📝 Part 1: Text Processing (20 min)

### 1. `cut` - Extract Columns from Text

```bash
# Sample: Extract specific fields from logs
echo "2026-01-07 10:00:01 ERROR Failed to connect" > sample.log

# Extract just the date (columns 1-2)
cut -d' ' -f1-2 sample.log
# Output: 2026-01-07 10:00:01

# Extract just the error type (column 3)
cut -d' ' -f3 sample.log
# Output: ERROR

# Extract error message (columns 4 onwards)
cut -d' ' -f4- sample.log
# Output: Failed to connect
```

**SRE Real-World:**
```bash
# Extract just timestamps from app.log
cut -d' ' -f1-2 app.log

# Extract just IPs from access logs
cut -d' ' -f1 /var/log/nginx/access.log | sort | uniq

# Get just error types
grep ERROR app.log | cut -d' ' -f3
```

---

### 2. `awk` - Powerful Text Processing

```bash
# awk syntax: awk 'pattern {action}' file

# Print specific columns
awk '{print $1, $3}' app.log          # Print columns 1 and 3

# Filter and print
awk '/ERROR/ {print $1, $2, $5}' app.log    # Only ERROR lines, specific columns

# Count occurrences
awk '/ERROR/ {count++} END {print count}' app.log

# Sum numbers (e.g., response times)
awk '{sum += $5} END {print sum}' times.log

# Print if condition met
awk '$5 > 100 {print $0}' times.log   # Print if column 5 > 100
```

**SRE Real-World Examples:**
```bash
# Count errors by type
awk '/ERROR/ {errors[$3]++} END {for (e in errors) print e, errors[e]}' app.log

# Extract IPs from logs
awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c | sort -rn

# Calculate average response time
awk '{sum+=$5; count++} END {print sum/count}' response_times.log

# Find all requests that took > 2 seconds
awk '$5 > 2000 {print $0}' response_times.log
```

---

### 3. `sed` - Stream Editor (Find and Replace)

```bash
# Basic syntax: sed 's/find/replace/' file

# Replace first occurrence in each line
sed 's/ERROR/CRITICAL/' app.log

# Replace ALL occurrences in each line
sed 's/ERROR/CRITICAL/g' app.log

# Delete lines matching pattern
sed '/WARNING/d' app.log              # Remove WARNING lines

# Keep only lines matching pattern
sed -n '/ERROR/p' app.log            # Print only ERROR lines

# Edit file in-place
sed -i 's/http/https/g' config.txt   # Change file directly

# Print specific line numbers
sed -n '10,20p' app.log              # Print lines 10-20
```

**SRE Real-World Examples:**
```bash
# Replace IP addresses in config
sed 's/192.168.1.100/10.0.0.50/g' nginx.conf

# Remove commented lines
sed '/^#/d' config.txt

# Add text before each line
sed 's/^/[APP] /' app.log            # Prefix each line with [APP]

# Extract specific log time range
sed -n '/10:00:00/,/11:00:00/p' app.log
```

---

## 🔧 Part 2: Process Management (15 min)

### 1. View Processes

```bash
# List all processes
ps aux

# Find specific process
ps aux | grep nginx
ps aux | grep python

# Tree view (show parent-child)
pstree

# Live view (like Task Manager)
top              # Press 'q' to quit
htop             # Better version (if installed)

# Check specific process by PID
ps -p 1234       # Replace 1234 with actual PID
```

---

### 2. Manage Processes

```bash
# Kill a process
kill 1234                # Graceful termination
kill -9 1234             # Force kill (last resort!)

# Kill by name
pkill nginx              # Kill all nginx processes
killall python           # Kill all python processes

# Background a process
command &                # Run in background
nohup command &          # Run in background even after logout

# Check background jobs
jobs

# Bring to foreground
fg %1                    # Bring job 1 to foreground
```

**SRE Real-World:**
```bash
# Find and kill stuck process
ps aux | grep "stuck_app"
kill -9 [PID]

# Start app in background
nohup python app.py > /var/log/app.log 2>&1 &

# Check if application is running
ps aux | grep myapp || echo "App is down!"
```

---

### 3. System Monitoring

```bash
# CPU and Memory
top                     # Interactive
top -bn1 | head -20     # One-time snapshot

# Memory usage
free -h

# Disk I/O
iostat                  # Need sysstat package

# Network connections
netstat -tuln           # All listening ports
ss -tuln                # Modern alternative

# Check specific port
netstat -tuln | grep :8080
lsof -i :8080           # What's using port 8080?
```

---

## 🔗 Part 3: Advanced Command Chaining (15 min)

### 1. Pipes and Redirection

```bash
# Multiple pipes
cat app.log | grep ERROR | awk '{print $1, $2}' | sort | uniq

# Save intermediate results
grep ERROR app.log > errors.txt
cat errors.txt | wc -l

# Append to file
grep WARNING app.log >> errors.txt

# Redirect errors
command 2> errors.log              # Only errors
command > output.log 2>&1          # Both stdout and stderr
command &> all.log                 # Same as above (shorthand)
```

---

### 2. Conditional Execution

```bash
# AND (&&) - Run second only if first succeeds
mkdir backup && cp *.txt backup/

# OR (||) - Run second only if first fails  
ping google.com || echo "No internet!"

# Chaining
cd /tmp && mkdir test && cd test && touch file.txt
```

**SRE Real-World:**
```bash
# Only restart if config is valid
nginx -t && systemctl restart nginx

# Backup before deployment
cp app.py app.py.backup && git pull && systemctl restart myapp

# Check disk space, alert if needed
df -h | grep /dev/sda1 | awk '{print $5}' | grep -q "9[0-9]%" && echo "ALERT: Disk full!"
```

---

### 3. Subcommands and Variables

```bash
# Store command output in variable
TODAY=$(date +%Y-%m-%d)
echo "Backup from $TODAY"

# Use in filenames
cp app.log app.log.$TODAY

# Count and store
ERROR_COUNT=$(grep -c ERROR app.log)
echo "Found $ERROR_COUNT errors"

# Conditional based on output
if [ $ERROR_COUNT -gt 10 ]; then
    echo "Too many errors!"
fi
```

---

## 📜 Part 4: Basic Shell Scripting (10 min)

### Create Your First Script

```bash
# Create script file
cat > health_check.sh << 'EOF'
#!/bin/bash

# Simple health check script
echo "=== System Health Check ==="
echo ""

echo "1. Disk Space:"
df -h | grep /dev/sda1

echo ""
echo "2. Memory Usage:"
free -h | grep Mem

echo ""
echo "3. CPU Load:"
uptime

echo ""
echo "4. Top 5 Memory Processes:"
ps aux --sort=-%mem | head -6

echo ""
echo "5. Application Status:"
if ps aux | grep -q "[p]ython app.py"; then
    echo "✓ Application is running"
else
    echo "✗ Application is DOWN!"
fi

echo ""
echo "=== Health Check Complete ==="
EOF

# Make it executable
chmod +x health_check.sh

# Run it
./health_check.sh
```

---

### Create a Log Analyzer Script

```bash
cat > analyze_logs.sh << 'EOF'
#!/bin/bash

# Log analyzer script
LOG_FILE=${1:-app.log}  # First argument or default to app.log

echo "Analyzing: $LOG_FILE"
echo "======================="

# Count by log level
echo ""
echo "Log Level Summary:"
echo "  INFO:    $(grep -c INFO $LOG_FILE)"
echo "  WARNING: $(grep -c WARNING $LOG_FILE)"
echo "  ERROR:   $(grep -c ERROR $LOG_FILE)"

# Top errors
echo ""
echo "Top 5 Error Messages:"
grep ERROR $LOG_FILE | cut -d' ' -f5- | sort | uniq -c | sort -rn | head -5

# Time range
echo ""
echo "Log Time Range:"
echo "  First: $(head -1 $LOG_FILE | cut -d' ' -f1-2)"
echo "  Last:  $(tail -1 $LOG_FILE | cut -d' ' -f1-2)"

# Total lines
echo ""
echo "Total Log Lines: $(wc -l < $LOG_FILE)"
EOF

chmod +x analyze_logs.sh

# Run it
./analyze_logs.sh app.log
```

---

## 🏋️ Part 5: Hands-On Practice (Remaining time)

### Practice on EC2:

```bash
# 1. Create a practice directory
cd ~
mkdir linux_advanced
cd linux_advanced

# 2. Create sample log files
cat > app1.log << 'EOF'
2026-01-07 10:00:01 INFO Application started
2026-01-07 10:00:05 ERROR Database connection failed
2026-01-07 10:00:10 WARNING High memory usage: 85%
2026-01-07 10:00:15 INFO Request from 192.168.1.10
2026-01-07 10:00:20 ERROR Failed to send email
2026-01-07 10:00:25 INFO Processing 100 records
EOF

# 3. Practice commands
# Extract just timestamps
cut -d' ' -f1-2 app1.log

# Count each log level
awk '{print $3}' app1.log | sort | uniq -c

# Replace ERROR with CRITICAL
sed 's/ERROR/CRITICAL/g' app1.log

# Find all errors and warnings
grep -E "ERROR|WARNING" app1.log

# Create a backup script
cat > backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR=~/backups/$(date +%Y-%m-%d)
mkdir -p $BACKUP_DIR
cp *.log $BACKUP_DIR/
echo "Backed up logs to $BACKUP_DIR"
EOF
chmod +x backup.sh
./backup.sh
```

---

## 📝 Quick Commands Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `cut -d' ' -f1-3` | Extract columns | `cut -d' ' -f1 file.txt` |
| `awk '{print $1}'` | Print column | `awk '/ERROR/ {print $0}' log` |
| `sed 's/old/new/g'` | Replace text | `sed 's/http/https/g' file` |
| `ps aux \| grep app` | Find process | `ps aux \| grep nginx` |
| `kill -9 PID` | Force kill | `kill -9 1234` |
| `command &` | Run in background | `python app.py &` |
| `variable=$(command)` | Store output | `DATE=$(date)` |

---

## 🎯 What You'll Know After This:

✅ Text processing with cut, awk, sed  
✅ Process management (ps, kill, jobs)  
✅ System monitoring (top, free, df)  
✅ Advanced command chaining  
✅ Basic shell scripting  
✅ Creating automation scripts  

---

**Next: After this hour, move to Python modules!**

*Time: 60 minutes*
