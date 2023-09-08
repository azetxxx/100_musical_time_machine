from bs4 import BeautifulSoup
import datetime as dt
import requests


today = dt.date.today()
date_today = today.strftime("%Y-%m-%d")


def is_date_format_valid(date_input):
    if len(date_input) != 10 or \
        date_input[4] and date_input [7] != "-" or \
        date_input.replace("-", "").isdigit() == False:
            print("\n❌ The input is invalid. Use the required date format! \n")
            return False

    input_year = int(date_input[:4])
    input_month = int(date_input[5:7])
    input_day = int(date_input[8:])
    if dt.date(input_year, input_month, input_day) > today:
        print("\n❌ The picked date is a day in the future. Try again! \n")
        return False
    else:
        return True


date_valid = False

while not date_valid:
    picked_date = input("📅 Pick a date in the past for time traveling! \
        \nHint: Use the following format (YYYY-MM-DD) ➡️ ")
    date_valid = is_date_format_valid(picked_date)

print(f"\n✅ Picked date: {picked_date}\n")

base_url = 'https://www.billboard.com/charts/hot-100/'
response = requests.get(base_url + picked_date)
chart_page = response.text

soup = BeautifulSoup(chart_page, 'html.parser')

print(soup.title)

song_titles = soup.select(selector='div.o-chart-results-list-row-container ul li:nth-of-type(4) ul li:first-of-type span')

for song in song_titles:
    for string in song.stripped_strings:
        print(string)
