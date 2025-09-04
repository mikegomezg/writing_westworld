#!/usr/bin/env python
"""
Test that demonstrates correct AI agent workflow
Run: python tools/test_ai_workflow.py
"""

import subprocess
import sys

def demonstrate_workflow():
    """Show the correct workflow for AI agents"""

    print("=" * 50)
    print("CORRECT AI AGENT WORKFLOW DEMONSTRATION")
    print("=" * 50)

    print("\n1. RETRIEVING CONTEXT (Python-only):")
    print("-" * 30)

    # Demonstrate context retrieval
    commands = [
        ("Character search", "python tools/retriever.py -t CH -k dolores"),
        ("Theme search", "python tools/retriever.py -t TH -k consciousness"),
        ("Beat search", "python tools/retriever.py -t BE -k awakening"),
    ]

    for name, cmd in commands:
        print(f"\n{name}:")
        print(f"Command: {cmd}")
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
            if "No Results Found" not in result.stdout and result.stdout.strip():
                print("✅ Context retrieved successfully")
            else:
                print("⚠️ No matching content found")
        except:
            print("❌ Command failed")

    print("\n2. ANALYZE RETRIEVED CONTENT:")
    print("-" * 30)
    print("- Review what exists in canon/")
    print("- Note established facts")
    print("- Identify connections to build upon")

    print("\n3. CREATE NEW CONTENT:")
    print("-" * 30)
    print("- Build on retrieved context")
    print("- Save to root directory")
    print("- Use descriptive filename")

    print("\n" + "=" * 50)
    print("NEVER USE POWERSHELL COMMANDS!")
    print("=" * 50)


if __name__ == "__main__":
    demonstrate_workflow()
