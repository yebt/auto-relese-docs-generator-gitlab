# Cache Feature Implementation Summary

## Overview
Implemented a comprehensive caching system with the `--cache` flag that enables recovery from interruptions during the changelog generation process.

## Changes Made

### 1. New Files Created

#### `src/cache_manager.py`
- **CacheManager class**: Manages all caching operations
- **Key methods**:
  - `save_commits_cache()`: Saves the list of commits between tags
  - `load_commits_cache()`: Loads cached commits
  - `save_commit_detail()`: Saves individual commit details incrementally
  - `load_commit_details()`: Loads all cached commit details
  - `clear_cache()`: Clears cache for specific tags or all cache

#### `CACHE_USAGE.md`
- Complete documentation of the cache feature
- Usage examples and scenarios
- Performance impact analysis
- Cache management instructions

#### `CHANGELOG_CACHE_FEATURE.md` (this file)
- Summary of implementation changes

### 2. Modified Files

#### `main.py`
- Added `--cache` argument to command-line parser
- Passes `use_cache` parameter to `ChangelogGenerator`

#### `src/changelog_generator.py`
- **`__init__` method**: Added `use_cache` parameter and cache manager initialization
- **`get_commits_between_tags` method**:
  - Checks cache before fetching from GitLab
  - Saves fetched commits to cache
  - Displays cache status messages
- **`get_commit_details` method**:
  - Loads previously cached commit details
  - Fetches only missing commits
  - Saves each commit detail incrementally
  - Handles interruptions gracefully (KeyboardInterrupt)
  - Shows progress with cache statistics
- **`generate` method**: Updated to pass tags to `get_commit_details`
- Fixed lint warnings (removed unused imports and variables)

#### `README.md`
- Added cache feature to features list
- Added cache usage examples
- Updated project structure to show `.cache/` directory and `cache_manager.py`
- Added reference to `CACHE_USAGE.md`
- Updated documentation list

#### `.gitignore`
- Added `.cache/` directory to ignore list

## How It Works

### Phase 1: Commit List Caching
When fetching commits between tags:
1. **First run**: Fetches from GitLab API and saves to cache
2. **Subsequent runs**: Loads from cache instantly

**Cache file**: `.cache/commits_{from_tag}_{to_tag}_{hash}.json`

### Phase 2: Incremental Commit Details Caching
When fetching detailed information for each commit:
1. Loads any previously cached details
2. Skips commits already in cache
3. Fetches only missing commits from GitLab
4. Saves each commit detail immediately after fetching
5. On interruption (Ctrl+C or error), progress is preserved

**Cache file**: `.cache/details_{from_tag}_{to_tag}_{hash}.json`

## Usage Examples

```bash
# Enable cache
python main.py --cache

# With specific tags
python main.py --from-tag v1.0.0 --to-tag v2.0.0 --cache

# Recovery scenario
python main.py --cache  # Interrupted at commit 100/254
python main.py --cache  # Resumes from commit 101
```

## Benefits

1. **Recovery from interruptions**: Ctrl+C, network errors, API failures
2. **Time savings**: No need to re-fetch hundreds of commits
3. **API efficiency**: Reduces calls to GitLab API
4. **Flexibility**: Fix Gemini API issues without re-fetching commit data

## Technical Details

### Cache Key Generation
- Uses MD5 hash of `{from_tag}:{to_tag}:{cache_type}`
- Ensures unique cache per tag combination
- Prevents conflicts between different tag ranges

### Error Handling
- **KeyboardInterrupt**: Saves progress and displays resume message
- **API errors**: Saves partial progress before raising exception
- **Cache corruption**: Falls back to fetching from GitLab

### Cache Storage Format
JSON files with UTF-8 encoding containing:
- Commit metadata (id, title, message, author, date)
- Commit details (diffs, stats)
- Tag information for validation

## Testing Recommendations

1. **Normal flow**: Run with `--cache` and verify completion
2. **Interruption**: Press Ctrl+C during commit details fetch, then resume
3. **Gemini failure**: Let commit fetch complete, simulate Gemini error, then retry
4. **Cache validation**: Verify `.cache/` directory contains JSON files
5. **Without cache**: Verify tool still works without `--cache` flag

## Performance Impact

**Example with 254 commits**:
- Without cache: ~8.5 minutes (254 × 2 seconds)
- With cache (after interruption at 100): ~5 minutes (saves ~3.5 minutes)
- With full cache: ~1 second (instant load)

## Backward Compatibility

✅ Fully backward compatible:
- `--cache` flag is optional
- Default behavior unchanged when flag not used
- No breaking changes to existing functionality
