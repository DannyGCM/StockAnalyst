# splash_screen.py
# Danny Garcia

# Imports
import pygame as pg


# Main function
def load_splash(window, clock):
    # Surfaces
    splash_screen = [pg.image.load("visual_data/_splash_screen/splash_screen_{:02.0f}.png".format(frame))
                     for frame in range(30)]

    # Frames in splash screen animation
    animation_frames = []

    # Splash screen animation frames build - Total 4.0 Seconds
    # Adjust for loops to alter duration of splash screen
    # Part 1 - Wait (0.5 Second[s])
    for frame in range(30):
        animation_frames += [splash_screen[0]]

    # Part 2 - Light up (1.0 Second[s])
    for frame in range(60):
        if not frame % 2:
            animation_frames += [splash_screen[frame // 2]]

    # Part 3 - Wait (1.0 Second[s])
    for frame in range(60):
        animation_frames += [splash_screen[29]]

    # Part 4 - Light down (1.0 Second[s])
    for frame in range(60):
        if not frame % 2:
            animation_frames += [splash_screen[29 - frame // 2]]

    # Part 5 - Wait (0.5 Second[s])
    for frame in range(30):
        animation_frames += [splash_screen[0]]

    # Frame counter
    frame = 0

    # Splash screen loop
    while True:
        # Event handling
        for event in pg.event.get():
            # Closes window with X button (Not the key)
            if event.type == pg.QUIT:
                return False

        # Displays next frame if possible
        if frame != len(animation_frames) - 1:
            window.blit(animation_frames[frame], (0, 0))
            frame += 1
        else:
            break

        # Screen update
        pg.display.flip()
        clock.tick(30)

    # If all frames have been successfully displayed, continue the program
    return True
