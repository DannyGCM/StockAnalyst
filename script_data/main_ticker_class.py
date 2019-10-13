# main_ticker_obj.py
# Danny Garcia

# Imports
from script_data.main_info_class import MainInfo
from statistics import mean
import pandas as pd
import pygame as pg
import threading


# Main Ticker class: Class in charge of the selected ticker and the management of its information.
class MainTicker:
    def __init__(self, window, profile):
        # Arguments
        self.window = window
        self.profile = profile

        # General class properties
        self.universal_click = False
        self.visual_mean = 0
        self.visual_max = 0
        self.ticker = "N/A"
        self.ticker_df = "N/A"
        self.fixed_ticker_df = "N/A"
        
        # Status[es]
        self.time_status = ["Inactive"] * 4
        self.max_box_button_status = "Inactive"
        self.mean_box_button_status = "Inactive"

        # Profile data
        self.time_scale = self.profile.company_settings["time_scale"]
        self.show_max = self.profile.company_settings["show_max"]
        self.show_mean = self.profile.company_settings["show_mean"]

        # Surface[s]
        self.grid = pg.image.load("visual_data/other/grid.png")
        self.max_tag = pg.image.load("visual_data/other/max_tag.png")
        self.mean_tag = pg.image.load("visual_data/other/mean_tag.png")
        self.tab_logo = pg.image.load("visual_data/other/logo.png")
        self.checkboxes = [pg.image.load(f"visual_data/_buttons/checkbox_{image}.png") for image in range(4)]

        # Font[s]
        self.open_sans_40 = pg.font.Font("visual_data/open_sans.ttf", 40)

        # Render[s]
        self.ticker_name = "N/A"  # Temporary value, should never equal "N/A" while in use
        self.max_text = self.open_sans_40.render("MAX", False, (42, 119, 166))
        self.mean_text = self.open_sans_40.render("MEAN", False, (42, 119, 166))

        scale_letters_all = [self.open_sans_40.render("A", False, i) for i in
                             [(42, 119, 166), (195, 240, 248), (255, 255, 255)]]
        scale_letters_year = [self.open_sans_40.render("Y", False, i) for i in
                              [(42, 119, 166), (195, 240, 248), (255, 255, 255)]]
        scale_letters_month = [self.open_sans_40.render("M", False, i) for i in
                               [(42, 119, 166), (195, 240, 248), (255, 255, 255)]]
        scale_letters_week = [self.open_sans_40.render("W", False, i) for i in
                              [(42, 119, 166), (195, 240, 248), (255, 255, 255)]]

        self.scale_letters = [scale_letters_all, scale_letters_year, scale_letters_month,
                              scale_letters_week]

        # Other
        self.info = MainInfo(self.window, self)

    # Makes updated information usable
    def initialize(self, redefine_data=True):
        # Check that ticker was defined
        if self.ticker == "N/A":
            raise Exception("Ticker must be defined before initialization.")

        # Update information if required
        if redefine_data:
            self.info.fetch_info()

        # Renders ticker name
        self.ticker_name = self.open_sans_40.render(self.ticker, False, (42, 119, 166))

        # Gathers and normalizes ticker data
        self.ticker_df = pd.read_csv(f"ticker_data/{self.ticker}.csv")
        self.ticker_df = self.ticker_df.iloc[range(len(self.ticker_df)), [4]]
        self.ticker_df = self.ticker_df["Close"].tolist()

        # Fixes time scale and data frame as necessary based on ticker history time
        if self.time_scale != "A":  # Time scale isn't all of history
            if self.time_scale == "Y":  # Year
                if len(self.ticker_df) < 240:  # Make month if data is not long enough
                    self.time_scale = "M"
                    self.profile.company_settings["time_scale"] = "M"
                else:
                    self.ticker_df = self.ticker_df[len(self.ticker_df) - 240: len(self.ticker_df)]
                    self.ticker_df = self.ticker_df[::10]
                    self.profile.company_settings["time_scale"] = "Y"
            if self.time_scale == "M":  # Month
                if len(self.ticker_df) < 20:  # Make week if data is not long enough
                    self.time_scale = "W"
                    self.profile.company_settings["time_scale"] = "W"
                else:
                    self.ticker_df = self.ticker_df[len(self.ticker_df) - 20: len(self.ticker_df)]
                    self.profile.company_settings["time_scale"] = "M"
            if self.time_scale == "W":  # Week
                self.ticker_df = self.ticker_df[len(self.ticker_df) - 5: len(self.ticker_df)]
                self.profile.company_settings["time_scale"] = "W"
        else:
            parsing_metric = len(self.ticker_df) // 24  # 24 points
            self.ticker_df = self.ticker_df[::-parsing_metric]
            self.ticker_df = self.ticker_df[::-1]
            self.profile.company_settings["time_scale"] = "A"

        # Saves time data
        self.profile.save_data()

        # Resets time status based on new time status
        self.time_status = ["Inactive"] * 4
        self.time_status[["A", "Y", "M", "W"].index(self.time_scale)] = "Clicked"

        # Sets max, mean, and fixed ticker df (For visuals)
        difference = 291 / (max(self.ticker_df) + 25)
        self.fixed_ticker_df = [self.ticker_df[i] * difference for i in range(len(self.ticker_df))]

        self.visual_mean = mean(self.fixed_ticker_df)
        self.visual_max = max(self.fixed_ticker_df)

    # Updates information
    def update(self):
        # Gets mouse position
        mouse_position = pg.mouse.get_pos()

        # Updates max box button status
        if 1020 <= mouse_position[0] <= 1052 and 47 <= mouse_position[1] <= 79:
            if self.universal_click:  # Clicked
                self.max_box_button_status = "Clicked"
                self.show_max = False if self.show_max else True
                self.profile.company_settings["show_max"] = self.show_max
                self.profile.save_data()
                self.universal_click = False
            else:
                self.max_box_button_status = "Hovered"
        else:
            self.max_box_button_status = "Inactive"

        # Updates mean box button status
        if 880 <= mouse_position[0] <= 912 and 47 <= mouse_position[1] <= 79:
            if self.universal_click:  # CLicked
                self.mean_box_button_status = "Clicked"
                self.show_mean = False if self.show_mean else True
                self.profile.company_settings["show_mean"] = self.show_mean
                self.profile.save_data()
                self.universal_click = False
            else:
                self.mean_box_button_status = "Hovered"
        else:
            self.mean_box_button_status = "Inactive"

        # Updates time statuses
        for status in range(len(self.time_status)):
            # Mouse is on top of any given time scale button
            # Condition --->
            if (2 <= status <= 3 and (1080 + status * 40 <= mouse_position[0] <= 1080 + status * 40 +
                                      self.scale_letters[status][0].get_size()[0]) and
                (35 <= mouse_position[1] <= 35 + self.scale_letters[status][0].get_size()[1])) or \
                    (0 <= status <= 1 and (1100 + status * 30 <= mouse_position[0] <= 1100 + status * 30 +
                                           self.scale_letters[status][0].get_size()[0]) and
                     (35 <= mouse_position[1] <= 35 + self.scale_letters[status][0].get_size()[1])):  # <---

                if self.universal_click:  # Clicked
                    if self.time_status.index("Clicked") != status:
                        self.time_status = ["Inactive"] * 4
                        self.time_status[status] = "Clicked"
                        self.time_scale = ["A", "Y", "M", "W"][status]
                        self.initialize(redefine_data=False)
                elif self.time_status[status] != "Clicked":
                    self.time_status[status] = "Hovered"
            elif self.time_status[status] != "Clicked":
                self.time_status[status] = "Inactive"

        # Draws now updated object
        self.draw()

    # Draws object
    def draw(self):
        # Draws main ticker bar items
        self.window.blit(self.ticker_name, (450, 35))
        self.window.blit(self.tab_logo, (375, 38))
        self.window.blit(self.max_text, (920, 35))
        self.window.blit(self.mean_text, (755, 35))

        # Draws time scale buttons
        for i in range(len(self.time_status)):
            if self.time_status[i] == "Inactive":
                if i > 1:
                    self.window.blit(self.scale_letters[i][0], (1080 + i * 40, 35))
                else:
                    self.window.blit(self.scale_letters[i][0], (1100 + i * 30, 35))
            elif self.time_status[i] == "Hovered":
                if i > 1:
                    self.window.blit(self.scale_letters[i][1], (1080 + i * 40, 35))
                else:
                    self.window.blit(self.scale_letters[i][1], (1100 + i * 30, 35))
            elif self.time_status[i] == "Clicked":
                if i > 1:
                    self.window.blit(self.scale_letters[i][2], (1080 + i * 40, 35))
                else:
                    self.window.blit(self.scale_letters[i][2], (1100 + i * 30, 35))

        # Standardizes x scale
        x = [401 + ((822 / (len(self.ticker_df) - 1)) * i) for i in range(len(self.ticker_df))]
        x = list(map(int, x))

        # Draws line fill
        for segment in range(len(x) - 1):
            # Polygon --->
            pg.draw.polygon(self.window, (171, 237, 248), [(x[segment], 391 - int(self.fixed_ticker_df[segment])),
                                                           (x[segment], 391), (x[segment + 1], 391), (
                                                           x[segment + 1],
                                                           391 - int(self.fixed_ticker_df[segment + 1]))])  # <---

        # Draws grid
        self.window.blit(self.grid, (400, 99))

        # Draws line
        for segment in range(len(x)):
            if segment < len(x) - 1:
                # Line --->
                pg.draw.line(self.window, (42, 119, 166), (x[segment], 391 - int(self.fixed_ticker_df[segment])),
                             (x[segment + 1], 391 - int(self.fixed_ticker_df[segment + 1])), 7)  # <---
            pg.draw.circle(self.window, (42, 119, 166), (x[segment], 391 - int(self.fixed_ticker_df[segment])), 8)

        # Draws mean and max tags if selected. Specific order of draws is to ensure visibility
        if self.show_max:
            pg.draw.line(self.window, (65, 69, 72), (401, 391 - int(self.visual_max)),
                         (1223, 391 - int(self.visual_max)), 5)

        if self.show_mean:
            pg.draw.line(self.window, (37, 42, 45), (401, 391 - int(self.visual_mean)),
                         (1223, 391 - int(self.visual_mean)), 5)

        if self.show_max:
            self.window.blit(self.max_tag, (450, 371 - int(self.visual_max)))

        if self.show_mean:
            self.window.blit(self.mean_tag, (401, 371 - int(self.visual_mean)))

        # Draws max box button
        if self.show_max:
            if self.max_box_button_status != "Inactive":
                self.window.blit(self.checkboxes[3], (1020, 47))
            else:
                self.window.blit(self.checkboxes[2], (1020, 47))
        else:
            if self.max_box_button_status != "Inactive":
                self.window.blit(self.checkboxes[1], (1020, 47))
            else:
                self.window.blit(self.checkboxes[0], (1020, 47))

        # Draws mean box button
        if self.show_mean:
            if self.mean_box_button_status != "Inactive":
                self.window.blit(self.checkboxes[3], (880, 47))
            else:
                self.window.blit(self.checkboxes[2], (880, 47))
        else:
            if self.mean_box_button_status != "Inactive":
                self.window.blit(self.checkboxes[1], (880, 47))
            else:
                self.window.blit(self.checkboxes[0], (880, 47))

        # Draws the main ticker's info
        self.info.draw()
