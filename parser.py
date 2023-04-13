import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

flat_data = {}
flat_data["description"] = []
flat_data["price"] = []
flat_data["location"] = []
flat_data["date"] = []
flat_data["area"] = []

for i in range(1, 26):
  url = f"https://www.olx.ua/d/uk/nedvizhimost/kvartiry/kiev/?currency=UAH&page={i}&search%5Bfilter_enum_number_of_rooms_string%5D%5B0%5D=dvuhkomnatnye&search%5Bfilter_float_price%3Ato%5D=8000"
  raw_data = requests.get(url)
  soup = BeautifulSoup(raw_data.text, "html.parser")
  flats = soup.find_all(True, {"class": ["css-qfzx1y"]})
  for flat in flats:
    flat_data["description"].append(flat.select("h6")[0].get_text().strip())
    flat_data["price"].append(flat.find("p", class_="css-10b0gli er34gjf0").get_text().strip())
    flat_data["location"].append(flat.find("p", class_="css-veheph er34gjf0").get_text().split("-")[0].strip())
    flat_data["date"].append(flat.find("p", class_="css-veheph er34gjf0").get_text().split("-")[1].strip())
    flat_data["area"].append(flat.find("span", class_="css-643j0o").get_text().strip())

kyiv_flats = pd.DataFrame(flat_data)
kyiv_flats["price"] = (kyiv_flats["price"].str[0:5].str.replace(" ", "")).astype(int)
kyiv_flats["area"] = (kyiv_flats["area"].str[0:-3]).astype(float)
kyiv_flats["location"] = kyiv_flats["location"].str[5:].str.strip()
kyiv_flats.to_csv("/content/sample_data/kyiv_flats.csv")
