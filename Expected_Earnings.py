import requests
import csv

api_key = input("Enter your Alpha Vantage API key: ")

symbols = []
while True:
    symbol = input("Enter a stock symbol and press enter (or 'q' to finish): ")
    if symbol == 'q':
        break
    symbols.append(symbol)

all_data = []

for symbol in symbols:
    url = f'https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&symbol={symbol}&horizon=3month&apikey={api_key}'

    with requests.Session() as s:
        download = s.get(url)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        all_data.extend(my_list)
        all_data.append([])

# write the combined data to a CSV file
filename = "_".join([symbol.replace(" ", "_") for symbol in symbols]) + "_earnings_calendar.csv"
with open(filename, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(all_data)

print(f"Data written to {filename}")
