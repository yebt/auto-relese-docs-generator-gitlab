#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GitLab Changelog Generator with Gemini AI

This script generates two types of changelogs from GitLab repository:
1. Commercial Changelog - For sales team and clients
2. Technical Changelog - For development team

It analyzes commits between the last two tags using Gemini AI.
"""

import argparse
from src.changelog_generator import ChangelogGenerator

def main():
    """Entry point for the script"""
    parser = argparse.ArgumentParser(description='Generate changelogs from GitLab commits between tags')
    parser.add_argument('--from-tag', help='Older tag to start from')
    parser.add_argument('--to-tag', help='Newer tag to end at')
    parser.add_argument('--cache', action='store_true', help='Enable caching for commits and commit details to allow recovery from interruptions')
    parser.add_argument('--api', action='store_true', help='Use Gemini API instead of Gemini CLI (requires GEMINI_TOKEN in .env)')
    args = parser.parse_args()
    
    try:
        # Use CLI by default, unless --api flag is provided
        use_cli = not args.api
        generator = ChangelogGenerator(use_cache=args.cache, use_cli=use_cli)
        generator.generate(args.from_tag, args.to_tag)
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user")
        import sys
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}")
        import sys
        sys.exit(1)

if __name__ == '__main__':
    main()