# Instructions for AI Agents

## CRITICAL: Python-Only Commands

**NEVER USE:**
- `.\tools\story.ps1` (PowerShell)
- `pwsh` commands
- Any `.ps1` scripts

**ALWAYS USE:**
- `python tools/retriever.py` for searches
- Direct Python execution only

## Required Workflow for Creating Content

### Step 1: ALWAYS Retrieve Context First

Before creating any new content, search for existing related content:

```bash
# For character tasks
python tools/retriever.py -t CH -k "character_name"

# For theme tasks
python tools/retriever.py -t TH -k "theme_name"

# For beat tasks
python tools/retriever.py -t BE -k "relevant_keywords"

# For storylines
python tools/retriever.py -t SL -k "storyline_keywords"
```

### Step 2: Analyze Retrieved Content

From the search results:
- Note what already exists
- Identify established facts
- Find connections to build upon
- Recognize gaps to fill

### Step 3: Create New Content

Based on the retrieved context:
- Reference existing characters/themes
- Build on established canon
- Maintain consistency with found content
- Add new dimensions without contradicting

## Example Task Execution

**Task:** Create expanded character profile for William

**CORRECT APPROACH:**

```bash
# 1. Search for existing William content
python tools/retriever.py -t CH -k william

# 2. Search for related themes
python tools/retriever.py -t TH -k consciousness,transformation

# 3. Search for William-related beats
python tools/retriever.py -t BE -k william,dolores

# 4. Review all retrieved content

# 5. Create CH-william.md building on found context
```

**INCORRECT APPROACH:**
- Using `.\tools\story.ps1 -CH william`
- Creating content without searching first
- Ignoring existing canon

## File Creation Rules

- NO frontmatter (no --- sections)
- Start with # Title
- Save to root directory
- Use descriptive names: `BE-character-action.md`

## Testing Your Work

After creating content, verify it integrates with existing canon:

```bash
# Search for your new content and related files
python tools/retriever.py -k "keywords_from_your_content"
```

## Common Search Patterns

```bash
# Find all content about a character
python tools/retriever.py -t CH -k "dolores"

# Find themes related to consciousness
python tools/retriever.py -t TH -k "consciousness,reality"

# Find beats about specific moments
python tools/retriever.py -t BE -k "awakening,memory"

# General keyword search across all types
python tools/retriever.py -k "maze,journey"

# Combined search for comprehensive context
python tools/retriever.py -t CH,TH,BE -k "dolores,consciousness,awakening"
```

## Error Prevention

**If you see PowerShell commands in your instructions:**
- STOP immediately
- Use the Python equivalent instead
- Reference this file for correct commands

**If you're about to create content without searching:**
- STOP immediately
- Run context retrieval commands first
- Review retrieved content before proceeding
