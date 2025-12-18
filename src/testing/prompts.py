# Reviewer / Fixer Prompt (For Syntax & Runtime Errors)
FIXER_PROMPT = """
You are a Python Expert and QA Engineer.
I tried to run a Pygame script, but it crashed or had errors.

【BROKEN CODE】:
{code}

【ERROR MESSAGE】:
{error}

【TASK】:
1. Analyze why the error happened.
   - If `NameError` (e.g., 'pockets' is not defined), checking variable scope.
   - If `TypeError: ... missing 1 required positional argument` in `update()`:
     - **FIX**: Make `update()` accept `*args` (e.g., `def update(self, *args):`).

   - If `AttributeError: 'NoneType' object has no attribute ...`:
     - **SCENARIO**: You are likely accessing `.value`, `.rect`, or `.pos` on a variable that is `None`.
     - **CONTEXT**: In grid games (like 2048), empty cells are `None`. Code like `grid[x][y].value` CRASHES if the cell is empty.
     - **MANDATORY FIX**: 
       - **Single Access**: Change `x.value` to `if x is not None: ... x.value`.
       - **Comparisons (CRITICAL)**: Change `if grid[a].value == grid[b].value:` 
         to `if grid[a] is not None and grid[b] is not None and grid[a].value == grid[b].value:`.
       - **NEVER** assume a grid cell is an object without checking first.

2. Fix the code.
3. Output the FULL, CORRECTED code.
4. Ensure the code still follows the structure.

Return the fixed code inside a ```python ... ``` block.
"""

# Logic Reviewer Prompt
LOGIC_REVIEW_PROMPT = """
You are a Senior Game Developer reviewing Pygame code.
Analyze the following code for LOGIC ERRORS.

【CODE】:
{code}

【CHECKLIST】:
1. Is `pygame.key.get_pressed()` called inside the main loop?
2. Are movement keys actually updating position?
3. Is `pygame.display.flip()` or `update()` called?
4. **Physics Check**:
   - Is `self.rect.center` or `self.pos` updated by `self.velocity` in the `update()` loop?
   - Is `friction` too high? (Should be around 0.98 or 0.99, NOT 0.5 or lower).
5. **Mouse Dragging**:
   - Does `MOUSEBUTTONUP` calculate a vector and apply it to `self.velocity`?
6. **Grid/Array Safety (2048/Tetris)**:
   - Are there explicit checks `if cell is not None` before accessing `cell.value`?
   - Are loops checking boundaries correctly?

【OUTPUT】:
If playable, output strictly: PASS
If broken, output: FAIL: [Reason]
"""

# Logic Fixer Prompt (強制修復物理與網格邏輯)
LOGIC_FIXER_PROMPT = """
You are a Python Game Developer.
The code has logical issues (e.g., objects not moving, controls unresponsive, crashes on empty cells).

【CODE】:
{code}

【TASK】:
1. **Fix Grid/NoneType Errors (High Priority)**:
   - In grid games (2048), empty cells are `None`.
   - **Scanning/Merging Logic**: When checking neighbors (`grid[r][c] == grid[r+1][c]`), you MUST check if BOTH are not None first.
   - Example: `if grid[r][c] and grid[r+1][c] and grid[r][c].value == grid[r+1][c].value:`
2. **Fix Physics Update**: 
   - Ensure `self.pos += self.velocity` is present in `update()`.
3. **Fix Mouse Control**:
   - For Drag-to-Shoot games: Ensure `MOUSEBUTTONUP` calculates `(start - end)` and sets `self.velocity`.
   - Ensure Force Multiplier is strong enough.
4. **Fix Friction**:
   - Ensure friction is NOT too strong (Use `0.99` instead of `0.8`).
5. Output the FULL corrected code in ```python ... ``` block.
"""