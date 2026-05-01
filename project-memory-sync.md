---
name: project-memory-sync
[span_27](start_span)description: Skill for querying the internal project vector memory[span_27](end_span)
---

# Project Memory Skill
[span_28](start_span)Use this skill when validating Terraform changes against organizational knowledge[span_28](end_span).

## Steps
1. **[span_29](start_span)Capture Intent**: Identify the specific Terraform resource or module the user is asking about[span_29](end_span).
2. **[span_30](start_span)Execute Local Search**: Run the command `python3 .gitlab/scripts/ask_agent.py` using the resource name as the argument[span_30](end_span).
3. **[span_31](start_span)Analyze & Compare**: Compare the retrieved "Best Practice" snippets from the terminal output against the user's code[span_31](end_span).
4. **[span_32](start_span)Correction**: If the user's code differs from the retrieved snippet, suggest a fix that aligns with the project's established memory[span_32](end_span).
