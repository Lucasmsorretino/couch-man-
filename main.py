import pygame
import random


# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600  # The dimensions of the game window
GRID_SIZE = 30  # Each cell in the grid is 30x30 pixels
ROWS, COLS = HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE  # Number of rows and columns in the grid
WHITE = (255, 255, 255)  # Color for empty paths and pellets
BLACK = (0, 0, 0)  # Background color
YELLOW = (255, 255, 0)  # Color for Pac-Manr
RED = (255, 0, 0)  # Color for ghosts
BLUE = (0, 0, 255)  # Color for walls

# Maze grid (1 = Wall, 0 = Empty path, 2 = Pellet, 3 = Ghost, 4 = Pac-Man)
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 3, 1, 0, 1, 3, 0, 0, 0, 0, 1, 3, 1, 0, 1, 3, 0, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Store pellet positions separately
pellet_positions = [(row_idx, col_idx) for row_idx, row in enumerate(maze) for col_idx, cell in enumerate(row) if cell == 2]



def draw_maze(screen):
    for row_idx, row in enumerate(maze):
        for col_idx, cell in enumerate(row):
            x, y = col_idx * GRID_SIZE, row_idx * GRID_SIZE
            if cell == 1:
                pygame.draw.rect(screen, BLUE, (x, y, GRID_SIZE, GRID_SIZE))
            elif cell == 2:
                pygame.draw.circle(screen, WHITE, (x + GRID_SIZE // 2, y + GRID_SIZE // 2), 5)
            elif cell == 3:
                pygame.draw.circle(screen, RED, (x + GRID_SIZE // 2, y + GRID_SIZE // 2), 12)
            elif cell == 4:
                pygame.draw.circle(screen, YELLOW, (x + GRID_SIZE // 2, y + GRID_SIZE // 2), 12)





# Get Pac-Man & Ghost positions
def get_positions():
    pacman_pos = None
    ghost_positions = []
    for row_idx, row in enumerate(maze):
        for col_idx, cell in enumerate(row):
            if cell == 4:
                pacman_pos = [row_idx, col_idx]
            elif cell == 3:
                ghost_positions.append([row_idx, col_idx])
    return pacman_pos, ghost_positions

pacman_pos, ghost_positions = get_positions()
score = 0
lives = 3


def move_pacman(direction, screen):
    global pacman_pos, score
    row, col = pacman_pos
    new_row, new_col = row, col
    
    if direction == "UP":
        new_row -= 1
    elif direction == "DOWN":
        new_row += 1
    elif direction == "LEFT":
        new_col -= 1
    elif direction == "RIGHT":
        new_col += 1
    
    if maze[new_row][new_col] != 1:  # Check if the new position is not a wall
        if (new_row, new_col) in pellet_positions:  # Check if Pac-Man eats a pellet
            pellet_positions.remove((new_row, new_col))  # Remove the pellet
            score += 10  # Increase the score
        
        maze[row][col] = 0  # Clear old position
        maze[new_row][new_col] = 4  # Move Pac-Man
        pacman_pos = [new_row, new_col]  # Update Pac-Man’s position
    
    check_collision(screen)  # Check if Pac-Man collides with a ghost

def move_ghosts(screen):
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Right, Left, Down, Up
    for ghost in ghost_positions:
        row, col = ghost
        random.shuffle(directions)  # Randomize movement direction
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            if maze[new_row][new_col] in [0, 2]:  # Check if new position is an empty path or pellet
                maze[row][col] = 0  # Restore empty path
                if (row, col) in pellet_positions:
                    maze[row][col] = 2  # Restore pellet if ghost was on one
                
                ghost[0], ghost[1] = new_row, new_col  # Update ghost position
                maze[new_row][new_col] = 3  # Move ghost
                break
    check_collision(screen)  # Check if a ghost has collided with Pac-Man



def check_collision(screen):
    global lives, pacman_pos
    for ghost in ghost_positions:
        if pacman_pos == ghost:  # Check if Pac-Man and a ghost occupy the same position
            lives -= 1  # Decrease lives count
            
            if lives > 0:
                display_message(screen, "You lost a life!", RED)  # Show a message if lives remain
            if lives == 0:
                display_message(screen, "Game Over!", RED)  # Show game over message
                pygame.quit()
                exit()
            
            # Reset Pac-Man position and update the maze immediately
            old_row, old_col = pacman_pos
            maze[old_row][old_col] = 0  # Clear old position
            pacman_pos = [1, 1]  # Reset Pac-Man to the starting position
            maze[1][1] = 4  # Place Pac-Man back on the grid


def display_message(screen, message, color=WHITE):
    font = pygame.font.Font(None, 50)  # Set the font size to 50
    text = font.render(message, True, color)  # Render the message text
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Center the text on the screen
    
    screen.blit(text, text_rect)  # Draw the message on the screen
    pygame.display.flip()  # Update the display to show the message
    pygame.time.delay(2000)  # Pause for 2 seconds before continuing


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Create the game window
    pygame.display.set_caption("Pac-Man (Beginner Version)")  # Set window title
    clock = pygame.time.Clock()  # Initialize game clock
    
    while True:
        screen.fill(BLACK)  # Clear screen to black before drawing
        draw_maze(screen)  # Render the maze and all game elements
        
        # Display score and lives
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (WIDTH - 100, 10))
        
        move_ghosts(screen)  # Update ghost positions
        pygame.display.flip()  # Update the display with new frame
        
        # Handle user inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move_pacman("UP", screen)
                elif event.key == pygame.K_DOWN:
                    move_pacman("DOWN", screen)
                elif event.key == pygame.K_LEFT:
                    move_pacman("LEFT", screen)
                elif event.key == pygame.K_RIGHT:
                    move_pacman("RIGHT", screen)
        
        clock.tick(5)  # Control game speed
    
if __name__ == "__main__":
    main()