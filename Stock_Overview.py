import requests
import csv

api_key = input("Enter your Alpha Vantage API key: ")

symbols = []
data_dict = {}

while True:
  symbol = input("Enter a stock symbol and press enter (or 'q' to quit): ")
  if symbol == 'q':
    break

  symbols.append(symbol)
  url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={api_key}'
  r = requests.get(url)
  data = r.json()

  for key, value in data.items():
    if key not in data_dict:
      data_dict[key] = {}
    data_dict[key][symbol] = value

# write all the data to a single CSV file
filename = "_".join(symbols) + "_Overview.csv"
with open(filename, "w", newline="") as f:
  writer = csv.DictWriter(f, fieldnames=["Attribute"] + symbols)
  writer.writeheader()
  for key, values in data_dict.items():
    row = {"Attribute": key}
    for symbol in symbols:
      row[symbol] = values.get(symbol, "")
    writer.writerow(row)

print(f"Data written to {filename}")
