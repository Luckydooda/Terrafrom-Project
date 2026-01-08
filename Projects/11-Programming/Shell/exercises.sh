#!/bin/bash
# Shell Scripting Exercises - Practice on EC2
# Complete each exercise and run the script to verify

echo "=============================================="
echo "Shell Scripting Exercises"
echo "=============================================="

# ==================================================
# EXERCISE 1: Variables and User Input
# ==================================================
echo ""
echo "📝 Exercise 1: Variables and User Input"
echo "----------------------------------------"

# TODO: Create a variable called SERVER_NAME with value "web-01"
# TODO: Create a variable called PORT with value 8080
# TODO: Print "Server: web-01 is running on port 8080"

# YOUR CODE HERE:
SERVER_NAME="Web-01"
PORT=8080
echo "server: $SERVER_NAME is running on $PORT"


# Expected output: "Server: web-01 is running on port 8080"

# ==================================================
# EXERCISE 2: Command Substitution
# ==================================================
echo ""
echo "📝 Exercise 2: Command Substitution"
echo "----------------------------------------"

# TODO: Store current date in variable TODAY using $(date +%Y-%m-%d)
# TODO: Store hostname in variable HOST using $(hostname)
# TODO: Print "Report generated on [date] from [hostname]"

# YOUR CODE HERE:

TODAY=$(date +%Y-%m-%d)
HOST=$(hostname)
echo "Report generated on $TODAY from $HOST"
# Expected output: "Report generated on 2026-01-08 from ip-xxx-xxx"

# ==================================================
# EXERCISE 3: Conditionals
# ==================================================
echo ""
echo "📝 Exercise 3: Conditionals"
echo "----------------------------------------"

DISK_USAGE=87

# TODO: Write an if-elif-else that:
#   - If DISK_USAGE > 90: print "🔴 CRITICAL"
#   - If DISK_USAGE > 80: print "🟡 WARNING"
#   - Else: print "🟢 OK"

# YOUR CODE HERE:
if [ $DISK_USAGE -gt 90 ]; then
echo "🔴 CRITICAL"
elif [ $DISK_USAGE -gt 80 ]; then
echo "🟡 WARNING"
else
echo "🟢 OK"
fi  

# Expected output (for 87): "🟡 WARNING"

# ==================================================
# EXERCISE 4: For Loop
# ==================================================
echo ""
echo "📝 Exercise 4: For Loop"
echo "----------------------------------------"

# TODO: Loop through servers: web-01 web-02 db-01 cache-01
# TODO: Print "Checking [server]..." for each

# YOUR CODE HERE:
for server in web-01 web-02 db-01 cache-01; do
   echo "Checking $server...."
done
# Expected output:
# Checking web-01...
# Checking web-02...
# Checking db-01...
# Checking cache-01...

# ==================================================
# EXERCISE 5: While Loop with Counter
# ==================================================
echo ""
echo "📝 Exercise 5: While Loop"
echo "----------------------------------------"

# TODO: Create a counter starting at 1
# TODO: While counter <= 5, print "Attempt [counter]"
# TODO: Increment counter each iteration

# YOUR CODE HERE:
counter=1
while [ $counter -le 5 ] ; do
   echo "Attempt $counter"
   counter=$((counter+1))
done

# Expected output:
# Attempt 1
# Attempt 2
# Attempt 3
# Attempt 4
# Attempt 5

# ==================================================
# EXERCISE 6: Function
# ==================================================
echo ""
echo "📝 Exercise 6: Function"
echo "----------------------------------------"

# TODO: Create a function called greet() that:
#   - Takes one argument (name)
#   - Prints "Hello, [name]! Welcome to the server."

# YOUR CODE HERE:
greet() {
    echo "Hello, $1! Welcome to the server."

}

greet "LUCKY"

# Call the function:
# greet "SRE"

# Expected output: "Hello, SRE! Welcome to the server."

# ==================================================
# EXERCISE 7: File Check
# ==================================================
echo ""
echo "📝 Exercise 7: File Check"
echo "----------------------------------------"

# TODO: Check if /etc/passwd exists
#   - If yes: print "✓ File exists"
#   - If no: print "✗ File not found"

# YOUR CODE HERE:
if [ -f /etc/passwd ]; then
    echo "✓ File exists"
else
    echo "✗ File not found"
fi


# Expected output: "✓ File exists"

# ==================================================
# EXERCISE 8: String Comparison
# ==================================================
echo ""
echo "📝 Exercise 8: String Comparison"
echo "----------------------------------------"

STATUS="running"

# TODO: If STATUS equals "running", print "App is UP"
# TODO: Else print "App is DOWN"

# YOUR CODE HERE:
if [ $STATUS == "running" ]; then
    echo "App is UP"
else
    echo "App is DOWN"
fi

# Expected output: "App is UP"

# ==================================================
# EXERCISE 9: Array and Loop
# ==================================================
echo ""
echo "📝 Exercise 9: Array and Loop"
echo "----------------------------------------"

# TODO: Create an array called SERVICES with: nginx mysql redis
# TODO: Loop through and print "Service: [name]" for each

# YOUR CODE HERE:
SERVICES=(nginx mysql redis)
for name in "${SERVICES[@]}"; do  
    echo "SERVICE: $name"
done    

# Expected output:
# Service: nginx
# Service: mysql
# Service: redis

# ==================================================
# EXERCISE 10: Combine It All - Mini Health Check
# ==================================================
echo ""
echo "📝 Exercise 10: Mini Health Check Script"
echo "----------------------------------------"

# TODO: Create a function check_disk() that:
#   1. Gets disk usage with: df -h / | awk 'NR==2 {print $5}' | tr -d '%'
#   2. If usage > 80: print "⚠️ Disk Warning: X%"
#   3. Else: print "✓ Disk OK: X%"

# YOUR CODE HERE:
check_disk(){
    DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')
    if [ $DISK_USAGE -gt 80 ]; then
        echo "⚠️ Disk Warning: $DISK_USAGE%"
    else
        echo "✓ Disk OK: $DISK_USAGE%"
    fi  

}

check_disk

# Call the function:
# check_disk

# Expected output: "✓ Disk OK: XX%" or "⚠️ Disk Warning: XX%"

echo ""
echo "=============================================="
echo "Done! Review your answers above."
echo "=============================================="
