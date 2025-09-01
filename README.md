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

## Workflow

1. Files in root = working/active development
2. Completed → `canon/` (established truth) or `inactive/` (archived)
3. Storylines defined in `canon/storylines/`
4. Daily sketches → `daily/YYYY-MM-DD-description.md`

## Usage

```powershell
# Retrieve context
.\tools\story.ps1 -query "Dolores consciousness" -types CH,TH,BE

# List storylines
.\tools\story.ps1 -storylines

# Move to canon
.\tools\story.ps1 -canonize BE-maze-revelation.md
```
