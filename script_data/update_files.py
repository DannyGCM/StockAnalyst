# Danny Garcia
# update_files.py

# Imports
import pandas_datareader.data as web
import datetime as dt
import requests
import bs4

# Main function
def up_files(profile):
	gather_tickers(profile)
	download_ticker_data(profile)

# Gather tickers
def gather_tickers(profile):
	# Fill profile ticker arraey from wikipedia
	if not profile.tickers:
		request = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
		soup = bs4.BeautifulSoup(request.text, "lxml")
		table = soup.find("table", {"class":"wikitable sortable"})
		
		tickers = []

		for row in table.findAll("tr")[1:]: # Starts from 1 to skip headers
			ticker = row.findAll("td")[0].text[:-1]
			if not ("." in ticker):
				tickers.append(ticker)
				profile.last_update_dates[tickers[-1]] = [2000, 1, 1]

		profile.tickers = tickers
		profile.save_data()

# Download company data for all outdated tickers (1 Day)
def download_ticker_data(profile):
	# Variables
	num_files = 1
	success_counter = 0

	print("||>   Gathering CSV Files\n")

	# Download company data
	for ticker in profile.tickers:
		if profile.last_update_dates[ticker] != [dt.datetime.now().year, dt.datetime.now().month, dt.datetime.now().day]:
			# Completion percentage
			if (num_files / len(profile.tickers)) * 100 > 0:
				print("Collecting {} ({}/{} - {:.02f}%)".format(ticker, num_files, len(profile.tickers), \
				(num_files / len(profile.tickers)) * 100) + " " * (6 - len(ticker)), end="   ")
			else:
				print("Collecting {} ({}/{} - 100.00%)".format(ticker, num_files, len(profile.tickers), end="   "))

            # Gather data from yahoo
			try:
				df = web.DataReader(ticker, "yahoo", dt.datetime(2000, 1, 1), dt.datetime.now())
				# Add moving averages
				df[f"{ticker}-15ma"] = df["Adj Close"].rolling(window=15, min_periods=0).mean()
				df[f"{ticker}-50ma"] = df["Adj Close"].rolling(window=50, min_periods=0).mean()
				df[f"{ticker}-100ma"] = df["Adj Close"].rolling(window=100, min_periods=0).mean()
				df[f"{ticker}-200ma"] = df["Adj Close"].rolling(window=200, min_periods=0).mean()
                
                # Save finalized file
				df.to_csv(f"ticker_data/{ticker}.csv")

				# Update last update information
				profile.last_update_dates[ticker] = [dt.datetime.now().year, dt.datetime.now().month, dt.datetime.now().day]
				profile.save_data()

				success_counter += 1
				print("SUCCESS")
			# Show errors and erases problematic tickers
			except Exception as error:
				print(f"ERROR: {error}")
				del profile.tickers[profile.tickers.index(ticker)]
				profile.save_data()
		else:
			print(f"Ticker {ticker}" + " " * (6 - len(ticker)) + "Is Up To Date")

		num_files += 1

	print(f"\n||>   Gathered {success_counter} Files\n")
