# main.py
# Danny Garcia

# About: Stock Analyst is meant to be used as a basic helper tool in the stock market. Predictions should
# not be blindly followed. Always do research and buy responsibly.

# Imports
from script_data.profile_class import Profile
import script_data.main_scene as main_scene
from os import environ
import pygame as pg


# Main function
def main():
    # Sets the window's start position to the center of the screen
    environ["SDL_VIDEO_CENTERED"] = "0"

    # Window initialization
    pg.init()
    window = pg.display.set_mode((1280, 720))
    pg.display.set_caption("Stock Analyst")

    # Sets application's icon
    icon_surface = pg.image.load("visual_data/other/icon.png")
    pg.display.set_icon(icon_surface)

    # Acquires or generates a user profile as needed
    profile = Profile("profile.stock")

    # Runs main scene
    main_scene.load_scene(window, profile)

    # Finalizes program
    pg.quit()


# Main call
if __name__ == "__main__":
    main()
