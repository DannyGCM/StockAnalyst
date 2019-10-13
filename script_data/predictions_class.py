# predictions_class.py
# Danny Garcia

# Imports
import script_data.confirmation_screen as confirmation_screen
import pygame as pg


# Predictions class: Makes and displays predictions.
class Predictions:
    def __init__(self, window, profile):
        # Argument[s]
        self.window = window
        self.profile = profile

        # General class properties
        self.universal_click = False
        self.prediction_index = 0
        self.prediction_type = "Increasing"
        self.prediction_batch = self.profile.predictions[0]

        # Status[es]
        self.left_arrow_status = "Inactive"
        self.right_arrow_status = "Inactive"
        self.prediction_type_status = "Inactive"
        self.update_button_status = "Inactive"

        # Surface[s]
        self.left_arrows = [pg.image.load(f"visual_data/_buttons/left_arrow_{image}.png") for image in range(2)]
        self.right_arrows = [pg.image.load(f"visual_data/_buttons/right_arrow_{image}.png") for image in range(2)]

        # Font[s]
        self.open_sans_30 = pg.font.Font("visual_data/open_sans.ttf", 30)

        # Render[s]
        self.prediction_index_text = self.open_sans_30.render(self.prediction_batch[0], False, (42, 119, 166))
        increasing_text = [self.open_sans_30.render("INCREASING", False, [(42, 119, 166), (195, 240, 248)][render]) for
                           render in range(2)]
        neutral_text = [self.open_sans_30.render("NEUTRAL", False, [(42, 119, 166), (195, 240, 248)][render]) for render
                        in range(2)]
        decreasing_text = [self.open_sans_30.render("DECREASING", False, [(42, 119, 166), (195, 240, 248)][render]) for
                           render in range(2)]
        self.prediction_types = [increasing_text, neutral_text, decreasing_text]
        self.update_button = [pg.image.load(f"visual_data/_buttons/update_button_{image}.png") for image in range(2)]

    # Updates information
    def update(self):
        # Gets mouse position
        mouse_position = pg.mouse.get_pos()

        # Updates left arrow status
        if 949 <= mouse_position[0] <= 1093 and 630 <= mouse_position[1] <= 687:
            if self.universal_click:  # Clicked
                self.left_arrow_status = "Clicked"
                self.prediction_index = self.prediction_index - 1 if self.prediction_index > 0 else 8
                self.prediction_index_text = self.open_sans_30.render(self.prediction_batch[self.prediction_index],
                                                                      False, (42, 119, 166))
                self.universal_click = False
            else:
                self.left_arrow_status = "Hovered"
        else:
            self.left_arrow_status = "Inactive"

        # Updates right arrow status
        if 1111 <= mouse_position[0] <= 1256 and 630 <= mouse_position[1] <= 687:
            if self.universal_click:  # Clicked
                self.right_arrow_status = "Clicked"
                self.prediction_index = self.prediction_index + 1 if self.prediction_index < 8 else 0
                self.prediction_index_text = self.open_sans_30.render(self.prediction_batch[self.prediction_index],
                                                                      False, (42, 119, 166))
                self.universal_click = False
            else:
                self.right_arrow_status = "Hovered"
        else:
            self.right_arrow_status = "Inactive"

        # Updates prediction type status
        if 967 <= mouse_position[0] <= 1154 and 490 <= mouse_position[1] <= 516:
            if self.universal_click:  # Clicked
                self.prediction_type_status = "Clicked"
                if self.prediction_type == "Increasing":
                    self.prediction_type = "Neutral"
                    self.prediction_batch = self.profile.predictions[1]
                elif self.prediction_type == "Neutral":
                    self.prediction_type = "Decreasing"
                    self.prediction_batch = self.profile.predictions[2]
                else:
                    self.prediction_type = "Increasing"
                    self.prediction_batch = self.profile.predictions[0]
                self.prediction_index_text = self.open_sans_30.render(self.prediction_batch[self.prediction_index],
                                                                      False, (42, 119, 166))
                self.universal_click = False
            else:
                self.prediction_type_status = "Hovered"
        else:
            self.prediction_type_status = "Inactive"

        # Draws now updated object
        self.draw_self()

        # Updates update button
        if 1191 <= mouse_position[0] <= 1242 and 480 <= mouse_position[1] <= 525:
            if self.universal_click:  # Clicked
                self.update_button_status = "Clicked"
                pg.image.save(self.window, "visual_data/other/screenshot.png")
                screenshot = pg.image.load("visual_data/other/screenshot.png")
                confirmation_screen.load_confirmation(self.window, self.profile, screenshot)
            else:
                self.update_button_status = "Hovered"
        else:
            self.update_button_status = "Inactive"

        # outside draw function to update screenshot
        # Draw prediction type
        if self.prediction_type_status != "Inactive":
            self.window.blit(
                self.prediction_types[["Increasing", "Neutral", "Decreasing"].index(self.prediction_type)][1],
                (1059 - self.open_sans_30.size(self.prediction_type.upper())[0] // 2, 480))
        else:
            self.window.blit(
                self.prediction_types[["Increasing", "Neutral", "Decreasing"].index(self.prediction_type)][0],
                (1059 - self.open_sans_30.size(self.prediction_type.upper())[0] // 2, 480))

    # Draws object
    def draw_self(self):
        # Draws left arrow
        if self.left_arrow_status != "Inactive":
            self.window.blit(self.left_arrows[1], (1010, 643))
        else:
            self.window.blit(self.left_arrows[0], (1010, 643))

        # Draws right arrow
        if self.right_arrow_status != "Inactive":
            self.window.blit(self.right_arrows[1], (1175, 643))
        else:
            self.window.blit(self.right_arrows[0], (1175, 643))

        # Draw update button
        if self.update_button_status != "Inactive":
            self.window.blit(self.update_button[1], (1191, 480))
        else:
            self.window.blit(self.update_button[0], (1191, 480))

        # Draw prediction
        self.window.blit(self.prediction_index_text,
                         (1102 - self.open_sans_30.size(self.prediction_batch[self.prediction_index])[0] // 2, 558))
