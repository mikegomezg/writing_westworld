import json
import sys
from pathlib import Path
from typing import List, Optional
import argparse

class StoryRetriever:
    """Ultra-simple context retrieval - no metadata, just search"""

    def __init__(self, root_path: Path = None):
        # If we're in tools/ directory, go up one level. Otherwise use current directory
        current = Path.cwd()
        if current.name == 'tools':
            self.root = root_path or current.parent
        else:
            self.root = root_path or current
        self.canon_dir = self.root / 'canon'
        # Folders to explicitly exclude from root search
        self.exclude_dirs = {'canon', 'inactive', 'tools', 'context', '.git'}

    def search_files(self, keywords: List[str] = None, types: List[str] = None) -> List[Path]:
        """
        Simple search:
        1. Search root (working files)
        2. Search canon/ (established)
        3. Filter by type prefix if specified
        4. Match keywords in filename or content
        5. Deduplicate results
        """
        results = []
        seen_files = set()  # Track files we've already added

        # Search root first (working files)
        for file in self.root.glob('*.md'):
            # Skip README and other non-story files
            if file.name == 'README.md':
                continue

            # Skip if type filter doesn't match
            if types and not any(file.name.startswith(f"{t}-") for t in types):
                continue

            # Check keywords
            if keywords:
                try:
                    content = file.read_text(encoding='utf-8').lower()
                    filename = file.name.lower()
                    if any(kw.lower() in filename or kw.lower() in content for kw in keywords):
                        if file not in seen_files:
                            results.append(file)
                            seen_files.add(file)
                except:
                    pass
            else:
                if file not in seen_files:
                    results.append(file)
                    seen_files.add(file)

        # Then search canon/ recursively
        if self.canon_dir.exists():
            for file in self.canon_dir.rglob('*.md'):
                # Skip if type filter doesn't match
                if types and not any(file.name.startswith(f"{t}-") for t in types):
                    continue

                # Check keywords
                if keywords:
                    try:
                        content = file.read_text(encoding='utf-8').lower()
                        filename = file.name.lower()
                        if any(kw.lower() in filename or kw.lower() in content for kw in keywords):
                            if file not in seen_files:
                                results.append(file)
                                seen_files.add(file)
                    except:
                        pass
                else:
                    if file not in seen_files:
                        results.append(file)
                        seen_files.add(file)

        return results

    def extract_excerpt(self, file_path: Path, max_lines: int = 10) -> str:
        """Get first meaningful lines from the file"""
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')

            # Get non-empty lines
            excerpt_lines = []
            for line in lines:
                if line.strip():
                    excerpt_lines.append(line)
                if len(excerpt_lines) >= max_lines:
                    break

            return '\n'.join(excerpt_lines)
        except:
            return f"[Could not read {file_path.name}]"

    def format_output(self, files: List[Path]) -> str:
        """Format results as simple markdown"""
        if not files:
            return "# No Results Found\n\nTry different keywords or check your file names."

        output = ["# Context Results\n"]

        # Separate root and canon files
        root_files = [f for f in files if f.parent == self.root]
        canon_files = [f for f in files if 'canon' in str(f)]

        # Show root files first (working)
        if root_files:
            output.append("## Working Files (Root)\n")
            for file in root_files:
                output.append(f"### {file.name}\n")
                output.append(self.extract_excerpt(file))
                output.append("\n")

        # Then canon files
        if canon_files:
            output.append("## Canon Files\n")
            for file in canon_files:
                # Show relative path from canon/
                try:
                    rel_path = file.relative_to(self.canon_dir)
                except ValueError:
                    rel_path = file.name
                output.append(f"### {rel_path}\n")
                output.append(self.extract_excerpt(file))
                output.append("\n")

        return '\n'.join(output)

def print_usage():
    """Print usage instructions for direct Python calls"""
    print("""
Usage: python tools/retriever.py [options]

Options:
  -t, --types     File types (comma-separated: CH,TH,BE,WO,IN,SL)
  -k, --keywords  Keywords to search (comma-separated)
  -o, --output    Output file path
  -h, --help      Show this help message

Examples:
  python tools/retriever.py -k "dolores,consciousness"
  python tools/retriever.py -t CH -k "william"
  python tools/retriever.py -t BE,TH -k "maze,journey"
  python tools/retriever.py -t CH,TH,BE -k "dolores,awakening" -o context/results.md
    """)
    sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description='Ultra-simple story context retrieval')
    parser.add_argument('-t', '--types', help='File types (comma-separated: CH,TH,BE,WO,IN,SL)')
    parser.add_argument('-k', '--keywords', help='Keywords to search (comma-separated)')
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('--help-examples', action='store_true', help='Show usage examples')
    
    args = parser.parse_args()
    
    if args.help_examples:
        print_usage()

    # Initialize retriever
    retriever = StoryRetriever()

    # Parse inputs
    types = [t.strip().upper() for t in args.types.split(',')] if args.types else None
    keywords = [k.strip() for k in args.keywords.split(',')] if args.keywords else None
    
    # If no arguments provided, show help
    if not types and not keywords:
        print("No search parameters provided. Use --help for options or --help-examples for usage examples.")
        sys.exit(1)

    # Search
    files = retriever.search_files(keywords=keywords, types=types)

    # Format output
    output = retriever.format_output(files)

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
