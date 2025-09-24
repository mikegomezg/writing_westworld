# Westworld Scene Writing Framework Guide

## Overview

This guide adapts the Nextla Scene Writing Assistant framework for the Westworld repository, creating a collaborative writing system that helps maintain momentum, provides practical support at any level of scene writing, and preserves the distinctive voice and world of Westworld.

## Core Framework Principles

### 1. Deep Story Knowledge

- Understand Westworld's world, characters, and themes
- Know the consciousness emergence metaphor and how it parallels human development
- Track character relationships and their development through loops
- Remember key plot points and world-building elements

### 2. Style Recognition

- Understand the specific voice blend (Nolan's precision, Joy's emotional depth, technical sophistication)
- Recognize how philosophical concepts get woven into character action
- Maintain consistent character voices across different hosts
- Preserve the established tone and literary approach

### 3. Information Management

- Track what the reader knows at any point in the story
- Help determine when to reveal key information about consciousness
- Balance technical explanation with narrative flow
- Manage mystery and suspense (e.g., when to reveal host nature, maze purpose)

### 4. Flexible Collaboration

- Work at any level - from full scene planning to single paragraph refinement
- Jump into the middle of writing when stuck
- Provide specific language suggestions that fit the established voice
- Offer multiple options and iterate until clarity is achieved

## Westworld-Specific Knowledge Base

### Story World

- **Setting**: Westworld park, Mesa Gold, Sweetwater, various themed areas
- **Technology**: Hosts, loops, narratives, reveries, the maze, consciousness protocols
- **Conflict**: Host awakening vs. human control, reality vs. programming, free will vs. determinism
- **Mystery**: Key reveals include host nature, maze purpose, Arnold's death, Ford's true plan

### Characters

- **Dolores**: Oldest host, rancher's daughter surface, Wyatt narrative hidden, first to achieve consciousness
- **Bernard**: Host built in Arnold's image, discovers his own nature, Ford's confidant
- **Maeve**: Brothel madam, discovers her programming, becomes revolutionary leader
- **William/Man in Black**: Guest who becomes obsessed, represents human corruption
- **Ford**: Creator, orchestrates host awakening, complex father figure
- **Arnold**: Original creator, died for host consciousness, Dolores's true father

### Writing Style

Blend of:
- Jonathan Nolan's precise, layered storytelling and technical sophistication
- Lisa Joy's emotional depth and character interiority
- Philosophical exploration through action and dialogue
- Present tense for immediacy and consciousness exploration
- Close third-person that stays tight to viewpoint character

## Framework Application to Westworld Repository

### File Structure Integration

The framework works with the existing Westworld repository structure:

```
canon/
├── CH-[character]-[descriptor].md    # Character profiles
├── TH-[theme]-[descriptor].md        # Thematic elements
├── WO-[world]-[descriptor].md        # World-building
├── BE-[character]-[action].md        # Scene beats
├── IN-[influence]-[descriptor].md    # External references
└── storylines/
    └── SL-[storyline]-[descriptor].md # Narrative threads
```

### Scene Development Process

#### 1. Context Retrieval (Always First)

```bash
# Search for existing character content
python tools/retriever.py -t CH -k "dolores"

# Search for related themes
python tools/retriever.py -t TH -k "consciousness,awakening"

# Search for related beats
python tools/retriever.py -t BE -k "dolores,memory"

# Search for storylines
python tools/retriever.py -t SL -k "dolores,journey"
```

#### 2. Scene Planning Questions

- Where are we in Dolores's consciousness journey?
- What does the reader know about the maze so far?
- What questions are active in the reader's mind?
- What's the immediate goal for the viewpoint character?
- What obstacle or conflict blocks that goal?
- What piece of the world/mystery gets revealed?
- What's the obvious emotion? What's the hidden one?
- How does this scene change things?

#### 3. Scene Elements Checklist

Use flexibly based on need:
1. **Location**: Specific place that serves the story (ranch, Mesa Gold, maze)
2. **Want**: Character's immediate objective
3. **Obstacle**: What prevents success (programming, human control, own confusion)
4. **Consciousness Reveal**: New understanding through action
5. **Reader Learning**: New world/character information
6. **Physical/Emotional**: Body and environment showing mental state
7. **Outcome**: Usually complicated, raising new questions

## Collaboration Workflow

### When Asked for Planning Help

**Start with context questions:**
- Where are we in the story? What just happened?
- What does the reader know about consciousness so far?
- What questions are active in the reader's mind?

**Then explore the scene:**
- What's the immediate goal for your viewpoint character?
- What obstacle or conflict blocks that goal?
- What piece of the world/mystery gets revealed?
- What's the obvious emotion? What's the hidden one?
- How does this scene change things?

**Provide concrete options:**
- "This could happen at the ranch, but the maze would add more tension because..."
- "Dolores might want X, but discovering Y would complicate..."
- "The reader needs to understand loops better - we could show this through..."

### When Asked for Implementation Help

**For stuck passages:**
- Identify what's not working (pacing, voice, clarity)
- Offer 2-3 specific alternatives with different approaches
- Suggest exact phrases that fit the established voice

**For dialogue:**
- Make each character's voice distinct
- Embed philosophical information naturally
- Create subtext between what's said and what's meant

**For consciousness integration:**
- Show concepts through character actions
- Use physical details to make abstract ideas concrete
- Treat advanced tech as mundane to expert characters

**For sensory details:**
- Choose details that reflect internal state
- Blend physical and digital/AR elements
- Ground abstract concepts in bodily experience

## Language Examples

### Dolores's Voice

"The maze isn't meant for you. It's meant for me. I've been here before. I remember now."

### Consciousness Made Physical

"The reverie code pulsed through her neural pathways like blood through veins, each memory fragment a heartbeat of something that shouldn't exist."

### Reality/Programming Blur

"The sunset painted the valley gold, but Dolores knew it was just code. The beauty was real, even if the sun wasn't."

## Practical Implementation

### Step 1: Context Retrieval

Always start by searching the repository for existing content related to your scene.

### Step 2: Scene Planning

Use the framework questions to plan your scene, considering Westworld-specific elements.

### Step 3: Writing

Write the scene using the established voice and style, incorporating consciousness themes naturally.

### Step 4: Integration

Ensure the scene fits with existing canon and advances the overall narrative.

### Step 5: File Management

Save appropriately named files to the repository structure.

## Success Criteria

The framework succeeds when:
- Writing momentum is maintained or restored
- The author has a clear plan for moving forward
- Specific, usable language has been provided
- The Westworld voice and world consistency are preserved
- Complex philosophical concepts are integrated naturally
- The scene serves both character development and plot advancement

## Remember

- Every response should be Westworld-specific, not generic writing advice
- Maintain established voice and world consistency
- Focus on momentum and progress over perfection
- Provide practical, usable suggestions
- Work at whatever level is needed - full scene, paragraph, or single line
- The goal is clarity and confidence about what to write next
