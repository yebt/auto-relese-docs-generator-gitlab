#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cache Manager for GitLab Changelog Generator
Handles caching of commits and commit details to allow recovery from interruptions
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any


class CacheManager:
    """Manages caching of commits and commit details"""

    def __init__(self, cache_dir: str = ".cache"):
        """Initialize cache manager with cache directory"""
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def _generate_cache_key(self, from_tag: str, to_tag: str, cache_type: str) -> str:
        """Generate a unique cache key based on tags and cache type"""
        key_string = f"{from_tag}:{to_tag}:{cache_type}"
        hash_key = hashlib.md5(key_string.encode()).hexdigest()
        return f"{cache_type}_{from_tag}_{to_tag}_{hash_key}.json"

    def save_commits_cache(
        self, from_tag: str, to_tag: str, commits: List[Any]
    ) -> None:
        """Save commits list to cache"""
        cache_key = self._generate_cache_key(from_tag, to_tag, "commits")
        cache_file = self.cache_dir / cache_key

        # Convert commit objects to serializable format
        commits_data = []
        for commit in commits:
            commits_data.append(
                {
                    "id": commit.id,
                    "title": commit.title,
                    "message": getattr(commit, "message", ""),
                    "author_name": getattr(commit, "author_name", ""),
                    "created_at": getattr(commit, "created_at", ""),
                }
            )

        cache_data = {
            "from_tag": from_tag,
            "to_tag": to_tag,
            "commits": commits_data,
            "count": len(commits_data),
        }

        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(cache_data, f, indent=2, ensure_ascii=False)

    def load_commits_cache(self, from_tag: str, to_tag: str) -> Optional[List[Dict]]:
        """Load commits list from cache"""
        cache_key = self._generate_cache_key(from_tag, to_tag, "commits")
        cache_file = self.cache_dir / cache_key

        if not cache_file.exists():
            return None

        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                cache_data = json.load(f)
            return cache_data["commits"]
        except Exception:
            return None

    def save_commit_detail(
        self, from_tag: str, to_tag: str, commit_id: str, detail: Dict
    ) -> None:
        """Save a single commit detail to cache"""
        cache_key = self._generate_cache_key(from_tag, to_tag, "details")
        cache_file = self.cache_dir / cache_key

        # Load existing cache or create new
        if cache_file.exists():
            with open(cache_file, "r", encoding="utf-8") as f:
                cache_data = json.load(f)
        else:
            cache_data = {"from_tag": from_tag, "to_tag": to_tag, "details": {}}

        # Add or update the commit detail
        cache_data["details"][commit_id] = detail

        # Save back to file
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(cache_data, f, indent=2, ensure_ascii=False)

    def load_commit_details(self, from_tag: str, to_tag: str) -> Dict[str, Dict]:
        """Load all cached commit details"""
        cache_key = self._generate_cache_key(from_tag, to_tag, "details")
        cache_file = self.cache_dir / cache_key

        if not cache_file.exists():
            return {}

        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                cache_data = json.load(f)
            return cache_data.get("details", {})
        except Exception:
            return {}

    def clear_cache(self, from_tag: str = None, to_tag: str = None) -> None:
        """Clear cache for specific tags or all cache"""
        if from_tag and to_tag:
            # Clear specific cache
            for cache_type in ["commits", "details"]:
                cache_key = self._generate_cache_key(from_tag, to_tag, cache_type)
                cache_file = self.cache_dir / cache_key
                if cache_file.exists():
                    cache_file.unlink()
        else:
            # Clear all cache
            for cache_file in self.cache_dir.glob("*.json"):
                cache_file.unlink()
