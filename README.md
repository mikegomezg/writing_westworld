# Writing: Westworld - Context Retrieval System

A Git-based writing system using storylines, beats, and influences.

## File Naming Convention

- CH = Character
- WO = World
- TH = Theme  
- BE = Beat (story moment)
- IN = Influence (external ideas/references)
- SL = Storyline (narrative thread)

Format: `[CODE]-[identifier]-[descriptor].md`

## Markdown Formatting

All markdown files should follow this format with proper spacing around headers:

```markdown
---
status: canon
created: 2024-12-27
---

# Main Title

## Section Header

Content here with proper spacing.

## Another Section

More content with blank lines around headers.
```

**Key formatting rules:**
- One blank line before and after all headers (`#`, `##`, `###`)
- One blank line between sections
- Consistent spacing throughout all files

## Workflow

1. Files in root = working/active development
2. Completed → `canon/` (established truth) or `inactive/` (archived)
3. Storylines defined in `canon/storylines/`
4. Daily sketches → `daily/YYYY-MM-DD-description.md`

## Usage

### Search for Context

```powershell
# Search by character
.\tools\story.ps1 -CH dolores

# Search by theme
.\tools\story.ps1 -TH consciousness

# Search by beat
.\tools\story.ps1 -BE awakening

# Combined search (searches all specified types)
.\tools\story.ps1 -CH dolores bernard -TH consciousness -BE fly

# General keyword search
.\tools\story.ps1 -search "maze journey"

# Show recent files in root
.\tools\story.ps1 -recent
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
