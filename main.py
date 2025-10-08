#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GitLab Changelog Generator with Gemini AI

This script generates two types of changelogs from GitLab repository:
1. Commercial Changelog - For sales team and clients
2. Technical Changelog - For development team

It analyzes commits between the last two tags using Gemini AI.
"""

from src.changelog_generator import main

if __name__ == '__main__':
    main()