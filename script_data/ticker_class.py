# ticker_class.py
# Danny Garcia

# Imports
from statistics import mean
import pandas as pd
import pygame as pg


# Ticker class: Ticker container. Has basic information and can be set to main.
class Ticker:
    def __init__(self, window, profile, point, main_ticker, id_):
        # Argument[s]
        self.window = window
        self.profile = profile
        self.point = point
        self.main_ticker = main_ticker
        self.id = id_

        # General class properties
        self.active = False
        self.ticker = self.profile.profile_tickers[f"ticker_{self.id}"]
        self.ticker_color = "N/A"
        self.main_ticker.ticker = self.ticker
        self.universal_click = False
        self.collection = []  # Initialization required
        
        # Status[es]
        self.cross_status = "Inactive"
        self.status = "Inactive"

        # Surface[s]
        self.empty_watermark = pg.image.load("visual_data/other/empty_watermark.png")
        self.cross_button = [pg.image.load(f"visual_data/_buttons/cross_{image}.png") for image in range(2)]
        if self.id % 2 != 0:
            self.panels = [pg.image.load(f"visual_data/_panels/panel_light_{image}.png") for image in range(3)]
        else:
            self.panels = [pg.image.load(f"visual_data/_panels/panel_dark_{image}.png") for image in range(3)]

        # Font[s]
        self.open_sans_25 = pg.font.Font("visual_data/open_sans.ttf", 25)

        # Render[s]
        self.last_value_render = "N/A"
        if self.ticker != "N/A":
            self.df, self.formatted_df = self.generate_df(self.ticker)
            self.name_render = self.open_sans_25.render(self.ticker, False, (141, 163, 167))

    # Updates information
    def update(self):
        # Gets mouse position
        mouse_position = pg.mouse.get_pos()

        # Updates ticker status
        # Condition --->
        if (self.point[0] <= mouse_position[0] <= self.point[0] + 330 and
            self.point[1] <= mouse_position[1] <= self.point[1] + 123) and \
            not (self.point[0] + 300 <= mouse_position[0] <= self.point[0] + 326 and
                 self.point[1] + 10 <= mouse_position[1] <= self.point[1] + 37):  # <---
            if self.universal_click:  # Clicked
                self.status = "Clicked"
                if self.ticker != "N/A":  # Ticker isn't empty
                    # Make ticker main
                    for ticker in self.collection:
                        if ticker.active:
                            ticker.active = False
                    # Update and initialize values
                    self.active = True
                    self.main_ticker.ticker = self.ticker
                    self.main_ticker.initialize()
        else:
            self.status = "Inactive"

        # Updates cross button status
        # Condition --->
        if (self.point[0] + 300 <= mouse_position[0] <= self.point[0] + 326 and self.point[1] + 10 <= mouse_position[1]
                <= self.point[1] + 37):  # <---
            if self.universal_click:  # Clicked
                # Ticker is main and there are more than one ticker
                if self.active and [self.collection[i].ticker for i in range(len(self.collection))].count("N/A") < 3:
                    # Change ticker main status and save data
                    self.active = False
                    self.ticker = "N/A"
                    self.profile.profile_tickers[f"ticker_{self.id}"] = "N/A"
                    self.profile.save_data()

                    # Select new main ticker
                    for ticker in self.collection:
                        if ticker.ticker != "N/A":
                            ticker.active = True
                            self.main_ticker.ticker = ticker.ticker
                            self.main_ticker.initialize()
                            break
                # Condition --->
                # Ticker isn't main
                elif not self.active and [self.collection[i].ticker for i in
                                          range(len(self.collection))].count("N/A") < 3:  # <---
                    # Erase ticker and save data
                    self.ticker = "N/A"
                    self.profile.profile_tickers[f"ticker_{self.id}"] = "N/A"
                    self.profile.save_data()
            else:
                self.cross_status = "Hovered"
        else:
            self.cross_status = "Inactive"

        # Draws now updated object
        self.draw()

    # Draws object
    def draw(self):
        # Draws based on ticker's main status
        if self.active:  # Ticker is main ticker
            # Draws line
            self.draw_line()

            # Draws panel
            self.window.blit(self.panels[2], self.point)

            # Draws info
            self.draw_info()

            # Draws cross button
            if self.cross_status == "Inactive":
                self.window.blit(self.cross_button[0], (self.point[0] + 300, self.point[1] + 10))
            else:
                self.window.blit(self.cross_button[1], (self.point[0] + 300, self.point[1] + 10))
        else:  # Ticker isn't main ticker
            if self.ticker != "N/A":
                # Draws line
                self.draw_line()

                # Draws panel
                if self.status in ["Inactive", "Clicked"]:
                    self.window.blit(self.panels[1], self.point)

                # Draws info
                self.draw_info()

                # Draws cross button
                if self.cross_status == "Inactive":
                    self.window.blit(self.cross_button[0], (self.point[0] + 300, self.point[1] + 10))
                else:
                    self.window.blit(self.cross_button[1], (self.point[0] + 300, self.point[1] + 10))
            else:  # No ticker
                # Draws panel
                self.window.blit(self.panels[0], self.point)

                # Draws empty watermark
                self.window.blit(self.empty_watermark, (self.point[0] + 98, self.point[1] + 35))

    # Draws ticker's preview line
    def draw_line(self):
        # Background
        pg.draw.rect(self.window, (141, 163, 167), (self.point[0] + 10, self.point[1] + 10, 160, 100))

        # Line
        for segment in range(len(self.formatted_df) - 1):
            # Draws line fill
            # Polygon --->
            pg.draw.polygon(self.window, [(124, 218, 124), (208, 99, 106)][["Green", "Red"].index(self.ticker_color)], [
                (self.point[0] + 13 + int((segment * 8.2)), self.point[1] + 160 - int(self.formatted_df[segment])),
                (self.point[0] + 13 + int((segment * 8.2)), self.point[1] + 110),
                (self.point[0] + 13 + (int((segment + 1) * 8.2)), self.point[1] + 110),
                (self.point[0] + 13 + (int((segment + 1) * 8.2)),
                 self.point[1] + 160 - int(self.formatted_df[segment + 1]))])  # <---
            # Draws line
            # Line --->
            pg.draw.line(self.window, [(36, 162, 36), (246, 35, 50)][["Green", "Red"].index(self.ticker_color)], (
                self.point[0] + 13 + int((segment * 8.2)), self.point[1] + 160 - int(self.formatted_df[segment])), (
                self.point[0] + 13 + (int((segment + 1) * 8.2)),
                self.point[1] + 160 - int(self.formatted_df[segment + 1])), 8)  # <---

    # Draws name of ticker and its last value
    def draw_info(self):
        self.window.blit(self.name_render, (self.point[0] + 179, self.point[1] + 30))
        self.window.blit(self.last_value_render, (self.point[0] + 179, self.point[1] + 60))

    # Generates data frame to be displayed
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
