# search_bar_class.py
# Danny Garcia

# Imports
from statistics import mean
from os import listdir
import pandas as pd
import pygame as pg


# Search bar class: Search bar for tickers. Used to add new tickers to profile tickers.
class SearchBar:
    def __init__(self, window):
        # Argument[s]
        self.window = window

        # General class properties
        self.ticker_color = "N/A"
        self.key_press = -2
        self.text = "SEARCH"
        self.frame = 0
        self.point = (-5, 115)
        self.first_key = True
        self.universal_click = False
        self.df = "N/A"
        self.formatted_df = "N/A"
        self.collection = []  # Initialization required

        # Status[es]
        self.status = "Inactive"
        self.key_status = "Unpressed"
        self.plus_status = "Inactive"

        # Surface[s]
        self.panel_search = [pg.image.load(f"visual_data/_panels/panel_search_{frame}.png") for frame in range(2)]
        self.search_bar = pg.image.load("visual_data/other/search_bar.png")
        self.plus_button = [pg.image.load(f"visual_data/_buttons/plus_{image}.png") for image in range(2)]

        # Font[s]
        self.open_sans_40 = pg.font.Font("visual_data/open_sans.ttf", 40)
        self.open_sans_25 = pg.font.Font("visual_data/open_sans.ttf", 25)

        # Render[s]
        self.text_render = self.open_sans_40.render(self.text, False, (86, 98, 100))
        self.name_render = "N/A"
        self.last_value_render = "N/A"

    # Updates search bar information
    def update(self):
        # Check that collections were initialized
        if len(self.collection) == 0:
            raise Exception("Collection must be initialized.")

        # Updates the current frame
        if self.status == "Active":
            self.frame += 1

        # Gets mouse position
        mouse_position = pg.mouse.get_pos()

        # Updates search bar status and resets frame count if clicked
        if 25 <= mouse_position[0] <= 312 and 24 <= mouse_position[1] <= 74:
            if self.universal_click and self.status == "Inactive":
                self.status = "Active"
                self.frame = 0
        else:
            if self.status == "Active" and self.universal_click:
                self.status = "Inactive"

        # Updates plus button status
        # Condition --->
        if (self.point[0] + 300 <= mouse_position[0] <= self.point[0] + 336 and self.point[1] + 10 <= mouse_position[1]
                <= self.point[1] + 45) and self.text + ".csv" in listdir("ticker_data"):  # <---
            if self.universal_click:
                # Current search text is not in collection
                if self.text not in [self.collection[i].ticker for i in range(len(self.collection))]:
                    for ticker in self.collection:
                        # Adds ticker to collection
                        if ticker.ticker == "N/A":
                            ticker.ticker = self.text
                            ticker.df, ticker.formatted_df = ticker.generate_df(ticker.ticker)
                            ticker.name_render = ticker.open_sans_25.render(ticker.ticker, False, (141, 163, 167))
                            ticker.profile.profile_tickers[f"ticker_{ticker.id}"] = self.text
                            ticker.profile.save_data()
                            break
            else:
                self.plus_status = "Hovered"
        else:
            self.plus_status = "Inactive"

        # Key pressed
        if self.key_press != -1 and self.status == "Active":
            # Resets text if it's the first keypress
            if self.first_key:
                self.text = ""
                self.first_key = False
            # Backslash
            if self.key_press == pg.K_BACKSPACE:
                self.text = self.text[:-1]
            # Letter
            elif 65 <= self.key_press <= 90 or 97 <= self.key_press <= 122:
                if self.open_sans_40.size(self.text + chr(self.key_press).upper())[0] < 190:
                    self.text = self.text + chr(self.key_press).upper()
            self.key_press = -1

            # Renders ticker name
            self.text_render = self.open_sans_40.render(self.text, False, (86, 98, 100))

            # Render df if in csv files
            if self.text + ".csv" in listdir("ticker_data"):
                self.df, self.formatted_df = self.generate_df(self.text)
                self.name_render = self.open_sans_25.render(self.text, False, (141, 163, 167))
                self.last_value_render = self.open_sans_25.render("{:.5}".format(self.df[-1]), False, (141, 163, 167))
            else:
                self.formatted_df = "N/A"

        # Draws now updated object
        self.draw()

    # Draws search bar and result if applicable
    def draw(self):
        if self.formatted_df != "N/A":
            # Draws base
            pg.draw.rect(self.window, (141, 163, 167), (18, 89, 160, 100))

            # Draws line
            for segment in range(len(self.formatted_df) - 1):
                # Polygon --->
                pg.draw.polygon(self.window,
                                [(124, 218, 124), (208, 99, 106)][["Green", "Red"].index(self.ticker_color)],
                                [(19 + int((segment * 8.2)), 235 - int(self.formatted_df[segment])),
                                 (19 + int((segment * 8.2)), 185), (19 + (int((segment + 1) * 8.2)), 185),
                                 (19 + (int((segment + 1) * 8.2)),
                                  235 - int(self.formatted_df[segment + 1]))])  # <---
                # Line --->
                pg.draw.line(self.window, [(36, 162, 36), (246, 35, 50)][["Green", "Red"].index(self.ticker_color)],
                             (19 + int((segment * 8.2)), 235 - int(self.formatted_df[segment])),
                             (19 + (int((segment + 1) * 8.2)), 235 - int(self.formatted_df[segment + 1])),
                             8)  # <---

            # Draws panel and info
            self.window.blit(self.panel_search[1], (0, 0))
            self.window.blit(self.name_render, (185, 105))
            self.window.blit(self.last_value_render, (185, 135))
        else:
            # Draws panel
            self.window.blit(self.panel_search[0], (0, 0))

        # Draws search bar and text in it
        self.window.blit(self.search_bar, (25, 24))
        self.window.blit(self.text_render, (95, 21))

        # Draws plus button if applicable
        if self.plus_status == "Inactive" and self.text + ".csv" in listdir("ticker_data"):
            self.window.blit(self.plus_button[0], (self.point[0] + 300, self.point[1] + 10))
        elif self.plus_status == "Hovered" and self.text + ".csv" in listdir("ticker_data"):
            self.window.blit(self.plus_button[1], (self.point[0] + 300, self.point[1] + 10))

        if self.status == "Active":
            if (self.frame % 12) < 7:
                # Line --->
                pg.draw.line(self.window, (86, 98, 100), (100 + self.open_sans_40.size(self.text)[0], 33),
                             (100 + self.open_sans_40.size(self.text)[0], 65), 4)  # <---

    # Generates data frame displayed
    def generate_df(self, ticker):
        # Loads ticker data frame
        df = pd.read_csv(f"ticker_data/{ticker}.csv")
        df = df.iloc[range(len(df.index) - 20, len(df.index)), [4]]
        df = df["Close"].tolist()

        formatted_df = df.copy()

        # Selects color for line
        if df[-1] > mean(df):
            self.ticker_color = "Green"
        else:
            self.ticker_color = "Red"

        # Generates multiplication and reduction factors to manipulate line position and size
        multiplication_factor = 200 / max(df)

        # Applies multiplication and reduction factors
        for value in range(len(formatted_df)):
            formatted_df[value] *= multiplication_factor

        reduction_factor = min(formatted_df) // 2

        for value in range(len(formatted_df)):
            formatted_df[value] -= reduction_factor

        # Renders ticker's last value
        self.last_value_render = self.open_sans_25.render("{:.5}".format(df[-1]), False, (141, 163, 167))

        return df, formatted_df
