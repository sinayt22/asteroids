# Asteroids (Pygame)

A fast-paced arcade-style Asteroids game built with Python and Pygame.

## Features

- Player ship movement with acceleration and rotation
- Asteroid spawning, splitting, and score tracking
- Multiple shot modes:
	- Normal shot
	- Triple shot pickup
	- Super shot pickup
- Bomb system with cooldown and limited bomb inventory
- Temporary shield (spawn shield + shield pickup)
- HUD elements for lives, score, asteroid count, shield timer, and bombs
- Runtime JSONL logging for game state and gameplay events

## Requirements

- Python `>=3.13`
- Pygame `2.6.1`

Dependencies are defined in `pyproject.toml`.

## Install

### Option 1: Using `uv` (recommended)

```bash
uv sync
```

### Option 2: Using `venv` + `pip`

```bash
python -m venv .venv
source .venv/bin/activate
pip install pygame==2.6.1
```

## Run

### With `uv`

```bash
uv run main.py
```

### With activated virtual environment

```bash
python main.py
```

## Controls

- `W`: Move forward
- `S`: Move backward
- `A`: Rotate left
- `D`: Rotate right
- `Space`: Shoot
- `Left Ctrl`: Drop bomb
- Window close button: Quit game

## Gameplay Notes

- You start with a temporary shield and a limited number of bombs.
- Shooting and bombs both have cooldown timers.
- Pickups spawn periodically and disappear after a short time.
- Super/triple shot pickups are temporary and revert to normal shot after timeout.

## Logs

During gameplay, the game writes:

- `game_state.jsonl`: periodic snapshots of scene/game objects
- `game_events.jsonl`: notable events (for example, hits and asteroid destruction)

Both files are overwritten on each run and then appended during that run.

## Project Structure

- `main.py`: game loop and collision handling
- `player.py`: player movement, shooting, bombs, shield, pickups
- `asteroid.py`, `asteroidfield.py`: asteroid behavior and spawning
- `shot.py`, `bomb.py`: projectile/bomb logic
- `pickup.py`: pickup types and behavior
- `logger.py`: JSONL state/event logging
- `constants.py`: gameplay tuning values

## Troubleshooting

- If assets fail to load, run the game from the project root so relative file paths resolve correctly.
- If `uv` is not installed, use the `venv` + `pip` installation option.
