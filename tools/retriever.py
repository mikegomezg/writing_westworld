import os
import re
import json
import yaml
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import argparse

class StoryRetriever:
    """Context retrieval system for story development"""
    
    # File type codes
    TYPES = {
        'CH': 'Character',
        'WO': 'World', 
        'TH': 'Theme',
        'BE': 'Beat',
        'IN': 'Influence',
        'SL': 'Storyline'
    }
    
    def __init__(self, root_path: Path = None):
        self.root = root_path or Path.cwd().parent  # Go up from tools/
        self.canon_dir = self.root / 'canon'
        self.storylines_dir = self.canon_dir / 'storylines'
        self.inactive_dir = self.root / 'inactive'
        self.daily_dir = self.root / 'daily'
        
    def find_files_by_code(self, codes: List[str]) -> Dict[str, List[Path]]:
        """Find all files matching given type codes"""
        results = {'canon': [], 'working': [], 'inactive': []}
        
        # Search canon (including storylines subfolder)
        if self.canon_dir.exists():
            for file in self.canon_dir.rglob('*.md'):
                if any(file.name.startswith(f"{code}-") for code in codes):
                    results['canon'].append(file)
        
        # Search working (root)
        for file in self.root.glob('*.md'):
            if any(file.name.startswith(f"{code}-") for code in codes):
                results['working'].append(file)
                
        # Search inactive
        if self.inactive_dir.exists():
            for file in self.inactive_dir.glob('*.md'):
                if any(file.name.startswith(f"{code}-") for code in codes):
                    results['inactive'].append(file)
                    
        return results
    
    def find_storylines(self) -> List[Path]:
        """Find all storyline files"""
        storylines = []
        if self.storylines_dir.exists():
            storylines.extend(self.storylines_dir.glob('SL-*.md'))
        return storylines
    
    def find_beats_by_storyline(self, storyline_name: str) -> List[Path]:
        """Find all beats belonging to a storyline"""
        beats = []
        
        # Search all locations for beat files
        for location in [self.canon_dir, self.root, self.inactive_dir]:
            if location.exists():
                for file in location.rglob('BE-*.md'):
                    metadata = self.extract_metadata(file)
                    if metadata.get('storyline') == storyline_name:
                        beats.append(file)
        
        return beats
    
    def search_content(self, keywords: List[str], files: List[Path]) -> List[Tuple[Path, int]]:
        """Search file content for keywords, return files with match count"""
        matches = []
        
        for file_path in files:
            try:
                content = file_path.read_text(encoding='utf-8').lower()
                match_count = sum(content.count(kw.lower()) for kw in keywords)
                if match_count > 0:
                    matches.append((file_path, match_count))
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
                
        # Sort by match count (descending)
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches
    
    def extract_metadata(self, file_path: Path) -> Dict:
        """Extract front matter metadata from file"""
        try:
            content = file_path.read_text(encoding='utf-8')
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    # Parse YAML front matter
                    import yaml
                    try:
                        return yaml.safe_load(parts[1])
                    except:
                        # Fallback to simple parsing
                        metadata = {}
                        for line in parts[1].strip().split('\n'):
                            if ':' in line:
                                key, value = line.split(':', 1)
                                metadata[key.strip()] = value.strip()
                        return metadata
        except Exception:
            pass
        return {}
    
    def extract_context(self, file_path: Path, max_lines: int = 20) -> str:
        """Extract relevant context from file"""
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')
            
            # Skip metadata if present
            start_idx = 0
            if lines[0] == '---':
                for i, line in enumerate(lines[1:], 1):
                    if line == '---':
                        start_idx = i + 1
                        break
            
            # Extract meaningful content
            content_lines = lines[start_idx:start_idx + max_lines]
            # Remove empty lines at start
            while content_lines and not content_lines[0].strip():
                content_lines.pop(0)
            
            return '\n'.join(content_lines)
        except Exception as e:
            return f"Error extracting from {file_path}: {e}"
    
    def find_influences_for_themes(self, themes: List[str]) -> List[Path]:
        """Find influence files related to themes"""
        influences = []
        
        # Get all influence files
        influence_files = []
        for location in [self.canon_dir, self.root, self.inactive_dir]:
            if location.exists():
                influence_files.extend(location.rglob('IN-*.md'))
        
        # Check which influences relate to themes
        for inf_file in influence_files:
            content = inf_file.read_text(encoding='utf-8').lower()
            for theme in themes:
                theme_name = theme.replace('TH-', '').replace('.md', '').replace('-', ' ')
                if theme_name in content:
                    influences.append(inf_file)
                    break
        
        return influences
    
    def build_context(self, query: str = None, types: List[str] = None, 
                     keywords: List[str] = None, storyline: str = None) -> Dict:
        """Build complete context for a query"""
        
        # Default to all types if none specified
        if not types:
            types = list(self.TYPES.keys())
            
        # Extract keywords from query if not provided
        if query and not keywords:
            # Simple keyword extraction
            keywords = [w for w in query.split() if len(w) > 3]
        
        context = {
            'query': query,
            'types_searched': types,
            'keywords': keywords,
            'storyline': storyline,
            'canon_facts': [],
            'storylines': [],
            'working_context': [],
            'influences': [],
            'connections': []
        }
        
        # If looking for specific storyline
        if storyline:
            beats = self.find_beats_by_storyline(storyline)
            for beat in beats[:10]:
                location = 'canon' if 'canon' in str(beat) else 'working'
                context[f'{location}_facts' if location == 'canon' else 'working_context'].append({
                    'file': beat.name,
                    'storyline': storyline,
                    'excerpt': self.extract_context(beat, 15)
                })
        else:
            # Find files by type
            files_by_location = self.find_files_by_code(types)
            
            # Process canon files
            if keywords and files_by_location['canon']:
                matches = self.search_content(keywords, files_by_location['canon'])
                for file_path, score in matches[:5]:
                    context['canon_facts'].append({
                        'file': file_path.name,
                        'relevance': score,
                        'excerpt': self.extract_context(file_path)
                    })
            elif files_by_location['canon']:
                for file_path in files_by_location['canon'][:5]:
                    context['canon_facts'].append({
                        'file': file_path.name,
                        'excerpt': self.extract_context(file_path, 10)
                    })
            
            # Process working files
            if keywords and files_by_location['working']:
                matches = self.search_content(keywords, files_by_location['working'])
                for file_path, score in matches[:3]:
                    context['working_context'].append({
                        'file': file_path.name,
                        'relevance': score,
                        'excerpt': self.extract_context(file_path)
                    })
        
        # Find relevant storylines
        if 'SL' in types or not types:
            for sl_file in self.find_storylines():
                if not keywords or any(kw.lower() in sl_file.read_text(encoding='utf-8').lower() for kw in keywords):
                    context['storylines'].append({
                        'file': sl_file.name,
                        'excerpt': self.extract_context(sl_file, 10)
                    })
        
        # Find relevant influences
        if 'IN' in types or 'TH' in types:
            theme_files = [f['file'] for f in context['canon_facts'] if f['file'].startswith('TH-')]
            if theme_files:
                influences = self.find_influences_for_themes(theme_files)
                for inf_file in influences[:3]:
                    context['influences'].append({
                        'file': inf_file.name,
                        'excerpt': self.extract_context(inf_file, 10)
                    })
        
        # Find connections
        context['connections'] = self.find_connections(context)
        
        return context
    
    def find_connections(self, context: Dict) -> List[str]:
        """Identify connections between retrieved elements"""
        connections = []
        
        # Extract all file names
        all_files = []
        for section in ['canon_facts', 'working_context', 'storylines', 'influences']:
            for item in context.get(section, []):
                all_files.append(item['file'])
        
        # Look for character-theme connections
        characters = [f for f in all_files if f.startswith('CH-')]
        themes = [f for f in all_files if f.startswith('TH-')]
        influences = [f for f in all_files if f.startswith('IN-')]
        
        if characters and themes:
            connections.append(f"Character-Theme overlap: {len(characters)} characters, {len(themes)} themes")
        
        if themes and influences:
            connections.append(f"External influences inform {len(themes)} themes")
        
        if context.get('storylines'):
            connections.append(f"{len(context['storylines'])} storylines provide narrative structure")
        
        return connections[:5]
    
    def format_output(self, context: Dict, format_type: str = 'markdown') -> str:
        """Format context for output"""
        
        if format_type == 'json':
            return json.dumps(context, indent=2, default=str)
        
        # Markdown format
        output = []
        output.append(f"# Context Retrieval Results\n")
        output.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n")
        
        if context.get('query'):
            output.append(f"**Query**: {context['query']}\n")
        
        if context.get('storyline'):
            output.append(f"**Storyline**: {context['storyline']}\n")
        
        if context.get('types_searched'):
            types_desc = [self.TYPES.get(t, t) for t in context['types_searched']]
            output.append(f"**Types**: {', '.join(types_desc)}\n")
        
        # Storylines
        if context.get('storylines'):
            output.append("\n## Storylines\n")
            for item in context['storylines']:
                output.append(f"### {item['file']}")
                output.append(f"```\n{item['excerpt']}\n```\n")
        
        # Canon facts
        if context.get('canon_facts'):
            output.append("\n## Canon (Established Facts)\n")
            for item in context['canon_facts']:
                output.append(f"### {item['file']}")
                if 'relevance' in item:
                    output.append(f"*Relevance: {item['relevance']}*\n")
                if 'storyline' in item:
                    output.append(f"*Storyline: {item['storyline']}*\n")
                output.append(f"```\n{item['excerpt']}\n```\n")
        
        # Working context
        if context.get('working_context'):
            output.append("\n## Working (Active Development)\n")
            for item in context['working_context']:
                output.append(f"### {item['file']}")
                if 'relevance' in item:
                    output.append(f"*Relevance: {item['relevance']}*\n")
                output.append(f"```\n{item['excerpt']}\n```\n")
        
        # Influences
        if context.get('influences'):
            output.append("\n## Influences (External Ideas)\n")
            for item in context['influences']:
                output.append(f"### {item['file']}")
                output.append(f"```\n{item['excerpt']}\n```\n")
        
        # Connections
        if context.get('connections'):
            output.append("\n## Connections\n")
            for conn in context['connections']:
                output.append(f"- {conn}")
        
        return '\n'.join(output)

def main():
    parser = argparse.ArgumentParser(description='Story Context Retrieval System')
    parser.add_argument('-q', '--query', help='Search query')
    parser.add_argument('-t', '--types', help='File types to search (comma-separated codes)')
    parser.add_argument('-k', '--keywords', help='Keywords to search (comma-separated)')
    parser.add_argument('-s', '--storyline', help='Specific storyline to search')
    parser.add_argument('-f', '--format', choices=['markdown', 'json'], 
                       default='markdown', help='Output format')
    parser.add_argument('-o', '--output', help='Output file path')
    
    args = parser.parse_args()
    
    # Initialize retriever
    retriever = StoryRetriever()
    
    # Parse types
    types = None
    if args.types:
        types = [t.strip().upper() for t in args.types.split(',')]
    
    # Parse keywords
    keywords = None
    if args.keywords:
        keywords = [k.strip() for k in args.keywords.split(',')]
    
    # Build context
    context = retriever.build_context(
        query=args.query,
        types=types,
        keywords=keywords,
        storyline=args.storyline
    )
    
    # Format output
    output = retriever.format_output(context, args.format)
    
    # Save or print
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding='utf-8')
        print(f"Context saved to: {output_path}")
    else:
        print(output)

if __name__ == '__main__':
    main()
