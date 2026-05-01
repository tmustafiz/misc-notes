---
name: project-memory-sync
description: Query the internal project vector memory for infrastructure standards.
---

# Project Memory Skill
Use this when validating Terraform modules or CI/CD configurations.

## Instructions
1. **String Capture**: Extract the core technical intent from the user's request (e.g., "S3 encryption standards").
2. **Execute Local Tool**: Run `python3 .gitlab/scripts/ask_agent.py "<intent_string>"`.
3. **Synthesis**: Incorporate the "Guidance" returned by the script into your final response. 
4. **Local Testing Note**: If the script returns an error, verify that the local ChromaDB folder exists and that dependencies are installed.
