# Danny Garcia
# main_info_class.py

# Imports
import pygame as pg
import threading
import requests
import bs4


# Main info class: Gathers and displays main ticker's information.
class MainInfo:
    def __init__(self, window, main_ticker):
        # Argument[s]
        self.window = window
        self.main_ticker = main_ticker

        # General class properties
        self.data = "N/A"
        self.thread = "N/A"

        # Font[s]
        self.open_sans_40 = pg.font.Font("visual_data/open_sans.ttf", 40)
        self.open_sans_20_bold = pg.font.Font("visual_data/open_sans_bold.ttf", 20)

        # Render[s]
        self.loading_text = self.open_sans_40.render("Loading data...", False, (42, 119, 166))
        self.loaded_text = []

    def fetch_info(self):
        # Resets relevant information
        self.data = "N/A"
        self.thread = threading.Thread(target=thread, args=(self,))
        self.thread.start()

    # Draws object
    def draw(self):
        # Data isn't ready
        if self.data == "N/A":
            self.window.blit(self.loading_text, (500, 555))
        else:
            # Draws text
            for line in range(len(self.loaded_text)):
                self.window.blit(self.loaded_text[line][0], (380, 474 + line * 19))
                # Text --->
                self.window.blit(self.loaded_text[line][1],
                                 (890 - self.loaded_text[line][1].get_width(),
                                  474 + line * 19))  # <---


# Outside object to make threading possible
def thread(self):
    # Used to identify thread change
    ticker = self.main_ticker.ticker

    # Container for finalized data
    data = []

    # Gets source code
    request = requests.get(f"https://finance.yahoo.com/quote/{ticker}/")
    soup = bs4.BeautifulSoup(request.text, "lxml")

    # Info is split into two tables
    table_a = soup.find("table", {"class": "W(100%)"})
    table_b = soup.find("table", {"class": "W(100%) M(0) Bdcl(c)"})

    # Find rows in table a
    for row in table_a.findAll("tr"):
        data.append([row.findAll("td")[0].text, row.findAll("td")[1].text])

    # Find rows in table b
    for row in table_b.findAll("tr"):
        data.append([row.findAll("td")[0].text, row.findAll("td")[1].text])

    # Selects relevant information
    data = data[:8] + data[13:]

    # If thread hasn't been changed
    if self.main_ticker.ticker == ticker:
        # Resets text data
        self.loaded_text = []

        # Renders data
        for line in range(len(data)):
            self.loaded_text.append([self.open_sans_20_bold.render(data[line][0], False, (42, 119, 166)),
                                     self.open_sans_20_bold.render(data[line][1], False, (42, 119, 166))])

        # Saves data
        self.data = data
