# Danny Garcia
# update_files.py

# Imports
from sklearn.ensemble import VotingClassifier, RandomForestClassifier
from sklearn.model_selection import train_test_split as tts
from contextlib import redirect_stdout
from sklearn import svm, neighbors
from warnings import simplefilter
import pandas as pd
import numpy as np

# Ignore deprecation warnings for classifiers
simplefilter(action='ignore', category=FutureWarning)

# Main function
def up_predictions(profile, predictions_pannel):
	# Generate dataframe
	df = generate_data(profile.tickers)
	df.fillna(0, inplace=True)

	# Reset predictions
	profile.predictions = [[], [], []]
	profile.save_data()

	print("||>   Performing Predictions\n")

	# Predict every ticker one by one
	for file_num, ticker in enumerate(profile.tickers):

		print("Predicting {} - {}/{}".format(ticker, file_num + 1, len(profile.tickers), end="   "))

		ticker_df = df

		# Append future values, alter for different ammounts of time in prediction (Current: 5 Days - 1 Trading week)
		for i in range(1, 6):
			ticker_df[f"{ticker}_d{i}"] = (df[ticker].shift(-i) - ticker_df[ticker]) / ticker_df[ticker]

		ticker_df.fillna(0, inplace=True)

		# Gather features, classifier, and confidence Of current ticker
		x_in, y_out, ticker_df = gather_features(ticker_df, profile.tickers, ticker)
		classifier, confidence, latest_value = learn(x_in, y_out, ticker_df)

		confidence = round(confidence * 100, 2)

		latest_prediction = classifier.predict(latest_value.reshape(1, -1))

		# Print and save latest prediction
		print("Prediction: {} ({}) - Confidence: {}% - {:.02f}% Done".format(latest_prediction, \
		("Increase", "Neutral", "Decrease")[(1, 0, -1).index(latest_prediction)], confidence, \
		((file_num + 1) / len(profile.tickers)) * 100) + " " * (6 - len(ticker)))

		profile.predictions[(1, 0, -1).index(latest_prediction)].append([confidence, ticker])
		profile.save_data()

	# Sort predictions in order of accuracy (Highest to lowest)
	for i in range(3):
		profile.predictions[i].sort(reverse=True)
		profile.predictions[i] = profile.predictions[i][:9]
		for e in range(len(profile.predictions[i])):
			profile.predictions[i][e] = profile.predictions[i][e][1] + " - "  + str(profile.predictions[i][e][0]) + "%"

	profile.updating = False
	profile.save_data()

	predictions_pannel.prediction_index = 0
	predictions_pannel.prediction_type = "Increasing"
	predictions_pannel.prediction_batch = self.profile.predictions[0]

	print("\n||>   Predictions Terminated   |]")

# Generate input file
def generate_data(tickers):
	# Variables
	count = 1
	df = pd.DataFrame()

	print("||>   Generating Input File\n")

	for ticker in tickers:
		# Leave only closing Values
		df_temp = pd.read_csv(f"ticker_data/{ticker}.csv")
		df_temp.set_index("Date", inplace=True)
		df_temp.rename(columns={"Adj Close": ticker}, inplace=True)

		# Drop unnecessary columns
		df_temp.drop(["Open", "High", "Low", "Close", "Volume", f"{ticker}-15ma", \
		f"{ticker}-50ma", f"{ticker}-100ma", f"{ticker}-200ma"], 1, inplace=True)
		
		# Join ticker data to the right (AI uses aggregate closing prices to make decisions)
		if df.empty:
			df = df_temp
		else:
			df = df.join(df_temp, how="outer")

		# Print percentage
		if count % 10 == 0 and not count == len(tickers):
			print(f"Compiled {count}/{len(tickers)} Files" + " " * (4 - len(str(count))) + "({:.02f}%)".format(count / len(tickers) * 100))
		elif count == len(tickers):
			print("Compiled {}/{} Files (100.00%)".format(count, len(tickers)))

		count += 1

	print("\n||>   Input File Generated\n")

	return df

# Return the features needed to apply a ML algorithm
def gather_features(df, tickers, ticker):
	# For binary classification
	# df["{ticker}_target"] = list(map(prediction_metric_a, * [df[f"{ticker}_d{i}"] for i in range(1, 6)]))
	# For Trinary Classification
	df[f"{ticker}_target"] = list(map(prediction_metric_b, * [df[f"{ticker}_d{i}"] for i in range(1, 6)]))
	# For N-nary Classification
	# df["{ticker}_target"] = list(map(prediction_metric_c, * [df[f"{ticker}_d{i}"] for i in range(1, 6)]))
	
	# Fix invalid values
	df.fillna(0, inplace=True)
	df = df.replace([np.inf, -np.inf], np.nan)
	df.dropna(inplace=True)

	# Get values adjusted for size
	df_values = df[[ticker for ticker in tickers]].pct_change()

	# Fixe invalid values
	df_values = df_values.replace([np.inf, -np.inf], 0)
	df_values.fillna(0, inplace=True)

	# Featureset and labels
	x_in = df_values.values
	y_out = df[f"{ticker}_target"].values  # Future Predictions Created By Chosen Classification Type

	return x_in, y_out, df

# Train the model and eeturn classifier alongside confidence
def learn(x_in, y_out, df):
	# Split data into training and testing sets, adjust for different results
	x_train, x_test, y_train, y_test = tts(x_in, y_out, test_size=0.2)

	# Build voting classifier using: LinearSVC Classifier, KNeighbors Classifier, And Random Forrest Classifier 
	# To edit, always use odd number of classifiers (Only 5 Couses Noticeable Slowdowns, Alter With Coution)
	classifier = VotingClassifier([("lsvc", svm.LinearSVC()), ("knn", neighbors.KNeighborsClassifier()), \
	("rfor", RandomForestClassifier())])

	classifier.fit(x_train, y_train)
	confidence = classifier.score(x_test, y_test)

	return classifier, confidence, x_test[-1]

# Return binary classification: Higher precision, lower detail
def prediction_metric_a(*args):
	# Variables
	threshold = 0.01

	columns = [column for column in args]

	for column in columns:
		if column > threshold:
			return 1
	return 0

# Return trinary classification: Lower precision, higher detail
def prediction_metric_b(*args):
	# Variables (Adjust To Alter Risk)
	positive_threshold = 0.025
	negative_threshold = -0.02

	columns = [column for column in args]

	for column in columns:
		if column > positive_threshold:
			return 1
		if column < negative_threshold:
			return -1
	return 0

# Return n-nary classification: Lowest precision, highest detail (WARNING: Should not be used for other purposes
# other than testing, it's unreliable)
def prediction_metric_c(*args):
	# Variables
	threshold = 0.025

	columns = [column for column in args]

	for column in columns:
		if column > threshold:
			return int((column * 100) - 1)
		if column < -threshold:
			return int((column * 100) + 1)
	return 0
