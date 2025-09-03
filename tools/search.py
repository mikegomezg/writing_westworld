#!/usr/bin/env python
"""
Simplified search interface for AI agents
Usage: python tools/search.py characters:dolores,william themes:consciousness
"""

import sys
from pathlib import Path
from retriever import StoryRetriever

def main():
    if len(sys.argv) < 2 or '--help' in sys.argv:
        print("""
Usage: python tools/search.py [type:keywords] [type:keywords] ...

Types: characters, themes, beats, world, influences, storylines
       (or use shortcuts: ch, th, be, wo, in, sl)

Examples:
  python tools/search.py characters:dolores
  python tools/search.py ch:william,dolores th:consciousness
  python tools/search.py keywords:maze,journey
  python tools/search.py ch:dolores be:awakening th:consciousness
        """)
        sys.exit(0)
    
    retriever = StoryRetriever()
    types = []
    keywords = []
    
    # Parse arguments
    for arg in sys.argv[1:]:
        if ':' in arg:
            search_type, search_terms = arg.split(':', 1)
            search_type = search_type.lower()
            
            # Map long names to codes
            type_map = {
                'characters': 'CH', 'ch': 'CH',
                'themes': 'TH', 'th': 'TH',
                'beats': 'BE', 'be': 'BE',
                'world': 'WO', 'wo': 'WO',
                'influences': 'IN', 'in': 'IN',
                'storylines': 'SL', 'sl': 'SL',
                'keywords': None  # General search
            }
            
            if search_type in type_map:
                if type_map[search_type]:
                    types.append(type_map[search_type])
                keywords.extend(search_terms.split(','))
    
    # Search
    files = retriever.search_files(keywords=keywords if keywords else None, 
                                   types=types if types else None)
    
    # Output
    print(retriever.format_output(files))

if __name__ == '__main__':
    main()
