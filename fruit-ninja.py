# Import necessary modules for the game.
import pygame, sys, os, random

# - pygame: The main library for creating games in Python. It handles graphics, sound, input, and more.
#   We use it to create the game window, draw images, handle mouse events, and control the game loop.
# - sys: Provides access to system-specific parameters and functions, like exiting the program.
# - os: Provides functions for interacting with the operating system, like handling file paths.
# - random: Used to generate random numbers, like random positions and speeds for fruits.

# Global variables to keep track of the game state.
# These are variables that can be accessed from anywhere in the code.
player_lives = 3  # The number of lives the player has left. Starts at 3, decreases when hitting bombs.
score = 0  # The player's current score. Increases when slicing fruits.
fruits = ['melon', 'orange', 'pomegranate', 'guava', 'bomb']  # List of all possible entities in the game.
# - Fruits are good to slice for points.
# - Bomb is bad; hitting it costs a life.

def resource_path(relative_path):
    """
    Get the absolute path to a resource file.

    This function is used to find image and font files, even when the game is packaged into an executable.
    When running as a script, it uses the current directory.
    When packaged with PyInstaller (a tool to make .exe files), it uses the temporary directory where files are extracted.

    Parameters:
    relative_path (str): The relative path to the resource file (e.g., 'images/fruit.png').

    Returns:
    str: The absolute path to the resource file.
    """
    
    # Try to get the path from PyInstaller's temporary directory.
    try:
        base_path = sys._MEIPASS  # This variable is set by PyInstaller when running from an executable.
    
    # If not packaged (running as a regular Python script), use the current working directory.
    except Exception:
        base_path = os.path.abspath(".")  # Get the absolute path of the current directory.
    
    # Join the base path with the relative path to get the full path.
    return os.path.join(base_path, relative_path)  # Combine paths safely, handling different operating systems.

# Initialize Pygame and set up the game window.
# This section sets up the basic game environment.
WIDTH = 800  # The width of the game window in pixels.
HEIGHT = 600  # The height of the game window in pixels.
FPS = 12  # Frames Per Second: How many times the game updates and redraws the screen per second.
# A lower value like 12 means the game runs slower, which is fine for this type of game.

# Initialize all Pygame modules. This must be called before using any Pygame functions.
pygame.init()

# Set the title of the game window.
pygame.display.set_caption('Fruit-Ninja')

# Load the game icon image from the file 'fruit-ninja.png'.
# resource_path ensures it works whether running as script or executable.
icon_img = pygame.image.load(resource_path('fruit-ninja.png'))

# Set the window icon to the loaded image.
pygame.display.set_icon(icon_img)

# Create the game window with the specified width and height.
# This returns a Surface object representing the window where we draw everything.
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))

# Create a Clock object to control the game's speed (frames per second).
clock = pygame.time.Clock()

# Define colors used in the game.
# Colors are defined as RGB tuples: (Red, Green, Blue) where each value is from 0 to 255.
WHITE = (255, 255, 255)  # Pure white color, often used for text.
BLACK = (0, 0, 0)  # Pure black color, used for backgrounds or text.
RED = (255, 0, 0)  # Bright red color, used for warnings or highlights.
GREEN = (0, 255, 0)  # Bright green color, used for positive indicators.
BLUE = (0, 0, 255)  # Bright blue color, used for UI elements.
# Note: These are basic colors; the game mainly uses images for visuals.

# Load the game background image.
background = pygame.image.load(resource_path('back.jpg'))  # Load the background image file.

# Load a font for displaying text.
# 'comic.ttf' is a custom font file; if not found, Pygame might fall back to a default.
font = pygame.font.Font(resource_path('comic.ttf'), 42)  # Create a font object with size 42.

# Render the score text initially.
# render() creates an image of the text that can be drawn on the screen.
score_text = font.render('Score : ' + str(score), True, (255, 255, 255))  # True enables anti-aliasing for smoother text.

# Load the image for lives (hearts or crosses).
lives_icon = pygame.image.load(resource_path('images/white_lives.png'))  # Image showing remaining lives.

# Generalized structure of the fruit Dictionary.
# This function sets up the properties for each fruit or bomb.
def generate_random_fruits(fruit):
    """
    Generate random properties for a fruit or bomb.

    This function creates a dictionary entry for each entity (fruit or bomb) with random position, speed, etc.
    It determines if the entity should be thrown (visible) or not.

    Parameters:
    fruit (str): The name of the fruit or 'bomb' (e.g., 'melon', 'bomb').

    No return value. Modifies the global 'data' dictionary.
    """
    
    # Create the file path for the fruit's image.
    fruit_path = resource_path("images/" + fruit + ".png")  # Combine path to get 'images/melon.png', etc.

    # Create a dictionary for this fruit with various properties.
    data[fruit] = {
        'img': pygame.image.load(fruit_path),  # Load the image for this fruit.
        'x': random.randint(100, 500),  # Random x-position where the fruit starts (between 100 and 500 pixels).
        'y': 800,  # Starting y-position: off the top of the screen (800 is below the visible area).
        'speed_x': random.randint(-10, 10),  # Random horizontal speed: left or right movement (-10 to 10).
        'speed_y': random.randint(-80, -60),  # Initial vertical speed: upward movement (-80 to -60, negative means up).
        'throw': False,  # Boolean: True if the fruit should be thrown (visible), False otherwise.
        't': 0,  # Time counter: used to increase gravity over time.
        'hit': False,  # Boolean: True if the fruit has been sliced, False otherwise.
    }

    # Randomly decide if this fruit should be thrown (75% chance to throw, 25% to not).
    if random.random() >= 0.75:  # random.random() returns a float between 0.0 and 1.0.
        data[fruit]['throw'] = True  # Throw this fruit.
    
    else:
        data[fruit]['throw'] = False  # Don't throw this fruit.

# Dictionary to hold the data for all fruits and bombs.
# This will be populated by calling generate_random_fruits for each.
data = {}  # Empty dictionary initially.

# Generate data for each fruit and bomb.
for fruit in fruits:  # Loop through the list ['melon', 'orange', 'pomegranate', 'guava', 'bomb'].
    generate_random_fruits(fruit)  # Call the function to set up each one.

def hide_cross_lives(x, y):
    """
    Draw a red cross over a life icon to indicate a lost life.

    This function is called when the player hits a bomb, to visually remove a life.

    Parameters:
    x (int): The x-coordinate where to draw the cross.
    y (int): The y-coordinate where to draw the cross.

    No return value. Draws directly to the screen.
    """
    
    # Load and draw the red cross image over the life icon.
    gameDisplay.blit(pygame.image.load(resource_path("images/red_lives.png")), (x, y))
    # blit() draws one surface onto another. Here, it draws the red cross at position (x, y).

# Generic method to draw fonts on the screen.
# This is a helper function to display text at any position.
font_name = pygame.font.match_font('comic.ttf')  # Find the font file; match_font() searches system fonts if not found.

def draw_text(display, text, size, x, y):
    """
    Draw text on the screen at a specified position.

    This function renders text with a given size and draws it centered at (x, y).

    Parameters:
    display: The surface to draw on (usually gameDisplay).
    text (str): The text to display.
    size (int): The font size.
    x (int): The x-coordinate to center the text at.
    y (int): The y-coordinate to center the text at.

    No return value. Draws directly to the screen.
    """
    
    # Create a font object with the specified size.
    font = pygame.font.Font(font_name, size)
    # Render the text into a surface (image).
    text_surface = font.render(text, True, WHITE)  # True for anti-aliasing, WHITE color.
    # Get the rectangle of the text surface for positioning.
    text_rect = text_surface.get_rect()
    # Center the text at the given coordinates.
    text_rect.midtop = (x, y)  # midtop means center horizontally, top at y.
    # Draw the text surface onto the display.
    gameDisplay.blit(text_surface, text_rect)

# Draw players lives on the screen.
def draw_lives(display, x, y, lives, image):
    """
    Draw the life icons on the screen.

    This shows how many lives the player has left by drawing icons side by side.

    Parameters:
    display: The surface to draw on.
    x (int): The starting x-coordinate for the first life icon.
    y (int): The y-coordinate for all life icons.
    lives (int): The number of lives to display.
    image (str): The path to the life icon image.

    No return value. Draws directly to the screen.
    """
    
    # Loop for each life the player has.
    for i in range(lives):  # range(lives) gives 0, 1, 2 for lives=3.
        
        # Load the life icon image.
        img = pygame.image.load(resource_path(image))
        # Get the rectangle for positioning.
        img_rect = img.get_rect()
        # Set the x-position: start at x, then add 35 pixels for each additional life.
        img_rect.x = int(x + 35 * i)  # 35 pixels spacing between icons.
        # Set the y-position: same for all.
        img_rect.y = y
        # Draw the icon on the display.
        display.blit(img, img_rect)

# Show game over display & front display.
def show_gameover_screen():
    """
    Display the game over screen.

    This shows the final score and waits for the player to press a key to restart or quit.

    No return value. Handles the game over state.
    """
    
    # Draw the background image.
    gameDisplay.blit(background, (0, 0))
    # Draw the title text.
    draw_text(gameDisplay, "FRUIT NINJA!", 90, WIDTH / 2, HEIGHT / 4)
    
    # If the game is not over (first time showing), display the score.
    if not game_over:
        draw_text(gameDisplay, "Score : " + str(score), 50, WIDTH / 2, HEIGHT / 2)
    
    # Draw the instruction text.
    draw_text(gameDisplay, "Press a key to begin!", 64, WIDTH / 2, HEIGHT * 3 / 4)
    # Update the display to show the changes.
    pygame.display.flip()
    # Set waiting to True to enter the loop.
    waiting = True
    
    # Loop until a key is pressed.
    while waiting:
        
        # Limit the loop to FPS to avoid using too much CPU.
        clock.tick(FPS)
        
        # Check for events.
        for event in pygame.event.get():
            
            # If the window close button is clicked.
            if event.type == pygame.QUIT:
                # User closed the window during game over screen.
                pygame.quit()  # Shut down Pygame.
                sys.exit()  # Exit the program.
            
            # If a key is released.
            if event.type == pygame.KEYUP:
                waiting = False  # Exit the waiting loop.

# Game Loop
# This is the main loop that runs the game. It continues until the player quits.
first_round = True  # Boolean: True for the first game start, to show the initial screen.
game_over = True  # Boolean: True when the game is over, False during gameplay.
game_running = True  # Boolean: True while the game is running, False to exit.

while game_running:  # Main game loop.
    
    # If the game is over, reset and start a new round.
    if game_over:
        
        # If it's the first round, show the game over screen (which acts as start screen).
        if first_round:
            show_gameover_screen()  # Display the start screen.
            first_round = False  # Set to False so it doesn't show again.
        
        # Reset game_over to False to start playing.
        game_over = False
        # Reset player lives to 3.
        player_lives = 3
        # Draw the life icons.
        draw_lives(gameDisplay, 690, 5, player_lives, 'images/red_lives.png')
        # Reset score to 0.
        score = 0
        # Update the score text.
        score_text = font.render('Score : ' + str(score), True, (255, 255, 255))
        # Regenerate fruits for a fresh round.
        data = {}  # Clear the data dictionary.
        
        for fruit in fruits:  # Loop through fruits again.
            generate_random_fruits(fruit)  # Generate new random properties.

    # Handle events: user input like mouse clicks or closing window.
    for event in pygame.event.get():  # Get all pending events.
        
        # If the window close button is clicked.
        if event.type == pygame.QUIT:
            game_running = False  # Exit the main loop.

    # Draw the background.
    gameDisplay.blit(background, (0, 0))
    # Draw the score text.
    gameDisplay.blit(score_text, (0, 0))
    # Draw the life icons.
    draw_lives(gameDisplay, 690, 5, player_lives, 'images/red_lives.png')

    # Loop through each fruit in the data dictionary.
    for key, value in data.items():  # key is 'melon', etc.; value is the dict of properties.
        
        # If this fruit is thrown (visible).
        if value['throw']:
            
            # Update the x-position based on speed_x.
            value['x'] += value['speed_x']  # Move left or right.
            # Update the y-position based on speed_y.
            value['y'] += value['speed_y']  # Move up or down.
            # Increase the downward speed (gravity effect).
            value['speed_y'] += (1 * value['t'])  # 't' increases over time, making it fall faster.
            # Increment the time counter.
            value['t'] += 1  # Used for gravity.

            # If the fruit is still on screen (y <= 800, but 800 is the bottom).
            if value['y'] <= 800:
                # Draw the fruit image at its current position.
                gameDisplay.blit(value['img'], (value['x'], value['y']))
            
            else:
                # If off screen, generate a new random fruit.
                generate_random_fruits(key)

            # Get the current mouse position as (x, y) coordinates.
            current_position = pygame.mouse.get_pos()  # Returns (mouse_x, mouse_y).

            # Check if the mouse is over the fruit and it hasn't been hit yet.
            if not value['hit'] and current_position[0] > value['x'] and current_position[0] < value['x'] + 60 \
                    and current_position[1] > value['y'] and current_position[1] < value['y'] + 60:
                
                # The fruit is 60x60 pixels, so check if mouse is within that rectangle.
                if key == 'bomb':  # If it's a bomb.
                    player_lives -= 1  # Decrease lives by 1.
                    
                    if player_lives == 0:  # If no lives left.
                        hide_cross_lives(690, 15)  # Hide the first life.
                    
                    elif player_lives == 1:  # If 1 life left.
                        hide_cross_lives(725, 15)  # Hide the second life.
                    
                    elif player_lives == 2:  # If 2 lives left.
                        hide_cross_lives(760, 15)  # Hide the third life.
                    
                    # If lives go below 0 (shouldn't happen, but safety).
                    if player_lives < 0:
                        show_gameover_screen()  # Show game over.
                        game_over = True  # End the game.
                    
                    # Set the image to explosion.
                    half_fruit_path = "images/explosion.png"
                
                else:  # If it's a fruit.
                    # Set the image to the half fruit.
                    half_fruit_path = "images/" + "half_" + key + ".png"
                
                # Load the new image (half fruit or explosion).
                value['img'] = pygame.image.load(resource_path(half_fruit_path))
                # Increase the horizontal speed for effect.
                value['speed_x'] += 10
                
                # If not a bomb, increase score.
                if key != 'bomb':
                    score += 1  # Add 1 point.
                
                # Update the score text.
                score_text = font.render('Score : ' + str(score), True, (255, 255, 255))
                # Mark the fruit as hit.
                value['hit'] = True
        
        else:  # If not thrown.
            generate_random_fruits(key)  # Regenerate it.

    # Update the display with all the drawings.
    pygame.display.update()
    # Limit the game to run at FPS frames per second.
    clock.tick(FPS)


# After the loop, quit Pygame and exit.
pygame.quit()
sys.exit()
