# Linux Basics for DevOps/SRE (1 Hour Session)

## 🎯 Goals for This Hour:
- Understand Linux file system structure
- Master essential commands for daily DevOps work
- Practice file/directory operations
- Learn permissions (critical for SRE!)

---

## 📂 Part 1: Linux File System (15 min)

### The Directory Tree

```
/                    (Root - everything starts here)
├── bin/            Binary executables (ls, cat, grep)
├── etc/            Configuration files (nginx.conf, ssh_config)
├── var/            Variable data (logs, cache, temp files)
│   └── log/        ⭐ MOST IMPORTANT FOR SRE - All logs live here!
├── home/           User home directories
│   └── username/   Your personal space
├── opt/            Optional software (Jenkins, custom apps)
├── tmp/            Temporary files (cleared on reboot)
└── usr/            User programs and libraries
    └── local/      Locally installed software
```

### 🎯 SRE Focus Areas:
- **`/var/log/`** - Where you'll spend 50% of your debugging time
- **`/etc/`** - Configuration files you'll edit
- **`/opt/`** - Where your apps might live
- **`/home/`** - Your workspace

---

## 🔧 Part 2: Essential Commands (30 min)

### 1. Navigation Commands

```bash
pwd                 # Print Working Directory (where am I?)
ls                  # List files
ls -la              # List all files with details (MOST USED!)
cd /var/log         # Change directory
cd ..               # Go up one level
cd ~                # Go to home directory
cd -                # Go to previous directory
```

**Practice:**
```bash
pwd                         # See current location
cd /var/log                # Go to logs
ls -la                     # List all log files
cd /etc                    # Go to config directory
ls -la | grep nginx        # Find nginx configs
cd -                       # Go back to /var/log
```

---

### 2. File Viewing Commands

```bash
cat file.txt               # Print entire file
cat error.log | head -20   # First 20 lines
cat error.log | tail -20   # Last 20 lines
tail -f app.log            # ⭐ CRITICAL: Follow log in real-time!
less file.txt              # View large files (q to quit)
```

**SRE Real-World Example:**
```bash
# Watching application logs live
tail -f /var/log/app/application.log

# Check last 50 errors
grep ERROR /var/log/app.log | tail -50
```

---

### 3. Searching Commands (SUPER IMPORTANT!)

```bash
# grep - Search inside files
grep "error" app.log                    # Find "error" in file
grep -i "error" app.log                 # Case-insensitive
grep -r "database" /var/log/            # Recursive search in directory
grep -n "error" app.log                 # Show line numbers

# find - Search for files
find /var/log -name "*.log"             # Find all .log files
find /var/log -name "error*"            # Find files starting with "error"
find /var/log -mtime -1                 # Files modified in last 24h
find /var/log -size +100M               # Files larger than 100MB
```

**SRE Real-World Example:**
```bash
# Find all error logs from today
find /var/log -name "*error*" -mtime 0

# Search for "OutOfMemory" in all logs
grep -r "OutOfMemory" /var/log/

# Find which log file has "500 Internal Server Error"
grep -r "500 Internal Server Error" /var/log/ | head -5
```

---

### 4. File Operations

```bash
touch newfile.txt          # Create empty file
mkdir mydir                # Create directory
mkdir -p path/to/nested    # Create nested directories
cp file.txt backup.txt     # Copy file
cp -r dir1 dir2            # Copy directory recursively
mv oldname.txt newname.txt # Rename/move file
rm file.txt                # Delete file
rm -rf directory/          # Delete directory (⚠️ DANGEROUS!)
```

**SRE Practice:**
```bash
# Create backup of config before editing
cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.backup

# Archive old logs
mkdir /var/log/archive
mv /var/log/app.log.old /var/log/archive/
```

---

### 5. Permissions (CRITICAL FOR SRE!)

```bash
ls -la                     # View permissions
chmod 755 script.sh        # Make script executable
chmod 644 file.txt         # Read/write for owner, read for others
chown user:group file.txt  # Change ownership
```

**Permission Format:** `rwxrwxrwx` = User, Group, Others

| Number | Permission | Meaning |
|--------|------------|---------|
| **r** = 4 | Read | Can read file |
| **w** = 2 | Write | Can modify file |
| **x** = 1 | Execute | Can run as script |

**Common Combinations:**
- `755` = rwxr-xr-x (Scripts you want to execute)
- `644` = rw-r--r-- (Config files)
- `600` = rw------- (Secrets - only you can read!)

**SRE Example:**
```bash
# Make deployment script executable
chmod +x deploy.sh

# Secure a private key
chmod 600 ~/.ssh/id_rsa

# Check who owns a log file
ls -la /var/log/app.log
```

---

### 6. System Information

```bash
whoami                    # Current user
hostname                  # Server name
uptime                    # How long server has been running
df -h                     # Disk space (human-readable)
du -sh /var/log           # Directory size
free -h                   # Memory usage
ps aux                    # All running processes
ps aux | grep nginx       # Find nginx processes
top                       # Live process monitor (q to quit)
```

**SRE Health Check Commands:**
```bash
# Check disk space
df -h

# Check memory
free -h

# Check CPU and memory usage
top

# See what's using most disk space
du -sh /var/log/* | sort -h

# Check if app is running
ps aux | grep "myapp"
```

---

## 💡 Part 3: Command Chaining (10 min)

```bash
# Pipe (|) - Send output of one command to another
cat app.log | grep ERROR | wc -l          # Count errors

# Redirect (>) - Save output to file
grep ERROR app.log > errors.txt            # Overwrite
grep ERROR app.log >> errors.txt           # Append

# AND (&&) - Run second command only if first succeeds
mkdir backup && cp *.txt backup/

# OR (||) - Run second command only if first fails
ping google.com || echo "No internet!"
```

**SRE Real Examples:**
```bash
# Extract errors and save to file
grep ERROR /var/log/app.log > /tmp/today_errors.txt

# Count 500 errors in last hour
grep "500" /var/log/nginx/access.log | wc -l

# Restart app only if config is valid
nginx -t && systemctl restart nginx
```

---

## 🎯 Part 4: Hands-On Practice (5 min)

Try these on your **AWS EC2 instance** or **local Linux VM**:

```bash
# 1. Navigate to logs and find errors
cd /var/log
ls -la
grep -i "error" * 2>/dev/null | head -10

# 2. Check system health
df -h              # Disk space
free -h            # Memory
uptime             # Server uptime

# 3. Find large files
find /var/log -size +10M

# 4. Create a practice directory
cd ~
mkdir devops_practice
cd devops_practice
touch test.txt
echo "Hello DevOps!" > test.txt
cat test.txt
```

---

## 📝 Quick Reference Card (Save This!)

| Task | Command |
|------|---------|
| Where am I? | `pwd` |
| List files detailed | `ls -la` |
| View file | `cat file.txt` |
| Follow logs live | `tail -f app.log` |
| Search in file | `grep "error" file.log` |
| Find files | `find /path -name "*.log"` |
| Make executable | `chmod +x script.sh` |
| Check disk space | `df -h` |
| Check processes | `ps aux \| grep app` |
| Count lines | `wc -l file.txt` |

---

## 🏆 What You Should Know After This Hour:

✅ Where logs live (`/var/log`)  
✅ How to search files (`grep`)  
✅ How to find files (`find`)  
✅ How to watch live logs (`tail -f`)  
✅ File permissions (755, 644, 600)  
✅ Basic system health checks  

---

**Next Steps:**
- Practice on a real Linux server (AWS EC2 free tier)
- Try debugging a real application log
- Learn `vim` or `nano` for editing files

*Time: ~60 minutes*  
*Difficulty: Beginner → Intermediate*
