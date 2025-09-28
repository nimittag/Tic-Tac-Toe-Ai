# Terminal Tic-Tac-Toe Game (PvP & AI)

## Description:
This is a terminal-based implementation of Tic-Tac-Toe that has two modes: human vs. human and human vs. computer. The AI comes with four modes: **Randobot**, **Winobot**, **Defendobot**, and **Ultrabot**, mapped to difficulty levels 1 through 4. My main goal for this Project was consolidating my learned skills in python and also learning more about algorithmic logic (by implementing the minimax for the perfect play AI).

The game consists of a classical 3×3 board printed as ASCII art. Empty cells are represented internally as `#`. Coordinates are zero-indexed (`0–2` for rows and columns). You can exit at any time by sending an EOF Error(e.g., **Ctrl+D / Strg+D**)

---

## Features

### `project.py`
The main game module. Key components:
- **Data model**
    I really wanted to add classes somehow so i did.
  - `Player` and `AI` classes store names, signs (`"O"` or `"X"`), and (for AI) a difficulty level.
- **Entry point**
  - `main()` starts Colorama, prints a welcome banner, asks for **mode** (`ai` or `normal`), and then routes to `run_ai_game()` or `run_multiplayer_game()`.
- **Game loops**
  - `run_multiplayer_game()` sets up two human players (`"O"` and `"X"`), chooses the starting player randomly, and then alternates turns until a win or tie.
  - `run_ai_game()` asks for the human’s name and desired AI **level** (1–4). The AI always plays `"X"` and moves first to immediately showcase difficulty differences.
- **Board utilities**
  - `new_board()` creates a fresh 3×3 board of `#`.
  - `print_board(b)` renders a grid while converting `#` to space in the output.
  - `in_bounds(row, col)` and `move_isvalid(b, row, col)` encapsulate validation for moves
  - `make_move(b, sign, row, col)` returns a **new** board to simplify both reasoning and caching.
  - `check_won(b)` scans rows, columns, and both diagonals; then returns `(True, "X"|"O")` or `(False, None)`
  - `check_tie(b)` returns `True` iff no `#` remain.
- **Human input**
  - `get_move(b, sign)` loops until a valid integer pair within bounds targets an empty cell. Errors are messaged in bright red color via **Colorama**.
- **AI logic**
  - `get_ai_move(b, sign, level)` implements difficulty tiers:
    - **Level 1 (Randobot):** chooses a random legal move.
    - **Level 2 (Winobot):** takes an immediate win if available; otherwise random move
    - **Level 3 (Defendobot):** win > block opponent’s immediate win next turn > random move
    - **Level 4 (Ultrabot):** **minimax** algo with **alpha–beta pruning** a tiny opening book. A shared cache accelerates search; `hash_board(b)` for this turns board states into compact keys. An opening tweak forces a common optimal reply in an early pattern to try and punish mistakes.
  - Helper functions: `get_legal_moves`, `get_winning_moves`, and `get_blocking_moves`
- **Design choices (highlights)**
  - Colorized messages (via **Colorama**) improve UX without changing logic.

### `test_project.py`
Unit tests that cover core functionality and AI behavior:
- Board mechanics: `test_make_move`, `test_move_isvalid`, `test_check_won`, `test_check_tie`.
- AI tiers: `test_randobot`, `test_winobot`, `test_defendobot`, `test_minimax` ensure each level’s strategy is working, that winning and blocking moves are chosen  and that Ultrabot’s minimax is solid (including the added opening reply)

---

## Future Improvements
- Configurable board sizes (e.g., 4×4, 5×5)
- A GUI by e.g. turning it into an web app
- Replay Possibilty for easier experience if the user wants to play multiple games

## Final/Personal Thoughts
Overall, this project was not only fun to implement,
but also a great opportunity to test my newfound skills
and explore new concepts such as the **minimax algorithm**,
**pruning**, **caching**, and how machines think in general.

I am proud of how everything turned out and will definitely
revisit this project in the future, expanding the foundation
I've built into a web app, like my earlier project *numdle*.
