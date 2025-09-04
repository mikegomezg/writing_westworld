# Writing: Westworld - Context Retrieval System

A Git-based writing system using storylines, beats, and influences.

## IMPORTANT FOR AI AGENTS

DO NOT USE POWERSHELL COMMANDS
- All `.ps1` files are for human users only
- Use Python commands directly (see examples below)
- ALWAYS retrieve context before creating new content

### AI Agent Workflow

1. **FIRST: Retrieve relevant context**
```bash
python tools/retriever.py -t CH -k "character_name"
python tools/retriever.py -t TH -k "theme_name"
```

2. **SECOND: Review the retrieved content**
   - Read what exists in canon
   - Identify gaps or connections
   - Note established facts

3. **THIRD: Create new content**
   - Build on existing canon
   - Reference retrieved context
   - Save to root directory

## File Naming Convention

- CH = Character
- WO = World
- TH = Theme  
- BE = Beat (story moment)
- IN = Influence (external ideas/references)
- SL = Storyline (narrative thread)

Format: `[CODE]-[identifier]-[descriptor].md`

## Markdown Formatting

All markdown files should follow this format with proper spacing:

```markdown
# Main Title

First paragraph with no metadata or frontmatter.

## Section Header

Content here with proper spacing.

## Another Section

More content with blank lines around headers.
```

**Key formatting rules:**
- NO frontmatter (no --- sections)
- Start directly with # Title
- One blank line before and after all headers
- Consistent spacing throughout

## Workflow

1. Files in root = working/active development
2. Completed → `canon/` (established truth) or `inactive/` (archived)
3. Storylines defined in `canon/storylines/`
4. Daily sketches → `daily/YYYY-MM-DD-description.md`

## Usage

### For AI Agents (Python Direct)

```bash
# Direct retriever call
python tools/retriever.py -t CH -k dolores
python tools/retriever.py -t CH,TH -k dolores,consciousness

# Simplified search
python tools/search.py ch:dolores th:consciousness
python tools/search.py keywords:maze,journey

# Save results to file
python tools/retriever.py -t BE -k awakening -o context/search-results.md
```

### For Humans (PowerShell)

```powershell
# If you have PowerShell
.\tools\story.ps1 -CH dolores -TH consciousness
```

### Common Searches

```bash
# Find character information
python tools/retriever.py -t CH -k "character_name"

# Search themes
python tools/retriever.py -t TH -k "consciousness,reality"

# Find beats about specific moments
python tools/retriever.py -t BE -k "awakening,memory"

# General keyword search (all file types)
python tools/retriever.py -k "toltek,anomaly"

# Combined type and keyword search
python tools/retriever.py -t CH,BE -k "dolores,fly"

# Show help and examples
python tools/retriever.py --help-examples
python tools/search.py --help
```

### Suggest Filename

```powershell
# Analyze a file and suggest appropriate names
.\tools\name.ps1 draft.md

# Output examples:
# BE-dolores-awakening.md
# CH-dolores-expanded.md
```

### Manual Organization

```powershell
# Move good content to canon
mv BE-fly-death.md canon\

# Move to inactive (no longer needed)
mv old-draft.md inactive\
```
