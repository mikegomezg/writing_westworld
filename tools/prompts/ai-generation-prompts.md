# AI Generation Prompts for Ultra-Simple System

## Core Instructions for AI

```
IMPORTANT: 
- Create markdown files with NO frontmatter (no --- sections)
- Start directly with # Title
- Use blank lines before and after all headers
- Save to root directory with descriptive names like BE-character-action.md
```

## Character Generation

### Expand Character

```
Using the provided context about [CHARACTER], expand their profile.

Create a file that includes:
- Overview paragraph
- 3-5 specific traits
- Goals and motivations  
- Key relationships
- Internal conflict

Format:
# [Character Name]

## Overview
[Paragraph]

## Traits
- [Specific traits with examples]

[Continue with other sections...]

NO FRONTMATTER. Start with # header.
Save as: CH-[name]-expanded.md
```

### Create Minor Character

```
Based on the canon context, create a new minor character.

Include Overview, Traits, Role, and Connections sections.
Start directly with # Character Name
No frontmatter or metadata.

Save as: CH-[name].md
```

## Beat Generation

### New Story Moment

```
Write a beat where [CHARACTER] does [ACTION].

Structure:
# [Descriptive Title]

[Brief description paragraph]

## Setting
[Where and when]

## What Happens
[Prose narrative of events]

## Significance
[Why this matters]

NO FRONTMATTER. Pure markdown.
Save as: BE-[description].md
```

### Character Interaction

```
Create a scene between [CHARACTER A] and [CHARACTER B].

Write as narrative prose with natural dialogue.
Start with # Title describing the moment.
Include Setting, What Happens, and Significance sections.

Save as: BE-[characterA]-[characterB]-[topic].md
```

## Theme Exploration

### Theme Manifestation

```
Show how [THEME] appears in the story.

# [Theme Name]

## Core Concept
[What this explores]

## Character Examples
- How characters embody this

## Story Moments
- Where this appears in beats

NO FRONTMATTER. Start directly with content.
Save as: TH-[theme]-examples.md
```

## Quick Generation Prompts

### Daily Beat

```
Write a 200-word beat about [CHARACTER] experiencing [MOMENT].
Format: Title, one paragraph of prose.
No metadata, just story.
Save as: BE-[moment].md
```

### Character Thought

```
Write [CHARACTER]'s internal monologue during [EVENT].
150 words, stream of consciousness.
Just title and prose.
Save as: BE-[character]-thoughts.md
```

### Relationship Dynamic

```
Describe the relationship between [CHARACTER A] and [CHARACTER B].
Focus on specific interactions and tensions.
Simple markdown, no metadata.
Save as: CH-[characterA]-[characterB]-relationship.md
```

## Context Integration

### Using Retrieved Context

```
Based on the canon files about [TOPIC]:
1. Identify what's established
2. Find gaps to fill
3. Create new content that connects existing elements

Remember: NO FRONTMATTER, just markdown with clear headers.
```

### Checking Consistency

```
Review this new content against canon:
[PASTE CONTENT]

Does it contradict established facts?
Does it advance the story?
Does it follow the template format (no frontmatter)?
```

## File Naming Guide

Always use descriptive names:
- `BE-dolores-awakening.md` not `BE-scene1.md`
- `CH-william-dark-turn.md` not `CH-character2.md`
- `TH-consciousness-maze.md` not `TH-theme1.md`

## Common Mistakes to Avoid

1. **DON'T** add frontmatter (no ---)
2. **DON'T** add metadata fields
3. **DON'T** create complex folder structures
4. **DON'T** use generic filenames
5. **DON'T** forget blank lines around headers

## Success Check

Good file structure:
```markdown
# Clear Title

First paragraph with no metadata.

## Section Name

Content continues naturally.

## Another Section

More content without any frontmatter.
```

Bad file structure:
```markdown
---
status: working
type: beat
---
# Title
Content without spacing
## Section
More content
```
