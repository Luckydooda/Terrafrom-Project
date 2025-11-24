# ⚡ Caching Dependencies - Quick Reference

## 🎯 The Basics

**What is caching?** Store dependencies between runs to speed up workflows (80-90% faster!)

**When to cache?** Always cache package manager dependencies (pip, npm, maven, etc.)

---

## 📝 Standard Template

### Python (pip)
```yaml
- name: Cache pip packages
  uses: actions/cache@v4
  id: cache
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-

- name: Install dependencies
  run: pip install -r requirements.txt

- name: Check cache status
  run: |
    if [ "${{ steps.cache.outputs.cache-hit }}" == "true" ]; then
      echo "✅ Cache HIT"
    else
      echo "❌ Cache MISS"
    fi
```

### Node.js (npm)
```yaml
- name: Cache npm packages
  uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-

- name: Install dependencies
  run: npm ci
```

---

## 🚀 Built-in Caching (Easier!)

### Python
```yaml
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.11'
    cache: 'pip'  # Automatic caching!
```

### Node.js
```yaml
- name: Set up Node.js
  uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'  # Automatic caching!
```

---

## 🔑 Cache Key Components

```yaml
key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
      │              │    │
      │              │    └─ Hash of dependency file (changes when deps change)
      │              └────── Package manager identifier
      └───────────────────── Operating system (ubuntu-latest, windows-latest, etc.)
```

**Why each part?**
- `runner.os`: Different OS = different binaries
- Package manager: Different managers = different cache
- `hashFiles()`: Changes when dependencies change = new cache

---

## 📍 Common Cache Paths

| Package Manager | Linux/Mac Path | Windows Path |
|----------------|----------------|--------------|
| pip | `~/.cache/pip` | `%LOCALAPPDATA%\pip\Cache` |
| npm | `~/.npm` | `%APPDATA%\npm-cache` |
| yarn | `~/.yarn/cache` | `%LOCALAPPDATA%\Yarn\Cache` |
| Maven | `~/.m2/repository` | `%USERPROFILE%\.m2\repository` |
| Gradle | `~/.gradle/caches` | `%USERPROFILE%\.gradle\caches` |

---

## ✅ Best Practices Checklist

- [ ] Include `${{ runner.os }}` in cache key
- [ ] Use `hashFiles()` for dependency files
- [ ] Add `restore-keys` for fallback
- [ ] Cache step comes **before** install step
- [ ] Use `id:` to check cache status
- [ ] Print cache hit/miss for debugging

---

## 🔍 Debugging

**Check logs for:**
- `Cache restored from key: ...` = ✅ Cache HIT
- `Cache not found for input keys: ...` = ❌ Cache MISS

**Common issues:**
- Cache not working? Check key matches exactly
- Wrong path? Verify OS-specific paths
- Cache too large? Use more specific paths (not `~/.cache`)

---

## 📊 Performance

| Scenario | Time | Downloads |
|----------|------|-----------|
| Without cache | 2-5 min | ~500MB |
| With cache (hit) | 10-30 sec | ~50MB |
| **Savings** | **80-90%** | **90%** |

---

## 🎓 Remember

1. **First run** = Cache MISS (expected, creates cache)
2. **Second run** = Cache HIT (fast!)
3. **When deps change** = New cache key = Cache MISS (then creates new cache)
4. **Cache limit**: 10GB per repository (old caches auto-deleted)

---

**📚 For detailed explanations, see [`caching-dependencies-guide.md`](caching-dependencies-guide.md)**

