[![Build](https://github.com/ShivamKR12/fruit-ninja/actions/workflows/build.yml/badge.svg)](https://github.com/ShivamKR12/fruit-ninja/actions/workflows/build.yml)
[![Release](https://img.shields.io/github/v/release/ShivamKR12/fruit-ninja?cacheSeconds=60)](https://github.com/ShivamKR12/fruit-ninja/releases)

# Fruit Ninja

A thrilling and addictive Fruit Ninja-style game developed in Python using the Pygame library. Experience the classic gameplay of slicing flying fruits while avoiding dangerous bombs. Test your reflexes and aim for the highest score in this fast-paced arcade game!

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [How to Play](#how-to-play)
- [Building an Executable](#building-an-executable)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)
- [Credits](#credits)

## Features

- **Intuitive Gameplay**: Click to slice fruits and avoid bombs with simple mouse controls.
- **Score Tracking**: Earn points for each fruit sliced and track your high score.
- **Lives System**: Start with multiple lives; lose one for each bomb hit.
- **Dynamic Graphics**: Smooth animations and vibrant fruit graphics.
- **Game Over and Restart**: When lives are depleted, restart with any key press.
- **Cross-Platform**: Runs on Windows, macOS, and Linux with Python and Pygame.
- **Standalone Executable**: Build a distributable binary using PyInstaller.

## Requirements

- **Python**: Version 3.10 or higher (tested with 3.13).
- **Pygame**: The game engine library. Install via `pip install pygame-ce`.
- **Assets**: Ensure the following files are present in the project directory:
  - `back.jpg` (background image)
  - `comic.ttf` (font file)
  - `fruit-ninja.png` (icon or additional asset)
  - `images/` folder (containing fruit and bomb images)

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ShivamKR12/fruit-ninja.git
   cd fruit-ninja
   ```

2. **Install Dependencies**:
   ```bash
   pip install pygame-ce
   ```

3. **Verify Assets**: Ensure all required assets (`back.jpg`, `comic.ttf`, `fruit-ninja.png`, and `images/` folder) are in the same directory as `main.py`.

## How to Play

1. **Launch the Game**:
   ```bash
   python main.py
   ```

2. **Gameplay Mechanics**:
   - Fruits will fly across the screen from various directions.
   - Use your mouse to click and drag to "slice" the fruits.
   - Avoid clicking on bombs, as they will deduct a life.
   - Each successfully sliced fruit increases your score.
   - The game ends when you run out of lives.

3. **Controls**:
   - **Left Mouse Button**: Slice fruits or bombs.
   - **Any Key**: Restart the game after game over.

4. **Objective**: Achieve the highest score possible by slicing as many fruits as you can without hitting bombs. Challenge yourself to beat your previous records!

## Building an Executable

To create a standalone executable for distribution (e.g., for Windows):

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Build the Executable:
   ```bash
   pyinstaller main.spec
   ```

3. The executable will be generated in the `dist/` folder, including the `fruit-ninja.ico` icon and all necessary resources. Share the `dist/main/` directory or the executable file as needed.

## Screenshots

*(Add screenshots here once available)*

- Gameplay in action
- Game over screen

## Contributing

Contributions are welcome! If you'd like to improve the game, add features, or fix bugs:

1. Fork the repository.
2. Create a new branch for your changes.
3. Make your modifications and test thoroughly.
4. Submit a pull request with a clear description of your changes.

Please ensure your code follows Python best practices and includes appropriate comments.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Credits

- Developed by [ShivamKR12](https://github.com/ShivamKR12).
- Built with [Pygame](https://www.pygame.org/) and [Pygame Community Edition](https://pyga.me/).
- Inspired by the original Fruit Ninja game by Halfbrick Studios.

For any questions or feedback, feel free to open an issue on GitHub.