#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple
import gitlab
from google import genai
from google.genai import types
from halo import Halo
from dotenv import load_dotenv
from .cache_manager import CacheManager


class ChangelogGenerator:
    """
    Generates commercial and technical changelogs from GitLab repository
    using Gemini AI to analyze commits between specified tags or last two tags.
    """
    
    def __init__(self, use_cache: bool = False):
        """Initialize the changelog generator with credentials from .env"""
        load_dotenv()
        
        # Load credentials
        self.gitlab_token = os.getenv('GITLAB_ACCESS_TOKEN')
        self.gitlab_project_id = os.getenv('GITLAB_PROJECT_ID')
        self.gemini_token = os.getenv('GEMINI_TOKEN')
        
        # Validate credentials1
        if not all([self.gitlab_token, self.gitlab_project_id, self.gemini_token]):
            raise ValueError(
                "Missing required environment variables. Please check your .env file.\n"
                "Required: GITLAB_ACCESS_TOKEN, GITLAB_PROJECT_ID, GEMINI_TOKEN"
            )
        
        # Initialize clients
        self.gl = None
        self.project = None
        self.gemini_client = None
        
        # Initialize cache manager
        self.use_cache = use_cache
        self.cache_manager = CacheManager() if use_cache else None
        
    def connect_gitlab(self) -> None:
        """Connect to GitLab API"""
        spinner = Halo(text='Connecting to GitLab...', spinner='dots')
        spinner.start()
        
        try:
            self.gl = gitlab.Gitlab(private_token=self.gitlab_token)
            self.gl.auth()
            self.project = self.gl.projects.get(self.gitlab_project_id)
            spinner.succeed(f'Connected to GitLab project: {self.project.name}')
        except Exception as e:
            spinner.fail(f'Failed to connect to GitLab: {str(e)}')
            raise
    
    def connect_gemini(self) -> None:
        """Connect to Gemini AI"""
        spinner = Halo(text='Connecting to Gemini AI...', spinner='dots')
        spinner.start()
        
        try:
            self.gemini_client = genai.Client(api_key=self.gemini_token)
            spinner.succeed('Connected to Gemini AI')
        except Exception as e:
            spinner.fail(f'Failed to connect to Gemini AI: {str(e)}')
            raise
    
    def get_tags(self, from_tag: str = None, to_tag: str = None) -> Tuple[str, str]:
        """Get the tags for changelog generation based on input parameters"""
        spinner = Halo(text='Fetching repository tags...', spinner='dots')
        spinner.start()
        
        try:
            # Get all tags sorted by updated desc
            tags = self.project.tags.list(order_by='updated', sort='desc', get_all=True)
            tag_names = [t.name for t in tags]
            
            if from_tag is None and to_tag is None:
                if len(tag_names) < 2:
                    spinner.fail('Not enough tags found. Need at least 2 tags.')
                    raise ValueError('Repository must have at least 2 tags')
                from_tag = tag_names[1]  # older
                to_tag = tag_names[0]  # newer
            elif to_tag is not None and from_tag is None:
                if to_tag not in tag_names:
                    spinner.fail(f'Tag {to_tag} not found')
                    raise ValueError(f'Tag {to_tag} not found')
                idx = tag_names.index(to_tag)
                if idx + 1 >= len(tag_names):
                    spinner.fail(f'No previous tag found before {to_tag}')
                    raise ValueError(f'No previous tag found before {to_tag}')
                from_tag = tag_names[idx + 1]
            elif from_tag is not None and to_tag is None:
                if from_tag not in tag_names:
                    spinner.fail(f'Tag {from_tag} not found')
                    raise ValueError(f'Tag {from_tag} not found')
                idx = tag_names.index(from_tag)
                if idx == 0:
                    spinner.fail(f'No next tag found after {from_tag}')
                    raise ValueError(f'No next tag found after {from_tag}')
                to_tag = tag_names[idx - 1]
            else:  # both specified
                if from_tag not in tag_names or to_tag not in tag_names:
                    missing = [t for t in [from_tag, to_tag] if t not in tag_names]
                    spinner.fail(f'Tags not found: {", ".join(missing)}')
                    raise ValueError(f'Tags not found: {", ".join(missing)}')
                idx_from = tag_names.index(from_tag)
                idx_to = tag_names.index(to_tag)
                if idx_from <= idx_to:
                    spinner.fail('from_tag must be older than to_tag in timeline')
                    raise ValueError('from_tag must be older than to_tag in timeline')
            
            # Get commits for display
            from_commit = next(t.commit['id'][:8] for t in tags if t.name == from_tag)
            to_commit = next(t.commit['id'][:8] for t in tags if t.name == to_tag)
            
            spinner.succeed(f'Found tags: {to_tag} (to) and {from_tag} (from)')
            print(f"   🏷️  {from_tag} → commit {from_commit}")
            print(f"   🏷️  {to_tag} → commit {to_commit}")
            print(f"   📊 Comparing: {from_tag}..{to_tag}\n")
            
            return from_tag, to_tag
        except Exception as e:
            spinner.fail(f'Failed to fetch tags: {str(e)}')
            raise
    
    def get_commits_between_tags(self, from_tag: str, to_tag: str) -> List[Dict]:
        """Get only the new commits introduced between two tags (from_tag..to_tag)"""
        # Check cache first if enabled
        if self.use_cache:
            cached_commits = self.cache_manager.load_commits_cache(from_tag, to_tag)
            if cached_commits:
                print(f'\n💾 Loaded {len(cached_commits)} commits from cache')
                print(f"\n📋 Commits to be analyzed ({len(cached_commits)}):")
                for i, commit in enumerate(cached_commits, 1):
                    short_hash = commit['id'][:8]
                    title = commit['title'][:60] + '...' if len(commit['title']) > 60 else commit['title']
                    print(f"   {i}. {short_hash} - {title}")
                print()
                return cached_commits
        
        spinner = Halo(text=f'Fetching commits between {from_tag} and {to_tag}...', spinner='dots')
        spinner.start()
        
        try:
            # Use GitLab's compare API to get only commits between the two tags
            # This returns commits that are in to_tag but not in from_tag (the new commits)
            comparison = self.project.repository_compare(from_tag, to_tag)
            
            # Get the commit objects from the comparison
            commit_shas = [commit['id'] for commit in comparison['commits']]
            
            # Fetch full commit objects
            commits = []
            for sha in commit_shas:
                commit = self.project.commits.get(sha)
                commits.append(commit)
            
            spinner.succeed(f'Found {len(commits)} new commits between {from_tag} and {to_tag}')
            
            # Save to cache if enabled
            if self.use_cache:
                self.cache_manager.save_commits_cache(from_tag, to_tag, commits)
                print('💾 Commits saved to cache')
            
            # Display commit hashes for visual verification
            if commits:
                print(f"\n📋 Commits to be analyzed ({len(commits)}):")
                for i, commit in enumerate(commits, 1):
                    short_hash = commit.id[:8]
                    title = commit.title[:60] + '...' if len(commit.title) > 60 else commit.title
                    print(f"   {i}. {short_hash} - {title}")
                print()
            
            return commits
        except Exception as e:
            spinner.fail(f'Failed to fetch commits: {str(e)}')
            raise
    
    def get_commit_details(self, commits: List, from_tag: str, to_tag: str) -> List[Dict]:
        """Get detailed information for each commit including diffs with incremental caching"""
        # Load cached details if cache is enabled
        cached_details = {}
        if self.use_cache:
            cached_details = self.cache_manager.load_commit_details(from_tag, to_tag)
            if cached_details:
                print(f'\n💾 Loaded {len(cached_details)} commit details from cache')
        
        spinner = Halo(text='Fetching commit details and diffs...', spinner='dots')
        spinner.start()
        
        commit_details = []
        fetched_count = 0
        
        try:
            for i, commit in enumerate(commits):
                # Handle both dict (from cache) and object (from GitLab) formats
                full_commit_id = commit.get('id') if isinstance(commit, dict) else commit.id
                
                # Check if this commit is already cached
                if self.use_cache and full_commit_id in cached_details:
                    commit_details.append(cached_details[full_commit_id])
                    spinner.text = f'Loading commit details {i+1}/{len(commits)} (from cache)...'
                    continue
                
                # Fetch from GitLab
                spinner.text = f'Fetching commit details {i+1}/{len(commits)}...'
                
                # Get full commit details
                full_commit = self.project.commits.get(full_commit_id)
                
                # Get diff
                diff = full_commit.diff(get_all=True)
                
                commit_info = {
                    'id': full_commit.id[:8],
                    'full_id': full_commit.id,
                    'message': full_commit.message,
                    'title': full_commit.title,
                    'author': full_commit.author_name,
                    'date': full_commit.created_at,
                    'diff': diff,
                    'stats': full_commit.stats
                }
                
                commit_details.append(commit_info)
                fetched_count += 1
                
                # Save to cache incrementally if enabled
                if self.use_cache:
                    self.cache_manager.save_commit_detail(from_tag, to_tag, full_commit.id, commit_info)
            
            cached_msg = f' ({len(commit_details) - fetched_count} from cache)' if self.use_cache and len(cached_details) > 0 else ''
            spinner.succeed(f'Fetched details for {len(commit_details)} commits{cached_msg}')
            return commit_details
        except KeyboardInterrupt:
            spinner.warn(f'Interrupted! Fetched {fetched_count} new details, {len(commit_details)} total')
            if self.use_cache:
                print('💾 Progress saved to cache. Run again with --cache to resume.')
            raise
        except Exception as e:
            spinner.fail(f'Failed to fetch commit details: {str(e)}')
            if self.use_cache and len(commit_details) > 0:
                print(f'💾 Partial progress saved to cache ({len(commit_details)} commits)')
            raise
    
    def prepare_context_for_gemini(self, commits: List[Dict], tag_name: str) -> str:
        """Prepare commit data as context for Gemini AI"""
        context = f"# Release: {tag_name}\n\n"
        context += f"Total commits: {len(commits)}\n\n"
        context += "## Commits:\n\n"
        
        for commit in commits:
            context += f"### Commit {commit['id']}\n"
            context += f"**Author:** {commit['author']}\n"
            context += f"**Date:** {commit['date']}\n"
            context += f"**Message:**\n{commit['message']}\n\n"
            context += f"**Stats:** +{commit['stats']['additions']} -{commit['stats']['deletions']}\n\n"
            
            # Add diff information (limited to avoid token limits)
            context += "**Changes:**\n"
            for diff_item in commit['diff'][:5]:  # Limit to first 5 files per commit
                context += f"- File: {diff_item.get('new_path', diff_item.get('old_path', 'unknown'))}\n"
                context += f"  Type: {diff_item.get('new_file', False) and 'new' or diff_item.get('deleted_file', False) and 'deleted' or 'modified'}\n"
                
                # Add a snippet of the diff (limited)
                if 'diff' in diff_item and diff_item['diff']:
                    diff_lines = diff_item['diff'].split('\n')[:20]  # First 20 lines
                    context += f"  Diff snippet:\n```\n{chr(10).join(diff_lines)}\n```\n"
            
            context += "\n---\n\n"
        
        return context
    
    def generate_commercial_changelog(self, context: str, tag_name: str) -> str:
        """Generate commercial changelog using Gemini AI"""
        spinner = Halo(text='Generating commercial changelog with Gemini AI...', spinner='dots')
        spinner.start()
        
        prompt = f"""Eres un experto en comunicación comercial y product management. 

Analiza los siguientes commits de un release de software y genera un changelog COMERCIAL para el equipo de ventas y clientes.

{context}

IMPORTANTE: El formato debe ser compatible con WhatsApp/Telegram usando emojis y formato de texto enriquecido.

Estructura requerida:

**📋 CHANGELOG COMERCIAL - Release {tag_name}**

*🎯 RESUMEN EJECUTIVO*
[Descripción breve y clara del release en 2-3 líneas]

*✨ NUEVAS CARACTERÍSTICAS*
🟢 [Característica 1]: Descripción clara del valor para el cliente
🟢 [Característica 2]: Descripción clara del valor para el cliente

*🔧 MEJORAS*
🔵 [Mejora 1]: Cómo beneficia al usuario
🔵 [Mejora 2]: Cómo beneficia al usuario

*🐛 CORRECCIONES*
🟡 [Fix 1]: Problema resuelto en lenguaje simple
🟡 [Fix 2]: Problema resuelto en lenguaje simple

*⚠️ CAMBIOS IMPORTANTES*
🔴 [Cambio 1]: Qué debe saber el cliente
🔴 [Cambio 2]: Qué debe saber el cliente

*💡 VALOR APORTADO*
[Explicación del impacto positivo general del release]

*🎯 OBJETIVOS ALCANZADOS*
✅ [Objetivo 1]
✅ [Objetivo 2]

*📌 NOTAS ADICIONALES*
[Información relevante para comunicar al cliente]

Reglas:
- NO uses términos técnicos innecesarios
- Enfócate en el VALOR y BENEFICIOS para el cliente
- Usa lenguaje claro y profesional
- Los emojis deben ayudar a identificar rápidamente el tipo de cambio
- Sé conciso pero informativo
"""
        
        # Configure structured output
        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema={
                "type": "object",
                "properties": {
                    "content": {"type": "string"}
                },
                "required": ["content"]
            }
        )
        
        try:
            response = self.gemini_client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt,
                config=config
            )
            
            spinner.succeed('Commercial changelog generated')
            return response.parsed['content']
        except Exception as e:
            spinner.fail(f'Failed to generate commercial changelog: {str(e)}')
            raise
    
    def generate_technical_changelog(self, context: str, tag_name: str) -> str:
        """Generate technical changelog using Gemini AI"""
        spinner = Halo(text='Generating technical changelog with Gemini AI...', spinner='dots')
        spinner.start()
        
        prompt = f"""Eres un experto en desarrollo de software y documentación técnica.

Analiza los siguientes commits de un release de software y genera un changelog TÉCNICO para el equipo de desarrollo.

{context}

IMPORTANTE: El formato debe ser compatible con WhatsApp/Telegram usando emojis y formato de texto enriquecido.

Estructura requerida:

*🔧 CHANGELOG TÉCNICO - Release {tag_name}*

*📊 RESUMEN TÉCNICO*
[Descripción técnica del release, arquitectura afectada, componentes modificados]

*✨ NUEVAS FUNCIONALIDADES*
🟢 [Feature 1]: Implementación técnica, APIs, componentes
🟢 [Feature 2]: Implementación técnica, APIs, componentes

*🔧 MEJORAS TÉCNICAS*
🔵 [Mejora 1]: Optimizaciones, refactoring, performance
🔵 [Mejora 2]: Optimizaciones, refactoring, performance

*🐛 BUGS CORREGIDOS*
🟡 [Bug 1]: Descripción técnica del problema y solución
🟡 [Bug 2]: Descripción técnica del problema y solución

*⚠️ BREAKING CHANGES*
🔴 [Breaking 1]: Cambios que rompen compatibilidad
🔴 [Breaking 2]: Cambios que rompen compatibilidad

*🏗️ CAMBIOS DE ARQUITECTURA*
🟣 [Cambio 1]: Modificaciones estructurales importantes
🟣 [Cambio 2]: Modificaciones estructurales importantes

*📦 DEPENDENCIAS*
[Nuevas dependencias, actualizaciones, deprecaciones]

*⚡ PERFORMANCE*
[Mejoras de rendimiento, optimizaciones]

*🔒 SEGURIDAD*
[Parches de seguridad, vulnerabilidades corregidas]

*🧪 TESTING*
[Nuevos tests, cobertura, mejoras en testing]

*⚠️ PROBLEMAS CONOCIDOS*
[Issues conocidos, limitaciones, workarounds]

*🎯 OBJETIVOS TÉCNICOS ALCANZADOS*
✅ [Objetivo 1]
✅ [Objetivo 2]

*💡 VALOR TÉCNICO APORTADO*
[Impacto técnico del release: mantenibilidad, escalabilidad, etc.]

*📝 NOTAS PARA DESARROLLADORES*
[Información importante para el equipo técnico, migraciones, configuraciones]

Reglas:
- USA términos técnicos precisos
- Incluye detalles de implementación relevantes
- Menciona archivos, funciones, clases modificadas cuando sea relevante
- Los emojis deben ayudar a identificar rápidamente el tipo de cambio
- Sé detallado y preciso
"""
        
        # Configure structured output
        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema={
                "type": "object",
                "properties": {
                    "content": {"type": "string"}
                },
                "required": ["content"]
            }
        )
        
        try:
            response = self.gemini_client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt,
                config=config
            )
            
            spinner.succeed('Technical changelog generated')
            return response.parsed['content']
        except Exception as e:
            spinner.fail(f'Failed to generate technical changelog: {str(e)}')
            raise
    
    def save_changelogs(self, commercial: str, technical: str, tag_name: str) -> Path:
        """Save both changelogs to files in results directory"""
        spinner = Halo(text='Saving changelogs...', spinner='dots')
        spinner.start()
        
        try:
            # Create results directory if it doesn't exist
            results_dir = Path('results')
            results_dir.mkdir(exist_ok=True)
            
            # Create release-specific directory with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            release_dir = results_dir / f"{tag_name}_{timestamp}"
            release_dir.mkdir(exist_ok=True)
            
            # Save commercial changelog
            commercial_file = release_dir / f"Changelog_comercial_{tag_name}.md"
            commercial_file.write_text(commercial, encoding='utf-8')
            
            # Save technical changelog
            technical_file = release_dir / f"Changelog_tech_{tag_name}.md"
            technical_file.write_text(technical, encoding='utf-8')
            
            spinner.succeed(f'Changelogs saved to: {release_dir}')
            return release_dir
        except Exception as e:
            spinner.fail(f'Failed to save changelogs: {str(e)}')
            raise
    
    def generate(self, from_tag: str = None, to_tag: str = None) -> Path:
        """Main method to generate changelogs"""
        print("\n" + "="*60)
        print("🚀 GitLab Changelog Generator with Gemini AI")
        print("="*60 + "\n")
        
        # Connect to services
        self.connect_gitlab()
        self.connect_gemini()
        
        # Get tags
        from_tag, to_tag = self.get_tags(from_tag, to_tag)
        
        # Get commits
        commits = self.get_commits_between_tags(from_tag, to_tag)
        
        if not commits:
            print("\n⚠️  No commits found between tags")
            return None
        
        # Get commit details
        commit_details = self.get_commit_details(commits, from_tag, to_tag)
        
        # Prepare context
        spinner = Halo(text='Preparing context for AI analysis...', spinner='dots')
        spinner.start()
        context = self.prepare_context_for_gemini(commit_details, to_tag)
        spinner.succeed('Context prepared')
        
        # Generate changelogs
        commercial_changelog = self.generate_commercial_changelog(context, to_tag)
        technical_changelog = self.generate_technical_changelog(context, to_tag)
        
        # Save changelogs
        output_dir = self.save_changelogs(commercial_changelog, technical_changelog, to_tag)
        
        print("\n" + "="*60)
        print("✅ Changelog generation completed successfully!")
        print("="*60)
        print(f"\n📁 Output directory: {output_dir.absolute()}")
        print("📄 Files generated:")
        print(f"   - Changelog_comercial_{to_tag}.md")
        print(f"   - Changelog_tech_{to_tag}.md")
        print("\n💬 Files are formatted for WhatsApp/Telegram sharing\n")
        
        return output_dir
