# Shell Scripting Basics for DevOps/SRE
## Learn Bash Automation

---

## 🎯 Goals for This Session:
- Understand shell script structure
- Learn variables, conditionals, loops
- Create practical automation scripts

---

## 📚 Part 1: Basics (15 min)

### 1. Your First Script

```bash
#!/bin/bash
# This is a comment

echo "Hello, SRE!"
```

**Run it:**
```bash
chmod +x script.sh   # Make executable
./script.sh          # Run it
```

---

### 2. Variables

```bash
#!/bin/bash

# Define variables (NO spaces around =)
NAME="John"
SERVER="web-01"
PORT=8080

# Use variables (with $)
echo "User: $NAME"
echo "Server: $SERVER on port $PORT"

# Command output as variable
TODAY=$(date +%Y-%m-%d)
HOSTNAME=$(hostname)
echo "Today is $TODAY on $HOSTNAME"
```

---

### 3. User Input

```bash
#!/bin/bash

echo "Enter server name:"
read SERVER_NAME

echo "You entered: $SERVER_NAME"
```

---

### 4. Command Line Arguments

```bash
#!/bin/bash

# $0 = script name, $1 = first arg, $2 = second arg
echo "Script name: $0"
echo "First argument: $1"
echo "Second argument: $2"
echo "All arguments: $@"
echo "Number of arguments: $#"
```

**Run:** `./script.sh web-01 8080`

---

## 🔧 Part 2: Conditionals (15 min)

### If-Else

```bash
#!/bin/bash

DISK_USAGE=85

if [ $DISK_USAGE -gt 90 ]; then
    echo "🔴 CRITICAL: Disk usage is $DISK_USAGE%"
elif [ $DISK_USAGE -gt 80 ]; then
    echo "🟡 WARNING: Disk usage is $DISK_USAGE%"
else
    echo "🟢 OK: Disk usage is $DISK_USAGE%"
fi
```

### Comparison Operators

| Operator | Meaning | Example |
|----------|---------|---------|
| `-eq` | Equal | `[ $a -eq $b ]` |
| `-ne` | Not equal | `[ $a -ne $b ]` |
| `-gt` | Greater than | `[ $a -gt $b ]` |
| `-lt` | Less than | `[ $a -lt $b ]` |
| `-ge` | Greater or equal | `[ $a -ge $b ]` |
| `-le` | Less or equal | `[ $a -le $b ]` |

### String Comparisons

```bash
#!/bin/bash

STATUS="running"

if [ "$STATUS" == "running" ]; then
    echo "App is running"
elif [ "$STATUS" == "stopped" ]; then
    echo "App is stopped"
else
    echo "Unknown status"
fi

# Check if string is empty
if [ -z "$VAR" ]; then
    echo "Variable is empty"
fi
```

### File Checks

```bash
#!/bin/bash

FILE="/var/log/app.log"

if [ -f "$FILE" ]; then
    echo "File exists"
fi

if [ -d "/var/log" ]; then
    echo "Directory exists"
fi

if [ -r "$FILE" ]; then
    echo "File is readable"
fi
```

| Operator | Meaning |
|----------|---------|
| `-f` | File exists |
| `-d` | Directory exists |
| `-r` | File is readable |
| `-w` | File is writable |
| `-x` | File is executable |

---

## 🔄 Part 3: Loops (15 min)

### For Loop

```bash
#!/bin/bash

# Loop through list
for SERVER in web-01 web-02 db-01; do
    echo "Checking $SERVER..."
done

# Loop through numbers
for i in 1 2 3 4 5; do
    echo "Iteration $i"
done

# C-style loop
for ((i=1; i<=5; i++)); do
    echo "Count: $i"
done

# Loop through files
for FILE in /var/log/*.log; do
    echo "Found: $FILE"
done
```

### While Loop

```bash
#!/bin/bash

COUNT=1

while [ $COUNT -le 5 ]; do
    echo "Count: $COUNT"
    COUNT=$((COUNT + 1))
done
```

### Reading File Line by Line

```bash
#!/bin/bash

while read LINE; do
    echo "Processing: $LINE"
done < servers.txt
```

---

## 🛠️ Part 4: Functions (10 min)

```bash
#!/bin/bash

# Define function
check_server() {
    SERVER=$1
    echo "Checking $SERVER..."
    
    if ping -c 1 "$SERVER" &> /dev/null; then
        echo "✓ $SERVER is UP"
        return 0
    else
        echo "✗ $SERVER is DOWN"
        return 1
    fi
}

# Call function
check_server "google.com"
check_server "fake.server.xyz"
```

---

## 📝 Part 5: Practical Scripts

### Script 1: Health Check

```bash
#!/bin/bash

# health_check.sh - Check system health

echo "=== System Health Check ==="
echo ""

# Disk usage
DISK=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')
if [ $DISK -gt 80 ]; then
    echo "🔴 Disk: ${DISK}% (CRITICAL)"
else
    echo "🟢 Disk: ${DISK}%"
fi

# Memory usage
MEM=$(free | awk '/Mem/ {printf("%.0f", $3/$2 * 100)}')
if [ $MEM -gt 80 ]; then
    echo "🔴 Memory: ${MEM}% (CRITICAL)"
else
    echo "🟢 Memory: ${MEM}%"
fi

# CPU load
LOAD=$(uptime | awk -F'load average:' '{print $2}' | cut -d, -f1 | xargs)
echo "📊 CPU Load: $LOAD"

# Uptime
echo "⏱️ Uptime: $(uptime -p)"

echo ""
echo "=== Check Complete ==="
```

---

### Script 2: Backup Script

```bash
#!/bin/bash

# backup.sh - Backup important directories

BACKUP_DIR="/tmp/backups"
DATE=$(date +%Y%m%d_%H%M%S)
SOURCE="/var/log"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Create backup
BACKUP_FILE="$BACKUP_DIR/backup_$DATE.tar.gz"
tar -czf "$BACKUP_FILE" "$SOURCE" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✓ Backup created: $BACKUP_FILE"
    echo "  Size: $(du -h $BACKUP_FILE | cut -f1)"
else
    echo "✗ Backup failed!"
    exit 1
fi
```

---

### Script 3: Log Monitor

```bash
#!/bin/bash

# log_monitor.sh - Monitor log file for errors

LOG_FILE=${1:-"/var/log/syslog"}

echo "Monitoring: $LOG_FILE"
echo "Press Ctrl+C to stop"
echo "---"

tail -f "$LOG_FILE" | while read LINE; do
    if echo "$LINE" | grep -q "ERROR"; then
        echo "🔴 $LINE"
    elif echo "$LINE" | grep -q "WARNING"; then
        echo "🟡 $LINE"
    fi
done
```

---

## 🎯 Quick Reference

```bash
# Variables
VAR="value"
echo $VAR

# Command substitution
TODAY=$(date)

# Conditionals
if [ condition ]; then
    # code
fi

# Loops
for item in list; do
    # code
done

# Functions
function_name() {
    # code
}

# Exit codes
exit 0  # Success
exit 1  # Error

# Redirect
command > file    # Overwrite
command >> file   # Append
command 2>/dev/null  # Hide errors
```

---

## 🏋️ Practice on EC2:

1. SSH into your EC2 instance
2. Create a `scripts` directory: `mkdir ~/scripts`
3. Create and run the health check script
4. Create and run the backup script

---

**Practice these and let me know when you're done!**
