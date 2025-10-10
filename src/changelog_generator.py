#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple
import gitlab
from google import genai
from google.genai import types
from halo import Halo
from dotenv import load_dotenv


class ChangelogGenerator:
    """
    Generates commercial and technical changelogs from GitLab repository
    using Gemini AI to analyze commits between the last two tags.
    """
    
    def __init__(self):
        """Initialize the changelog generator with credentials from .env"""
        load_dotenv()
        
        # Load credentials
        self.gitlab_token = os.getenv('GITLAB_ACCESS_TOKEN')
        self.gitlab_project_id = os.getenv('GITLAB_PROJECT_ID')
        self.gemini_token = os.getenv('GEMINI_TOKEN')
        
        # Validate credentials
        if not all([self.gitlab_token, self.gitlab_project_id, self.gemini_token]):
            raise ValueError(
                "Missing required environment variables. Please check your .env file.\n"
                "Required: GITLAB_ACCESS_TOKEN, GITLAB_PROJECT_ID, GEMINI_TOKEN"
            )
        
        # Initialize clients
        self.gl = None
        self.project = None
        self.gemini_client = None
        
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
    
    def get_last_two_tags(self) -> Tuple[str, str]:
        """Get the last two tags from the repository"""
        spinner = Halo(text='Fetching repository tags...', spinner='dots')
        spinner.start()
        
        try:
            tags = self.project.tags.list(order_by='updated', sort='desc', per_page=2, get_all=False)
            
            if len(tags) < 2:
                spinner.fail('Not enough tags found. Need at least 2 tags.')
                raise ValueError('Repository must have at least 2 tags')
            
            latest_tag = tags[0].name
            previous_tag = tags[1].name
            
            spinner.succeed(f'Found tags: {latest_tag} (latest) and {previous_tag} (previous)')
            return latest_tag, previous_tag
        except Exception as e:
            spinner.fail(f'Failed to fetch tags: {str(e)}')
            raise
    
    def get_commits_between_tags(self, tag1: str, tag2: str) -> List[Dict]:
        """Get only the new commits introduced between two tags (tag2..tag1)"""
        spinner = Halo(text=f'Fetching commits between {tag2} and {tag1}...', spinner='dots')
        spinner.start()
        
        try:
            # Use GitLab's compare API to get only commits between the two tags
            # This returns commits that are in tag1 but not in tag2 (the new commits)
            comparison = self.project.repository_compare(tag2, tag1)
            
            # Get the commit objects from the comparison
            commit_shas = [commit['id'] for commit in comparison['commits']]
            
            # Fetch full commit objects
            commits = []
            for sha in commit_shas:
                commit = self.project.commits.get(sha)
                commits.append(commit)
            
            spinner.succeed(f'Found {len(commits)} new commits between {tag2} and {tag1}')
            return commits
        except Exception as e:
            spinner.fail(f'Failed to fetch commits: {str(e)}')
            raise
    
    def get_commit_details(self, commits: List) -> List[Dict]:
        """Get detailed information for each commit including diffs"""
        spinner = Halo(text='Fetching commit details and diffs...', spinner='dots')
        spinner.start()
        
        commit_details = []
        
        try:
            for i, commit in enumerate(commits):
                spinner.text = f'Fetching commit details {i+1}/{len(commits)}...'
                
                # Get full commit details
                full_commit = self.project.commits.get(commit.id)
                
                # Get diff
                diff = full_commit.diff()
                
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
            
            spinner.succeed(f'Fetched details for {len(commit_details)} commits')
            return commit_details
        except Exception as e:
            spinner.fail(f'Failed to fetch commit details: {str(e)}')
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

*📋 CHANGELOG COMERCIAL - Release {tag_name}*

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
        
        try:
            response = self.gemini_client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt
            )
            
            spinner.succeed('Commercial changelog generated')
            return response.text
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
        
        try:
            response = self.gemini_client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt
            )
            
            spinner.succeed('Technical changelog generated')
            return response.text
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
    
    def generate(self) -> Path:
        """Main method to generate changelogs"""
        print("\n" + "="*60)
        print("🚀 GitLab Changelog Generator with Gemini AI")
        print("="*60 + "\n")
        
        # Connect to services
        self.connect_gitlab()
        self.connect_gemini()
        
        # Get tags
        latest_tag, previous_tag = self.get_last_two_tags()
        
        # Get commits
        commits = self.get_commits_between_tags(latest_tag, previous_tag)
        
        if not commits:
            print("\n⚠️  No commits found between tags")
            return None
        
        # Get commit details
        commit_details = self.get_commit_details(commits)
        
        # Prepare context
        spinner = Halo(text='Preparing context for AI analysis...', spinner='dots')
        spinner.start()
        context = self.prepare_context_for_gemini(commit_details, latest_tag)
        spinner.succeed('Context prepared')
        
        # Generate changelogs
        commercial_changelog = self.generate_commercial_changelog(context, latest_tag)
        technical_changelog = self.generate_technical_changelog(context, latest_tag)
        
        # Save changelogs
        output_dir = self.save_changelogs(commercial_changelog, technical_changelog, latest_tag)
        
        print("\n" + "="*60)
        print("✅ Changelog generation completed successfully!")
        print("="*60)
        print(f"\n📁 Output directory: {output_dir.absolute()}")
        print(f"📄 Files generated:")
        print(f"   - Changelog_comercial_{latest_tag}.md")
        print(f"   - Changelog_tech_{latest_tag}.md")
        print("\n💬 Files are formatted for WhatsApp/Telegram sharing\n")
        
        return output_dir


def main():
    """Entry point for the script"""
    try:
        generator = ChangelogGenerator()
        generator.generate()
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
