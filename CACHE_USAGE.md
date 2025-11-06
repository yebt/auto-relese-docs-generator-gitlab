# Cache Feature Documentation

## Overview

The `--cache` flag enables caching functionality that saves intermediate results during the changelog generation process. This allows recovery from interruptions and avoids re-fetching data from GitLab when the process is interrupted.

## How It Works

The cache system operates in two critical phases:

### 1. Fetching Commits Between Tags

When you run the tool with `--cache`, it:
- **First run**: Fetches commits between the specified tags from GitLab and saves them to cache
- **Subsequent runs**: Loads commits from cache instead of fetching from GitLab

**Cache key**: Based on `from_tag` and `to_tag` combination

**Example output**:
```
💾 Loaded 254 commits from cache

📋 Commits to be analyzed (254):
   1. a1b2c3d4 - Fix authentication bug
   2. e5f6g7h8 - Add new feature
   ...
```

### 2. Fetching Commit Details (Incremental)

This is the most time-consuming operation. The cache system:
- **Saves each commit detail incrementally** as it's fetched
- **Resumes from where it stopped** if interrupted (Ctrl+C, error, etc.)
- **Skips already-cached commits** on subsequent runs

**Example workflow**:

**First run** (interrupted at commit 100/254):
```
✔ Found 254 new commits between v3.92.4 and v3.94.15
⚠ Interrupted! Fetched 100 new details, 100 total
💾 Progress saved to cache. Run again with --cache to resume.
```

**Second run** (resumes from commit 101):
```
💾 Loaded 254 commits from cache
💾 Loaded 100 commit details from cache
✔ Fetched details for 254 commits (100 from cache)
```

## Usage

### Basic Usage

```bash
# Enable cache for the default tags (last two)
python main.py --cache

# Enable cache with specific tags
python main.py --from-tag v1.0.0 --to-tag v2.0.0 --cache
```

### Recovery Scenarios

#### Scenario 1: Interrupted During Commit Details Fetch

```bash
# First attempt - interrupted
python main.py --cache --from-tag v3.92.4 --to-tag v3.94.15
# ... fetches 100 of 254 commits, then Ctrl+C

# Resume - continues from commit 101
python main.py --cache --from-tag v3.92.4 --to-tag v3.94.15
# Loads 100 from cache, fetches remaining 154
```

#### Scenario 2: Gemini API Error After Fetching

```bash
# First attempt - Gemini fails
python main.py --cache --from-tag v3.92.4 --to-tag v3.94.15
# ... fetches all 254 commits successfully
# ... Gemini API error occurs

# Fix Gemini API key in .env, then retry
python main.py --cache --from-tag v3.92.4 --to-tag v3.94.15
# Loads all 254 commits from cache immediately
# No need to re-fetch from GitLab!
```

## Cache Location

Cache files are stored in the `.cache` directory in the project root:

```
.cache/
├── commits_v3.92.4_v3.94.15_<hash>.json      # Commit list
└── details_v3.92.4_v3.94.15_<hash>.json      # Commit details
```

## Cache Management

### Clearing Cache

The cache is automatically managed per tag combination. To manually clear cache:

```bash
# Remove the entire cache directory
rm -rf .cache
```

### Cache Invalidation

Cache is automatically invalidated when:
- You use different `from_tag` or `to_tag` values
- The cache files are deleted manually

## Benefits

1. **Time Savings**: Avoid re-fetching hundreds of commits from GitLab
2. **Resilience**: Recover from interruptions without losing progress
3. **Cost Efficiency**: Reduce API calls to GitLab
4. **Flexibility**: Fix Gemini API issues without re-fetching commit data

## Performance Impact

**Without cache**:
- 254 commits × ~2 seconds per commit = ~8.5 minutes

**With cache** (after interruption):
- 100 cached commits × ~0.01 seconds = ~1 second
- 154 remaining commits × ~2 seconds = ~5 minutes
- **Total**: ~5 minutes (saves ~3.5 minutes)

## Important Notes

1. **Cache is optional**: The tool works perfectly without `--cache`
2. **Cache is safe**: Interruptions are handled gracefully
3. **Cache is automatic**: No manual management needed
4. **Cache is per-tag**: Different tag combinations use different cache files
