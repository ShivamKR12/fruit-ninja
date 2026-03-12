# Fruit Ninja

A simple Fruit Ninja–style game built with Pygame.

You slice fruits by clicking on them and avoid bombs. The game keeps track
of your score and lives. When you run out of lives the game is over, and
you can press any key to restart.

## Requirements

- Python 3.10+ (3.13 tested)
- [Pygame](https://www.pyga.me/) (pip install pygame-ce)

## Running the game

1. Clone or download the repository.
2. Make sure the required assets (`back.jpg`, `comic.ttf`, `fruit-ninja.png`,
   and the `images` folder) are present alongside `main.py`.
3. Install dependencies:
   ```sh
   pip install pygame-ce
   ```
4. Launch:
   ```sh
   py main.py
   ```

## Building an executable

The project includes a `main.spec` for PyInstaller. To create a Windows
binary, run:

```sh
pyinstaller main.spec
```

The resulting executable will include the `fruit-ninja.ico` icon and all
necessary resources.

## Controls

- **Left click**: "Slice" a fruit or bomb.
- **Press any key**: Restart after game over.

## License

This project is provided as-is for educational purposes.