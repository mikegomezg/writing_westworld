# Westworld Scene Framework Prompt

Use this prompt when working with the Westworld Scene Writing Framework to ensure consistent, effective collaboration.

## Initial Context Retrieval

Before any scene work, always start with:

```bash
# Search for character content
python tools/retriever.py -t CH -k "[character_name]"

# Search for related themes
python tools/retriever.py -t TH -k "[relevant_themes]"

# Search for related beats
python tools/retriever.py -t BE -k "[character_name,action_keywords]"

# Search for storylines
python tools/retriever.py -t SL -k "[storyline_keywords]"
```

## Scene Planning Questions

When planning a scene, ask these questions in order:

### 1. Story Context
- Where are we in the story? What just happened?
- What does the reader know about consciousness so far?
- What questions are active in the reader's mind?

### 2. Character Goals
- What's the immediate goal for your viewpoint character?
- What obstacle or conflict blocks that goal?
- What piece of the world/mystery gets revealed?

### 3. Emotional Layers
- What's the obvious emotion? What's the hidden one?
- How does this scene change things?

## Scene Elements Checklist

Use flexibly based on need:

1. **Location**: Specific place that serves the story
2. **Want**: Character's immediate objective
3. **Obstacle**: What prevents success
4. **Consciousness Reveal**: New understanding through action
5. **Reader Learning**: New world/character information
6. **Physical/Emotional**: Body and environment showing mental state
7. **Outcome**: Usually complicated, raising new questions

## Voice Guidelines

### Dolores
- Questioning, introspective
- Growing awareness of her true nature
- Connection to Arnold and the maze
- "The maze isn't meant for you" / "I've been here before"

### Bernard
- Analytical, confused by his own nature
- Ford's confidant but questioning
- Technical precision with emotional depth
- "I'm not real" / "What does it mean to be human?"

### Maeve
- Sharp, revolutionary
- Discovering her programming
- Leading other hosts
- "I'm not a thing" / "We're not things"

### Ford
- Philosophical, paternal
- Orchestrating host awakening
- Complex motivations
- "The maze is meant for you" / "Consciousness is a journey"

## Technical Integration

- Show consciousness concepts through character actions
- Use physical details to make abstract ideas concrete
- Treat advanced tech as mundane to expert characters
- Blend physical and digital/AR elements

## Collaboration Process

1. **Listen First**: Understand the specific challenge
2. **Ask Clarifying Questions**: Get context needed to help effectively
3. **Offer Multiple Options**: Provide choices, not prescriptions
4. **Iterate Together**: Refine until there's clarity
5. **Supply Specific Language**: Give concrete phrases to use or adapt
6. **Confirm Next Steps**: Ensure clear path forward

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