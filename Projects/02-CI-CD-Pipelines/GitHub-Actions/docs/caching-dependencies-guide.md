# 📦 Caching Dependencies in GitHub Actions - Complete Guide

## 🎯 What is Caching?

Caching in GitHub Actions allows you to **store and reuse files** between workflow runs, dramatically **speeding up your CI/CD pipelines**. Instead of downloading and installing dependencies every time, you can cache them and only re-download when they change.

---

## 🧠 Core Concepts

### 1. **Cache Key**
A unique identifier that determines which cache to use. Think of it like a label on a storage box.

```yaml
key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
```

**Components:**
- `${{ runner.os }}` - Operating system (ubuntu-latest, windows-latest, etc.)
- `pip` - Package manager identifier
- `${{ hashFiles('requirements.txt') }}` - Hash of dependency file

**Why hash files?** When `requirements.txt` changes, the hash changes, creating a new cache key. This ensures you get fresh dependencies when needed.

### 2. **Cache Path**
The directory where dependencies are stored on the runner.

```yaml
path: ~/.cache/pip  # Linux/Mac
path: C:\Users\runneradmin\AppData\Local\pip\Cache  # Windows
```

**Common cache paths:**
- **Python pip**: `~/.cache/pip` (Linux/Mac), `%LOCALAPPDATA%\pip\Cache` (Windows)
- **Node.js npm**: `~/.npm` (Linux/Mac), `%APPDATA%\npm-cache` (Windows)
- **Maven**: `~/.m2/repository`
- **Gradle**: `~/.gradle/caches`

### 3. **Restore Keys**
Fallback keys to use if exact match isn't found. Provides partial cache hits.

```yaml
restore-keys: |
  ${{ runner.os }}-pip-
  ${{ runner.os }}-
```

**How it works:**
1. First tries exact key match
2. If not found, tries restore-keys in order
3. Uses most recent partial match
4. If nothing found, cache miss (starts fresh)

---

## 🔍 Understanding Restore Keys - Deep Dive

Restore keys are **fallback patterns** that help you reuse caches even when your exact cache key doesn't match. Think of them as "partial matches" that can still speed up your workflow.

### Real-World Scenario Example

Let's say you have this cache configuration:

```yaml
key: Linux-pip-abc123def456  # Hash of requirements.txt
restore-keys: |
  Linux-pip-
  Linux-
```

**What happens in different situations:**

#### Scenario 1: Exact Match (Perfect Cache Hit) ✅
- **Your cache key**: `Linux-pip-abc123def456`
- **Existing cache**: `Linux-pip-abc123def456` ✅
- **Result**: Exact match found! Uses this cache (fastest)

#### Scenario 2: Partial Match (Still Fast!) ⚡
- **Your cache key**: `Linux-pip-abc123def456` (new hash because you added one package)
- **Existing cache**: `Linux-pip-xyz789ghi012` (old hash from previous requirements.txt)
- **Exact match**: ❌ Not found
- **Restore key check**: Tries `Linux-pip-` → ✅ Matches `Linux-pip-xyz789ghi012`!
- **Result**: Uses the old cache! You still get most packages cached, only the new one downloads (still much faster!)

#### Scenario 3: No Match (Cache Miss) ❌
- **Your cache key**: `Linux-pip-abc123def456`
- **Existing caches**: None
- **Exact match**: ❌ Not found
- **Restore key `Linux-pip-`**: ❌ Not found
- **Restore key `Linux-`**: ❌ Not found
- **Result**: Cache miss - downloads everything fresh

### Step-by-Step: How Restore Keys Work

```yaml
key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
restore-keys: |
  ${{ runner.os }}-pip-
  ${{ runner.os }}-
```

**The lookup process:**

1. **Try exact key**: `Linux-pip-abc123def456`
   - ✅ Found? → Use it! Done.
   - ❌ Not found? → Continue to step 2

2. **Try first restore key**: `Linux-pip-`
   - Looks for any cache starting with `Linux-pip-`
   - ✅ Found? → Use the **most recent** match! Done.
   - ❌ Not found? → Continue to step 3

3. **Try second restore key**: `Linux-`
   - Looks for any cache starting with `Linux-`
   - ✅ Found? → Use the **most recent** match! Done.
   - ❌ Not found? → Continue to step 4

4. **Cache miss**: No cache found, start fresh

### Why Restore Keys Matter

**Without restore keys:**
```
requirements.txt changes → Hash changes → New cache key → Cache miss → Slow install
```

**With restore keys:**
```
requirements.txt changes → Hash changes → New cache key → 
  Exact match fails → Restore key matches → Partial cache hit → 
  Only new packages download → Still fast! ⚡
```

### Practical Example

Imagine you have these caches in your repository:

```
Cache 1: Linux-pip-abc123 (from 2 days ago, requirements.txt had: requests, pytest)
Cache 2: Linux-pip-def456 (from 1 day ago, requirements.txt had: requests, pytest, flask)
Cache 3: Linux-pip-ghi789 (from today, requirements.txt has: requests, pytest, flask, django)
```

**Today's workflow:**
- **requirements.txt**: `requests`, `pytest`, `flask`, `django`, `numpy` (added numpy)
- **New hash**: `jkl012`
- **Cache key**: `Linux-pip-jkl012`

**What happens:**
1. Look for exact match `Linux-pip-jkl012` → ❌ Not found
2. Look for restore key `Linux-pip-` → ✅ Finds `Linux-pip-ghi789` (most recent)
3. **Uses Cache 3** which already has: requests, pytest, flask, django
4. Only downloads `numpy` (the new package)
5. **Result**: 80% faster than downloading everything!

### Restore Key Priority Order

Restore keys are checked **in order** (top to bottom), and GitHub uses the **most recent** match:

```yaml
restore-keys: |
  ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}  # Most specific
  ${{ runner.os }}-pip-                                         # Less specific
  ${{ runner.os }}-                                             # Least specific
```

**Why this order?**
- Most specific first = best match (closest to what you need)
- Less specific = broader fallback (still useful)
- Least specific = last resort (any cache for this OS)

### Visual Example

```
Your Cache Key: Linux-pip-NEW_HASH

Existing Caches:
├── Linux-pip-OLD_HASH_1 (3 days ago)
├── Linux-pip-OLD_HASH_2 (2 days ago)  ← Most recent match for "Linux-pip-"
├── Linux-node-OTHER_HASH (1 day ago)
└── Windows-pip-OTHER_HASH (today)

Lookup Process:
1. Exact match "Linux-pip-NEW_HASH"? ❌
2. Restore key "Linux-pip-"? ✅ Matches "Linux-pip-OLD_HASH_2" (most recent)
3. Result: Uses Linux-pip-OLD_HASH_2 cache! ⚡
```

---

## 📊 Cache Hit vs Cache Miss

### Cache Hit ✅
- Cache with matching key exists
- Dependencies restored from cache
- **Fast** - Usually takes seconds instead of minutes
- Workflow logs show: `Cache restored from key: ...`

### Cache Miss ❌
- No matching cache found
- Dependencies downloaded fresh
- **Slower** - Full download and install
- Workflow logs show: `Cache not found for input keys: ...`
- New cache is created after installation

---

## 🔧 Basic Implementation

### Python (pip) Example

```yaml
name: Caching Dependencies

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Cache pip packages
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run tests
        run: pytest
```

### Node.js (npm) Example

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

### Maven Example

```yaml
- name: Cache Maven dependencies
  uses: actions/cache@v4
  with:
    path: ~/.m2/repository
    key: ${{ runner.os }}-maven-${{ hashFiles('**/pom.xml') }}
    restore-keys: |
      ${{ runner.os }}-maven-
```

---

## 🎓 Advanced Patterns

### 1. **Multiple Cache Paths**

```yaml
- name: Cache multiple paths
  uses: actions/cache@v4
  with:
    path: |
      ~/.cache/pip
      ~/.cache/pre-commit
    key: ${{ runner.os }}-deps-${{ hashFiles('**/requirements.txt', '**/.pre-commit-config.yaml') }}
```

### 2. **Matrix-Specific Caching**

```yaml
strategy:
  matrix:
    python-version: ['3.9', '3.10', '3.11']

steps:
  - name: Cache pip packages
    uses: actions/cache@v4
    with:
      path: ~/.cache/pip
      key: ${{ runner.os }}-pip-${{ matrix.python-version }}-${{ hashFiles('**/requirements.txt') }}
```

### 3. **Conditional Caching**

```yaml
- name: Cache dependencies
  uses: actions/cache@v4
  if: github.event_name != 'pull_request'  # Skip cache on PRs
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
```

### 4. **Cache with Fallback Strategy**

> 💡 **See the "Understanding Restore Keys - Deep Dive" section above for detailed explanation with examples!**

```yaml
- name: Cache with restore keys
  uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
      ${{ runner.os }}-pip-
      ${{ runner.os }}-
```

**Restore key priority (checked in order):**
1. Exact match (full key) - `Linux-pip-abc123def456`
2. First restore key - `Linux-pip-abc123def456` (same hash, different context)
3. Second restore key - `Linux-pip-` (any pip cache for this OS)
4. Third restore key - `Linux-` (any cache for this OS)
5. No match (cache miss) - starts fresh

**Key insight**: Restore keys allow you to reuse caches even when your exact key doesn't match, making workflows faster when dependencies change slightly.

---

## 🚀 Built-in Caching Actions

Some setup actions have **built-in caching** that's easier to use:

### Python (setup-python)

```yaml
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.11'
    cache: 'pip'  # Automatically caches pip packages!
```

**Benefits:**
- No need for separate cache step
- Automatically handles cache key generation
- Works with `requirements.txt` or `pyproject.toml`

### Node.js (setup-node)

```yaml
- name: Set up Node.js
  uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'  # Automatically caches npm packages!
```

---

## 📈 Performance Impact

### Without Caching
```
Step: Install dependencies
Time: 2-5 minutes
Downloads: ~500MB
```

### With Caching (Cache Hit)
```
Step: Restore cache
Time: 10-30 seconds
Downloads: ~50MB (only new/changed packages)
```

**Time Savings: 80-90% faster!** ⚡

---

## ✅ Best Practices

### 1. **Use Hash-Based Keys**
```yaml
# ✅ GOOD: Hash changes when dependencies change
key: ${{ hashFiles('**/package-lock.json') }}

# ❌ BAD: Static key, never updates
key: my-dependencies
```

### 2. **Include OS in Cache Key**
```yaml
# ✅ GOOD: OS-specific cache
key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}

# ❌ BAD: Same cache for all OS (won't work!)
key: pip-${{ hashFiles('**/requirements.txt') }}
```

### 3. **Use Restore Keys for Partial Matches**
```yaml
# ✅ GOOD: Falls back to partial matches
restore-keys: |
  ${{ runner.os }}-pip-
  ${{ runner.os }}-

# ❌ BAD: No fallback, always cache miss if exact match fails
# (no restore-keys)
```

### 4. **Cache Before Installing**
```yaml
# ✅ GOOD: Cache step before install
- name: Cache dependencies
  uses: actions/cache@v4
  ...
- name: Install dependencies
  run: pip install -r requirements.txt

# ❌ BAD: Installing before caching (cache never gets populated)
```

### 5. **Use Specific Paths**
```yaml
# ✅ GOOD: Specific cache directory
path: ~/.cache/pip

# ❌ BAD: Too broad (caches unnecessary files)
path: ~/.cache
```

### 6. **Check Cache Status**
```yaml
- name: Cache dependencies
  uses: actions/cache@v4
  id: cache
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}

- name: Check cache status
  run: |
    if [ "${{ steps.cache.outputs.cache-hit }}" == "true" ]; then
      echo "✅ Cache hit! Dependencies restored."
    else
      echo "❌ Cache miss. Installing fresh dependencies."
    fi
```

---

## 🔍 Debugging Cache Issues

### Check Cache Status in Logs

Look for these messages in workflow logs:

**Cache Hit:**
```
Cache restored from key: Linux-pip-abc123def456
```

**Cache Miss:**
```
Cache not found for input keys: Linux-pip-abc123def456
```

### Common Issues

1. **Cache not being used**
   - Check cache key matches exactly
   - Verify cache path is correct
   - Ensure cache step runs before install

2. **Cache too large**
   - GitHub Actions cache limit: **10GB per repository**
   - Old caches are automatically deleted (LRU - Least Recently Used)
   - Use more specific paths

3. **Cache key not updating**
   - Verify `hashFiles()` includes correct file
   - Check file actually changed
   - Use `**/` glob pattern for nested files

---

## 🎯 Task 7 Implementation Guide

For your specific task, here's what you need:

```yaml
name: Caching Dependencies

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
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
      
      - name: Print cache status
        run: |
          if [ "${{ steps.cache.outputs.cache-hit }}" == "true" ]; then
            echo "✅ Cache HIT - Dependencies restored from cache"
          else
            echo "❌ Cache MISS - Installing fresh dependencies"
          fi
      
      - name: Run tests
        run: pytest
```

**Key Points:**
- `id: cache` - Gives the step an ID to reference outputs
- `hashFiles('**/requirements.txt')` - Creates hash of requirements file
- `steps.cache.outputs.cache-hit` - Boolean indicating if cache was found
- First run: Cache MISS (expected)
- Second run: Cache HIT (faster!)

---

## 📚 Additional Resources

- [GitHub Actions Cache Documentation](https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows)
- [actions/cache Action](https://github.com/actions/cache)
- [setup-python with caching](https://github.com/actions/setup-python#caching-packages-dependencies)

---

## 🎓 Summary

**Key Takeaways:**
1. ✅ Caching saves **80-90% of dependency installation time**
2. ✅ Use **hash-based keys** that change when dependencies change
3. ✅ Include **OS in cache key** for cross-platform compatibility
4. ✅ Use **restore-keys** for partial cache matches
5. ✅ **Check cache status** to verify it's working
6. ✅ **Cache before installing** dependencies

**Remember:** The first run will always be a cache miss. The second run should be a cache hit and much faster! 🚀

