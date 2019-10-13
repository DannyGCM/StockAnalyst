# main_scene.py
# Danny Garcia

# Imports
from script_data.update_predictions import up_predictions
from script_data.predictions_class import Predictions
from script_data.main_ticker_class import MainTicker
from script_data.search_bar_class import SearchBar
from script_data.splash_screen import load_splash
from script_data.update_files import up_files
from script_data.ticker_class import Ticker
from threading import Thread
from sys import exit
import pygame as pg


# Main function
def load_scene(window, profile):
    # Sequence variables
    running = True

    # FPS tracker
    clock = pg.time.Clock()

    # Sound effects
    bell_ding = pg.mixer.Sound("audio_data/bell_ding.wav")

    # Surfaces
    base_gradient = pg.image.load("visual_data/_backgrounds/base_gradient.png")
    info_container = pg.image.load("visual_data/_backgrounds/info_container.png")
    main_container = pg.image.load("visual_data/_backgrounds/main_container.png")
    predictions_container = pg.image.load("visual_data/_backgrounds/predictions_container.png")
    loading_screen = pg.image.load(f"visual_data/other/loading_screen.png")

    panel_padding = pg.image.load("visual_data/_panels/panel_padding.png")
    border = pg.image.load("visual_data/other/border.png")

    # Main ticker
    main_ticker = MainTicker(window, profile)

    # Profile tickers initialization
    collection = [Ticker(window, profile, (0, 204 + 129 * ticker), main_ticker, ticker + 1) for ticker in range(4)]
    for ticker in collection:
        ticker.collection = collection

    # Main ticker initialization
    for ticker in collection:
        if ticker.ticker != "N/A":
            ticker.active = True
            ticker.main_ticker.ticker = ticker.ticker
            ticker.main_ticker.initialize()
            break

    # Search bar
    search_bar = SearchBar(window)
    search_bar.collection = collection

    # Predictions object
    predictions_pannel = Predictions(window, profile)

    # Displays splash screen
    running = load_splash(window, clock)

    # Main loop
    while running:
        # Update if required
        if profile.updating:
            window.blit(loading_screen, (0, 0))

            # Screen update
            pg.display.flip()

            up_files(profile)
            up_predictions(profile, predictions_pannel)

            pg.mixer.Sound.play(bell_ding)

        # Event handling
        for event in pg.event.get():
            # Closes window with X button (Not the key)
            if event.type == pg.QUIT:
                running = False
            # Clicked
            if event.type == pg.MOUSEBUTTONDOWN:
                for item in collection + [main_ticker, search_bar, predictions_pannel]:
                    item.universal_click = True
            # Didn't click
            else:
                for item in collection + [main_ticker, search_bar, predictions_pannel]:
                    item.universal_click = False
            # Key presses for search bar
            if event.type == pg.KEYDOWN:
                search_bar.key_press = event.key

        # Static graphics
        window.blit(base_gradient, (0, 0))
        window.blit(main_container, (355, 24))
        window.blit(info_container, (355, 462))
        window.blit(predictions_container, (935, 462))
        window.blit(panel_padding, (0, 0))

        # Updates
        for item in collection + [main_ticker, search_bar, predictions_pannel]:
            item.update()

        # Border
        window.blit(border, (0, 0))

        # Screen update
        clock.tick(60)
        pg.display.flip()
