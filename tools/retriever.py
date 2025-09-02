import os
import re
import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import argparse

class StoryRetriever:
    """Simplified context retrieval system for story development"""

    def __init__(self, root_path: Path = None):
        self.root = root_path or Path.cwd().parent  # Go up from tools/
        self.canon_dir = self.root / 'canon'
        self.working_dir = self.root  # Root is the working directory
        # Never search discarded

    def search_files(self, keywords: List[str] = None, types: List[str] = None) -> List[Path]:
        """
        Simple search:
        1. If types provided (CH, TH, etc), filter by prefix
        2. Search for keywords in filename and content
        3. Return canon first, then working
        """
        results = []

        # Search canon first, then working (root)
        for directory in [self.canon_dir, self.working_dir]:
            if not directory.exists():
                continue

            if directory == self.working_dir:
                # For root directory, only search direct .md files (not subdirectories)
                for file in directory.glob('*.md'):
                    # Skip if type filter doesn't match
                    if types and not any(file.name.startswith(f"{t}-") for t in types):
                        continue

                    # Check if keywords in filename or content
                    if keywords:
                        try:
                            content = file.read_text(encoding='utf-8').lower()
                            filename = file.name.lower()
                            if any(kw.lower() in filename or kw.lower() in content
                                   for kw in keywords):
                                results.append(file)
                        except Exception as e:
                            print(f"Error reading {file}: {e}")
                    else:
                        results.append(file)
            else:
                # For canon directory, search recursively
                for file in directory.rglob('*.md'):
                    # Skip if type filter doesn't match
                    if types and not any(file.name.startswith(f"{t}-") for t in types):
                        continue

                    # Check if keywords in filename or content
                    if keywords:
                        try:
                            content = file.read_text(encoding='utf-8').lower()
                            filename = file.name.lower()
                            if any(kw.lower() in filename or kw.lower() in content
                                   for kw in keywords):
                                results.append(file)
                        except Exception as e:
                            print(f"Error reading {file}: {e}")
                    else:
                        results.append(file)

        return results

    def extract_excerpt(self, file_path: Path, lines: int = 10) -> str:
        """Get first meaningful lines after any front matter"""
        try:
            content = file_path.read_text(encoding='utf-8')
            lines_list = content.split('\n')

            # Skip any frontmatter
            start = 0
            if lines_list[0] == '---':
                for i, line in enumerate(lines_list[1:], 1):
                    if line == '---':
                        start = i + 1
                        break

            # Return excerpt
            excerpt_lines = []
            for line in lines_list[start:]:
                if line.strip():  # Skip empty lines
                    excerpt_lines.append(line)
                if len(excerpt_lines) >= lines:
                    break

            return '\n'.join(excerpt_lines)
        except Exception as e:
            return f"Error extracting from {file_path}: {e}"

    def format_output(self, files: List[Path], format_type: str = 'markdown') -> str:
        """Format search results for output"""

        if format_type == 'json':
            result_data = []
            for file_path in files:
                result_data.append({
                    'file': file_path.name,
                    'path': str(file_path),
                    'excerpt': self.extract_excerpt(file_path)
                })
            return json.dumps(result_data, indent=2, default=str)

        # Markdown format
        output = []
        output.append("# Context Results\n")

        # Group by directory
        canon_files = [f for f in files if 'canon' in str(f)]
        working_files = [f for f in files if f.parent == self.working_dir]

        if canon_files:
            output.append("\n## Canon Files\n")
            for file_path in canon_files:
                output.append(f"### {file_path.name}")
                output.append(f"{self.extract_excerpt(file_path)}\n")

        if working_files:
            output.append("\n## Working Files\n")
            for file_path in working_files:
                output.append(f"### {file_path.name}")
                output.append(f"{self.extract_excerpt(file_path)}\n")

        return '\n'.join(output)

def main():
    parser = argparse.ArgumentParser(description='Simplified Story Context Retrieval System')
    parser.add_argument('-t', '--types', help='File types to search (comma-separated codes)')
    parser.add_argument('-k', '--keywords', help='Keywords to search (comma-separated)')
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

    # Search files
    files = retriever.search_files(keywords=keywords, types=types)

    # Format output
    output = retriever.format_output(files, args.format)

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
