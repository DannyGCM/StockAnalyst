# confirmation_screen.py
# Danny Garcia

# Imports
import pygame as pg
from sys import exit


# Main function
def load_confirmation(window, profile, screenshot):
    # FPS tracker
    clock = pg.time.Clock()
    screen_filter = pg.Surface((1280, 720))
    screen_filter.set_alpha(150)
    screen_filter.fill((0, 0, 0))

    # Fonts
    open_sans_50 = pg.font.Font("visual_data/open_sans.ttf", 50)
    open_sans_40 = pg.font.Font("visual_data/open_sans.ttf", 40)
    open_sans_20 = pg.font.Font("visual_data/open_sans.ttf", 20)

    # Renders
    yes_render = open_sans_40.render("YES", False, (170, 170, 180))
    no_render = open_sans_40.render("NO", False, (170, 170, 180))
    warning_part_1 = open_sans_50.render("ARE YOU SURE YOU WANT TO UPDATE", False, (170, 170, 180))
    warning_part_2 = open_sans_50.render("ALL PREDICTIONS AN TICKERS?", False, (170, 170, 180))
    warning_part_3 = open_sans_20.render("(THIS MIGHT TAKE A FEW HOURS)", False, (170, 170, 180))

    # Statuses
    yes_button_status = "Inactive"
    no_button_status = "Inactive"

    # Confirmation loop
    while True:
        # Event handling
        for event in pg.event.get():
            # Closes window with X button (Not the key)
            if event.type == pg.QUIT:
                exit()
            # Clicked
            if event.type == pg.MOUSEBUTTONDOWN:
                yes_button_status, no_button_status = update(True)
            # Didn't click
            else:
                yes_button_status, no_button_status = update(False)

        # Checks click status for yes button
        if yes_button_status == "Clicked":
            profile.updating = True
            profile.save_data()
            break

        # Checks click status for no button
        if no_button_status == "Clicked":
            break

        # Draws screen background
        window.blit(screenshot, (0, 0))
        window.blit(screen_filter, (0, 0))
        pg.draw.rect(window, (74, 74, 79), (0, 210, 1280, 300))
        window.blit(warning_part_1, (165, 260))
        window.blit(warning_part_2, (240, 310))
        window.blit(warning_part_3, (450, 370))

        # Draws yes button
        if yes_button_status != "Inactive":
            pg.draw.rect(window, (64, 64, 69), (400, 420, 180, 70))
        else:
            pg.draw.rect(window, (54, 54, 59), (400, 420, 180, 70))

        # Draws no button
        if no_button_status != "Inactive":
            pg.draw.rect(window, (64, 64, 69), (640, 420, 180, 70))
        else:
            pg.draw.rect(window, (54, 54, 59), (640, 420, 180, 70))

        window.blit(yes_render, (455, 428))
        window.blit(no_render, (700, 428))

        # Screen update
        pg.display.flip()
        clock.tick(30)


# Updates the status of the yes and no buttons
def update(clicked):
    # Gets mouse position
    mouse_position = pg.mouse.get_pos()
    yes_status = "N/A"
    no_status = "N/A"

    # Updates yes button status
    if 400 <= mouse_position[0] <= 580 and 420 <= mouse_position[1] <= 490:
        if clicked:
            yes_status = "Clicked"
        else:
            yes_status = "Hovered"
    else:
        yes_status = "Inactive"

    # Updates no button status
    if 640 <= mouse_position[0] <= 820 and 420 <= mouse_position[1] <= 490:
        if clicked:
            no_status = "Clicked"
        else:
            no_status = "Hovered"
    else:
        no_status = "Inactive"

    return yes_status, no_status
