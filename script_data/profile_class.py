# profile_class.py
# Danny Garcia

# Imports
from os import listdir
import pickle


# Profile class: Manages user's data
# noinspection PyArgumentList
class Profile:
    def __init__(self, data):
        # Generate/Grab profile information
        if data in listdir():  # File found - load data
            # Opens file
            file = open(data, "rb")

            # Loads saved data
            self.profile_tickers = pickle.load(file)
            self.company_settings = pickle.load(file)
            self.last_update_dates = pickle.load(file)
            self.tickers = pickle.load(file)
            self.predictions = pickle.load(file)
            self.updating = pickle.load(file)

            # Closes file
            file.close()
        else:  # File not found - generate data
            # Generates default data
            # Values --->
            self.profile_tickers, self.company_settings, self.last_update_dates, \
            self.tickers, self.predictions, self.updating = self.initialize_data()  # <---

            # Saves file
            self.save_data()

    # Saves profile's data
    def save_data(self):
        # Opens file
        file = open("profile.stock", "wb")

        # Dumps data in profile file
        pickle.dump(self.profile_tickers, file)
        pickle.dump(self.company_settings, file)
        pickle.dump(self.last_update_dates, file)
        pickle.dump(self.tickers, file)
        pickle.dump(self.predictions, file)
        pickle.dump(self.updating, file)

        # Closes file
        file.close()

    # Returns default data values
    @staticmethod
    def initialize_data():
        # Ticker list
        profile_tickers = {"ticker_1": "GOOGL", "ticker_2": "NFLX",
                           "ticker_3": "AAPL", "ticker_4": "N/A"}

        # Main ticker saved settings
        company_settings = {"time_scale": "A", "show_max": True, "show_mean": False}

        # Last update date for individual tickers: Used in update
        last_update_dates = {}

        # List of ticker names in S&P 500
        tickers = []

        # Most confident predictions for week after update (Increase|Neutral|Decrease)
        # WARNING: Does not take into account anything other than relationship between prices
        # across all companies listed in tickers. Always do research and buy responsibly.
        predictions = [["N/A"] * 9] * 3  # List with 3 lists of length 9

        # Boolean value which triggers an update
        updating = True

        return profile_tickers, company_settings, last_update_dates, tickers, predictions, updating
