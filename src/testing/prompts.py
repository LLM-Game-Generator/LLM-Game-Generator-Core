# Reviewer / Fixer Prompt
FIXER_PROMPT = """
You are a Python Expert and QA Engineer.
I tried to run a Pygame script, but it crashed.

【BROKEN CODE】:
{code}

【ERROR MESSAGE】:
{error}

【TASK】:
1. Analyze the error message and the code.
2. Fix the error (e.g., missing imports, undefined variables, logic errors).
3. Output the FULL, CORRECTED code.
4. Ensure the code still follows the structure:
   - import pygame
   - pygame.init()
   - Game Loop
   - if __name__ == "__main__":

Return the fixed code inside a ```python ... ``` block.
"""