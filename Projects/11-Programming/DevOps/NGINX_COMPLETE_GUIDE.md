# Nginx Complete Guide for SRE
## What You Learned Today + Reference

---

## 🎯 What is Nginx?

**Nginx = Flexible Server** (Does what you configure!)

```
Client → Nginx → Backend(s)
           ↓
    • Web Server
    • Reverse Proxy
    • Load Balancer
    • SSL Termination
```

---

## 📁 Config Files

| Path | Purpose |
|------|---------|
| `/etc/nginx/nginx.conf` | Main config |
| `/etc/nginx/sites-available/` | Site configs |
| `/etc/nginx/sites-enabled/` | Active sites (symlinks) |
| `/var/log/nginx/access.log` | Access logs |
| `/var/log/nginx/error.log` | Error logs |

---

## 🔧 Essential Commands

```bash
nginx -t              # Test config (ALWAYS do this first!)
nginx -s reload       # Reload without downtime
nginx -s stop         # Stop immediately
systemctl status nginx
systemctl restart nginx
```

---

## 📝 Config Modes

### Mode 1: Web Server (Serve Files)
```nginx
server {
    listen 80;
    root /var/www/html;
    
    location / {
        index index.html;
    }
}
```

### Mode 2: Reverse Proxy
```nginx
server {
    listen 80;
    
    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Mode 3: Load Balancer
```nginx
upstream backend {
    server app1:8080 weight=3;  # 60% traffic
    server app2:8080 weight=1;  # 20% traffic
    server app3:8080 weight=1;  # 20% traffic
}

server {
    listen 80;
    
    location / {
        proxy_pass http://backend;
    }
}
```

### Mode 4: SSL Termination
```nginx
server {
    listen 443 ssl;
    ssl_certificate /etc/ssl/cert.pem;
    ssl_certificate_key /etc/ssl/key.pem;
    
    location / {
        proxy_pass http://backend:8080;
    }
}
```

---

## 🔀 Load Balancing Methods

| Method | Config | Use Case |
|--------|--------|----------|
| Round Robin | (default) | Equal distribution |
| Least Conn | `least_conn;` | Send to least busy |
| IP Hash | `ip_hash;` | Same client → same server |
| Weight | `weight=3` | More traffic to powerful servers |

```nginx
upstream backend {
    least_conn;  # Use least connections method
    server app1:8080 weight=3;
    server app2:8080;
    server app3:8080 backup;  # Only if others fail
}
```

---

## 📍 Location Block Priority

```nginx
# 1. Exact match (highest priority)
location = /health {
    return 200 "OK";
}

# 2. Prefix match with ^~
location ^~ /static/ {
    root /var/www;
}

# 3. Regex match
location ~* \.(jpg|png|gif)$ {
    expires 30d;
}

# 4. Prefix match (lowest priority)
location / {
    proxy_pass http://backend;
}
```

---

## 🔍 Useful Headers

```nginx
location / {
    proxy_pass http://backend;
    
    # Pass client info to backend
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

---

## 🚨 Health Checks

```nginx
# Simple health endpoint
location /health {
    return 200 "OK\n";
    add_header Content-Type text/plain;
}

# Or proxy to app health
location /health {
    proxy_pass http://backend/health;
}
```

---

## 🎯 Interview Questions & Answers

**Q1: Nginx vs Apache?**
> Nginx is event-driven (many connections, few threads). Apache is process-based. Nginx is faster for static content and proxying.

**Q2: What is upstream?**
> A group of backend servers for load balancing.

**Q3: Zero-downtime reload?**
> `nginx -t && nginx -s reload` - gracefully restarts workers.

**Q4: Load balancing methods?**
> Round-robin (default), least_conn, ip_hash, weight.

**Q5: What's reverse proxy?**
> Nginx sits between client and backend. Client talks to Nginx, Nginx talks to backend.

**Q6: How to troubleshoot?**
> Check logs: `tail -f /var/log/nginx/error.log`, test config: `nginx -t`.

---

## 🧪 Hands-On Practice (Done Today!)

| Scenario | What You Did |
|----------|--------------|
| ✅ Web Server | Created location blocks |
| ✅ Reverse Proxy | Forwarded to Python server |
| ✅ Load Balancer | Distributed to 3 backends |

---

## 🔗 Quick Reference

```bash
# Install
apt install nginx -y

# Start
systemctl start nginx

# Test config
nginx -t

# Reload (zero downtime)
nginx -s reload

# Check logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

---

*Practiced on Killercoda - Jan 8, 2026*
