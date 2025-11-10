#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gemini CLI Analyzer
Handles interaction with Gemini CLI for analyzing commits and generating changelogs
"""

import json
import subprocess
from typing import Dict, List
from halo import Halo


class GeminiCLIAnalyzer:
    """Manages interaction with Gemini CLI for local analysis"""
    
    def __init__(self):
        """Initialize the Gemini CLI analyzer"""
        self.verify_gemini_cli()
    
    def verify_gemini_cli(self) -> None:
        """Verify that Gemini CLI is installed and accessible"""
        try:
            result = subprocess.run(
                ['gemini', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode != 0:
                raise RuntimeError("Gemini CLI is not working properly")
        except FileNotFoundError:
            raise RuntimeError(
                "Gemini CLI not found. Please install it first:\n"
                "Visit: https://ai.google.dev/gemini-api/docs/cli"
            )
        except subprocess.TimeoutExpired:
            raise RuntimeError("Gemini CLI verification timed out")
    
    def _call_gemini_cli(self, prompt: str) -> str:
        """
        Call Gemini CLI in non-interactive mode using --prompt.
        """
        cmd = ['gemini', '--prompt', prompt]
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            if result.returncode != 0:
                raise RuntimeError(f"Gemini CLI error: {result.stderr}")
            return result.stdout.strip()
        except subprocess.TimeoutExpired:
            raise RuntimeError("Gemini CLI request timed out after 5 minutes")
    
    def analyze_commits_batch(self, commits_batch: List[Dict], batch_num: int, total_batches: int) -> Dict:
        """
        Analyze a batch of commits using Gemini CLI
        
        Args:
            commits_batch: List of commit details to analyze
            batch_num: Current batch number
            total_batches: Total number of batches
            
        Returns:
            Dictionary with categorized changes
        """
        spinner = Halo(
            text=f'Analyzing batch {batch_num}/{total_batches} with Gemini CLI...',
            spinner='dots'
        )
        spinner.start()
        
        # Prepare context for this batch
        context = self._prepare_batch_context(commits_batch)
        
        # Prepare analysis prompt
        prompt = """Analiza estos commits y categorízalos en:
- features: Nuevas características
- improvements: Mejoras a funcionalidad existente
- fixes: Correcciones de bugs
- breaking_changes: Cambios que rompen compatibilidad
- architecture: Cambios arquitectónicos
- dependencies: Cambios en dependencias
- performance: Mejoras de rendimiento
- security: Parches de seguridad
- testing: Cambios en tests
- docs: Cambios en documentación
- other: Otros cambios

Para cada commit, proporciona:
- category: La categoría principal
- title: Título descriptivo
- description: Descripción detallada
- technical_details: Detalles técnicos relevantes
- files_affected: Archivos principales afectados

Responde SOLO con un JSON válido con esta estructura:
{
  "commits": [
    {
      "id": "commit_id",
      "category": "category_name",
      "title": "título",
      "description": "descripción",
      "technical_details": "detalles técnicos",
      "files_affected": ["file1", "file2"]
    }
  ]
}"""
        
        # Combine prompt and context for CLI
        combined_prompt = f"{prompt}\n\n=== CONTEXTO DE COMMITS (LOTE {batch_num}/{total_batches}) ===\n\n{context}"
        
        try:
            response = self._call_gemini_cli(combined_prompt)
            
            # Parse JSON response
            # Extract JSON from response (in case there's extra text)
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                json_str = response[json_start:json_end]
                result = json.loads(json_str)
            else:
                raise ValueError("No valid JSON found in response")
            
            spinner.succeed(f'Batch {batch_num}/{total_batches} analyzed')
            return result
        except json.JSONDecodeError as e:
            spinner.fail(f'Failed to parse Gemini response for batch {batch_num}')
            raise RuntimeError(f"Invalid JSON response from Gemini CLI: {str(e)}")
        except Exception:
            spinner.fail(f'Failed to analyze batch {batch_num}')
            raise
    
    def _prepare_batch_context(self, commits: List[Dict]) -> str:
        """Prepare context for a batch of commits"""
        context = "# Commits to Analyze\n\n"
        
        for commit in commits:
            context += f"## Commit {commit['id']}\n"
            context += f"**Author:** {commit['author']}\n"
            context += f"**Date:** {commit['date']}\n"
            context += f"**Message:**\n{commit['message']}\n\n"
            context += f"**Stats:** +{commit['stats']['additions']} -{commit['stats']['deletions']}\n\n"
            
            # Add file changes
            context += "**Files Changed:**\n"
            for diff_item in commit['diff'][:10]:  # Limit to 10 files per commit
                file_path = diff_item.get('new_path', diff_item.get('old_path', 'unknown'))
                context += f"- {file_path}\n"
                
                # Add diff snippet if available
                if 'diff' in diff_item and diff_item['diff']:
                    diff_lines = diff_item['diff'].split('\n')[:15]  # First 15 lines
                    context += f"  ```diff\n{chr(10).join(diff_lines)}\n  ```\n"
            
            context += "\n---\n\n"
        
        return context
    
    def generate_commercial_changelog(self, analyzed_commits: List[Dict], tag_name: str) -> str:
        """
        Generate commercial changelog from analyzed commits using Gemini CLI
        
        Args:
            analyzed_commits: List of analyzed and categorized commits
            tag_name: The release tag name
            
        Returns:
            Commercial changelog text
        """
        spinner = Halo(text='Generating commercial changelog...', spinner='dots')
        spinner.start()
        
        # Prepare summary context
        context = self._prepare_summary_context(analyzed_commits)
        
        prompt = f"""Basándote en el análisis de commits proporcionado, genera un CHANGELOG COMERCIAL para el release {tag_name}.

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
- Sé conciso pero informativo"""
        
        # Combine prompt and context
        combined_prompt = f"{prompt}\n\n=== RESUMEN ANALIZADO ===\n\n{context}"
        try:
            response = self._call_gemini_cli(combined_prompt)
            spinner.succeed('Commercial changelog generated')
            return response
        except Exception:
            spinner.fail('Failed to generate commercial changelog')
            raise
    
    def generate_technical_changelog(self, analyzed_commits: List[Dict], tag_name: str) -> str:
        """
        Generate technical changelog from analyzed commits using Gemini CLI
        
        Args:
            analyzed_commits: List of analyzed and categorized commits
            tag_name: The release tag name
            
        Returns:
            Technical changelog text
        """
        spinner = Halo(text='Generating technical changelog...', spinner='dots')
        spinner.start()
        
        # Prepare summary context
        context = self._prepare_summary_context(analyzed_commits)
        
        prompt = f"""Basándote en el análisis de commits proporcionado, genera un CHANGELOG TÉCNICO para el release {tag_name}.

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
- Sé detallado y preciso"""
        
        # Combine prompt and context
        combined_prompt = f"{prompt}\n\n=== RESUMEN ANALIZADO ===\n\n{context}"
        try:
            response = self._call_gemini_cli(combined_prompt)
            spinner.succeed('Technical changelog generated')
            return response
        except Exception:
            spinner.fail('Failed to generate technical changelog')
            raise
    
    def _prepare_summary_context(self, analyzed_commits: List[Dict]) -> str:
        """Prepare summary context from analyzed commits"""
        context = "# Analyzed Commits Summary\n\n"
        
        # Group by category
        categories = {}
        for commit_data in analyzed_commits:
            for commit in commit_data.get('commits', []):
                category = commit.get('category', 'other')
                if category not in categories:
                    categories[category] = []
                categories[category].append(commit)
        
        # Format by category
        for category, commits in categories.items():
            context += f"## {category.upper()}\n\n"
            for commit in commits:
                context += f"### {commit.get('title', 'No title')}\n"
                context += f"**ID:** {commit.get('id', 'unknown')}\n"
                context += f"**Description:** {commit.get('description', 'No description')}\n"
                context += f"**Technical Details:** {commit.get('technical_details', 'None')}\n"
                
                files = commit.get('files_affected', [])
                if files:
                    context += f"**Files:** {', '.join(files[:5])}\n"
                
                context += "\n"
            context += "---\n\n"
        
        return context
