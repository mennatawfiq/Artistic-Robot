import pygame
from src.game import Game

def main():
    """Initialize and run the simulation."""
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"Error running simulation: {e}")
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()